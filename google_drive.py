# google drive api imports
from __future__ import print_function
from googleapiclient.discovery import build
from google.oauth2 import service_account
# import unit tests
import unittest
# import environment variables
from os import environ
# convert string to dict
import ast


creds = None

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/drive.file']

COMPLETED_FOLDER_ID = environ.get('COMPLETED_FOLDER_ID')
PENDING_APPROVAL_FOLDER_ID = environ.get('PENDING_APPROVAL_FOLDER_ID')
PENDING_REVIEW_FOLDER_ID = environ.get('PENDING_REVIEW_FOLDER_ID')
JPG_FOLDER_ID = environ.get('JPG_FOLDER_ID')

SHARED_DRIVE_ID = environ.get('SHARED_DRIVE_ID')

SERVICE_ACCOUNT_INFO = environ.get("SERVICE_ACCOUNT_INFO")
SERVICE_ACCOUNT_INFO = ast.literal_eval(SERVICE_ACCOUNT_INFO)

creds = service_account.Credentials.from_service_account_info(
    SERVICE_ACCOUNT_INFO, scopes=SCOPES)

# google drive api
service = build('drive', 'v3', credentials=creds)

docs_service = build('docs', 'v1', credentials=creds)


class Test(unittest.TestCase):
    def test_authentication(self):
        try:
            # google drive api
            service = build('drive', 'v3', credentials=creds)

            docs_service = build('docs', 'v1', credentials=creds)
        except:
            self.fail("The credentials provided in credentials.json were either unavailable or invalid.")

    def test_jpg_folder(self):
        try:
            file = service.files().get(
            fileId=JPG_FOLDER_ID,
            supportsAllDrives=True
            ).execute()
        except:
            self.fail("The JPG Folder ID was not valid.")

    def test_pending_review_folder(self):
        try:
            file = service.files().get(
            fileId=PENDING_REVIEW_FOLDER_ID,
            supportsAllDrives=True
            ).execute()
        except:
            self.fail("The Pending Review Folder ID was not valid.")

    def test_pending_approval_folder(self):
        try:
            file = service.files().get(
            fileId=PENDING_APPROVAL_FOLDER_ID,
            supportsAllDrives=True
            ).execute()
        except:
            self.fail("The Pending Approval Folder ID was not valid.")
        
    def test_completed_folder(self):
        try:
            file = service.files().get(
            fileId=PENDING_REVIEW_FOLDER_ID,
            supportsAllDrives=True
            ).execute()
        except:
            self.fail("The Completed Transcription Folder ID was not valid.")


if __name__ == '__main__':
    unittest.main()