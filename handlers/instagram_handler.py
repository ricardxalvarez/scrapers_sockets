from .scrapers.instagram import Instagram


class InstagramHandler():
    def __init__(self, sid, emit):
        self.sid = sid
        self.emit = emit

    def auth(self, data):
        print(data)
        try:
            data["username"]
            data["password"]
            data["message"]
        except KeyError:
            return self.emit({"status": False, "content": 'Make sure of sending email and password'})
        self.i = Instagram(self.emit)
        i = self.i
        return i.auth(data["username"], data["password"])

    def validate_auth(self, data):
        try:
            data["validation_code"]
        except KeyError:
            self.emit("message", {
                      'status': False, 'content': 'Make sure of sending validation code'})
        i = self.i
        i.validate_auth(data["validation_code"])

    def scrape_followers(self, data):
        i = self.i
        try:
            if (data["is_followers_checked"] == True):
                i.scrape_followers()
        except KeyError:
            pass

    def scrape_following(self, data):
        i = self.i
        try:
            if (data["is_following_checked"] == True):
                i.scrape_following()
        except KeyError:
            pass

    def send_messages(self, data):
        i = self.i
        i.send_messages(data["message"])

    def quit(self):
        i = self.i
        i.quit()
