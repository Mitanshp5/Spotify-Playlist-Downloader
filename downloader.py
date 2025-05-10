import os
import yt_dlp
import shutil
import spotipy
from urllib.parse import urlparse
from spotipy.oauth2 import SpotifyOAuth
from googleapiclient.discovery import build

SPOTIPY_CLIENT_ID = 'ee4debf0b2304dda8ca485f3edede48f'
SPOTIPY_CLIENT_SECRET = 'bbb96d6c8b8e43fbab8874cf97a477bd'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:8000/callback'

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
    if media_type == 'video':
        return [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]
    else:  # audio
        return [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    
def download_media(url, media_type='audio', playlist_name=None):
    ffmpeg_path = 'C:/ffmpeg/bin/ffmpeg.exe'

    output_dir = f"./{playlist_name}/" if playlist_name else "./downloads/"
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
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

    api_key = 'AIzaSyBcp3Bz71_BR05W9rMaXR3xsMMf04c-278'
    
    print(f"Playlist Name: {playlist_name}")
    print(f"Found {len(tracks)} tracks in the playlist:")
    for i, item in enumerate(tracks):
        track = item['track']
        song = f"{track['name']} by {', '.join([artist['name'] for artist in track['artists']])}"
        print(f"{i+1}. {song}")
        download_media(get_youtube_video_link(api_key, song),'audio', playlist_name)


playlist_url = input("Enter Spotify playlist URL: ")
download_playlist(playlist_url)