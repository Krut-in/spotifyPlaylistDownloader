#!/usr/bin/env python3
"""
Spotify to YouTube Link Converter

A fully automated application that:
1. Automatically installs required packages if missing
2. Takes Spotify playlist URL as input
3. Exports playlist to CSV with Track Name and Artist Name(s)
4. Searches YouTube for each song using "{song} lyrics" query
5. Adds YouTube links to the dataset
6. Saves results to organized CSV files
7. Automatically downloads all songs to playlist-specific folders
"""

import os
import sys
import subprocess
import importlib
from typing import Optional, Tuple, List

# Package management functions
def install_package(package: str) -> bool:
    """Install a Python package using pip"""
    try:
        print(f"Installing {package}...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f"Successfully installed {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to install {package}")
        return False

def check_and_install_packages() -> bool:
    """Check if required packages are installed and install missing ones"""
    print("Checking and installing required packages...")
    print("=" * 50)
    
    required_packages = {
        "spotipy": "spotipy",
        "pandas": "pandas", 
        "googleapiclient": "google-api-python-client",
        "tqdm": "tqdm",
        "dotenv": "python-dotenv"
    }
    
    missing_packages = []
    
    for import_name, package_name in required_packages.items():
        try:
            importlib.import_module(import_name)
            print(f"{package_name} is already installed")
        except ImportError:
            print(f"{package_name} is missing")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\nInstalling {len(missing_packages)} missing packages...")
        success_count = 0
        
        for package in missing_packages:
            if install_package(package):
                success_count += 1
        
        print(f"\nPackage installation summary:")
        print(f"  Successfully installed: {success_count}")
        print(f"  Failed to install: {len(missing_packages) - success_count}")
        
        if success_count < len(missing_packages):
            print("\nSome packages failed to install. Please install them manually:")
            for package in missing_packages:
                print(f"  pip install {package}")
            return False
        
        print("All required packages are now installed!")
        return True
    else:
        print("All required packages are already installed!")
        return True

def check_yt_dlp() -> bool:
    """Check if yt-dlp is installed and install it if missing"""
    try:
        result = subprocess.run(
            ['yt-dlp', '--version'],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"yt-dlp is installed (version: {result.stdout.strip()})")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("yt-dlp is not installed")
        print("Installing yt-dlp...")
        try:
            subprocess.run(
                [sys.executable, '-m', 'pip', 'install', 'yt-dlp'],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print("yt-dlp installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print("Failed to install yt-dlp")
            print("Please install manually: pip install yt-dlp")
            return False

# Import packages after ensuring they're installed
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from googleapiclient.discovery import build
from tqdm import tqdm
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Utility functions
def sanitize_filename(filename: str) -> str:
    """Convert playlist name to a valid folder name"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    filename = filename.strip(' .')
    
    if len(filename) > 100:
        filename = filename[:100]
    
    return filename

def check_environment() -> bool:
    """Check if all required environment variables are set"""
    required_vars = ['SPOTIFY_CLIENT_ID', 'SPOTIFY_CLIENT_SECRET', 'YOUTUBE_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("Missing required environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\nPlease create a .env file with your API keys:")
        print("1. Copy env_template.txt to .env")
        print("2. Fill in your actual API keys")
        print("3. Never commit .env to version control")
        return False
    
    return True

# Core functionality functions
def export_spotify_playlist(playlist_url: str) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    """Export Spotify playlist or album to DataFrame with Track Name and Artist Name(s)"""
    
    # Check if it's an album or playlist
    if 'album/' in playlist_url:
        # It's an album
        album_id = playlist_url.split('album/')[1].split('?')[0]
        
        try:
            album = sp.album(album_id)
            album_name = album['name']
            print(f"Album: {album_name}")
            print(f"Total tracks: {album['total_tracks']}")
            
            # Extract track information
            track_data = []
            for track in album['tracks']['items']:
                track_info = {
                    'Track Name': track['name'],
                    'Artist Name(s)': ', '.join([artist['name'] for artist in track['artists']])
                }
                track_data.append(track_info)
            
            return pd.DataFrame(track_data), album_name
            
        except Exception as e:
            print(f"Error: {e}")
            return None, None
    
    elif 'playlist/' in playlist_url:
        # It's a playlist
        playlist_id = playlist_url.split('playlist/')[1].split('?')[0]
        
        try:
            playlist = sp.playlist(playlist_id)
            playlist_name = playlist['name']
            print(f"Playlist: {playlist_name}")
            print(f"Total tracks: {playlist['tracks']['total']}")
            
            tracks = []
            results = sp.playlist_tracks(playlist_id)
            tracks.extend(results['items'])
            
            # Handle playlists with more than 100 songs
            while results['next']:
                results = sp.next(results)
                tracks.extend(results['items'])
            
            # Extract track information
            track_data = []
            for track in tracks:
                if track['track']:
                    track_info = {
                        'Track Name': track['track']['name'],
                        'Artist Name(s)': ', '.join([artist['name'] for artist in track['track']['artists']])
                    }
                    track_data.append(track_info)
            
            return pd.DataFrame(track_data), playlist_name
            
        except Exception as e:
            print(f"Error: {e}")
            return None, None
    else:
        print("Invalid URL format. Please provide a Spotify playlist or album URL.")
        return None, None

def get_youtube_link(song_name: str, artist: Optional[str] = None) -> Tuple[Optional[str], Optional[str]]:
    """Search YouTube for '{song_name} lyrics' and return first result with video title"""
    query = f"{song_name} lyrics"
    if artist:
        query += f" {artist}"

    try:
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        
        request = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=1,
            videoCategoryId=10  # Music category
        )
        response = request.execute()

        if response['items']:
            video_id = response['items'][0]['id']['videoId']
            video_title = response['items'][0]['snippet']['title']
            youtube_url = f"https://www.youtube.com/watch?v={video_id}"
            return youtube_url, video_title
    except Exception as e:
        print(f"Error searching for '{query}': {e}")

    return None, None

def create_playlist_folder(playlist_name: str) -> Optional[str]:
    """Create a folder with the playlist name"""
    folder_name = sanitize_filename(playlist_name)
    
    try:
        os.makedirs(folder_name, exist_ok=True)
        print(f"Created folder: {folder_name}")
        return folder_name
    except Exception as e:
        print(f"Failed to create folder: {e}")
        return None

def download_songs(links: List[str], playlist_folder: str) -> bool:
    """Execute yt-dlp command to download all songs to the playlist folder"""
    if not links or not playlist_folder:
        print("No YouTube links or playlist folder specified")
        return False
    
    print(f"\nStarting download of {len(links)} songs...")
    print(f"Downloading to folder: {playlist_folder}")
    print("This may take a while depending on the number of songs...")
    
    # Change to the playlist folder
    original_dir = os.getcwd()
    os.chdir(playlist_folder)
    
    try:
        # Create the yt-dlp command using Python module
        cmd = [
            sys.executable,
            '-m', 'yt_dlp',
            '-f', 'bestaudio[ext=m4a]',
            '--output', '%(title)s.%(ext)s'
        ]
        cmd.extend(links)
        
        print(f"\nExecuting command: {' '.join(cmd[:7])}... [and {len(links)} URLs]")
        print("=" * 60)
        
        # Execute the download command
        subprocess.run(cmd, check=True)
        
        print("=" * 60)
        print("Download completed successfully!")
        print(f"Songs downloaded to: {os.path.abspath('.')}")
        
        # List all downloaded files
        downloaded_files = [f for f in os.listdir('.') if f.endswith('.m4a')]
        if downloaded_files:
            print(f"\nDownloaded {len(downloaded_files)} songs:")
            for file in downloaded_files:
                print(f"  - {file}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Download failed with error: {e}")
        return False
    except KeyboardInterrupt:
        print("\nDownload interrupted by user")
        return False
    finally:
        # Return to original directory
        os.chdir(original_dir)

def process_playlist(playlist_url: str) -> bool:
    """Main function to process a Spotify playlist"""
    print("\nExporting Spotify playlist...")
    df, playlist_name = export_spotify_playlist(playlist_url)
    
    if df is None or playlist_name is None:
        print("Failed to export playlist. Please check your URL and try again.")
        return False
    
    # Create folder for the playlist
    playlist_folder = create_playlist_folder(playlist_name)
    if not playlist_folder:
        print("Failed to create playlist folder")
        return False
    
    print(f"Successfully exported {len(df)} tracks!")
    
    # Show first few tracks
    print("\nFirst few tracks:")
    print(df.head())
    
    print("\nStarting YouTube search...")
    
    # Add progress bar for visual feedback
    tqdm.pandas(desc="Searching YouTube")
    
    # Create YouTube links and video titles
    df[['YouTube Link', 'YouTube Video Title']] = df.progress_apply(
        lambda row: pd.Series(get_youtube_link(row['Track Name'], row['Artist Name(s)'])),
        axis=1
    )
    
    # Check results
    print("\nCompleted searches!")
    print(df[['Track Name', 'Artist Name(s)', 'YouTube Link', 'YouTube Video Title']].head())
    
    # Save enhanced CSV file
    final_output = os.path.join(playlist_folder, "spotify_playlist_with_youtube.csv")
    df.to_csv(final_output, index=False)
    print(f"\nSaved results to {final_output}")
    
    # Show completion message
    success_rate = df['YouTube Link'].notnull().mean()
    print(f"Success rate: {success_rate:.0%}")
    
    # Generate download command and execute
    links = df[df['YouTube Link'].notna()]['YouTube Link'].tolist()
    
    if links:
        command = 'yt-dlp -f "bestaudio[ext=m4a]" --output "%(title)s.%(ext)s" \\\n'
        command += " \\\n".join([f'"{link}"' for link in links])
        
        print("\nDownload command is ready:")
        print("\n" + "="*50)
        print(command)
        print("="*50)
        print(f"\nTotal songs to download: {len(links)}")
        print(f"Songs will be downloaded to: {playlist_folder}/")
        
        # Automatically execute the download
        print("\nStarting automatic download...")
        return download_songs(links, playlist_folder)
    else:
        print("\nNo YouTube links found. Please check your API key and try again.")
        return False

def main():
    """Main application function"""
    print("Spotify Playlist to YouTube Downloader")
    print("=" * 50)
    
    # Check and install required packages
    if not check_and_install_packages():
        print("Failed to install required packages. Please try again.")
        return
    
    # Check environment variables
    if not check_environment():
        return
    
    # Check if yt-dlp is available
    if not check_yt_dlp():
        return
    
    # Get playlist URL from user
    playlist_url = input("Paste your Spotify playlist URL: ").strip()
    
    if not playlist_url:
        print("No URL provided!")
        return
    
    # Process the playlist
    success = process_playlist(playlist_url)
    
    if success:
        print("\nProcess completed successfully!")
    else:
        print("\nProcess failed. Please check the error messages above.")

if __name__ == "__main__":
    # Get API keys from environment variables
    CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
    API_KEY = os.getenv('YOUTUBE_API_KEY')
    
    # Setup Spotify authentication
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    ))
    
    main()
