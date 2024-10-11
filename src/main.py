import logging
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
from fastapi import FastAPI, Request
from call_bedrock import call_bedrock_invoke, call_bedrock_knowledgebase, call_kendra_knowledgebase

logging.basicConfig(level=logging.DEBUG)

app = AsyncApp()
app_handler = AsyncSlackRequestHandler(app)

@app.event("app_mention")
async def handle_mentions(event, client, say, context):
    api_response = await client.reactions_add(
        channel=event["channel"],
        timestamp=event["ts"],
        name="eyes",
    )
    text = event['text']
    bot_user_id = context['bot_user_id']
    mention = f'<@{bot_user_id}>'
    clean_text = text.replace(mention, '').strip()
    if clean_text:
        await say("Hmmm... Let me have a look...")
        # If there's text after removing the mention, respond to it
        result = call_bedrock_knowledgebase(clean_text)
        await say(f':bulb: {result}')
    else:
        # If there's no text after removing the mention, ask how to help
        await say("How can I help you?")

@app.event("message")
async def handle_message(say):
    pass

@app.command("/bedrock-ask")
async def bedrock_ask_command(ack, respond, command):
    await ack()
    await respond("Let me think about it...")
    prompt = command["text"]
    result = call_bedrock_invoke(prompt)
    await respond(f':thinking_face: Question: *{prompt}*\n:bulb: Answer: {result}')

@app.command("/bedrock-find")
async def bedrock_find_command(ack, respond, command):
    await ack()
    await respond("Let me have a look...")
    prompt = command["text"]
    result = call_bedrock_knowledgebase(prompt)
    await respond(f':thinking_face: Question: *{prompt}*\n:bulb: Answer: {result}')

@app.command("/kendra-find")
async def bedrock_find_command(ack, respond, command):
    await ack()
    await respond("Let me have a look...")
    prompt = command["text"]
    result = call_kendra_knowledgebase(prompt)
    await respond(f':thinking_face: Question: *{prompt}*\n:bulb: Answer: {result}')

api = FastAPI()

@api.post("/slack/events")
async def endpoint(req: Request):
    return await app_handler.handle(req)