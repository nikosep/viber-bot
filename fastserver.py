import uvicorn
from fastapi import FastAPI, Request, Response
import logging
import os
from starlette.middleware.cors import CORSMiddleware
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest

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
    name='hotilitieschat',
    avatar='',
    auth_token=os.environ['TOKEN']
    # auth_token="test"
))


@app.post("/")
async def incoming(request: Request):
    body = await request.body()
    logging.info(f"received request. post data: {body}")
    viber_request = viber.parse_request(body)
    message = viber_request.message
    viber.send_messages(viber_request.sender.id, [f"Hello {viber_request.sender.id}, {message} :P"])
    return Response(status_code=200)
    # if not viber.verify_signature(request.json(), request.headers.get('X-Viber-Content-Signature')):
    #     return Response(status_code=403)
    # else:
    #     return Response(status_code=200, content={"message": request.json()})


@app.get("/status")
async def status():
    return Response(status_code=200, content="Running...")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, )
