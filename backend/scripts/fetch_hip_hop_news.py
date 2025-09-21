import requests
import json
import re

def get_top_artists():
    """Read top 5 artists from data.js"""
    try:
        with open('/Users/aryantyagi/rap-news/src/data.js', 'r') as f:
            content = f.read()
        
        # Extract artist names from the JS array
        artists = re.findall(r'"([^"]*)"', content)
        return artists[:5]  # Only top 5
    except:
        print("❌ Could not read data.js")
        return []

def fetch_news():
    """Fetch news for top 5 artists"""
    artists = get_top_artists()
    
    if not artists:
        return
    
    print(f"🎤 Getting news for: {', '.join(artists)}")
    
    # Simple query with top 5 artists
    query = f"({' OR '.join(artists)}) AND (new music OR album OR single)"
    
    url = "https://newsapi.org/v2/everything"
    params = {
        'q': query,
        'sortBy': 'publishedAt',
        'language': 'en',
        'pageSize': 50,
        'apiKey': '16e19aeccf1741178b1e20ac86da364f'
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # Save to public/articles/articles.json
        with open('/Users/aryantyagi/rap-news/public/articles/articles.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Saved {len(data.get('articles', []))} articles")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    fetch_news()