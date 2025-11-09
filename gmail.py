from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

def get_service():
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    return build('gmail', 'v1', credentials=creds)

def list_messages(service, user_id='me', max_results=100, page_token=None):
    return service.users().messages().list(userId=user_id, maxResults=max_results, pageToken=page_token).execute()

def get_message(service, msg_id, user_id='me', fmt='full'):
    return service.users().messages().get(userId=user_id, id=msg_id, format=fmt, metadataHeaders=['From','To','Subject']).execute()

def get_or_create_label(service, name, user_id='me'):
    labels = service.users().labels().list(userId=user_id).execute().get('labels', [])
    by_name = {lbl['name']: lbl['id'] for lbl in labels}
    if name in by_name:
        return by_name[name]
    created = service.users().labels().create(userId=user_id, body={
        'name': name,
        'labelListVisibility': 'labelShow',
        'messageListVisibility': 'show'
    }).execute()
    return created['id']

def modify_message_labels(service, msg_id, add=None, remove=None, user_id='me'):
    body = { 'addLabelIds': add or [], 'removeLabelIds': remove or [] }
    return service.users().messages().modify(userId=user_id, id=msg_id, body=body).execute()
