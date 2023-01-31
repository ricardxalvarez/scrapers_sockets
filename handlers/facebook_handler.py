from .scrapers.facebook import Facebook
from flask_socketio import disconnect


class FacebookHandler():
    def __init__(self, sid, emit):
        self.sid = sid
        self.emit = emit

    def auth(self, data):
        print(data)
        try:
            data["email"]
            data["password"]
            data["message"]
        except KeyError:
            self.emit("message", {
                      'status': False, 'content': 'Make sure of sending email and password'})
            return disconnect(self.sid)
        f = Facebook(self.emit, self.sid)
        self.f = f
        f.auth(data["email"], data["password"])

    def scrape_friends(self, data):
        f = self.f
        try:
            if (data["is_friends_checked"] == True):
                f.scrape_friends()
        except KeyError:
            pass

    def scrape_followers(self, data):
        f = self.f
        try:
            if (data["is_followers_checked"] == True):
                f.scrape_followers()
        except KeyError:
            pass

    def send_messages(self, data):
        f = self.f
        f.send_messages(data["message"])

    def quit(self):
        f = self.f
        f.quit()
