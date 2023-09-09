# Use a Python base image suitable for your Flask app
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files to the container
COPY pyproject.toml poetry.lock ./

# Install Poetry and project dependencies
RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Copy the entire src directory to the container
COPY src/ ./

# Expose the port on which your Flask app will run (usually 5000)
EXPOSE 5000

# Start the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
