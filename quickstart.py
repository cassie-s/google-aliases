from __future__ import print_function

import os.path
import csv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/admin.directory.user']


def main():
    """Shows basic usage of the Admin SDK Directory API.
    Prints the emails and names of the first 10 users in the domain.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('admin', 'directory_v1', credentials=creds)

    # Call the Admin SDK Directory API
    print('Getting all users and user aliases from the domain')
    results = service.users().list(customer='my_customer',
                                   orderBy='email', projection='full',).execute()
    users = results.get('users', [])

    if not users:
        print('No users in the domain.')
    else:
        with open('user_data.csv', mode='w', newline='') as csv_file:
            fieldnames = ['Email', 'Full Name', 'Aliases']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for user in users:
                aliases = user.get('aliases', [])
                alias_list = ', '.join(aliases)
                writer.writerow({'Email': user['primaryEmail'], 
                                 'Full Name': user['name']['fullName'], 
                                 'Aliases': alias_list})
    print('File created!')
                


if __name__ == '__main__':
    main()