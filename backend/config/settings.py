# Your NewsAPI configuration
NEWS_API_KEY = "16e19aeccf1741178b1e20ac86da364f"
BASE_URL = "https://newsapi.org/v2/everything"

# Hip-hop search query
HIP_HOP_QUERY = "(hip hop OR rap OR rapper) AND (new music OR album OR single OR track OR release OR debut OR drops OR announces) -crime -arrest -shooting -murder -death -jail -prison"

# Date range (last month)
from datetime import datetime, timedelta
FROM_DATE = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')