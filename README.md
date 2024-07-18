# Amazon Bedrock with Slack Gateway / Bot

This project is a Slack bot application built using the `slack_bolt` library and the FastAPI web framework. The bot listens for app mentions and messages in Slack channels and responds accordingly. It also provides two slash commands: `/bedrock-ask` and `/bedrock-find`.

## main.py

The `main.py` file is the entry point of the application and contains the following components:

### Event Handlers

- `handle_app_mentions`: This event handler listens for app mentions in Slack channels and responds with a greeting message.
- `handle_message`: This event handler is currently empty but can be used to handle incoming messages in Slack channels.

### Slash Commands

- `/bedrock-ask`: This slash command accepts a user's prompt as input, calls the [Amazon Bedrock Invoke API](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-invoke.html) pass the user's prompt into Anthropic Claude 3 Haiku LLM, and responds with the result.
- `/bedrock-find`: This slash command accepts a user's prompt as input, calls the [Amazon Bedrock Knowledge Base API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html) pass the user's prompt and retrieve the context via Knowledge Base RAG, generate response, and responds with the result. Specified knowledge base may have data sources such as Confluence, S3, Sharepoint, Salesforce, etc.

### FastAPI Endpoint

The `endpoint` function is a FastAPI endpoint that handles incoming requests from Slack. It uses the `AsyncSlackRequestHandler` to process the requests and route them to the appropriate event handlers or slash commands.

### Imports

The file imports the necessary modules and libraries, including:

- `logging` for logging purposes
- `slack_bolt` for building the Slack bot
- `fastapi` for creating the web application
- `call_bedrock` for invoking the Bedrock AI service

### Configuration

The logging level is set to `DEBUG` using `logging.basicConfig(level=logging.DEBUG)`.

### Main Function

The `main.py` file does not contain a `main` function. Instead, it sets up the Slack bot, defines the event handlers and slash commands, and creates the FastAPI application.

### Run locally

```
python3 -m venv venv
source venv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

Create .env file in the root folder and set variables

```
SLACK_SIGNING_SECRET="SLACK_SIGNING_SECRET"
SLACK_BOT_TOKEN="SLACK_BOT_TOKEN"
BEDROCK_KNOWLEDGE_BASE_ID="BEDROCK_KNOWLEDGE_BASE_ID"
AWS_REGION=us-east-1
BEDROCK_INVOKE_MODEL_ID=anthropic.claude-3-haiku-20240307-v1:0
BEDROCK_KNOWLEDGE_BASE_MODEL_ARN=arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-haiku-20240307-v1:0
```

In vscode "Run & Debug" -> "Debug Bedrock Gateway"

### Deployment

```
# Update these env variables in src/Dockerfile

ENV SLACK_SIGNING_SECRET "SLACK_SIGNING_SECRET"
ENV SLACK_BOT_TOKEN "SLACK_BOT_TOKEN"
ENV BEDROCK_KNOWLEDGE_BASE_ID "BEDROCK_KNOWLEDGE_BASE_ID"
ENV AWS_REGION "us-east-1"
ENV BEDROCK_INVOKE_MODEL_ID "anthropic.claude-3-haiku-20240307-v1:0"
ENV BEDROCK_KNOWLEDGE_BASE_MODEL_ARN "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-haiku-20240307-v1:0"
```

```
docker build -t bedrock-gateway-img .
docker run -d -p 8000:8000 --name bedrock-gateway bedrock-gateway-img
```
