"""
Pull player clues from Google Sheet and regenerate data/players_enriched.js.

Usage:
    SHEET_ID=<your-sheet-id> python3 scripts/sheet_to_js.py

Expects columns (row 1 = headers):
    id | name | era | aliases | clue_50_text | clue_50_source | clue_50_url
    | clue_40_text | clue_40_source | clue_40_url | clue_30_text | ...
    | clue_20_text | ... | clue_10_text | clue_10_source | clue_10_url
"""
import json, os
import gspread
from google.oauth2.service_account import Credentials

def load_config():
    with open('config.json') as f:
        return json.load(f)

CREDS_FILE = 'credentials/service_account.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
OUTPUT = 'data/players_enriched.js'


def row_to_player(row):
    def col(i):
        return row[i].strip() if i < len(row) else ''

    aliases = [a.strip() for a in col(3).split('|') if a.strip()]

    clues = []
    for i, pts in enumerate([50, 40, 30, 20, 10]):
        base = 4 + i * 3
        text = col(base)
        if text:
            clues.append({
                'pts': pts,
                'text': text,
                'source': col(base + 1),
                'url': col(base + 2) or None,
            })

    return {
        'id': col(0),
        'name': col(1),
        'era': col(2),
        'aliases': aliases,
        'clues': clues,
    }


def main():
    sheet_id = os.environ.get('SHEET_ID') or load_config().get('sheet_id') or input('Google Sheet ID: ').strip()

    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    gc = gspread.authorize(creds)
    ws = gc.open_by_key(sheet_id).sheet1

    rows = ws.get_all_values()
    data_rows = rows[1:]  # skip header row

    players = [row_to_player(r) for r in data_rows if r and r[0].strip()]

    js = 'const PLAYERS = ' + json.dumps(players, indent=2, ensure_ascii=False) + ';\n'
    with open(OUTPUT, 'w') as f:
        f.write(js)

    print(f"Done — {len(players)} players written to {OUTPUT}.")


if __name__ == '__main__':
    main()
