from decal import db
from decal import gdrive

labid = input('What lab do you wanna see (a1, b2, etc): ').strip()

lab = next(lab for lab in db.get_labs() if lab.name == labid)

if not lab.responses_gdoc:
    gdoc_url = input('Enter the responses spreadsheet for this lab ').strip()

    responses = gdrive.read_spreadsheet(gdoc_url)

    db.update_lab_gdoc(lab.id, gdoc_url)
else:
    responses = gdrive.read_spreadsheet(lab.responses_gdoc)


