from selenium import webdriver
import time
import random
import decimal
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from flask_socketio import disconnect
from dotenv import load_dotenv
import os

load_dotenv()

development = bool(os.environ['development'])


class Facebook():
    def __init__(self, emit, sid):
        self.emit = emit
        self.sid = sid
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument('--disable-notifications')

        # chrome_options.add_argument('--proxy-server=%s' % PROXY)
        chrome_options.add_argument(
            '--disable-blink-features=AutomationControlled')
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        self.browser = webdriver.Chrome(
            'chromedriver', chrome_options=chrome_options)
        browser = self.browser
        browser.get('https://facebook.com')
        browser.set_window_size(900, 700)
        time.sleep(random.randrange(4, 6))

        # declare set of users we will send messages
        self.users = set()

    # sign in to facebook account

    def auth(self, email: str, password: str):
        try:
            self.email = email
            self.password = password
            browser = self.browser
            emit = self.emit
            emit('message', {'status': True, 'content': 'Trying to log in'})
            input_email = browser.find_element_by_name('email')
            input_password = browser.find_element_by_name('pass')
            time.sleep(float(decimal.Decimal(random.randrange(2, 3))))
            input_email.send_keys(email)
            time.sleep(float(decimal.Decimal(random.randrange(2, 3))))
            input_password.send_keys(password)
            time.sleep(float(decimal.Decimal(random.randrange(4, 5))))
            input_password.send_keys(Keys.ENTER)
            time.sleep(float(decimal.Decimal(random.randrange(10, 12))))
            try:
                error = browser.find_element_by_xpath(
                    '/html/body/div[1]/div[1]/div[1]/div/div[2]/div[2]/form/div/div[2]/div[2]').text
                time.sleep(float(decimal.Decimal(random.randrange(2, 3))))
                print(error)
                emit("message", {"status": False, "content": error})
                self.quit()
                return
            except NoSuchElementException:
                pass
            try:
                error = browser.find_element_by_xpath(
                    '/html/body/div[1]/div[1]/div[1]/div/div[2]/div[2]/form/div[1]/div[1]').text
                time.sleep(float(decimal.Decimal(random.randrange(2, 3))))
                print(error)
                emit("message", {"status": False, "content": error})
                self.quit()
                return
            except NoSuchElementException:
                pass

            try:
                error = browser.find_element_by_xpath(
                    '/html/body/div[1]/div[1]/div[1]/div/div[2]/div[2]/form/div/div[1]/div[2]').text
                time.sleep(float(decimal.Decimal(random.randrange(2, 3))))
                print(error)
                emit("message", {"status": False, "content": error})
                self.quit()
                return
            except NoSuchElementException:
                pass

            emit("message", {"status": True,
                 "content": "Successfully logged in"})

            time.sleep(float(decimal.Decimal(random.randrange(5, 7))))
        except NoSuchElementException as err:
            print(err)
            emit("message", {
                 "status": False, "content": "Internal server error, please try again"})
            if development == False:
                self.quit()

    def scrape_friends(self):
        try:
            browser = self.browser
            emit = self.emit
            self.friends = set()
            emit("message", {"status": True, "content": "Listing friends..."})
            browser.set_window_size(900, 700)
            time.sleep(float(decimal.Decimal(random.randrange(1, 2))))

            time.sleep(float(decimal.Decimal(random.randrange(5, 7))))
            browser.get('https://www.facebook.com/me')

            time.sleep(float(decimal.Decimal(random.randrange(5, 7))))

            # browser.execute_script("window.scrollTo(0, 100)")
            # time.sleep(random.randrange(1, 2))
            browser.get('{}&sk=friends'.format(browser.current_url))
            # friends_quantity.click()
            time.sleep(float(decimal.Decimal(random.randrange(12, 15))))
            friends_quantity = int(browser.find_element_by_xpath(
                '/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[2]/span/a').text.split(' ')[0])
            print(friends_quantity)
            # browser.find_element_by_xpath(
            #     '/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[3]/div/div/div/div[1]/div/div/div[1]/div/div/div/div/div/div/a[3]').click()
            time.sleep(float(decimal.Decimal(random.randrange(3, 5))))
            loops_count = 0
            while True:
                try:
                    loops_count = loops_count + 1
                    if (loops_count % 5 == 0):
                        time.sleep(
                            float(decimal.Decimal(random.randrange(10, 17))))
                        loops_count = 0
                    time.sleep(float(decimal.Decimal(random.randrange(2, 4))))
                    browser.execute_script(
                        "window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(float(decimal.Decimal(random.randrange(2, 3))))
                    friends_list = browser.find_elements_by_xpath(
                        '/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div/div/div/div/div/div[3]/div')
                    time.sleep(float(decimal.Decimal(random.randrange(5, 6))))
                    for friend in friends_list:
                        try:
                            id = friend.find_element_by_xpath(
                                './/div[1]/a').get_attribute('href').split('/')[3]

                            name = friend.find_element_by_xpath(
                                './/div[2]/div[1]/a/span').text

                            if "profile.php?id=" in id:
                                id = id.strip('profile.php?id=')
                            if (id and name):
                                self.friends.add((name, id))
                        except NoSuchElementException:
                            continue
                    if (friends_quantity <= friends_list.__len__()):
                        browser.execute_script(
                            "window.scrollTo(0, 0);")
                        emit("message", {"status": True, "content": '{} friends listed'.format(
                            self.friends.__len__() or 0)})
                        break
                    try:
                        photos = browser.find_element_by_xpath(
                            '/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[2]/div/div/div/div')
                        if (photos):
                            emit("message", {"status": True, "content": '{} friends listed'.format(
                                self.friends.__len__() or 0)})
                            break
                    except NoSuchElementException:
                        pass
                except StaleElementReferenceException:
                    pass
            browser.refresh()
            time.sleep(float(decimal.Decimal(random.randrange(5, 7))))
            time.sleep(float(decimal.Decimal(random.randrange(5, 7))))
        except NoSuchElementException as err:
            print(err)
            print(development)
            emit("message", {
                 "status": False, "content": "Internal server error, please try again"})
            if development == False:
                self.quit()

    def scrape_followers(self):
        try:
            browser = self.browser
            emit = self.emit
            self.followers = set()
            emit("message", {"status": True, "content": "Listing followers"})
            browser.set_window_size(900, 700)
            time.sleep(float(decimal.Decimal(random.randrange(4, 6))))

            time.sleep(float(decimal.Decimal(random.randrange(5, 7))))
            browser.get('https://www.facebook.com/me')
            # browser.execute_script(
            time.sleep(float(decimal.Decimal(random.randrange(5, 7))))
            #     "window.scrollTo(0, 500);")
            browser.get('{}&sk=followers'.format(browser.current_url))
            loops_count = 0
            while True:
                try:
                    loops_count = loops_count + 1
                    if (loops_count % 5 == 0):
                        time.sleep(
                            float(decimal.Decimal(random.randrange(10, 17))))
                        loops_count = 0

                    time.sleep(float(decimal.Decimal(random.randrange(2, 4))))
                    browser.execute_script(
                        "window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(float(decimal.Decimal(random.randrange(2, 3))))

                    followers_list = browser.find_elements_by_xpath(
                        '/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[3]/div')
                    for follower in followers_list:
                        try:
                            id = follower.find_element_by_xpath(
                                './/div[1]/a').get_attribute('href').split('/')[3]

                            name = follower.find_element_by_xpath(
                                './/div[2]/div[1]/a/span').text

                            if "profile.php?id=" in id:
                                id = id.strip('profile.php?id=')
                            if (name and id):
                                self.followers.add((name, id))
                        except NoSuchElementException:
                            continue
                    try:
                        photos = browser.find_element_by_xpath(
                            '/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[2]/div/div/div/div')
                        if (photos):
                            emit("message", {"status": True, "content": "{} followers listed".format(
                                self.followers.__len__() or 0)})
                            break
                    except NoSuchElementException:
                        pass

                except StaleElementReferenceException:
                    pass
            time.sleep(float(decimal.Decimal(random.randrange(5, 7))))
            browser.refresh()
        except NoSuchElementException as err:
            print(err)
            emit("message", {"status": True,
                 "content": "Successfully logged in"})
            if development == False:
                self.quit()

    def send_messages(self, message_struc: str):
        try:
            browser = self.browser
            emit = self.emit

            for user in self.followers:
                self.users.add(user)

            for user in self.friends:
                self.users.add(user)

            browser.set_window_size(1200, 700)
            emit("message", {"status": True,
                 "content": "Sending messages to all users listed"})
            browser.maximize_window()
            time.sleep(float(decimal.Decimal(random.randrange(5, 7))))
            try:
                browser.find_element_by_xpath(
                    '/html/body/div[1]/div[1]/div[1]/div/div[2]/div[4]/div[1]/div[2]/span/span/div/div[1]').click()
            except NoSuchElementException:
                browser.find_element_by_xpath(
                    '/html/body/div[1]/div/div[1]/div/div[2]/div[5]/div[1]/div[2]/span/span/div/div[1]').click()

            time.sleep(float(decimal.Decimal(random.randrange(2, 4))))
            try:
                browser.find_element_by_xpath(
                    '/html/body/div[1]/div[1]/div[1]/div/div[2]/div[4]/div[2]/div/div/div[1]/div[1]/div/div/div/div/div/div/div[1]/div/div/div[2]/span/a').click()
            except NoSuchElementException:
                browser.find_element_by_xpath(
                    '/html/body/div[1]/div/div[1]/div/div[2]/div[5]/div[2]/div/div/div[1]/div[1]/div/div/div/div/div/div/div[1]/div/div/div[2]/span/a').click()

            time.sleep(float(decimal.Decimal(random.randrange(13, 15))))
            for receiver in self.users:
                browser.get(
                    'https://www.facebook.com/messages/t/{}'.format(receiver[1]))

                time.sleep(float(decimal.Decimal(random.randrange(7, 10))))
                try:

                    time.sleep(float(decimal.Decimal(random.randrange(3, 4))))
                    try:
                        message_input = browser.find_element_by_xpath(
                            '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[1]/div[2]/div/div/div[2]/div/div/div[4]/div[2]/div/div/div[1]')
                    except NoSuchElementException:
                        try:
                            message_input = browser.find_element_by_xpath(
                                '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[4]/div[2]/div/div/div[1]')
                        except NoSuchElementException:
                            message_input = browser.find_element_by_xpath(
                                '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[4]/div[2]/div/div/div[1]')
                    message_input.click()

                    message = message_struc.replace('/&&/', receiver[0])
                    print(message)
                    message_input.send_keys(message)
                    time.sleep(float(decimal.Decimal(random.randrange(3, 4))))
                    message_input.send_keys(Keys.ENTER)
                    time.sleep(float(decimal.Decimal(random.randrange(2, 3))))
                except (NoSuchElementException, StaleElementReferenceException) as err:
                    print(err)
            emit("message", {"status": True, "content": "Messages successfully sent to {} users".format(
                self.users.__len__())})
            time.sleep(float(decimal.Decimal(random.randrange(5, 7))))
        except NoSuchElementException as err:
            print(err)
            emit("message", {
                 "status": False, "content": "Internal server error, please try again"})
            if development == False:
                self.quit()

    def quit(self):
        self.browser.quit()
        self.emit('message', {'status': False,
                  'content': 'Session disconnected'})
        disconnect(self.sid)
