# list_vehicles_status

A Python script to retrieve JSON data from (https://my.fleerp.com/api/v1/tobjects) an API and upload it to an FTP server.

## Requirements
- Python 3.x
- `requests` library (can be installed via pip with `pip install requests`)
- `ftplib` library (can be installed via pip with `pip install ftplib`)
- `google-auth` library (can be installed via pip with `pip install oauth2client`)

## Usage
To run the script, you will need to pass several arguments:

- `credentials_file_path`: the path to the service account credentials JSON file.

Example for local file:
```
python list_vehicles_status.py /path/to/credentials.json
```

Example for help
```
python list_vehicles_status.py -h
```


## How it works
The script retrieves an access token using the provided service account credentials file, and uses the token to authenticate API requests. It retrieves the JSON data from the API using the `requests` library, and serializes the result.

Next, it uses the `ftplib` library to connect to the FTP server and upload the serialized result to the specified target directory. The filename is formatted with the current date, in the format `YYYY-MM-DD.json` and `YYYY-MM-DD.csv`.
