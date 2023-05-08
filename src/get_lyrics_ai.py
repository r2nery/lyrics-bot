import openai
from pathlib import Path
import config as config

openai.api_key = config.API_KEY_OPENAI

cwd = Path.cwd()
dl_dir = cwd / "1.crops"


def get_srt_whisper(file):
    audio_file = open(file, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file, response_format="srt").strip()

    # save srt to lyrics folder
    lyrics_dir = cwd / "2.lyrics"
    with open(lyrics_dir / f"{file.stem}.srt", "w") as f:
        # write transcript to file, cleaning up leading and trailing whitespace
        f.write(transcript)

    pieces = [line for line in transcript.split("\n") if line != ""]
    string = f"\n\n{int(pieces[-3])+1}\n{pieces[-2][-12:]} --> 00:02:00,000"

    with open(lyrics_dir / f"{file.stem}.srt", "a") as f:
        f.write(string)
