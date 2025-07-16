# 🤖 Reddit User Persona Generator

This project is a command-line tool that scrapes Reddit posts and comments from any public Reddit user profile and builds a detailed **User Persona** using Google's Gemini language model. The persona is saved in `.txt`, `.pdf`, or an editable `.html` format with a visually appealing design.

## ✨ Features

- Scrapes up to 50 posts and 50 comments from a given Reddit profile.
- Sends the content to Gemini (Google Generative AI) to build a structured persona.
- Outputs the result in your preferred format:
  - 📝 Plain Text (.txt)
  - 📄 PDF Document (.pdf)
  - 🌐 HTML Card UI (.html)
- Extracts key fields like:
  - Goals & Needs
  - Interests
  - Personality Traits
  - Behavior, Skills, Frustrations
  - And more...
## Setting up Environment Variables

This script requires Reddit and Google API keys.

1. Create a `.env` file in the project root (you can copy from `.env.example`): 
2. Fill in your actual keys:
```env
REDDIT_CLIENT_ID=your-client-id
REDDIT_CLIENT_SECRET=your-client-secret
REDDIT_USER_AGENT=your-user-agent
GOOGLE_API_KEY=your-google-api-key



## 🛠️ How It Works

1. You provide a Reddit profile URL.
2. The script scrapes public posts and comments using `PRAW`.
3. It sends the text to Gemini via Google Generative AI API.
4. The generated persona is parsed and formatted as an editable HTML profile card.

## 🧪 Example Usage

```bash
python reddit_persona_generator.py https://www.reddit.com/user/GallowBoob --format html
