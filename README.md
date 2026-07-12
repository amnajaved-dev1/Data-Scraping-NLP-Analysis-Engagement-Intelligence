<div align="center">

# 🍳 Instagram Data Intelligence — @sozal_foods

**Scraping → NLP Sentiment → LLM Content Classification**

A complete, multi-part Instagram data intelligence pipeline built around food content creator **[@sozal_foods](https://www.instagram.com/sozal_foods/)** — from lightweight metadata scraping, to full Selenium deep-scroll extraction with sentiment analysis, to LLM-powered content classification using audio transcription.

[![Live Report](https://img.shields.io/badge/Live%20Report-view-E3A72E?style=for-the-badge)](https://amnajaved-dev1.github.io/Data-Scraping-NLP-Analysis-Engagement-Intelligence/)
[![Python](https://img.shields.io/badge/Python-3-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-8E75B2?style=flat-square)](https://ai.google.dev/)
[![Whisper](https://img.shields.io/badge/OpenAI-Whisper-412991?style=flat-square&logo=openai&logoColor=white)](https://github.com/openai/whisper)
[![Selenium](https://img.shields.io/badge/Selenium-WebDriver-43B02A?style=flat-square&logo=selenium&logoColor=white)](https://www.selenium.dev/)
[![License](https://img.shields.io/badge/status-research%20project-9B9F8C?style=flat-square)]()

</div>

---

## 📌 Quick Facts

| | |
|---|---|
| 🎯 **Target account** | [@sozal_foods](https://www.instagram.com/sozal_foods/) |
| 👁️ **Top reel** | 1.14M views · 85.29% engagement rate |
| 💬 **Comments analyzed** | 519 total (302 in Part 1, 217 in Part 2) |
| 🧠 **LLM dimensions classified** | 8 content-strategy dimensions via Gemini 2.5 Flash |
| 🎙️ **Audio validation** | 5 reels transcribed with Whisper — captions matched spoken audio almost exactly |

---

## 🗂️ Repository Structure

```
Data-Scraping-NLP-Analysis-Engagement-Intelligence/
├── README.md
├── .gitignore
├── .env.example                      # Template for required API keys (never commit real .env)
│
├── notebooks/
│   ├── part1_data_scraping.ipynb     # Instaloader + TextBlob + Excel export
│   └── part2_nlp_analysis.ipynb      # Selenium scraper + sentiment classifier
│
├── scripts/                          # Part 3 — Python scripts (not notebook-based)
│   ├── auto_processor.py             # Downloads reels + Whisper transcription
│   └── classifier.py                 # Gemini 2.5 Flash reel classifier
│
├── data/
│   ├── raw/
│   │   ├── sozal_foods_brownie_comments.csv
│   │   └── keyword_bank.json
│   └── processed/
│       ├── analyzed_comments_dataset.csv
│       ├── auto_deep_comments_output.csv
│       ├── auto_scroll_account_metrics.csv
│       ├── provided_links_metrics.csv
│       ├── reels_data.csv
│       └── sozal_classified_output.csv
│
├── charts/
│   ├── sentiment_matrix_chart.png
│   └── sozal_analysis_charts.png
│
└── docs/
    └── index.html                    # 📊 Live GitHub Pages report — charts, pipeline overview, error log
```

> ⚠️ **`videos/` and `.env` are intentionally excluded from this repo.** `.env` holds the Gemini API key and must never be committed. `videos/` contains downloaded reel `.mp4` files used only for local transcription and is excluded via `.gitignore` due to size and copyright considerations.

---

## 🧩 Project Parts Overview

### 1️⃣ Instaloader Metadata Scraping & Sentiment
`notebooks/part1_data_scraping.ipynb`

A 12-cell Google Colab notebook that scrapes public Instagram metadata (no login required) and runs baseline NLP sentiment on a pre-exported comment CSV.

| Tool | Purpose |
|---|---|
| `instaloader` | Scrapes public post/account metadata (likes, views, comments, followers, bio) |
| `pandas` | DataFrame structuring, cleaning |
| `openpyxl` | Multi-sheet Excel (`.xlsx`) export engine |
| `textblob` | Polarity-based sentiment scoring (-1.0 to +1.0) |
| `re` | Regex hashtag extraction |
| `collections` | Keyword frequency counting |
| `IPython.display` | In-notebook HTML dashboard rendering |
| `google.colab.files` | Triggers local file download from Colab |

**Key outputs:** Account metrics, viral reel analysis (1.14M views, 85.29% engagement rate), 302-comment sentiment breakdown (Positive/Neutral/Negative + Spam/Question/Complaint detection), posting pattern analysis, content pillar classification, and an 8-sheet Excel report (`sozal_foods_FULL_REPORT.xlsx`).

---

### 2️⃣ Selenium Deep-Scroll Scraper & 3-Tier Sentiment Model
`notebooks/part2_nlp_analysis.ipynb`

Since Instaloader alone can't reliably reach deep comment threads or bypass Instagram's dynamic rendering at scale, Part 2 rebuilds the pipeline using **browser automation** to physically scroll and extract data like a real user session.

| Tool | Purpose |
|---|---|
| `Selenium WebDriver` (Chrome) | Automates a real Chrome session — logs in, scrolls the feed, opens each reel, and extracts rendered data. Required because Instagram uses client-side JS and lazy-loaded content that static scrapers can't see. |
| `pandas` | Compiles scraped rows into clean, flattened CSV matrices (`utf-8-sig` encoding) |
| `json` / `re` | Extracts raw metadata directly from hidden Open-Graph meta tags and `<time>` HTML blocks; strips comma-formatted numbers (e.g. `"12,342"` → `12342`) |
| Custom rules-based sentiment engine | Classifies comments into **Positive / Neutral / Negative** using keyword, slang, and emoji signals |

**Data outputs** (`data/processed/`):
- `auto_scroll_account_metrics.csv` — auto-scrolled profile feed metrics (20 reels)
- `provided_links_metrics.csv` — targeted extraction across 21 specific reel URLs
- `auto_deep_comments_output.csv` — deep comment scrape (217 comments)
- `analyzed_comments_dataset.csv` — final 3-tier sentiment classification

**Result:** 217 comments classified — **67.3% Neutral, 31.3% Positive, 1.4% Negative.**

**Key engineering challenges solved:**
- **Missing timestamps** → pulled directly from hidden Open-Graph/`<time>` tags instead of relative text ("3w ago")
- **Comma-splitting bugs** → stripped commas from numeric fields before writing to CSV
- **Instagram bot-detection blocks** → capped scroll depth to 4 per reel (10–14 comments/reel) to avoid triggering account flags

---

### 3️⃣ LLM-Powered Reel Classifier
`scripts/`

Part 3 moves beyond sentiment into **strategic content classification**, using Google's Gemini LLM to categorize each reel across 8 content-strategy dimensions, cross-validated against human-labeled data, and supplemented with real audio transcription.

| Tool | Purpose |
|---|---|
| **Google Gemini 2.5 Flash API** (`gemini-2.5-flash` via `google-generativeai` / `google.genai`) | Core LLM — classifies each reel across 8 dimensions (Appeal Type, Narrative Style, Transparency Level, CTA Presence, Narrative Transportation, Parasocial Bonding, Perceived Authenticity, Audience Transformation) from caption + engagement data |
| **OpenAI Whisper** (`openai-whisper`, base model) | Speech-to-text transcription of 5 sampled reels (`Reel_01`–`Reel_05`) to validate whether captions represent spoken content accurately |
| **FFmpeg** | Required by Whisper to decode audio streams from `.mp4` video files |
| `yt-dlp` | Attempted automated video downloading (blocked by Instagram; manual download via browser + `snapinsta.app` used as fallback) |
| `python-dotenv` | Loads `GEMINI_API_KEY` securely from a local `.env` file (never committed to GitHub) |
| `matplotlib` | Generates 3-panel analysis charts (Appeal Type distribution, Transparency Level, AI-vs-Human agreement %) |
| `csv` / `json` | I/O for `reels_data.csv`, `keyword_bank.json`, and `sozal_classified_output.csv` |

**Two-layer classification approach:**
1. **Keyword matching** — scores each reel against a custom `keyword_bank.json` across multiple dimensions
2. **Gemini AI classification** — sends caption + engagement metadata as a structured prompt, returns strict JSON labels, validated against human-coded ground truth

**Validation results (AI vs. Human agreement):**

| Dimension | Agreement | Why |
|---|---|---|
| CTA Present | 🟢 73% | Keywords like "vote," "comment" are easy to match |
| Appeal Type | 🟡 40% | Genuine disagreement — AI reads nuance differently than humans |
| Transparency Level | 🔴 13% | Label-format mismatch (human: Good/Low, AI: High/Medium/Low) |
| Narrative Style | 🔴 0% | Label-format mismatch |
| Parasocial Bonding | 🔴 0% | Human data used Yes/No, AI used High/Medium/Low |
| Perceived Authenticity | 🔴 0% | Same label-mismatch issue |

**Key discovery:** Whisper-transcribed audio from all 5 sampled reels matched almost perfectly with the written captions — confirming @sozal_foods writes complete recipes/instructions in captions, making caption-only analysis a reliable proxy for spoken content.

---

## 📊 Live Report

The full pipeline — stat strip, part-by-part breakdown, and live sentiment / agreement charts — is published via GitHub Pages from `docs/index.html`:

**➡️ [View the live report](https://amnajaved-dev1.github.io/Data-Scraping-NLP-Analysis-Engagement-Intelligence/)**

---

## 🔑 API Keys & Environment Setup

Part 3 requires a Gemini API key. Create a `.env` file in your local project root (this file is **git-ignored** and must never be pushed):

```
GEMINI_API_KEY=your_api_key_here
```

A safe placeholder template is provided in `.env.example`:
```
GEMINI_API_KEY=your_key_here
```

Install dependencies before running Part 3 scripts:
```bash
pip install python-dotenv google-generativeai matplotlib openai-whisper ffmpeg-python yt-dlp
winget install FFmpeg   # Windows — required for Whisper audio decoding
```

---

## 🛠️ Full Technology Stack

| Category | Tools |
|---|---|
| **Scraping** | Instaloader, Selenium WebDriver, yt-dlp |
| **LLMs / AI** | Google Gemini 2.5 Flash API, OpenAI Whisper (speech-to-text) |
| **NLP** | TextBlob (polarity sentiment), custom keyword-based rules engine |
| **Data Processing** | pandas, json, re, csv |
| **Export/Reporting** | openpyxl (Excel), matplotlib (charts), IPython.display (HTML dashboards) |
| **Environment/Secrets** | python-dotenv, `.env` |
| **Media Processing** | FFmpeg |
| **Languages/Env** | Python 3, Google Colab, VS Code |

---

## ⚠️ Known Errors & Fixes

| Error | Cause | Fix |
|---|---|---|
| `edges` API error | Instagram restricted GraphQL field | Used `post.owner_profile` instead of `Profile.from_username()` |
| Instaloader `AttributeError` | Outdated library version | `pip install --upgrade instaloader` |
| `get_posts()` blocked after ~10 posts | Instagram rate-limiting | Switched to manually confirmed post-date dataset |
| `KeyError` on comment column | CSV column name mismatch | Explicitly set `comment_column = 'Comment_Text'` |
| `NameError: df_comments` | Inconsistent variable naming | Standardized to `df_comments = df` before Excel export |
| Comma-split spreadsheet columns | Raw numbers like `"12,342"` broke CSV columns | Stripped commas via `.replace(",", "")` before saving |
| Instagram bot-detection blocks | Excessive scroll depth (100+) per reel | Capped scrolling to 4 per reel |
| `Import whisper could not be resolved` | Wrong Python interpreter in VS Code | `python -m pip install openai-whisper ffmpeg-python --user` |
| `WinError 5 Access is denied` | Windows file lock during install | Installed with `--user` flag |
| `No video formats found` (yt-dlp) | Instagram blocks automated video downloads | Manual download via browser + snapinsta.app |
| `WinError 2` in Whisper | Missing FFmpeg | `winget install FFmpeg` |
| Gemini `429` rate limit | Free tier: 5 requests/minute | Added delay + retry logic between requests |

---

## 📌 Credits

**Author:** Amna Javed (Reg. No. 23-BCS-009)
**Instructor:** Dr. Sadaf Arauf
**Target Account:** [@sozal_foods](https://www.instagram.com/sozal_foods/)
