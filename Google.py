import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request


def Create_Service(client_secret_file, api_name, api_version, *scopes):
    """
    Creates and returns a Google API service object for the specified API and version.

    This function handles authentication and authorization using OAuth 2.0. 
    It checks for existing credentials in a pickle file and refreshes or generates new credentials as necessary.

    :param client_secret_file: str
        The path to the JSON file that contains the client's OAuth 2.0 credentials.
    :param api_name: str
        The name of the Google API service to be accessed (e.g., 'sheets').
    :param api_version: str
        The version of the API to be used (e.g., 'v4').
    :param scopes: list
        A variable number of string parameters indicating the scopes of access required by the API.

    :return: googleapiclient.discovery.Resource
        A service object that allows interaction with the specified Google API.
    """
    print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]] # Extract scopes from the passed argument
    print(SCOPES)

    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'

    # Load credentials from the pickle file if it exists
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    #  Check if credentials are valid or need to be refreshed
    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        # Save the credentials to a pickle file for future use
        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    # Build the API service
    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None

