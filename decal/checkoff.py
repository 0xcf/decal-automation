from collections import namedtuple

from decal import db
from decal import gdrive

CheckoffRow = namedtuple(
    'CheckoffRow',
    ['rowid', 'timestamp', 'facilitator', 'labid', 'username', 'correct', 'feedback']
)

def get_checkoffs_sheet():
    """Get a list of CheckoffRows from the GDrive spreadsheet."""

    checkoffs_sheet_url = db.get_checkoffs_sheet()
    checkoffs_sheet = gdrive.read_spreadsheet(checkoffs_sheet_url)

    # The first element is the labels, which we will ignore
    checkoffs = list(checkoffs_sheet)[1:]

    return [
        CheckoffRow(
            # Add one to offset the labels row that was ignore
            rowid = n+1,
            timestamp = gdrive.parse_datetime(c[0]),
            facilitator = c[1].split('@')[0],
            labid = c[2],
            username = c[3],
            correct = c[4].lower().startswith('yes'),
            feedback = c[5],
        )
        for n, c in enumerate(checkoffs)
        if c[0]
    ]

def insert_into_db(cursor, checkoff):
    db.insert_checkoff(
        cursor,
        timestamp=checkoff.timestamp,
        student=checkoff.username,
        lab=checkoff.labid,
        facilitator=checkoff.facilitator,
        correct=checkoff.correct,
        row_id=checkoff.rowid,
    )
