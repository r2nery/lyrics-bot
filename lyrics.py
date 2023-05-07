import requests
import json
import config

api_key = config.API_KEY_MUSIXMATCH

# set the artist and song variables
artist_name = "Bruno Mars"
song_name = "Uptown Funk"

# set the API endpoint URLs
search_url = "https://api.musixmatch.com/ws/1.1/track.search"
lyrics_url = "https://api.musixmatch.com/ws/1.1/track.subtitle.get"

# make a request to the search endpoint to get the track ID
search_params = {"apikey": api_key, "q_artist": artist_name, "q_track": song_name}
search_response = requests.get(search_url, params=search_params)
search_data = json.loads(search_response.text)
# save as json
with open("search_data.json", "w") as outfile:
    json.dump(search_data, outfile)
track_id = search_data["message"]["body"]["track_list"][0]["track"]["commontrack_id"]

# make a request to the lyrics endpoint to get the lyrics
lyrics_params = {"apikey": api_key, "commontrack_id": track_id}
lyrics_response = requests.get(lyrics_url, params=lyrics_params)
lyrics_data = json.loads(lyrics_response.text)
# print(lyrics_data)
lyrics = lyrics_data["message"]["body"]["lyrics"]["lyrics_body"]

# print the lyrics
print(lyrics)
