from fastapi import FastAPI, Request, Response
from viberbot import Api, BotConfiguration
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.messages.rich_media_message import RichMediaMessage
from src.chatbot import ChatBot
from config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
chat_bot = ChatBot()

# Initialize Viber bot
viber = Api(BotConfiguration(
    name=Config.VIBER_BOT_NAME,
    avatar='',
    auth_token=Config.VIBER_TOKEN
))


# Route to handle incoming messages
@app.post("/{app_id}")
async def incoming(app_id: str, request: Request):
    identifier = app_id
    body = await request.body()
    viber_request = viber.parse_request(body)
    if not viber.verify_signature(body, request.headers.get('X-Viber-Content-Signature')):
        return Response(status_code=403)
    try:
        message = viber_request.message
        if message.text:
            chat_bot.initialize()
            response = chat_bot.chat_response(message.text)
            viber.send_messages(viber_request.sender.id, [TextMessage(text=response)])
    except Exception as e:
        logger.error(f"Error occurred during message handling: {e}")
        pass
    return Response(status_code=200)
