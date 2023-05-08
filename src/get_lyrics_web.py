import requests
from pathlib import Path
from bs4 import BeautifulSoup
from config import *


class GetLyrics:
    def __init__(self, query, source):
        self.query = query
        self.source = source
        self.exclude = [
            "-",
            "feat",
            "ft",
            "ft.",
            "ft:",
            "ft-",
            "[Official",
            "(Official",
            "(Oficial",
            "[Oficial",
            "[Official]",
            "(Official)",
            "(Oficial)",
            "[Oficial]",
            "[Video",
            "(Video",
            "[Vídeo",
            "(Vídeo",
            "[Video]",
            "(Video)",
            "[Vídeo]",
            "(Vídeo)",
            "Video]",
            "Video)",
            "Vídeo]",
            "Vídeo)",
            "Official]",
            "Official)",
            "Oficial]",
            "Oficial)",
            "Official",
            "Video",
            "[",
            "]",
            "(",
            ")",
            "Oficial",
            "Lyric",
            "Lyrics",
            "Video",
            "Music",
            "Audio",
            "Visualizer",
            "&",
        ]

        if self.source not in ["letras", "genius"]:
            raise ValueError(f"Unsupported source: {self.source}")

    def get_lyrics(self):
        if self.source == "letras":
            return self.get_lyrics_letras()
        elif self.source == "genius":
            return self.get_lyrics_genius()

    def get_lyrics_letras(self):
        query = [i for i in self.query.split(" ") if i not in self.exclude]
        query = "%20".join(query)
        g_url = f"https://www.googleapis.com/customsearch/v1/siterestrict?key={API_KEY_GOOGLE}&cx={ENGINE_ID_GOOGLE}&q={query}"
        r = requests.get(g_url).json()
        url = r["items"][0]["link"]
        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        body = soup.find("div", class_="cnt-letra")
        lyrics = body.get_text(strip=True, separator="\n").splitlines()
        lyrics = [i.split("(")[0] for i in lyrics]  # strip characters inside parentheses

        return lyrics


if __name__ == "__main__":
    query = "Preto no Branco - Ninguém Explica Deus (Ao Vivo) ft. Gabriela Rocha"
    source = "letras"
    lyrics = GetLyrics(query, source).get_lyrics()

    # save lyrics to file
    cwd = Path.cwd()
    lyrics_dir = cwd / "2.lyrics"
    with open(lyrics_dir / f"{query}.txt", "w") as f:
        f.write("\n".join(lyrics))
