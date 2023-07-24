# Use an official Python 3.10 runtime as a parent image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

# Set the working directory in the container to /app
WORKDIR /app/chatbot

# Install system-level dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc

# Copy the current directory contents into the container at /app
ADD . /app

# Change the working directory to /app/chatbot where the Python scripts are
# WORKDIR /app/chatbot

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r ../requirements.txt

# Make port available to the world outside this container
EXPOSE 8080


# RUN echo "#!/bin/sh\n\
# uvicorn main:app --host 0.0.0.0 --port 8080 &\n\
# python -m unittest test_chatbot.py" > run_app.sh

# Make the shell script executable
RUN chmod +x /app/run_app.sh

# Set the entrypoint to run the shell script when the container starts
ENTRYPOINT ["/app/run_app.sh"]