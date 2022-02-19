import os
import random
from enum import Enum
import shutil
# Remove the imports below, handle all logic in browserHandler

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import re
from browserHandler import SetupBrowser
import logins as ac
import base64
import elements as xpath
from glob import glob


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


def prepare_assignment_file(directory, index):
    # Find file in directory
    project_files = glob(directory + "*.docx") + glob(directory + "*.pdf")
    print(project_files)
    assignment = project_files[0]
    assignment = assignment.replace(directory, "")
    print(assignment)
    # Removing names and ids from assignment name
    lexicals = ["Arbaz", "Ahmed", "Mughal", "Hira", "Sher", "Saad", "Muhammad", "M\.", "Mohammad",
                ".Sadeeq"] + ac.ids + ac.students
    for lexical in lexicals:
        pattern = re.compile(lexical, re.IGNORECASE)
        assignment = pattern.sub("", assignment)
    final = assignment.strip()
    print(final)
    shutil.copy('/etc/hostname', '/var/tmp/testhostname')
    os.rename(project_files[0], directory+final)


def upload_assignment_student(array, assignment):
    status = check_assignment_submission_statuses(array)
    if status == Status.some_students_submitted:
        nally_students = get_specific_students_who_did_not_submit(array)
        for student in nally_students:
            browser = SetupBrowser()
            browser.login(ac.ids[student], base64.b64decode(ac.paswds[student]).decode("utf-8"))
            assignment_upload_link = browser.fetch_assignment_upload_link(assignment)
            browser.upload_given_assignment(assignment_upload_link, "IT3161 Assignment 1.docx")
            print("Uploaded Assignment of" + ac.ids[student])
    elif status == Status.all_students_submitted:
        print("All students have submitted the Assignment")
    elif status == Status.no_student_submitted:
        print("No student submitted")
    else:
        print("unknown error")
