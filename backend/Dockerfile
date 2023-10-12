# Use a Python base image suitable for your Flask app
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt ./

# Install project dependencies using pip
RUN pip install -r requirements.txt

# Copy the entire src directory to the container
COPY src/ ./src/

# Expose the port on which your Flask app will run (usually 5000)
EXPOSE 5000

# Start the Flask app from the src directory
CMD ["sh", "-c", "cd src && flask run --debug --host=0.0.0.0 --port=5001"]
