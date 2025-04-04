# 🧠 Snapzel – AI-Powered Company Brochure & Landing Page Generator

**Version:** 0.0.1  
**Status:** Experimental, CLI-based prototype (Web version coming soon 🚀)

---

## ✨ What is Snapzel?

Snapzel is a developer-focused AI-powered tool that:

- Scrapes content from any public website 🌐
- Analyzes it using GPT to generate a **human-readable brochure** 📄
- Converts that brochure into **clean Markdown**
- Transforms the Markdown into a fully styled **HTML landing page** 🖥
- Saves everything locally for viewing or reuse

It's like a one-click assistant for building company overviews, marketing pages, or even startup decks — using nothing but a URL.

---

## 📦 Current Features

- ✅ Intelligent web scraper (using `requests` + `BeautifulSoup`)
- ✅ Markdown brochure generator via GPT (OpenAI API)
- ✅ Styled HTML landing page generator (via AI)
- ✅ Local file output: `brochure.md` and `landing.html`
- ✅ Clean, modular Python architecture
- ✅ Session-based file separation using UUIDs

---

## 🛠 How It Works

1. You provide a website URL.
2. Snapzel scrapes it, analyzes relevant content, and generates a brochure.
3. It then builds a full HTML landing page based on the brochure.
4. All files are saved under `temp/<session_id>/`.

---

## 🧪 Installation

```bash
git clone https://github.com/yourusername/snapzel.git
cd snapzel
pip install -r requirements.txt
Make sure to set your OpenAI API key in a .env file:
OPENAI_API_KEY=your-key-here
python main.py
```

## 🌍 Web Version (Coming Soon)
Snapzel will soon support a lightweight FastAPI-based web UI, allowing you to:

- Input a URL through a browser
- Generate & view the brochure instantly
- Download .md or .html files
- Preview the generated landing page in-browser

## 📘 Roadmap
- Local CLI version
- FastAPI web interface
- Background job processing
- PDF brochure generation
- API access for integrations
- Hosted version (SaaS model?)


## 📝 License
MIT – feel free to fork, remix, and evolve it.

celery --broker=redis://default:beIlJ3BlYJO3TRkbERa6mX8Ge71WOdPI@redis-16959.c74.us-east-1-4.ec2.redns.redis-cloud.com:16959
