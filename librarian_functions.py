# google drive api imports
from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account
from google_drive import *
# random number
import secrets
# unit testing
import unittest


# ON PAGE LOAD:
def get_transcription():
    results = service.files().list(pageSize = 10, q="'{0}' in parents and name contains '.JPG'".format(PENDING_APPROVAL_FOLDER_ID), fields='files/webViewLink, nextPageToken, files(name, id)', driveId=SHARED_DRIVE_ID, corpora='drive', includeItemsFromAllDrives=True, supportsAllDrives=True).execute()
    # print(results)
    jpg_list = results.get('files', [])
    global jpg_file_id
    global jpg_file_name
    global jpg_view_link
    if not jpg_list:
        jpg_file_id = None
        jpg_file_name = None
        jpg_view_link = None
        print('No files found')
    else:
        jpg_list = secrets.choice(jpg_list)
        # jpg_file_id = u'{0}'.format(jpg_list['id'])
        # jpg_file_name = u'{0}'.format(jpg_list['name'])
        # # REMOVES EVERYTHING AFTER /view in URL AND APPENDS /preview
        # jpg_view_link = u'{0}'.format(jpg_list['webViewLink']).split("/view")[0] + "/preview"

        return jpg_list
        get_transcription_txt()


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
        # global txt_file_name
        txt_file_name = jpg_file_name.split('.JPG')[0] + ".txt"
        results = service.files().list(pageSize=1, q="'{0}' in parents and name='{1}' and name contains '.txt'".format(PENDING_APPROVAL_FOLDER_ID, txt_file_name), fields='files(id)', driveId=SHARED_DRIVE_ID, corpora='drive', includeItemsFromAllDrives=True, supportsAllDrives=True).execute()
        txt_list = results.get('files')
        if not txt_list:
            print('No files found')
        else:
            for item in txt_list:
                txt_list = item
            # global txt_id
            txt_id = u'{0}'.format(txt_list['id'])
            # print(txt_id)
            return txt_id
            # return txt_id


def read_txt_file(txt_id):
    # print(txt_file_id + "yes")
    results = service.files().export(
    fileId=txt_id,
    mimeType='text/plain').execute()
    # global txt_file_content

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


# SEE LAST LINE, IMPLEMENT
def approve_transcription(file_id, jpg_id):
    if jpg_id != None:
        file = service.files().update(fileId=file_id,
                                addParents=COMPLETED_FOLDER_ID,
                                removeParents=PENDING_APPROVAL_FOLDER_ID,
                                fields='id, description, parents', supportsAllDrives="true").execute()

        file2 = service.files().update(fileId=jpg_id,
                                addParents=COMPLETED_FOLDER_ID,
                                removeParents=PENDING_APPROVAL_FOLDER_ID,
                                fields='id, description, parents', supportsAllDrives="true").execute()


def disapprove_transcription(file_id, jpg_id):
    if jpg_id != None:
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

            file = service.files().update(fileId=txt_id,
                                addParents=COMPLETED_FOLDER_ID,
                                removeParents=PENDING_APPROVAL_FOLDER_ID,
                                fields='id, description, parents', supportsAllDrives="true").execute()

            file2 = service.files().update(fileId=jpg_id,
                                addParents=COMPLETED_FOLDER_ID,
                                removeParents=PENDING_APPROVAL_FOLDER_ID,
                                fields='id, description, parents', supportsAllDrives="true").execute()

def checkFile(jpg_file):
    try:
        file = service.files().get(
            fileId=jpg_file,
            fields='parents',
            supportsAllDrives=True
            ).execute()
        if file["parents"][0] == PENDING_APPROVAL_FOLDER_ID:
            return True
        else:
            print("The file was not in the correct folder; it has likely already been transcribed.")
            return False
    except:
        print("The file was not found.")
        return False


# --------------- Unit Testing ---------------

class Test(unittest.TestCase):
    def test_get_transcription(self):
        try:
            get_transcription()
        except Exception:
            self.fail("Test Failed; get_transcription() caused error")

    def test_approve_transcription(self):
        jpg_data = get_transcription()
        # Tests assuming that Google Drive is properly populated with .jpg and .txt files; otherwise, pass
        if jpg_data != None:
            jpg_name = get_jpg_name(jpg_data)
            jpg_id = get_jpg_id(jpg_data)

            txt_id = get_transcription_txt(jpg_name)
            approve_transcription(txt_id, jpg_id)
            # Tests whether file was properly movedto COMPLETED_FOLDER
            file = service.files().get(
                fileId=jpg_id,
                fields='parents',
                supportsAllDrives=True
                ).execute()

            self.assertEqual(file['parents'][0], COMPLETED_FOLDER_ID)


if __name__ == '__main__':
    unittest.main()
