from flask import Flask, request, session
from flask_socketio import SocketIO, emit, disconnect
from handlers.facebook_handler import FacebookHandler
from handlers.instagram_handler import InstagramHandler
from engineio.payload import Payload
from dotenv import load_dotenv
import os

load_dotenv()

development = os.environ['development']
Payload.max_decode_packets = 500
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Secret'
socketio = SocketIO(app, cors_allowed_origins='*', ping_timeout=5)


@app.route('/')
def index():
    return 'Hello'


@socketio.on('auth_facebook')
def func(data):
    facebook = FacebookHandler(request.sid, emit)
    # session["facebook"] = facebook
    facebook.auth(data)
    facebook.scrape_friends(data)
    facebook.scrape_followers(data)
    facebook.send_messages(data)
    if development == False:
        facebook.quit()
    print('finished')


@socketio.on('auth_instagram')
def func(data):
    instagram = InstagramHandler(request.sid, emit)
    session["instagram"] = instagram
    if instagram.auth(data):
        instagram.scrape_followers(data)
        instagram.scrape_following(data)
        instagram.send_messages(data)
        if development == False:
            instagram.quit()
    print('finished')


@socketio.on('validate_auth_instagram')
def func(data):
    if session["instagram"]:
        instagram = session["instagram"]
        instagram.validate_auth(data)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=443)
