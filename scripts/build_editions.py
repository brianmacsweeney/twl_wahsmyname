"""
Build three editions of player clue data:
- all_time: all 114 players (original clues from build_clues_v2)
- modern: 2020-2025 players only
- season_2026: 2026 players with FRESH clues drawn from 2026 round-by-round data
"""
import json, re

# ── Load existing player data ────────────────────────────────────────────────
with open('/home/claude/players_final.js') as f:
    js = f.read()

players_json = js[len("const PLAYERS = "):-2]
all_players = json.loads(players_json)

# Build lookup
by_name = {p['name']: p for p in all_players}
print(f"Loaded {len(all_players)} players")

# ── Season data for filtering ────────────────────────────────────────────────
with open('/home/claude/warriors_who_am_i_v3.json') as f:
    db_data = json.load(f)
db_by_name = {x['name']: x for x in db_data if x['type'] == 'player'}

def get_seasons(name):
    if name in db_by_name:
        return db_by_name[name].get('seasons', [])
    # Stacey Jones, Manu Vatuvei not in DB
    if name == 'Stacey Jones': return ['1995','1996','1997','1998','1999','2000','2001','2002','2003','2004','2005']
    if name == 'Manu Vatuvei': return ['2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017']
    return []

# ── 2026 FRESH CLUES ─────────────────────────────────────────────────────────
# Written from 2026 round-by-round data — NO overlap with existing clues
# Key rule: existing clues cover career/background/history — new clues cover 2026 SEASON specifics

CLUES_2026 = {

"Tanah Boyd": [
    (1, "In the 2026 season opener, Will wrote: \u201cWhat a night for the oft-maligned ex-Titan\u201d — he dummied through for his first NRL try as a Warrior, set up five more tries, and scored 8.5/10."),
    (2, "In Round 3, 2026, this player posted 653 kicking metres including 23 of the Warriors' 25 general play kicks — the most by any Warrior halfback in a single game of the 2026 season."),
    (3, "Rounds 1 and 2 of 2026 were the only back-to-back 8.5/10 ratings Will has ever given a Warriors halfback to open a season."),
    (4, "Halfback. In Round 2, 2026, Will described his kicking game — long, short and high — as terrorising the Raiders. He scored a try for the second consecutive week."),
    (5, "Halfback. The starting No.7 for the Warriors in 2026. Has set up and scored tries in nearly every game — Will called him \u201cnot the main reason the Warriors are unbeaten, but try telling that to the scoreboard.\u201d"),
],

"Jackson Ford": [
    (1, "In Round 8, 2026, this player made 57 tackles — the most by any Warriors forward in a single game recorded in the 2026 season — while also running for 206 metres in 80 minutes. Will asked: \u201cShould he be getting a rest?\u201d"),
    (2, "In Rounds 1 and 2 of 2026, he made 219 metres and 219 metres from prop — the highest two-game running total by a Warriors forward to open a season. Will asked at what point do we call him an NSW Origin contender."),
    (3, "In Round 3, 2026, he played the full 80 minutes, made two line-breaks, scored a try and topped both run metres (236) and tackles (44) — while Will noted it may have ended his perfect Dally M Medal streak."),
    (4, "Prop. Led the 2026 Warriors in run metres in multiple rounds. Will noted he ran for 113 post-contact metres in Round 1 — the most by a Warriors prop in a single 2026 game."),
    (5, "Prop. The 2026 Dally M Medal frontrunner from the Warriors through the first eight rounds — Will has been tracking him as a genuine NRL award contender."),
],

"James Fisher-Harris": [
    (1, "In Round 8, 2026, this player put in a 59-minute shift after a co-captain's early exit — running for 164 metres and making 30 tackles. Will noted \u201can ill-conceived pass\u201d was the only black mark."),
    (2, "In Round 1, 2026, Will wrote: \u201cThis is the four-time premiership-winning version of JFH we banked on getting\u201d — calling it arguably his best performance for the club to date."),
    (3, "In Round 7, 2026, Will wrote: \u201cIf not for Ford's heroics, JFH would be an early Dally M Team of the Year front-runner\u201d — after 128 metres, 43 tackles and a neat try assist for Clark."),
    (4, "Prop. His 2026 season included scoring a 55-metre try in Round 3 against the Knights — storming up in support after narrowly being denied twice earlier in the game."),
    (5, "Prop. Warriors co-captain. Has been described by Will in 2026 as developing into \u201can excellent club captain.\u201d His leadership is now cited as central to the Warriors' strong start."),
],

"Chanel Harris-Tavita": [
    (1, "In Round 8, 2026, this was his 100-game milestone for the Warriors. Will noted: \u201cLovely touches in both of AKP's tries, took the kicking pressure off Boyd\u201d — and still called it his least impressive of 2026."),
    (2, "In Round 6, 2026, Will wrote: \u201cSimply has to be in the side — in the halves — from now on. Brings an indefinable calm to the Warriors and invariably pulls out big plays.\u201d Rating: 8.5/10."),
    (3, "Scored 8.5/10 in Rounds 1 and 6 of 2026 — the only Warrior other than Boyd and Ford to score back-to-back 8.5s at any point in the first eight rounds."),
    (4, "Five-eighth. In Round 1, 2026, scored two tries off Roger Tuivasa-Sheck passes — the second a match-sealer started with his own bomb. Will called him one of the best on ground."),
    (5, "Five-eighth. 'CHT.' Reached 100 games for the Warriors in Round 8, 2026. Will has described his combination with Boyd as the Warriors' most productive halves pairing of the season."),
],

"Roger Tuivasa-Sheck": [
    (1, "In Round 6, 2026, this player was shifted to centre for the first time since the penultimate round of 2024 — and rated 8.5/10. Will noted his \u201cbooming try-saver\u201d as one of the highlights."),
    (2, "In Round 2, 2026, he played his 150th game for the Warriors — Will called it a \u201cmilestone man\u201d game, with 212 metres on 22 carries as he \u201cworkhorsed\u201d his way to the win."),
    (3, "In Rounds 7 and 8, 2026, he played at centre — providing two try assists for Alofiana Khan-Pereira in Round 7 and a tip-on assist in Round 8. Will called him \u201cmore of a threat on attack than during a failed stint in the position in 2024.\u201d"),
    (4, "Wing/centre. In Round 1, 2026, he scored 8.5/10 for spectacularly laying on three tries by climbing to take high balls and producing passes in all three — Will called it a \u201cmasterful display in a rather unexpected department.\u201d"),
    (5, "Wing/centre. 'RTS.' Played his 150th game for the Warriors in 2026. Moved to centre during 2026 with striking success. Will referred to him as \u201cour club legend\u201d and wrote of getting \u201ca little melancholy thinking about the prospect of our club legend finishing his NRL career elsewhere.\u201d"),
],

"Taine Tuaupiki": [
    (1, "In Round 8, 2026, this player ran for 235 metres, made 10 tackle-breaks and scored the match-winning try from Wayde Egan's kick — Will wrote he \u201cstaked a genuine claim for the No.1 jersey.\u201d"),
    (2, "In Round 2, 2026, he was an emergency replacement at fullback — and ran 210 metres on 22 carries with six tackle-breaks across 72 minutes. Will wrote: \u201cLikely to get the No.1 jersey next week.\u201d"),
    (3, "In Round 3, 2026, he made a searing line-break then unselfishly gave the final try to Luke Hanson — while also making a game-high seven tackle-breaks. Will noted his \u201cmost important contribution you won't find in any stats.\u201d"),
    (4, "Fullback. Stepped in across multiple rounds in 2026 when Charnze Nicoll-Klokstad was unavailable or moved to centre. Each time, Will highlighted his superiority as an attacking fullback option."),
    (5, "Fullback. 'Taine.' After his 235-metre, match-winning performance in Round 8, 2026, Will wrote the fullback debate \u201ccan't last much longer.\u201d Has been the Warriors' most electric back in 2026."),
],

"Wayde Egan": [
    (1, "In Round 6, 2026, Will wrote this player \u201cthoroughly outplayed\u201d Queensland and Australian hooker Harry Grant — directing traffic around the rucks, finishing with two try assists before taking an early mark. An Origin statement."),
    (2, "In Round 3, 2026, Will wrote: \u201cThe elite rake hasn't overly stood out during this trio of thrashings — but he has needed to. Instead, he expertly marshals the ruck and puts his passes on a dime.\u201d 7.5/10."),
    (3, "In Round 8, 2026, this player laid on the match-winning try for Taine Tuaupiki with one of his two line-break assists — then had a hand in DWZ's try off the back of the scrum. 6.5/10."),
    (4, "Hooker. In Round 2, 2026, he spent 12 minutes at five-eighth to close out the game — an indicator of his versatility as the Warriors' most trusted ball-player."),
    (5, "Hooker. The Warriors' starting No.9 across all 8 rounds in 2026. Will has consistently rated him as one of the best hookers in the NRL — and in Round 6, he outplayed Australian hooker Harry Grant."),
],

"Erin Clark": [
    (1, "In Round 8, 2026, this player made two memorable line-breaks in 48 minutes — helping him to a season-high 178 metres from 12 runs. Will called it \u201ca barnstorming performance.\u201d 7.5/10."),
    (2, "In Round 3, 2026, he scored a \u201cbarnstorming maiden try for the Warriors\u201d before notching 138 metres and 23 tackles — while making 14 passes including a line-break assist."),
    (3, "Scored 7.5/10 in four separate rounds of 2026 (Rounds 2, 3, 7, 8) — the joint-most 7.5-or-above ratings of any Warriors forward across the first eight rounds."),
    (4, "Lock. In 2026, his impact dropped from his 2025 Dally M Lock of Year standards — Will noted he has been \u201csignificantly less\u201d than his 2025 form. His response was two consecutive 7.5s in Rounds 7 and 8."),
    (5, "Lock. No.13. After winning the TWL POTY in 2025, he has been measured against a very high bar in 2026 — and has responded with strong second-half form, including a try and a run-around play with JFH in Round 7."),
],

"Leka Halasima": [
    (1, "In Round 1, 2026, this player scored his 14th try in 23 NRL games — thrown into the match at minute 46. Will wrote he was \u201cthrowring down the gauntlet to Nanai and Olakau'atu as arguably the best aerial forward in the NRL.\u201d"),
    (2, "In Round 2, 2026, he started for the first time in 2026 and scored a sensational double — pouncing on a grubber and then beating four defenders — while playing the full 80 minutes."),
    (3, "His scoring rate across 2025-26: 14 tries from his last 17 games before Round 4. Will cited this figure in his Round 3 ratings as the benchmark of his consistency."),
    (4, "Back-rower. In Round 3, 2026, he played in the centres (not his position) and still scored a try and made 120 metres from 12 carries. Will described him as not looking \u201cat home\u201d out wide — but he still performed."),
    (5, "Back-rower. 2026 stats through eight rounds: consistently the Warriors' most dynamic edge forward. Will described him as a player who \u201csimply is too good to hold back\u201d from a permanent starting role."),
],

"Charnze Nicoll-Klokstad": [
    (1, "In Round 2, 2026, he was \u201cshoehorned into five-eighth\u201d after CHT's concussion at nine minutes — playing most of the game out of position. Will rated him 6.5/10, noting he \u201cdid a difficult job well.\u201d"),
    (2, "In Round 5, 2026, Will described a failed experiment: \u201cThe CNK to centre experiment appears to have already run its course\u201d after he struggled on the edge as the Warriors conceded three tries."),
    (3, "In Round 3, 2025, this player received a '9' from Will — the highest single-game rating for any Warrior in the entire 2025 season. In 2026, his highest is 7.5. Will has noted his form is \u201cgood but not 2025-level.\u201d"),
    (4, "Fullback. His 2026 season has been characterised by a positional debate — Will has had him shifted between fullback, centre and five-eighth across the first eight rounds."),
    (5, "Fullback. 'CNK.' In 2026, shared the fullback role with Taine Tuaupiki across the first eight rounds as Andrew Webster worked through his best combination at the back."),
],

"Mitch Barnett": [
    (1, "In Round 3, 2026, this player returned from an ACL injury in his first NRL game since June 2025 — 36 minutes, 121 metres on 11 runs, a try assist for Ford. Will wrote: \u201cwasn't it dripping with quality?\u201d Rating: 7.5/10."),
    (2, "In Round 7, 2026, he returned from a broken thumb — 45 minutes, 161 metres, 21 tackles. Will wrote: \u201cGives the pack an even harder edge\u201d and noted his \u201cmouth-watering\u201d return."),
    (3, "In Round 8, 2026, he completed 14 runs for 116 metres in just 23 minutes before an unscheduled exit — Will noted he \u201cwill inevitably be out next week\u201d due to injury."),
    (4, "Prop. Co-captain. His 2026 season has been interrupted by an ACL return (Rd 3), then a broken thumb (Rd 7), then a new injury (Rd 8). Despite this, Will says his presence makes the Warriors \u201ca harder-edged team.\u201d"),
    (5, "Prop. Co-captain. Has appeared in Rounds 3, 4, 7 and 8 of 2026 despite ongoing injury management. Will called his Rd 7 return \u201cmouth-watering signs in the Brisbane-bound enforcer's early return.\u201d"),
],

"Dallin Watene-Zelezniak": [
    (1, "In Round 5, 2026, this player scored a hat-trick at Shark Park — including a \u201csensational 12-point turnaround long-range intercept try.\u201d Will rated him 7.5/10. He then scored a double in Round 6 and a try in Round 7."),
    (2, "In Round 4, 2026, Will described \u201ca mind-boggling error on the kick return that makes you want to quit watching rugby league forever\u201d — immediately after praising \u201csome great defused kicks.\u201d Classic DWZ."),
    (3, "In Round 8, 2026, he scored a try and defended well — but gave away two penalties and a play-the-ball blunder in the final 10 minutes. Will noted he \u201cmay miss next week.\u201d 5.5/10."),
    (4, "Winger. In Round 2, 2026, he scored two tries including an outstanding first-up finish to set the tone — then nearly gifted the Raiders a try with a goal-line blunder that \u201cthankfully went unpunished.\u201d"),
    (5, "Winger. 'DWZ.' Scored five tries across Rounds 5, 6 and 7 of 2026 — the most by any Warriors back in a three-round stretch this season. Still the cult hero. Still the highlight reel."),
],

"Demitric Vaimauga": [
    (1, "In Round 6, 2026, Will wrote: \u201cThis was the performance we've been waiting patiently for.\u201d The 21-year-old \u201cemasculated the Storm pack in 41 blockbusting minutes\u201d — 130 metres, 18 runs, 11 tackles. Rating: 8.5/10."),
    (2, "In Round 1, 2026, Will noted he played 27 minutes \u201cwithout a miss\u201d in his tackle count and wrote \u201che will get his chance to play a more prominent role.\u201d By Round 6, he had it."),
    (3, "His 8.5/10 in Round 6, 2026 was the highest single-game rating of any Warriors player from the bench across the first eight rounds of the season."),
    (4, "Prop. His 2026 trajectory: limited bench minutes in Rounds 1-3, then a breakthrough 8.5/10 rating in Round 6. Will called him \u201cthe budding enforcer\u201d and said his Round 6 showing was \u201clong overdue.\u201d"),
    (5, "Prop. 21 years old. In Round 6, 2026, he delivered the breakout performance Will had been waiting for — 8.5/10, described as \u201cblockbusting\u201d and one of the best forward displays of the Warriors' 2026 season."),
],

"Kurt Capewell": [
    (1, "In Round 1, 2026, Will wrote this was \u201cperhaps his finest performance for the club\u201d — a try assist for Adam Pompey, a try of his own, and a \u201ctremendous\u201d reflex slip-catch of a dangerous kick that epitomised his elite clean-up work. Rating: 8.5/10."),
    (2, "His Round 1, 2026 rating of 8.5/10 was the highest score ever given to this player by Will — surpassing anything from his 2024 season. Will wrote he made \u201cten runs for 88 metres\u201d alongside \u201ca massive contribution in the middle third.\u201d"),
    (3, "Missed Rounds 2-6 through injury before returning in Round 7. Will immediately noted he \u201cshapes as a key figure for the campaign ahead.\u201d Played Rounds 7 and 8 strongly."),
    (4, "Back-rower. Available for three of the first eight rounds of 2026 due to injury but made an 8.5/10 impact when fit. Will cited his \u201celite clean-up work\u201d as something the Warriors miss when he's out."),
    (5, "Back-rower. Three-time grand finalist. Queensland Origin rep. His 2026 Round 1 was described by Will as possibly his best performance for the Warriors. Is building into a key figure for the season."),
],

"Tanner Stowers-Smith": [
    (1, "In Round 5, 2026, Will wrote he was \u201cby far the most eye-catching of the Warriors' forwards\u201d — 143 metres on 16 carries, 22 tackles. Will added: \u201cseems to have gained a couple of extra yards of pace in the off-season.\u201d Rating: 7.5/10."),
    (2, "In Round 1, 2026, he \u201cpowered through 112 metres on 13 carries\u201d in 40 minutes on debut — Will noting he made it \u201cvery hard to leave him out of the 17, despite being the most likely to make way when Mitch Barnett returns.\u201d"),
    (3, "Will has called this player a dilemma for Andrew Webster — consistently outstanding in 2026 but expected to lose his spot when the co-captain returns from injury. Through Round 8, he hasn't lost it."),
    (4, "Back-rower. Has earned Will's 7.5/10 twice in the first eight rounds of 2026 — the joint-most of any Warriors bench forward this season."),
    (5, "Back-rower. Local product. Has been one of the surprise performers of the 2026 Warriors season — Will described his Round 5 as the best individual forward display of the round."),
],

"Adam Pompey": [
    (1, "In Round 1, 2026, this player scored a try in a game where Will rated his teammate Boyd 8.5/10 — Pompey's try came directly off a Boyd kick assist. Will described him as \u201cvirtually a certainty\u201d for 2026 after a career-best 2025."),
    (2, "After scoring 11 tries in 2025, his first four rounds of 2026 averaged just 5.5/10 from Will — a sharp contrast to his 2025 form. Will noted the team's output had dropped from Rounds 4 onward."),
    (3, "Centre. In Will's pre-season analysis, he was the \u201conly player locked into a definitive Warriors three-quarter spot\u201d for 2026 — a reflection of his 2025 career-best season rather than his 2026 form so far."),
    (4, "Centre. 'Wets.' Appeared in all 8 rounds of the Warriors' 2026 season. Will called him \u201cvirtually a certainty\u201d — then his early-season ratings suggested the certainty was of his spot, not his performance level."),
    (5, "Centre. 'Wets.' One of the first names on Andrew Webster's 2026 teamsheet. Six-plus seasons, 120+ games. A Warriors institution who had a career-best 2025 — and is working back to that form in 2026."),
],

"Ali Leiataua": [
    (1, "In Round 1, 2026, this player received 3.5/10 from Will — one of the lowest ratings ever given to a Warriors starter. Will wrote he \u201cinstilled little confidence he is the elusive long-term centre solution\u201d after being schooled by Billy Smith twice in the first 50 minutes."),
    (2, "In Round 2, 2026, he scored a \u201cbrilliant intercept try\u201d — which Will noted \u201ccould be the precursor to belatedly cementing the right centre spot.\u201d Went from 3.5 to 6.5/10 in one week."),
    (3, "By Round 6, 2026, Will noted he was 6-0 across the grades this season with four tries — his improvement across the season described as \u201ctantalising ability on display more often than not.\u201d"),
    (4, "Centre/winger. Nephew of Ali Lauitiiti. In 2026, he has improved steadily across eight rounds — from Will's 3.5/10 in Round 1 to consistent 6.5s, with Will increasingly backing him as a long-term centre option."),
    (5, "Centre/winger. Nephew of Warriors legend Ali Lauitiiti. His 2026 season has been a story of improvement — a low of 3.5/10 in Round 1, then consistent 6.5s through the back half of the opening stretch."),
],

"Sam Healey": [
    (1, "In Round 6, 2026, Will noted his father Mitch Healey's connection to Cronulla — in a round where Wayde Egan \u201cthoroughly outplayed\u201d Queensland and Australian hooker Harry Grant at the same venue Mitch Healey called home for 200+ games."),
    (2, "In Round 2, 2026, his chances of playing \u201cnosedived when CHT exited early\u201d — then he played the final 27 minutes at dummy-half and was \u201calways looking to poke his nose through.\u201d Will called him \u201ca hot start\u201d operator. Rating: 6.5/10."),
    (3, "In Round 5, 2026, he scored a try in 12 minutes including \u201ca deft grubber that resulted in Clark's try\u201d — before suffering a head knock. His running game is what separates him from a traditional backup hooker."),
    (4, "Hooker. Backup to Wayde Egan. Has averaged around 20 minutes per game across 2026. Will has highlighted his \u201celusive running game, offloading ability and support play\u201d as different from what Egan provides."),
    (5, "Hooker. Son of Cronulla Sharks legend Mitch Healey. Backup to Wayde Egan in 2026. Has impressed fans whenever used — Will's dilemma is how to get him more game-time without disrupting Egan's rhythm."),
],

"Alofiana Khan-Pereira": [
    (1, "In Round 7, 2026, this player scored two tries off Roger Tuivasa-Sheck assists — Will described his first finish as \u201cbrilliant\u201d and wrote that RTS \u201cseems to love playing inside him.\u201d Only appeared from Round 6 onward."),
    (2, "In Round 8, 2026, he scored two tries — a tip-on from RTS and a second later in the match. Will noted he was a major threat despite the Warriors' \u201cscrappy\u201d performance around him."),
    (3, "Has scored in every game he's played in 2026 — four tries from three appearances (Rounds 6, 7, 8). Will described him as potentially \u201cthe quickest Warrior ever\u201d in his pre-season preview."),
    (4, "Winger. 'AKP.' Made his 2026 debut in Round 6 and immediately started scoring. Four tries in three games. Will described his partnership with RTS as the Warriors' most dangerous attacking combination in 2026."),
    (5, "Winger. 'AKP.' Joined from Gold Coast in 2026. Has scored four tries in his first three appearances for the Warriors. Will wrote: \u201ccan conjure four points out of thin air.\u201d"),
],

"Marata Niukore": [
    (1, "In Round 5, 2026, this player appeared in only four games across the first eight rounds — Will's ratings for him peaked at 5.5/10, with the comment that his output had been \u201cunderwhelming\u201d compared to his 2023 and 2024 form."),
    (2, "Has the most career sin-bins in Warriors history — five — but in 2026 has been a more disciplined operator, averaging 5.5/10 across four rated appearances with no cards to his name."),
    (3, "Back-rower. In 2026, his opportunities have been limited by the outstanding form of James Fisher-Harris, Mitch Barnett and Demitric Vaimauga ahead of him in the middle rotation."),
    (4, "Back-rower. New Zealand international. In 2026, used mainly as a bench option — his role diminished by the Warriors' deep prop rotation. Will has not called him out but the numbers have been below his 2023 peak."),
    (5, "Back-rower. New Zealand international. 2026 has been a challenging season for him — limited minutes and below-par ratings as the Warriors' forward depth has pushed him down the pecking order."),
],

"Luke Metcalf": [
    (1, "In Round 1, 2026, this player rated 4.5/10 from Will — the lowest competitive rating of his Warriors career. Will noted \u201chis confidence and control\u201d were missing compared to his 2025 form."),
    (2, "Only appeared in Rounds 1 and 2 of 2026 before his return from injury was managed. His Round 1 4.5/10 was the worst rating given to any Warriors halfback in the 2026 season."),
    (3, "His 2026 return from ACL surgery has been carefully managed — appearing in just the first two rounds before a break in his comeback schedule. Will was openly cautious about his pace of return."),
    (4, "Halfback. His 2026 return from ACL has been slower than anticipated — two appearances, a 4.5/10, and a return to management. Will has been measured about expectations for the second half of his comeback."),
    (5, "Halfback. Has played just two games in 2026 while managing his ACL return. Will rated him 4.5/10 in Round 1 — his lowest Warriors rating — as he works back to 2025 form."),
],

"Jacob Laban": [
    (1, "In Round 4, 2026, this player scored the Warriors' opening try from a Tanah Boyd pass — his second NRL try and his first of the 2026 season. The Warriors lost 14-32. Will rated him 6.5/10."),
    (2, "Has averaged 6.17/10 across three rated appearances in 2026 — solid for a young edge forward competing against Halasima, Clark and Capewell for game-time."),
    (3, "Back-rower. Warriors Rookie of Year 2024. In 2026, has had limited opportunities — appearing in eight rounds but only rated in three, as the Warriors' forward depth limits his exposure."),
    (4, "Back-rower. Local product. In 2026, competes with Leka Halasima, Erin Clark and Kurt Capewell for the edge back-row spots. Will has noted his \u201csteady if unspectacular\u201d contribution."),
    (5, "Back-rower. Warriors Rookie of Year 2024. Has appeared in multiple 2026 squads but gets limited top-grade minutes behind the Warriors' established back-row stars."),
],

"Wayde Egan": [  # Additional fresh clue - already have entry above
    (1, "In Round 6, 2026, Will wrote this player \u201cthoroughly outplayed\u201d Queensland and Australian hooker Harry Grant — directing traffic around the rucks, finishing with two try assists before taking an early mark. An Origin statement."),
],
}

# Remove duplicated Wayde Egan entry at bottom
if len(CLUES_2026.get('Wayde Egan', [])) > 5:
    CLUES_2026['Wayde Egan'] = CLUES_2026['Wayde Egan'][:5]

# ── Build edition arrays ─────────────────────────────────────────────────────

def player_era_filter(p, mode):
    """Return True if player should appear in this edition"""
    seasons = get_seasons(p['name'])
    if mode == 'all_time':
        return True
    elif mode == 'modern':
        return any(s in seasons for s in ['2018','2019','2020','2021','2022','2023','2024','2025']) \
               and not any(s in seasons for s in ['2026'])
    elif mode == 'season_2026':
        return '2026' in seasons

# Build 2026 card variants (fresh clues only)
def build_2026_card(p):
    name = p['name']
    if name not in CLUES_2026:
        return None  # No fresh 2026 clues available, skip
    
    fresh = CLUES_2026[name]
    clue_objs = []
    for diff, text in sorted(fresh, key=lambda x: x[0]):
        pts = 50 - (diff - 1) * 10
        clue_objs.append({'pts': pts, 'text': text, 'source': 'TWL 2026 Ratings', 'url': None})
    
    # Pad to 5 clues if needed using position from original
    pts_present = {c['pts'] for c in clue_objs}
    for orig in p['clues']:
        if orig['pts'] not in pts_present and len(clue_objs) < 5:
            clue_objs.append(orig)
            pts_present.add(orig['pts'])
    
    clue_objs.sort(key=lambda c: -c['pts'])
    
    return {
        'id': p['id'] + '-2026',
        'name': p['name'],
        'era': '2026',
        'aliases': p['aliases'],
        'clues': clue_objs
    }

# Build all three editions
editions = {
    'all_time': [],
    'modern': [],
    'season_2026': []
}

for p in all_players:
    for mode in ['all_time', 'modern']:
        if player_era_filter(p, mode):
            editions[mode].append(p)

# 2026 edition uses fresh clues
for p in all_players:
    if player_era_filter(p, 'season_2026'):
        card = build_2026_card(p)
        if card:
            editions['season_2026'].append(card)
        else:
            # Use original card if no fresh clues written
            editions['season_2026'].append(p)

print(f"all_time: {len(editions['all_time'])} players")
print(f"modern (2018-2025): {len(editions['modern'])} players")
print(f"season_2026: {len(editions['season_2026'])} players with 2026-specific clues")

# Add Stacey Jones and Manu Vatuvei to modern edition? No - they're pre-2018
# Check
sj = by_name.get('Stacey Jones')
mv = by_name.get('Manu Vatuvei')
print(f"\nStacey Jones in modern: {any(p['name']=='Stacey Jones' for p in editions['modern'])}")
print(f"Manu Vatuvei in modern: {any(p['name']=='Manu Vatuvei' for p in editions['modern'])}")

# Write JS with all three editions
import json as json_mod
output_js = f"""const EDITIONS = {{
  all_time: {json_mod.dumps(editions['all_time'], ensure_ascii=False)},
  modern: {json_mod.dumps(editions['modern'], ensure_ascii=False)},
  season_2026: {json_mod.dumps(editions['season_2026'], ensure_ascii=False)}
}};
"""

with open('/home/claude/editions.js', 'w', encoding='utf-8') as f:
    f.write(output_js)

# Validate with node
import subprocess
with open('/tmp/test_editions.js', 'w', encoding='utf-8') as f:
    f.write(output_js)
    f.write("""
console.log('all_time:', EDITIONS.all_time.length);
console.log('modern:', EDITIONS.modern.length);
console.log('season_2026:', EDITIONS.season_2026.length);
// Check first 2026 player clues
const p = EDITIONS.season_2026[0];
console.log('First 2026 player:', p.name, '| clues:', p.clues.length);
p.clues.forEach(c => console.log('  ', c.pts+'pts:', c.text.slice(0,60)));
""")

result = subprocess.run(['node', '/tmp/test_editions.js'], capture_output=True, text=True, timeout=10)
print(f"\nNode output:\n{result.stdout}")
if result.stderr: print(f"Errors: {result.stderr[:300]}")

print(f"\nEditions JS size: {len(output_js)//1024} KB")
