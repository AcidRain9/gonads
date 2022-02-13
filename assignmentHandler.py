import random
from enum import Enum


class Status(Enum):
    all_students_submitted = 1,
    no_student_submitted = 0,
    some_students_submitted = 10


def random_positive_index(array):
    new_list = list(array)
    i = random.choice(range(len(new_list)))
    while array[i] != 1:
        random.shuffle(new_list)
        i = random.choice(range(len(new_list)))
    return i


def check_assignment_submission_statuses(array):
    new_list = list(array)
    res = all(ele == new_list[0] for ele in new_list)
    if res:
        if new_list[0] == 0:
            print("All have not submitted")
            return Status.no_student_submitted
        elif new_list[0] == 1:
            print("All have submitted")
            return Status.all_students_submitted
    else:
        print("Some Users have not submitted")
        return Status.some_students_submitted


def get_students_who_submitted(array):
    status = check_assignment_submission_statuses(array)
    students_who_submitted_list = []
    if status == Status.some_students_submitted:
        for index, x in enumerate(array):
            if x == 1:
                students_who_submitted_list.append(index)
    if status == status.some_students_submitted:
        print(students_who_submitted_list)
        return students_who_submitted_list


def get_students_who_did_not_submit(array):
    status = check_assignment_submission_statuses(array)
    students_who_did_not_submit_list = []
    if status == Status.some_students_submitted:
        for index, x in enumerate(array):
            if x == 0:
                students_who_did_not_submit_list.append(index)
    if status == status.some_students_submitted:
        print(students_who_did_not_submit_list)
        return students_who_did_not_submit_list


# lst = (0, 1, 0, 1)
# get_students_who_submitted(lst)
# get_students_who_did_not_submit(lst)
# print(random_positive_index(lst))
def download_assignments():
    print("Download Assignments")
    # todo download assignments
    # todo add comments to explain the logic of functions
