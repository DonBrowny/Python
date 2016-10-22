from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient import errors

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():

    """Gets / Sets valid user credentials from storage"""
    
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    query = GetUserQuery()
    ListMessagesMatchingQuery(service,'me',query)

def GetUserQuery():

    """Sets the query from user input"""
    
    _from = input('Enter the from Email Adress: ')
    _fromDate = input('Enter Received after Date(YYYY/MM/DD): ')
    _toDate = input('Enter Received before Date(YYYY/MM/DD): ')
    return 'in:unread from:' + _from + ' after:' + _fromDate + ' before:' + _toDate

def ListMessagesMatchingQuery(service, user_id, query):

  """Get a Message for the given query"""
    
  try:
    response = service.users().messages().list(userId=user_id,
                                               q=query).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])
    
    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(userId=user_id, q=query,
                                         pageToken=page_token).execute()
      messages.extend(response['messages'])
    print('Retrived Message')
    for temp in messages:
        GetMessage(service,temp['threadId'])
  except :
    print ('An error occurred: ' , errors.HttpError)

def GetMessage(service, msg_id):
    
  """Get a Message with given ID  """
  
  try:
    message = service.users().messages().get(userId='me', id=msg_id).execute()

    print ('Message snippet: ' , message['snippet'])

    return message
  except :
    print ('An error occurred: ', errors.HttpError)
    
if __name__ == '__main__':
    main()
