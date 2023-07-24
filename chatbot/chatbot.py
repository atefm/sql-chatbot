import psycopg2
import os
import openai

class Chatbot:
    def __init__(self):
        user = os.getenv('POSTGRES_USER')
        password = os.getenv('POSTGRES_PASSWORD')
        dbname = os.getenv('POSTGRES_DB')
        host = os.getenv('POSTGRES_HOST')
        port = os.getenv('POSTGRES_PORT')

        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

        self.cur = self.conn.cursor()
        openai.api_key = os.getenv('OPENAI_API_KEY')

    def get_table_information(self, table_name):

        columns_info = ""
        self.cur.execute("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = %s
            """, (table_name,))
        for row in self.cur.fetchall():
            column_name, data_type, is_nullable = row
            columns_info += f"{column_name} ({data_type})"
            if is_nullable == 'NO':
                columns_info += " NOT NULL"
            columns_info += "\n"

        # Get constraint information
        constraints_info = ""
        self.cur.execute("""
                SELECT constraint_name, constraint_type
                FROM information_schema.table_constraints
                WHERE table_name = %s
            """, (table_name,))
        for row in self.cur.fetchall():
            constraint_name, constraint_type = row
            constraints_info += f"{constraint_name}: {constraint_type}\n"

        # Get primary key information
        primary_key_info = ""
        self.cur.execute("""
                SELECT column_name
                FROM information_schema.key_column_usage
                WHERE constraint_name = (
                    SELECT constraint_name
                    FROM information_schema.table_constraints
                    WHERE table_name = %s AND constraint_type = 'PRIMARY KEY'
                )
            """, (table_name,))
        for row in self.cur.fetchall():
            column_name = row[0]
            primary_key_info += f"Primary Key: {column_name}\n"

        # Get sample data
        sample_data = ""
        self.cur.execute(f"SELECT * FROM {table_name} LIMIT 100")
        for row in self.cur.fetchall():
            sample_data += ', '.join(str(cell) for cell in row) + "\n"


        # Build the final information string
        table_information = f"Table: {table_name}\n\n"
        table_information += "Columns:\n" + columns_info + "\n"
        table_information += "Constraints:\n" + constraints_info + "\n"
        table_information += "Primary Key:\n" + primary_key_info + "\n"
        table_information += "Sample Data:\n" + sample_data + "\n"


        return table_information

    def get_table_information_for_all_tables(self):

        self.cur.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
            """)
        table_names = [row[0] for row in self.cur.fetchall()]

        all_table_information = ""

        # Loop through each table and fetch its information
        for table_name in table_names:
            table_information = self.get_table_information(table_name)
            all_table_information += table_information
            all_table_information += "\n\n"

        return all_table_information

    def generate_prompt(self, user_prompt, top_k=5):

        db_tables_info = self.get_table_information_for_all_tables()


        prompt = f"You are a PostgreSQL expert. Your task is to answer questions related to the given input: '{user_prompt}' " \
                 f"by creating syntactically correct PostgreSQL queries. Follow these guidelines to ensure consistency " \
                 f"and accuracy in your responses:\n\n" \
                 f"1. Create a query that retrieves the necessary data to answer the question. Use the LIMIT clause to return " \
                 f"at most {top_k} results, unless a specific number of examples is requested in the question.\n" \
                 f"2. When querying tables, only request the columns needed to answer the question. Wrap each column name in " \
                 f"double quotes (\") to denote them as delimited identifiers.\n" \
                 f"3. Avoid querying for columns that do not exist in the tables provided. Pay attention to which column is in " \
                 f"which table.\n" \
                 f"4. Thoroughly check whether the questions asked can be answered using the tables provided below. If" \
                 f"not then say 'I don't understand'.\n" \
                 f"5. DO NOT generate any statements that modify the tables (e.g., INSERT, UPDATE, DELETE, DROP). If such " \
                 f"operations are attempted, respond with 'This operation is not permitted'.\n" \
                 f"6. If the question is not related to the provided tables below or cannot be understood, respond with " \
                 f"'I don't understand'.\n" \
                 f"Please follow this format when responding:\n\n" \
                 f"Input: {user_prompt}\nQuery: SQL Query to run. Say 'I don't understand' if the Question is blank or not " \
                 f"understood. Say 'This operation is not permitted' if point 6 or 3 is raised.\nResult: Result of the Query. " \
                 f"Say 'I don't understand' if the Question is blank or not " \
                 f"understood. Say 'This operation is not permitted' if point 5 is raised.\n\n" \
                 f"Only use the following tables:\n{db_tables_info}\n\n" \
                 f"Question: {user_prompt}"

        return prompt

    def generate_sql_from_user_prompt(self, user_prompt):

        if user_prompt == "":
            return "I don't understand."

        prompt = self.generate_prompt(user_prompt)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user",
                 "content": user_prompt}
            ],
            temperature=0.2

        )

        #TODO: Test the crap out of this because this is super unreliable.
        return response['choices'][0]['message']['content']

    def execute_sql_and_return_response(self, sql):
        # This is not reliable at all as there are a number of actions that need to be performed before a query can be executed.

        try:
            self.cur.execute(sql)

            # Fetch all the rows
            rows = self.cur.fetchall()

            # Return the DataFrame
            return rows
        except Exception as e:
            return e

    def close(self):
        # Close the cursor and the connection
        self.cur.close()
        self.conn.close()

