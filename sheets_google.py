import os
import json
import pandas as pd
from Google import Create_Service
import pprint
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

def transform_permissions_to_dataframe(permissions):
    all_permissions = ['view_grades', 'change_grades', 'add_grades', 'delete_grades',
                       'view_classes', 'change_classes', 'add_classes', 'delete_classes']

    # Create a dictionary to store user permissions as rows
    data = {
        user: [1 if perm in user_perms else 0 for perm in all_permissions]
        for user, user_perms in permissions.items()
    }
    header_row_bin = {' ': all_permissions}
    bin = pd.concat([pd.DataFrame(header_row_bin).T, pd.DataFrame(data).reset_index(drop=True).T], ignore_index=True)
    bin.index = [' ']+list(data.keys())
    
    return bin

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