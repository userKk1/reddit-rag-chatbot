from reddit_fetcher import search_reddit, get_comments
from llm import ask_llm, extract_search_query

def answer_question(question):
    
    # Step 1: make the query smarter
    query = extract_search_query(question)
    print(f"\n Searching Reddit for: '{query}'")
    print(f"\n Searching Reddit for: '{question}'")
    
    # Step 1: fetch posts
    posts = search_reddit(query, limit=5)
    
    # Step 2: enrich with comments
    for post in posts:
        permalink = post["url"].replace("https://reddit.com", "")
        post["comments"] = get_comments(permalink, limit=5)
    
    print(f" Found {len(posts)} posts with comments")
    
    # Step 3: ask LLM
    print(" Asking LLM...\n")
    answer = ask_llm(question, posts)
    
    return answer, posts
"""
    # Step 4: print answer + sources
    print(" Answer:")
    print(answer)
    print("\n Sources:")
    for post in posts:
        print(f"  - {post['title']}")
        print(f"    {post['url']}")
"""

if __name__ == "__main__":
    question = input("Ask anything: ")
    answer_question(question)