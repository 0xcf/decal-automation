#!/usr/bin/env python3
# Contains utility scripts for seeing which labs need to be checked off.
# When executed, lists this information.

from collections import defaultdict
import sys

from decal import checkoff
from decal import db
from decal import gdrive

# Maps (student, lab) to the datetime of the latest submission
last_submission_time = {}
for lab in db.get_labs():
    if not lab.responses_gdoc:
        continue
    
    for response in list(gdrive.read_spreadsheet(lab.responses_gdoc))[1:]:
        # If there is a score column, username is in fourth column, otherwise third
        if ' / ' in response[2]:
            username = response[3]
        else:
            username = response[2]
        if not username:
            continue
        username = username.lower()
        last_submission_time[(username, lab.name)] = gdrive.parse_datetime(response[0])

# Maps (student, lab) to the most recent checkoff they've had
latest_checkoff = {}

for co in checkoff.get_checkoffs_sheet():
    sl = (co.username, co.labid)

    # If this student was checked off, we don't have to worry about their later
    # submissions.
    if co.correct and sl in last_submission_time:
        del last_submission_time[sl]
        continue

    latest_checkoff[sl] = co.timestamp

def pending_labs():
    """
    Returns a dictionary mapping lab to a list of (timestamp, student) pairs
    that are pending checkoff.
    """

    p = defaultdict(list)
    for sl, timestamp in last_submission_time.items():
        if sl not in latest_checkoff or timestamp > latest_checkoff[sl]:
            p[sl[1]].append((timestamp, sl[0]))

    return p

def main():
    for lab, pairs in sorted(pending_labs().items()):
        print('({}) {} - {}'.format(len(pairs), lab, ', '.join(db.facilitator_labs(lab))))
        for pair in pairs:
            print('{} {}'.format(*pair))
        print()

if __name__ == '__main__':
    sys.exit(main())

