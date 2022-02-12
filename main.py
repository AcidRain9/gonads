import logins as ac
import base64
import sqlite3
from browerHandler import SetupBrowser

browser = SetupBrowser()
browser.login(ac.ids[0], base64.b64decode(ac.paswds[0]).decode("utf-8"))
assignments = browser.fetch_links()

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
            browser.visit(row[0])
            tmp2 = "UPDATE test SET {0} = 1 WHERE Assignments = '{1}'"
            query2 = tmp2.format(student, row[0])
            conn.execute(query2)
            conn.commit()
