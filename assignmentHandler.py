import os
import random
from enum import Enum
import shutil
import databaseHandler
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
        print("No file to Download - All students have submitted the Assignment")
    elif status == Status.no_student_submitted:
        print("No file to Download - No student submitted")
    else:
        print("Download - unknown error")


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
    final_filename = assignment.strip()
    extension = ""
    if ".docx" in final_filename:
        extension = ".docx"
    else:
        extension = ".pdf"
    final_filename = final_filename.replace(".docx", "")
    final_filename = final_filename.replace(".pdf", "")
    print(final_filename)
    # saving file
    final_filename = directory + final_filename + " - " + ac.students[index] + " " + ac.ids[index] + extension
    shutil.copy(project_files[0], final_filename)
    return final_filename


def remove_assignment_file(assignment_file):
    if os.path.isfile(assignment_file):
        os.remove(assignment_file)
    else:
        print("The file does not exist")


def upload_assignment_student(array, assignment_link):
    status = check_assignment_submission_statuses(array)
    if status == Status.some_students_submitted:
        nally_students = get_specific_students_who_did_not_submit(array)
        for student in nally_students:
            browser = SetupBrowser()
            browser.login(ac.ids[student], base64.b64decode(ac.paswds[student]).decode("utf-8"))
            assignment_upload_link = browser.fetch_assignment_upload_link(assignment_link)
            directory = browser.prefs.get("download.default_directory")
            print(directory)
            filex = prepare_assignment_file(directory + "/", student)
            print(filex)
            browser.upload_given_assignment(assignment_upload_link, filex)
            print("Uploaded Assignment of " + ac.ids[student] + " " + assignment_link)
            databaseHandler.update_student_assign_status_to_positive(ac.students[student], assignment_link)
            remove_assignment_file(filex)
    elif status == Status.all_students_submitted:
        print("No file to Upload - All students have submitted the Assignment")
    elif status == Status.no_student_submitted:
        print("No file to Upload - No student submitted")
    else:
        print("Upload - unknown error")
