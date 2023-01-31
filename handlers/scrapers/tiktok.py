from selenium import webdriver
import time
import random
import decimal
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains


class Tiktok():
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
        # chrome_options.add_argument("--profile-directory=Default")
        chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        # tz_params = {'timezoneId': 'America/New_York'}
        # chrome_options.add_argument(
        #     "--user-data-dir=C:/Users/user/AppData/Local/Google/Chrome/User Data")
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        self.browser = webdriver.Chrome(
            'chromedriver', chrome_options=chrome_options)
        browser = self.browser
        browser.execute_cdp_cmd('Network.setBlockedURLs', {
                                'urls': ['https://mon.us.tiktokv.com/monitor_browser/collect/batch/', 'https://mon-va.byteoversea.com/monitor_browser/collect/batch']})
        browser.execute_cdp_cmd('Network.enable', {})
        # browser.execute_cdp_cmd('Emulation.setTimezoneOverride', tz_params)
        browser.get('https://tiktok.com')
        browser.set_window_size(900, 700)
        browser.execute_script('localStorage.clear()')
        browser.execute_script('sessionStorage.clear()')
        time.sleep(random.randrange(5, 8))

        self.users = set()

    def auth(self, username: str, password: str):
        try:
            browser = self.browser
            emit = self.emit

            browser.find_element_by_xpath(
                '/html/body/div[2]/div[2]/div/div[2]/button').click()
            time.sleep(random.randrange(7, 10))
            browser.find_element_by_xpath(
                '/html/body/div[7]/div[3]/div/div/div[1]/div[1]/div/div/a[2]/div').click()
            time.sleep(random.randrange(7, 10))
            browser.find_element_by_xpath(
                '/html/body/div[7]/div[3]/div/div/div[1]/div[1]/div[2]/form/div[1]/a').click()
            time.sleep(random.randrange(7, 10))
            # browser.get('https://tiktok.com/login')
            # time.sleep(random.randrange(6, 8))
            # browser.get('https://tiktok.com/login/phone-or-email/email')
            # time.sleep(random.randrange(6, 8))
            input_username = browser.find_element_by_name('username')
            # input_password = browser.find_element_by_xpath(
            #     '/html/body/div[2]/div[2]/div[2]/div[1]/form/div[2]/div/input')
            input_password = browser.find_element_by_xpath(
                '/html/body/div[7]/div[3]/div/div/div[1]/div[1]/div[2]/form/div[2]/div/input')
            time.sleep(random.randrange(1, 2))
            input_username.send_keys(username)
            time.sleep(random.randrange(1, 2))
            input_password.send_keys(password)
            time.sleep(random.randrange(4, 5))
            input_password.send_keys(Keys.ENTER)
            time.sleep(random.randrange(15, 17))

            try:
                # browser.find_element_by_xpath(
                #     '/html/body/div[2]/div[2]/div[2]/div[1]/form/div[3]')
                browser.find_element_by_xpath(
                    '/html/body/div[7]/div[3]/div/div/div[1]/div[1]/div[2]/form/div[3]')

                time.sleep(random.randrange(2, 5))
                loops_count = 0
                while True:
                    browser.set_window_size(random.randrange(
                        800, 1000), random.randrange(600, 900))
                    browser.set_window_position(
                        random.randrange(100, 600), random.randrange(100, 200))
                    try:
                        if browser.find_element_by_class_name('captcha_verify_container'):
                            break
                    except NoSuchElementException:
                        pass
                    time.sleep(random.randrange(15, 17))
                    loops_count = loops_count + 1
                    print(loops_count)
                    # print(loops_count % 5)
                    if loops_count % 5 == 0:
                        browser.delete_all_cookies()
                        browser.execute_script('localStorage.clear()')
                        browser.execute_script('sessionStorage.clear()')
                        browser.refresh()
                        # time.sleep(random.randrange(9, 13))
                        # input_username = browser.find_element_by_name(
                        #     'username')
                        # # input_password = browser.find_element_by_xpath(
                        # #     '/html/body/div[2]/div[2]/div[2]/div[1]/form/div[2]/div/input')
                        # input_password = browser.find_element_by_xpath(
                        #     '/html/body/div[7]/div[3]/div/div/div[1]/div[1]/div[2]/form/div[2]/div/input')
                        # time.sleep(random.randrange(1, 2))
                        # input_username.send_keys(username)
                        # time.sleep(random.randrange(1, 2))
                        # input_password.send_keys(password)
                        # time.sleep(random.randrange(4, 5))
                        self.auth(username, password)
                        return
                        loops_count = 0
                    input_password.send_keys(Keys.ENTER)
                    print('loop')
                    time.sleep(random.randrange(6, 7))
                    try:
                        if browser.find_element_by_class_name('captcha_verify_container'):
                            print(1)
                            break
                    except NoSuchElementException:
                        # if not browser.find_element_by_xpath(
                        #         '/html/body/div[2]/div[2]/div[2]/div[1]/form/div[3]') and loops_count % 5 != 0:
                        #     print(2)
                        #     break
                        if not browser.find_element_by_xpath(
                                '/html/body/div[7]/div[3]/div/div/div[1]/div[1]/div[2]/form/div[3]') and loops_count % 5 != 0:
                            print(2)
                            break
            except NoSuchElementException:
                pass
            print('looped')
            time.sleep(random.randrange(6, 8))
            s = browser.find_element_by_class_name('captcha_verify_container')
            time.sleep(random.randrange(3, 5))

            outer_image = s.find_element_by_xpath(
                './/div[2]/img[1]').get_attribute('src')
            inner_image = ''
            try:
                inner_image = s.find_element_by_xpath(
                    './/div[2]/img[2]').get_attribute('src')
            except NoSuchElementException:
                browser.delete_all_cookies()
                browser.execute_script('localStorage.clear()')
                browser.execute_script('sessionStorage.clear()')
                browser.refresh()
                time.sleep(random.randrange(3, 4))
                self.auth(username, password)
                return
            print(outer_image)
            print(inner_image)
            emit("validation_slider_tiktok", {'validation_outer_image': outer_image,
                                              'validation_inner_image': inner_image})
        except TimeoutException or NoSuchElementException or WebDriverException as error:
            print(error)
            emit('message', {'status': False,
                 'content': 'Internal server error'})

    def validate_auth_scroll(self, scroll_x):
        browser = self.browser
        emit = self.emit
        try:
            # s = browser.find_element_by_class_name('captcha_verify_container')
            button = self.validation_button

            # rand_offset_x = float(decimal.Decimal(random.randrange(3, 6)))
            actions = ActionChains(browser)
            # ActionBuilder(browser)
            # actions.drag_and_drop_by_offset(
            #     button, scroll_x, 0).perform()
            # actions.pause(float(decimal.Decimal(random.randrange(1, 2))))
            actions.click_and_hold(button)
            actions.move_by_offset_duration(scroll_x, 0, 1)
            actions.perform()

            # time.sleep(random.randrange(5, 6))

        except AttributeError:
            # self.validation_button = browser.find_element_by_xpath(
            #     '/html/body/div[6]/div/div[3]/div[2]/div[2]')
            self.validation_button = browser.find_element_by_xpath(
                '/html/body/div[9]/div/div[3]/div[2]/div[2]')
            actions = ActionChains(browser)
            actions.click_and_hold(self.validation_button)
            self.validate_auth_scroll(scroll_x)

    def validate_auth_scroll_check(self):
        browser = self.browser
        emit = self.emit
        try:
            button = self.validation_button

            transform_x_string = browser.execute_script(
                "return document.evaluate('/html/body/div[6]/div/div[3]/div[2]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.style.transform")
            # print(scroll_x / 6)
            transform_x = float(transform_x_string[transform_x_string.index(
                '(') + 1: transform_x_string.index('px')])

            emit('validate_auth_scroll_check', transform_x)
        except AttributeError:
            pass

    def validate_auth_drop(self):
        browser = self.browser
        emit = self.emit
        try:
            button = self.validation_button

            actions = ActionChains(browser)
            actions.pause(float(decimal.Decimal(random.randrange(1, 2))))
            actions.release(button)
            actions.perform()
            time.sleep(4)
            try:
                s = browser.find_element_by_class_name(
                    'captcha_verify_container')
                outer_image = s.find_element_by_xpath(
                    './/div[2]/img[1]').get_attribute('src')
                inner_image = ''
                try:
                    error = browser.find_element_by_xpath(
                        '/html/body/div[6]/div/div[2]/div[2]/div[2]/div').text
                    emit('message', {'status': True, 'content': error})
                    return
                except NoSuchElementException:
                    pass
                try:
                    inner_image = s.find_element_by_xpath(
                        './/div[2]/img[2]').get_attribute('src')
                    emit("validation_slider_tiktok", {'validation_outer_image': outer_image,
                                                      'validation_inner_image': inner_image})
                    print({'validation_outer_image': outer_image,
                           'validation_inner_image': inner_image}
                          )
                    emit("message", {"status": False,
                         "content": "Something went wrong"})
                except NoSuchElementException:
                    browser.refresh()
                    time.sleep(random.randrange(3, 4))
                    # self.auth(username, password)
            except NoSuchElementException:
                pass
        except AttributeError:
            pass

    def scrape_following(self):
        browser = self.browser
        time.sleep(random.randrange(4, 7))
        browser.find_element_by_xpath(
            '/html/body/div[2]/div[1]/div/div[2]/div[4]').click()
        time.sleep(random.randrange(3, 4))
        browser.find_element_by_xpath(
            '/html/body/div[2]/div[1]/div/div[2]/div[4]/div/ul/li[1]/a').click()
        browser.set_window_size(1150, 700)
        while True:
            following_accounts_list = browser.find_element_by_xpath(
                '/html/body/div[2]/div[2]/div[1]/div/div[2]/div/div[1]/div[4]/div')
            see_more_button_possible_list = browser.find_elements_by_xpath(
                '/html/body/div[2]/div[2]/div[1]/div/div[2]/div/div[1]/div[4]/div').text
            see_more_button = None
            for button in see_more_button_possible_list:
                try:
                    see_more_button = button.find_element_by_xpath('.//p').text
                    break
                except NoSuchElementException:
                    continue
            if (see_more_button.lowerCase() == 'see less'):
                break
            for account in following_accounts_list:
                username = account.find_element_by_xpath('.//a[2]/div/h4').text
                self.users.add(username)

    def send_messages(self):
        browser = self.browser
        time.sleep(random.randrange(4, 6))
        messages = ['Hello {}, this for testing', 'Hi {}, this is for testing',
                    'Hallo {}, das ist für testing', 'Hola {}, esto es para testear']
        for account in self.users:
            browser.get('https://www.tiktok.com/@{}'.format(account))
            time.sleep(random.randrange(4, 6))
            message_button = browser.find_element_by_xpath(
                '/html/body/div[2]/div[2]/div[2]/div/div[1]/div[1]/div[2]/div/div[2]/a/button')
            if (message_button.text.lowerCase() == 'messages'):
                message_button.click()
                time.sleep(random.randrange(4, 6))
                input = browser.find_element_by_xpath(
                    '/html/body/div[2]/div[2]/div/div[2]/div[3]/div/div[1]/div/div/div[2]/div')
                input.click()

                def replace(message):
                    return message.format(account)

                messages_to_send = []

                for message in messages:
                    messages_to_send.append(replace(message=message))

                message_to_send = random.choice(messages_to_send)

                input.send_keys(message_to_send)
                input.send_keys(Keys.ENTER)
                time.sleep(random.randrange(4, 7))
                input.clear()
                time.sleep(random.randrange(12, 15))
            else:
                continue

    def quit(self):
        self.browser.quit()
