# TWL WARRIORS NRL KNOWLEDGE BASE — PROCESSING RULES & PROMPT

## PURPOSE
This document enables any Claude instance to take a new export of the This Warriors Life
(thiswarriorslife.com) Substack archive — a ZIP of HTML files — and produce an updated
knowledge base in the established format. Paste the full contents of this file as your
system prompt or initial instruction, then provide the ZIP.

---

## STEP 0 — SETUP

The input is a ZIP file of HTML articles exported from Substack.
Unzip to a working directory. All `.html` files in the archive are articles;
ignore `__MACOSX/` folders entirely.

```bash
unzip Archive.zip -d archive_contents/
```

Expected: 1,000–2,000+ HTML files. Total raw HTML will be 20–30 MB.
Output target: a single `.txt` file, ideally 400–700 KB.

---

## STEP 1 — HTML TEXT EXTRACTION

Use Python's built-in `html.parser`. Strip all content inside:
`script`, `style`, `nav`, `footer`, `noscript`, `iframe` tags.

After extraction, remove lines matching any of these patterns (case-insensitive):
```
subscribe | patreon | youtube | spotify | facebook | twitter
kingz container | appeared first on | https:// | brought to you
frank podcast | big league mag | book chapter menu
get your exclusive | follow this warriors life | support this warriors life
please visit the gofundme | for all your container | hit the work with us
```

Also strip: Twitter/X embed lines (lines containing `@username` followed by `#NRL`),
and lines shorter than 5 characters.

**Do not use the HTML `<title>` tag for article titles** — it is blank in these Substack
exports. Derive the title from the filename slug instead:
```python
slug = re.sub(r'^\d+\.', '', basename).replace('.html','')
title = slug.replace('-', ' ').title()
```

---

## STEP 2 — ARTICLE CATEGORISATION

Categorise every file by matching its filename (lowercase) against these rules, in order:

| Category | Filename contains |
|---|---|
| `ratings` | `player-rating`, `kingz-container-crew-warriors-player`, `warriors-round-N-player`, `warriors-player.html`, `warriors-player-0` |
| `poty` | `player-of-the-year`, `poty`, `leaderboard` |
| `season_history` | `new-zealand-warriors-YYYY`, `warriors-YYYY.html`, `auckland-warriors-YYYY`, `in-focus-warriors-` |
| `in_focus` | `in-focus-warriors-` (subset of season_history, treat as priority) |
| `rivalry` | `the-rivalry-warriors-v-` |
| `top_list` | `twl-top-10-`, `top-10-`, `twl-top-`, `warriors-top-30-` |
| `once_were` | `once-were-warriors-` |
| `profile` | `shaun-johnsons-top-`, `twl-top-10-rtss-` |
| `captains` | `captains`, `a-short-history-of-warriors-captains` |
| `history` | `a-short-history-of-`, `short-history` |
| `preview` | `preview` |
| `stats` | `stats`, `spirit-running`, `numbers-game` |
| `match_wrap` | `wrap`, `recap`, `grandstand`, `hoodoo-busting` |
| `roster` | `signing`, `recruit`, `transfer`, `contract`, `released`, `named`, `retained` |
| `editorial` | everything else (excluding podcasts) |
| `podcast` | `podcast`, `friday-beers`, `ep-N`, `twl-202X-ep`, `-ep-` |

**Podcasts are low-value** for the knowledge base (episode descriptions only, no factual
content). Include only a minimal episode list, not full text.

---

## STEP 3 — CONTENT PRIORITY TIERS

Process articles in this priority order. Higher tiers get more space in the output.

### TIER 1 — MUST INCLUDE IN FULL (these are the gold)
These article types contain dense, unique, structured facts not found elsewhere:

- `in-focus-warriors-*` articles (position-by-position records, award histories, family
  connections, discipline records, crowd/venue stats, rivalries overview, best-and-worst)
- `the-rivalry-warriors-v-*` articles (head-to-head records, key stats per rivalry)
- `a-short-history-of-*` articles (captains, Kiwis, State of Origin, field goals)
- `twl-top-10-*` and `warriors-top-30-*` listicles
- `once-were-warriors-*` player profiles
- POTY award articles (every year available)
- Season history book chapters (`new-zealand-warriors-YYYY`, `auckland-warriors-YYYY`,
  `warriors-YYYY.html`)
- `2026-selection-table-*` articles (most recent pre-season analysis)
- `in-focus-warriors-rookies`, `in-focus-warriors-award-winners`, etc.

### TIER 2 — INCLUDE WITH MODERATE COMPRESSION
- Match wraps for finals matches
- `numbers-game-warriors-*` stats reviews
- `twl-2020-warriors-season-by-the-numbers` style annual stats summaries
- `this-warriors-lifes-YYYY-awards` end-of-season award articles
- `10-hoodoos-*`, `2020-vision-*`, `generation-next-*` editorial analyses
- Flashback/anniversary articles about historically significant matches

### TIER 3 — INCLUDE LIGHTLY (key facts only, 1–3 sentences)
- Regular season match wraps (extract result, scorers, key ratings only)
- Signing/roster news (extract: player name, from/to club, contract length)
- Team selection articles (skip unless announcing a debut or milestone)

### TIER 4 — SKIP
- Podcast episode descriptions (keep a bare episode list only)
- `friday-beers-*` articles (low factual content)
- Pure news wires/media watch without Warriors-specific data
- Duplicate articles (if same content appears in multiple files, use the most complete)

---

## STEP 4 — COMPRESSION RULES

These rules apply to all text before writing to the knowledge base:

**Remove:**
- Filler adverbs: *somewhat, undeniably, unquestionably, clearly, obviously, genuinely,
  inevitably, admittedly*
- Opener phrases: *"It's worth noting that", "It's fair to say that", "It's safe to say",
  "There was a sense that"*
- Social media embeds: lines matching `@username` + `#NRL` pattern
- Redundant attribution: don't repeat the article source in every paragraph

**Preserve verbatim (never compress):**
- Numbered/ranked lists (leaderboards, records, career stats)
- Direct quotes — keep the full quote AND the attribution
- Scores, dates, jersey numbers, try tallies
- Win/loss records and percentages
- Any sentence containing a superlative claim (first, most, only, record, never)

**Depth by era (recency weighting):**
- 2023–present: full depth, include all available detail
- 2018–2022: moderate depth, include key narrative + all stats
- 2011–2017: lighter, focus on records, awards, milestones
- Pre-2011: summary level only, keep facts/figures, compress narrative

---

## STEP 5 — DOCUMENT STRUCTURE

Write the output in this section order. Use `## SECTION NAME` headers throughout
so the file is easily parsed by regex or grep.

```
# TWL WARRIORS NRL KNOWLEDGE BASE
# [metadata line: source, date generated, ratings author note]
================================================================================

## CLUB OVERVIEW & RECORDS
## COACHES
## CAPTAINS – FULL HISTORY
## ALL-TIME APPEARANCES & IRONMEN
## TRYSCORING RECORDS
## POINTSCORING RECORDS
## GOALKICKING RECORDS
## FIELD GOALS
## POSITION-BY-POSITION: FULLBACKS
## POSITION-BY-POSITION: WINGERS & CENTRES
## POSITION-BY-POSITION: HALVES
## POSITION-BY-POSITION: PROPS
## POSITION-BY-POSITION: HOOKERS
## POSITION-BY-POSITION: BACK-ROWERS & LOCKS
## UTILITY PLAYERS
## ROOKIE SEASONS & YOUNG PLAYERS
## AWARD WINNERS – ALL ERAS
## TWL KINGZ CONTAINER CREW PLAYER OF THE YEAR – BY SEASON
## KIWIS INTERNATIONALS
## STATE OF ORIGIN HISTORY
## REP PLAYERS
## FAMILY CONNECTIONS
## RUGBY UNION CONVERTS
## DISCIPLINE RECORDS
## RIVALRIES – HEAD-TO-HEAD RECORDS
## BEST & WORST RESULTS RECORDS
## CROWDS & VENUES
## TOP-30 TRIES OF ALL TIME
## 25 GREATEST GAMES
## GREATEST MONTHS / COMEBACKS / TURNAROUNDS
## ONE-GAME WONDERS & IRONMEN LISTS
## PLAYER PROFILES (Once Were Warriors series + special features)
## SEASON SUMMARIES (1995–[current-3 years], compressed)
## [CURRENT YEAR -2] SEASON – DETAILED
## [CURRENT YEAR -1] SEASON – DETAILED
## [CURRENT YEAR] SEASON – DETAILED
## [NEXT YEAR] SQUAD – PRE-SEASON ANALYSIS (if available)
## NOTABLE QUOTES COLLECTION
## ANDREW WEBSTER ERA NOTES (or current coach)
```

**If a section has no source articles**, write `[No source articles found]` and continue.

**If NEW section types appear** in the new archive that don't fit existing headers
(e.g. a new "in-focus" series covering a topic not previously covered),
add them after the relevant existing section with a `##` header.

---

## STEP 6 — RATINGS ARTICLES (special handling)

Player ratings articles (`twl-rdN-*`, `kingz-container-crew-warriors-player-*`) are
numerous (~25 per season) and verbose. They are valuable for:
- Per-game individual player ratings (the number at the end of each player's entry)
- Standout individual performances
- Brief match context (score, key moments)

**Do NOT include full ratings articles in the knowledge base.**
Instead, for each ratings article, extract only:

1. Match result line (who won, score, round/year)
2. Any player who scored 8.5 or higher (name + rating + one-line reason)
3. Any player who scored 5.0 or lower (name + rating + one-line reason)
4. Season POTY leaderboard if included at article end

Format:
```
RATINGS Rd N YYYY: [Opponent] [Score W/L]. 
  HIGH: [Player] [Rating] – [reason in <10 words]
  LOW: [Player] [Rating] – [reason in <10 words]
```

Group all ratings for a season under `### YYYY PLAYER RATINGS HIGHLIGHTS`.

---

## STEP 7 — DETECTING NEW ARTICLE TYPES

When processing a new archive, scan filenames you haven't seen before.
Look for patterns indicating new standing series:

- New `in-focus-warriors-[topic]` articles → add as new position/topic section
- New `the-rivalry-warriors-v-[club]` → add to rivalries section (new expansion clubs)
- New `2026-selection-table-[position]` → add to pre-season squad section
- New season history chapters (e.g. `warriors-2021.html`) → add to season summaries
- New `once-were-warriors-[player]` profiles → add to player profiles section

Check if any new articles are **updates** to existing standing articles
(e.g. a new captains history article). If so, **replace** the old content, don't append.

---

## STEP 8 — FINDING THE POTY ARTICLES

POTY articles follow these filename patterns (check all):
```
*player-of-the-year-award*
*twl-kingz-container-crew-player-of-the-year*
*fonua-blake-claims-*-twl-*
*erin-clark-takes-out-*
*tohu-shades-roger-*
*rts-claims-back-to-back-*
*jazz-tevaga-takes-out-*
*shaun-johnson-snares-*
```

For each POTY article, extract and preserve in full:
- Winner name and total points
- Full leaderboard (all players listed, points)
- Full average score table (all players listed, minimum 5 games)
- Any note about the Simon Mannering Medal winner vs TWL POTY divergence
- Any quote about the season

---

## STEP 9 — QUOTES EXTRACTION

As you process Tier 1 and Tier 2 articles, maintain a running list of
**quotable passages**. A quote is worth preserving if it:

- Comes from a named player, coach, or official (not anonymous)
- Reveals character, philosophy, or a unique perspective on a specific event
- Contains a memorable or surprising claim
- Concerns a pivotal moment in club history

At the end of the document, write these to `## NOTABLE QUOTES COLLECTION`.
Format: `"[Quote text]" – [Attribution], [context if needed].`

Do not include: generic praise quotes, media hot-takes, promotional copy.

---

## STEP 10 — OUTPUT FILE

Save as `twl_warriors_knowledge_base_YYYY.txt` where YYYY is the current year.
Target size: 400–700 KB. If significantly over 700 KB, apply further compression
to Season Summaries (pre-2015 especially) and Editorial sections.

The file should be parseable by any AI model with no special formatting knowledge.
Avoid markdown tables (use plain aligned text instead). Use `##` headers throughout.
Leaderboards and records should use consistent `NNN – Player Name` format.

---

## WHAT NOT TO DO

- Do not include full match wrap prose — extract result + 2–3 facts maximum
- Do not transcribe podcast episode content — they contain almost no facts
- Do not include URLs, social media handles, or promotional copy
- Do not include duplicate information (if a stat appears in an in-focus article
  AND a season history article, include it once in the in-focus section)
- Do not write narrative summaries of articles — distil to facts, stats, quotes only
- Do not use bullet points for records/leaderboards — use the `NNN – Name` format

---

## WORKED EXAMPLE — POTY ARTICLE

**Input (raw extracted text, ~400 words):**
> Erin Clark has capped a stellar return to the club by earning the TWL Kingz Container Crew
> Player of the Year award – based on our weekly KCC-sponsored player ratings – in convincing style.
> Fashioned on now-defunct Rugby League Week's system of giving every player a rating out of 10
> for every game – which Will Evans has been dishing out for each Warriors game since the start of
> 2018 – the TWL POTY gong goes to Warriors player with the most accumulated points at the end of
> the season (including finals matches). To give players that miss a few games with injury an
> opportunity to still vie for the honour, we've eliminated every player's three lowest scores at
> the end of year (including matches missed). Here's how the leaderboard finished up.
> 165 – Erin Clark
> 149 – Chanel Harris-Tavita
> [...]

**Output in knowledge base:**
```
### TWL POTY 2025
WINNER: Erin Clark (165 pts, avg 7.28/10)
NOTE: Clark won TWL POTY; Roger Tuivasa-Sheck won official Simon Mannering Medal.
Durability note: Clark, CHT, Halasima missed just 1 game between them all season.
RTS hindered by 6-game injury absence in cumulative standings.

FULL LEADERBOARD:
165 – Erin Clark
149 – Chanel Harris-Tavita
148.5 – Leka Halasima
144 – Charnze Nicoll-Klokstad
141.5 – Demetric Vaimauga
141.5 – Adam Pompey
140.5 – Jackson Ford
139 – Marata Niukore
137 – Kurt Capewell
136.5 – Wayde Egan
132 – Roger Tuivasa-Sheck
125.5 – James Fisher-Harris

HIGHEST AVERAGES (min 5 games):
7.33 – Roger Tuivasa-Sheck
7.28 – Erin Clark
6.86 – Taine Tuaupiki
6.83 – Wayde Egan
6.77 – Mitch Barnett
6.69 – Jackson Ford
```

---

## WORKED EXAMPLE — RIVALRY ARTICLE

**Input:** Full rivalry article (~2,000 words with narrative history)

**Output in knowledge base:**
```
### v BRONCOS
Overall: Played 47 – Brisbane 26 wins, Warriors 20 wins, 1 draw.
Brisbane 996 pts, Warriors 920 pts.
Biggest wins: Brisbane – 44-6 (QEII Stadium 1995); Warriors – 56-18 (Suncorp 2013).
Longest streaks: Brisbane – 9 (1995–2000); Warriors – 4 (2002–03).
Finals: 1 played – Brisbane won (2023 prelim final).
Most appearances: Darren Lockyer (Brisbane) 25; Simon Mannering (Warriors) 23.
Most tries: Shaun Berrigan 9; Michael De Vere 9; Francis Meli (Warriors) 7.
Most points: Shaun Johnson (Warriors) 99; Michael De Vere 88; Corey Parker 82.
[2–3 sentence narrative on defining era of rivalry, if space permits]
```

---

## FINAL NOTE ON JUDGMENT

The job is **distillation, not summarisation**. A summary compresses a 500-word article
into 50 words of prose. Distillation converts it into 10 lines of structured facts.

When in doubt: if it's a number, a name, a date, a record, a quote, or a superlative —
keep it. If it's scene-setting, mood, or narrative glue — cut it.

The goal is a file where every line earns its place.
