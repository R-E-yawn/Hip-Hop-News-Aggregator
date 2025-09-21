import praw
import json
from datetime import datetime

def get_reddit_credentials():
    return {
        'client_id': 'XckUtGXr_Xr8f3okIzzkqg',
        'client_secret': 'nj3RoTsFR-wOIsT9cJkFotNOjaqzEg',
        'user_agent': 'rap-news-app/1.0 by Ok-Stop-9954'
    }

def get_top_artists_from_spotify():
    try:
        with open('spotify_data.json', 'r') as f:
            spotify_data = json.load(f)
        
        top_artists = [artist['name'] for artist in spotify_data['top_artists']['short_term']]
        
        print(f"🎤 Using your personal top artists: {top_artists[:5]}...")
        return top_artists
        
    except FileNotFoundError:
        print("⚠️  spotify_data.json not found, using fallback artists")
        return ["Drake", "The Weeknd", "JAY-Z", "Eminem", "Tyler, The Creator"]
    except Exception as e:
        print(f"⚠️  Error reading Spotify data: {e}, using fallback artists")
        return ["Drake", "The Weeknd", "JAY-Z", "Eminem", "Tyler, The Creator"]

def get_additional_artists():
    return ["Kendrick Lamar", "Travis Scott", "Future", "Lil Baby", "21 Savage", 
            "Post Malone", "Kanye West", "Lil Wayne", "Cardi B", "Megan Thee Stallion",
            "Doja Cat", "SZA", "Frank Ocean", "A$AP Rocky", "J. Cole"]

def is_relevant_post(title, selftext="", user_artists=None):
    # Filter posts based on user's music taste
    target_artists = (user_artists or []) + get_additional_artists()
    
    text_to_check = (title + " " + selftext).lower()
    
    for artist in target_artists:
        if artist.lower() in text_to_check:
            return True
    
    music_keywords = [
        'new music', 'new album', 'new single', 'drops', 'releases', 
        'mixtape', 'ep', 'leak', 'snippet', 'announces', 'teaser',
        'music video', 'collaboration', 'feature', 'beef', 'diss track'
    ]
    
    for keyword in music_keywords:
        if keyword in text_to_check:
            return True
    
    return False

def fetch_reddit_news():
    user_top_artists = get_top_artists_from_spotify()
    
    creds = get_reddit_credentials()
    
    try:
        reddit = praw.Reddit(
            client_id=creds['client_id'],
            client_secret=creds['client_secret'],
            user_agent=creds['user_agent']
        )
        
        print("🔗 Connected to Reddit successfully!")
        
    except Exception as e:
        print(f"❌ Failed to connect to Reddit: {e}")
        return
    
    subreddit = reddit.subreddit('hiphopheads')
    
    print(f"🎤 Getting news from r/{subreddit.display_name}...")
    print(f"📊 Subreddit has {subreddit.subscribers:,} subscribers")
    
    articles = []
    processed_posts = set()
    
    print("🔥 Fetching hot posts...")
    for post in subreddit.hot(limit=100):
        if post.id not in processed_posts and is_relevant_post(post.title, post.selftext, user_top_artists):
            articles.append(create_article_object(post, "Hot"))
            processed_posts.add(post.id)
    
    print("🆕 Fetching new posts...")
    for post in subreddit.new(limit=100):
        if post.id not in processed_posts and is_relevant_post(post.title, post.selftext, user_top_artists):
            articles.append(create_article_object(post, "New"))
            processed_posts.add(post.id)
    
    print("⭐ Fetching top posts from today...")
    for post in subreddit.top(time_filter='day', limit=50):
        if post.id not in processed_posts and is_relevant_post(post.title, post.selftext, user_top_artists):
            articles.append(create_article_object(post, "Top"))
            processed_posts.add(post.id)
    
    # Sort articles by score and recency
    articles.sort(key=lambda x: (x.get('score', 0) * 0.7 + 
                                (1000 if 'hours ago' in x.get('age', '') else 0)), 
                  reverse=True)
    
    output = {
        "status": "ok",
        "totalResults": len(articles),
        "articles": articles[:50]
    }
    
    try:
        with open('/Users/aryantyagi/rap-news/public/articles/articles.json', 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"✅ Saved {len(articles)} relevant hip-hop articles from Reddit")
        
        print("\n🎵 TOP ARTICLES FOUND:")
        for i, article in enumerate(articles[:10]):
            print(f"{i+1}. {article['title'][:80]}... (Score: {article.get('score', 0)})")
            
    except Exception as e:
        print(f"❌ Error saving file: {e}")

def create_article_object(post, category):
    time_diff = datetime.now() - datetime.fromtimestamp(post.created_utc)
    hours_ago = int(time_diff.total_seconds() / 3600)
    age = f"{hours_ago} hours ago" if hours_ago > 0 else "Just now"
    
    article = {
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
    
    return article

if __name__ == "__main__":
    fetch_reddit_news()