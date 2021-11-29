# google drive api imports
from __future__ import print_function
import os.path
from google_drive import *
# random number
import secrets


# ON PAGE LOAD:
def get_transcription():
    results = service.files().list(pageSize = 15, orderBy="createdTime", q="'{0}' in parents and name contains '.JPG'".format(PENDING_REVIEW_FOLDER_ID), fields='files/webViewLink, nextPageToken, files(name, id)', driveId=SHARED_DRIVE_ID, corpora='drive', includeItemsFromAllDrives=True, supportsAllDrives=True).execute()
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

def get_transcription_txt(jpg_file_name):
    if jpg_file_name != None:
        txt_file_name = jpg_file_name.split('.JPG')[0] + ".txt"
        results = service.files().list(pageSize=1, q="'{0}' in parents and name='{1}' and name contains '.txt'".format(PENDING_REVIEW_FOLDER_ID, txt_file_name), fields='files(id)', driveId=SHARED_DRIVE_ID, corpora='drive', includeItemsFromAllDrives=True, supportsAllDrives=True).execute()
        txt_list = results.get('files')
        if not txt_list:
            print('No files found')
        else:
            for item in txt_list:
                txt_list = item
            txt_id = u'{0}'.format(txt_list['id'])
            return txt_id


def read_txt_file(txt_id):
    results = service.files().export(
    fileId=txt_id,
    mimeType='text/plain').execute()

    txt_file_content = results.decode("utf-8")
    return txt_file_content


def get_file_description(file_id):
    if file_id != None:
        file = service.files().get(
            fileId=file_id,
            fields='description',
            supportsAllDrives=True
            ).execute()
        x = file['description']
        return(x)
    

def submit_edit(txt_id, jpg_id, jpg_name, data):
    if jpg_id != None:
        txt_file_content = read_txt_file(get_transcription_txt(jpg_name))
        if len(txt_file_content) > 0:
            delete_requests = [
                    {
                        'replaceAllText': {
                            'replaceText': '',
                            'containsText': {
                                'text': txt_file_content[1:],
                            },
                    }
                }]


            docs_service.documents().batchUpdate(
                documentId=txt_id,
                body={'requests': delete_requests}
            ).execute()


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
                documentId=txt_id,
                body={'requests': requests}
            ).execute()

            result = service.files().update(
                fileId=txt_id,
                body={
                'description':0},
                supportsAllDrives=True
                ).execute()


# SEE LAST LINE, IMPLEMENT
def increment_review_counter(txt_id, jpg_id):
    if jpg_id != None:    
        result = service.files().update(
            fileId=txt_id,
            body={
            'description':str(int(get_file_description(txt_id))+1)},
            supportsAllDrives=True
            ).execute()
        # print(get_file_description(txt_id))

        if int(get_file_description(txt_id)) >= 2:
            file = service.files().update(fileId=txt_id,
                                    addParents=PENDING_APPROVAL_FOLDER_ID,
                                    removeParents=PENDING_REVIEW_FOLDER_ID,
                                    fields='id, description, parents', supportsAllDrives="true").execute()

            file2 = service.files().update(fileId=jpg_id,
                                    addParents=PENDING_APPROVAL_FOLDER_ID,
                                    removeParents=PENDING_REVIEW_FOLDER_ID,
                                    fields='id, description, parents', supportsAllDrives="true").execute()


def decrement_review_counter(txt_id, jpg_id):
    if jpg_id != None:
        if int(get_file_description(txt_id)) > -2:
            result = service.files().update(
                fileId=txt_id,
                body={
                'description':str((int(get_file_description(txt_id))-1))},
                supportsAllDrives=True
                ).execute()
        else:
            pass

def checkFile(jpg_file):
    try:
        file = service.files().get(
            fileId=jpg_file,
            fields='parents',
            supportsAllDrives=True
            ).execute()
        if file["parents"][0] == PENDING_REVIEW_FOLDER_ID:
            return True
        else:
            print("The file was not in the correct folder; it has likely already been transcribed.")
            return False
    except:
        print("The file was not found.")
        return False