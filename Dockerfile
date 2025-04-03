# Use a Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install Node.js (LTS version)
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    # Clean up
    apt-get purge -y curl && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install json-diff (latest version)
RUN npm install -g json-diff --unsafe-perm && \
    # Verify installation
    json-diff --help

# Copy application files
COPY . .

# Set entrypoint
ENTRYPOINT ["python", "json_diff_checker.py"]
CMD ["--help"]