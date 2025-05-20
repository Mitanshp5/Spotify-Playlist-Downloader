# Spotify Playlist Downloader (SPD)

A Python script that downloads songs from a Spotify playlist by finding them on YouTube and saving them as MP3 files.

## Prerequisites

Before using this script, you'll need to:

1. Install Python (3.6 or higher recommended)
2. Install required Python modules
3. Install FFmpeg and configure its path in the script
4. Set up API credentials for Spotify and YouTube

## Installation Guide

### 1. Install Python Modules

Run the following command to install all required Python modules:

```bash
pip install spotipy yt-dlp google-api-python-client
```

### 2. Install FFmpeg

#### Windows:
1. Download FFmpeg from https://ffmpeg.org/download.html
2. Extract the downloaded ZIP file
3. Add the `bin` folder to your system PATH or note the full path to the `ffmpeg.exe` file

#### macOS (using Homebrew):
```bash
brew install ffmpeg
```

#### Linux (Debian/Ubuntu):
```bash
sudo apt install ffmpeg
```

### 3. API Credentials Setup

1. **Spotify API**:
   - Go to https://developer.spotify.com/dashboard/
   - Create a new app and get your Client ID and Client Secret
   - Add `http://127.0.0.1:8000/callback` as a Redirect URI in your app settings

2. **YouTube API**:
   - Go to https://console.cloud.google.com/
   - Create a new project
   - Enable the YouTube Data API v3 (https://console.developers.google.com/apis/api/youtube.googleapis.com/overview)
   - Create an API key

### 4. Configure the Script

Open `SPD.py` and fill in the following variables at the top of the file:

```python
SPOTIPY_CLIENT_ID = 'your_spotify_client_id'  # Enter your Spotify Client ID
SPOTIPY_CLIENT_SECRET = 'your_spotify_client_secret'  # Enter your Spotify Client Secret
YT_API_KEY = 'your_youtube_api_key'  # Enter your YouTube API Key
FFMPEG_PATH = 'path_to_ffmpeg'  # Enter your ffmpeg path (e.g., 'C:/ffmpeg/bin/ffmpeg.exe' or '/usr/bin/ffmpeg')
```

## Usage

1. Run the script:
   ```bash
   python SPD.py
   ```

2. When prompted, enter the URL of the Spotify playlist you want to download.

3. The script will:
   - Fetch all tracks from the Spotify playlist
   - Search for each track on YouTube
   - Download the audio and save it as MP3 in a folder named after the playlist

## Notes

- The downloaded files will be saved in a `Playlists` folder in the same directory as the script
- The script will automatically clean up temporary folders after completion
- You can restart the script by entering 'r' when prompted

## Disclaimer

This script is for educational purposes only. Please respect copyright laws and only download content you have the rights to access. The developers are not responsible for any misuse of this tool.
