import sqlite3

conn = sqlite3.connect('assignments1.db')


def update_student_assign_status_to_positive(student_name, assignment_link):
    query = "UPDATE test SET {0} = 1 WHERE Assignments = '{1}'"
    query = query.format(student_name, assignment_link)
    conn.execute(query)
    conn.commit()

