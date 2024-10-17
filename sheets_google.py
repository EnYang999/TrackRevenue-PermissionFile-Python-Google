import os
import json
import pandas as pd
from Google import Create_Service

def initialize_service(client_secret_file, api_service_name='sheets', api_version='v4', scopes=None):
    """
    Initializes the Google API service for accessing Google Sheets.

    This function creates a service object that allows interaction with the Google Sheets API, using the provided client secret file and specified parameters.

    :param client_secret_file: str
        The path to the JSON file containing the client secrets for API access.
    :param api_service_name: str, optional
        The name of the API service to interact with. Defaults to 'sheets'.
    :param api_version: str, optional
        The version of the API to use. Defaults to 'v4'.
    :param scopes: list, optional
        The scopes that define the level of access requested by the API. 
        If None, the default scope for Google Sheets is used.
    
    :return: service
        A service object that can be used to interact with the Google Sheets API.
    """ 
    if scopes is None:
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
    
    return Create_Service(client_secret_file, api_service_name, api_version, scopes)

def create_spreadsheet(service, title='Track Revenue Sheets'):
    """
    Creates a new Google Sheets spreadsheet using the specified service.

    This function initializes a Google Sheets document with the given title and default properties.

    :param service: googleapiclient.discovery.Resource
        The authorized Google Sheets API service object obtained from the initialization function.
    :param title: str, optional
        The title of the spreadsheet to be created. Defaults to 'Track Revenue Sheets'.
    
    :return: dict
        The response from the Google Sheets API containing details of the created spreadsheet, including the spreadsheet ID and URL.
    """ 
    sheet_body = {
        'properties': {
            'title': title,
            'locale': 'en_US',  # optional
            'autoRecalc': 'ON_CHANGE',  # calculation setting
            'timeZone': 'America/Toronto'
        },
        'sheets': [
            {'properties': {'title': 'Permission'}}
        ]
    }
    
    return service.spreadsheets().create(body=sheet_body).execute()

def load_permissions_from_json(json_file_path):
    """
    Loads permissions from a JSON file.

    This function reads a JSON file located at the specified path and returns its contents as a Python dictionary.

    :param json_file_path: str
        The path to the JSON file containing permissions data that needs to be loaded.
    
    :return: dict
        A dictionary representation of the JSON file containing permission data, where keys are user identifiers and values are lists of permissions associated with those users.
    """ 
    with open(json_file_path, 'r') as file:
        return json.load(file)

def transform_permissions_to_dataframe(user_permissions):
    """
    Transforms user permissions into a pandas DataFrame.

    This function creates a DataFrame that represents the permission statuses for each user,
    mapping permissions to binary values (1 or 0) based on whether they are assigned to the user.

    :param user_permissions: dict
        A dictionary where keys are user identifiers (e.g., usernames or roles) and values are lists of permissions assigned to each user.
    
    :return: pandas.DataFrame
        A DataFrame containing a row for each user with columns representing permissions and binary indicators (1 for granted, 0 for not granted). 
        The first column serves as a header for permissions, and the first row is blank to align with this.
    """ 
    # Define all possible permissions
    all_permissions = [
        'view_grades', 'change_grades', 'add_grades', 'delete_grades',
        'view_classes', 'change_classes', 'add_classes', 'delete_classes'
    ]

    # Create a dictionary to store each user's permission status as rows
    permissions_matrix = {
        user: [1 if perm in assigned_perms else 0 for perm in all_permissions]
        for user, assigned_perms in user_permissions.items()
    }

    # Create the header row for permissions
    header_row = {' ': all_permissions}

    # Concatenate the header row with the user permission data
    permissions_df = pd.concat(
        [pd.DataFrame(header_row).T, pd.DataFrame(permissions_matrix).reset_index(drop=True).T], 
        ignore_index=True
    )

    # Set the row labels to match users, adding an empty label for the header
    permissions_df.index = [' '] + list(permissions_matrix.keys())
    
    return permissions_df

def update_spreadsheet_with_data(service, spreadsheet_id, data):
    """
    Updates a Google Sheets spreadsheet with provided data.

    This function sends data to the specified Google Sheets spreadsheet, overwriting the existing values starting from cell A1.

    :param service: googleapiclient.discovery.Resource
        The authorized Google Sheets API service object used to perform the update operation.
    :param spreadsheet_id: str
        The ID of the Google Sheets spreadsheet to be updated.
    :param data: pandas.DataFrame
        A DataFrame containing the data to be written to the spreadsheet. The DataFrame is converted to a list of lists, which represents rows of data.
    
    :return: None
        The function does not return any value. It only performs an update operation on the spreadsheet.
    """ 
    values = data.reset_index().values.tolist()
    body = {
        'values': values,
        'majorDimension': 'ROWS'
    }

    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        valueInputOption='RAW',
        range='A1',
        body=body
    ).execute()

def main():
    """
    Main function to initialize the Google Sheets API service, create a new spreadsheet,
    load user permissions from a JSON file, transform the data into a DataFrame,
    and update the spreadsheet with the permission data.
    """
    # Define the folder path and client secret file
    folder_path = r'.'
    client_secret_file = os.path.join(folder_path, 'Client_Secret.json')

    # Initialize the Google Sheets API service
    service = initialize_service(client_secret_file)

    # Create a new spreadsheet and print the URL
    spreadsheet_info = create_spreadsheet(service)
    print(spreadsheet_info['spreadsheetUrl'])

    # Get the spreadsheet ID for further updates
    spreadsheet_id = spreadsheet_info['spreadsheetId']

    # Load permissions from JSON file
    permissions_json_file = 'example.json'  # Update with your JSON file path
    permissions = load_permissions_from_json(permissions_json_file)

    # Transform the permissions data into a DataFrame
    permissions_df = transform_permissions_to_dataframe(permissions)
    
    # Update the Google Sheets spreadsheet with the permissions data
    update_spreadsheet_with_data(service, spreadsheet_id, permissions_df)

if __name__ == "__main__":
    main()