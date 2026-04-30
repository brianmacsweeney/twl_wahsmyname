"""
One-time script: seed the Google Sheet from data/players_enriched.js.
Outputs one row per clue (tall format). Run this when restructuring the sheet.

Usage:
    python3 scripts/populate_sheet.py

Sheet must be shared with the service account in credentials/service_account.json.
Sheet ID is read from config.json.
"""
import json, os
import gspread
from google.oauth2.service_account import Credentials

CREDS_FILE = 'credentials/service_account.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
PTS_TO_LEVEL = {50: 5, 40: 4, 30: 3, 20: 2, 10: 1}

HEADERS = ['player_id', 'player_name', 'era', 'aliases', 'level', 'text', 'source', 'url']


def load_config():
    with open('config.json') as f:
        return json.load(f)


def load_players():
    with open('data/players_enriched.js') as f:
        js = f.read()
    return json.loads(js[len('const PLAYERS = '):-2])


def main():
    sheet_id = os.environ.get('SHEET_ID') or load_config().get('sheet_id') or input('Google Sheet ID: ').strip()

    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    gc = gspread.authorize(creds)
    ws = gc.open_by_key(sheet_id).sheet1

    players = load_players()
    rows = [HEADERS]

    for p in players:
        aliases = '|'.join(p.get('aliases', []))
        sorted_clues = sorted(p['clues'], key=lambda c: -c['pts'])
        for i, clue in enumerate(sorted_clues):
            rows.append([
                p['id'],
                p['name'] if i == 0 else '',
                p.get('era', '') if i == 0 else '',
                aliases if i == 0 else '',
                PTS_TO_LEVEL.get(clue['pts'], clue['pts']),
                clue.get('text', ''),
                clue.get('source', ''),
                clue.get('url', '') or '',
            ])

    ws.clear()
    ws.update(rows)
    print(f"Done — {len(players)} players, {len(rows) - 1} clue rows written to sheet.")


if __name__ == '__main__':
    main()
