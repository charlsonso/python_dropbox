import os.path
import io
from python_dropbox.app.credential_checker import get_service
from mimetypes import MimeTypes
import urllib
from googleapiclient.http import MediaFileUpload as MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
import dateutil.parser as dp
import datetime
import time
from pathlib import Path

def app_runner(target_folder, credential, pickle_token):
    service = get_service(credential, pickle_token, target_folder)
    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name, modifiedTime)").execute()
    items = results.get('files', [])
    files_in_local = os.listdir(target_folder)
    files_in_drive = []
    for drive_item in items:
        files_in_drive.append(drive_item['name'])

    db_path = os.path.join(target_folder, '.db')
    if not os.path.exists(db_path):
        Path(db_path).touch()
    with open(db_path) as f:
        files_uploaded = f.readlines()

    files_uploaded = [x.strip('\n') for x in files_uploaded]
    files_to_be_delete = list(set(files_uploaded) - set(files_in_drive))
    #Ignore token.pickle, db files, and files deleted from the drive
    if 'token.pickle' in files_in_local:
        files_in_local.remove('token.pickle')
    if '.db' in files_in_local:
        files_in_local.remove('.db')
    for i in files_in_local:
        if i in files_to_be_delete:
            files_in_local.remove(i)

    #Find Files to upload
    new_files = set(files_in_local) - set(files_in_drive)
    new_files = list(new_files)
    if len(new_files) > 0:
        print('New Items in your local folder:\n')
        for i in new_files:
            print('\t'+i)
        upload_new_files(new_files, service, target_folder, db_path)
    download_files = set(files_in_drive) - set(files_in_local)
    download_files = list(download_files)
    if len(download_files) > 0:
        print('Files in Drive not in your local folder:\n')
        for i in download_files:
            print('\t'+i)
        download_drive_files(download_files, items, service, target_folder)

    #Modified Files to update
    intersect_files = set(files_in_local).intersection(set(files_in_drive))
    modified_files = get_modified_files(intersect_files, items, target_folder) 

    if len(modified_files) > 0:
        print('Updating Modified Files...')
        download_files = []
        update_files_to_drive = []
        for f in modified_files:
            if f[1] == 1:
                download_files.append(f[0])
            if f[1] == 2:
                update_files_to_drive.append(f[0])
        if len(download_files) > 0:
            download_drive_files(download_files, items, service, target_folder)
        if len(update_files_to_drive) > 0:
            update_drive_files(update_files_to_drive, items, service, target_folder)

    #Deleted Files in Drive. Delete in local
    if len(files_to_be_delete) > 0:
        print('The following has been deleted from the Drive. Deleting it locally...')
        for i in files_to_be_delete:
            print('\t'+i)
            os.remove(os.path.join(target_folder, i))
            files_uploaded.remove(i)
        overwrite_db(db_path, files_uploaded)

def overwrite_db(db_path, list_of_files):
    with open(db_path, 'r+') as f:
        for i in list_of_files:
            f.write(i+'\n')

def append_to_db(db_path, file_path):
    with open(db_path, 'a+') as f:
        f.write(file_path+'\n')

def update_drive_files(update_files, items, service, target_folder):
    for f in update_files:
        file_id = None
        for i in items:
            if i['name'] == f:
                file_id = i['id']
                break
        abs_path = os.path.join(target_folder, f)
        mime = MimeTypes()
        url = urllib.request.pathname2url(abs_path)
        mime_type = mime.guess_type(url)
        body = {'name': f, 'mimeType':mime_type[0]}
        media_body = MediaFileUpload(abs_path, mimetype=mime_type[0], resumable = True)
        service.files().update(fileId=file_id, body=body, media_body=media_body).execute()
        print('Updated {} on Drive'.format(f))

def download_drive_files(download_files, google_item_dict, service, target_folder):
    for f in download_files:
        google_item = None
        for item in google_item_dict:
            if item['name'] == f:
                google_item = item
                break
        file_id = item['id']
        request = service.files().get_media(fileId=file_id)
        fh = io.FileIO(os.path.join(target_folder, f), 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        print('Finished Downloading {}'.format(f))

#returns list of (modified_file_name, change_value)
#change_value = 1 - changed in google drive, download file and replace current 2 - changed in local, update file in google drive
def get_modified_files(files_to_compare_times, google_item_dict, target_folder):
    modified_files = []
    for f in files_to_compare_times:
        time_modified_in_drive = None
        for item in google_item_dict:
            if item['name'] == f:
                time_modified_in_drive = item['modifiedTime']
                break
        time_modified_in_drive = float(dp.parse(time_modified_in_drive).strftime('%s'))
        time_modified_in_local = time.mktime(datetime.datetime.utcfromtimestamp(os.path.getmtime(os.path.join(target_folder, f))).timetuple())
        #Drive file was edited
        if time_modified_in_drive > time_modified_in_local:
            modified_files.append((f, 1))
        #local file was edited
        if time_modified_in_drive < time_modified_in_local:
            modified_files.append((f,2))
    return modified_files

def upload_new_files(files, service, target_folder, db_path):
    for new_file in files:
        abs_path_file = os.path.abspath(os.path.join(target_folder, new_file))
        mime = MimeTypes()
        url = urllib.request.pathname2url(abs_path_file)
        mime_type = mime.guess_type(url)
        file_m_time = datetime.datetime.utcfromtimestamp(os.path.getmtime(os.path.join(target_folder, new_file))).isoformat()+"Z"
 
        file_metadata = {'name' : new_file,
                         'modifiedTime': file_m_time}
        media = MediaFileUpload(abs_path_file,
                                mimetype = mime_type[0])
        file_upload = service.files().create(body=file_metadata,
                                             media_body=media,
                                             fields='id').execute()
        print('>>> Uploaded {} to Google Drive.'.format(new_file))
        append_to_db(db_path, new_file)


if __name__ == '__main__':
    main()
