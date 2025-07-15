# reddit_persona_generator.py
# A script to scrape a Reddit user's posts and comments, build a persona using Gemini, and save it as TXT, PDF, or HTML with a styled Persona Card.

import os
import re
import argparse
import time
import difflib
import threading
import webbrowser
from datetime import datetime
from dotenv import load_dotenv

import praw
import google.generativeai as genai
from fpdf import FPDF

def load_env():
    load_dotenv()
    required = ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USER_AGENT", "GOOGLE_API_KEY"]
    missing = [var for var in required if not os.getenv(var)]
    if missing:
        raise RuntimeError(f"Missing environment variables: {', '.join(missing)}")
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_reddit_client():
    return praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
    )

def extract_username(url: str) -> str:
    match = re.search(r"reddit.com/user/([A-Za-z0-9_-]+)/?", url)
    if not match:
        raise ValueError(f"Invalid Reddit profile URL: {url}")
    return match.group(1)

def scrape_user_data(reddit, username: str, limit: int = 50):
    user = reddit.redditor(username)
    posts, comments = [], []
    try:
        for submission in user.submissions.new(limit=limit):
            posts.append({
                "title": submission.title,
                "body": submission.selftext[:150],
                "url": f"https://www.reddit.com{submission.permalink}"
            })
    except Exception as e:
        print(f"⚠️ Error fetching posts: {e}")
    try:
        for comment in user.comments.new(limit=limit):
            comments.append({
                "body": comment.body[:150],
                "url": f"https://www.reddit.com{comment.permalink}"
            })
    except Exception as e:
        print(f"⚠️ Error fetching comments: {e}")
    return posts, comments

def build_persona_with_llm(posts: list, comments: list, username: str) -> str:
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

    def format_entry(entry, type_):
        if type_ == "post":
            return f"- Title: {entry['title']}\n  Body: {entry['body']}\n  URL: {entry['url']}"
        else:
            return f"- Comment: {entry['body']}\n  URL: {entry['url']}"

    context = ["### POSTS:"]
    for p in posts[:10]:
        context.append(format_entry(p, "post"))
    context.append("### COMMENTS:")
    for c in comments[:10]:
        context.append(format_entry(c, "comment"))

    if not posts and not comments:
        return "❌ No Reddit posts or comments available to generate persona."

    prompt = (
        f"You are an AI trained to extract structured user personas from Reddit data.\n"
        f"Given the posts and comments below from u/{username}, generate a detailed persona in this format:\n\n"
        f"👤 Reddit User Persona: u/{username}\n"
        f"🎯 Goals and Needs:\n- ... 🔗 Source: <url>\n"
        f"💡 Interests:\n- ... 🔗 Source: <url>\n"
        f"🧠 Personality Traits:\n- ... 🔗 Source: <url>\n"
        f"🔥 Strengths:\n- ...\n"
        f"😤 Frustrations:\n- ... 🔗 Source: <url>\n"
        f"📌 Behavior:\n- ...\n"
        f"Skills:\n- ...\n"
        f"Other Unique Traits:\n- ...\n"
        f"(Include only traits found from the data. Use citations from the URLs provided.)\n\n"
        + "\n".join(context)
    )

    def show_spinner():
        spinner = ["|", "/", "-", "\\"]
        idx = 0
        while not stop_spinner:
            print(f"\r⏳ Generating... {spinner[idx % 4]}", end="")
            idx += 1
            time.sleep(0.2)

    stop_spinner = False
    spinner_thread = threading.Thread(target=show_spinner)
    spinner_thread.start()

    try:
        start_time = time.time()
        response = model.generate_content(prompt)
        duration = time.time() - start_time
        stop_spinner = True
        spinner_thread.join()
        print(f"\n🕒 Gemini response time: {duration:.2f} seconds")
        text = response.text.strip()
        print("\n🔍 Gemini Persona Output:\n" + text[:1000])
        lines = text.splitlines()
        mid = len(lines) // 2
        if difflib.SequenceMatcher(None, lines[:mid], lines[mid:]).ratio() > 0.9:
            return "\n".join(lines[:mid]).strip()
        return text
    except Exception as e:
        stop_spinner = True
        spinner_thread.join()
        return f"❌ Error generating content with Gemini: {e}"

def save_persona(username, persona, output_dir="output", output_format="txt"):
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"u_{username}_persona.{output_format}")

    if output_format == "txt":
        with open(filename, "w", encoding="utf-8") as f:
            f.write(persona)
    elif output_format == "pdf":
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        for line in persona.splitlines():
            pdf.multi_cell(0, 10, line)
        pdf.output(filename)
    elif output_format == "html":
        from html_generator import save_as_html_card
        save_as_html_card(persona, filename)
        webbrowser.open(f"file://{os.path.abspath(filename)}")
    else:
        raise ValueError(f"Unsupported format: {output_format}")

    print(f"✅ Persona saved to: {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a Reddit user persona from a profile URL.")
    parser.add_argument("url", help="Reddit user profile URL")
    parser.add_argument("--output-dir", default="output")
    parser.add_argument("--format", default="html", choices=["txt", "pdf", "html"])
    parser.add_argument("--limit", type=int, default=50, help="Number of posts/comments to fetch")
    args = parser.parse_args()

    load_env()
    reddit = get_reddit_client()
    username = extract_username(args.url)

    print("🔍 Demo: Reddit User Persona Generator")
    print("🎯 Input:")
    print(f"Reddit profile URL:\n{args.url}")
    print(f"\n🧠 Step 1: The script collects data...")

    posts, comments = scrape_user_data(reddit, username, limit=args.limit)

    print(f"\n🔍 Posts scraped: {len(posts)}")
    print(f"🔍 Comments scraped: {len(comments)}")
    for p in posts[:2]:
        print(f"Post: \"{p['title']}\"")
    for c in comments[:3]:
        print(f"Comment: \"{c['body']}\"")

    print("\n🏗️ Step 2: The script analyzes the content...")
    print("It uses a language model (Gemini) to understand the user's interests, tone, and personality.\n")

    persona = build_persona_with_llm(posts, comments, username)

    print("📄 Step 3: Final Output — User Persona")
    save_persona(username, persona, output_dir=args.output_dir, output_format=args.format)
    print(f"✅ Output:\nA file named u_{username}_persona.{args.format} is saved with all this information.")
