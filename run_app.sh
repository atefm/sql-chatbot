#!/bin/sh

# Run uvicorn in the background
uvicorn main:app --host 0.0.0.0 --port 8080 &

# Save the process ID of uvicorn
uvicorn_pid=$!

# Run the tests
python -m unittest test_chatbot.py

# Wait for uvicorn to finish (optional, you can remove this line if not needed)
wait $uvicorn_pid