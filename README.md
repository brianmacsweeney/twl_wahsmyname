# Wahs My Name?

A Warriors NRL trivia game by [This Warriors Life](https://thiswarriorslife.substack.com). Identify a mystery player from five progressively easier clues — each clue you need costs you points.

**Play it:** [kickon.thiswarriorslife.com](https://kickon.thiswarriorslife.com)

---

## Three editions

| Edition | Players | Coverage |
|---|---|---|
| All-Time | 114 | 2018–present + legends |
| 2018–2025 | 88 | Modern era |
| 2026 Season | 24 | Current squad |

## Clue scoring

| Points | Difficulty |
|---|---|
| 50 | Hardest — birthplace, family, obscure career fact |
| 40 | Hard — specific achievement or season stat |
| 30 | Medium — career milestone or rep honour |
| 20 | Easy — position + era + key context |
| 10 | Easiest — position + nickname + most famous thing |

---

## Project structure

```
game/index.html       ← the complete game (single file, no dependencies)
data/editions.js      ← three edition arrays
data/players_enriched.js  ← flat player array with 5 clues each
data/warriors_who_am_i_v3.json  ← master clue database
scripts/              ← build scripts for clues and editions
```

## Deploy

Edit `game/index.html`, then:

```bash
cp game/index.html index.html
git add -A && git commit -m "your message" && git push
```

Cloudflare Pages auto-deploys from `main`.

---

*Powered by TWL's per-game player ratings system — every Warriors player rated /10 since 2018.*
