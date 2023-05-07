import youtube_dl
from pathlib import Path

cwd = Path.cwd()
dl_dir = cwd / "downloads"
if not dl_dir.exists():
    dl_dir.mkdir()

# Replace the URL with the URL of the YouTube video you want to download
url = "https://www.youtube.com/watch?v=wSKKEAnLTDw"

# Set the options for youtube_dl
ydl_opts = {
    "outtmpl": str(dl_dir / "%(title)s.%(ext)s"),
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
}

# Create a downloader object
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    # Download the video and get the metadata
    info_dict = ydl.extract_info(url, download=True)
