# Spotify/YouTube Playlist Downloader

A fully automated Python application that downloads entire music collections with a single command. Support for both **Spotify playlists/albums** and **YouTube playlists**:
- **Spotify**: Paste a playlist or album link, and the app intelligently searches YouTube, matches each track, and downloads high-quality audio files
- **YouTube**: Paste a YouTube playlist URL, and the app directly downloads all videos as audio files

All downloads are organized into neatly structured folders without any manual intervention required.

---

## The Challenge We Tackled

Music streaming has revolutionized how we consume audio content, but it comes with a fundamental limitation: you never truly own your music. Spotify, despite its vast library and sophisticated algorithms, operates on a rental model. Your carefully curated playlists exist only as long as you maintain your subscription and the licensing agreements hold. When songs are removed from the platform or when you travel to regions with limited connectivity, your music becomes inaccessible.

The traditional workaround involves manually searching for each song on YouTube, downloading them individually, and organizing hundreds of files by hand. This process is not only time-consuming but also error-prone. You might download the wrong version, end up with inconsistent audio quality, or struggle with file naming conventions that make organization a nightmare.

We identified three critical pain points in the current landscape:

**Manual Labor at Scale:** Downloading a 50-song playlist means performing the same search-download-organize cycle 50 times. This repetitive task consumes hours that could be better spent elsewhere.

**Inconsistent Quality and Versions:** YouTube hosts multiple versions of the same song—live performances, covers, remixes, lyric videos, and official audio. Without careful attention, you might download a concert recording when you wanted the studio version, or vice versa.

**Organization Chaos:** After downloading, users face the daunting task of organizing files, creating folders, and maintaining a structure that makes sense. File names from YouTube are often cryptic or excessively long, making library management frustrating.

These challenges inspired us to build a solution that respects both the convenience of modern streaming and the autonomy of owning your music collection.

---

## What This Downloader Does

Our solution emerged from a simple question: what if we could automate the entire workflow while giving users precise control over what they download? We designed this application to support two powerful workflows:

### Spotify Workflow

The journey begins with Spotify's API. When you provide a playlist or album URL, we extract complete track information: song titles, artist names, and album details. This data serves as our blueprint. Next, we leverage YouTube's Data API to intelligently search for each track. Here's where we introduced a key innovation: **customizable search keywords**. Users can specify whether they want "lyrics" videos, "visualizer" versions, "official audio," or any other modifier. This granular control ensures you get exactly the version you desire.

Once matches are identified, our application delegates the download process to yt-dlp, a robust command-line tool that handles YouTube's ever-changing architecture. We extract high-quality M4A audio files while maintaining metadata integrity. Every download is logged in a structured CSV file that maps each track to its corresponding YouTube video, creating a transparent record of your collection.

### YouTube Playlist Workflow (NEW)

When you provide a YouTube playlist URL, the app automatically detects it and switches to direct download mode. It extracts all video URLs from the playlist using yt-dlp's playlist extraction capabilities, then downloads each video as high-quality M4A audio files—completely bypassing the YouTube search step since you're already providing direct links. This is perfect for:
- Downloading curated YouTube music playlists
- Archiving YouTube music collections
- Getting audio from video compilations
- Any public YouTube playlist with music content

### Core Features

#### Automatic URL Detection

- **Intelligently detects** whether input is a Spotify or YouTube playlist URL
- Routes to appropriate workflow automatically—no manual selection needed
- Supports Spotify playlists, Spotify albums, and YouTube playlists
- Works seamlessly with URL formats including query parameters

#### Intelligent Track Matching (Spotify)

- Automatically extracts song and artist information from Spotify playlists and albums
- Searches YouTube with **customizable keywords** to find the exact version you want
- Supports "lyrics," "visualizer," "official audio," "live," "acoustic," and custom search terms
- Uses YouTube's music category filter to prioritize official content
- **Handles pagination** for large playlists exceeding 100 tracks seamlessly

#### Direct Playlist Download (YouTube)

- **NEW**: Extracts all videos from YouTube playlist URLs directly
- No YouTube search needed—downloads from direct video links
- Supports public YouTube playlists with any number of videos
- Perfect for music compilations, curated playlists, and audio archives

#### Multi-Platform Support

- Works with **Spotify playlists and albums** using the same interface
- Works with **YouTube playlists** with automatic detection
- Parses URLs automatically to determine content type
- Maintains compatibility with Spotify's authentication flow
- Extracts complete metadata including track names, artists, and album information

#### Smart Organization System

- Creates dedicated folders named after playlists or albums
- Sanitizes folder names to ensure file system compatibility
- Downloads all tracks as high-quality M4A audio files
- Preserves YouTube video titles in filenames for easy identification
- Generates a comprehensive CSV file with four columns: Track Name, Artist(s), YouTube Link, and **Video Title**

#### Transparent Tracking

- Records every downloaded track in a structured CSV format
- Maps each song to its specific YouTube source for future reference
- Enables users to verify which versions were downloaded
- Provides a permanent record that survives file reorganization

#### Automated Dependency Management

- Checks for required Python packages and **installs them automatically**
- Verifies yt-dlp availability and installs if missing
- Validates API credentials before processing
- Provides clear error messages when setup is incomplete

---

## Technical Foundation

Building a reliable automation tool required careful selection of technologies that balance power, maintainability, and ease of deployment. Our architecture relies on proven libraries and modern APIs.

### Core Technologies

**Python 3.7+** serves as our foundation, chosen for its robust ecosystem and cross-platform compatibility. The language's readability ensures that the codebase remains accessible to developers of varying skill levels.

**Spotipy** provides our gateway to Spotify's Web API. This official Python library handles authentication complexities and API rate limiting, allowing us to focus on business logic rather than HTTP request management.

**Google API Python Client** connects us to YouTube's Data API v3. We use this to perform intelligent searches within YouTube's music category, ensuring results are relevant and high-quality.

**yt-dlp** handles the actual download process. This actively maintained fork of youtube-dl adapts quickly to YouTube's frequent changes, providing reliability that custom download implementations cannot match.

**Pandas** manages our data structures. We use DataFrames to organize track information, perform bulk operations, and export results to CSV format with minimal code complexity.

**python-dotenv** manages our environment variables. API keys remain secure in local .env files, never exposed in version control or hardcoded into source files.

**tqdm** enhances user experience with real-time progress bars. Users see exactly how many tracks have been processed and how many remain, reducing perceived wait times.

### Architecture Decisions

We structured the application around three core principles: **modularity**, **error resilience**, and **user transparency**.

**Modularity** manifests in our function design. Each function handles a single responsibility—extracting Spotify data, searching YouTube, creating folders, or downloading files. This separation allows us to test components independently and swap implementations without cascading changes.

**Error resilience** guided our exception handling strategy. When a single track fails to download, the application logs the error and continues with remaining tracks. Network timeouts, API rate limits, and missing videos don't crash the entire process. Users receive a success rate summary at the end, highlighting what worked and what needs attention.

**User transparency** drove our decision to generate detailed CSV files. Rather than operating as a black box, we provide a clear audit trail. Users can inspect which YouTube videos were selected, verify that versions match expectations, and manually intervene if needed.

### API Integration Strategy

Spotify and YouTube impose rate limits to prevent abuse. We respect these constraints through intelligent request management. For Spotify, we batch track requests and handle pagination automatically. For YouTube, we limit concurrent searches and implement exponential backoff when approaching quota limits.

Authentication follows industry best practices. Spotify uses OAuth 2.0 client credentials flow, while YouTube relies on API keys. Both credentials remain local, never transmitted outside official API endpoints.

---

## Getting Started

### Prerequisites

Before running the application, ensure your system meets these requirements:

- **Python 3.7 or higher** installed and accessible from your terminal
- **Active internet connection** for API requests and downloads
- **Spotify Developer Account** for API credentials
- **Google Cloud Account** for YouTube Data API access

### Step 1: Obtain API Credentials

#### Spotify API Setup

1. Navigate to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account credentials
3. Click the "Create an App" button in the dashboard
4. Provide an application name and description (these are for your reference only)
5. After creation, locate your **Client ID** and **Client Secret** on the app's dashboard
6. Keep these credentials secure—they authenticate your application with Spotify's servers

#### YouTube API Setup

1. Visit the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one from the project dropdown
3. Navigate to the "APIs & Services" section in the left sidebar
4. Click "Enable APIs and Services" and search for "YouTube Data API v3"
5. Enable the API for your project
6. Go to "Credentials" and click "Create Credentials," then select "API Key"
7. Copy the generated API key—this authenticates your YouTube requests
8. Consider restricting the key to YouTube Data API v3 only for security

### Step 2: Configure Environment Variables

The application reads API credentials from a local environment file, keeping sensitive information out of source code.

1. Locate the `env_template.txt` file in the project directory
2. Create a new file named `.env` (note the leading dot—this makes it hidden on Unix systems)
3. Open `.env` in a text editor and add your credentials:

```
SPOTIFY_CLIENT_ID=your_actual_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_actual_spotify_client_secret
YOUTUBE_API_KEY=your_actual_youtube_api_key
```

Replace the placeholder values with the credentials obtained in Step 1. Ensure there are no spaces around the equals signs and no quotation marks around values.

**Important:** Never commit the `.env` file to version control. The `.gitignore` file already excludes it, but verify before pushing to remote repositories.

### Step 3: Install Dependencies

The application requires several Python packages. You have three installation options:

#### Option A: Automated Installation (Recommended)

Run the included helper script:

```bash
python install_requirements.py
```

This script installs all dependencies automatically and provides a summary of successful installations.

#### Option B: Virtual Environment (Best Practice)

Using a virtual environment isolates dependencies and prevents conflicts with system packages.

On macOS and Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install spotipy pandas google-api-python-client tqdm python-dotenv yt-dlp
```

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install spotipy pandas google-api-python-client tqdm python-dotenv yt-dlp
```

#### Option C: System-Wide Installation

Install packages directly to your system Python (not recommended for production use):

```bash
pip install spotipy pandas google-api-python-client tqdm python-dotenv yt-dlp
```

### Step 4: Run the Application

Navigate to the project directory in your terminal and execute the main script.

If using a virtual environment (recommended):

```bash
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows

python spotify_to_youtube.py
```

Or run directly without activation:

```bash
.venv/bin/python spotify_to_youtube.py  # On macOS/Linux
# or
.venv\Scripts\python spotify_to_youtube.py  # On Windows
```

### Step 5: Provide Input

The application prompts for a Spotify URL and an optional search keyword:

```
Enter your Spotify playlist/album URL and optional search keyword
Format: {URL} [keyword]

Input:
```

#### Basic Usage

Paste a Spotify URL without keywords to use the default "lyrics" search:

```
https://open.spotify.com/album/4a6NzYL1YHRUgx9e3YZI6I
```

The application searches YouTube for "[Song Name] [Artist] lyrics" for each track.

#### Advanced Usage with Keywords

Add a space and keyword after the URL to customize search terms:

```
https://open.spotify.com/album/4a6NzYL1YHRUgx9e3YZI6I visualizer
```

This searches for "[Song Name] [Artist] visualizer" instead.

**Useful Keywords:**

- `official audio` - Studio recordings without video
- `visualizer` - Animated visual content
- `lyric video` - Videos with on-screen lyrics
- `live` - Concert performances
- `acoustic` - Unplugged versions
- `instrumental` - Versions without vocals
- `remix` - Remixed versions

### Step 6: Monitor Progress

The application provides real-time feedback throughout the process:

1. **Spotify Extraction:** Displays album/playlist name and track count
2. **Folder Creation:** Confirms folder creation with sanitized name
3. **YouTube Search:** Shows progress bar as each track is matched
4. **Match Summary:** Displays first five matches with video titles
5. **Download Progress:** Indicates download status for each file
6. **Completion Report:** Lists all successfully downloaded files with their locations

### Step 7: Access Your Music

After completion, find your downloads in the newly created folder:

```
Project Directory/
└── [Album or Playlist Name]/
    ├── [Track 1 with YouTube Title].m4a
    ├── [Track 2 with YouTube Title].m4a
    ├── [Track 3 with YouTube Title].m4a
    └── spotify_playlist_with_youtube.csv
```

The CSV file contains four columns:

- **Track Name:** Original song title from Spotify
- **Artist Name(s):** Performing artists
- **YouTube Link:** Direct URL to the downloaded video
- **YouTube Video Title:** Actual title of the YouTube video

This file serves as a reference for which versions were downloaded and allows you to verify matches.

---

## Troubleshooting

### ModuleNotFoundError: No module named 'spotipy'

**Cause:** Python cannot locate installed packages, typically because you are using system Python instead of your virtual environment.

**Solution:** Run the script using the virtual environment's Python interpreter:

```bash
.venv/bin/python spotify_to_youtube.py  # macOS/Linux
.venv\Scripts\python spotify_to_youtube.py  # Windows
```

Alternatively, activate the virtual environment before running:

```bash
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate  # Windows
python spotify_to_youtube.py
```

### API Key Not Found

**Cause:** The application cannot locate your `.env` file or it contains incorrect key names.

**Solution:** Verify the following:

- File is named exactly `.env` (with a leading dot)
- File exists in the same directory as `spotify_to_youtube.py`
- Variable names match exactly: `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, `YOUTUBE_API_KEY`
- No spaces around equals signs
- No quotation marks around credential values

### YouTube API Quota Exceeded

**Cause:** YouTube imposes daily quotas on API usage (10,000 units per day by default). Large playlists or multiple sessions can exhaust this limit.

**Solution:**

- Wait 24 hours for the quota to reset
- Create a new API key from a different Google Cloud project
- Use more specific keywords to reduce the number of searches
- Request a quota increase from Google Cloud Console if you need higher limits regularly

### Invalid Playlist URL

**Cause:** The application cannot parse the provided URL or it does not point to a valid Spotify playlist or album.

**Solution:** Ensure you are copying the full URL from Spotify:

- Right-click a playlist or album in Spotify
- Select "Share" then "Copy link to playlist" or "Copy link to album"
- Paste the entire URL, including `https://open.spotify.com/`
- Valid formats: `https://open.spotify.com/playlist/...` or `https://open.spotify.com/album/...`

### Download Failures

**Cause:** Network interruptions, regional restrictions, or YouTube blocking bot-like behavior.

**Solution:**

- Verify internet connectivity is stable
- Update yt-dlp to the latest version: `pip install --upgrade yt-dlp`
- Try downloading smaller batches (use shorter playlists)
- Check if YouTube is accessible from your network (some institutions block it)
- Consider using a VPN if regional restrictions apply

### Permission Errors

**Cause:** Insufficient file system permissions in the project directory.

**Solution:**

- Ensure you have write permissions for the directory
- On Unix systems, check with `ls -la` and modify with `chmod` if needed
- Run terminal as administrator on Windows if necessary
- Choose a different directory where you have full permissions

---

## Project Structure

```
audioDownloader/
├── spotify_to_youtube.py      # Main application script
├── install_requirements.py    # Dependency installation helper
├── env_template.txt           # Template for API credentials
├── .env                       # Your actual credentials (create this)
├── .gitignore                 # Files to exclude from version control
├── README.md                  # This documentation
└── SETUP.md                   # Additional setup instructions
```

---

## Best Practices

**Start Small:** Test the application with a small playlist (5-10 tracks) before processing larger collections. This helps you verify that credentials are configured correctly and identify any issues early.

**Use Specific Keywords:** Experiment with different search keywords to find the versions that best match your preferences. "Official audio" typically provides studio quality, while "visualizer" offers a balance of quality and visual interest.

**Review CSV Files:** Before assuming downloads are correct, open the generated CSV file and spot-check a few YouTube links. This verification step ensures you are getting the intended versions.

**Respect API Limits:** YouTube and Spotify both impose rate limits. Avoid running multiple instances of the application simultaneously, as this may trigger throttling or temporary bans.

**Keep Credentials Secure:** Never share your `.env` file or commit it to public repositories. Treat API keys like passwords—they provide access to your accounts.

**Update Dependencies Regularly:** Libraries evolve to fix bugs and adapt to API changes. Run `pip install --upgrade [package-name]` periodically to stay current, especially for yt-dlp.

---

## Future Enhancements

While the current implementation solves the core problem effectively, several enhancements could extend functionality:

- **Metadata Preservation:** Embed artist, album, and track information directly into M4A files using ID3 tags
- **Parallel Downloads:** Implement concurrent downloads to reduce total processing time for large playlists
- **Quality Selection:** Allow users to choose between different audio quality levels (128kbps, 320kbps, lossless)
- **GUI Interface:** Develop a graphical user interface for users less comfortable with command-line tools
- **Playlist Synchronization:** Detect changes in Spotify playlists and download only new additions
- **Format Options:** Support additional output formats beyond M4A (MP3, FLAC, WAV)

---

## Contributing

This project welcomes contributions from developers interested in music automation, API integration, or Python development. Whether you are fixing bugs, improving documentation, or proposing new features, your input is valuable.

---

## License

This project is intended for educational purposes and personal use. Ensure you comply with YouTube's Terms of Service and respect copyright laws when downloading content. The developers of this application are not responsible for misuse or violations of third-party terms.

---

## Acknowledgments

This application builds upon the excellent work of the open-source community, particularly the developers of Spotipy, yt-dlp, and the Google API Python Client. Their robust libraries made this project possible without reinventing complex API interactions.
