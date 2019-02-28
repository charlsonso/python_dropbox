import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/drive']

def get_service(credential, pickle_token, target_folder):
    creds = None
    
    if pickle_token is not None and os.path.exists(pickle_token):
        with open(pickle_token, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if credential is None:
                raise Exception('No pickle file found. Please enable google drive api. Go to \'https://developers.google.com/drive/api/v3/quickstart/python\' and follow Step 1 and download your credential.json and input with the command line option --credential')
            flow = InstalledAppFlow.from_client_secrets_file(
                    credential, SCOPES)
            creds = flow.run_local_server()
            with open(os.path.join(target_folder, 'token.pickle'), 'wb') as token:
                pickle.dump(creds, token)
            print('Pickle is saved in target folder {}. Use the option --pickle next time you run the application.'.format(target_folder))
    service = build('drive', 'v3', credentials=creds)
    return service

