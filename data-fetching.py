import musicbrainzngs
import json
from typing import Dict, List
import time

# Set up MusicBrainz API
musicbrainzngs.set_useragent(
    "MusicDataCollector",
    "1.0",
    "your@email.com"  # Replace with your email
)

def search_collaborations(start_year: int = 1999, end_year: int = 2009, limit: int = 100) -> List[Dict]:
    """
    Search for songs with multiple artists within the specified year range.
    
    Args:
        start_year (int): Start year for search
        end_year (int): End year for search
        limit (int): Maximum number of results to return
        
    Returns:
        List[Dict]: List of songs matching the criteria
    """
    songs_data = []
    offset = 0
    
    try:
        # We'll search year by year to get better results
        for year in range(start_year, end_year + 1):
            print(f"Searching for collaborations from {year}...")
            
            # Search with specific query parameters
            result = musicbrainzngs.search_recordings(
                query=f'date:{year}',
                limit=limit,
                offset=offset
            )
            
            if 'recording-list' in result:
                for recording in result['recording-list']:
                    # Check if recording has artist credits
                    artist_credit = recording.get('artist-credit', [])
                    
                    # Filter for multiple artists
                    artists = [credit['artist']['name'] 
                             for credit in artist_credit 
                             if isinstance(credit, dict) and 'artist' in credit]
                    
                    if len(artists) < 2:
                        continue
                        
                    # Get release information
                    release_list = recording.get('release-list', [])
                    if not release_list:
                        continue
                        
                    release = release_list[0]
                    release_year = release.get('date', '').split('-')[0]
                    
                    if not release_year.isdigit() or int(release_year) != year:
                        continue
                    
                    # Create song data
                    song_data = {
                        "Song Title": recording['title'],
                        "Artists": ", ".join(artists),
                        "Year": str(year),
                        "Country": release.get('country', '')
                    }
                    
                    songs_data.append(song_data)
                    print(f"Found: {song_data['Song Title']} by {song_data['Artists']}")
            
            # Respect rate limiting
            time.sleep(1)
    
    except Exception as e:
        print(f"Error fetching data: {str(e)}")
        return songs_data  # Return any data collected before error
    
    return songs_data

def save_to_json(songs_data: List[Dict], filename: str = "multi_artist_songs.json") -> None:
    """
    Save the songs data to a JSON file.
    
    Args:
        songs_data (List[Dict]): List of song data dictionaries
        filename (str): Name of the output JSON file
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(songs_data, f, indent=4, ensure_ascii=False)
        print(f"\nData successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving data: {str(e)}")

def main():
    # Fetch collaborations from 1999-2009
    print("Searching for songs with multiple artists from 1999-2009...")
    songs_data = search_collaborations(1999, 2009)
    
    if songs_data:
        print(f"\nFound {len(songs_data)} songs with multiple artists")
        save_to_json(songs_data)
    else:
        print("No matching songs found")

if __name__ == "__main__":
    main()