import os
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials

# Set up the Google Drive API credentials
# Make sure you have the necessary credentials file (client_secrets.json) and token file (token.json)
# Replace 'YOUR_CREDENTIALS_FILE.json' with the path to your credentials file
credentials_file = 'drive_client_secrets.json'
scopes = ['https://www.googleapis.com/auth/drive.readonly']
with open(os.path.join(os.path.dirname(os.path.basename(__file__)), credentials_file), "r") as config:
    config = json.load(config)
    credentials = Credentials.from_authorized_user_info(info=config.get("drive1").get("installed"), scopes=scopes)
    # if not credentials or not credentials.valid:
    #     if credentials and credentials.expired and credentials:


# Build the service
service = build('drive', 'v3', credentials=credentials, cache_discovery=False)

# Set the folder ID of the Google Drive folder containing the videos
folder_id = '1UwfrY3UkRVX5GuZut-LL0W3d4GKFu6DE'

def download_videos_from_folder(folder_id):
    # Retrieve the list of files in the folder
    results = service.files().list(q=f"'{folder_id}' in parents",
                                   fields="files(name, id)").execute()
    files = results.get('files', [])

    # Iterate over the files and download them
    for i, file in enumerate(files):
        file_name = "video%d.mp4" % i
        file_id = file['id']
        request = service.files().get_media(fileId=file_id)

        # Create a new directory to save the downloaded videos (if it doesn't exist)
        save_directory = 'downloaded_videos'
        os.makedirs(save_directory, exist_ok=True)

        # Download the video file
        with open(os.path.join(save_directory, file_name), 'wb') as video_file:
            downloader = MediaIoBaseDownload(video_file, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Downloading {file_name} - {int(status.progress() * 100)}%")

    print("Video download complete.")

# Call the function to download videos from the specified folder
download_videos_from_folder(folder_id)
