import pickle
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

gmail_service = None

TOKEN_PATH = Path.home() / '.gmail_mcp_token.pickle'

def get_gmail_service():
    global gmail_service
    
    if gmail_service:
        return gmail_service
    
    credentials = None

    if TOKEN_PATH.exists():
        try:
            with open(TOKEN_PATH, 'rb') as token:
                credentials = pickle.load(token)
        except Exception as e:
            print(f'Error loading token: {e}')

    if credentials:
        if credentials.expired and credentials.refresh_token:
            try:
                credentials.refresh(Request())
                with open(TOKEN_PATH, 'wb') as token:
                    pickle.dump(credentials, token)
            except Exception as e:
                credentials = None
                print(f'Error refreshing token: {e}')
    
    if credentials and credentials.valid:
        return build('gmail', 'v1', credentials=credentials)
    
    return None

def save_credentials(credentials: Credentials):

    global gmail_service

    with open(TOKEN_PATH, 'wb') as token:
        pickle.dump(credentials, token)
    
    gmail_service = build('gmail', 'v1', credentials=credentials)


def ensure_auth():
    service = get_gmail_service()
    if not service:
        raise Exception('Unauthenticated')
    return service

def logout():
    """Clear authentication credentials"""
    global gmail_service
    gmail_service = None

    if TOKEN_PATH.exists():
        TOKEN_PATH.unlink()
        return True
    return False