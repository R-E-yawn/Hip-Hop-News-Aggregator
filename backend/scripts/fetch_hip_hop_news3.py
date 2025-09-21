import praw
import json
from datetime import datetime

def get_reddit_credentials():
    """Your actual Reddit API credentials"""
    return {
        'client_id': 'XckUtGXr_Xr8f3okIzzkqg',
        'client_secret': 'nj3RoTsFR-wOIsT9cJkFotNOjaqzEg',
        'user_agent': 'rap-news-app/1.0 by Ok-Stop-9954'
    }

def get_top_artists():
    """Return hardcoded top 5 artists + additional hip-hop artists for filtering"""
    return ["Drake", "The Weeknd", "JAY-Z", "Eminem", "Tyler, The Creator"]

def get_additional_artists():
    """Additional artists to catch more relevant content"""
    return ["Kendrick Lamar", "Travis Scott", "Future", "Lil Baby", "21 Savage", 
            "Post Malone", "Kanye West", "Lil Wayne", "Cardi B", "Megan Thee Stallion",
            "Doja Cat", "SZA", "Frank Ocean", "A$AP Rocky", "J. Cole"]

def is_relevant_post(title, selftext=""):
    """Check if post is relevant to our target artists or hip-hop news"""
    target_artists = get_top_artists() + get_additional_artists()
    
    text_to_check = (title + " " + selftext).lower()
    
    # Check for artist names
    for artist in target_artists:
        if artist.lower() in text_to_check:
            return True
    
    # Check for music-related keywords
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
    """Fetch hip-hop news from Reddit using PRAW"""
    
    # Get credentials
    creds = get_reddit_credentials()
    
    # Initialize Reddit instance
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
    
    # Get r/hiphopheads subreddit
    subreddit = reddit.subreddit('hiphopheads')
    
    print(f"🎤 Getting news from r/{subreddit.display_name}...")
    print(f"📊 Subreddit has {subreddit.subscribers:,} subscribers")
    
    articles = []
    processed_posts = set()  # Avoid duplicates
    
    # Get hot posts (trending now)
    print("🔥 Fetching hot posts...")
    for post in subreddit.hot(limit=100):
        if post.id not in processed_posts and is_relevant_post(post.title, post.selftext):
            articles.append(create_article_object(post, "Hot"))
            processed_posts.add(post.id)
    
    # Get new posts (latest)
    print("🆕 Fetching new posts...")
    for post in subreddit.new(limit=100):
        if post.id not in processed_posts and is_relevant_post(post.title, post.selftext):
            articles.append(create_article_object(post, "New"))
            processed_posts.add(post.id)
    
    # Get top posts from today
    print("⭐ Fetching top posts from today...")
    for post in subreddit.top(time_filter='day', limit=50):
        if post.id not in processed_posts and is_relevant_post(post.title, post.selftext):
            articles.append(create_article_object(post, "Top"))
            processed_posts.add(post.id)
    
    # Sort by score (popularity) and recency combined
    articles.sort(key=lambda x: (x.get('score', 0) * 0.7 + 
                                (1000 if 'hours ago' in x.get('age', '') else 0)), 
                  reverse=True)
    
    # Create output in News API format
    output = {
        "status": "ok",
        "totalResults": len(articles),
        "articles": articles[:50]  # Limit to top 50
    }
    
    # Save to JSON file
    try:
        with open('/Users/aryantyagi/rap-news/public/articles/articles.json', 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"✅ Saved {len(articles)} relevant hip-hop articles from Reddit")
        
        # Show preview of top articles
        print("\n🎵 TOP ARTICLES FOUND:")
        for i, article in enumerate(articles[:10]):
            print(f"{i+1}. {article['title'][:80]}... (Score: {article.get('score', 0)})")
            
    except Exception as e:
        print(f"❌ Error saving file: {e}")

def create_article_object(post, category):
    """Convert Reddit post to News API format"""
    
    # Calculate how long ago post was made
    time_diff = datetime.now() - datetime.fromtimestamp(post.created_utc)
    hours_ago = int(time_diff.total_seconds() / 3600)
    age = f"{hours_ago} hours ago" if hours_ago > 0 else "Just now"
    
    # Create article object
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