import os
import json
import pandas as pd
from Google import Create_Service

def initialize_service(client_secret_file, api_service_name='sheets', api_version='v4', scopes=None):
    if scopes is None:
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
    
    return Create_Service(client_secret_file, api_service_name, api_version, scopes)

def create_spreadsheet(service, title='Track Revenue Sheets'):
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
    with open(json_file_path, 'r') as file:
        return json.load(file)

def transform_permissions_to_dataframe(user_permissions):
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
    folder_path = r'.'
    client_secret_file = os.path.join(folder_path, 'Client_Secret.json')
    
    service = initialize_service(client_secret_file)

    spreadsheet_info = create_spreadsheet(service)
    print(spreadsheet_info['spreadsheetUrl'])

    spreadsheet_id = spreadsheet_info['spreadsheetId']

    permissions_json_file = 'example.json'  # Update with your JSON file path
    permissions = load_permissions_from_json(permissions_json_file)
    permissions_df = transform_permissions_to_dataframe(permissions)
    
    update_spreadsheet_with_data(service, spreadsheet_id, permissions_df)

if __name__ == "__main__":
    main()