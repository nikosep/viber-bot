import uvicorn
from fastapi import FastAPI, Request, Response
import logging
import os
from starlette.middleware.cors import CORSMiddleware
from viberbot import Api
from viberbot.api.api_request_sender import ApiRequestSender
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import KeyboardMessage, RichMediaMessage, PictureMessage, ContactMessage
from viberbot.api.messages.data_types.contact import Contact
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest

# from dev import chat_response


SAMPLE_RICH_MEDIA = {
    "Type": "rich_media",
    "BgColor": "#FFFFFF",
    "min_api_version": 7,
    "ButtonsGroupColumns": 6,
    "ButtonsGroupRows": 7,
    "Buttons": [
        {
            "ActionBody": "https://www.google.com",
            "Columns": 6,
            "Rows": 3,
            "ActionType": "open-url",
            "Image": "https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1770&q=80",

        },
        {
            "Columns": 6,
            "Rows": 2,
            "ActionBody": "https://www.google.com",
            "TextSize": "medium",
            "TextVAlign": "middle",
            "TextHAlign": "left",
            "Text": "<font color=#323232><b>Headphones with Microphone, On-ear Wired earphones</b></font><font color=#777777><br>Sound Intone </font><font color=#6fc133>$17.99</font>",
        },
        {
            "Columns": 6,
            "Rows": 2,
            "ActionType": "open-url",
            "ActionBody": "https://www.skroutz.gr/s/40552581/Samsung-Galaxy-S23-Ultra-5G-Dual-SIM-8GB-256GB-Cream.html?from=home_price_drops",
            # "Text": "<font color=#ffffff>Buy</font>",
            "TextSize": "large",
            "TextVAlign": "middle",
            "TextHAlign": "middle",
            "Image": "https://www.liveleanrxhouston.com/wp-content/uploads/2019/11/Buy-Now-V2.jpg",
            "InternalBrowser.ActionButton": "none"
        }
    ]
}

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

app = FastAPI()

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

viber = Api(BotConfiguration(
    name=os.getenv('VIBER_BOT_NAME'),
    avatar='',
    auth_token=os.getenv('VIBER_TOKEN')
))


@app.post("/")
async def incoming(request: Request):
    body = await request.body()
    viber_request = viber.parse_request(body)
    if not viber.verify_signature(body, request.headers.get('X-Viber-Content-Signature')):
        return Response(status_code=403)
    try:
        message = viber_request.message
        print(f"Event: {viber_request.event_type}")
        # response = chat_response(message.text)
        # viber.send_messages(viber_request.sender.id, [TextMessage(text=response)])
        # contact = Contact(name="Nikos User", phone_number="+306978691989", avatar="http://link.to.avatar")
        # contact_message = ContactMessage(contact=contact)
        # viber.send_messages(viber_request.sender.id, [contact_message])
        viber.send_messages(viber_request.sender.id,
                            [RichMediaMessage(rich_media=SAMPLE_RICH_MEDIA, min_api_version=7)])
    except:
        pass
    return Response(status_code=200)


counter = []


@app.get("/status")
async def status():
    counter.append(1)
    print(len(counter))
    return Response(status_code=200, content="Running...")


if __name__ == "__main__":
    uvicorn.run("fastserver:app", host="0.0.0.0", port=80, reload=True)
