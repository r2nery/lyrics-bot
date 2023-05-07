import librosa
import numpy as np
import os
from pathlib import Path
from pydub import AudioSegment


class CropAudio:
    def __init__(self, audio_file, out_dir=None, duration=60, format="mp3", verbose=False):
        self.audio_file = Path(audio_file).resolve()
        self.out_dir = Path(out_dir).resolve() if out_dir else None
        self.duration = duration
        self.format = format.lower()
        self.verbose = verbose

        # Validate format
        if self.format not in ["mp3", "wav", "ogg"]:
            raise ValueError(f"Unsupported audio format: {self.format}")

        # Validate input paths
        if not self.audio_file.exists():
            raise ValueError(f"Input audio file '{self.audio_file}' does not exist.")
        if not self.audio_file.is_file():
            raise ValueError(f"Input audio file '{self.audio_file}' is not a file.")
        if self.out_dir is not None:
            if not self.out_dir.exists():
                raise ValueError(f"Output directory '{self.out_dir}' does not exist.")
            if not self.out_dir.is_dir():
                raise ValueError(f"Output directory '{self.out_dir}' is not a directory.")

    def crop(self):
        # Load the audio file
        try:
            y, sr = librosa.load(self.audio_file)
        except Exception as e:
            raise ValueError(f"Failed to load audio file: {e}")

        # Compute the spectrogram of the audio signal
        S = np.abs(librosa.stft(y))

        # Compute the mean value of each frequency band
        band_means = np.mean(S, axis=1)

        # Find the index of the frequency band with the maximum mean value
        max_index = np.argmax(band_means)

        # Compute the start and end time of the most salient portion in seconds
        start_time = round(librosa.frames_to_time(np.argmax(S[max_index, :])))
        end_time = round(start_time + self.duration)

        # Create an AudioSegment object
        audio_segment = AudioSegment.from_file(self.audio_file)

        # Extract the salient portion from the audio segment
        extracted_segment = audio_segment[start_time * 1000 : end_time * 1000]

        if self.out_dir is not None:
            # Save the extracted portion to a new file
            outfile = self.out_dir / f"{self.audio_file.stem}_extracted.{self.format}"
            extracted_segment.export(outfile, format=self.format)

        if self.verbose:
            print(f"Saved audio from {start_time:.2f} to {end_time:.2f} seconds to {outfile}.")

        return extracted_segment
