from moviepy.editor import *
from pathlib import Path
import os

os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/local/bin/ffmpeg"

cwd = Path.cwd()
dl_dir = cwd / "downloads"
results_dir = cwd / "results"

if not results_dir.exists():
    results_dir.mkdir()
if not dl_dir.exists():
    dl_dir.mkdir()

# Define the input and output files
input_file = dl_dir / "v1.mp4"
output_file = results_dir / "v1_edit.mp4"

# Set the new size and position of the video in the new frame
comp_size = (720, 1280)  # 9:16 aspect ratio

# Load the input video
clip = VideoFileClip(str(input_file))

# Get the original size of the input video
scale_factor = min(comp_size[0] / clip.size[0], comp_size[1] / clip.size[1])
clip_small = clip.resize(scale_factor)
clip_large = clip.resize(1.5)

# Add black bars at the top and bottom
clip_final = CompositeVideoClip(
    [
        ColorClip(comp_size, color=(0, 0, 0)),  # black background
        clip_large.set_position((0, 0)),  # resized video
        clip_small.set_position((0, 0)),  # resized video
    ]
)
# make duration 15 seconds
clip_final = clip_final.set_duration(5)

# Write the output video
clip_final.write_videofile(
    str(output_file), fps=clip.fps, threads=8, preset="ultrafast", codec="libx264"
)
