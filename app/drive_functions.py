# google drive api imports
from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account
# error message imports
from apiclient import errors
from apiclient import http


creds = None

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly https://www.googleapis.com/auth/drive']

SERVICE_ACCOUNT_FILE = 'credentials.json'

COMPLETED_FOLDER_ID = '1e6WGPJjOCfndBGvP7KLKi6H7xB2gKYuc'
PENDING_REVIEW_FOLDER_ID = '1uFleH0-Rznf_IpEZR8n3Czs0zau7od3V'
OVERFLOW_REVIEW_FOLDER_ID = '1eQWxGiI7EovoENa4CwbSDuP-RTmTwLbT'
BLANK_TRANSCRIPT_ID = '1O_937zukto10_pUEQQZkKtwvuIRHp7tg'
JPG_FOLDER_ID = '1jfNrqneyBHqvvABZ319If-i7xq8ERT1k'

# maybe not needed // actually i think it rlly is needed
SHARED_DRIVE_ID = '0AD484V2JtzcFUk9PVA'

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('drive', 'v3', credentials=creds)

docs_service = build('docs', 'v1', credentials=creds)
# Call the Drive v3 API



def list_one_file():
    results = service.files().list(
        pageSize=10, includeItemsFromAllDrives=True, supportsAllDrives=True, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    file_list=[]

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            file_list.append(item['name'])
            file_list.append(item['id'])
            # print(u'{0} ({1})'.format(item['name'], item['id']))
        return(file_list)

def getSharedDriveFiles():

    results = service.files().list(pageSize = 10, fields='nextPageToken, files(name, id)', driveId=SHARED_DRIVE_ID, corpora='drive', includeItemsFromAllDrives=True, supportsAllDrives=True).execute()

    items = results.get('files', [])
    if not items:
        print('No files found')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))


def read_text_file():
    results = service.files().export(
    fileId='1f2kbWFz_c8HKGgAMX-KmmsBMLJL3fHGpTr2gPpc3i8g',
    # supportsAllDrives=True,
    mimeType='text/plain').execute()
    print(results.decode("utf-8-sig").encode("utf-8"))


def write_to_file(data):
    requests = [
     {
        'insertText': {
            'location': {
                'index': 1,
            },
            'text': data + "\n\n"
        }
    }]

    docs_service.documents().batchUpdate(
        documentId="1OCLMSLg9xP2s3wW6hvTIvNHeK4UsekHne1-AP7jDuas",
        body={'requests': requests}
    ).execute()



def download_jpg(service, file_id, local_fd):
  """Download a Drive file's content to the local filesystem.

  Args:
    service: Drive API Service instance.
    file_id: ID of the Drive file that will downloaded.
    local_fd: io.Base or file object, the stream that the Drive file's
        contents will be written to.
  """
  request = service.files().get_media(fileId=file_id)
  media_request = http.MediaIoBaseDownload(local_fd, request)

  while True:
    try:
      download_progress, done = media_request.next_chunk()
    except (errors.HttpError, error):
      print('An error occurred: %s' % error)
      return
    if download_progress:
      print('Download Progress: %d%%' % int(download_progress.progress() * 100))
    if done:
      print('Download Complete')
      return

def get_file_name(service, file_id):
  """Return a file's metadata.

  Args:
    service: Drive API service instance.
    file_id: ID of the file to print metadata for.
  """
  try:
    file = service.files().get(fileId=file_id, supportsAllDrives=True).execute()

    return(file['name'])
    # print(file['permissions(1U770WJJRdkJcYxAM3fJt-HFqLQpcogUtGHQjYluqKjQ'])
  except (errors.HttpError, error):
    print('An error occurred: %s' % error)

# FIX FOR SHARED DRIVE EZ
def create_file():
    file = service.files().create(body={
        # CRAZY IMPORTANT TO GIVE FILE OWNERSHIP OR SOMETHING TO MAIN ACCOUNT ACTUALLY NO IT'S NOT STFU
        'name': 'photo.jpg',
        # SUPER IMPORTANT TO INCLUDE FOLDER ID
        'parents': ["1UsEQYkR-v9GqglHp6RK9XCnvg2nVybYv"]
    }, fields='id').execute()

# DANGEROUS
def delete_file(service, file_id):
  """Permanently delete a file, skipping the trash.

  Args:
    service: Drive API service instance.
    file_id: ID of the file to delete.
  """
  try:
    service.files().delete(fileId=file_id).execute()
  except (errors.HttpError, error):
    print('An error occurred: %s' % error)



getSharedDriveFiles()

# write_to_file("abc")

# print(list_one_file())

# delete_file(service, '1KMX61WBhgoT0RRrIKsNr5GKPkLuNxZXU')


# print(get_file_name(service, '1f2kbWFz_c8HKGgAMX-KmmsBMLJL3fHGpTr2gPpc3i8g'))



# read_text_file()

# write_to_file("yes") 

# f = open("myfile.jpg", "r+b")
# download_jpg(service, "1JoVHsYafukj9nL15ZpScLEb5f2Q_D9h-", f)

# create_file()
