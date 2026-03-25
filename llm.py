from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_llm(question, reddit_posts):
    # Build context from reddit posts + comments
    context = ""
    for i, post in enumerate(reddit_posts, 1):
        context += f"\n[Post {i}] {post['title']}\n"
        if post["text"]:
            context += f"{post['text']}\n"
        for c in post.get("comments", []):
            context += f"  - u/{c['author']}: {c['body']}\n"

    prompt = f"""You are a helpful assistant that answers questions based on Reddit discussions.

Here are relevant Reddit posts and comments:
{context}

Based on these posts, answer this question:
{question}

Be conversational, cite specific posts or comments when relevant."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content

def extract_search_query(question):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": f"""Convert this question into a short, specific Reddit search query (3-5 keywords max).
Only return the search query, nothing else.

Question: {question}
Search query:"""
        }],
        temperature=0
    )
    return response.choices[0].message.content.strip()

