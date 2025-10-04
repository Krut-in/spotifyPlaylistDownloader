# Spotify to YouTube Downloader - Complete Code Walkthrough

## Project Overview

**What does this project do?**
This is an automated music downloader that takes a Spotify playlist/album URL and downloads all the songs to your computer. Think of it as a "magic tool" that:
1. Reads your Spotify playlist or album
2. Finds the same songs on YouTube
3. Downloads them as high-quality audio files
4. Organizes everything in neat folders

**Why was this built?**
Spotify doesn't let you download songs, and manually finding each song on YouTube is tedious. This tool automates the entire process - you just paste a playlist/album link and get all your music downloaded automatically.

**Example:**
- Input: `https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M` (Today's Top Hits)
- Output: A folder called "Today's Top Hits" containing 50 downloaded songs as M4A audio files

---

## 🚀 Quick Start Guide - Steps to Download Songs

### Prerequisites

Before running the script, you need:

1. **Python 3.7 or higher** installed on your system
2. **Spotify API credentials** (Client ID and Client Secret)
3. **YouTube Data API key**
4. Internet connection

### Step 1: Get Your API Keys

#### Spotify API Setup:
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account
3. Click "Create an App"
4. Fill in the app name and description
5. Copy your **Client ID** and **Client Secret**

#### YouTube API Setup:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable "YouTube Data API v3"
4. Go to "Credentials" and create an API key
5. Copy your **YouTube API Key**

### Step 2: Configure Environment Variables

1. In the project folder, you'll find `env_template.txt`
2. Create a new file named `.env` (exactly like this, starting with a dot)
3. Copy the content from `env_template.txt` to `.env`
4. Replace the placeholder values with your actual API keys:

```env
SPOTIFY_CLIENT_ID=your_actual_client_id_here
SPOTIFY_CLIENT_SECRET=your_actual_client_secret_here
YOUTUBE_API_KEY=your_actual_youtube_api_key_here
```

**Important:** Never share or commit your `.env` file to version control!

### Step 3: Install Python Dependencies

The script automatically installs required packages, but you can install them manually:

```bash
pip install spotipy pandas google-api-python-client tqdm python-dotenv yt-dlp
```

### Step 4: Run the Script

1. Open your terminal/command prompt
2. Navigate to the project folder:
   ```bash
   cd path/to/audioDownloader
   ```

3. Run the script:
   ```bash
   python spotify_to_youtube.py
   ```

### Step 5: Provide Input

When the script runs, you'll see:

```
============================================================
Enter your Spotify playlist/album URL and optional search keyword
Format: {URL} [keyword]
Examples:
  https://open.spotify.com/playlist/xxx
  https://open.spotify.com/album/xxx Visualizer
  https://open.spotify.com/playlist/xxx Audio
============================================================

Input:
```

**You have two options:**

#### Option 1: Basic Usage (Default 'lyrics' search)
Just paste the Spotify URL:
```
https://open.spotify.com/album/4a6NzYL1YHRUgx9e3YZI6I
```
This will search YouTube for each song with "lyrics" appended (e.g., "Song Name Artist lyrics")

#### Option 2: Custom Keyword Search
Paste the URL followed by a space and your preferred keyword:
```
https://open.spotify.com/album/4a6NzYL1YHRUgx9e3YZI6I Visualizer
```

**Supported keywords:**
- `Visualizer` - For official visualizer videos
- `Audio` - For official audio tracks
- `Official` - For official music videos
- `Live` - For live performances
- `Acoustic` - For acoustic versions
- Or any custom keyword you want!

### Step 6: Wait for Downloads

The script will automatically:
1. ✅ Extract song information from Spotify
2. ✅ Create a folder with the playlist/album name
3. ✅ Search YouTube for each song
4. ✅ Save a CSV file with all song details and YouTube links
5. ✅ Download all songs as M4A audio files

**Progress indicators will show:**
- YouTube search progress
- Download progress for each song
- Total songs downloaded

### Step 7: Access Your Downloaded Songs

After completion, you'll find:
- **Folder:** Named after your playlist/album
- **Audio Files:** High-quality M4A files
- **CSV File:** `spotify_playlist_with_youtube.csv` containing:
  - Track Name
  - Artist Name(s)
  - YouTube Link
  - YouTube Video Title

### Example Run

```bash
$ python spotify_to_youtube.py

Spotify Playlist to YouTube Downloader
==================================================
Checking and installing required packages...
All required packages are already installed!

Enter your Spotify playlist/album URL and optional search keyword
Input: https://open.spotify.com/album/4a6NzYL1YHRUgx9e3YZI6I Visualizer

Exporting Spotify playlist...
Album: The Life of a Showgirl
Total tracks: 12
Created folder: The Life of a Showgirl
Successfully exported 12 tracks!

Using custom YouTube search keyword: 'Visualizer'

Starting YouTube search...
Searching YouTube: 100%|██████████| 12/12 [00:15<00:00]

Success rate: 100%

Starting download of 12 songs...
[Download progress for each song...]

Download completed successfully!
Songs downloaded to: The Life of a Showgirl/

Process completed successfully!
```

### Troubleshooting

**Problem: "No module named 'spotipy'"**
- Solution: Run `pip install spotipy pandas google-api-python-client tqdm python-dotenv yt-dlp`

**Problem: "API key not found"**
- Solution: Make sure your `.env` file exists and contains valid API keys

**Problem: "Invalid playlist URL"**
- Solution: Make sure you're using a valid Spotify playlist or album URL

**Problem: "YouTube API quota exceeded"**
- Solution: YouTube API has daily limits. Wait 24 hours or create a new API key

**Problem: Downloads fail**
- Solution: Check your internet connection and ensure yt-dlp is updated

### Tips for Best Results

1. 🎵 **Use specific keywords** for better YouTube matches
2. 📁 **Organize by genre** - Download different playlists to different folders
3. ⚡ **Smaller playlists first** - Test with small playlists before large ones
4. 🔍 **Check CSV file** - Review YouTube links before downloading
5. 💾 **Keep CSV files** - They serve as a backup reference

---

## Technologies & Libraries

### Core Python Libraries
- **`os`** - File and folder operations
- **`sys`** - System information and Python executable path
- **`subprocess`** - Run external commands (like pip install)
- **`importlib`** - Check if packages are installed
- **`typing`** - Type hints for better code clarity

### Third-Party Libraries
- **`spotipy`** - Official Spotify API client
- **`pandas`** - Data manipulation and CSV handling
- **`googleapiclient`** - YouTube Data API v3 client
- **`tqdm`** - Progress bars for user feedback
- **`python-dotenv`** - Load API keys from .env file
- **`yt-dlp`** - YouTube video downloader

### APIs Used
- **Spotify Web API** - Access playlist data
- **YouTube Data API v3** - Search for music videos

---

## Code Structure & Functions

### 1. Package Management Functions

```python
def install_package(package: str) -> bool:
    """Install a Python package using pip"""
```
**Purpose:** Installs missing Python packages automatically
**How it works:** Runs `pip install [package]` and hides verbose output
**Returns:** `True` if successful, `False` if failed

```python
def check_and_install_packages() -> bool:
    """Check if required packages are installed and install missing ones"""
```
**Purpose:** Ensures all required packages are available before running
**How it works:** 
- Tries to import each package
- Lists missing packages
- Installs them automatically
- Shows installation summary

```python
def check_yt_dlp() -> bool:
    """Check if yt-dlp is installed and install it if missing"""
```
**Purpose:** Ensures the YouTube downloader tool is available
**How it works:** Runs `yt-dlp --version` and installs if missing

### 2. Utility Functions

```python
def sanitize_filename(filename: str) -> str:
    """Convert playlist name to a valid folder name"""
```
**Purpose:** Makes playlist names safe for folder creation
**How it works:** Replaces invalid characters (`<>:"/\|?*`) with underscores

```python
def check_environment() -> bool:
    """Check if all required environment variables are set"""
```
**Purpose:** Verifies API keys are configured
**How it works:** Checks if `.env` file contains required variables

### 3. Core Functionality Functions

```python
def export_spotify_playlist(playlist_url: str) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    """Export Spotify playlist to DataFrame with Track Name and Artist Name(s)"""
```
**Purpose:** Extracts song information from Spotify playlist
**How it works:**
- Parses playlist ID from URL
- Fetches playlist data via Spotify API
- Handles playlists with >100 songs (pagination)
- Returns DataFrame with track names and artists

```python
def get_youtube_link(song_name: str, artist: Optional[str] = None) -> Optional[str]:
    """Search YouTube for '{song_name} lyrics' and return first result"""
```
**Purpose:** Finds YouTube video for each song
**How it works:**
- Creates search query: "Song Name lyrics Artist"
- Uses YouTube Data API to search
- Returns first video URL found
- Filters for music category videos

```python
def create_playlist_folder(playlist_name: str) -> Optional[str]:
    """Create a folder with the playlist name"""
```
**Purpose:** Creates organized folder for downloads
**How it works:** Sanitizes name and creates folder using `os.makedirs()`

```python
def download_songs(links: List[str], playlist_folder: str) -> bool:
    """Execute yt-dlp command to download all songs to the playlist folder"""
```
**Purpose:** Downloads all songs using yt-dlp
**How it works:**
- Changes to playlist folder
- Runs yt-dlp command with all URLs
- Downloads in M4A audio format
- Lists all downloaded files
- Returns to original directory

### 4. Main Workflow Functions

```python
def process_playlist(playlist_url: str) -> bool:
    """Main function to process a Spotify playlist"""
```
**Purpose:** Orchestrates the entire playlist processing workflow
**How it works:**
1. Exports playlist from Spotify
2. Creates organized folder
3. Searches YouTube for each song
4. Saves enhanced CSV with YouTube links
5. Downloads all songs automatically

```python
def main():
    """Main application function"""
```
**Purpose:** Entry point and setup coordinator
**How it works:**
1. Checks and installs packages
2. Verifies environment variables
3. Ensures yt-dlp is available
4. Gets playlist URL from user
5. Calls `process_playlist()` function

---

## Process Flow

```
1. Script starts
   ↓
2. Check/install required packages
   ↓
3. Verify API keys in .env file
   ↓
4. Ensure yt-dlp is available
   ↓
5. Get Spotify playlist URL from user
   ↓
6. Export playlist data from Spotify
   ↓
7. Create organized folder
   ↓
8. Search YouTube for each song
   ↓
9. Save enhanced CSV with YouTube links
   ↓
10. Download all songs using yt-dlp
   ↓
11. Show completion status
```

---

## Key Concepts

### API Integration
- **REST APIs** for Spotify and YouTube data
- **Client credentials** for Spotify authentication
- **API quotas** and rate limiting handling

### Data Processing
- **DataFrames** for structured data manipulation
- **CSV export/import** for data persistence
- **Data transformation** from API responses

### System Integration
- **Automatic package management** via pip
- **File system operations** for organization
- **External tool execution** (yt-dlp)

### User Experience
- **Progress tracking** with visual feedback
- **Error handling** with helpful messages
- **Fully automated** workflow

---

## Why This Architecture?

1. **Modular Design** - Each function has single responsibility
2. **Error Handling** - Graceful failure at each step
3. **User Feedback** - Clear progress and status information
4. **Security** - API keys stored in environment variables
5. **Automation** - Minimal user interaction required
6. **Organization** - Clean folder structure for downloads
7. **Portability** - Works on any system with Python

This creates a **professional-grade application** that's both powerful and user-friendly, suitable for academic projects and open-source sharing.