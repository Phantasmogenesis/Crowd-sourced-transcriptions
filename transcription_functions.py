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
PENDING_REVIEW_FOLDER_ID = '1uFleH0-Rznf_IpEZR8n3Czs0zau7od3V'
OVERFLOW_REVIEW_FOLDER_ID = '1eQWxGiI7EovoENa4CwbSDuP-RTmTwLbT'
BLANK_TRANSCRIPT_ID = '1O_937zukto10_pUEQQZkKtwvuIRHp7tg'
JPG_FOLDER_ID = '10ABcW2n70qS28LcJXpbafjuv44AM1lAl'
# SEE ABOVE

jpg_file_id = None
jpg_file_name = None
jpg_view_link = None

txt_file_id = None
txt_file_name = None

# ACTUALLY NEEDED IG
SHARED_DRIVE_ID = '0AD484V2JtzcFUk9PVA'

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# google drive api
service = build('drive', 'v3', credentials=creds)

docs_service = build('docs', 'v1', credentials=creds)

# ON PAGE LOAD:
def get_random_jpg():
    results = service.files().list(pageSize = 5, q="'{0}' in parents".format(JPG_FOLDER_ID), fields='files/webViewLink, nextPageToken, files(name, id)', driveId=SHARED_DRIVE_ID, corpora='drive', includeItemsFromAllDrives=True, supportsAllDrives=True).execute()
    # print(results)
    jpg_list = results.get('files', [])
    if not jpg_list:
        print(jpg_list)
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


def create_file(data):
    # MAKE THIS TAKE INPUT PARAMETER FOR FILE NAME?
    if jpg_file_id != None:
        global text_file_name
        text_file_name = jpg_file_name.split('.JPG')[0] + ".txt"
        file = service.files().create(body={
            'name': text_file_name,
            'description': 0,
            'parents': [PENDING_REVIEW_FOLDER_ID],
            'mimeType': 'application/vnd.google-apps.document',
        }, fields='id', supportsAllDrives="true").execute()

        global text_file_id
        text_file_id = (u'{0}'.format(file['id']))
        # print((u'{0}'.format(file['properties'])))
    
        # WRITE METADATA FIELDS FOR LIBRARIAN
        requests = [
            {
                'insertText': {
                'location': {
                    'index': 1,
                },
                'text': data
            }
        }]

        docs_service.documents().batchUpdate(
            documentId=(u'{0}'.format(file['id'])),
            body={'requests': requests}
        ).execute()

        file = service.files().update(fileId=jpg_file_id,
                                        addParents=PENDING_REVIEW_FOLDER_ID,
                                        removeParents=JPG_FOLDER_ID,
                                        fields='id, parents', supportsAllDrives="true").execute()




# THIS IS NOT WORKING. CHANGE TO USE DRIVE API CREATE METHOD OR SOMETHING
# WTF THIS IS WORKING NOW? FILE NEEDS TO BE MADE BY USER??????????????????


# def write_to_file(data):
#     requests = [
#      {
#         'insertText': {
#             'location': {
#                 'index': 1,
#             },
#             'text': data + "\n\n"
#         }
#     }]

#     docs_service.documents().batchUpdate(
#         documentId=txt_file_id,
#         body={'requests': requests}
#     ).execute()






# NEXT: MOVE TO OVERFLOW IF PENDING REVIEW CONTAINS TOO MANY FILES

def get_file_description(file_id):
    file = service.files().get(
        fileId=file_id,
        fields='description',
        supportsAllDrives=True
        ).execute()
    
    # CATCH EXCEPTION IF 'PROPERTIES' IS NULL OH JEEZ UR GONNA MESS THIS UP
    x = file['description']
    return(x)
    # print(x['reviews'])


# def change_description():
#     result = service.files().update(
#         fileId=file_id,
        
#     )



# CHANGE TO BE GET_FILE_DESCRIPTION