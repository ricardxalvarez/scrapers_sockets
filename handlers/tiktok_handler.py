from flask_socketio import disconnect
from .scrapers.tiktok import Tiktok


class TiktokHandler:
    def __init__(self, sid, emit):
        self.sid = sid
        self.emit = emit

    def auth(self, data):
        print(data)
        try:
            data["username"]
            data["password"]
        except KeyError:
            self.emit("message", {
                      'status': False, 'content': 'Make sure of sending email and password'})
            return disconnect(self.sid)
        t = Tiktok(self.emit, self.sid)
        self.t = t
        t.auth(data["username"], data["password"])

    def validate_auth_scroll(self, scroll_x: int):
        t = self.t
        t.validate_auth_scroll(scroll_x)

    def validate_auth_drop(self):
        t = self.t
        t.validate_auth_drop()

    def validate_auth_scroll_check(self):
        t = self.t
        t.validate_auth_scroll_check()
