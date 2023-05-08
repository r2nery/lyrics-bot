# read srt file as a dict
import re
from pathlib import Path
from collections import defaultdict
import math


def srt_to_tuples(srt_file):
    with open(srt_file, "r") as f:
        srt_text = f.read()

    # split the SRT text into individual subtitle blocks
    srt_blocks = re.split(r"\n\s*\n", srt_text.strip())

    # loop through the subtitle blocks and extract the text and timecodes
    tuples_list = []
    for block in srt_blocks:
        # extract the text
        text_lines = block.split("\n")[2:]
        text = " ".join(text_lines)

        # extract the timecodes
        timecode_line = block.split("\n")[1]
        start_time, end_time = re.findall(r"(\d\d:\d\d:\d\d,\d\d\d)", timecode_line)

        # add the text and timecode tuple to the list
        tuples_list.append((text, (start_time, end_time)))

    return tuples_list


cwd = Path.cwd()
lyrics_dir = cwd / "2.lyrics"
file = "Preto no Branco - Ninguém Explica Deus (Ao Vivo) ft. Gabriela Rocha.mp3.srt"
file_txt = "Preto no Branco - Ninguém Explica Deus (Ao Vivo) ft. Gabriela Rocha.txt"

# get list of strings from txt
with open(lyrics_dir / file_txt, "r") as f:
    lyrics_text = f.read().splitlines()

# convert the SRT file to a list of tuples
srt_tuples = srt_to_tuples(lyrics_dir / file)
limit = len(lyrics_text) - len(srt_tuples)

p = None

jacs = []
for i in range(limit):
    for j in range(len(srt_tuples)):
        sets_1 = [set(srt_tuples[j][0].split()) for j in range(len(srt_tuples))]
        sets_2 = [set(lyrics_text[j + i].split()) for j in range(len(srt_tuples))]
        jac_sims = [
            len(set1.intersection(set2)) / len(set1.union(set2))
            for set1, set2 in zip(sets_1, sets_2)
        ]
    jac_avg = sum(jac_sims) / len(jac_sims)
    jacs.append((i, jac_avg))
# get first value of tuple with max second value
max_jac = max(jacs, key=lambda x: x[1])[0]

lyrics_text = lyrics_text[max_jac : max_jac + len(srt_tuples)]
a = [(x, y[0]) for x, y in zip(lyrics_text, srt_tuples)]
[print(_) for _ in a]
