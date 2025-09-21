import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

CLIENT_ID = '758bdff266684d8889d8c44b7e8a6354'
CLIENT_SECRET = '0fda1038c0f0423ea2278f56b8c17be7'
REDIRECT_URI = 'http://127.0.0.1:8888/callback'

SCOPE = 'user-read-private user-read-email user-top-read user-library-read playlist-read-private'

def get_spotify_data():
    print("🎵 Starting Spotify authentication...")
        
    auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        cache_path=".spotify_cache"
    )
        
    sp = spotipy.Spotify(auth_manager=auth_manager)
        
    try:
        print("✅ Authentication successful!")
                
        print("📊 Fetching user profile...")
        user = sp.user(sp.me()['id'])
                
        print("🎤 Fetching top artists...")
        top_artists_short = sp.current_user_top_artists(limit=20, time_range='short_term')
        top_artists_medium = sp.current_user_top_artists(limit=20, time_range='medium_term')
        top_artists_long = sp.current_user_top_artists(limit=20, time_range='long_term')
                
        print("🎵 Fetching top tracks...")
        top_tracks_short = sp.current_user_top_tracks(limit=20, time_range='short_term')
        top_tracks_medium = sp.current_user_top_tracks(limit=20, time_range='medium_term')
        top_tracks_long = sp.current_user_top_tracks(limit=20, time_range='long_term')
                
        print("💾 Fetching saved tracks...")
        saved_tracks = sp.current_user_saved_tracks(limit=50)
                
        print("📋 Fetching playlists...")
        playlists = sp.current_user_playlists(limit=50)
                
        # Organize all data into structured format
        user_info = sp.me()
        spotify_data = {
            'user_profile': {
                'id': user.get('id', 'N/A'),
                'display_name': user.get('display_name', 'N/A'),
                'followers': user.get('followers', {}).get('total', 0),
                'country': user.get('country', 'N/A'),
                'email': user_info.get('email', 'N/A')
            },
            'top_artists': {
                'short_term': [{'name': artist.get('name', 'Unknown'),
                                'genres': artist.get('genres', []),
                                'popularity': artist.get('popularity', 0)}
                               for artist in top_artists_short.get('items', [])],
                'medium_term': [{'name': artist.get('name', 'Unknown'),
                                 'genres': artist.get('genres', []),
                                 'popularity': artist.get('popularity', 0)}
                                for artist in top_artists_medium.get('items', [])],
                'long_term': [{'name': artist.get('name', 'Unknown'),
                               'genres': artist.get('genres', []),
                               'popularity': artist.get('popularity', 0)}
                              for artist in top_artists_long.get('items', [])]
            },
            'top_tracks': {
                'short_term': [{'name': track.get('name', 'Unknown'),
                               'artist': track.get('artists', [{}])[0].get('name', 'Unknown'),
                               'popularity': track.get('popularity', 0)}
                               for track in top_tracks_short.get('items', [])],
                'medium_term': [{'name': track.get('name', 'Unknown'),
                                'artist': track.get('artists', [{}])[0].get('name', 'Unknown'),
                                'popularity': track.get('popularity', 0)}
                                for track in top_tracks_medium.get('items', [])],
                'long_term': [{'name': track.get('name', 'Unknown'),
                              'artist': track.get('artists', [{}])[0].get('name', 'Unknown'),
                              'popularity': track.get('popularity', 0)}
                              for track in top_tracks_long.get('items', [])]
            },
            'saved_tracks_count': saved_tracks.get('total', 0),
            'playlists': [{'name': playlist.get('name', 'Unknown'),
                           'tracks': playlist.get('tracks', {}).get('total', 0)}
                          for playlist in playlists.get('items', [])]
        }
                
        with open('spotify_data.json', 'w') as f:
            json.dump(spotify_data, f, indent=2)
                
        print("\n🎉 SUCCESS! Your Spotify data has been saved to 'spotify_data.json'")
                
        print(f"\n📈 Quick Stats:")
        print(f"   • User: {spotify_data['user_profile']['display_name']}")
        print(f"   • Followers: {spotify_data['user_profile']['followers']}")
        print(f"   • Saved tracks: {spotify_data['saved_tracks_count']}")
        print(f"   • Playlists: {len(spotify_data['playlists'])}")
                
        print(f"\n🎤 Your top artists (last 4 weeks):")
        for i, artist in enumerate(spotify_data['top_artists']['short_term'][:5], 1):
            genres = ', '.join(artist['genres'][:2]) if artist['genres'] else 'No genres'
            print(f"   {i}. {artist['name']} ({genres})")
                
        print(f"\n🎵 Your top tracks (last 4 weeks):")
        for i, track in enumerate(spotify_data['top_tracks']['short_term'][:5], 1):
            print(f"   {i}. {track['name']} by {track['artist']}")
                    
        return spotify_data
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Spotify Data Fetcher")
    print("=" * 50)
        
    try:
        import spotipy
    except ImportError:
        print("❌ Please install spotipy first:")
        print("   pip install spotipy")
        exit(1)
        
    # Main execution flow
    data = get_spotify_data()
        
    if data:
        print(f"\n✨ Spotify data collection complete!")
        print(f"🔄 Ready for next step in workflow...")
    else:
        print(f"\n💥 Something went wrong. Make sure your credentials are correct.")
        exit(1)