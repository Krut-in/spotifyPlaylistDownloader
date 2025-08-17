#!/usr/bin/env python3
"""
Installation script for Spotify to YouTube Downloader
"""

import subprocess
import sys

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"Successfully installed {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to install {package}")
        return False

def main():
    print("Installing required packages for Spotify to YouTube Downloader")
    print("=" * 60)
    
    packages = [
        "spotipy",
        "pandas", 
        "google-api-python-client",
        "tqdm",
        "python-dotenv",
        "yt-dlp"
    ]
    
    success_count = 0
    for package in packages:
        if install_package(package):
            success_count += 1
    
    print("\n" + "=" * 60)
    if success_count == len(packages):
        print("All packages installed successfully!")
        print("\nNext steps:")
        print("1. Copy env_template.txt to .env")
        print("2. Fill in your API keys in .env file")
        print("3. Run: python spotify_to_youtube.py")
        print("4. The script will automatically download songs after processing!")
    else:
        print(f"{len(packages) - success_count} packages failed to install")
        print("Please try installing them manually:")
        for package in packages:
            print(f"   pip install {package}")

if __name__ == "__main__":
    main()
