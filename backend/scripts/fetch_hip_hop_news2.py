import requests
import json

def get_top_artists():
    """Return hardcoded top 5 artists"""
    return ["Drake", "The Weeknd", "JAY-Z", "Eminem", "Tyler, The Creator"]

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