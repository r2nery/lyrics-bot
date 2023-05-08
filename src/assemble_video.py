from moviepy.editor import *
from pathlib import Path
import random
from moviepy.video.tools.subtitles import SubtitlesClip

# Define the input and output files
input_file = Path("0.downloads/0.1.clips/v1.mp4")
output_file = Path("results/v1_edit.mp4")
audio_file = Path("1.crops/a1.mp3")
lyrics_file = Path("2.lyrics/l1.srt")
snippet_duration = 5  # in seconds
final_duration = 60  # in seconds


def create_karaoke_video(
    input_file,
    output_file,
    audio_file,
    lyrics_file,
    padding=10,
    snippet_duration=5,
    final_duration=60,
):
    clip = VideoFileClip(str(input_file))
    valid_start_time = padding
    valid_end_time = clip.duration - padding - snippet_duration

    # Define the list of snippet start times
    snippet_start_times = []
    while sum([snippet_duration for start in snippet_start_times]) < final_duration:
        # Generate a random start time within the valid range
        start_time = random.uniform(valid_start_time, valid_end_time)
        # Check if the start time is too close to any existing snippet
        if all(abs(start_time - s) >= snippet_duration for s in snippet_start_times):
            snippet_start_times.append(start_time)
    # Create the list of snippet clips
    snippet_clips = []
    for start_time in snippet_start_times:
        end_time = start_time + snippet_duration
        snippet_clip = clip.subclip(start_time, end_time)
        snippet_clips.append(snippet_clip)
    # Concatenate the snippet clips to form the final clip
    final_clip = concatenate_videoclips(snippet_clips)

    # Resize the final clip
    new_height = 1280
    new_width = int(final_clip.w * (new_height / final_clip.h))
    final_clip = final_clip.resize(width=new_width, height=new_height)

    # Create a new black background clip with the desired frame dimensions
    background = ColorClip(size=(720, 1280), color=(0, 0, 0))

    # Calculate the position of the top-left corner of the final clip in the new frame
    x_pos = (720 - final_clip.w) // 2
    y_pos = 0

    # Overlay the final clip on top of the black background clip at the desired position
    final_clip = CompositeVideoClip([background, final_clip.set_position((x_pos, y_pos))])

    # Create the subtitles clip
    generator = lambda txt: TextClip(
        txt,
        font="HelveticaNeueLTStd-HvCn",
        fontsize=32,
        color="white",
        stroke_color="black",
        stroke_width=1,
        method="caption",
        size=(700, 700),
    )
    subs = SubtitlesClip(str(lyrics_file), generator)
    subtitles = SubtitlesClip(subs, generator)

    # Overlay the subtitles on top of the final clip
    final_clip = CompositeVideoClip([final_clip, subtitles.set_pos(("center", "center"))])

    # Set the duration of the final clip
    final_clip = final_clip.set_duration(final_duration)

    # Load the audio file
    audio_clip = AudioFileClip(str(audio_file))
    final_clip = final_clip.set_audio(audio_clip)

    # Write the output video
    final_clip.write_videofile(
        str(output_file), fps=clip.fps, threads=8, preset="ultrafast", codec="libx264"
    )
