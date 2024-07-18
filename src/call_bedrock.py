import json
import boto3
import os

# Load environment variables
region_name = os.getenv('AWS_REGION')
model_id = os.getenv('BEDROCK_INVOKE_MODEL_ID')
knowledge_base_id = os.getenv('BEDROCK_KNOWLEDGE_BASE_ID')
model_arn = os.getenv('BEDROCK_KNOWLEDGE_BASE_MODEL_ARN')

# Initialize AWS clients
bedrock_runtime_client = boto3.client('bedrock-runtime', region_name=region_name)
bedrock_agent_runtime_client = boto3.client('bedrock-agent-runtime', region_name=region_name)

def call_bedrock_invoke(question):
    body = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": question
                    }
                ]
            }
        ],
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2000,
        "temperature": 1,
        "top_k": 250,
        "top_p": 0.999,
        "stop_sequences": ["\n\nHuman:"]
    })

    accept = 'application/json'
    content_type = 'application/json'

    # Call the Bedrock AI model
    response = bedrock_runtime_client.invoke_model(
        body=body,
        modelId=model_id,
        accept=accept,
        contentType=content_type
    )
    
    response_body = json.loads(response.get('body').read())
    # The response from the model now mapped to the answer
    answer = response_body.get('content')[0].get('text')
    return answer

def call_bedrock_knowledgebase(question):
    response = bedrock_agent_runtime_client.retrieve_and_generate(
        input={
            'text': question,
        },
        retrieveAndGenerateConfiguration={
            'type': 'KNOWLEDGE_BASE',
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': knowledge_base_id,
                'modelArn': model_arn,
            }
        }
    )
    # The response from the model now mapped to the answer
    answer = response['output']['text']
    return answer