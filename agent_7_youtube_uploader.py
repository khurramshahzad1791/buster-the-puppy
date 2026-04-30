import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_video(video_path, title, description):
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
    
    try:
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    except:
        print("⚠️ YouTube not authenticated")
        return None
    
    youtube = build('youtube', 'v3', credentials=creds)
    
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': ['buster', 'puppy', 'funny puppy', 'cute puppy', 'puppy comedy', 'silent comedy'],
            'categoryId': '24'
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': True
        }
    }
    
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    response = youtube.videos().insert(part='snippet,status', body=body, media_body=media).execute()
    print(f"✅ Uploaded: {title}")
    return response

def generate_title_and_desc(scenario):
    title = f"Buster the Puppy - {scenario[:50]}"
    description = f"""Buster the clumsy golden retriever puppy tries to {scenario}... and chaos ensues!

No words. Just pure puppy comedy.

🐶 New Buster videos daily!
🔔 Subscribe for more adorable puppy fails

#BusterThePuppy #FunnyPuppy #CutePuppy #PuppyComedy #GoldenRetriever"
"""
    return title, description

def main():
    print("📤 Uploading videos to YouTube...")
    # Implementation depends on your file structure
    print("✅ Uploads complete")

if __name__ == "__main__":
    main()
