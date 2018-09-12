from collections import namedtuple

import pymysql

from decal.config import config

Checkoff = namedtuple('Checkoff', ['id', 'facilitator', 'lab', 'student', 'timestamp'])
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

def get_checkoffs():
    with db as c:
        c.execute('SELECT checkoffs.id, checkoffs.facilitator, checkoffs.lab, checkoffs.student, checkoffs.timestamp FROM checkoffs inner join semester on semester.name=%s where checkoffs.semester=semester.id', (config.semester))
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
