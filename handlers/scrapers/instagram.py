from selenium import webdriver
import time
import random
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


class Instagram():
    def __init__(self, emit):
        self.emit = emit
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
        browser.get('https://instagram.com')
        browser.set_window_size(900, 700)
        time.sleep(random.randrange(5, 7))
        try:
            browser.find_element_by_xpath(
                '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[2]').click()
        except NoSuchElementException:
            pass
        # declare set of users we will send messages
        self.users = set()
        self.followers = set()
        self.following = set()

    def auth(self, username: str, password: str):
        browser = self.browser
        self.username = username
        emit = self.emit
        emit('message', {'status': True, 'content': 'Trying to log in'})
        time.sleep(random.randrange(5, 7))
        try:
            browser.find_element_by_xpath(
                '/html/body/div[4]/div/div/button[2]'
            ).click()

            time.sleep(random.randrange(5, 7))
        except NoSuchElementException:
            print('No error')

        input_username = browser.find_element_by_name('username')
        input_password = browser.find_element_by_name('password')
        time.sleep(random.randrange(1, 2))
        input_username.send_keys(username)
        time.sleep(random.randrange(1, 2))
        input_password.send_keys(password)
        time.sleep(random.randrange(4, 5))
        input_password.send_keys(Keys.ENTER)
        time.sleep(random.randrange(10, 12))
        try:
            error = browser.find_element_by_xpath(
                '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div[2]/p').text
            emit("message", {"status": False, "content": error})
            browser.quit()
            return
        except NoSuchElementException:
            print('No error')
        try:
            error = browser.find_element_by_xpath(
                '/html/body/div[1]/div/div/section/main/article/div[2]/div[1]/div[2]/form/div[2]/p').text
            emit("message", {"status": False, "content": error})
            browser.quit()
            return
        except NoSuchElementException:
            print('No error')
        time.sleep(random.randrange(2, 3))
        try:
            error = browser.find_element_by_xpath(
                '/html/body/div[1]/section/div/div/p').text
            error1 = browser.find_element_by_xpath(
                '/html/body/div[1]/section/div/div/div[3]/form/div/div/label').text
            emit("message", {"status": False,
                 "content": error + "\n" + error1})
            browser.find_element_by_xpath(
                '/html/body/div[1]/section/div/div/div[3]/form/span/button').click()
            return
        except NoSuchElementException:
            pass
        try:
            browser.find_element_by_xpath(
                '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]').click()
        except NoSuchElementException:
            print('Pop out element not found')

        emit("message", {"status": True, "content": "Successfully logged in"})
        time.sleep(13)
        # except Exception as err:
        #     print(err)
        #     browser.quit()
        return True

    def validate_auth(self, code):
        browser = self.browser
        emit = self.emit
        inputs = browser.find_elements_by_xpath(
            '/html/body/div[1]/section/div/div/div[2]/form/div/div/div')
        time.sleep(random.randrange(2, 4))
        for dex, i in enumerate(inputs):
            time.sleep(random.randrange(2, 4))
            print(i)
            print(dex)
            # i.send_keys(code[dex])

    def scrape_followers(self):
        browser = self.browser
        emit = self.emit
        emit('message', {'status': True, 'content': 'Listing followers'})
        time.sleep(random.randrange(7, 10))
        try:
            browser.find_element_by_xpath(
                '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div[2]/div[7]/div/div/a').click()
        except NoSuchElementException:
            try:
                browser.find_element_by_xpath(
                    '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[7]/div/div/a').click()
            except NoSuchElementException:
                browser.find_element_by_xpath(
                    '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[7]/div/div/a').click()
        time.sleep(random.randrange(15, 17))
        time.sleep(random.randrange(15, 17))
        #  gets the quantity this user has
        # so we can know when to stop 'while is_scrolling' loop
        try:
            followers_quantity = int(browser.find_element_by_xpath(
                '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[2]/a/div/span').get_attribute('title'))
        except NoSuchElementException:
            try:
                followers_quantity = int(browser.find_element_by_xpath(
                    '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a/div/span').text)
            except NoSuchElementException:
                followers_quantity = int(browser.find_element_by_xpath(
                    '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/ul/li[2]/a/div/span').text)
    #     # finds and opens followers list
        try:
            followers_button = browser.find_element_by_xpath(
                '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[2]/a')
        except NoSuchElementException:
            try:
                followers_button = browser.find_element_by_xpath(
                    '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a')
            except NoSuchElementException:
                followers_button = browser.find_element_by_xpath(
                    '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/ul/li[2]/a')
        followers_button.click()
        time.sleep(random.randrange(10, 13))
        is_scrolling = True
        time.sleep(random.randrange(3, 5))
        # global not_changed
        not_changed = 0
        while is_scrolling:
            if (not_changed == 2):
                break
            time.sleep(random.randrange(1, 3))
            # scrolls down to the end
            try:
                browser.find_element_by_xpath(
                    '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]')
                browser.execute_script(
                    "document.evaluate('/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollTop+=document.evaluate('/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight || 200")
            except NoSuchElementException:
                browser.find_element_by_xpath(
                    '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]')
                browser.execute_script(
                    "document.evaluate('/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollTop+=document.evaluate('/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight || 200")

            time.sleep(0.1)
            # checks if loader exists, if it doesn't it means we've reached the limit of users
            # this avoids an infite loop
            try:
                is_valid = False
                try:
                    browser.find_element_by_xpath(
                        "/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[2]/div")
                    is_valid = True
                except NoSuchElementException:
                    pass
                try:
                    browser.find_element_by_xpath(
                        '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[2]/div')
                    is_valid = True
                except NoSuchElementException:
                    pass

                if (is_valid == False):
                    not_changed = not_changed + 1

            except NoSuchElementException or StaleElementReferenceException:
                not_changed = not_changed + 1
            # gets a new list of followers (10 more approximaly)
            try:
                browser.find_element_by_xpath(
                    '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]')
                followers = browser.find_elements_by_xpath(
                    '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div')
            except NoSuchElementException:
                pass

            try:
                browser.find_element_by_xpath(
                    '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]')
                followers = browser.find_elements_by_xpath(
                    '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div')
            except NoSuchElementException:
                pass
            #    # Getting url from href attribute
            for i in followers:
                element = i.find_element_by_xpath(
                    ".//div[2]/div[1]/div/div/span/a")
                if element.get_attribute('href'):
                    # adds username to followers_list set
                    self.followers.add(
                        element.get_attribute('href').split("/")[3])
                else:
                    continue
            # if this set is larger or equal than the followers quantity then will brake this loop
            if (followers_quantity <= self.followers.__len__()):
                break
        emit("message", {
             "status": True, "content": "{} followers listed".format(self.followers.__len__())})

        try:
            browser.find_element_by_xpath(
                '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/button').click()
        except NoSuchElementException:
            pass

        try:
            browser.find_element_by_xpath(
                '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/button').click()
        except NoSuchElementException:
            pass

    def add_users_to_set(self, list: set):
        for user in list:
            self.users.add(user)

    def scrape_following(self):
        browser = self.browser
        emit = self.emit
        emit("message", {"status": True,
             "content": "Listing people you follow"})
        try:
            # takes how many people follows you
            time.sleep(random.randrange(7, 10))
            try:
                browser.find_element_by_xpath(
                    '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[1]/div/div/div/div/div[2]/div[7]/div/div/a').click()
            except NoSuchElementException:
                try:
                    browser.find_element_by_xpath(
                        '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[7]/div/div/a').click()
                except NoSuchElementException:
                    browser.find_element_by_xpath(
                        '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[7]/div/div/a').click()
            time.sleep(random.randrange(13, 15))
            time.sleep(random.randrange(13, 15))

            try:
                following_count = int(browser.find_element_by_xpath(
                    '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[3]/a/div/span').text)
            except NoSuchElementException:
                try:
                    following_count = int(browser.find_element_by_xpath(
                        '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/a/div/span').text)
                except NoSuchElementException:
                    following_count = int(browser.find_element_by_xpath(
                        '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/ul/li[3]/a/div/span/span').text)
            # opnes ths pop out showing a list
            try:
                browser.find_element_by_xpath(
                    '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[3]/a').click()
            except NoSuchElementException:
                try:
                    browser.find_element_by_xpath(
                        '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/a').click()
                except:
                    browser.find_element_by_xpath(
                        '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/ul/li[3]/a').click()
            # await client_socket.send('This user has {} followers'.format(following_count))
            is_scrolling = True
            not_changed = 0
            time.sleep(random.randrange(10, 13))
            while is_scrolling:
                if (not_changed == 2):
                    break
                time.sleep(random.randrange(1, 3))
                # scrolls down to the end
                try:
                    browser.find_element_by_xpath(
                        '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]')
                    browser.execute_script(
                        "document.evaluate('/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollTop+=document.evaluate('/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")
                except NoSuchElementException:
                    pass

                try:
                    browser.find_element_by_xpath(
                        '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]')
                    browser.execute_script(
                        "document.evaluate('/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollTop+=document.evaluate('/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")
                except NoSuchElementException:
                    pass
                time.sleep(0.1)
                # checks if loader exists, if it doesn't it means we've reached the limit of users
                try:
                    is_valid = False
                    try:
                        browser.find_element_by_xpath(
                            "/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[2]/div")
                        is_valid = True
                    except NoSuchElementException:
                        pass
                    try:
                        browser.find_element_by_xpath(
                            "/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[2]/div")
                        is_valid = True
                    except NoSuchElementException:
                        pass
                    if (is_valid == False):
                        not_changed = not_changed + 1
                except NoSuchElementException:
                    not_changed = not_changed + 1
                # gets a new list of followers (10 more approximaly)
                try:
                    browser.find_element_by_xpath(
                        '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]')
                    following = browser.find_elements_by_xpath(
                        '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div')
                except NoSuchElementException:
                    pass
                try:
                    browser.find_element_by_xpath(
                        '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]')
                    following = browser.find_elements_by_xpath(
                        '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div')
                except NoSuchElementException:
                    pass

                for i in following:
                    try:
                        element = i.find_element_by_xpath(
                            ".//div[2]/div[1]/div/div/span/a")
                        if element.get_attribute('href'):
                            # adds username to followers_list set
                            self.following.add(
                                element.get_attribute('href').split("/")[3])
                        else:
                            print('not found')
                            continue
                    except NoSuchElementException or StaleElementReferenceException:
                        continue
                print(following_count)
                print(self.following)

                # if this set is larger or equal than the followers quantity then will brake this loop
                if (following_count <= self.following.__len__()):
                    break

            emit("message", {
                 "status": True, "content": "{} users listed".format(self.following.__len__())})
            # await client_socket.send('{} users scraped'.format(following_list.__len__()))
            # print('[DONE] - Your followers are saved in followers.txt file!')

            # writes a file of the followers
            # with open('following.txt', 'a') as file:
            #     file.write('\n'.join(following_list) + "\n")
        except NoSuchElementException as err:
            print(err)
            browser.quit()

    def send_messages(self, message_struc: str):
        browser = self.browser
        emit = self.emit
        for u in self.followers:
            self.users.add(u)

        for u in self.following:
            self.users.add(u)

        print(self.users)

        emit(
            ("message", {"status": True, "content": "Sending messages to selected users"}))
        try:
            # await client_socket.send('Starting to send messages')
            # goes to inbox page
            browser.get('https://www.instagram.com/direct/inbox/')
            time.sleep(random.randrange(3, 5))
            # closes pop out of turn on notifications
            try:
                browser.find_element_by_xpath(
                    '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]').click()
            except NoSuchElementException:
                try:
                    browser.find_element_by_xpath(
                        '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]').click()
                except NoSuchElementException:
                    print('Turn on notifications pop out already closed')

            # open mmessage sender
            try:
                browser.find_element_by_xpath(
                    '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div/div[2]/div/div/div[2]/div/div[3]/div/button').click()
            except NoSuchElementException:
                try:
                    browser.find_element_by_xpath(
                        '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[1]/div[1]/div/div[3]/button').click()
                except NoSuchElementException:
                    browser.find_element_by_xpath(
                        '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[1]/div[1]/div/div[3]/button').click()

            time.sleep(random.randrange(2, 3))
            test_users = set()
            test_users.add('dorkcoon')
            test_users.add('oriiicastillo')
            for follower in test_users:
                time.sleep(random.randrange(3, 5))
                # selects users search input
                try:
                    searcher_input = browser.find_element_by_xpath(
                        '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[1]/div/div[2]/input')
                except NoSuchElementException:
                    searcher_input = browser.find_element_by_xpath(
                        '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[1]/div/div[2]/input')

                searcher_input.click()
                searcher_input.clear()

                time.sleep(random.randrange(4, 6))
                # searches for the user
                searcher_input.send_keys(follower)

                time.sleep(random.randrange(4, 7))
                # gets the list of results
                try:
                    browser.find_element_by_xpath(
                        '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]')
                    users = browser.find_elements_by_xpath(
                        '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]/div')
                except NoSuchElementException:
                    browser.find_element_by_xpath(
                        '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]')
                    users = browser.find_elements_by_xpath(
                        '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]/div')

                # checks te list of results
                # await client_socket.send('Sending messages...')
                for user in users:
                    # get the username of each results
                    username = user.find_element_by_xpath(
                        './/div/div[2]/div[1]/div'
                    ).text
                    # checks if the result is the same as the accout we are looking for
                    if (username == follower):
                        # selects the user
                        user.find_element_by_xpath(
                            './/div').click()
                        # takes us to the dm of the user
                        try:
                            browser.find_element_by_xpath(
                                '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[3]/div/button').click()
                        except NoSuchElementException:
                            browser.find_element_by_xpath(
                                '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[3]/div/button').click()

                        time.sleep(random.randrange(4, 6))
                        # finds the input that the message will be in
                        try:
                            message_input = browser.find_element_by_xpath(
                                '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')
                        except NoSuchElementException:
                            try:
                                message_input = browser.find_element_by_xpath(
                                    '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')
                            except NoSuchElementException:
                                message_input = browser.find_element_by_xpath(
                                    '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')

                        message_input.click()
                        message_input.clear()
                        # sends the message to the input

                        message = message_struc.replace('/&&/', username)
                        print(message)
                        message_input.send_keys(message)

                        time.sleep(random.randrange(1, 2))
                        # click button to send the message
                        try:
                            browser.find_element_by_xpath(
                                '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button').click()
                        except NoSuchElementException:
                            try:
                                browser.find_element_by_xpath(
                                    '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button').click()
                            except NoSuchElementException:
                                browser.find_element_by_xpath(
                                    '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button').click()

                        time.sleep(3)
                        # opens again dm searcher
                        try:
                            browser.find_element_by_xpath(
                                '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div/div[2]/div/div/div[1]/div[1]/div/div[3]/button').click()
                        except NoSuchElementException:
                            try:
                                browser.find_element_by_xpath(
                                    '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[1]/div[1]/div/div[3]/button').click()
                            except NoSuchElementException:
                                browser.find_element_by_xpath(
                                    '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[1]/div[1]/div/div[3]/button').click()

                        break

            emit("message", {
                 "status": True, "content": "Messages sent to {} users".format(self.users.__len__())})
        except Exception as err:
            print(err)

    def quit(self):
        self.browser.quit()
