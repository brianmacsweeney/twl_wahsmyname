# Wahs My Name? — Claude Code Project
*Powered by This Warriors Life*

## What this is
A Warriors NRL trivia game where fans identify a mystery player from five progressively easier clues. Built for TWL (This Warriors Life) — a NRL Warriors fan publication with a proprietary per-game player ratings system since 2018.

Game file: `game/index.html` — single HTML file, zero dependencies, no build step.
Deploy: drag to GitHub → Cloudflare Pages auto-deploys to kickon.thiswarriorslife.com

---

## Three editions
- **All-Time** (114 players) — full archive 2018–present plus pre-ratings legends
- **2018–2025** (88 players) — modern era, excludes current 2026 squad
- **2026 Season** (24 players) — current squad with fresh round-by-round clues

Edition selector on title screen. Each edition is a separate PLAYERS array in `data/editions.js`.

---

## Clue structure
Each player has exactly 5 clues at difficulty levels 1–5:

| Points | Difficulty | Content |
|--------|-----------|---------|
| 50 | Hardest | Deep trivia — birthplace, family, obscure career fact |
| 40 | Hard | Specific achievement/record/season stat |
| 30 | Medium | Career milestone, rep honour, notable fact |
| 20 | Easy | Position + era + key career context |
| 10 | Easiest | Position + nickname + most famous thing about them |

**Critical rules:**
- NO ratings-only clues ("Will gave X a 7.5/10") — facts about person preferred
- Every clue needs a `source_url` where possible (Substack URL pattern)
- No repeated facts across the 5 clues for the same player
- 2026 Season edition clues must not overlap with All-Time edition clues for same player

---

## Clue writing style (Will Evans voice)
- Dry, fan-to-fan, specific, no clichés
- Stats woven into prose, not listed separately
- Short punchy sentences after longer ones
- Never: "went the extra mile", "stepped up", "gave 110%"
- See `docs/SPORTS_KB_PROMPT_SHORT.md` for full style guide

---

## Key data files
- `data/warriors_who_am_i_v3.json` — master clue database (114 players, all clues, difficulty levels)
- `data/players_enriched.js` — final player array used in the game (flat structure, 5 clues each)
- `data/editions.js` — three edition arrays (all_time, modern, season_2026)
- `data/twl_warriors_kb.txt` — compressed TWL knowledge base (~14K tokens)
- `game/index.html` — the complete game (308KB, self-contained)

---

## Build scripts
- `scripts/build_clues_v2.py` — generates clues from the raw ratings archive (requires `/new_archive/` HTML files)
- `scripts/build_editions.py` — builds three edition arrays from player data + 2026 clues
- `scripts/build_who_am_i_v2.py` — original bulk clue generator
- `scripts/patch_clues.py` — patches missing difficulty levels in existing player data

---

## TWL ratings system
- Will Evans rates every Warriors player /10 per game since 2018
- Scale: 7+ = good, 6–6.9 = solid/mixed, 5–5.9 = below par, under 5 = poor
- 8+ and under 4.5 are reserved for exceptional performances
- POTY (Player of the Year) = accumulated ratings, 3 lowest dropped each season
- Articles published at: thiswarriorslife.substack.com

---

## Common tasks

**Add a new round's 2026 clues:**
1. Read the new ratings article from thiswarriorslife.substack.com
2. Add fresh clues to `CLUES_2026` dict in `scripts/build_editions.py`
3. Ensure no overlap with existing All-Time clues for same player
4. Run `python3 scripts/build_editions.py` to rebuild editions.js
5. Inject new editions.js into game/index.html

**Update a single player's clue:**
1. Open `data/players_enriched.js`
2. Find the player by name
3. Edit the relevant clue text
4. The game reads directly from this file — copy updated PLAYERS array into game/index.html

**Fix a bug in the game:**
- The game is entirely in `game/index.html`
- EDITIONS object is defined near top of the `<script>` block
- State variables: `let PLAYERS = [], deck, roundIdx, score, streak, bestStreak, currentEdition`
- Autocomplete reads from `PLAYERS` live (not a cached array at load time)

**Deploy:**
```
cp game/index.html → rename to index.html → push to GitHub repo
Cloudflare Pages auto-deploys from the repo
```

---

## Player naming notes
- Some players have multiple name variants in the archive (e.g. NICOLL-KLOKSTAD vs NICOL-KLOKSTAD)
- Normalisation dict in build scripts handles known variants
- Aliases in player objects handle nicknames: RTS, CHT, DWZ, SJ, JFH, AKP, AFB

---

## Archive structure
If the raw HTML archive is available (1,417 HTML files from Substack export):
- Location expected at `/new_archive/` relative to project root
- Ratings files identified by filename pattern: `twl-rd-\d+-kingz|warriors-round-\d+-player`
- Year mapped by file ID range (182024xxx = 2025, 190xxxxxx = 2026, etc.)
- URL pattern: `https://thiswarriorslife.substack.com/p/{filename-without-numeric-prefix-and-extension}`
