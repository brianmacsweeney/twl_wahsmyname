"""
One-time script: seed a Google Sheet from data/players_enriched.js.

Usage:
    SHEET_ID=<your-sheet-id> python3 scripts/populate_sheet.py

The sheet must already exist and be shared with the service account email
in credentials/service_account.json.
"""
import json, os, re
import gspread
from google.oauth2.service_account import Credentials

def load_config():
    with open('config.json') as f:
        return json.load(f)

CREDS_FILE = 'credentials/service_account.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

HEADERS = [
    'id', 'name', 'era', 'aliases',
    'clue_50_text', 'clue_50_source', 'clue_50_url',
    'clue_40_text', 'clue_40_source', 'clue_40_url',
    'clue_30_text', 'clue_30_source', 'clue_30_url',
    'clue_20_text', 'clue_20_source', 'clue_20_url',
    'clue_10_text', 'clue_10_source', 'clue_10_url',
]


def load_players():
    with open('data/players_enriched.js') as f:
        js = f.read()
    js = js[len('const PLAYERS = '):-2]
    return json.loads(js)


def player_to_row(p):
    row = [
        p.get('id', ''),
        p.get('name', ''),
        p.get('era', ''),
        '|'.join(p.get('aliases', [])),
    ]
    for pts in [50, 40, 30, 20, 10]:
        clue = next((c for c in p['clues'] if c['pts'] == pts), {})
        row += [
            clue.get('text', ''),
            clue.get('source', ''),
            clue.get('url', '') or '',
        ]
    return row


def main():
    sheet_id = os.environ.get('SHEET_ID') or load_config().get('sheet_id') or input('Google Sheet ID: ').strip()

    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    gc = gspread.authorize(creds)
    ws = gc.open_by_key(sheet_id).sheet1

    players = load_players()
    rows = [HEADERS] + [player_to_row(p) for p in players]

    ws.clear()
    ws.update(rows)
    print(f"Done — {len(players)} players written to sheet.")


if __name__ == '__main__':
    main()
