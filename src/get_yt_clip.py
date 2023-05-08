import youtube_dl
from pathlib import Path

cwd = Path.cwd()
dl_dir = cwd / "0.downloads" / "0.1.clips"
if not dl_dir.exists():
    dl_dir.mkdir()

# Replace the URL with the URL of the YouTube video you want to download
url = "https://www.youtube.com/watch?v=rPJ0q1j8n6U"

# Set the options for youtube_dl
ydl_opts = {
    "outtmpl": str(dl_dir / "v3.%(ext)s"),
    "format": "mp4",
}

# Create a downloader object
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    # Download the video and get the metadata
    info_dict = ydl.extract_info(url, download=True)
