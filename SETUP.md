# Setup Guide for Spotify to YouTube Downloader

## Environment Configuration

This project uses environment variables to keep your API keys secure. Follow these steps to set up your environment:

### Step 1: Configure Environment Variables

#### Option A: Using .env file (Recommended)

1. **Copy the template:**

   ```bash
   cp env_template.txt .env
   ```

2. **Edit the .env file** with your actual API keys:

   ```bash
   # Open .env in your preferred editor
   nano .env
   # or
   code .env
   # or
   vim .env
   ```

3. **Fill in your API keys:**

   ```env
   # Spotify API Credentials
   SPOTIFY_CLIENT_ID=your_actual_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_actual_spotify_client_secret

   # YouTube API Key
   YOUTUBE_API_KEY=your_actual_youtube_api_key
   ```

#### Option B: Set Environment Variables Directly

```bash
# macOS/Linux
export SPOTIFY_CLIENT_ID="your_spotify_client_id"
export SPOTIFY_CLIENT_SECRET="your_spotify_client_secret"
export YOUTUBE_API_KEY="your_youtube_api_key"

# Windows (Command Prompt)
set SPOTIFY_CLIENT_ID=your_spotify_client_id
set SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
set YOUTUBE_API_KEY=your_youtube_api_key

# Windows (PowerShell)
$env:SPOTIFY_CLIENT_ID="your_spotify_client_id"
$env:SPOTIFY_CLIENT_SECRET="your_spotify_client_secret"
$env:YOUTUBE_API_KEY="your_youtube_api_key"
```

### Step 2: Get Your API Keys

#### Spotify API

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Copy the Client ID and Client Secret
4. Add them to your .env file

#### YouTube API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable YouTube Data API v3
4. Create credentials (API Key)
5. Add the API key to your .env file

### Step 3: Run the Application

```bash
python spotify_to_youtube.py
```

**That's it!** The script will automatically:

- ✅ Install all required packages if missing
- ✅ Check for yt-dlp and install it if needed
- ✅ Ask for your Spotify playlist URL
- ✅ Process the playlist and download all songs
- ✅ Organize everything in playlist-specific folders

If everything is configured correctly, you should see:

```
Spotify Playlist to YouTube Downloader
==================================================
Paste your Spotify playlist URL:
```

## Security Notes

- **Never commit your .env file** to version control
- **The .gitignore file** is already configured to exclude .env
- **Regenerate your API keys** if they were ever exposed publicly
- **Keep your .env file** in your local machine only

## Troubleshooting

### "Missing required environment variables"

- Check that your .env file exists
- Verify the variable names match exactly
- Ensure no extra spaces around the = sign

### "Failed to export playlist"

- Verify your Spotify API credentials
- Check if the playlist is public or you have access

### "No YouTube links found"

- Verify your YouTube API key
- Check if you've exceeded API quotas

### "Failed to create playlist folder"

- Check if you have write permissions in the current directory
- Ensure the playlist name doesn't contain too many invalid characters

### Package installation errors

- The script automatically handles package installation
- If it fails, try updating pip: `pip install --upgrade pip`
- Use virtual environment: `python -m venv venv && source venv/bin/activate`

## File Structure After Setup

```
audioDownloader/
├── .env                          ← Your API keys (not in git)
├── .gitignore                   ← Excludes sensitive files
├── env_template.txt             ← Template for .env
├── spotify_to_youtube.py        ← Your one-file application
├── README.md                    ← Project documentation
├── SETUP.md                     ← This setup guide
└── [Playlist Name]/             ← Organized song folders
    ├── csv.csv
    ├── spotify_playlist_with_youtube.csv
    └── [Song1].m4a, [Song2].m4a, etc.
```

## Ready to Use!

Once you've completed the setup:

1. Your API keys are secure
2. The project is ready for open-source sharing
3. You can run the application with just one command
4. Everything is automatic - no manual package installation needed

---

**Happy coding!**
