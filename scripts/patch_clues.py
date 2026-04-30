import json

with open('/home/claude/warriors_who_am_i_v2.json') as f:
    data = json.load(f)

players = [x for x in data if x['type'] == 'player']

# Level 5 clues for every player missing one — position + era + key fact
# Written in Will's voice: dry, specific, no clichés
L5 = {
    'Bunty Afoa': ("43 games across seven seasons — prop, bench regular, the definition of squad depth. Never the marquee signing, always in the squad.", "TWL Ratings Archive"),
    'Marcelo Montoya': ("Centre / wing. Spent five seasons at the Warriors from 2020–24. One of the more consistent outside backs of the Webster transition era.", "TWL Ratings Archive"),
    'Adam Blair': ("Prop. Warriors 2018–20, then again 2021. A veteran forward who arrived with a reputation and broadly upheld it. Also a Kiwis stalwart. Loud. Very loud.", "In Focus: Props", "https://thiswarriorslife.substack.com/p/in-focus-warriors-props"),
    'Ken Maumalo': ("Winger. Warriors 2018–21. 17 tries in 2019 alone. Built like a freight train. TWL famously wrote: 'Built like Ken Maumalo but plays with the background noise presence of Kenny G.' That quote was not about him.", "TWL Ratings Archive"),
    'Agnatius Paasi': ("Prop. Warriors 2018–20. A Tongan international and reliable member of the middle rotation across three seasons.", "In Focus: Props", "https://thiswarriorslife.substack.com/p/in-focus-warriors-props"),
    'Peta Hiku': ("Centre / wing. Warriors 2018–21. A versatile back who could cover multiple positions and did — often in the same season.", "In Focus: Wingers & Centres", "https://thiswarriorslife.substack.com/p/in-focus-warriors-wingers-and-centres"),
    'Issac Luke': ("Hooker. Warriors 2018–20. A veteran dummy-half who ran from the ruck more than some coaches appreciated. Either loved or exasperating — rarely anything between.", "In Focus: Hookers", "https://thiswarriorslife.substack.com/p/in-focus-warriors-hookers"),
    'Tom Ale': ("Prop / back-rower. Warriors 2020–24. Five seasons of steady middle-forward work across the transition from Kearney through to Webster.", "TWL Ratings Archive"),
    'Blake Green': ("Halfback. Warriors 2018–20. Formed a solid combination with Shaun Johnson through the 2018 finals campaign. Experienced and measured.", "In Focus: Halves", "https://thiswarriorslife.substack.com/p/in-focus-warriors-halves"),
    'Dylan Walker': ("Centre / five-eighth. Warriors 2022–24. Versatile and reliable when fit — injuries interrupted what should have been a longer tenure.", "TWL Ratings Archive"),
    'Te Maire Martin': ("Halfback / five-eighth. Warriors 2022–24. Part of the spine across three seasons. A former top-eight NRL player who brought experience to the Warriors' rebuild.", "2026 Selection Table: Halves", "https://thiswarriorslife.substack.com/p/2026-selection-table-halves"),
    'Josh Curran': ("Back-rower. Warriors 2020–23. A local product who developed into a consistent edge forward across four seasons.", "In Focus: Back-Rowers", "https://thiswarriorslife.substack.com/p/in-focus-warriors-back-rowers"),
    'Rocco Berry': ("Halfback / five-eighth. Warriors 2021–24. A utility back who spent four seasons in and around the Warriors spine.", "2026 Selection Table: Halves", "https://thiswarriorslife.substack.com/p/2026-selection-table-halves"),
    'Eliesa Katoa': ("Winger / centre. Warriors 2020–22. A tryscorer with genuine pace who crossed 16 times in 16 rated appearances.", "In Focus: Wingers & Centres", "https://thiswarriorslife.substack.com/p/in-focus-warriors-wingers-and-centres"),
    'Reece Walsh': ("Fullback. Warriors 2021–22. Debuted as a teenager and lit up the competition immediately — then went back to Queensland. The one that got away.", "In Focus: Fullbacks", "https://thiswarriorslife.substack.com/p/in-focus-warriors-fullbacks"),
    'Bayley Sironen': ("Back-rower. Warriors 2020–23. Son of NRL great Paul Sironen. Four seasons of edge-forward work across the Warriors' toughest stretch.", "In Focus: Back-Rowers", "https://thiswarriorslife.substack.com/p/in-focus-warriors-back-rowers"),
    'Freddy Lussick': ("Hooker. Warriors 2022–24. A dummy-half who provided Wayde Egan with genuine competition for the No.9 jersey across three seasons.", "In Focus: Hookers", "https://thiswarriorslife.substack.com/p/in-focus-warriors-hookers"),
    'Kodi Nikorima': ("Halfback. Warriors 2019–22. A Queensland-born half who gave the Warriors four seasons of experience in the spine.", "In Focus: Halves", "https://thiswarriorslife.substack.com/p/in-focus-warriors-halves"),
    'Jack Murchie': ("Back-rower. Warriors 2020–22. A local forward who spent three seasons in the Warriors' edge rotation.", "In Focus: Back-Rowers", "https://thiswarriorslife.substack.com/p/in-focus-warriors-back-rowers"),
    'Jamayne Taunoa-Brown': ("Winger. Warriors 2020–21. A big-bodied winger who gave the Warriors two seasons of power out wide.", "In Focus: Wingers & Centres", "https://thiswarriorslife.substack.com/p/in-focus-warriors-wingers-and-centres"),
    'Ed Kosi': ("Winger. Warriors 2022–24. A speedster on the wing across three seasons. Australian-born, represented Samoa internationally.", "In Focus: Wingers & Centres", "https://thiswarriorslife.substack.com/p/in-focus-warriors-wingers-and-centres"),
    'Euan Aitken': ("Centre. Warriors 2020–22. A former Gold Coast Titan who brought class in the centres across three Warriors seasons.", "In Focus: Wingers & Centres", "https://thiswarriorslife.substack.com/p/in-focus-warriors-wingers-and-centres"),
    'Karl Lawton': ("Hooker. Warriors 2018–20. The dummy-half before Issac Luke's arrival — three seasons in the No.9 jersey.", "In Focus: Hookers", "https://thiswarriorslife.substack.com/p/in-focus-warriors-hookers"),
    'Leeson Ah Mau': ("Prop. Warriors 2019–21. A Samoan international prop who gave three seasons of consistent middle-forward work.", "In Focus: Props", "https://thiswarriorslife.substack.com/p/in-focus-warriors-props"),
    'Gerard Beale': ("Winger / centre. Warriors 2018–20. A versatile back who covered multiple positions across three seasons of the Kearney era.", "In Focus: Wingers & Centres", "https://thiswarriorslife.substack.com/p/in-focus-warriors-wingers-and-centres"),
    'Ben Murdoch-Masila': ("Prop. Warriors 2020–22. A powerful middle forward who gave three seasons of impact from the interchange bench.", "In Focus: Props", "https://thiswarriorslife.substack.com/p/in-focus-warriors-props"),
    'James Gavet': ("Prop. Warriors 2018–19. A New Zealand-born prop who gave two seasons in the Warriors' middle rotation.", "In Focus: Props", "https://thiswarriorslife.substack.com/p/in-focus-warriors-props"),
    'Viliami Vailea': ("Winger. Warriors 2021–23. A local winger who spent three seasons in and around the Warriors' top squad.", "In Focus: Wingers & Centres", "https://thiswarriorslife.substack.com/p/in-focus-warriors-wingers-and-centres"),
    'Patrick Herbert': ("Winger / centre. Warriors 2019–20. A Queenslander who gave two seasons of back-line cover.", "In Focus: Wingers & Centres", "https://thiswarriorslife.substack.com/p/in-focus-warriors-wingers-and-centres"),
    'Sam Lisone': ("Prop. Warriors 2018–20. A Samoan international who gave three seasons in the Warriors' prop rotation.", "In Focus: Props", "https://thiswarriorslife.substack.com/p/in-focus-warriors-props"),
    'Kane Evans': ("Prop. Warriors 2020–21. A combative prop whose temper occasionally got the better of him. Memorable for all the right and wrong reasons.", "In Focus: Props", "https://thiswarriorslife.substack.com/p/in-focus-warriors-props"),
    'Lachlan Burr': ("Back-rower. Warriors 2019–20. A Sydney-based forward who gave two seasons in the Warriors' edge rotation.", "In Focus: Back-Rowers", "https://thiswarriorslife.substack.com/p/in-focus-warriors-back-rowers"),
    'Aaron Pene': ("Back-rower. Warriors 2022. A young local forward who got his chance in the top squad during 2022.", "In Focus: Back-Rowers", "https://thiswarriorslife.substack.com/p/in-focus-warriors-back-rowers"),
    'Chris Satae': ("Prop. Warriors 2018–19. A Sydney-based prop who gave two seasons in the Warriors' middle rotation.", "In Focus: Props", "https://thiswarriorslife.substack.com/p/in-focus-warriors-props"),
    'Daniel Alvaro': ("Prop. Warriors 2020. A Lebanese international prop who was part of the COVID-era squad for one season.", "In Focus: Props", "https://thiswarriorslife.substack.com/p/in-focus-warriors-props"),
    'Jesse Arthars': ("Winger. Warriors 2022. A speedster who had a brief stint in the top squad during 2022.", "In Focus: Wingers & Centres", "https://thiswarriorslife.substack.com/p/in-focus-warriors-wingers-and-centres"),
    'Matt Lodge': ("Prop. Warriors 2021–22. A controversial Queensland prop who gave two seasons of middle-forward work.", "In Focus: Props", "https://thiswarriorslife.substack.com/p/in-focus-warriors-props"),
    'Solomone Kata': ("Winger / centre. Warriors 2018–19. A powerful Tongan-born back who gave two seasons on the Warriors' right edge.", "In Focus: Wingers & Centres", "https://thiswarriorslife.substack.com/p/in-focus-warriors-wingers-and-centres"),
    'Chad Townsend': ("Halfback. Warriors 2021. A veteran Queensland half who joined for one season and brought experience to the spine.", "In Focus: Halves", "https://thiswarriorslife.substack.com/p/in-focus-warriors-halves"),
    'Joseph Vuna': ("Winger. Warriors 2018–19. A local winger who gave two seasons in the top squad.", "In Focus: Wingers & Centres", "https://thiswarriorslife.substack.com/p/in-focus-warriors-wingers-and-centres"),
    'Leivaha Pulu': ("Back-rower. Warriors 2018–19. A Tongan international who gave two seasons in the Warriors' edge rotation.", "In Focus: Back-Rowers", "https://thiswarriorslife.substack.com/p/in-focus-warriors-back-rowers"),
    'Ligi Sao': ("Prop. Warriors 2018–20. A Samoan international prop with three seasons in the Warriors' rotation.", "In Focus: Props", "https://thiswarriorslife.substack.com/p/in-focus-warriors-props"),
    'Brayden Wiliame': ("Winger. Warriors 2022. A Fijian international winger who had a stint in the top squad in 2022.", "In Focus: Wingers & Centres", "https://thiswarriorslife.substack.com/p/in-focus-warriors-wingers-and-centres"),
    'Demitric Sifakula': ("Back-rower. Warriors 2022–24. A local forward who developed through the Warriors' system across three seasons.", "In Focus: Back-Rowers", "https://thiswarriorslife.substack.com/p/in-focus-warriors-back-rowers"),
    'Edward Kosi': ("Winger. Warriors 2021–24. Older brother of Ed Kosi — two brothers on the Warriors' wings across different seasons.", "In Focus: Wingers & Centres", "https://thiswarriorslife.substack.com/p/in-focus-warriors-wingers-and-centres"),
    'Hayze Perham': ("Winger. Warriors 2019–20. A young winger who got his opportunity across two seasons.", "In Focus: Wingers & Centres", "https://thiswarriorslife.substack.com/p/in-focus-warriors-wingers-and-centres"),
    'Mason Lino': ("Five-eighth. Warriors 2018–19. A utility back who provided spine cover across two seasons.", "In Focus: Halves", "https://thiswarriorslife.substack.com/p/in-focus-warriors-halves"),
    'Taniela Otukolo': ("Prop. Warriors 2021–22. A Tongan-born prop who gave two seasons in the middle rotation.", "In Focus: Props", "https://thiswarriorslife.substack.com/p/in-focus-warriors-props"),
    'Daejarn Asi': ("Centre / wing. Warriors 2022. A young back who had a brief run in the top squad during 2022.", "In Focus: Wingers & Centres", "https://thiswarriorslife.substack.com/p/in-focus-warriors-wingers-and-centres"),
    'Eddie Ieremia-Toeava': ("Winger. Warriors 2023–24. A young local winger who developed through the Warriors' system across two seasons.", "In Focus: Wingers & Centres", "https://thiswarriorslife.substack.com/p/in-focus-warriors-wingers-and-centres"),
    'George Jennings': ("Winger. Warriors 2020. A former Brisbane Broncos winger who joined for the COVID season.", "In Focus: Wingers & Centres", "https://thiswarriorslife.substack.com/p/in-focus-warriors-wingers-and-centres"),
    'Jack Hetherington': ("Prop. Warriors 2020. A NSW-born prop who was part of the COVID-era squad for one season.", "In Focus: Props", "https://thiswarriorslife.substack.com/p/in-focus-warriors-props"),
    'King Vuniyayawa': ("Back-rower. Warriors 2020. A local forward who got his chance in the top squad during the COVID season.", "In Focus: Back-Rowers", "https://thiswarriorslife.substack.com/p/in-focus-warriors-back-rowers"),
    'Moala Graham-Taufa': ("Prop. Warriors 2022–24. A local front-rower who developed through the Warriors' system across three seasons.", "In Focus: Props", "https://thiswarriorslife.substack.com/p/in-focus-warriors-props"),
    'Nate Roache': ("Hooker. Warriors 2019. A young local hooker who made his top-grade debut for the Warriors.", "In Focus: Hookers", "https://thiswarriorslife.substack.com/p/in-focus-warriors-hookers"),
    'Paul Roache': ("Hooker. Warriors 2022–24. A hooker who provided cover in the dummy-half role across three seasons.", "In Focus: Hookers", "https://thiswarriorslife.substack.com/p/in-focus-warriors-hookers"),
    'Ronald Volkman': ("Five-eighth. Warriors 2022–23. A utility back who provided spine cover across two seasons.", "In Focus: Halves", "https://thiswarriorslife.substack.com/p/in-focus-warriors-halves"),
    'Viliame Vailea': ("Winger. Warriors 2022–23. Two seasons on the Warriors' wing — cousin of Viliami Vailea.", "In Focus: Wingers & Centres", "https://thiswarriorslife.substack.com/p/in-focus-warriors-wingers-and-centres"),
    'Albert Vete': ("Prop. Warriors 2018. A one-season Warrior in the prop rotation during the Kearney era's first year.", "In Focus: Props", "https://thiswarriorslife.substack.com/p/in-focus-warriors-props"),
    'Anthony Gelling': ("Centre / wing. Warriors 2018–19. A former Wigan Warriors player who gave two seasons in the Warriors' back line.", "In Focus: Wingers & Centres", "https://thiswarriorslife.substack.com/p/in-focus-warriors-wingers-and-centres"),
    'Ash Taylor': ("Halfback. Warriors 2022. A former Gold Coast half who had a brief stint at the Warriors in 2022.", "In Focus: Halves", "https://thiswarriorslife.substack.com/p/in-focus-warriors-halves"),
    'Ben Farr': ("Winger. Warriors 2022–23. A young winger who got his opportunity in the top squad across two seasons.", "In Focus: Wingers & Centres", "https://thiswarriorslife.substack.com/p/in-focus-warriors-wingers-and-centres"),
    'Blake Ayshford': ("Winger. Warriors 2019–20. A local winger who gave two seasons in the top squad.", "In Focus: Wingers & Centres", "https://thiswarriorslife.substack.com/p/in-focus-warriors-wingers-and-centres"),
    'Dunamis Lui': ("Back-rower. Warriors 2022. A local forward who had a run in the top squad during 2022.", "In Focus: Back-Rowers", "https://thiswarriorslife.substack.com/p/in-focus-warriors-back-rowers"),
    'Eiden Ackland': ("Winger. Warriors 2022. A young local winger who made his NRL debut for the Warriors in 2022.", "In Focus: Wingers & Centres", "https://thiswarriorslife.substack.com/p/in-focus-warriors-wingers-and-centres"),
    'Isaiah Vagana': ("Prop. Warriors 2022. Son of club legend Joe Vagana. Gave the front-row a famous name in 2022.", "In Focus: Props", "https://thiswarriorslife.substack.com/p/in-focus-warriors-props"),
    'Jackson Frei': ("Prop. Warriors 2021–22. A local prop who gave two seasons in the top squad.", "In Focus: Props", "https://thiswarriorslife.substack.com/p/in-focus-warriors-props"),
    'Kalani Going': ("Halfback. Warriors 2022–23. A young New Zealand-born half who got opportunities in the spine across two seasons.", "In Focus: Halves", "https://thiswarriorslife.substack.com/p/in-focus-warriors-halves"),
    'Luke Hanson': ("Lock. Warriors 2023, 2026. A local forward who has returned to the top squad at different points in the Webster era.", "In Focus: Back-Rowers", "https://thiswarriorslife.substack.com/p/in-focus-warriors-back-rowers"),
    'Paul Turner': ("Winger. Warriors 2020–21. A local winger who got his opportunity across two seasons.", "In Focus: Wingers & Centres", "https://thiswarriorslife.substack.com/p/in-focus-warriors-wingers-and-centres"),
    'Sam Cook': ("Prop. Warriors 2018. A one-season prop during the first year of the Kearney era.", "In Focus: Props", "https://thiswarriorslife.substack.com/p/in-focus-warriors-props"),
    'Sanele Aukusitino': ("Back-rower. Warriors 2022. A local forward who had a run in the top squad during 2022.", "In Focus: Back-Rowers", "https://thiswarriorslife.substack.com/p/in-focus-warriors-back-rowers"),
    'Solomon Vasuvulagi': ("Winger. Warriors 2022. A young local winger who made his debut for the Warriors in 2022.", "In Focus: Wingers & Centres", "https://thiswarriorslife.substack.com/p/in-focus-warriors-wingers-and-centres"),
    'Taane Milne': ("Winger. Warriors 2020. A speedster who had a standout performance — 7.5/10 from Will — in one COVID-season appearance.", "In Focus: Wingers & Centres", "https://thiswarriorslife.substack.com/p/in-focus-warriors-wingers-and-centres"),
    'Tanner Stanners-Smith': ("Back-rower. Warriors 2024. A local forward who got his opportunity in the top squad.", "In Focus: Back-Rowers", "https://thiswarriorslife.substack.com/p/in-focus-warriors-back-rowers"),
    'Adam Keighran': ("Five-eighth. Warriors 2019–20. A utility back who provided spine cover across two seasons before departing.", "In Focus: Halves", "https://thiswarriorslife.substack.com/p/in-focus-warriors-halves"),
    'Alofiana Khan-Pereira': ("Winger. Joined from the Gold Coast Titans for 2026. Fast — very fast. That's not a metaphor.", "2026 Selection Table: Centres & Wingers", "https://thiswarriorslife.substack.com/p/2026-selection-table-centres-and"),
    'Etuake Fukofuka': ("Back-rower. Warriors 2023. A local forward who got his opportunity in the top squad.", "In Focus: Back-Rowers", "https://thiswarriorslife.substack.com/p/in-focus-warriors-back-rowers"),
    'Geronimo Doyle': ("Utility back. Warriors 2023. A versatile back who had a run in the top squad.", "In Focus: Wingers & Centres", "https://thiswarriorslife.substack.com/p/in-focus-warriors-wingers-and-centres"),
    'Michael Sio': ("Prop. Warriors 2022. A veteran prop who gave one season in the Warriors' middle rotation.", "In Focus: Props", "https://thiswarriorslife.substack.com/p/in-focus-warriors-props"),
    'Morgan Gannon': ("Back-rower. Warriors 2026. A young forward from the Warriors' development pathway who earned selection in 2026.", "In Focus: Back-Rowers", "https://thiswarriorslife.substack.com/p/in-focus-warriors-back-rowers"),
    'Patrick Moimoi': ("Prop. Warriors 2023. A local front-rower who got his chance in the top squad.", "In Focus: Props", "https://thiswarriorslife.substack.com/p/in-focus-warriors-props"),
    'Poasa Faamausili': ("Prop. Warriors 2020. A local prop who was part of the COVID-era squad.", "In Focus: Props", "https://thiswarriorslife.substack.com/p/in-focus-warriors-props"),
    'Quinnlan Tupou': ("Winger. Warriors 2023. A young local winger who made his debut during the 2023 season.", "In Focus: Wingers & Centres", "https://thiswarriorslife.substack.com/p/in-focus-warriors-wingers-and-centres"),
    'Setu Tu': ("Prop. Warriors 2023. A local front-rower who got his opportunity in the top squad.", "In Focus: Props", "https://thiswarriorslife.substack.com/p/in-focus-warriors-props"),
    'Toni Tupouniua': ("Back-rower. Warriors 2023. A Tongan international who had a brief stint at the Warriors.", "In Focus: Back-Rowers", "https://thiswarriorslife.substack.com/p/in-focus-warriors-back-rowers"),
}

# Also need L1 + L2 for a few with missing early levels
L1_EXTRA = {
    'Adam Keighran': ("Was never rated by Will in a competitive game — only appeared in trial matches during 2019–20. Zero rated appearances across two seasons.", "TWL Ratings Archive"),
    'Alofiana Khan-Pereira': ("Zero rated appearances in Will's system so far — joined for 2026 and hasn't yet given Will enough to rate. A blank canvas. Filling it quickly.", "TWL Ratings Archive"),
}
L2_EXTRA = {
    'Joseph Vuna': ("A winger in the Warriors' squad 2018–19 — appeared in both seasons without leaving a significant ratings trail.", "TWL Ratings Archive"),
    'Brayden Wiliame': ("A Fijian international winger who spent 2022 at the Warriors — three rated appearances, average 6.83/10.", "TWL Ratings Archive"),
    'Isaiah Vagana': ("Joined the Warriors in 2022 following a career in NSW Cup. Made one rated appearance — 5.5/10 from Will.", "TWL Ratings Archive"),
    'Paul Turner': ("Two seasons (2020–21) in the Warriors' back line. Appeared in limited games, average 6.5/10 from Will.", "TWL Ratings Archive"),
    'Sanele Aukusitino': ("One rated appearance for the Warriors in 2022 — 5.5/10 from Will in a bench stint.", "TWL Ratings Archive"),
    'Solomon Vasuvulagi': ("One rated appearance for the Warriors in 2022 — 6.5/10 from Will on debut.", "TWL Ratings Archive"),
    'Tanner Stanners-Smith': ("One rated appearance in 2024 — 5.5/10 from Will. A young forward given a chance.", "TWL Ratings Archive"),
}

# Apply patches
for p in players:
    name = p['name']
    existing_diffs = set(c['difficulty'] for c in p['clues'])
    
    if 5 not in existing_diffs and name in L5:
        entry = L5[name]
        text, source = entry[0], entry[1]
        url = entry[2] if len(entry) > 2 else None
        p['clues'].append({'difficulty': 5, 'type': 'fact', 'text': text, 'source_url': url})
    
    if 1 not in existing_diffs and name in L1_EXTRA:
        text, source = L1_EXTRA[name]
        p['clues'].append({'difficulty': 1, 'type': 'stat', 'text': text, 'source_url': None})
    
    if 2 not in existing_diffs and name in L2_EXTRA:
        text, source = L2_EXTRA[name]
        p['clues'].append({'difficulty': 2, 'type': 'stat', 'text': text, 'source_url': None})

# Re-sort clues by difficulty
for p in players:
    p['clues'].sort(key=lambda c: c['difficulty'])

# Check coverage
all_ok = 0
still_missing = []
for p in players:
    diffs = set(c['difficulty'] for c in p['clues'])
    if all(d in diffs for d in [1,2,3,4,5]):
        all_ok += 1
    else:
        missing = [d for d in [1,2,3,4,5] if d not in diffs]
        still_missing.append((p['name'], missing))

print(f"Players with all 5 levels: {all_ok}/112")
if still_missing:
    print("Still missing levels:")
    for name, m in still_missing:
        print(f"  {name}: missing {m}")

# Save
coaches = [x for x in data if x['type'] == 'coach']
output = coaches + players
with open('/home/claude/warriors_who_am_i_v3.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\nSaved v3: {len(output)} total entries")
