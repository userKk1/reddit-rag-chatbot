import requests

HEADERS = {"User-Agent": "rag-chatbot/0.1"}

def search_reddit(query, limit=5):
    url = "https://www.reddit.com/search.json"
    params = {
        "q": query,
        "sort": "relevance",
        "limit": limit,
        "type": "link"
    }
    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()
    
    posts = []
    for post in data["data"]["children"]:
        p = post["data"]
        posts.append({
            "title": p["title"],
            "url": "https://reddit.com" + p["permalink"],
            "score": p["score"],
            "text": p["selftext"][:500] if p["selftext"] else ""
        })
    
    return posts

def get_comments(permalink, limit=5):
    url = f"https://www.reddit.com{permalink}.json"
    response = requests.get(url, headers=HEADERS)
    data = response.json()

    comments = []
    for comment in data[1]["data"]["children"][:limit]:
        c = comment["data"]
        if c.get("body") and c["body"] != "[deleted]":
            comments.append({
                "author": c.get("author", "unknown"),
                "body": c["body"][:300],
                "score": c.get("score", 0)
            })

    return comments


if __name__ == "__main__":
    results = search_reddit("learn python 2025")
    for post in results:
        print(post["title"])
        print(post["url"])
        comments = get_comments(post['url'].replace("https://reddit.com", ""))
        for c in comments:
            print(f"  u/{c['author']}: {c['body'][:100]}")
        print("---")
        print("---")