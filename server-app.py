import logging
import os
import sched
import threading
import time

from flask import Flask, request, Response
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest

context = ('/etc/letsencrypt/live/pharmaproof.com/cert.pem', '/etc/letsencrypt/live/pharmaproof.com/privkey.pem')

app = Flask(__name__)

viber = Api(BotConfiguration(
    name='parkara',
    avatar='',
    auth_token=os.environ['TOKEN']
))


@app.route('/', methods=['POST'])
def incoming():
    if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)
    viber_request = viber.parse_request(request.get_data())

    if isinstance(viber_request, ViberMessageRequest):
        logging.error("Entered in valid viber request")
        message = viber_request.message
        # lets echo back
        user_data = Api.get_user_details("userId")
        print(user_data)
        viber.send_messages(viber_request.sender.id, ["Hello from Nikos"])
    elif isinstance(viber_request, ViberSubscribedRequest):
        viber.send_messages(viber_request.get_user.id, [
            TextMessage(text="thanks for subscribing!")
        ])
    elif isinstance(viber_request, ViberFailedRequest):
        logging.warn("client failed receiving message. failure: {0}".format(viber_request))
    return Response(status=200)

    # handle the request here
    return Response(status=200)


def set_webhook(viber):
    viber.set_webhook('https://pharmaproof.com:443/')


if __name__ == "__main__":
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(5, 1, set_webhook, (viber,))
    t = threading.Thread(target=scheduler.run)
    t.start()
    app.run(host="0.0.0.0", port=443, debug=True, ssl_context=context)
    # app.run(host='134.209.247.209', debug=True, ssl_context=context)
    # app.run(host='https://pharmaproof.com', port=443, debug=True, ssl_context=context)
