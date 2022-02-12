from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import re
import logins as ac
import base64
import sqlite3

# Setting up Google Chrome/Chromium Instance
op = Options()
op.add_argument("start-maximized")
op.add_argument("--incognito")
op.add_experimental_option("excludeSwitches", ['enable-automation'])
prefs = {
    'profile.managed_default_content_settings.images': 2,
    'profile.managed_default_content_settings.javascript': 2
}
op.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=op)

# Finding Login Fields
driver.get("https://sktlms.umt.edu.pk/")
_id = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@id='username']")))
_pass = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@id='password']")))
_loginbtn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='loginbtn']")))

# Passing login data
_id.send_keys(ac.ids[0])
_pass.send_keys(base64.b64decode(ac.paswds[0]).decode("utf-8"))
_loginbtn.click()

# Loading course
driver.get(ac.course1)

# Finding Assignment  Links
soup = BeautifulSoup(driver.page_source, 'html.parser')
assignments = soup.find_all('a', href=re.compile("https://sktlms\.umt\.edu\.pk/moodle/mod/assign/view\.php\?id="))

# Connect to database
conn = sqlite3.connect('assignments1.db')

# Prepare the CREATE TABLE query
tmp = ""
for x in ac.students:
    tmp += x + " INTEGER DEFAULT (0), "
tmp = tmp[:-2]
query = "CREATE TABLE IF NOT EXISTS test(ID INTEGER PRIMARY KEY AUTOINCREMENT,Assignments TEXT UNIQUE,{0}" + ");"
query = query.format(tmp)

# Executing query
conn.execute(query)

# Adding Assignment Links to DB
for assignment in assignments:
    tmp = "INSERT OR IGNORE INTO test(Assignments) VALUES ('{0}');"
    query = tmp.format(assignment['href'])
    conn.execute(query)

# Commit Changes to DB
conn.commit()

# Parsing Assignments Per User
tmp = "SELECT Assignments,{0} FROM test"
for student in ac.students:
    query = tmp.format(student)
    result = conn.execute(query).fetchall()
    print(student)
    for row in result:
        if row[1] == 0:
            driver.get(row[0])
            tmp2 = "UPDATE test SET {0} = 1 WHERE Assignments = '{1}'"
            query2 = tmp2.format(student, row[0])
            conn.execute(query2)
            conn.commit()
