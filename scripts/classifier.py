"""
@sozal_foods Instagram Reel Classifier
=====================================
Part 3 - Post Final Exam
Uses: Gemini Flash 2.5 + Keyword Matching
"""

import csv
import json
import re
import os
import time
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import google.generativeai as genai

# ── LOAD API KEY FROM .env ──────────────────────────────────────
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")
print("Gemini 2.5 Flash ready!\n")

# ── LOAD FILES ──────────────────────────────────────────────────
with open("keyword_bank.json", "r", encoding="utf-8") as f:
    keyword_bank = json.load(f)

reels = []
with open("reels_data.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        reels.append(row)

print(f"Loaded {len(reels)} reels and {len(keyword_bank)} keyword dimensions.\n")


# ══════════════════════════════════════════════════════════════
# LAYER 1 — KEYWORD MATCHING
# ══════════════════════════════════════════════════════════════
def keyword_match(text):
    text_lower = text.lower()
    results = {}
    for dimension, keywords in keyword_bank.items():
        matched = [kw for kw in keywords if kw.lower() in text_lower]
        results[dimension] = {
            "hit_count": len(matched),
            "matched_terms": ", ".join(matched) if matched else "none"
        }
    return results


# ══════════════════════════════════════════════════════════════
# LAYER 2 — GEMINI AI CLASSIFICATION
# ══════════════════════════════════════════════════════════════
def ai_classify(reel):
    prompt = f"""
You are an expert social media content analyst specializing in Pakistani food content creators.

Analyze this Instagram Reel from @sozal_foods (a food content creator from Pakistan):

REEL ID: {reel['reel_id']}
POST DATE: {reel['post_date']}
CAPTION / NOTES: {reel['caption']}
ENGAGEMENT: {reel['likes']} likes | {reel['views']} views | {reel['saves']} saves | {reel['shares']} shares

Note: Content may include English, Urdu, and Roman Urdu mixed together.

Classify across ALL 8 dimensions using ONLY the given labels:

1. Appeal_Type: Instructional / Challenge-frame / Underdog-Hardship / Prosocial / Other
2. Narrative_Style: Results-in-Progress / Ongoing-Journey / Direct-Sell / Storytelling / Other
3. Transparency_Level: High / Medium / Low
   (High = shows prices/costs/suppliers, Medium = shows process but not financials, Low = only visuals)
4. CTA_Present: Yes / No (if Yes, specify what type e.g. vote, comment, like, follow)
5. Narrative_Transportation: High / Medium / Low
   (Does the caption/content pull the viewer into a scene or experience?)
6. Parasocial_Bonding: High / Medium / Low
   (Does the creator speak directly and personally to the viewer?)
7. Perceived_Authenticity: High / Medium / Low
   (Does the content feel genuine and real rather than scripted or promotional?)
8. Audience_Transformation: Literacy / Burnout / Both / None
   (Literacy = teaching skills. Burnout = hustle/grind culture signals)

Respond ONLY in this exact JSON format with no extra text or markdown:
{{
  "Appeal_Type": "...",
  "Narrative_Style": "...",
  "Transparency_Level": "...",
  "CTA_Present": "...",
  "Narrative_Transportation": "...",
  "Parasocial_Bonding": "...",
  "Perceived_Authenticity": "...",
  "Audience_Transformation": "...",
  "Reasoning": "2-3 sentences explaining the key classifications"
}}
"""
    response = model.generate_content(prompt)
    raw = response.text.strip()
    raw = re.sub(r"```json|```", "", raw).strip()
    return json.loads(raw)


# ══════════════════════════════════════════════════════════════
# VALIDATION — Compare AI vs Human Labels
# ══════════════════════════════════════════════════════════════
def normalize(val):
    return str(val).strip().lower()

def compare_labels(human, ai):
    matches = {}
    dimensions = {
        "Appeal_Type":            ("human_appeal_type",        "Appeal_Type"),
        "Narrative_Style":        ("human_narrative_style",    "Narrative_Style"),
        "Transparency_Level":     ("human_transparency",       "Transparency_Level"),
        "CTA_Present":            ("human_cta",                "CTA_Present"),
        "Parasocial_Bonding":     ("human_parasocial_bonding", "Parasocial_Bonding"),
        "Perceived_Authenticity": ("human_authenticity",       "Perceived_Authenticity"),
    }
    for dim, (h_col, a_col) in dimensions.items():
        h_val = normalize(human.get(h_col, ""))
        a_val = normalize(ai.get(a_col, ""))
        match = (h_val in a_val) or (a_val in h_val) or (h_val == a_val)
        matches[dim] = match
    return matches


# ══════════════════════════════════════════════════════════════
# MAIN — Run Classifier
# ══════════════════════════════════════════════════════════════
all_results = []
validation_scores = {
    "Appeal_Type": [], "Narrative_Style": [], "Transparency_Level": [],
    "CTA_Present": [], "Parasocial_Bonding": [], "Perceived_Authenticity": []
}

for reel in reels:
    print(f"Processing {reel['reel_id']} ({reel['post_date']})...")
    combined_text = reel.get('caption', '')

    # Layer 1 - Keywords
    kw = keyword_match(combined_text)

    # Layer 2 - Gemini AI (with retry on rate limit)
    import time
    ai = None
    for attempt in range(5):
        try:
            ai = ai_classify(reel)
            break
        except Exception as e:
            if "429" in str(e):
                # Extract retry delay from error if available
                import re as re2
                delay_match = re2.search(r'retry_delay\s*\{\s*seconds:\s*(\d+)', str(e))
                wait = int(delay_match.group(1)) + 5 if delay_match else 30 + (attempt * 15)
                print(f"  Rate limit hit, waiting {wait} seconds...")
                time.sleep(wait)
            else:
                print(f"  ERROR on {reel['reel_id']}: {e}")
                break
    if ai is None:
        print(f"  SKIPPED {reel['reel_id']} after retries")
        continue

    # Validation
    matches = compare_labels(reel, ai)
    for dim, result in matches.items():
        validation_scores[dim].append(result)

    # Build output row
    row = {
        "reel_id":                    reel["reel_id"],
        "post_date":                  reel["post_date"],
        "likes":                      reel["likes"],
        "views":                      reel["views"],
        "saves":                      reel["saves"],
        "shares":                     reel["shares"],
        "comments":                   reel["comments"],
        # AI Labels
        "AI_Appeal_Type":             ai.get("Appeal_Type", ""),
        "AI_Narrative_Style":         ai.get("Narrative_Style", ""),
        "AI_Transparency_Level":      ai.get("Transparency_Level", ""),
        "AI_CTA_Present":             ai.get("CTA_Present", ""),
        "AI_Narrative_Transportation":ai.get("Narrative_Transportation", ""),
        "AI_Parasocial_Bonding":      ai.get("Parasocial_Bonding", ""),
        "AI_Perceived_Authenticity":  ai.get("Perceived_Authenticity", ""),
        "AI_Audience_Transformation": ai.get("Audience_Transformation", ""),
        "AI_Reasoning":               ai.get("Reasoning", ""),
        # Human Labels
        "Human_Appeal_Type":          reel.get("human_appeal_type", ""),
        "Human_Narrative_Style":      reel.get("human_narrative_style", ""),
        "Human_Transparency":         reel.get("human_transparency", ""),
        "Human_CTA":                  reel.get("human_cta", ""),
        "Human_Parasocial_Bonding":   reel.get("human_parasocial_bonding", ""),
        "Human_Authenticity":         reel.get("human_authenticity", ""),
        # Keyword Evidence
        "KW_Instructional_hits":      kw.get("Appeal_Type_Instructional", {}).get("hit_count", 0),
        "KW_CTA_hits":                kw.get("CTA", {}).get("hit_count", 0),
        "KW_Transparency_hits":       kw.get("Transparency", {}).get("hit_count", 0),
        "KW_Parasocial_hits":         kw.get("Parasocial_Bonding", {}).get("hit_count", 0),
        "KW_Authenticity_hits":       kw.get("Perceived_Authenticity", {}).get("hit_count", 0),
        "KW_matched_terms":           kw.get("CTA", {}).get("matched_terms", ""),
    }
    all_results.append(row)
    print(f"  Appeal={ai.get('Appeal_Type')} | Auth={ai.get('Perceived_Authenticity')} | Match={sum(matches.values())}/6")
    time.sleep(15)  # 15 seconds between reels for gemini-2.5-flash free tier

# ── SAVE CSV ─────────────────────────────────────────────────────
output_file = "sozal_classified_output.csv"
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=all_results[0].keys())
    writer.writeheader()
    writer.writerows(all_results)
print(f"\nSaved: {output_file}")


# ══════════════════════════════════════════════════════════════
# VALIDATION REPORT
# ══════════════════════════════════════════════════════════════
print("\n" + "="*50)
print("VALIDATION REPORT — AI vs Human Labels")
print("="*50)
for dim, scores in validation_scores.items():
    if scores:
        pct = (sum(scores) / len(scores)) * 100
        print(f"  {dim:30s}: {sum(scores)}/{len(scores)} = {pct:.0f}% agreement")


# ══════════════════════════════════════════════════════════════
# VISUALIZATION — 3 Charts
# ══════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle("@sozal_foods Reel Analysis — Gemini AI Classifications", fontsize=14, fontweight='bold')

# Chart 1: Appeal Type distribution
appeal_types = [r["AI_Appeal_Type"] for r in all_results]
labels1 = list(set(appeal_types))
counts1 = [appeal_types.count(l) for l in labels1]
axes[0].bar(labels1, counts1, color="steelblue")
axes[0].set_title("Appeal Type Distribution")
axes[0].set_xlabel("Appeal Type")
axes[0].set_ylabel("Number of Reels")
axes[0].tick_params(axis='x', rotation=20)

# Chart 2: Transparency Level
trans = [r["AI_Transparency_Level"] for r in all_results]
labels2 = ["High", "Medium", "Low"]
counts2 = [trans.count(l) for l in labels2]
axes[1].bar(labels2, counts2, color=["green", "orange", "red"])
axes[1].set_title("Transparency Level")
axes[1].set_xlabel("Level")
axes[1].set_ylabel("Number of Reels")

# Chart 3: Validation % per dimension
dims = list(validation_scores.keys())
pcts = [(sum(v)/len(v))*100 if v else 0 for v in validation_scores.values()]
short_dims = [d.replace("_", "\n") for d in dims]
bars = axes[2].bar(short_dims, pcts, color="purple")
axes[2].set_title("AI vs Human Agreement %")
axes[2].set_xlabel("Dimension")
axes[2].set_ylabel("% Agreement")
axes[2].set_ylim(0, 110)
for bar, pct in zip(bars, pcts):
    axes[2].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                 f'{pct:.0f}%', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig("sozal_analysis_charts.png", dpi=150)
plt.show()
print("Charts saved: sozal_analysis_charts.png")
print("\nDONE! All files created successfully.")