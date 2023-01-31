from flask import Flask, request, session
from flask_socketio import SocketIO, emit, disconnect
from handlers.facebook_handler import FacebookHandler
from handlers.instagram_handler import InstagramHandler
from handlers.tiktok_handler import TiktokHandler
from engineio.payload import Payload

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
    facebook.quit()
    disconnect(request.sid)


@socketio.on('auth_instagram')
def func(data):
    instagram = InstagramHandler(request.sid, emit)
    session["instagram"] = instagram
    if instagram.auth(data):
        instagram.scrape_followers(data)
        instagram.scrape_following(data)
        instagram.send_messages(data)
        instagram.quit()
        disconnect(request.sid)
    print('finished')
# @socketio.on('scrape_friends_facebook')
# def func(data):
#     facebook = session["facebook"]
#     facebook.scrape_friends()


@socketio.on('validate_auth_instagram')
def func(data):
    if session["instagram"]:
        instagram = session["instagram"]
        instagram.validate_auth(data)


@socketio.on('auth_tiktok')
def func(data):
    print(data)
    tiktok = TiktokHandler(request.sid, emit)
    session["tiktok"] = tiktok
    tiktok.auth(data)


@socketio.on('validate_auth_tiktok_scroll')
def func(scroll_x):
    if (session["tiktok"]):
        print(scroll_x)
        tiktok = session["tiktok"]
        tiktok.validate_auth_scroll(scroll_x)


@socketio.on('validate_auth_tiktok_scroll_check')
def func(data):
    if (session["tiktok"]):
        tiktok = session["tiktok"]
        tiktok.validate_auth_scroll_check()


@socketio.on('validate_auth_tiktok_drop')
def func(data):
    if session["tiktok"]:
        tiktok = session["tiktok"]
        tiktok.validate_auth_drop()


if __name__ == '__main__':
    socketio.run(app)
