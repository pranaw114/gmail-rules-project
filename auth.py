from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

def generate_token(client_secret_path='client_secret.json', token_path='token.json'):
    flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, SCOPES)
    creds = flow.run_local_server(port=0)
    with open(token_path, 'w') as f:
        f.write(creds.to_json())
    return token_path


generate_token()
