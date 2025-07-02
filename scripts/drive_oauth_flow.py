import os
import webbrowser
from google_auth_oauthlib.flow import InstalledAppFlow

# Scopes required for Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive']

# Path to your downloaded OAuth 2.0 client secrets file
CLIENT_SECRET_FILE = os.getenv("GDRIVE_CLIENT_SECRET_PATH")

# Path to Brave browser executable
BRAVE_PATH = os.getenv("BRAVE_PATH")

def main():
    # Register Brave in incognito mode
    webbrowser.register(
        'brave-incognito',
        None,
        webbrowser.BackgroundBrowser(f'"{BRAVE_PATH}" --incognito %s')
    )

    # Initialize OAuth flow
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    auth_url, _ = flow.authorization_url()

    # Open authorization URL in Brave (incognito)
    webbrowser.get('brave-incognito').open(auth_url)

    # Start local server to receive OAuth response
    creds = flow.run_local_server(open_browser=False)

    # Save access token to token.json
    with open('token.json', 'w') as token_file:
        token_file.write(creds.to_json())

    print("✅ token.json created successfully.")

if __name__ == '__main__':
    main()
