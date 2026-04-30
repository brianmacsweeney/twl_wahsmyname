"""
Pull player clues from Google Sheet and regenerate data/players_enriched.js.
Sheet format: one row per clue (player_id | player_name | era | aliases | level | text | source | url)
player_name/era/aliases only needed on first row per player — blanks inherit from above.

Usage:
    python3 scripts/sheet_to_js.py
"""
import json, os
import gspread
from google.oauth2.service_account import Credentials

CREDS_FILE = 'credentials/service_account.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
OUTPUT = 'data/players_enriched.js'
LEVEL_TO_PTS = {5: 50, 4: 40, 3: 30, 2: 20, 1: 10}


def load_config():
    with open('config.json') as f:
        return json.load(f)


def main():
    sheet_id = os.environ.get('SHEET_ID') or load_config().get('sheet_id') or input('Google Sheet ID: ').strip()

    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    gc = gspread.authorize(creds)
    ws = gc.open_by_key(sheet_id).sheet1

    rows = ws.get_all_values()[1:]  # skip header

    players = {}
    order = []
    last_meta = {}

    for row in rows:
        pid = row[0].strip() if row else ''
        if not pid:
            continue

        name        = row[1].strip() if len(row) > 1 and row[1].strip() else last_meta.get('name', '')
        era         = row[2].strip() if len(row) > 2 and row[2].strip() else last_meta.get('era', '')
        aliases_raw = row[3].strip() if len(row) > 3 and row[3].strip() else last_meta.get('aliases_raw', '')
        level_str   = row[4].strip() if len(row) > 4 else ''
        text        = row[5].strip() if len(row) > 5 else ''
        source      = row[6].strip() if len(row) > 6 else ''
        url         = row[7].strip() if len(row) > 7 else ''

        if not text or not level_str:
            continue

        last_meta = {'name': name, 'era': era, 'aliases_raw': aliases_raw}

        if pid not in players:
            players[pid] = {
                'id': pid,
                'name': name,
                'era': era,
                'aliases': [a.strip() for a in aliases_raw.split('|') if a.strip()],
                'clue_pool': [],
            }
            order.append(pid)

        level = int(level_str)
        players[pid]['clue_pool'].append({
            'level': level,
            'pts': LEVEL_TO_PTS.get(level, level * 10),
            'text': text,
            'source': source,
            'url': url or None,
        })

    # Build backwards-compatible `clues` — first clue per level, hardest first
    for p in players.values():
        seen = {}
        for c in p['clue_pool']:
            seen.setdefault(c['level'], c)
        p['clues'] = [seen[lv] for lv in [5, 4, 3, 2, 1] if lv in seen]

    result = [players[pid] for pid in order]
    js = 'const PLAYERS = ' + json.dumps(result, ensure_ascii=False) + ';\n'
    with open(OUTPUT, 'w') as f:
        f.write(js)

    print(f"Done — {len(result)} players written to {OUTPUT}.")


if __name__ == '__main__':
    main()
