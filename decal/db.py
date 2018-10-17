from collections import namedtuple

import pymysql

from decal.config import config

Checkoff = namedtuple('Checkoff', ['id', 'facilitator', 'lab', 'student', 'timestamp', 'correct', 'row_id'])
Facilitator = namedtuple('Facilitator', ['id', 'name', 'username'])
Lab = namedtuple('Lab', ['id', 'name', 'fullname', 'track', 'responses_gdoc'])
Student = namedtuple('Student', ['id', 'email', 'track', 'username'])

db = pymysql.connect(
    user=config.db_user,
    password=config.db_pass,
    db=config.db_dbname,
    host=config.db_host,
    cursorclass=pymysql.cursors.DictCursor,
    charset='utf8mb4',
    autocommit=True,
)

def get_cursor():
    return db.cursor()

def get_checkoffs():
    """Get the list of checkoffs that have been recorded in the database."""
    with db as c:
        c.execute('SELECT checkoffs.id, checkoffs.facilitator, labs.name as lab, checkoffs.student, checkoffs.timestamp, checkoffs.correct, checkoffs.row_id FROM checkoffs inner join labs on labs.id=checkoffs.lab inner join semester on semester.name=%s where labs.semester=semester.id', (config.semester))
        return [Checkoff(**l) for l in c]

def get_labs():
    with db as c:
        c.execute('SELECT labs.id, labs.name, labs.fullname, labs.track, labs.responses_gdoc FROM labs inner join semester on semester.name=%s where labs.semester=semester.id', (config.semester))
        return [Lab(**l) for l in c]

def get_students():
    with db as c:
        c.execute('SELECT students.id, students.email, students.track, students.username FROM students inner join semester on semester.name=%s where students.semester=semester.id', (config.semester))
        return [Student(**l) for l in c]

def get_facilitators():
    with db as c:
        c.execute('SELECT facilitator.id, facilitator.name, facilitator.username FROM facilitator')
        return [Facilitator(**l) for l in c]

def get_attendance_sheet():
    """Get the URL of the attendance sheet for the current semester."""
    with db as c:
        c.execute('SELECT attendance_sheet FROM semester WHERE name=%s', (config.semester,))
        return c.fetchone()['attendance_sheet']

def get_checkoffs_sheet():
    """Get the URL of the checkoffs sheet for the current semester."""
    with db as c:
        c.execute('SELECT checkoffs_sheet FROM semester WHERE name=%s', (config.semester,))
        return c.fetchone()['checkoffs_sheet']

def insert_checkoff(cursor, timestamp, student, lab, facilitator, correct, row_id):
    cursor.execute('INSERT INTO checkoffs (timestamp, student, facilitator, correct, row_id, lab) values (%s, %s, %s, %s, %s, (select labs.id from labs inner join semester on semester.name=%s where labs.semester=semester.id and labs.name=%s))',
        (timestamp, student, facilitator, correct, row_id, config.semester, lab)
    )

def update_lab_gdoc(lab_dbid, gdoc_url):
    with db as c:
        c.execute('UPDATE labs SET responses_gdoc = %s where id=%s', (gdoc_url, lab_dbid))
