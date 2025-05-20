SPOTIPY_CLIENT_ID = 'your_spotify_client_id'  # Enter your Spotify Client ID
SPOTIPY_CLIENT_SECRET = 'your_spotify_client_secret'  # Enter your Spotify Client Secret
YT_API_KEY = 'your_youtube_api_key'  # Enter your YouTube API Key
FFMPEG_PATH = 'path_to_ffmpeg'  # Enter your ffmpeg path (e.g., 'C:/ffmpeg/bin/ffmpeg.exe' or '/usr/bin/ffmpeg')
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:8000/callback'

import os
import yt_dlp
import shutil
import spotipy
from urllib.parse import urlparse
from spotipy.oauth2 import SpotifyOAuth
from googleapiclient.discovery import build

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope="playlist-read-private"
))

def get_playlist_tracks(playlist_url):
    # Extract playlist ID from URL
    playlist_id = playlist_url.split('/')[-1].split('?')[0]
    
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    
    return tracks

def get_youtube_video_link(api_key, video_name):
    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.search().list(
        q=video_name,
        part='snippet',
        type='video',
        maxResults=1
    )

    response = request.execute()

    if response['items']:
        video_id = response['items'][0]['id']['videoId']
        return f'https://www.youtube.com/watch?v={video_id}'
    else:
        return 'No video found.'
    
def get_postprocessors(media_type):
    """Configure post-processing"""
    if media_type == 'audio':
        return [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    
def download_media(url, media_type='audio', playlist_name=None):
    ffmpeg_path = FFMPEG_PATH

    output_dir = f"Playlists/{playlist_name}/" if playlist_name else "Playlists/downloads/"
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'quiet': True,
        'verbose': False,
        'no-warnings': True,
        'ffmpeg_location': ffmpeg_path,
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'format': 'bestaudio/best' if media_type == 'audio' else 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }] if media_type == 'audio' else []
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    
def get_playlist_tracks(playlist_url):
    playlist_id = playlist_url.split('/')[-1].split('?')[0]
    
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    
    return tracks, playlist_id

    
def download_playlist(playlist_url):
    
    tracks, playlist_id = get_playlist_tracks(playlist_url)

    playlist_info = sp.playlist(playlist_id)
    playlist_name = playlist_info['name']

    api_key = YT_API_KEY
    
    print(f"Playlist Name: {playlist_name}")
    print(f"Found {len(tracks)} tracks in the playlist:")
    for i, item in enumerate(tracks):
        track = item['track']
        song = f"{track['name']} by {', '.join([artist['name'] for artist in track['artists']])}"
        print(f"{i+1}. {song}")
        download_media(get_youtube_video_link(api_key, song),'audio', playlist_name)

def main():
    playlist_url = input("Enter Spotify playlist URL: ")
    if not playlist_url.startswith("https://open.spotify.com/playlist/"):
        print("Invalid Spotify playlist URL.")
        main()
    else:
        print("Downloading playlist...")
        download_playlist(playlist_url)
        print("Download completed.")
        shutil.rmtree('Playlists/downloads', ignore_errors=True)
        shutil.rmtree('Playlists', ignore_errors=True)
        x = input("Enter r to restart or any key to exit: ")
        if x == 'r': 
            main()
        else:
            exit()

if __name__ == "__main__":
    main()
