import time
import re
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver

class MySeleniumTests(StaticLiveServerTestCase):

    fixtures = ['user-data.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_basic(self):
        # GET request to initial page
        self.selenium.get(self.live_server_url)
        username = 'test_one'
        password = 'test_for_pass'
        time.sleep(2)

        # click set up
        first_link = self.selenium.find_elements_by_css_selector("a")[0]
        first_link.click()
        time.sleep(1)
        
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(username)
        time.sleep(1)

        # input register data
        email_input = self.selenium.find_element_by_name("email")
        email_input.send_keys('test_one@gmail.com')
        time.sleep(1)

        birthdate_input = self.selenium.find_element_by_name("BirthDate")
        birthdate_input.send_keys('21/02/1999')
        time.sleep(1)

        password_input = self.selenium.find_element_by_name("password1")
        password_input.send_keys(password)
        time.sleep(1)

        password2_input = self.selenium.find_element_by_name("password2")
        password2_input.send_keys(password)
        time.sleep(1)

        self.selenium.find_element_by_xpath('//button[text()="Register"]').click()
        time.sleep(1)
        
        #login the user
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(username)
        time.sleep(1)

        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(password)
        time.sleep(1)

        self.selenium.find_element_by_xpath('//button[text()="Login"]').click()
        time.sleep(2)

        #go to an article
        article_link = self.selenium.find_elements_by_css_selector("a")[5]
        article_link.click()
        time.sleep(2)

        #like this article
        like_button = self.selenium.find_element_by_id("like")
        like_button.click()
        time.sleep(2)

        #post a comment
        comment_area = self.selenium.find_element_by_name("content")
        comment_area.send_keys('testing')
        time.sleep(2)
        comment_post = self.selenium.find_element_by_id("post_button")
        comment_post.click()
        time.sleep(2)

        #delete the comment
        comment_del = self.selenium.find_element_by_name("comment-delete-btn")
        comment_del.click()
        time.sleep(2)