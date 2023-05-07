import openai
from pathlib import Path
import config

openai.api_key = config.API_KEY_OPENAI

cwd = Path.cwd()
dl_dir = cwd / "downloads"
audio_file = open(str(dl_dir / "v1.mp3"), "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file, timings=True)

print(transcript)
