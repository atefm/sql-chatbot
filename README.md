# SQL Chatbot with FastAPI and OpenAI

This project contains a SQL chatbot that uses OpenAI's to generate SQL queries based on user prompts and execute them on a PostgreSQL database. 
It allows users to interact with the chatbot through a FastAPI web interface, where they can input questions related to the database.

## Design and Development Decisions

- The project is built using FastAPI making it user-friendly and suitable for real-time chatbot interactions.
- The SQL Chatbot utilizes OpenAI's language model to understand and process natural language queries.
- The PostgreSQL database is used for data storage, and the prompt is created to query specific columns to optimize performance and avoid unnecessary data retrieval.

## Prerequisites

- Docker installed on your system.

## Installation and Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/sql-chatbot.git
cd sql-chatbot
```

2. Set up your OpenAI API key:
   - Insert your OpenAI API key in the `.env` file:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

To run the SQL Chatbot application, simply use `docker-compose`:
```bash
docker-compose up --build
```

This will build the Docker image and start the FastAPI web server and PostgreSQL database. The database will be auto populated 
with random data. 

Access the chatbot web interface at `http://localhost:8080` or the appropriate server address.

The chatbot will prompt you to input a question related to the database.

Enter your question, and the chatbot will generate a corresponding PostgreSQL query.

The chatbot will display the results of the query as an answer to your question if applicable.

## Example Questions

1. "How many orders were placed today?"
2. "Show me the top 5 most expensive products."
3. "Get the names of customers from their emails."
4. "What is the total revenue from orders in the past week?"
5. "Which products are out of stock?"


## Unit Testing

The SQL Chatbot includes some basic unit testing to ensure the functionality of SQL generation component. To run the unit tests, use the following command:

python -m unittest test_chatbot.py

The unit tests cover various scenarios and edge cases to validate the chatbot's behavior, ensuring it handles different types of user queries and provides accurate responses.


## Limitations and TODO
1. The execution of the query has been intentionally left out as there are quite a few checks need to be performed before the query can be executed on the actual DB.
2. Better input/output handling.
3. Handling of maximum tokens limitation with OpenAI especially when dealing with multiple tables.
4. Ensure deterministic output with smaller with multiple but smaller prompts and validation thereof.