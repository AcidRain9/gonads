import random
from enum import Enum

# Remove the imports below, handle all logic in browserHandler

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import re
from browserHandler import SetupBrowser
import logins as ac
import base64
import elements as xpath


class Status(Enum):
    all_students_submitted = 1,
    no_student_submitted = 0,
    some_students_submitted = 10


def select_random_student(array):
    new_list = list(array)
    random.shuffle(new_list)
    i = random.choice(new_list)
    return i


def check_assignment_submission_statuses(array):
    new_list = list(array)
    res = all(ele == new_list[0] for ele in new_list)
    if res:
        if new_list[0] == 0:
            #            print("All have not submitted")
            return Status.no_student_submitted
        elif new_list[0] == 1:
            #            print("All have submitted")
            return Status.all_students_submitted
    else:
        #        print("Some Users have not submitted")
        return Status.some_students_submitted


def get_specific_students_who_submitted(array):
    status = check_assignment_submission_statuses(array)
    students_who_submitted_list = []
    if status == Status.some_students_submitted:
        for index, x in enumerate(array):
            if x == 1:
                students_who_submitted_list.append(index)
    if status == status.some_students_submitted:
        print(students_who_submitted_list)
        return students_who_submitted_list


def get_specific_students_who_did_not_submit(array):
    status = check_assignment_submission_statuses(array)
    students_who_did_not_submit_list = []
    if status == Status.some_students_submitted:
        for index, x in enumerate(array):
            if x == 0:
                students_who_did_not_submit_list.append(index)
    if status == status.some_students_submitted:
        print(students_who_did_not_submit_list)
        return students_who_did_not_submit_list


def download_assignment_student(array, assignment):
    status = check_assignment_submission_statuses(array)
    if status == Status.some_students_submitted:
        x = get_specific_students_who_submitted(array)
        i = select_random_student(x)
        browser = SetupBrowser()
        browser.login(ac.ids[i], base64.b64decode(ac.paswds[i]).decode("utf-8"))
        get_link = browser.fetch_assignment_download_link(assignment)
        browser.assignment_download_manager(get_link)
        print(i)
    elif status == Status.all_students_submitted:
        print("All students have submitted the Assignment")
    elif status == Status.no_student_submitted:
        print("No student submitted")
    else:
        print("unknown error")


# Proof of Concept

browser = SetupBrowser()
directory = browser.prefs.get("download.default_directory")
file = "1. Course Introduction..mp4"


def upload_assignment(assignment):
    assignment += "&action=editsubmission"
    browser.visit(assignment)
    soup = BeautifulSoup(browser.driver.page_source, 'html.parser')
    draft_manager = soup.find('object',
                              data=re.compile(
                                  "https://sktlms\.umt\.edu\.pk/moodle/repository/draftfiles_manager\.php\?env=filemanager&action=browse&itemid="))
    draft_manager = draft_manager.get('data')
    filepicker = draft_manager.replace("draftfiles_manager.php", "filepicker.php")
    filepicker += "&action=list&draftpath=%2F&savepath=%2F&repo_id=4"
    browser.visit(filepicker)
    upload_dialog = browser.driver.find_element(By.XPATH, xpath.choose_file)
    print(browser.prefs.get("download.default_directory"))
    print(directory + "/" + file)
    upload_dialog.send_keys(directory + "/" + file)
    upload_button = browser.driver.find_element(By.XPATH, xpath.upload_button)
    upload_button.click()
    browser.visit("https://sktlms.umt.edu.pk/moodle/mod/assign/view.php?id=217247&action=editsubmission")
