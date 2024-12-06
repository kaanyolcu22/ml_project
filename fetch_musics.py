import requests
from pydub import AudioSegment
import io
import os

# Replace with your actual client_id
client_id = "1867c83e"
url = "https://api.jamendo.com/v3.0/tracks"

# List of genres to retrieve
genres = ["rock", "pop", "jazz", "electronic", "classical", "hiphop", "metal", "blues", "reggae", "country"]

# Main directory to save clipped samples
main_output_dir = "audio_samples"
os.makedirs(main_output_dir, exist_ok=True)

# Dictionary to store downloadable tracks by genre
downloadable_tracks_by_genre = {}

# Iterate over each genre and retrieve only downloadable tracks
for genre in genres:
    print(f"Fetching downloadable tracks for genre: {genre}")
    
    # Define parameters for the request
    params = {
        "client_id": client_id,
        "format": "json",
        "limit": 10,  # Limit the number of tracks for each genre as an example
        "tags": genre,
        "durationbetween": "50_100",  # Filter for short samples
        "audiodlformat": "mp32",
        "include": "musicinfo",
        "prolicensing": "true"  # Only include tracks with pro licensing (downloadable)
    }
    
    # Make the request to Jamendo API
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        
        # Create subdirectory for the genre
        genre_output_dir = os.path.join(main_output_dir, genre)
        os.makedirs(genre_output_dir, exist_ok=True)
        
        # Initialize the list for the genre
        downloadable_tracks_by_genre[genre] = []
        
        # Store each track in the genre list only if downloadable
        for track in data['results']:
            if track.get("audiodownload_allowed", False):  # Check if download is allowed
                track_info = {
                    "name": track.get("name", "No name available"),
                    "artist": track.get("artist_name", "No artist available"),
                    "audio_url": track.get("audio", "No audio available"),
                    "download_url": track.get("audiodownload", "No download available")
                }
                
                # Append track info to the genre's list if downloadable
                downloadable_tracks_by_genre[genre].append(track_info)
                
                # Download the audio file and clip the segment from 30 to 40 seconds
                audio_response = requests.get(track_info["download_url"])
                if audio_response.status_code == 200:
                    audio_data = io.BytesIO(audio_response.content)
                    audio = AudioSegment.from_file(audio_data, format="mp3")
                    
                    # Clip the 10 seconds from 30 to 40 seconds
                    start_time = 30000  # 30 seconds in milliseconds
                    end_time = 40000    # 40 seconds in milliseconds
                    clipped_audio = audio[start_time:end_time]
                    
                    # Save the clipped audio in the genre-specific folder
                    output_path = os.path.join(genre_output_dir, f"{track_info['name']}.mp3")
                    clipped_audio.export(output_path, format="mp3")
                    print(f"Saved 10-second clip (30-40s) for track: {track_info['name']} in genre {genre}")
                else:
                    print(f"Failed to download audio for track: {track_info['name']}")

    else:
        print(f"Error fetching tracks for genre {genre}: {response.status_code}")