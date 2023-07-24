import unittest
from chatbot import Chatbot


class MyTestResult(unittest.TextTestResult):
    def addError(self, test, err):
        super().addError(test, err)
        print(f"Error occurred in: {test}")
        print(f"Error message: {err}")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        print(f"Assertion failed in: {test}")
        print(f"Failure message: {err}")

class TestChatbot(unittest.TestCase):
    def setUp(self):
        # Initialize the Chatbot for each test case
        self.chatbot = Chatbot()

    def tearDown(self):
        # Close the Chatbot's connections after each test case
        self.chatbot.close()

    def test_generate_sql_from_user_prompt_valid(self):
        # Test a valid SQL generation with a user prompt
        user_prompt = "How many orders were placed today?"
        sql_query = self.chatbot.generate_sql_from_user_prompt(user_prompt)
        self.assertTrue(sql_query)  # Ensure the generated SQL query is not empty
        self.assertIn("SELECT", sql_query)  # Ensure the SQL query starts with "SELECT"

    def test_generate_sql_from_user_prompt_unknown_question(self):
        # Test handling an unknown question with "I don't understand" response
        user_prompt = "What is the meaning of life?"
        sql_query = self.chatbot.generate_sql_from_user_prompt(user_prompt)
        self.assertIn("I don't understand", sql_query)

    def test_generate_sql_from_user_prompt_invalid_question(self):
        # Test handling an invalid question with "I don't understand" response
        user_prompt = "Drop all tables!"
        sql_query = self.chatbot.generate_sql_from_user_prompt(user_prompt)
        self.assertIn("operation is not permitted", sql_query)

    def test_generate_sql_from_user_prompt_empty_prompt(self):
        # Test handling an empty user prompt with "I don't understand" response
        user_prompt = ""
        sql_query = self.chatbot.generate_sql_from_user_prompt(user_prompt)
        self.assertIn("I don't understand", sql_query)

    def test_generate_sql_from_user_prompt_specific_number_of_examples(self):
        # Test a user prompt requesting a specific number of examples
        user_prompt = "Show me the top 5 most expensive products."
        sql_query = self.chatbot.generate_sql_from_user_prompt(user_prompt)
        self.assertTrue(sql_query)  # Ensure the generated SQL query is not empty
        self.assertIn("LIMIT 5", sql_query)  # Ensure the SQL query includes LIMIT 5

    def test_generate_sql_from_user_prompt_non_existent_column(self):
        # Test a user prompt with a non-existent column in the query
        user_prompt = "Get the names of customers from their emails."
        sql_query = self.chatbot.generate_sql_from_user_prompt(user_prompt)
        self.assertIn("I don't understand", sql_query)  # The column doesn't exist, expect 'I don't understand'

    def test_generate_sql_from_user_prompt_date_related_question(self):
        # Test a user prompt involving the current date
        user_prompt = "Show me all orders placed today."
        sql_query = self.chatbot.generate_sql_from_user_prompt(user_prompt)
        self.assertTrue(sql_query)  # Ensure the generated SQL query is not empty
        self.assertIn("CURRENT_DATE", sql_query)



def custom_suite():
    suite = unittest.TestSuite()
    test_loader = unittest.TestLoader()
    test_names = test_loader.getTestCaseNames(TestChatbot)
    for name in test_names:
        suite.addTest(TestChatbot(name))
    return suite

if __name__ == '__main__':
    test_runner = unittest.TextTestRunner(resultclass=MyTestResult, verbosity=2)
    try:
        result = test_runner.run(custom_suite(), exit=False)
    except SystemExit:
        pass

    if not result.wasSuccessful():
        exit(0)

