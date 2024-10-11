# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /src

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the FastAPI application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Define environment variable
ENV SLACK_SIGNING_SECRET "SLACK_SIGNING_SECRET"
ENV SLACK_BOT_TOKEN "SLACK_BOT_TOKEN"
ENV AWS_REGION "us-east-1"
ENV BEDROCK_KNOWLEDGE_BASE_ID "BEDROCK_KNOWLEDGE_BASE_ID"
ENV BEDROCK_INVOKE_MODEL_ID "anthropic.claude-3-haiku-20240307-v1:0"
ENV BEDROCK_KNOWLEDGE_BASE_MODEL_ARN "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-haiku-20240307-v1:0"
# For Kendra based scenarios
ENV KENDRA_INDEX_ID ""

# Command to run the application
CMD ["uvicorn", "main:api", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]