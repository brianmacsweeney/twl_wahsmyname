# SPORTS KNOWLEDGE BASE — PROCESSING PROMPT

## BEFORE YOU START

Tell Claude: subject (team/sport), source site, current season/year, ratings system if any, target output size, and intended use (trivia, chatbot, etc.).

---

## SETUP

Unzip the archive. Ignore `__MACOSX/` folders and non-`.html` files. Note total file count and size range.

```bash
unzip Archive.zip -d archive_contents/
```

---

## EXTRACTION

Strip tags: `script`, `style`, `nav`, `footer`, `noscript`, `iframe`.

Remove any line containing: `subscribe | patreon | https:// | appeared first on | brought to you | follow us | support us | get your exclusive | please visit`

Also remove: lines under 5 characters, social media embeds (`@username` + hashtag).

**Publication boilerplate:** Scan 10–20 random files, identify recurring promotional phrases specific to this source, add them to the strip list.

**Titles:** Don't use the HTML `<title>` tag — it's often blank. Derive from filename slug:
```python
slug = re.sub(r'^\d+\.', '', basename).replace('.html', '')
title = slug.replace('-', ' ').title()
```

---

## CATEGORISATION

Scan all filenames first to identify this publication's article series patterns. Universal categories and what to look for:

| Category | Filename signals |
|---|---|
| Player ratings | `ratings`, `rd-N-`, `round-N-player` |
| Awards / POTY | `player-of-the-year`, `poty`, `award`, `leaderboard` |
| Season histories | team name + 4-digit year |
| All-time overviews | `in-focus`, `history-of`, `all-time`, `position-by-position` |
| Rivalries | `rivalry`, `v-[opponent]`, `vs-[opponent]` |
| Ranked lists | `top-10`, `top-5`, `greatest`, `best-ever` |
| Player profiles | `profile`, `once-were`, `career-of` |
| Match reports | `wrap`, `recap`, `report`, `review` |
| Stats analysis | `stats`, `numbers`, `by-the-numbers` |
| Squad analysis | `selection-table`, `squad-preview`, `position-battle` |
| Roster news | `signing`, `transfer`, `contract`, `released` |
| Podcasts | `podcast`, `ep-N`, `episode`, `-ep-` |
| Previews | `preview`, `team-lists` |

---

## CONTENT PRIORITY

**TIER 1 — Include in full:**
All-time records and overviews, rivalry head-to-head articles, "history of..." series, ranked lists, player profiles/retrospectives, awards/POTY articles, season history chapters, pre-season squad analysis.

**TIER 2 — Include compressed:**
Finals match reports, end-of-season stats reviews, anniversary features, original analytical editorials.

**TIER 3 — Key facts only (1–3 sentences):**
Regular season match reports (result + top performer), transfer news (player, from/to, contract length).

**TIER 4 — Skip:**
Podcasts, previews, team selection news (unless debut/milestone), duplicate articles, social media roundups.

---

## COMPRESSION RULES

**Remove:** filler adverbs (somewhat, clearly, obviously, genuinely), throat-clearing phrases ("It's worth noting", "It's fair to say", "Needless to say"), repeated source attribution.

**Always preserve verbatim:** leaderboards and ranked lists, direct quotes with attribution, scores/dates/stats, win-loss records, any sentence with a superlative (first, most, only, record, never).

**Recency weighting:**
- Current season → full detail
- Last 2–3 seasons → key narrative + stats
- 4–7 seasons ago → records, awards, milestones only
- 8+ seasons ago → one-line facts only

---

## OUTPUT STRUCTURE

Use `##` headers throughout. Avoid markdown tables — use `NNN – Name` for leaderboards, `LABEL: value` for records, `|` separators for inline multi-stat lines.

```
# [PUBLICATION] — [SUBJECT] KNOWLEDGE BASE
# Source: [URL] | [Ratings system note if applicable] | Generated: [date]
================================================================================

# PART 1: CURRENT SEASON [YEAR]   ← ~90% of file

## CURRENT SEASON — SQUAD & CONTEXT
## CURRENT SEASON — POSITIONAL ANALYSIS
## CURRENT SEASON — RESULTS & RATINGS
## CURRENT SEASON — STATS & STANDINGS

# PART 2: HISTORICAL ARCHIVE   ← ~10% of file

## ALL-TIME RECORDS
## COACHES — HISTORY
## CAPTAINS — HISTORY
## AWARDS — ALL YEARS
## STATISTICAL LEADERS BY POSITION
## HEAD-TO-HEAD RECORDS
## SEASON SUMMARIES
## KEY PLAYER PROFILES
## RANKED LISTS & TRIVIA
## NOTABLE QUOTES
```

**Size targets:**

| Use case | Target |
|---|---|
| Single-prompt trivia | 40–60 KB (~13K tokens) |
| RAG source | 200–400 KB (~75K tokens) |
| Full reference | 400–700 KB (~150K tokens) |

---

## PLAYER RATINGS (if applicable)

Compress each match to: result line + one line per player with jersey, name, rating, and bracketed stats. No prose.

**Stat codes:** `14r/120m` (runs/metres) · `65pcm` (post-contact metres) · `T` `2T` `3T` (tries) · `TA` (try assist) · `6TB` (tackle breaks ≥4) · `42tkl` (tackles ≥35) · `7/8g` (goals) · `FG` (field goal) · `SB` (sin bin) · `HIA` · `err` (error)

Current season: include every round in full.
Previous seasons: include only exceptional (9+) or poor (4.5 or below) performances, plus finals.

```
Rd 7 v Opponent HOME W 28-16
RATINGS:
  6 PLAYER X 8.5 [19r/187m, 4TB, TA]
  9 PLAYER Y 5.5 [8r/67m, err]
```

---

## AWARDS ARTICLES

Search filenames for: `player-of-the-year`, `poty`, `award`, `wins-*-award`, `takes-out-*`, `claims-*`, `[year]-awards`.

Extract: winner + points/votes, full leaderboard, full averages table (if ratings-based), any divergence from official award, one notable quote.

```
POTY 2025 — WINNER: [Player] (165 pts, avg 7.28/10)
LEADERBOARD: 165 – A | 149 – B | 148 – C | 144 – D
AVERAGES: 7.33 – A | 7.28 – B | 6.86 – C
```

---

## QUOTES

Preserve quotes that: come from a named person, reveal character or philosophy, make a surprising claim, or mark a turning point. Discard generic praise and clichés.

Format: `"[Quote]" – [Name], [context], [year].`

---

## FINAL PRINCIPLE

**Distillation, not summarisation.**

A summary compresses 500 words into 50 words of prose.
Distillation converts 500 words into 8 lines of structured facts.

Keep it if it's a number, name, date, record, or quote.
Cut it if it's atmosphere, transition, or narrative glue.

Every line must earn its place.
