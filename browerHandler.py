import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import logins as ac
from bs4 import BeautifulSoup
import re


class SetupBrowser:

    # Setting up Google Chrome/Chromium Instance
    def __init__(self):
        self.op = Options()
        self.op.add_argument("start-maximized")
        self.op.add_argument("--incognito")
        self.op.add_experimental_option("excludeSwitches", ['enable-automation'])
        prefs = {
            'profile.managed_default_content_settings.images': 2,
            'profile.managed_default_content_settings.javascript': 2
        }
        self.op.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(options=self.op)

    def login(self, studentid, passwords):
        # Finding Login Fields
        self.driver.get("https://sktlms.umt.edu.pk/")
        _id = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='username']")))
        _pass = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='password']")))
        _loginbtn = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='loginbtn']")))
        # Passing login data
        _id.send_keys(studentid)
        _pass.send_keys(passwords)
        _loginbtn.click()

    # fetch links
    def fetch_links(self):
        # load course
        self.driver.get(ac.course1)
        # Finding Assignment  Links
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        assignments = soup.find_all('a',
                                    href=re.compile("https://sktlms\.umt\.edu\.pk/moodle/mod/assign/view\.php\?id="))
        return assignments

    def visit(self, link):
        self.driver.get(link)

    def exit(self):
        self.driver.quit()

    def restart(self):
        self.exit()
        time.sleep(2)
        self.driver = webdriver.Chrome(options=self.op)
