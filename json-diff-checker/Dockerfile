# Use a Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install json-diff via npm
RUN apt-get update && \
    apt-get install -y nodejs npm && \
    npm install -g json-diff

# Copy the rest of the application
COPY . .

# Specify the default command to run the script
ENTRYPOINT ["python", "json_diff_checker.py"]

# Define the default command for the container
CMD ["--help"]
