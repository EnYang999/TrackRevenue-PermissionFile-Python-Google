# Google Sheets API: Permission Tracking Script

This script is designed to interact with Google Sheets using the Google Sheets API. It automates the process of creating a new spreadsheet, transforming user permission data into a DataFrame, and updating the spreadsheet with the transformed data. The primary use case is for managing and tracking user permissions in a Google Sheet.

## Prerequisites

Before running the script, ensure you have the following:

- **Google Cloud Account**: Set up a project on Google Cloud Platform.
- **Google Sheets API enabled**: Enable the Sheets API for your project.
- **Client Secret JSON**: Download the client secret file (Client_Secret.json) from your Google Cloud project for authentication.
- **Python libraries**:
  - `google-auth`
  - `google-auth-oauthlib`
  - `google-auth-httplib2`
  - `google-api-python-client`
  - `pandas`

You can install the required libraries using the following command:

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client pandas
```

## Usage

1. Ensure the `Client_Secret.json` file is placed in the same directory as the script.
2. Create a `permissions.json` file with the user permissions data. Example structure:

```json
{
	"user1": ["view_grades", "change_grades"],
	"user2": ["view_classes", "add_classes"],
	"user3": ["delete_grades", "change_classes"]
}
```

3. Run the script using the following command:

```bash
python your_script_name.py
```

The script will:

- Authenticate with Google Sheets API.
- Create a new spreadsheet titled "Track Revenue Sheets".
- Load permissions from the `example.json` file.
- Transform the permission data and update it into the created spreadsheet.

## Function Descriptions

### `initialize_service(client_secret_file, api_service_name='sheets', api_version='v4', scopes=None)`

Initializes and returns a Google Sheets service object. It authenticates the user using the client secret file.

- **Parameters**:

  - `client_secret_file` (str): Path to the client secret JSON file.
  - `api_service_name` (str): Name of the API service. Default is `'sheets'`.
  - `api_version` (str): Version of the API. Default is `'v4'`.
  - `scopes` (list): List of API scopes. Default is the scope for Google Sheets.

- **Returns**: A Google Sheets service object for interacting with the Sheets API.

### `create_spreadsheet(service, title='Track Revenue Sheets')`

Creates a new Google Spreadsheet with a given title and initializes it with default properties.

- **Parameters**:

  - `service`: The authenticated Google Sheets API service object.
  - `title` (str): Title of the spreadsheet. Default is `'Track Revenue Sheets'`.

- **Returns**: A dictionary containing information about the created spreadsheet (e.g., `spreadsheetId`, `spreadsheetUrl`).

### `load_permissions_from_json(json_file_path)`

Loads user permission data from a JSON file.

- **Parameters**:

  - `json_file_path` (str): Path to the JSON file that contains user permissions.

- **Returns**: A dictionary of user permissions.

### `transform_permissions_to_dataframe(user_permissions)`

Transforms the user permission data into a DataFrame format, creating a table where rows represent users and columns represent permissions.

- **Parameters**:

  - `user_permissions` (dict): Dictionary containing user permissions data, where keys are usernames and values are lists of permissions.

- **Returns**: A `pandas.DataFrame` with users as rows and permissions as columns.

### `update_spreadsheet_with_data(service, spreadsheet_id, data)`

Updates the Google Spreadsheet with the provided data, writing it to the first sheet starting at cell A1.

- **Parameters**:

  - `service`: The authenticated Google Sheets API service object.
  - `spreadsheet_id` (str): ID of the spreadsheet to update.
  - `data` (`pandas.DataFrame`): DataFrame containing the data to be written to the spreadsheet.

- **Returns**: None. This function directly updates the Google Sheet.

### `main()`

The main function that ties everything together:

1. Authenticates with the Google Sheets API.
2. Creates a new Google Spreadsheet.
3. Loads permissions from a JSON file.
4. Transforms the permissions data to a DataFrame.
5. Updates the newly created spreadsheet with the transformed data.

---

### Example JSON Data (`example.json`)

```json
{
	"user1": ["view_grades", "change_grades"],
	"user2": ["add_grades", "delete_grades"],
	"user3": ["view_classes", "add_classes"]
}
```

## License

This project is licensed under the MIT License.

---

This `README.md` provides a clear overview of the script, its functions, and instructions for usage. It also describes the purpose of each function concisely.
