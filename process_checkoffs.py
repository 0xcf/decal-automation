from textwrap import dedent
import traceback

from ocflib.misc.mail import email_for_user
from ocflib.misc.mail import send_mail

from decal import checkoff
from decal import db
from decal import gdrive

checkoffs_sheet_url = db.get_checkoffs_sheet()
checkoffs_sheet = gdrive.read_spreadsheet(checkoffs_sheet_url)

stored_checkoffs = db.get_checkoffs()
stored_rowids = {c.row_id for c in stored_checkoffs}

template = dedent('''
Hi {name},

{correct_sentence}

{facilitator} left the following comments:

{feedback}
''').strip()

for co in checkoff.get_checkoffs_sheet():
    try:
        if co.rowid in stored_rowids:
            continue

        if co.correct:
            sentence = 'Congratulations, you were checked off for lab {}.'
        else:
            sentence = 'Unfortunately you were not checked off for lab {}.'

        sentence = sentence.format(co.labid)

        full_text = template.format(name=co.username, correct_sentence=sentence, facilitator=co.facilitator, feedback=co.feedback)

        to_email = email_for_user(co.username)

        try:
            cursor = db.get_cursor()
            checkoff.insert_into_db(cursor, co)
        except:
            db.db.rollback()
            db.db.close()
            raise
        else:
            db.db.commit()

            # send the email
            send_mail(
                to=to_email,
                subject='[Decal] Feedback on lab {}'.format(co.labid),
                body=full_text,
                cc='decal+checkoffs@ocf.berkeley.edu',
                sender='decal@ocf.berkeley.edu',
            )

    except Exception as err:
        # Subtract 1 from the rowid to cancel out the first header row. This will print the actual row when looking at the google doc
        print('Error on row {} (facilitator: {})'.format(co.rowid - 1, co.facilitator))
        traceback.print_tb(err.__traceback__)
