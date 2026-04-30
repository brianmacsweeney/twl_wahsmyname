"""
WHO AM I? v2 — Warriors Player Clue Generator
- Source URLs added to every clue
- All clue text rewritten in Will Evans voice/style
- Clues written as quiz questions (You-addressed, dry, specific, no clichés)
"""
import os, glob, re, json
from html.parser import HTMLParser
from collections import defaultdict

SKIP_WORDS = ['subscribe','patreon','https://','appeared first on','brought to you',
              'frank podcast','book chapter','kingz container award']
BASE_URL = "https://thiswarriorslife.substack.com/p/"

def slug_to_url(filename):
    """Convert filename to Substack URL"""
    slug = re.sub(r'^\d+\.', '', os.path.basename(filename)).replace('.html','')
    return BASE_URL + slug

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []; self.skip = False
        self.skip_tags = {'script','style','nav','footer','noscript'}
    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags: self.skip = True
    def handle_endtag(self, tag):
        if tag in self.skip_tags: self.skip = False
    def handle_data(self, data):
        if not self.skip:
            d = data.strip()
            if d and len(d) > 2: self.text.append(d)

def get_text(fp):
    if not os.path.exists(fp): return ''
    with open(fp, encoding='utf-8', errors='ignore') as f: html = f.read()
    p = TextExtractor(); p.feed(html)
    return '\n'.join(l.strip() for l in '\n'.join(p.text).split('\n')
                     if l.strip() and len(l.strip()) > 2
                     and not any(x in l.lower() for x in SKIP_WORDS))

def normalise(name):
    name = re.sub(r'\s+', ' ', name).strip()
    fixes = {
        'NICOL-KLOKSTAD': 'NICOLL-KLOKSTAD',
        'ADDIN-FONUA BLAKE': 'ADDIN FONUA-BLAKE',
        'CHANEL HAARIS-TAVITA': 'CHANEL HARRIS-TAVITA',
        'DALLIN WATENE-ZELENZIAK': 'DALLIN WATENE-ZELEZNIAK',
        'DALLIN WATENE-ZELEZIAK': 'DALLIN WATENE-ZELEZNIAK',
        'DALLIN WATENE-ZELENIAK': 'DALLIN WATENE-ZELEZNIAK',
        'MITCHELL BARNETT': 'MITCH BARNETT',
        'SAMUEL HEALEY': 'SAM HEALEY',
        'DEMITIRC VAIMAUGA': 'DEMITRIC VAIMAUGA',
        'DEMETRIC VAIMAUGA': 'DEMITRIC VAIMAUGA',
        'DEMETRIC SIFAKULA': 'DEMITRIC SIFAKULA',
        'DEMETRIC SIFUKULA': 'DEMITRIC SIFAKULA',
        'TAINE TUAUIKI': 'TAINE TUAUPIKI',
        'TAINE TUAPIKI': 'TAINE TUAUPIKI',
        'NATHANIEL ROACHE': 'NATE ROACHE',
        'AGNASTIUS PAASI': 'AGNATIUS PAASI',
        'PATRICK  MOIMOI': 'PATRICK MOIMOI',
        'EDDIE IEREMIA-TOEVA': 'EDDIE IEREMIA-TOEAVA',
    }
    for bad, good in fixes.items():
        if bad in name: name = name.replace(bad, good)
    return name

def get_season_year(fname):
    b = os.path.basename(fname)
    fid = int(b.split('.')[0])
    if fid >= 190000000: return '2026'
    if fid >= 187000000: return 'trial'
    if 182028000 <= fid <= 182029000: return '2018'
    if 182027000 <= fid <= 182028000: return '2019'
    if 182026200 <= fid <= 182027000: return '2020'
    if 182025800 <= fid <= 182026200: return '2021'
    if 182025500 <= fid <= 182025800: return '2022'
    if 182025200 <= fid <= 182025500: return '2023'
    if 182024800 <= fid <= 182025200: return '2024'
    if 182024000 <= fid <= 182024800: return '2025'
    return 'unknown'

def get_round_from_file(fname):
    b = os.path.basename(fname)
    m = re.search(r'(?:rd|round)-?(\d+)', b, re.I)
    if m: return int(m.group(1))
    if 'finals-week-1' in b: return 28
    if 'finals-week-2' in b: return 29
    if 'finals-week-3' in b: return 30
    if 'trial' in b: return 0
    return None

# ── COLLECT ALL RATINGS DATA ──────────────────────────────────────────────────
files = sorted([f for f in glob.glob('/home/claude/new_archive/*.html') if '__MACOSX' not in f])
ratings_files = [f for f in files if re.search(
    r'player-rating|kingz-container-crew-warriors-player|warriors-round-\d+-player|'
    r'warriors-player\.html|warriors-player-0|twl-rd-\d+-kingz|twl-rd-\d+-warriors|rd-\d+-kingz',
    os.path.basename(f).lower())]

player_appearances = defaultdict(list)

for fpath in sorted(ratings_files):
    year = get_season_year(fpath)
    rnd = get_round_from_file(fpath)
    text = get_text(fpath)
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    url = slug_to_url(fpath)
    
    i = 0
    while i < len(lines):
        m = re.match(r'^(\d{1,2})\s+([A-Z][A-Z\s\'\-\.]+):$', lines[i])
        if m:
            jersey = m.group(1)
            name = normalise(m.group(2).strip())
            if len(name) < 4 or len(name) > 45:
                i += 1; continue
            
            prose_lines = []
            rating = None
            i += 1
            while i < len(lines):
                nxt = lines[i]
                if re.match(r'^(\d{1,2})\s+[A-Z][A-Z\s\'\-\.]+:$', nxt): break
                if re.match(r'^\d+(?:\.\d)?$', nxt):
                    try:
                        r = float(nxt)
                        if 1.0 <= r <= 10.0:
                            rating = r; i += 1
                            if not prose_lines: continue
                            else: break
                    except: pass
                prose_lines.append(nxt); i += 1
            
            prose = ' '.join(prose_lines).strip()
            if prose and len(prose) > 20 and year not in ('trial','unknown'):
                player_appearances[name].append({
                    'year': year, 'round': rnd, 'jersey': jersey,
                    'rating': rating, 'prose': prose,
                    'file': os.path.basename(fpath),
                    'url': url
                })
        else:
            i += 1

def extract_stats(prose):
    stats = {}
    run_m = re.search(r'(\d+)\s+runs?\s+for\s+(\d+)\s+metres?', prose, re.I)
    if run_m: stats['runs'] = int(run_m.group(1)); stats['metres'] = int(run_m.group(2))
    tb_m = re.search(r'(\d+)\s+tackle.break', prose, re.I)
    if tb_m: stats['tackle_breaks'] = int(tb_m.group(1))
    pcm_m = re.search(r'(\d+)\s+post.contact\s+metres?', prose, re.I)
    if pcm_m: stats['pcm'] = int(pcm_m.group(1))
    tkl_m = re.search(r'(\d+)\s+tackles?', prose, re.I)
    if tkl_m: stats['tackles'] = int(tkl_m.group(1))
    if re.search(r'hat.trick|three tries', prose, re.I): stats['tries'] = 3
    elif re.search(r'two tries|second try|another try|double', prose, re.I): stats['tries'] = 2
    elif re.search(r'\btry\b', prose, re.I): stats['tries'] = 1
    if re.search(r'try.assist|assisted.*try|set up.*try', prose, re.I): stats['try_assist'] = True
    if re.search(r'field goal', prose, re.I): stats['fg'] = True
    if re.search(r'sin.?bin', prose, re.I): stats['sb'] = True
    goal_m = re.search(r'(\d+)\s+goals?\s+from\s+(\d+)', prose, re.I)
    if goal_m: stats['goals'] = int(goal_m.group(1)); stats['goal_att'] = int(goal_m.group(2))
    return stats

JERSEY_POS = {
    '1': 'fullback', '2': 'right wing', '3': 'right centre', '4': 'left centre',
    '5': 'left wing', '6': 'five-eighth', '7': 'halfback', '8': 'prop', '9': 'hooker',
    '10': 'prop', '11': 'edge back-rower', '12': 'edge back-rower', '13': 'lock',
}

def rd_label(rnd):
    if rnd == 0: return "a pre-season trial"
    if rnd == 28: return "Finals Week 1"
    if rnd == 29: return "Finals Week 2 (semi-final)"
    if rnd == 30: return "Finals Week 3 (preliminary final)"
    return f"Round {rnd}"

# ── STYLE-COMPLIANT CLUE BUILDERS ────────────────────────────────────────────
# Clue text written in Will's voice: dry, specific, no clichés, fan-to-fan tone

def clue_high_rating(app, stats):
    """Level 1: specific high rating with stats context"""
    r = app['rating']
    yr = app['year']
    rl = rd_label(app['round'])
    
    parts = []
    if stats.get('runs') and stats.get('metres'):
        parts.append(f"{stats['runs']} runs for {stats['metres']} metres")
        if stats.get('pcm'): parts.append(f"{stats['pcm']} post-contact")
    if stats.get('tackle_breaks', 0) >= 5: parts.append(f"{stats['tackle_breaks']} tackle-breaks")
    if stats.get('tries', 0) == 3: parts.append("a hat-trick")
    elif stats.get('tries', 0) == 2: parts.append("a double")
    elif stats.get('tries', 0) == 1: parts.append("a try")
    if stats.get('try_assist'): parts.append("a try assist")
    if stats.get('fg'): parts.append("a field goal")
    if stats.get('goals'): parts.append(f"{stats['goals']}/{stats['goal_att']} goals")
    
    stat_str = ", ".join(parts[:3])
    if stat_str:
        return f"Will handed this player {r}/10 in {yr} {rl} — {stat_str}."
    return f"Will handed this player {r}/10 in {yr} {rl}."

def clue_low_rating(app):
    """Level 1: specific low rating"""
    r = app['rating']
    yr = app['year']
    rl = rd_label(app['round'])
    # Vary the phrasing
    if r <= 4.0:
        return f"Will gave this player just {r}/10 in {yr} {rl}. Rough night."
    return f"This player managed only {r}/10 from Will in {yr} {rl}."

def clue_career_avg(name, appearances):
    """Level 1: career average rating"""
    vals = [a['rating'] for a in appearances if a['rating']]
    if not vals: return None
    avg = sum(vals) / len(vals)
    if avg >= 7.5:
        return f"Career TWL rating average of {avg:.2f}/10 across {len(vals)} games — elite by any measure."
    elif avg >= 6.5:
        return f"Solid rather than spectacular: a career TWL average of {avg:.2f}/10 across {len(vals)} rated games."
    else:
        return f"Career TWL average of {avg:.2f}/10 across {len(vals)} games. Make of that what you will."

def clue_season_avg(year, avg, games):
    """Level 2: season average"""
    if avg >= 7.5:
        return f"Will's ratings averaged {avg:.2f}/10 across {games} games in {year} — one of the standout performers that season."
    elif avg >= 7.0:
        return f"Averaged {avg:.2f}/10 in Will's {year} ratings across {games} games."
    else:
        return f"A {avg:.2f}/10 average across {games} games in {year} tells its own story."

def clue_hat_trick(app):
    """Level 2: hat-trick"""
    return f"Ran in three tries in {app['year']} {rd_label(app['round'])}."

def clue_will_quote(app, sentence):
    """Level 2: verbatim Will quote, style-attributed"""
    rl = rd_label(app['round'])
    # Strip the quote cleanly
    sentence = sentence.strip().strip('"').strip("'")
    if len(sentence) < 30 or len(sentence) > 220: return None
    return f'Will on this player in {app["year"]} {rl}: "{sentence}"'

def clue_position(jersey, jersey_count):
    """Level 3: jersey/position"""
    pos = JERSEY_POS.get(jersey, f'No. {jersey}')
    if jersey in ('1','6','7','9'):
        return f"Spine player — spent the majority of their Warriors career at {pos}."
    if jersey in ('8','10'):
        return f"Middle forward. Spent most of their Warriors time in the prop rotation — No. {jersey}."
    if jersey in ('11','12'):
        return f"Edge forward — {pos}. The No. {jersey} jersey was home for most of their Warriors career."
    return f"Wore No. {jersey} ({pos}) for the Warriors."

def clue_debut(app):
    """Level 3: first appearance"""
    rl = rd_label(app['round'])
    return f"First cropped up in Will's ratings in {app['year']} — specifically {rl}."

def clue_try_volume(count):
    """Level 3: try-scoring volume"""
    if count >= 15:
        return f"Scored tries in at least {count} rated appearances — a proper threat out wide."
    return f"Crossed for tries in at least {count} games through their Warriors career."

def clue_games_rated(count):
    """Level 3: longevity"""
    if count >= 40:
        return f"Racked up {count} rated appearances in a Warriors jersey — that's genuine longevity."
    elif count >= 20:
        return f"Notched {count} appearances in Will's ratings, which speaks to consistent selection."
    return f"Made {count} appearances in Will's ratings across their Warriors career."

def clue_seasons_span(years):
    """Level 4: seasons played"""
    if len(years) == 1:
        return f"Was a Warrior for just the {years[0]} season."
    elif len(years) >= 5:
        return f"Put in {len(years)} seasons across {years[0]}–{years[-1]} — part of the furniture."
    return f"Featured across the {', '.join(years)} seasons."

def clue_broad_position(jersey):
    """Level 4: broad position"""
    backs = {'1','2','3','4','5','6','7'}
    forwards = {'8','9','10','11','12','13'}
    bench = {'14','15','16','17'}
    if jersey in backs:
        return "A back. That's your first clue — work from there."
    elif jersey in forwards:
        return "A forward. Narrows it down — a bit."
    return "Predominantly a bench player across their Warriors career."

def clue_recent_rating(app):
    """Level 5: current season rating — fans following along will know"""
    rl = rd_label(app['round'])
    return f"Will gave this player {app['rating']}/10 in {app['year']} {rl}."

# ── KNOWN FACTS LIBRARY (Level 4-5, hand-crafted in Will's voice) ─────────────
KNOWN_FACTS = {
    'DALLIN WATENE-ZELEZNIAK': [
        (5, 'achievement', "Holds the Warriors' single-season tryscoring record — 24 in 2023. Previous record had stood since Francis Meli in 2003.", None),
        (4, 'fact', "A cult hero who's been at the club twice — Penrith sent him across, and he keeps coming back.", None),
    ],
    'SHAUN JOHNSON': [
        (5, 'achievement', "The Warriors' all-time leading points scorer. 1,213 points. Nobody else is close.", None),
        (5, 'achievement', "Won the Dally M Medal in 2018 — the first Warrior ever to claim the NRL's top individual honour.", None),
        (4, 'fact', "Left in 2019, came back in 2022. The circumstances of that first exit were... not great.", None),
        (3, 'stat', "18 career field goals in Warriors colours — a club record. Stacey Jones, the previous holder, managed 14.", None),
    ],
    'ROGER TUIVASA-SHECK': [
        (5, 'achievement', "Won the Dally M Medal in 2018 — a fullback, which tells you everything about how dominant he was.", None),
        (5, 'achievement', "Club captain 2017–21. Left for All Blacks and Blues rugby union, came back in 2024. It's a love story, basically.", None),
        (4, 'fact', "Arguably the club's greatest-ever fullback. Arguments welcomed, just be prepared to lose.", None),
    ],
    'MITCH BARNETT': [
        (5, 'achievement', "First Warrior to debut for NSW State of Origin. That happened in 2024.", None),
        (4, 'fact', "Co-captain alongside James Fisher-Harris from 2025 — before an ACL ended his season early.", None),
    ],
    'JAMES FISHER-HARRIS': [
        (5, 'achievement', "Four premiership rings from Penrith before joining the Warriors in 2025. Four.", None),
        (4, 'fact', "Co-captain with Mitch Barnett. Also captains the Kiwis.", None),
    ],
    'LEKA HALASIMA': [
        (5, 'achievement', "13 tries in 2025. Shortlisted for Dally M Rookie of the Year. Finished the year as a genuine fan favourite.", None),
        (4, 'fact', "Edge back-rower with a nose for the tryline that belies his relative inexperience at NRL level.", None),
    ],
    'LUKE METCALF': [
        (4, 'fact', "His 2025 season — 8 tries and 9 try assists — was cut short by an ACL in Round 15. Timing was brutal.", None),
        (4, 'stat', "Was tracking as a genuine Dally M Medal contender before the knee gave out.", None),
    ],
    'TOHU HARRIS': [
        (5, 'achievement', "Club captain 2022–24. Won the Dally M Lock of the Year in 2023. Medically retired in early 2025 — back injury. One of the most respected Warriors ever.", None),
        (4, 'achievement', "Two-time club POTY (2020, 2021). Named in Dally M Team of Year 2023. Did everything right.", None),
    ],
    'JAZZ TEVAGA': [
        (5, 'achievement', "Won the TWL POTY in 2021 — recognition for years of thankless dummy-half work.", None),
        (4, 'fact', "One of the longest-serving Warriors — a hooker who built his entire NRL career at Mt Smart.", None),
    ],
    'ERIN CLARK': [
        (5, 'achievement', "TWL POTY 2025 winner with 165 points. The official club award went elsewhere — Will's numbers disagreed.", None),
        (4, 'stat', "Averaged 147 metres a game and 34.3 tackles in 2025. Career-best numbers, and it wasn't particularly close.", None),
    ],
    'ADDIN FONUA-BLAKE': [
        (5, 'achievement', "TWL POTY 2024 (170 points). Two-time Dally M Team of the Year. Left after 2024.", None),
        (4, 'fact', "Elite front-rower who gave the Warriors a dimension in the middle they'd not had for years.", None),
    ],
    'TANAH BOYD': [
        (5, 'achievement', "Slotted in as starting halfback in 2026 and scored 18 points in Round 1 — a Warriors season-opener record.", None),
        (4, 'fact', "Stepped up when Luke Metcalf's ACL forced the issue. Made a convincing case for the starting spot.", None),
    ],
    'TAINE TUAUPIKI': [
        (5, 'achievement', "Warriors Club Rookie of the Year in 2023. Filled in at fullback for extended stretches in 2026 — and thrived.", None),
        (4, 'fact', "The kind of player that makes you forget whoever he's replacing — which is the highest compliment.", None),
    ],
    'CHARNZE NICOLL-KLOKSTAD': [
        (4, 'fact', "Arrived from Canberra before the 2023 season. Reliable at the back, though his attacking ceiling divides opinion.", None),
    ],
    'JACKSON FORD': [
        (5, 'achievement', "100th NRL game in Round 3, 2026. Marked the occasion by being one of the best props in the competition.", None),
        (4, 'fact', "Prop. Developed from a handy addition into one of the Warriors' most consistent performers.", None),
    ],
    'WAYDE EGAN': [
        (4, 'fact', "Seven seasons at the Warriors and counting — hooker, workhorse, perennial underseller of his own contribution.", None),
    ],
    'ADAM POMPEY': [
        (4, 'fact', "Six-plus seasons of Warriors bench cover across multiple coaching regimes. The definition of reliable squad depth.", None),
    ],
    'ALOFIANA KHAN-PEREIRA': [
        (5, 'fact', "Came across from the Gold Coast Titans for 2026. Quick. Very quick.", None),
    ],
    'SIMON MANNERING': [
        (5, 'achievement', "301 games — the Warriors' all-time appearance record. The club's POTY award was renamed the Simon Mannering Medal in his honour.", None),
        (4, 'achievement', "Captain for a record six consecutive seasons. Five-time club POTY.", None),
    ],
    'REECE WALSH': [
        (4, 'fact', "Arrived as a teenager and lit up the 2021 season before heading back to Queensland. The one that got away.", None),
        (4, 'stat', "As a Warriors rookie, scored 9 tries and 78 points — the most points ever by a Warriors debutant.", None),
    ],
    'KEN MAUMALO': [
        (4, 'fact', "Hard-running winger whose exit from the club prompted a TWL passage so brutal it became exemplar material: 'Built like Ken Maumalo but plays with the background noise presence of Kenny G.'", None),
    ],
    'ISSAC LUKE': [
        (4, 'fact', "The hooker from the 2018–20 era. You either loved the dummy-half runs or you didn't — there was no in-between.", None),
    ],
    'BLAKE GREEN': [
        (4, 'fact', "Half who formed one of the Warriors' better modern combinations with Shaun Johnson across 2018–20.", None),
    ],
    'DYLAN WALKER': [
        (4, 'fact', "Versatile, dependable across the centre-five-eighth axis. Injuries interrupted what should've been a stellar Warriors tenure.", None),
    ],
    'MARATA NIUKORE': [
        (4, 'fact', "Arrived from Parramatta as part of the 2023 rebuild and settled in as a reliable edge forward.", None),
    ],
    'CHANEL HARRIS-TAVITA': [
        (4, 'fact', "The longest-serving current Warrior as of 2026. CHT to absolutely everyone who follows the club.", None),
    ],
}

POTY_WINNERS = {
    'ERIN CLARK': ('2025', '165 points'),
    'ADDIN FONUA-BLAKE': ('2024', '170 points'),
    'SHAUN JOHNSON': ('2023', '190.5 points'),
    'JAZZ TEVAGA': ('2021', None),
    'TOHU HARRIS': ('2020', None),
    'ROGER TUIVASA-SHECK': ('2018', None),
    'ROGER TUIVASA-SHECK': ('2019', None),
}

# ── MAIN CLUE BUILDER ─────────────────────────────────────────────────────────
def build_clues(name, appearances):
    clues = []
    appearances.sort(key=lambda x: (x['year'], x['round'] or 0))
    years = sorted(set(a['year'] for a in appearances))

    # ── Level 1: Specific game ratings ───────────────────────────────────────
    for app in appearances:
        if not app['rating']: continue
        stats = extract_stats(app['prose'])
        
        if app['rating'] >= 8.5:
            text = clue_high_rating(app, stats)
            clues.append({'difficulty': 1, 'type': 'rating', 'text': text, 'source_url': app['url']})
        
        if app['rating'] <= 4.5:
            text = clue_low_rating(app)
            clues.append({'difficulty': 1, 'type': 'rating', 'text': text, 'source_url': app['url']})

    # Career average
    avg_clue = clue_career_avg(name, appearances)
    if avg_clue:
        clues.append({'difficulty': 1, 'type': 'stat', 'text': avg_clue, 'source_url': None})

    # ── Level 2: Season averages, standout games, Will quotes ────────────────
    for year in years:
        year_apps = [a for a in appearances if a['year'] == year]
        yr_ratings = [a['rating'] for a in year_apps if a['rating']]
        if yr_ratings and len(yr_ratings) >= 3:
            avg = sum(yr_ratings) / len(yr_ratings)
            if avg >= 7.0 or avg <= 5.5:
                text = clue_season_avg(year, avg, len(yr_ratings))
                clues.append({'difficulty': 2, 'type': 'stat', 'text': text, 'source_url': None})

    # Hat-tricks
    for app in appearances:
        if re.search(r'hat.trick|three tries', app['prose'], re.I):
            clues.append({'difficulty': 2, 'type': 'performance',
                         'text': clue_hat_trick(app), 'source_url': app['url']})

    # Will quotes — pick the most vivid sentences
    quote_pool = []
    for app in appearances:
        sentences = re.split(r'[.!?]', app['prose'])
        for s in sentences:
            s = s.strip()
            if (50 <= len(s) <= 200 and
                not any(x in s.lower() for x in ['https','subscribe','twitter']) and
                re.search(r'\b(superb|brilliant|outstanding|electric|devastating|clinical|'
                          r'barnstorming|monstrous|vintage|freakish|ridiculous|sensational|'
                          r'record|milestone|debut|century|100th|first|career.best|'
                          r'worst|disaster|criminal|shocking|atrocious|abysmal|stinker|'
                          r'best|finest|greatest|awful|woeful|catastrophic)\b', s, re.I)):
                quote_pool.append((app, s))

    for app, s in quote_pool[:4]:
        t = clue_will_quote(app, s)
        if t:
            clues.append({'difficulty': 2, 'type': 'quote', 'text': t, 'source_url': app['url']})

    # ── Level 3: Position, debut, try volume, games played ───────────────────
    jerseys = [a['jersey'] for a in appearances]
    primary = max(set(jerseys), key=jerseys.count) if jerseys else None
    if primary:
        clues.append({'difficulty': 3, 'type': 'position',
                     'text': clue_position(primary, jerseys.count(primary)), 'source_url': None})

    if appearances:
        first = appearances[0]
        clues.append({'difficulty': 3, 'type': 'career',
                     'text': clue_debut(first), 'source_url': first['url']})

    total_rated = len([a for a in appearances if a['rating']])
    if total_rated >= 20:
        clues.append({'difficulty': 3, 'type': 'stat',
                     'text': clue_games_rated(total_rated), 'source_url': None})

    try_games = len([a for a in appearances if re.search(r'\btry\b', a['prose'], re.I)])
    if try_games >= 3:
        clues.append({'difficulty': 3, 'type': 'stat',
                     'text': clue_try_volume(try_games), 'source_url': None})

    # Cross-ref extra sources for facts (simplified — use known_facts for most)
    if name in KNOWN_FACTS:
        for diff, typ, text, url in KNOWN_FACTS[name]:
            if diff == 3:
                clues.append({'difficulty': 3, 'type': typ, 'text': text, 'source_url': url})

    # ── Level 4: Seasons span, broad position, known facts ───────────────────
    clues.append({'difficulty': 4, 'type': 'career',
                 'text': clue_seasons_span(years), 'source_url': None})

    if primary:
        clues.append({'difficulty': 4, 'type': 'position',
                     'text': clue_broad_position(primary), 'source_url': None})

    if name in KNOWN_FACTS:
        for diff, typ, text, url in KNOWN_FACTS[name]:
            if diff == 4:
                clues.append({'difficulty': 4, 'type': typ, 'text': text, 'source_url': url})

    # ── Level 5: Famous/obvious facts, current season rating ─────────────────
    # POTY
    if name in POTY_WINNERS:
        yr, pts = POTY_WINNERS[name]
        pts_str = f" ({pts})" if pts else ""
        clues.append({'difficulty': 5, 'type': 'achievement',
                     'text': f"Won the TWL Player of the Year award in {yr}{pts_str}.",
                     'source_url': None})

    # Most recent 2026 rating
    recent = sorted([a for a in appearances if a['year'] == '2026' and a['rating']],
                    key=lambda x: x['round'] or 0)
    if recent:
        latest = recent[-1]
        clues.append({'difficulty': 5, 'type': 'rating',
                     'text': clue_recent_rating(latest), 'source_url': latest['url']})

    # Known facts Level 5
    if name in KNOWN_FACTS:
        for diff, typ, text, url in KNOWN_FACTS[name]:
            if diff == 5:
                clues.append({'difficulty': 5, 'type': typ, 'text': text, 'source_url': url})

    # Dedupe
    seen = set()
    deduped = []
    for c in clues:
        key = c['text'][:80]
        if key not in seen:
            seen.add(key)
            deduped.append(c)

    return sorted(deduped, key=lambda x: x['difficulty'])

# ── BUILD OUTPUT ──────────────────────────────────────────────────────────────
output = []

# Coaches — hand-crafted, with URLs pointing to relevant season articles
COACHES = [
    {
        'name': 'Andrew Webster',
        'type': 'coach',
        'seasons': ['2023', '2024', '2025', '2026'],
        'clues': [
            {'difficulty': 1, 'type': 'fact',
             'text': "The only Warriors head coach to reach finals in each of his first three seasons. Which, given the franchise's history, is either a remarkable achievement or a statistical inevitability — probably both.",
             'source_url': 'https://thiswarriorslife.substack.com/p/twl-rd-1-kingz-container-crew-warriors'},
            {'difficulty': 2, 'type': 'fact',
             'text': "Won two premiership rings at Penrith — 2021 and 2022 — as Ivan Cleary's assistant, before returning to the club he'd previously served in a lesser capacity.",
             'source_url': None},
            {'difficulty': 3, 'type': 'fact',
             'text': "Led the Warriors to a preliminary final in his debut season, 2023. Lost to the Broncos 22-18 in Brisbane. Fifty-two thousand people were there. It stung.",
             'source_url': None},
            {'difficulty': 4, 'type': 'fact',
             'text': "Current Warriors head coach — the one who finally made finals feel normal again.",
             'source_url': None},
            {'difficulty': 5, 'type': 'fact',
             'text': "The Warriors head coach as of 2026. If you need that clue, welcome to rugby league.",
             'source_url': None},
        ]
    },
    {
        'name': 'Stephen Kearney',
        'type': 'coach',
        'seasons': ['2017', '2018', '2019', '2020'],
        'clues': [
            {'difficulty': 1, 'type': 'fact',
             'text': "Sacked during the 2020 COVID season with a 2-8 record — after coaching the club to its first finals appearance in a decade just two years prior. Rugby league is a short-memory business.",
             'source_url': None},
            {'difficulty': 2, 'type': 'achievement',
             'text': "The coach when Roger Tuivasa-Sheck won the Dally M Medal in 2018, and the Warriors ended a ten-year finals drought. That season alone should have bought him more time.",
             'source_url': None},
            {'difficulty': 3, 'type': 'fact',
             'text': "A former Warriors player who later returned as head coach — one of relatively few to make that crossing.",
             'source_url': None},
            {'difficulty': 4, 'type': 'fact',
             'text': "Coached the Warriors from 2017 to 2020. New Zealand representative as a player, later New Zealand coach.",
             'source_url': None},
            {'difficulty': 5, 'type': 'fact',
             'text': "Warriors head coach from 2017 to 2020.",
             'source_url': None},
        ]
    },
    {
        'name': 'Daniel Anderson',
        'type': 'coach',
        'seasons': ['2001', '2002', '2003', '2004'],
        'clues': [
            {'difficulty': 1, 'type': 'achievement',
             'text': "The only Warriors coach to win the Dally M Coach of the Year award (2001). He also took the club to their first two Grand Finals — 2002 and reached the preliminary final in 2003. Nothing else in the archive comes close.",
             'source_url': None},
            {'difficulty': 2, 'type': 'achievement',
             'text': "Under this coach, the Warriors went from 9th in 2000 to minor premiers in 2002 and Grand Finalists against the Roosters. The transformation took one off-season and a clear plan.",
             'source_url': None},
            {'difficulty': 3, 'type': 'fact',
             'text': "Came in relatively unknown and assembled the Stacey Jones–era team that remains the benchmark for Warriors success. Quietly one of the great coaching jobs in NRL history.",
             'source_url': None},
            {'difficulty': 4, 'type': 'fact',
             'text': "Coached the Warriors from 2001 to 2004, including their first and (still) only NRL Grand Final appearance.",
             'source_url': None},
            {'difficulty': 5, 'type': 'fact',
             'text': "The Warriors coach for the 2002 Grand Final, which they lost 30-8 to the Sydney Roosters.",
             'source_url': None},
        ]
    },
    {
        'name': 'Ivan Cleary',
        'type': 'coach',
        'seasons': ['2006', '2007', '2008', '2009', '2010', '2011'],
        'clues': [
            {'difficulty': 1, 'type': 'fact',
             'text': "Before becoming arguably the NRL's most successful modern coach at Penrith, this man spent six seasons at the Warriors — the longest tenure of any Warriors head coach at the time — and took them to the 2011 Grand Final.",
             'source_url': None},
            {'difficulty': 2, 'type': 'achievement',
             'text': "Took the Warriors to four consecutive finals series and a Grand Final in 2011. His son, you may have heard, became a fairly competent halfback.",
             'source_url': None},
            {'difficulty': 3, 'type': 'fact',
             'text': "The father of a household name in NRL. Coached the Warriors through their most sustained finals era before departing.",
             'source_url': None},
            {'difficulty': 4, 'type': 'fact',
             'text': "Led the Warriors from 2006 to 2011. Later won multiple premierships elsewhere.",
             'source_url': None},
            {'difficulty': 5, 'type': 'fact',
             'text': "Warriors head coach 2006–2011, including the 2011 Grand Final loss to Manly.",
             'source_url': None},
        ]
    },
]

for coach in COACHES:
    output.append(coach)

# Players
for name in sorted(player_appearances.keys()):
    appearances = player_appearances[name]
    if len(appearances) < 1: continue
    
    years = sorted(set(a['year'] for a in appearances if a['year'] not in ('trial','unknown')))
    clues = build_clues(name, appearances)
    if len(clues) < 2: continue
    
    ratings_vals = [a['rating'] for a in appearances if a['rating']]
    avg_rating = round(sum(ratings_vals)/len(ratings_vals), 2) if ratings_vals else None
    
    jerseys = [a['jersey'] for a in appearances]
    primary_jersey = max(set(jerseys), key=jerseys.count) if jerseys else None
    
    output.append({
        'name': name.title(),
        'type': 'player',
        'seasons': years,
        'games_rated': len(ratings_vals),
        'average_rating': avg_rating,
        'primary_jersey': primary_jersey,
        'clues': clues
    })

# Write
with open('/home/claude/warriors_who_am_i_v2.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"Entries: {len(output)}")
total_clues = sum(len(x['clues']) for x in output)
print(f"Total clues: {total_clues}")
for d in [1,2,3,4,5]:
    n = sum(sum(1 for c in x['clues'] if c['difficulty']==d) for x in output)
    print(f"  Level {d}: {n}")
from collections import Counter
urls_present = sum(1 for x in output for c in x['clues'] if c.get('source_url'))
urls_none = sum(1 for x in output for c in x['clues'] if not c.get('source_url'))
print(f"\nSource URLs: {urls_present} clues with URL, {urls_none} calculated/historical")
size = os.path.getsize('/home/claude/warriors_who_am_i_v2.json')
print(f"File size: {size/1024:.0f} KB")
