[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/YOUR_USERNAME/YOUR_REPO/blob/main/scraper.ipynb)


# 📊 Instagram Analytics Scraper — @sozal_foods

> A full end-to-end data scraping and NLP analytics pipeline built in Google Colab to extract, process, and visualise Instagram metrics — targeting a viral brownie recipe reel by **@sozal_foods**.

---

## 🗂️ Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Pipeline Walkthrough](#pipeline-walkthrough)
- [Data Scraped](#data-scraped)
- [Errors & Fixes](#errors--fixes)
- [Results & Key Findings](#results--key-findings)
- [Output Files](#output-files)
- [How to Run](#how-to-run)
- [Limitations](#limitations)
- [Disclaimer](#disclaimer)

---

## Overview

This project scrapes and analyses a public Instagram account and a specific viral reel using **Instaloader**, processes 302 user comments through an **NLP pipeline** (TextBlob), detects posting patterns, classifies content pillars, computes virality scores, and exports everything into a structured Excel report and an HTML dashboard.

**Target Account:** [`@sozal_foods`](https://www.instagram.com/sozal_foods/) — Sofia and Urooj, Karachi, Pakistan  
**Target Reel:** [Brownie Recipe Reel](https://www.instagram.com/sozal_foods/reel/DNKo_RTIG4e/) (posted 10 Aug 2025)  
**Scrape Date:** 19 May 2026

---

## Features

- 🔍 **Reel metric scraping** — views, likes, comments, hashtags, caption, and date via Instaloader
- 👤 **Account-level profiling** — followers, following, bio, post count, verification status
- 📊 **Audience authenticity scoring** — follower-to-following ratio + engagement rate calculation
- 💬 **Comment NLP analysis** — sentiment (positive/neutral/negative), spam detection, question detection, complaint detection, keyword frequency
- 📅 **Posting pattern analysis** — best day/hour, average posting gap, posts per week (29 real dates)
- 🏷️ **Content pillar classification** — keyword-based labelling of captions into Recipe/How-to, Product Showcase, Behind the Scenes, Promotion/Deal
- 🚀 **Virality & velocity scoring** — like-to-view ratio and custom virality formula
- 🎨 **HTML dashboard** — dark-themed, inline analytics dashboard rendered in Colab
- 📁 **Excel export** — 8-sheet Excel file (`sozal_foods_FULL_REPORT.xlsx`) covering all dimensions

---

## Tech Stack

| Library | Version | Purpose |
|---|---|---|
| `instaloader` | Latest | Instagram public data scraping |
| `pandas` | — | Data manipulation and export |
| `openpyxl` | — | Excel multi-sheet writer engine |
| `textblob` | 0.19.0 | NLP sentiment analysis |
| `nltk` | 3.9.1 | Tokenisation, POS tagging, corpora |
| `re` | stdlib | Hashtag extraction via regex |
| `collections` | stdlib | Counter and defaultdict for frequency analysis |
| `IPython.display` | — | HTML dashboard rendering in Colab |
| `google.colab.files` | — | File download trigger |

**Environment:** Google Colab (Python 3.12)  
**No Instagram login required** for reel and account scraping.

---

## Project Structure

```
instagram-scraper-sozal-foods/
│
├── scraper.ipynb                         # Main Google Colab notebook (12 cells)
├── sozal_foods_brownie_comments.csv      # Pre-collected comment dataset (302 rows)
├── processed_instagram_comments.csv      # NLP-enriched output (generated)
├── sozal_foods_FULL_REPORT.xlsx          # 8-sheet Excel report (generated)
└── README.md
```

---

## Pipeline Walkthrough

The notebook is split into **12 sequential cells**, each with a single responsibility:

### Cell 1 — Install & Import
Installs `instaloader`, `pandas`, `openpyxl`, `textblob`. Downloads NLTK corpora (`brown`, `punkt_tab`, `wordnet`, `averaged_perceptron_tagger_eng`, `conll2000`, `movie_reviews`).

### Cell 2 — Reel URL Input
Set `REEL_URL` here — the shortcode is auto-extracted from the URL tail.
```python
REEL_URL = "https://www.instagram.com/sozal_foods/reel/DNKo_RTIG4e/"
shortcode = REEL_URL.rstrip("/").split("/")[-1]
# → DNKo_RTIG4e
```

### Cell 3 — Scrape Reel Metrics
Uses `instaloader.Post.from_shortcode()` to fetch the reel object. Extracts views, likes, comments, caption, hashtags (via `re.findall(r'#\w+', caption)`), and date.

### Cell 4 — Account Metrics
Pulls `post.owner_profile` to retrieve account data in one call (no second API request). Includes a 4-second `time.sleep()` to respect rate limits.

### Cell 5 — Audience Authenticity
Calculates two quality signals:
- **F/F Ratio** = `followers / following` — healthy threshold: > 2
- **Engagement Rate** = `(likes + comments) / followers × 100` — good threshold: > 1%

### Cell 6 — Comment NLP Processing
Loads `sozal_foods_brownie_comments.csv`. Runs four detection passes:

| Pass | Method | Output Column |
|---|---|---|
| Sentiment | TextBlob polarity score | `sentiment` |
| Spam | Keyword matching | `spam_detection` |
| Questions | `'?' in text` | `question_detection` |
| Complaints | Keyword matching | `complaint_detection` |

### Cell 7 — Comment Analytics Dashboard (HTML)
Renders a styled HTML dashboard in Colab showing sentiment distribution bar, spam/question/complaint counts, top keywords, and professional insights.

### Cell 8 — Posting Pattern (Final Version)
Uses 29 manually confirmed post dates from @sozal_foods to compute:
- Best posting day and hour
- Average gap between posts
- Posts per week estimate

> **Note:** An earlier dynamic version of this cell failed due to a `NameError` — see [Errors & Fixes](#errors--fixes) below.

### Cell 9 — Content Pillar Detection
Classifies each post caption against four keyword-based pillar categories using `defaultdict` counters.

### Cell 10 — Velocity & Virality
```python
virality_score = (likes + comments * 2) / views * 100
like_to_view   = likes / views * 100
```
Verdicts: **Viral** > 5, **Strong** > 2, **Average** < 2.

### Cell 11 — Full HTML Analytics Report
Renders a premium dark-themed HTML dashboard inside Colab with sections for account overview, reel stats, sentiment analysis, posting timeline, hashtag cloud, and professional insights.

### Cell 12 — Excel Export
Exports all data objects to `sozal_foods_FULL_REPORT.xlsx` with 8 named sheets, then triggers download via `google.colab.files.download()`.

---

## Data Scraped

### Reel Metrics

| Field | Value |
|---|---|
| Reel URL | instagram.com/sozal_foods/reel/DNKo_RTIG4e/ |
| Date Posted | 10 August 2025 |
| Views | 1,143,528 |
| Likes | 44,067 |
| Comments | 335 |
| Hashtag Count | 18 |
| Shares / Saves | N/A (owner-only metrics) |

### Account Metrics

| Field | Value |
|---|---|
| Username | sozal_foods |
| Full Name | Sofia and Urooj |
| Followers | 52,057 |
| Following | 138 |
| Verified | No |
| First Post | 19 December 2024 |
| Last Post | 11 May 2026 |

### Comment Dataset Schema (302 rows)

| Column | Description |
|---|---|
| `Comment_No` | Sequential ID |
| `Username` | Commenter handle |
| `Time_Ago` | Relative post time (e.g. "39 w") |
| `Weeks_Ago` | Numeric weeks ago |
| `Comment_Text` | Raw comment (English / Urdu / Mixed) |
| `Reply_To` | Parent username if reply, else NaN |
| `Is_Creator_Reply` | Boolean — @sozal_foods reply? |
| `Category` | Manual label (e.g. Positive/Appreciation) |
| `Contains_Question` | Yes / No |
| `Has_Emoji` | Yes / No |
| `Language` | English / Mixed/Urdu / Urdu |
| `Comment_Length` | Character count |

---

## Errors & Fixes

### ❌ Error 1 — GraphQL JSON Parse Warning

```
JSON Query to graphql/query: Expecting value: line 1 column 1 (char 0) [retrying; skip with ^C]
```

**Cause:** Instagram's CDN returned an empty body on the first GraphQL request (transient rate-limit soft block).  
**Fix:** Instaloader's built-in retry logic handled it automatically. No code change needed. Appeared in Cells 3 and 4.

---

### ❌ Error 2 — NameError: `owner` is not defined (Cell 8 — First Attempt)

```
⚠️ Outer error: name 'owner' is not defined
✅ Collected 0 posts
```

**Cause:** Cell 8 was run before Cell 4, so the `owner` variable (set by `post.owner_profile`) did not exist in the runtime.  
**Fix:** Redesigned Cell 8 as fully self-contained. Replaced live API post iteration with a hardcoded list of 29 manually confirmed post dates, eliminating the `owner` dependency entirely.

> **Attempts:** 2 — dynamic version failed → replaced with `Cell 8 (FINAL)` using manual dates.

---

### ❌ Error 3 — Instaloader Version Outdated

**Cause:** Installed Instaloader version had a known bug affecting the comment iterator on recent Instagram API changes.  
**Fix:** Added a dedicated upgrade cell before comment processing:

```python
!pip install --upgrade instaloader --quiet
print("✅ Instaloader upgraded")
```

---

### ❌ Error 4 — `post_count` Returns `None`

```
Post Count : None
```

**Cause:** `owner.mediacount` did not populate correctly for this account type in the Instaloader version used — a known field mapping issue in v3.x.  
**Fix:** Post count (141) was confirmed manually from the profile page and hardcoded into `account_data`.

---

## Results & Key Findings

| Metric | Value | Verdict |
|---|---|---|
| Engagement Rate | 85.29% | ✅ Excellent (benchmark: 1–3%) |
| F/F Ratio | 377.2 : 1 | ✅ Healthy (organic growth) |
| Virality Score | 3.91 | ✅ Strong |
| Like-to-View Ratio | 3.85% | ✅ Above average |
| Positive Comments | 15.2% | ✅ Good |
| Negative Comments | 7.3% | ⚠️ Monitor |
| Spam Rate | 0.7% | ✅ Clean |
| Questions | 54 | 💡 Content opportunity |
| Complaints | 16 | ⚠️ Oil quantity concern |
| Best Posting Day | Sunday | — |
| Content Pillar | Recipe / How-to | 100% of posts |
| Top Comment Keywords | recipe, oil, brownies, use, can | — |

**Key insight:** 1.14M views from a 52K account = **22× reach multiplier**. The dominant complaint theme (oil quantity) is a direct content brief for a follow-up reel.

---

## Output Files

| File | Description |
|---|---|
| `processed_instagram_comments.csv` | 302 comments with sentiment, spam, question, and complaint labels |
| `sozal_foods_FULL_REPORT.xlsx` | 8-sheet Excel report covering all metrics |

### Excel Sheets

1. **Account Metrics** — profile data
2. **Reel Metrics** — views, likes, comments, hashtags
3. **Comments + Sentiment** — full NLP-enriched comment table
4. **Audience Authenticity** — F/F ratio and engagement rate
5. **Posting Pattern** — best day/hour, frequency, gap analysis
6. **Content Pillars** — per-post caption classification
7. **Top Keywords** — comment keyword frequency table
8. **Velocity & Virality** — LTV ratio, virality score, verdict

---

## How to Run

1. **Open the notebook** in [Google Colab](https://colab.research.google.com/)

2. **Run Cell 1** to install dependencies

3. **Edit Cell 2** — paste any public Instagram reel URL:
   ```python
   REEL_URL = "https://www.instagram.com/your_target/reel/SHORTCODE/"
   ```

4. **Upload your comment CSV** when Cell 6 runs (must match the schema above), or skip Cell 6–7 if you don't have comment data

5. **Run all cells top to bottom** — Cell 12 will auto-download the Excel report

> ⚠️ Always run cells **in order** (1 → 12). Running Cell 8 before Cell 4 will raise a `NameError`. See [Errors & Fixes](#errors--fixes).

---

## Limitations

- **Shares, Saves, and Reposts** are owner-only metrics — not accessible without account authentication
- **Comment scraping via API** is restricted by Instagram for unauthenticated sessions; comments were pre-collected manually into CSV
- **`post_count`** may return `None` depending on Instaloader version and account type
- **Rate limiting:** Instagram may temporarily block requests — the 4-second sleep in Cell 4 and Instaloader's retry logic mitigate this but do not eliminate it
- **Sentiment accuracy** is limited for Urdu and mixed-language comments since TextBlob is trained on English corpora; Urdu text is often scored as Neutral by default

---

## Disclaimer

This project is built for **educational and research purposes only**. All data scraped belongs to the respective Instagram account owners. No private or authenticated data was accessed. Usage must comply with [Instagram's Terms of Service](https://help.instagram.com/581066165581870) and [Meta's Developer Policies](https://developers.facebook.com/policy/).

---

*Built with Python · Instaloader · TextBlob · Pandas · Google Colab*
