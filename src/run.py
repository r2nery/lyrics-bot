from assemble_video import *
from get_yt_mp3 import *
from get_lyrics_ai import *
from crop_audio import *
from pathlib import Path

cwd = Path.cwd()
dl_dir = cwd / "0.downloads"
clips_dir = dl_dir / "0.1.clips"
crops_dir = cwd / "1.crops"
lyrics_dir = cwd / "2.lyrics"
results_dir = cwd / "3.results"

url = "https://www.youtube.com/watch?v=AWGqoCNbsvM"
song = yt_dl(url)

v_clip = Path(clips_dir / f"v2.mp4")
a_clip = Path((dl_dir / f"{song}.mp3"))
crop_a_clip = Path(crops_dir / f"{song}.mp3")
lyrics = Path(lyrics_dir / f"{song}.srt")
output = Path(results_dir / f"{song}.mp4")

CropAudio(a_clip, crops_dir).crop()
get_srt_whisper(crop_a_clip)
create_karaoke_video(v_clip, output, crop_a_clip, lyrics, snippet_duration=3, final_duration=60)
