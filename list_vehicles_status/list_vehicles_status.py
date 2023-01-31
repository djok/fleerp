import json
import csv
import os
import ftplib
import argparse
import requests
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def get_access_token(credentials_file_path):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file_path)
    access_token = credentials.get_access_token().access_token
    return access_token

def upload_to_ftp(file_path, file_path_csv, ftp_host, ftp_user, ftp_pass, ftp_directory):
    with ftplib.FTP(ftp_host) as ftp:
        ftp.login(ftp_user, ftp_pass)
        ftp.cwd(ftp_directory)
        with open(file_path, 'rb') as fp:
            ftp.storbinary('STOR ' + os.path.basename(file_path), fp)
        with open(file_path_csv, 'rb') as fp:
            ftp.storbinary('STOR ' + os.path.basename(file_path_csv), fp)
    print("Upload to FTP complete")

def save_locally_csv(file_path, file_path_csv):
    # load json data from file
    with open(file_path) as json_file:
        data = json.load(json_file)
    # write data to csv file
    with open(file_path_csv, 'w', newline='') as csv_file:
        fieldnames = [
                        'cid', 
                        'manufacturer', 
                        'model', 
                        'type', 
                        'year', 
                        'id', 
                        'name', 
                        'firstName', 
                        'lastName', 
                        'groupId', 
                        'inventoryId', 
                        'label', 
                        'lastIgnition', 
                        'lastIgnitionOff', 
                        'lastMove', 
                        'lat', 
                        'lng', 
                        'lastStop', 
                        'lastUpdate', 
                        'lpn', 
                        'mileage', 
                        'mountedAt', 
                        'msisdn', 
                        'trackingId', 
                        'type'
                        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow({
                            'cid': item['cid'],
                            'manufacturer': item['description']['manufacturer'],
                            'model': item['description']['model'],
                            'type': item['description']['type'],
                            'year': item['description']['year'],
                            'id': item['deviceModel']['id'],
                            'name': item['deviceModel']['name'],
                            'firstName': item['driver']['firstName'],
                            'lastName': item['driver']['lastName'],
                            'groupId': item['groupId'],
                            'inventoryId': item['inventoryId'],
                            'label': item['label'],
                            'lastIgnition': item['lastIgnition'],
                            'lastIgnitionOff': item['lastIgnitionOff'],
                            'lastMove': item['lastMove'],
                            'lat': item['lastPoint']['location']['lat'],
                            'lng': item['lastPoint']['location']['lng'],
                            'lastStop': item['lastStop'],
                            'lastUpdate': item['lastUpdate'],
                            'lpn': item['lpn'],
                            'mileage': item['mileage'],
                            'mountedAt': item['mountedAt'],
                            'msisdn': item['msisdn'],
                            'trackingId': item['trackingId'],
                            'type': item['type']
                            })

def main(credentials_file_path, save_option, ftp_host=None, ftp_user=None, ftp_pass=None, ftp_directory=None):
    access_token = get_access_token(credentials_file_path)
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get("https://my.fleerp.com/api/v1/tobjects", headers=headers)

    if response.status_code == 200:
        result_json = response.json()
        current_date = datetime.today().strftime('%Y-%m-%d')
        file_path = f"{current_date}.json"
        file_path_csv = f"{current_date}.csv"
        with open(file_path, 'w') as f:
            f.write(json.dumps(result_json, indent=4))
        save_locally_csv(file_path, file_path_csv)

        if save_option == "ftp":
            if ftp_host is None or ftp_user is None or ftp_pass is None or ftp_directory is None:
                raise Exception("FTP host, username, password and directory are required when using ftp save option")
            upload_to_ftp(file_path, file_path_csv, ftp_host, ftp_user, ftp_pass, ftp_directory, result_json)
        elif save_option == "local":
            print("Result saved locally")
        else:
            raise Exception("Invalid save option. Choose either 'ftp' or 'local'")
    else:
        print(f"Failed to connect to the web service. Response status code: {response.status_code}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("credentials_file_path", help="Path to the service account credentials JSON file.")
    parser.add_argument("--save_option", help="Save option, either 'local' or 'ftp'.", default="local")
    parser.add_argument("--ftp-host", help="FTP host.")
    parser.add_argument("--ftp-user", help="FTP user.")
    parser.add_argument("--ftp-password", help="FTP password.")
    parser.add_argument("--ftp-directory", help="FTP directory to upload the result to.")
    args = parser.parse_args()
    main(args.credentials_file_path, args.save_option, args.ftp_host, args.ftp_user, args.ftp_password, args.ftp_directory)
