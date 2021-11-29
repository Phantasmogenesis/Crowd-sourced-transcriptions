# google drive api imports
from __future__ import print_function
import os.path
from google_drive import *
# random number
import secrets


# ON PAGE LOAD:
def get_random_jpg():
    results = service.files().list(pageSize = 10, orderBy="createdTime", q="'{0}' in parents".format(JPG_FOLDER_ID), fields='files/webViewLink, nextPageToken, files(name, id)', driveId=SHARED_DRIVE_ID, corpora='drive', includeItemsFromAllDrives=True, supportsAllDrives=True).execute()
    # print(results)
    jpg_list = results.get('files', [])
    if not jpg_list:
        print('No files found')
        return None
    else:
        jpg_list = secrets.choice(jpg_list)

        return jpg_list

def get_jpg_id(jpg_list):
    jpg_id = u'{0}'.format(jpg_list['id'])
    return jpg_id

def get_jpg_name(jpg_list):
    jpg_file_name = u'{0}'.format(jpg_list['name'])
    return jpg_file_name

def get_jpg_link(jpg_list):
    jpg_view_link = u'{0}'.format(jpg_list['webViewLink']).split("/view")[0] + "/preview"
    return jpg_view_link


def create_file(jpg_file_id, jpg_file_name, data):
    # MAKE THIS TAKE INPUT PARAMETER FOR FILE NAME?
    if jpg_file_name != None:
        text_file_name = jpg_file_name.split('.JPG')[0] + ".txt"
        try:
            results = service.files().list(pageSize = 1, q="'{0}' in parents and name = '{1}'".format(PENDING_REVIEW_FOLDER_ID, text_file_name), fields='files/webViewLink, nextPageToken, files(name, id)', driveId=SHARED_DRIVE_ID, corpora='drive', includeItemsFromAllDrives=True, supportsAllDrives=True).execute()
            print(results.get('files', []))
            if results.get('files', []) == []:
                pass
            else:
                print("There is already a transcription.")
                return
        except:
            print("The file was not found.")
            return
        
        file = service.files().create(body={
            'name': text_file_name,
            'description': 0,
            'parents': [PENDING_REVIEW_FOLDER_ID],
            'mimeType': 'application/vnd.google-apps.document',
        }, fields='id', supportsAllDrives="true").execute()
    
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


def get_file_description(file_id):
    file = service.files().get(
        fileId=file_id,
        fields='description',
        supportsAllDrives=True
        ).execute()
    
    # CATCH EXCEPTION IF 'PROPERTIES' IS NULL OH JEEZ UR GONNA MESS THIS UP
    x = file['description']
    return(x)


def checkFile(jpg_file):
    try:
        file = service.files().get(
            fileId=jpg_file,
            fields='parents',
            supportsAllDrives=True
            ).execute()
        if file["parents"][0] == JPG_FOLDER_ID:
            return True
        else:
            print("The file was not in the correct folder; it has likely already been transcribed.")
            return False
    except:
        print("The file was not found.")
        return False