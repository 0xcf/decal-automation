import csv
import io

from google.oauth2 import service_account
import googleapiclient.discovery

from decal.config import config

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

credentials = service_account.Credentials.from_service_account_file(
    config.google_creds_path,
    scopes=SCOPES,
)

drive = googleapiclient.discovery.build(
    'drive',
    'v3',
    credentials=credentials
)

def url_to_fileid(url):
    """Converts a Google Spreadsheet URL to just its file ID"""
    if url.startswith('http://') or url.startswith('https://'):
        return url.split('/')[5]
    else:
        return url

def read_spreadsheet(spreadsheet_url):
    fileid = url_to_fileid(spreadsheet_url)

    response_bytes = drive.files().export(fileId=fileid, mimeType='text/csv').execute()
    response_io = io.StringIO(response_bytes.decode())
    return csv.DictReader(response_io)
