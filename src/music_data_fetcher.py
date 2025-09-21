#!/usr/bin/env python3

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import praw
import json
from datetime import datetime
import sys
import os

CLIENT_ID = '758bdff266684d8889d8c44b7e8a6354'
CLIENT_SECRET = '0fda1038c0f0423ea2278f56b8c17be7'
REDIRECT_URI = 'http://127.0.0.1:8888/callback'
SCOPE = 'user-read-private user-read-email user-top-read user-library-read playlist-read-private'

# Spotify and Reddit API setup
REDDIT_CREDENTIALS = {
    'client_id': 'XckUtGXr_Xr8f3okIzzkqg',
    'client_secret': 'nj3RoTsFR-wOIsT9cJkFotNOjaqzEg',
    'user_agent': 'rap-news-app/1.0 by Ok-Stop-9954'
}

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

def get_additional_artists():
    return ["Kendrick Lamar", "Travis Scott", "Future", "Lil Baby", "21 Savage", 
            "Post Malone", "Kanye West", "Lil Wayne", "Cardi B", "Megan Thee Stallion",
            "Doja Cat", "SZA", "Frank Ocean", "A$AP Rocky", "J. Cole", "Metro Boomin"]

def is_relevant_post(title, selftext="", user_top_artists=None):
    target_artists = (user_top_artists or []) + get_additional_artists()
    
    text_to_check = (title + " " + selftext).lower()
    
    for artist in target_artists:
        if artist.lower() in text_to_check:
            return True
    
    music_keywords = [
        'new music', 'new album', 'new single', 'drops', 'releases', 
        'mixtape', 'ep', 'leak', 'snippet', 'announces', 'teaser',
        'music video', 'collaboration', 'feature', 'beef', 'diss track',
        'fresh', 'first impressions'
    ]
    
    for keyword in music_keywords:
        if keyword in text_to_check:
            return True
    
    return False

def create_article_object(post, category):
    time_diff = datetime.now() - datetime.fromtimestamp(post.created_utc)
    hours_ago = int(time_diff.total_seconds() / 3600)
    age = f"{hours_ago} hours ago" if hours_ago > 0 else "Just now"
    
    return {
        "source": {
            "id": "reddit-hiphopheads",
            "name": f"r/hiphopheads ({category})"
        },
        "author": f"u/{post.author.name}" if post.author else "Unknown",
        "title": post.title,
        "description": post.selftext[:200] + "..." if len(post.selftext) > 200 else post.selftext,
        "url": f"https://reddit.com{post.permalink}",
        "urlToImage": getattr(post, 'thumbnail', None) if hasattr(post, 'thumbnail') and post.thumbnail.startswith('http') else None,
        "publishedAt": datetime.fromtimestamp(post.created_utc).isoformat() + "Z",
        "content": post.selftext[:400] + "..." if len(post.selftext) > 400 else post.selftext or f"Reddit discussion: {post.title}",
        "score": post.score,
        "comments": post.num_comments,
        "age": age,
        "reddit_url": post.url if not post.is_self else f"https://reddit.com{post.permalink}"
    }

def fetch_reddit_articles(user_top_artists):
    print(f"\n📰 Now fetching Reddit articles based on your music taste...")
    print(f"🎯 Filtering by: {user_top_artists[:3]}... and other hip-hop artists")
    
    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CREDENTIALS['client_id'],
            client_secret=REDDIT_CREDENTIALS['client_secret'],
            user_agent=REDDIT_CREDENTIALS['user_agent']
        )
        
        print("✅ Connected to Reddit successfully!")
        
        subreddit = reddit.subreddit('hiphopheads')
        articles = []
        processed_posts = set()
        
        # Fetch posts from different Reddit categories
        print("🔥 Scanning hot posts...")
        for post in subreddit.hot(limit=100):
            if post.id not in processed_posts and is_relevant_post(post.title, post.selftext, user_top_artists):
                articles.append(create_article_object(post, "Hot"))
                processed_posts.add(post.id)
        
        print("🆕 Scanning new posts...")
        for post in subreddit.new(limit=100):
            if post.id not in processed_posts and is_relevant_post(post.title, post.selftext, user_top_artists):
                articles.append(create_article_object(post, "New"))
                processed_posts.add(post.id)
        
        print("⭐ Scanning top posts...")
        for post in subreddit.top(time_filter='day', limit=50):
            if post.id not in processed_posts and is_relevant_post(post.title, post.selftext, user_top_artists):
                articles.append(create_article_object(post, "Top"))
                processed_posts.add(post.id)
        
        articles.sort(key=lambda x: (x.get('score', 0) * 0.7 + 
                                    (1000 if 'hours ago' in x.get('age', '') else 0)), 
                      reverse=True)
        
        final_articles = articles[:30]
        
        print(f"✅ Found {len(final_articles)} relevant articles!")
        return final_articles
        
    except Exception as e:
        print(f"❌ Reddit error: {e}")
        return []

def save_to_data_js(articles):
    print(f"\n💾 Saving {len(articles)} articles to src/data.js...")
    
    try:
        js_content = f"""const articles = {json.dumps(articles, indent=2)};

export default articles;"""
        
        data_js_path = "/Users/aryantyagi/rap-news/src/data.js"
        
        print(f"📁 Writing to: {data_js_path}")
        
        with open(data_js_path, 'w', encoding='utf-8') as f:
            f.write(js_content)
        
        if os.path.exists(data_js_path):
            print(f"✅ Successfully updated: {data_js_path}")
            file_size = os.path.getsize(data_js_path)
            print(f"📊 File size: {file_size} bytes")
        else:
            print(f"❌ File was not created!")
        
        if articles:
            print(f"\n🎵 Preview of top articles:")
            for i, article in enumerate(articles[:5], 1):
                print(f"   {i}. {article['title'][:60]}... (Score: {article['score']})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error saving data.js: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Combined Spotify + Reddit Data Fetcher")
    print("=" * 50)
        
    try:
        import spotipy
        import praw
    except ImportError as e:
        print("❌ Please install required packages:")
        print("   pip install spotipy praw")
        exit(1)
        
    print("STEP 1: Getting your Spotify data...")
    spotify_data = get_spotify_data()
        
    if not spotify_data:
        print("💥 Spotify step failed. Check your credentials.")
        exit(1)
    
    print(f"\nSTEP 2: Extracting your top artists for filtering...")
    top_artist_names = [artist['name'] for artist in spotify_data['top_artists']['short_term'][:5]]
    print(f"🎯 Your top 5 artists: {top_artist_names}")
    
    print(f"\nSTEP 3: Getting Reddit articles...")
    articles = fetch_reddit_articles(top_artist_names)
    
    if not articles:
        print("💥 Reddit step failed. Using fallback.")
        articles = []
    
    # Final data processing and file output
    print(f"\nSTEP 4: Creating data.js...")
    success = save_to_data_js(articles)
    
    if success:
        print(f"\n🎉 COMPLETE SUCCESS!")
        print(f"📊 Based on your Spotify artists: {', '.join(top_artist_names)}")
        print(f"📰 Found {len(articles)} personalized articles")
        print(f"📱 data.js is ready for your app!")
    else:
        print(f"\n💥 Something went wrong with data.js creation.")