#!/usr/bin/env python3
# Emails facilitators reminding them to check off their labs.

from textwrap import dedent
import sys

from ocflib.misc.mail import email_for_user
from ocflib.misc.mail import send_mail

from decal import db
from pending_labs import pending_labs

template = dedent('''
Hi {names},

You have pending decal lab submissions for lab {lab}. Please complete your
checkoffs as soon as possible.

{submissions}
''').strip()

def main():
    for lab, pairs in pending_labs().items():
        facilitators = db.facilitator_labs(lab)
        emails = [email_for_user(f) for f in facilitators]

        submissions_txt = '\n'.join('{} {}'.format(*p) for p in pairs)
        body = template.format(
                names=', '.join(facilitators),
                lab=lab,
                submissions=submissions_txt,
        )

        send_mail(
            to=', '.join(emails),
            subject='Decal Checkoff Reminder for lab {}'.format(lab),
            body=body,
            sender='decal@ocf.berkeley.edu',
        )


if __name__ == '__main__':
    sys.exit(main())

