# google drive api imports
from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account
# random number
import secrets


creds = None

# MAYBE REMOVE DRIVE.FILE EW
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/drive.file']

SERVICE_ACCOUNT_FILE = 'credentials.json'

# MAKE THIS NOT SUCK MAYBE? USE FOLDER NAME FOR EASE OF SETUP
COMPLETED_FOLDER_ID = '1e6WGPJjOCfndBGvP7KLKi6H7xB2gKYuc'
PENDING_APPROVAL_FOLDER_ID = '1X8D5v4MNkvv5wYYpXVGTPE7c--9XOeXR'
PENDING_REVIEW_FOLDER_ID = '1uFleH0-Rznf_IpEZR8n3Czs0zau7od3V'
OVERFLOW_REVIEW_FOLDER_ID = '1eQWxGiI7EovoENa4CwbSDuP-RTmTwLbT'
BLANK_TRANSCRIPT_ID = '1O_937zukto10_pUEQQZkKtwvuIRHp7tg'
JPG_FOLDER_ID = '1jfNrqneyBHqvvABZ319If-i7xq8ERT1k'
# SEE ABOVE

jpg_file_id = None
jpg_file_name = None
jpg_view_link = None

txt_file_id = None
txt_file_name = None
txt_file_content = None

# ACTUALLY NEEDED IG
SHARED_DRIVE_ID = '0AD484V2JtzcFUk9PVA'

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# google drive api
service = build('drive', 'v3', credentials=creds)

docs_service = build('docs', 'v1', credentials=creds)

# ON PAGE LOAD:
def get_transcription():
    results = service.files().list(pageSize = 10, q="'{0}' in parents and name contains '.JPG'".format(PENDING_APPROVAL_FOLDER_ID), fields='files/webViewLink, nextPageToken, files(name, id)', driveId=SHARED_DRIVE_ID, corpora='drive', includeItemsFromAllDrives=True, supportsAllDrives=True).execute()
    # print(results)
    jpg_list = results.get('files', [])
    if not jpg_list:
        print('No files found')
    else:
        jpg_list = secrets.choice(jpg_list)
        global jpg_file_id
        global jpg_file_name
        global jpg_view_link
        jpg_file_id = u'{0}'.format(jpg_list['id'])
        jpg_file_name = u'{0}'.format(jpg_list['name'])
        # REMOVES EVERYTHING AFTER /view in URL AND APPENDS /preview
        jpg_view_link = u'{0}'.format(jpg_list['webViewLink']).split("/view")[0] + "/preview"

        get_transcription_txt()


def get_transcription_txt():
    global txt_file_name
    txt_file_name = jpg_file_name.split('.JPG')[0] + ".txt"
    results = service.files().list(pageSize=1, q="'{0}' in parents and name='{1}' and name contains '.txt'".format(PENDING_APPROVAL_FOLDER_ID, txt_file_name), fields='files(id)', driveId=SHARED_DRIVE_ID, corpora='drive', includeItemsFromAllDrives=True, supportsAllDrives=True).execute()
    txt_list = results.get('files')
    if not txt_list:
        print('No files found')
    else:
        for item in txt_list:
            txt_list = item
        global txt_file_id
        txt_file_id = u'{0}'.format(txt_list['id'])
        read_txt_file(txt_file_id)


def read_txt_file(file_id):
    results = service.files().export(
    fileId=file_id,
    mimeType='text/plain').execute()
    global txt_file_content

    txt_file_content = results.decode("utf-8")



def get_file_description(file_id):
    file = service.files().get(
        fileId=file_id,
        fields='description',
        supportsAllDrives=True
        ).execute()
    
    # CATCH EXCEPTION IF 'PROPERTIES' IS NULL OH JEEZ UR GONNA MESS THIS UP
    x = file['description']
    return(x)


# SEE LAST LINE, IMPLEMENT
def approve_transcription(file_id, jpg_id):
    file = service.files().update(fileId=file_id,
                            addParents=COMPLETED_FOLDER_ID,
                            removeParents=PENDING_APPROVAL_FOLDER_ID,
                            fields='id, description, parents', supportsAllDrives="true").execute()

    file2 = service.files().update(fileId=jpg_id,
                            addParents=COMPLETED_FOLDER_ID,
                            removeParents=PENDING_APPROVAL_FOLDER_ID,
                            fields='id, description, parents', supportsAllDrives="true").execute()


def disapprove_transcription(file_id, jpg_id):
    result = service.files().update(
        fileId=file_id,
        body={
        'description':0},
        supportsAllDrives=True
        ).execute()

    file = service.files().update(fileId=file_id,
                            addParents=PENDING_REVIEW_FOLDER_ID,
                            removeParents=PENDING_APPROVAL_FOLDER_ID,
                            fields='id, description, parents', supportsAllDrives="true").execute()

    file2 = service.files().update(fileId=jpg_id,
                            addParents=PENDING_REVIEW_FOLDER_ID,
                            removeParents=PENDING_APPROVAL_FOLDER_ID,
                            fields='id, description, parents', supportsAllDrives="true").execute()
