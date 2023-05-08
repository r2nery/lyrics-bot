# Lyric video maker

This is a simple lyric video generator based on Whisper.

Inputs are YouTube URLs for the background video and song.
The most salient minute is detected with spectrogram analysis and the lyrics are generated using the OpenAI API with the Whisper model. 
Input videos must be 16:9 and output is 9:16. Parameters such as length, fontsize, bitrate and more can also be tweaked.


````
bot = VideoBot(
        bg_url=bg_url,
        song_url=song_url,
        results_dir=results_dir,
        downloads_dir=downloads_dir,
        lyrics_dir=lyrics_dir,
        length=30,
        padding=50,
        snippets=2,
        verbose=False,
    )
    
bot.run()
