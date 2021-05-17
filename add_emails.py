"""Gets an email, student csv from stdin and associates emails with students."""
from sys import stdin

from decal import db

email_names = [tuple(l.strip().split()) for l in stdin]

assert all(len(t) == 2 for t in email_names)
assert all('@' in email for email, _ in email_names)
assert all('@' not in username for _, username in email_names)

students_db = db.get_students()

for email, username in email_names:
    with db.db as c:
        if not any(student.username == username for student in students_db):
            print('User {} not in database'.format(username))
        c.execute('UPDATE students SET email=%s WHERE username=%s', (email, username))

print('Students without emails:')
students_db = db.get_students()
for student in students_db:
    if not student.email:
        print(student.username)
