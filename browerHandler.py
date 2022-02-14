import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import logins as ac
import os.path
from bs4 import BeautifulSoup
import elements as xpath
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
            'profile.managed_default_content_settings.javascript': 2,
            "download.default_directory": "/home/arbaz/Documents/assignments"
        }
        self.op.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(options=self.op)

    def login(self, studentid, passwords):
        # Finding Login Fields
        self.driver.get("https://sktlms.umt.edu.pk/")
        _id = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, xpath.username)))
        _pass = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, xpath.password)))
        _loginbtn = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, xpath.login_btn)))
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

    def get_submission_status(self):
        status = self.driver.find_element(By.XPATH, xpath.submission_status).text
        return status

    def assignment_download_manager(self, url):
        script = '''window.open("{0}","_blank");'''
        script = script.format(url[0])
        self.driver.execute_script(script)
        p = "/home/arbaz/Documents/assignments/{0}"
        path = p.format(url[1])
        while not os.path.exists(path):
            time.sleep(2)

    def fetch_assignment_link(self, assignment):
        assignment_link_and_name = []
        self.driver.get(assignment)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        download_link = soup.find_all('a',
                                      href=re.compile("https://sktlms\.umt\.edu\.pk/moodle/pluginfile\.php/"))

        for dl in download_link:
            assignment_link_and_name.append(dl['href'])
            assignment_link_and_name.append(dl.get_text())
        return assignment_link_and_name

# todo implement functions to download assignment
