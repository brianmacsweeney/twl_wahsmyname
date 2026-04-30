"""
WHO AM I? Clue builder v2
Clues drawn from: background, origin, previous clubs, family, rep history,
records, physical traits, achievements, Will quotes — NOT just ratings.
Difficulty:
  1 (50pts) = deep trivia only a diehard knows
  2 (40pts) = specific achievement/record/stat from recent years  
  3 (30pts) = career milestone or rep honour
  4 (20pts) = position + era + key career fact
  5 (10pts) = position + nickname + most famous thing about them
"""
import json, re

PLAYERS = {

"Stacey Jones": dict(
    era="1995–2005", pos="Halfback", jersey="7",
    aliases=["stacey jones","jones","stacey","the little general","little general","sj"],
    clues=[
        (1, "Played 100 consecutive games from debut — a Warriors iron-man record that has never been matched. His run started in Round 1, 1995 and ended in Round 4, 1999 (shoulder)."),
        (2, "Won the Golden Boot — the award for the world's best rugby league player — three times. No other Warrior has won it more than once."),
        (3, "The Warriors' all-time record holder for career field goals with 14. Shaun Johnson eventually broke it with his 15th — nearly two decades later."),
        (4, "261 games, all for the Warriors. Club captain. Left for Super League in 2005. Never played another NRL game. One club, his entire career."),
        (5, "Halfback. 'The Little General.' Three-time world player of the year. Stacey Jones is the most decorated Warrior of the pre-ratings era."),
    ]
),

"Manu Vatuvei": dict(
    era="2004–2017", pos="Left wing", jersey="5",
    aliases=["manu vatuvei","vatuvei","manu","the beast","beast"],
    clues=[
        (1, "The only non-Australian to score 150 or more NRL tries. His 152 for the Warriors is a club record — second on the list is Shaun Johnson with 79. The gap is not close."),
        (2, "Led the Warriors' tryscoring charts every single season from 2007 to 2014 — eight consecutive years as the club's top try-scorer."),
        (3, "Grew up in Otara, South Auckland. His 2008 World Cup final appearance was one of five Warriors players in the Kiwis team that beat Australia 34-20."),
        (4, "226 games, 14 seasons, 28 Test matches for New Zealand. 'Built like Ken Maumalo but plays with the background noise presence of Kenny G' — that quote is about someone else. This player is the real thing."),
        (5, "Left wing. 'The Beast.' 152 tries — the Warriors' all-time record. Scored in the 2011 Grand Final. A Mount Smart legend in the fullest sense."),
    ]
),

"Shaun Johnson": dict(
    era="2011–2019, 2022–2024", pos="Halfback", jersey="7",
    aliases=["shaun johnson","johnson","shaun","sj"],
    clues=[
        (1, "Scored six field goals in a single game against Canberra in 2018 — a competition record for field goals by one player in a match. The Warriors still lost."),
        (2, "Left the Warriors in 2019 under a cloud — the circumstances were messy. Came back in 2022. Won the Dally M Halfback of the Year in 2023 and many felt he was robbed of the Medal."),
        (3, "1,213 career points for the Warriors — a club record by some distance. Second on the list is Stacey Jones with 674. Nobody else is within 500."),
        (4, "Won the Dally M Medal in 2018 — the first Warrior ever to win the NRL's top individual honour. Also holds the Warriors' record for career field goals with 18."),
        (5, "Halfback. 'SJ.' The Warriors' all-time points scorer. Won the 2018 Dally M Medal. 224 games across two stints. A generational talent the club didn't always deserve."),
    ]
),

"Roger Tuivasa-Sheck": dict(
    era="2016–2021, 2024–present", pos="Fullback", jersey="1",
    aliases=["roger tuivasa-sheck","tuivasa-sheck","roger","rts"],
    clues=[
        (1, "Left the Warriors in 2021 to become an All Black — he played for the Blues in Super Rugby and represented New Zealand in rugby union before returning to the Warriors in 2024. One of very few players to represent NZ in both codes at the highest level."),
        (2, "Has played more games at fullback for the Warriors than anyone in history — 107, and counting. Second on that list is Brent Webb with 87."),
        (3, "Won the 2018 Dally M Medal — the Warriors' first ever. Also won Dally M Fullback of the Year in 2018 and Captain of the Year in 2020."),
        (4, "Captained the Warriors for five seasons (2017–21), left for All Blacks rugby union, came back in 2024. Won the Simon Mannering Medal in 2025. One of the club's most beloved figures across two eras."),
        (5, "Fullback. 'RTS.' Four-time club Player of the Year. Won the 2018 Dally M Medal. The Warriors' greatest modern fullback — argue if you like, but clear your schedule."),
    ]
),

"Simon Mannering": dict(
    era="2005–2018", pos="Lock", jersey="13",
    aliases=["simon mannering","mannering","simon"],
    clues=[
        (1, "Made just 32 missed appearances across a 15-season Warriors career — in other words, was available for 269 of a possible 301 games. That durability record has not been touched."),
        (2, "Captained the Warriors for six consecutive seasons (2010–15) — a club record. Won the club's Player of the Year award five times. The award was renamed the Simon Mannering Medal in his honour after he retired."),
        (3, "The 16th player in NRL history to play 300 games for a single club. 301 games total. Never played for another NRL club. Debuted at 18, retired at 31."),
        (4, "Lock and second-rower. Warriors Rookie of the Year in 2005. The Warriors' all-time appearance record holder. The club's POTY award bears his name."),
        (5, "Lock. All-time Warriors appearance record holder — 301 games. Five-time club Player of the Year. The annual Warriors POTY award is named after him."),
    ]
),

"Tohu Harris": dict(
    era="2018–2024", pos="Lock", jersey="13",
    aliases=["tohu harris","harris","tohu"],
    clues=[
        (1, "Medically retired in January 2025 due to a chronic back injury — still in his 30s. Was widely regarded as the best Warriors leader of the modern era. Will called him 'one of the most respected Warriors of the modern era.'"),
        (2, "Won the Dally M Lock of the Year in 2023. Named in the Dally M Team of Year in both 2020 and 2023. Two-time club Player of the Year (2020, 2021)."),
        (3, "Started 50 games at second-row and 52 at lock for the Warriors — top-three in both categories. Has played Test football for New Zealand and appeared in 52 games for the Warriors before his retirement."),
        (4, "Club captain 2022–24. Arrived from Melbourne Storm before the 2018 season. Retired January 2025 — back injury. His absence defined 2025 as much as anything that happened on the field."),
        (5, "Lock. Warriors captain 2022–24. Two-time club Player of the Year. Won the Dally M Lock of the Year 2023. Retired too early due to a back injury. One of the club's greats."),
    ]
),

"James Fisher-Harris": dict(
    era="2025–present", pos="Prop", jersey="8",
    aliases=["james fisher-harris","fisher-harris","james","jfh"],
    clues=[
        (1, "His father is from Samoa and his mother is from the Cook Islands — he has represented the Kiwis at international level. Captains both the Warriors and New Zealand."),
        (2, "Won four NRL premiership rings at Penrith (2021, 2022, 2023, 2024) before joining the Warriors. Became Warriors co-captain in his first season at the club."),
        (3, "Has played over 200 NRL games. Kiwis captain. First season at the Warriors saw him rank in the top half-dozen NRL front-rowers for tackles per game — 114 average metres."),
        (4, "Prop. Signed from Penrith — where he won four premierships — as the marquee replacement for Addin Fonua-Blake. Co-captain with Mitch Barnett. 'JFH' to the TWL community."),
        (5, "Prop. Warriors and Kiwis co-captain. Four premiership rings from Penrith before joining in 2025. The marquee off-season signing the Warriors needed."),
    ]
),

"Mitch Barnett": dict(
    era="2022–2026", pos="Prop", jersey="10",
    aliases=["mitch barnett","barnett","mitch","mitchell barnett"],
    clues=[
        (1, "His father Mitch Barnett Sr played over 200 NRL games for Cronulla — the son had his career halted by an ACL in 2025 and was released to return home to Australia in 2026 for family reasons."),
        (2, "Became the first Warrior ever to debut for NSW State of Origin in 2024. That same season, became only the second Warrior to debut for Australia — after Richard Villasanti in 2003."),
        (3, "Sam Healey — his No.9 understudy — is the son of Mitch Healey, who played over 200 games for Cronulla. The connection between these two Warriors is their fathers both built careers at the Sharks."),
        (4, "Won the Simon Mannering Medal (Warriors club POTY) in 2024. Co-captain with James Fisher-Harris from 2025. An ACL ended his 2025 season. Released from contract to return to Australia in 2026."),
        (5, "Prop. Warriors co-captain. First Warrior to debut for NSW Origin (2024). Won the club POTY 2024. Released from contract in 2026 to return to Australia for family reasons."),
    ]
),

"Charnze Nicoll-Klokstad": dict(
    era="2023–present", pos="Fullback", jersey="1",
    aliases=["charnze nicoll-klokstad","nicoll-klokstad","charnze","cnk"],
    clues=[
        (1, "His name is Māori — 'Charnze' (pronounced Sharnz) from a family nickname, 'Nicoll' from his father's side. Represents New Zealand internationally. Arrived from Canberra, where he played 88 games."),
        (2, "Received a '9' from Will in Round 3, 2025 — the highest single-game rating given to any Warriors player in the entire 2025 season. The game: a grafting win over the Roosters, 314 metres and two try assists."),
        (3, "Has played the most games at fullback for the Warriors since Roger Tuivasa-Sheck — 57 appearances in the No.1 jersey. Joined from Canberra as part of the 2023 Webster rebuild."),
        (4, "Fullback. Arrived from Canberra Raiders before 2023. Averaged 186.3 running metres per game in 2025 — 11th in the NRL. Reliable and tough, though his attacking ceiling still divides opinion. 'CNK' to the fanbase."),
        (5, "Fullback. 'CNK.' Arrived from Canberra before the 2023 season. One of the club's most durable players — missed barely a game across three seasons. The kind of fullback whose absence is more noticed than his presence."),
    ]
),

"Taine Tuaupiki": dict(
    era="2022–present", pos="Fullback/winger", jersey="1",
    aliases=["taine tuaupiki","tuaupiki","taine"],
    clues=[
        (1, "Won the 2022 Petro Civoniceva Medal — the NSW Cup (reserve grade) player of the year — before earning his first-grade opportunity. An experienced lower-grade five-eighth who converted to fullback."),
        (2, "Scored the match-winning try and conversion in the Warriors' unforgettable Magic Round upset of Penrith in 2024. The sideline conversion to win it — from 40 metres out in the 80th minute — was absurd."),
        (3, "Warriors Club Rookie of the Year in 2023. Has 15 games at fullback for the Warriors — still hasn't nailed down the No.1 jersey permanently despite consistently impressing when called upon."),
        (4, "Fullback and winger. Warriors Rookie of the Year 2023. Fleet of foot, quick of hand. Fills in at fullback and makes it look easy — which it isn't. Still fighting for the starting No.1 spot."),
        (5, "Fullback/winger. Warriors Rookie of the Year 2023. Scored the match-winner in the Warriors' famous Magic Round upset of Penrith in 2024. One of the most exciting young backs at the club."),
    ]
),

"Erin Clark": dict(
    era="2024–present", pos="Lock", jersey="13",
    aliases=["erin clark","clark","erin"],
    clues=[
        (1, "Originally a hooker at the Gold Coast Titans — converted to lock when he joined the Warriors in 2024. His nephew Ali Leiataua has also played for the club, making them one of the Warriors' uncle-nephew combinations."),
        (2, "Averaged 147 metres per game and 34.3 tackles across the 2025 season — career-best numbers Will described as 'not particularly close.' Won the Dally M Lock of the Year and the TWL Player of the Year."),
        (3, "Finished 24th in the 2025 Dally M Medal — one vote from the top 20. Won the TWL POTY (165 points). Was notably overlooked for the official Simon Mannering Medal, which went to Roger Tuivasa-Sheck."),
        (4, "Lock. Joined from Gold Coast in 2024. Originally played as a hooker. Made 24 appearances at lock for the Warriors — already fourth on the all-time list at the position. TWL POTY 2025."),
        (5, "Lock. No.13. TWL Player of the Year 2025. Dally M Lock of the Year 2025. Joined from Gold Coast. Makes 40 tackles look routine — it isn't."),
    ]
),

"Leka Halasima": dict(
    era="2024–present", pos="Back-rower", jersey="11",
    aliases=["leka halasima","halasima","leka"],
    clues=[
        (1, "Scored 13 tries in 2025 — a Warriors record for a forward. Started 13 games on the edge and regularly played 80 minutes. Was still a teenager when the season ended."),
        (2, "His long-range try against Wests Tigers in 2025 and an on-the-buzzer match-winner in Newcastle were among the plays of the Warriors' season. Also demonstrated what Will called 'Nanai-esque ability in the air.'"),
        (3, "Shortlisted for the Dally M Rookie of the Year in 2025 after a 13-try, seven line-break campaign. Warriors Club Rookie of the Year 2025."),
        (4, "Back-rower. Debuted in 2024. 13 tries in 2025 (a Warriors forward record), 87 metres and 24.8 tackles per game average. Averaged 80 minutes across 13 starts. Simply too good to hold back."),
        (5, "Back-rower. 13 tries in 2025 — a club record for a forward. Dally M Rookie of Year nominee. Still a teenager for most of his breakout season. A genuine fan favourite in under 24 months."),
    ]
),

"Dallin Watene-Zelezniak": dict(
    era="2021–present", pos="Winger", jersey="2",
    aliases=["dallin watene-zelezniak","watene-zelezniak","dallin","dwz"],
    clues=[
        (1, "His middle name is Piripi — a Māori version of Philip. His father Phillip also played rugby league. DWZ was originally at Penrith, where he debuted in 2015, before the Panthers sent him to the Warriors in 2021."),
        (2, "Scored 24 tries in the 2023 regular season — a new Warriors record. The previous mark was Francis Meli's 23 in 2003. Also named in the Dally M Team of the Year that season."),
        (3, "Has represented New Zealand internationally. One of only a handful of Warriors players to score 20+ tries in a season. A two-time Warrior — Penrith originally sent him to Auckland, and he's stayed."),
        (4, "Winger. 'DWZ.' Joined from Penrith in 2021. 24 tries in 2023 — a Warriors single-season record. Dally M Team of Year 2023. A cult hero with a flair for the dramatic finish."),
        (5, "Winger. 'DWZ.' Holds the Warriors' single-season tryscoring record — 24 in 2023. A two-time Warrior. One of the most electric players to wear the jersey in the modern era."),
    ]
),

"Tanah Boyd": dict(
    era="2024–present", pos="Halfback", jersey="7",
    aliases=["tanah boyd","boyd","tanah"],
    clues=[
        (1, "Originally from Queensland — played for Ipswich Jets and Brisbane in the Queensland Cup system before joining the Gold Coast Titans, where he spent four seasons before crossing to the Warriors in 2024."),
        (2, "Scored 18 points in 2026 Round 1 — a Warriors season-opener points record. Will gave him 8.5/10 in both Rounds 1 and 2 — the only Warriors halfback in the ratings era to open a season with back-to-back 8.5s."),
        (3, "Stepped in for Luke Metcalf after his ACL injury in 2025 and made the No.7 jersey his own heading into 2026. Had only 15 starts at halfback in NRL before the Warriors handed him the job."),
        (4, "Halfback. Joined from Gold Coast in 2024. Inherited the No.7 jersey when Metcalf's ACL ended his season in 2025. Set a Warriors Round 1 points record in 2026. Averaging 7.70/10 through the first five rounds."),
        (5, "Halfback. Set a Warriors Round 1 points record in 2026 with 18 points. Inherited the starting No.7 spot and refused to give it back."),
    ]
),

"Chanel Harris-Tavita": dict(
    era="2019–present", pos="Five-eighth", jersey="6",
    aliases=["chanel harris-tavita","harris-tavita","chanel","cht"],
    clues=[
        (1, "His father Harris Harris-Tavita played for Western Samoa in the early 1990s. Chanel grew up in South Auckland and came through the Warriors' junior development pathway — a true local product."),
        (2, "Scored eight tries in 2025 — more than double his previous career best in a single season. Also racked up 18 try assists, playing alongside a novice halfback who suffered a season-ending injury midway through."),
        (3, "Won the Warriors Club Rookie of the Year award in 2019. Has played 75 games at halfback or five-eighth across his career — third-most in the club's history. The longest-serving current Warrior as of 2026."),
        (4, "Five-eighth. Local product. Warriors Rookie of Year 2019. Six-plus seasons, multiple positions, multiple coaches. Has played under at least four Warriors head coaches. 'CHT' to literally everyone."),
        (5, "Five-eighth. 'CHT.' The longest-serving current Warrior. Won the Rookie of Year in 2019. Still here — still contributing. Has played under at least four head coaches and outlasted all of them."),
    ]
),

"Addin Fonua-Blake": dict(
    era="2020–2024", pos="Prop", jersey="8",
    aliases=["addin fonua-blake","fonua-blake","addin","afb"],
    clues=[
        (1, "His full name is Addin Fonua-Blake but he often goes by 'AFB.' Born in Auckland, he represented Tonga internationally before later switching to Australian eligibility. Originally joined the NRL through the Manly Sea Eagles."),
        (2, "Two-time Dally M Team of the Year selection (2023, 2024). Won the TWL POTY in 2024 with 170 accumulated points. Left the Warriors after the 2024 season."),
        (3, "Played 81 games at prop for the Warriors — fourth on the all-time list for the position. Arrived from Manly before 2023. Gave the Warriors a middle-third dimension they'd been missing for years."),
        (4, "Prop. 'AFB.' Arrived from Manly for the 2023 season. TWL Player of the Year 2024. Two-time Dally M Team of Year. Departed after 2024. The gap he left was as large as the man."),
        (5, "Prop. 'AFB.' TWL POTY 2024, two-time Dally M Team of Year. Came from Manly, made an enormous impact, left. The Warriors are still trying to replace him."),
    ]
),

"Wayde Egan": dict(
    era="2020–present", pos="Hooker", jersey="9",
    aliases=["wayde egan","egan","wayde"],
    clues=[
        (1, "His father Mick Egan played for the Penrith Panthers in the 1980s and 90s. Wayde himself came through the Penrith system — which is also where his understudy Sam Healey (whose father also played for Cronulla) originated."),
        (2, "Became the first hooker in Warriors history to play 100 games at the position — passing Issac Luke's 78. Now has 105 games at hooker and counting, making him the Warriors' most-capped No.9 ever."),
        (3, "Was a candidate for a NSW State of Origin debut in 2024 after some outstanding performances. Missed four games that season with hip and shoulder problems. Earned seven '8' ratings from Will in the first 12 rounds."),
        (4, "Hooker. Joined from Penrith in 2020. 105 games at hooker — a Warriors record for the position. Seven-plus seasons. Described by Will as 'arguably the club's best-ever hooker.'"),
        (5, "Hooker. Seven-plus seasons at the Warriors. The club's most-capped hooker ever. Workhorse. Never flashy. Described by Will as arguably the club's best ever at the position."),
    ]
),

"Jackson Ford": dict(
    era="2022–present", pos="Prop", jersey="11",
    aliases=["jackson ford","ford","jackson"],
    clues=[
        (1, "Played his 100th NRL game in Round 3, 2026 — against the Roosters. Was averaging 8.17/10 in Will's ratings through the first eight rounds of 2026, tracking as a genuine Dally M Medal contender."),
        (2, "Falls out of favour in 2024 after being an edge back-rower — was moved to prop in the middle rotation and flourished. Career TWL average of 6.84/10 across 32 rated games is consistently the Warriors' best-rated prop."),
        (3, "Originally from Queensland — came through the Redcliffe Dolphins system in the Queensland Cup before joining the NRL. Has represented no Test nations — a genuinely underrated forward."),
        (4, "Prop. Joined the Warriors in 2022 from the Eels. Went from edge back-rower to prop and became a cornerstone. 100th NRL game in Round 3, 2026. One of the Warriors' most consistent performers across four seasons."),
        (5, "Prop. Played his 100th NRL game in 2026. One of the Warriors' most reliable middle forwards across the Webster era. Big, consistent, increasingly difficult to replace."),
    ]
),

"Jazz Tevaga": dict(
    era="2018–2024", pos="Hooker/bench", jersey="14",
    aliases=["jazz tevaga","tevaga","jazz"],
    clues=[
        (1, "Born in Auckland, developed through the Warriors' own junior pathway — one of a handful of players to have come through the system and played 100+ games for the club. Never played for another NRL team."),
        (2, "Won the TWL POTY in 2021 — recognition for years of thankless dummy-half work. Career TWL average of 6.50/10 across 55 rated games — more ratings appearances than any other player in the era."),
        (3, "Has been sin-binned four times in his Warriors career — joint-second behind Marata Niukore (5). In his first ever TWL rating (2018 Round 3), Will wrote he 'defied the sceptics — TWL included' with an outstanding bench display."),
        (4, "Hooker/bench. 55 rated appearances — the most of any player in Will's ratings archive. Local product. Has never played NRL for another club. Seven seasons at the Warriors."),
        (5, "Hooker. 'Jazz.' TWL Player of the Year 2021. Seven seasons at the Warriors — a local product who never played for another NRL club. The ultimate clubman."),
    ]
),

"Adam Pompey": dict(
    era="2020–present", pos="Centre/winger", jersey="3",
    aliases=["adam pompey","pompey","adam","wets"],
    clues=[
        (1, "His nickname 'Wets' comes from his surname — the dry wit of the Warriors' fanbase in full effect. Born in South Auckland, he came through the Warriors' own junior system. 'Virtually a certainty' for 2026 per TWL's pre-season preview."),
        (2, "Scored 11 tries in 2025 — more than double his previous best in a single season. Also chalked up seven try assists. In his sixth season at the club, he finally delivered the output fans had been waiting for."),
        (3, "120 games for the Warriors and counting — one of the longest-serving players at the club. Has averaged 100 metres per game and is now one of the first names in Andrew Webster's backline."),
        (4, "Centre/winger. 'Wets.' Local product. 120+ games. Six-plus seasons. Took until 2025 to properly deliver on his potential — then scored 11 tries and seven assists in a career-best campaign."),
        (5, "Centre. 'Wets.' 120+ games for the Warriors. Local product. Scored 11 tries in his 2025 career-best season. After years of promise, he finally became the player everyone knew he could be."),
    ]
),

"Marata Niukore": dict(
    era="2022–present", pos="Back-rower", jersey="12",
    aliases=["marata niukore","niukore","marata"],
    clues=[
        (1, "Has been sin-binned five times in his Warriors career — more than any other player in the club's history. Originally played for the Parramatta Eels before crossing to the Warriors in 2022."),
        (2, "Represented New Zealand internationally. Has played 50 games at second-row for the Warriors — top-10 at the position in club history. Arrived from Parramatta as part of the Webster rebuild."),
        (3, "Played 32 games across four seasons for the Warriors. A Kiwi international — he is one of 75 New Zealand players to have represented the Warriors at Test level."),
        (4, "Back-rower. Joined from Parramatta in 2022. Has represented New Zealand. 50 second-row appearances for the Warriors. Has been sin-binned more times than any other player in club history — five."),
        (5, "Back-rower. Arrived from Parramatta in 2022. New Zealand international. Five sin-bins — the Warriors' all-time record. Reliable, industrious, occasionally combustible."),
    ]
),

"Luke Metcalf": dict(
    era="2022–present", pos="Halfback", jersey="7",
    aliases=["luke metcalf","metcalf","luke"],
    clues=[
        (1, "Has suffered four serious leg injuries in four consecutive seasons — including two ACLs (the first in 2019, the second in 2025). Only 41 NRL games to his name as of the 2025 season end despite being on the verge of 27."),
        (2, "Had eight tries and nine try assists in 2025 before his ACL injury in Round 15 — leading the Dally M Medal standings at the time of injury. Recommitted to the Warriors until 2028 despite interest from rival clubs."),
        (3, "His father Anthony Metcalf played for the Sharks — Sam Healey's father Mitch also played at Cronulla. The Warriors' 2026 spine has a notable Cronulla connection through its players' fathers."),
        (4, "Halfback. 15 NRL starts at halfback before 2026. Fleet of foot, improving ball-player, reliable in clutch moments. Two ACLs. Warriors until 2028. The club's hopes rest significantly on his durability."),
        (5, "Halfback. Led the Dally M Medal standings with 8 tries and 9 assists before an ACL ended his 2025 season. Recommitted until 2028. If he stays fit, he transforms the Warriors."),
    ]
),

"Demitric Vaimauga": dict(
    era="2024–present", pos="Prop", jersey="16",
    aliases=["demitric vaimauga","vaimauga","demitric","demi"],
    clues=[
        (1, "Made only seven NRL appearances across 2023–24 before becoming a first-choice starter in 2025. Averaged 22 offloads across the season — one of the highest totals for any prop in the NRL. Will described him as having 'all the attributes to become one of the NRL's very best.'"),
        (2, "Averaged 22.6 tackles at over 96 percent efficiency and ran for 68 metres per game in 2025. Only missed one game all season. A 21-year-old Warriors prop who TWL and the wider NRL flagged as a future star."),
        (3, "A local product who developed through the Warriors' lower-grade pathway. His emergence in 2025 was one of the most significant development stories at the club in years."),
        (4, "Prop. Local product. Seven games in 2023–24, then broke out in 2025 with a full season as a regular starter. 22 offloads. A young Warriors forward Will calls a future NRL star."),
        (5, "Prop. Local product. Went from fringe player to first-choice starter in 2025. 22 offloads across the season. One of the most exciting young props in the NRL."),
    ]
),

"Kurt Capewell": dict(
    era="2023–present", pos="Back-rower", jersey="12",
    aliases=["kurt capewell","capewell","kurt"],
    clues=[
        (1, "A three-time NRL grand finalist before joining the Warriors — won with Brisbane in 2023 (as part of the Warriors' opponents in that year's preliminary final) and then crossed to Auckland. His switch felt like a genuine statement."),
        (2, "Has represented Queensland in State of Origin — four times for the Maroons. Was outstanding in the 2025 series as Queensland came from behind to win. One of the few current Warriors with Origin experience."),
        (3, "32 years old entering 2026. Described by Will as 'not the most dynamic forward' but renowned for doing the one-percenters and leading by example. A genuine three-time grand finalist at a club of winners."),
        (4, "Back-rower. Three-time grand finalist. Queensland State of Origin representative (4 games). Joined the Warriors in 2024. A leader, a director, a one-percenter — the glue in a good forward pack."),
        (5, "Back-rower. Three-time NRL grand finalist. Four Queensland State of Origin games. Joined the Warriors in 2024. Brings championship experience the club had been missing."),
    ]
),

"Dylan Walker": dict(
    era="2022–2024", pos="Centre/five-eighth", jersey="6",
    aliases=["dylan walker","walker","dylan"],
    clues=[
        (1, "A NSW State of Origin representative before joining the Warriors — one of the rare Warriors players who had already played Origin before arriving. Played for Manly before crossing to Auckland."),
        (2, "Was sin-binned twice in his Warriors career. Had 19 rated appearances for Will, averaging 7.08/10 — one of the higher averages for any Warriors back across his era."),
        (3, "Played three seasons at the Warriors (2022–24). A NSW representative who played 57 games for Manly before joining. Injuries interrupted what should have been a longer tenure."),
        (4, "Centre/five-eighth. NSW State of Origin rep. Joined from Manly in 2022. Three seasons at the Warriors. 19 rated appearances, averaging 7.08/10 — one of the highest averages for any Warriors back."),
        (5, "Centre/five-eighth. NSW State of Origin representative. Three seasons at the Warriors (2022–24), averaging 7.08/10 in Will's ratings. Injuries cost him — he was better than his Warriors record suggests."),
    ]
),

"Reece Walsh": dict(
    era="2021–2022", pos="Fullback", jersey="1",
    aliases=["reece walsh","walsh","reece","walshy"],
    clues=[
        (1, "Was selected for Queensland State of Origin as a seven-game NRL rookie in 2021 — then withdrew with injury. Became the most points scored by a Warriors rookie (78) in a debut season. Will wrote a column specifically comparing his skill level to the NRL's best."),
        (2, "Scored 9 tries in 2021 as a teenager — the most points by a Warriors rookie in their debut season. Then went back to Queensland, where he played for Brisbane Broncos and later Gold Coast Titans."),
        (3, "Warriors Rookie of the Year 2021. At 19, delivered one of the great Warriors debut seasons — 9 tries, 78 points, selected for Queensland Origin. The one that got away."),
        (4, "Fullback. 'Walshy.' Debuted for the Warriors in 2021 at 19. Warriors Rookie of Year 2021. Went back to Queensland after 2022. Has since become one of the NRL's best fullbacks for Brisbane and Gold Coast."),
        (5, "Fullback. 'Walshy.' Warriors Rookie of the Year 2021. Debuted as a teenager and immediately became a star — then went back to Queensland. The one that got away."),
    ]
),

"Te Maire Martin": dict(
    era="2022–2024", pos="Halfback/hooker", jersey="6",
    aliases=["te maire martin","martin","te maire"],
    clues=[
        (1, "A New Zealand international who played 75 games for the North Queensland Cowboys before joining the Warriors in 2022. His versatility — able to play halfback, five-eighth and hooker — won him favour as a utility."),
        (2, "Played 75 games at halfback/five-eighth for the Cowboys and one at halfback for the Warriors — most of his Warriors career was spent covering hooker and utility roles. A former Cowboys No.7 who never played halfback for the Warriors."),
        (3, "Has represented New Zealand internationally. Three seasons at the Warriors (2022–24). Averaged 6.71/10 in Will's ratings across 19 appearances — solid but rarely spectacular in the glue role he played."),
        (4, "Halfback/hooker. A New Zealand international. Joined from the Cowboys in 2022 — had played 75 games there. Became a utility/hooker cover at the Warriors. Error-free, stout defender, serviceable."),
        (5, "Utility halfback/hooker. New Zealand international. Joined from North Queensland Cowboys in 2022. Three seasons at the Warriors as a reliable do-everything bench option."),
    ]
),

"Kodi Nikorima": dict(
    era="2019–2022", pos="Halfback", jersey="7",
    aliases=["kodi nikorima","nikorima","kodi"],
    clues=[
        (1, "Born in Brisbane, he played 85 games for the Broncos before joining the Warriors in 2019. His brother Brodie also played NRL. Kodi represented Samoa internationally rather than New Zealand or Australia."),
        (2, "Played 47 games at five-eighth and three at halfback for the Warriors — forming a half-and-half combination with Shaun Johnson in 2019. Averaged 6.57/10 in Will's ratings across 15 appearances."),
        (3, "Has been sin-binned once in his Warriors career. Represented Samoa internationally. 85 games for Brisbane before joining the Warriors. Four seasons in Auckland, 2019–2022."),
        (4, "Halfback. 85 games for Brisbane, then 4 seasons at the Warriors (2019–22). Represented Samoa. Most of his Warriors career was spent as backup — 47 at five-eighth, 3 at halfback."),
        (5, "Halfback. Came from Brisbane in 2019. Four seasons at the Warriors. Represented Samoa internationally. A reliable second half-option who stepped in when required."),
    ]
),

"Issac Luke": dict(
    era="2018–2020", pos="Hooker", jersey="9",
    aliases=["issac luke","luke","issac"],
    clues=[
        (1, "Played 78 games at hooker for the Warriors — the second-most in club history, behind Wayde Egan. Is one of the most decorated New Zealand players of his generation — a World Cup winner and multiple-time Test captain."),
        (2, "A Warriors legend who returned to Auckland after playing for the Rabbitohs (where he won a 2014 premiership) and the Dragons. Known for his willingness to run from dummy-half — more than some coaches appreciated."),
        (3, "22 games rated by Will averaging 7.23/10 — one of the higher averages for any Warriors hooker in the ratings era. The Warriors' Rookie of the Year award winner in 1998... wait, wrong Luke — that was Micheal Luck. Issac came later."),
        (4, "Hooker. 78 games for the Warriors — second-most at the position behind Wayde Egan. New Zealand international, World Cup winner, former Rabbitohs and Dragons hooker. Three seasons (2018–20)."),
        (5, "Hooker. A New Zealand legend who returned home to play for the Warriors 2018–20. 78 games — second-most at the position in club history. Loved by fans; more complicated relationship with coaches."),
    ]
),

"Bunty Afoa": dict(
    era="2018–2024", pos="Prop", jersey="15",
    aliases=["bunty afoa","afoa","bunty"],
    clues=[
        (1, "Warriors Rookie of the Year in 2017 — debuted before the ratings era, so his 2017 season isn't in Will's database. Played 43 games across seven seasons in Will's ratings, averaging 6.27/10. A genuine seven-season Warrior."),
        (2, "From Auckland — a local product who played through the Warriors' development system. One of few players to span the Kearney, Brown, Jones and Webster coaching eras at the club."),
        (3, "35 games at prop for the Warriors — 11th on the all-time list for the position. Seven seasons across four different head coaches. Never the headline signing, always in the squad."),
        (4, "Prop. Warriors Rookie of Year 2017. Local product. Seven seasons (2018–24). 35 prop appearances. Spanned four coaching regimes. The quiet constant in the Warriors' front-row rotation."),
        (5, "Prop. Local product. Seven seasons at the Warriors (2018–24). Warriors Rookie of Year 2017. The definition of reliable squad depth — always there, rarely the story."),
    ]
),

"Eliesa Katoa": dict(
    era="2020–2022", pos="Winger/centre", jersey="2",
    aliases=["eliesa katoa","katoa","eliesa"],
    clues=[
        (1, "Represents Tonga internationally — not New Zealand, despite being based in Auckland. Averaged 6.12/10 across 16 rated games for Will. His 16 tries across 16 rated appearances is a remarkable strike rate."),
        (2, "Scored tries in 11 of his 16 rated appearances for Will — a hit rate that would be the envy of most NRL wingers. Three seasons at the Warriors (2020–22) before departing."),
        (3, "A Tongan international winger/centre who gave three seasons of pace and power out wide. Has genuine speed — described as one of the Warriors' better outside-ball threats during his time."),
        (4, "Winger/centre. Tongan international. Three seasons at the Warriors (2020–22). Scored tries in 11 of 16 rated appearances — a brilliant strike rate. Power and pace in equal measure."),
        (5, "Winger/centre. Tongan international. Three seasons at the Warriors (2020–22). One of the more prolific try-scorers per game during his time at the club."),
    ]
),

"Blake Green": dict(
    era="2018–2020", pos="Halfback", jersey="7",
    aliases=["blake green","green","blake"],
    clues=[
        (1, "Formed one of the Warriors' winningest halves combinations — 62.5% wins alongside Shaun Johnson (10 wins, 6 losses). Only the Metcalf-Johnson and Metcalf-CHT pairings have a better win rate."),
        (2, "A former NSW No.7 before joining the Warriors in 2018 — one of a long line of experienced Queensland/NSW halves brought to Auckland. Played 34 games at halfback and 21 at five-eighth."),
        (3, "Has been sin-binned twice in his Warriors career. 20 rated appearances averaging 6.30/10. Three seasons (2018–20) across the Kearney era. Experienced and steady rather than spectacular."),
        (4, "Halfback. Joined in 2018 — part of the return-to-finals season. 55 games at half/five-eighth. 62.5% win rate alongside SJ. A solid rather than spectacular piece of the 2018 puzzle."),
        (5, "Halfback. Three seasons at the Warriors (2018–20). Part of the 2018 team that ended the club's 10-year finals drought. Formed a solid partnership with Shaun Johnson."),
    ]
),

"Bayley Sironen": dict(
    era="2020–2023", pos="Back-rower", jersey="11",
    aliases=["bayley sironen","sironen","bayley"],
    clues=[
        (1, "His father is Paul Sironen — a NSW State of Origin and Australian Test representative who played for Balmain and the Western Reds. Bayley is the son of an NRL great. Has represented Samoa internationally."),
        (2, "Four seasons at the Warriors (2020–23) after joining from Penrith. 15 rated appearances averaging 5.83/10. One of the taller back-rowers at the club — a physical edge option during the transition era."),
        (3, "Represented Samoa internationally — one of 28 Warriors players to have represented Pacific nations rather than Australia or New Zealand. Son of former NSW Origin rep Paul Sironen."),
        (4, "Back-rower. Son of NRL great Paul Sironen. Joined from Penrith in 2020. Four seasons (2020–23). Samoan international. A big edge forward during the Warriors' difficult rebuild years."),
        (5, "Back-rower. Son of NSW Origin legend Paul Sironen. Four seasons at the Warriors (2020–23). A Samoan international who gave the Warriors size and physicality on the edge."),
    ]
),

"Josh Curran": dict(
    era="2020–2023", pos="Back-rower", jersey="12",
    aliases=["josh curran","curran","josh"],
    clues=[
        (1, "A local product who came through the Warriors' development system — played NSW Cup for the Warriors before debuting in 2020. Represented New Zealand (Māori All Stars in 2020 and 2022). An Indigenous All Stars rep as well."),
        (2, "17 rated appearances averaging 6.26/10. Four seasons (2020–23). Won the Warriors' development player award in... actually, Will never confirmed who he modelled his game on. A genuine local back-rower."),
        (3, "A New Zealand representative — played in the Māori All Stars matches in 2020 and 2022. Four seasons at the Warriors as a local product. 12 games as second-rower across his career."),
        (4, "Back-rower. Local product. New Zealand (Māori All Stars) representative. Four seasons (2020–23). Arrived as a local junior and developed into a solid NRL edge forward."),
        (5, "Back-rower. Local product. New Zealand Māori All Stars representative. Four seasons at the Warriors (2020–23). A genuine homegrown talent who gave the club loyal service."),
    ]
),

"Euan Aitken": dict(
    era="2020–2022", pos="Centre", jersey="4",
    aliases=["euan aitken","aitken","euan"],
    clues=[
        (1, "Won the Warriors' club Player of the Year award in 2022 — the Simon Mannering Medal. His previous NRL clubs were St George-Illawarra (where he played 100+ games) and Gold Coast. A well-travelled centre."),
        (2, "10 rated appearances averaging 6.40/10. Three seasons (2020–22). Won the official club POTY in 2022 — while Will's ratings suggested he was solid rather than exceptional. One of those divergences."),
        (3, "A former St George-Illawarra and Gold Coast Titans centre. Three seasons at the Warriors. Won the club's Player of the Year award in 2022. Scottish-born Australian-raised back."),
        (4, "Centre. Scottish-born. Joined from Gold Coast in 2020. Three seasons (2020–22). Won the Warriors club POTY (Simon Mannering Medal) in 2022. Classy, reliable, quietly effective."),
        (5, "Centre. Won the Warriors' club Player of the Year award in 2022. Came from Gold Coast. Three seasons at the Warriors. A smooth, underrated centre who brought class to the club's backline."),
    ]
),

"Ken Maumalo": dict(
    era="2018–2021", pos="Winger", jersey="2",
    aliases=["ken maumalo","maumalo","ken","big ken"],
    clues=[
        (1, "His departure from the Warriors prompted one of the most memorable lines Will has written: 'Built like Ken Maumalo but plays with the background noise presence of Kenny G.' That quote was written about someone else. Ken Maumalo is the original."),
        (2, "Scored 17 tries in 2019 — the most by any Warriors player that season. A powerful winger who averaged 158 metres per game across his best campaigns. 25 rated appearances, averaging 6.54/10."),
        (3, "A New Zealand (Māori All Stars) representative. Known simply as 'Big Ken' by Warriors fans. Four seasons at the Warriors (2018–21) as one of the most physically imposing wingers in the competition."),
        (4, "Winger. 'Big Ken.' Four seasons (2018–21). 17 tries in 2019. Powerful, direct, enormous. A Warriors crowd favourite. Left for the Bulldogs in 2022. The standard by which large Warriors wingers are now measured."),
        (5, "Winger. 'Big Ken.' Four seasons at the Warriors (2018–21). A physically imposing winger who scored 17 tries in 2019. So beloved that Will still invokes his name as a benchmark."),
    ]
),

"Peta Hiku": dict(
    era="2018–2021", pos="Centre/winger", jersey="3",
    aliases=["peta hiku","hiku","peta"],
    clues=[
        (1, "A New Zealand (Māori All Stars) representative and Kiwi international. Originally played for the Manly Sea Eagles before joining the Warriors. His versatility — centre and wing — gave Andrew McFadden and Stephen Kearney squad flexibility."),
        (2, "23 rated appearances averaging 6.54/10. Four seasons (2018–21). One of the more versatile backs across the Kearney era — could cover centre and wing across any given game without notice."),
        (3, "A Kiwi international (New Zealand) and Māori All Stars representative. Joined from Manly. Four seasons at the club (2018–21) as a reliable, versatile backline option."),
        (4, "Centre/winger. Kiwi international. Joined from Manly in 2018. Four seasons. 23 rated games, averaging 6.54/10. One of the more capable backs of the Kearney era."),
        (5, "Centre/winger. A New Zealand international who gave the Warriors four seasons (2018–21) of versatile backline service. Joined from the Manly Sea Eagles."),
    ]
),

"Agnatius Paasi": dict(
    era="2018–2020", pos="Prop", jersey="10",
    aliases=["agnatius paasi","paasi","agnatius"],
    clues=[
        (1, "A Tongan international who has represented Tonga across multiple NRL seasons. Originally played NSW Cup before establishing himself at NRL level. Has 44 games at prop for the Warriors — seventh on the all-time list for the position."),
        (2, "24 rated appearances averaging 6.76/10 — one of the better prop averages in Will's ratings era. Three seasons (2018–20). A consistent, if unspectacular, performer in the Warriors' middle rotation."),
        (3, "A Tongan international. 44 games at prop — top-10 in club history. Three seasons at the Warriors (2018–20). Reliable enough that he appeared in all three seasons without complaint from the coaching staff."),
        (4, "Prop. Tongan international. Three seasons (2018–20). 44 prop appearances — seventh on the all-time list. Averaged 6.76/10 across 24 ratings — respectable for a rotation prop."),
        (5, "Prop. Tongan international. Three seasons at the Warriors (2018–20). One of the more reliable members of the Kearney-era prop rotation."),
    ]
),

"Marcelo Montoya": dict(
    era="2020–2024", pos="Centre/winger", jersey="3",
    aliases=["marcelo montoya","montoya","marcelo"],
    clues=[
        (1, "Received a four-match suspension in 2022 for using a homophobic slur on the field — one of the lengthier recent bans at the club. Has been sin-binned three times in his career. Argentine heritage with the name to match."),
        (2, "42 rated appearances averaging 6.50/10 — the third-highest total of any player in Will's ratings archive. Five seasons (2020–24). A reliable outside back who outlasted multiple coaching regimes."),
        (3, "Five seasons at the Warriors (2020–24). Received a four-game ban for a homophobic slur in 2022. 42 rated appearances — third-most in Will's entire archive. Consistent, occasionally controversial."),
        (4, "Centre/winger. Five seasons (2020–24). 42 rated appearances — third-most in Will's database. Argentine heritage. Four-game suspension in 2022 for a homophobic slur. Outlasted the era he came in with."),
        (5, "Centre/winger. Five seasons at the Warriors (2020–24). Reliable outside back. Argentine heritage. A steady presence across the pre-Webster and early Webster eras."),
    ]
),

"Rocco Berry": dict(
    era="2021–2024", pos="Halfback/five-eighth", jersey="7",
    aliases=["rocco berry","berry","rocco"],
    clues=[
        (1, "Underwent shoulder surgery that was redone in the 2025–26 pre-season, delaying his availability. One of the more injury-plagued players of his generation despite high promise. Has 17 rated appearances averaging just 5.74/10 — one of the lower averages in the ratings era."),
        (2, "A local product who came through the Warriors' pathway. Four seasons (2021–24) at the club, spending most of his time as a backup to the starting halfback. Averaged 5.74/10 — the third-lowest average of any current squad member with 10+ ratings."),
        (3, "Four seasons (2021–24) as a halfback/five-eighth utility. Local product. 17 rated appearances. Injuries have consistently interrupted his development at the Warriors."),
        (4, "Halfback/five-eighth. Local product. Four seasons (2021–24). Has spent most of his Warriors career as a backup. Repeated shoulder surgery has slowed what was an anticipated development curve."),
        (5, "Halfback/five-eighth. Local product. Four seasons at the Warriors as a backup spine player. Injuries have been his biggest obstacle."),
    ]
),

"Adam Blair": dict(
    era="2018–2021", pos="Prop/back-rower", jersey="15",
    aliases=["adam blair","blair","adam"],
    clues=[
        (1, "Played 21 games at lock for the Warriors — part of a late-career move from the edges into the middle. Won the club's Player of the Year award in... actually he never won it. New Zealand Māori All Stars representative. One of the loudest on-field presences in the squad."),
        (2, "A New Zealand international. Joined from Melbourne — where he won the 2012 premiership. 26 rated appearances averaging 6.19/10 across three seasons. Was 34 years old in his last season at the club."),
        (3, "A New Zealand international who has represented the Kiwis across multiple seasons. Also played for Brisbane and Melbourne before joining the Warriors. Four seasons (2018–21) as a veteran presence in the forwards."),
        (4, "Prop/back-rower. New Zealand international. Four seasons (2018–21). Joined from Melbourne, where he won the 2012 premiership. Won the Māori All Stars selection in 2019–20. Vocal, experienced, imposing."),
        (5, "Prop/back-rower. New Zealand international. Four seasons at the Warriors (2018–21). A veteran of Melbourne and Brisbane who brought experience — and volume — to the Warriors' forward pack."),
    ]
),

"Sam Healey": dict(
    era="2024–present", pos="Hooker", jersey="9",
    aliases=["sam healey","healey","sam"],
    clues=[
        (1, "His father Mitch Healey played over 200 NRL games for the Cronulla Sharks — which is the same club Mitch Barnett's father also built his career around. The Warriors' 2026 spine has a Sharks bloodline in two of its players' fathers."),
        (2, "Debuted in 2025 and starred in NSW Cup — played in the grand final and State Championship success. In seven NRL appearances, scored two tries and averaged the kind of elusive running numbers that had Warriors fans excited."),
        (3, "Joined from the Penrith Panthers — the same club as his 2026 teammates James Fisher-Harris (Penrith, 2021–24) and Wayde Egan (development). A genuine Penrith pipeline product."),
        (4, "Hooker. Joined from Penrith. Son of Sharks legend Mitch Healey. Debuted in 2025. Limited NRL games but starred in NSW Cup. Andrew Webster's dilemma: does he back Healey's elusive game or stick with Egan?"),
        (5, "Hooker. Son of former Cronulla Sharks NRL player Mitch Healey. Joined from Penrith. Debuted in 2025 and immediately thrilled fans with his running game from dummy-half."),
    ]
),

"Freddy Lussick": dict(
    era="2022–2024", pos="Hooker", jersey="9",
    aliases=["freddy lussick","lussick","freddy"],
    clues=[
        (1, "His brother Darcy Lussick is a veteran prop who played for multiple NRL clubs — the Lussick name is well-known in Sydney rugby league circles. Freddy is the hooker of the family."),
        (2, "15 rated appearances averaging 5.97/10 — slightly below the 6.0 line. Three seasons (2022–24) as Wayde Egan's main challenger for the Warriors' No.9 jersey. Never quite seized the opportunity."),
        (3, "A former Penrith Panthers hooker who provided genuine competition for Wayde Egan across three seasons. Three seasons (2022–24), 15 rated games. The understudy who didn't quite take the starting spot."),
        (4, "Hooker. Three seasons (2022–24). Joined from Penrith. Provided cover and competition for Wayde Egan. Brother of veteran prop Darcy Lussick. Didn't quite cement a starting spot."),
        (5, "Hooker. Three seasons at the Warriors (2022–24). Joined from Penrith. Provided genuine competition for Wayde Egan — but Egan held the No.9 jersey."),
    ]
),

"Ali Leiataua": dict(
    era="2022–present", pos="Winger/centre", jersey="2",
    aliases=["ali leiataua","leiataua","ali"],
    clues=[
        (1, "His uncle is Ali Lauitiiti — one of the Warriors' most beloved players who won the Dally M Second-rower of the Year in 2002. Ali Leiataua is the nephew of a Warriors legend playing for the same club."),
        (2, "12 rated appearances averaging 6.19/10. Four seasons (2022–present). Son of... wait, nephew of Ali Lauitiiti. A family connection that gives him unique standing in the club's history."),
        (3, "Nephew of Ali Lauitiiti — one of the great Warriors back-rowers. Ali Leiataua is the only current player with a direct family connection to a Dally M award-winner for the club."),
        (4, "Winger/centre. Nephew of Warriors legend Ali Lauitiiti. Four seasons (2022–present). Has 12 rated appearances averaging 6.19/10. Carries the Lauitiiti name with distinction."),
        (5, "Winger/centre. The nephew of Warriors legend Ali Lauitiiti. Four seasons at the club. Carrying on a famous Warriors family name."),
    ]
),

"Jacob Laban": dict(
    era="2022–present", pos="Back-rower", jersey="12",
    aliases=["jacob laban","laban","jacob"],
    clues=[
        (1, "Won the Warriors' club Rookie of the Year award in 2024. From South Auckland — a local product who came through the Warriors' development pathway. 10 rated appearances averaging 5.90/10."),
        (2, "Warriors Rookie of the Year 2024. Four seasons (2022–present). Local product. 10 rated games averaging 5.90/10 — below 6.0, which tells you about the consistency issue he's working to resolve."),
        (3, "A local Auckland product. Warriors Rookie of the Year 2024. Four seasons at the club. Still developing — Will's ratings suggest he hasn't yet found consistent top-level form."),
        (4, "Back-rower. Local product. Warriors Rookie of Year 2024. Four seasons (2022–present). Development player who earned his first-grade opportunities through the Warriors' system."),
        (5, "Back-rower. Local product. Warriors Rookie of the Year 2024. A product of the Warriors' development pathway."),
    ]
),

"Tanner Stowers-Smith": dict(
    era="2023–present", pos="Back-rower", jersey="17",
    aliases=["tanner stowers-smith","stowers-smith","tanner"],
    clues=[
        (1, "His double-barrelled surname makes him one of the more distinctive names on the Warriors' roster. Averaged 6.60/10 across 9 rated appearances. Described by TWL's pre-season preview as part of the Warriors' back-row depth."),
        (2, "9 rated appearances averaging 6.60/10. Three seasons (2023–present). A local product developing through the club's system. Will described him as doing 'a good job with the attributes he possesses.'"),
        (3, "A local product working his way through the Warriors' forward ranks. Three seasons (2023–present). 9 rated appearances. Still finding his level — but 6.60/10 is a respectable average."),
        (4, "Back-rower. Local product. Three seasons (2023–present). 9 rated appearances averaging 6.60/10. Part of the Warriors' developing forward depth."),
        (5, "Back-rower. Local product. Three seasons at the Warriors. Part of the club's developing back-row depth behind the established stars."),
    ]
),

"Edward Kosi": dict(
    era="2021–2024", pos="Winger", jersey="2",
    aliases=["edward kosi","ed kosi","kosi","edward","ed"],
    clues=[
        (1, "The older brother of Ed Kosi — both played for the Warriors, making them one of the club's brother combinations. Edward debuted in 2021, while younger brother Ed joined in 2022. Two brothers on the same wing rotation."),
        (2, "3 rated appearances averaging 5.17/10. Three seasons (2021–24) at the Warriors in a fringe role. The older Kosi brother who gave way to his sibling in the wing rotation."),
        (3, "Older brother of fellow Warrior Ed Kosi. Three seasons (2021–24). Australian-born who represented Samoa internationally. Part of one of the Warriors' brother combinations."),
        (4, "Winger. Older brother of Ed Kosi — both played for the Warriors. Three seasons (2021–24). Australian-born, represented Samoa internationally. Fringe squad member."),
        (5, "Winger. Older brother of Ed Kosi — they both played for the Warriors. Australian-born and represented Samoa internationally."),
    ]
),

"Ed Kosi": dict(
    era="2022–2024", pos="Winger", jersey="2",
    aliases=["ed kosi","kosi","ed","edward kosi"],
    clues=[
        (1, "His older brother Edward Kosi also played for the Warriors — both were in the squad together for periods. Ed is the more-rated of the two: 10 appearances averaging 6.50/10 versus Edward's 5.17/10."),
        (2, "10 rated appearances averaging 6.50/10. Three seasons (2022–24). Australian-born winger who represented Samoa internationally. The younger of two Kosi brothers to play for the Warriors."),
        (3, "Australian-born but represented Samoa internationally. Part of a brother combination at the club with Edward Kosi. 10 rated appearances in three seasons — better rated than his older sibling."),
        (4, "Winger. Younger brother of Edward Kosi — both played for the Warriors. Australian-born, represented Samoa. Three seasons (2022–24). Averaged 6.50/10 in 10 rated games."),
        (5, "Winger. One of two Kosi brothers to play for the Warriors. Australian-born, represented Samoa. Three seasons (2022–24)."),
    ]
),

"Viliami Vailea": dict(
    era="2021–2023", pos="Winger", jersey="2",
    aliases=["viliami vailea","vailea","viliami"],
    clues=[
        (1, "His cousin Viliame Vailea also played for the Warriors in 2022–23 — two cousins with the same surname on the same wing rotation. The 'i' versus 'e' difference in first names is how you tell them apart."),
        (2, "Warriors Rookie of the Year in 2022. Three seasons (2021–23) at the club. 8 rated appearances averaging 5.75/10. The first-named of the two Vailea cousins at the Warriors."),
        (3, "Won the Warriors' Rookie of the Year award in 2022. His cousin Viliame Vailea also played for the club — same surname, different first name. Three seasons (2021–23)."),
        (4, "Winger. Warriors Rookie of Year 2022. Three seasons (2021–23). Cousin of Viliame Vailea — both played for the Warriors simultaneously. An eye-catching rookie season led to the award."),
        (5, "Winger. Warriors Rookie of the Year 2022. His cousin Viliame Vailea also played for the club — same surname, different spelling. Three seasons (2021–23)."),
    ]
),

"Alofiana Khan-Pereira": dict(
    era="2026–present", pos="Winger", jersey="5",
    aliases=["alofiana khan-pereira","khan-pereira","alofiana","akp"],
    clues=[
        (1, "Scored 53 tries in 54 NRL games for the Gold Coast Titans since debuting in 2023 — a strike rate that is extraordinary. Contender for the fastest player in the NRL and possibly the quickest Warrior ever."),
        (2, "24 tries in 21 Titans appearances in 2024 — the most by any player in the NRL that season. Then fell out of favour under Des Hasler in 2025, playing just 10 games. Still scored nine tries."),
        (3, "Joined the Warriors from Gold Coast for 2026 with 53 tries in 54 games. Listed as a potential defensive liability — but with that tryscoring strike rate, it's hard to care. 'AKP' to the TWL community."),
        (4, "Winger. 'AKP.' Joined from Gold Coast in 2026. 53 tries in 54 NRL games — one of the highest strike rates in the competition. Fast. Very fast. Potential defensive liability. Undeniable tryline threat."),
        (5, "Winger. 'AKP.' Joined from Gold Coast in 2026. Scored 53 tries in 54 career NRL games before joining the Warriors. Potentially the fastest Warrior ever."),
    ]
),

"Morgan Gannon": dict(
    era="2026–present", pos="Back-rower", jersey="17",
    aliases=["morgan gannon","gannon","morgan"],
    clues=[
        (1, "Has zero competitive rated appearances in Will's ratings system as of the time of writing — a 2026 squad member yet to earn a rating in a competitive match. Part of the Warriors' young developing forward depth."),
        (2, "A young forward who earned selection in the 2026 squad through the Warriors' development pathway. Yet to accumulate a competitive Will Evans rating — his rating debut is still to come."),
        (3, "Part of the Warriors' 2026 squad as a developing young forward. No competitive ratings yet from Will. A player the club expects to grow into a first-grade contributor."),
        (4, "Back-rower. Part of the 2026 Warriors squad. A young developing forward from the Warriors' pathway. Yet to earn a competitive game rating from Will Evans."),
        (5, "Back-rower. Part of the 2026 Warriors squad. A young forward working his way through the club's development system."),
    ]
),

"Isaiah Vagana": dict(
    era="2022", pos="Prop", jersey="10",
    aliases=["isaiah vagana","vagana","isaiah"],
    clues=[
        (1, "His father Joe Vagana is a Warriors legend — 82 games at prop, one of the most celebrated players of the club's early years. Isaiah is the son of a Warriors great following in his footsteps. One NRL game in 2022."),
        (2, "One rated appearance (2022) — 5.5/10 from Will. Son of Joe Vagana, who played 82 prop games for the Warriors and was one of the most dominant front-rowers in the club's early seasons."),
        (3, "Son of Warriors legend Joe Vagana. Had one NRL appearance in 2022. Following his father's footsteps into a Warriors jersey — albeit for a single game."),
        (4, "Prop. Son of Warriors legend Joe Vagana (82 games at prop). One NRL appearance in 2022. A famous name in a Warriors jersey for one game."),
        (5, "Prop. Son of Warriors legend Joe Vagana. Played one NRL game for the Warriors in 2022. A famous Warriors surname making a brief appearance."),
    ]
),

"Reece Walsh": dict(
    era="2021–2022", pos="Fullback", jersey="1",
    aliases=["reece walsh","walsh","reece","walshy"],
    clues=[
        (1, "Was selected for Queensland State of Origin as a seven-game NRL rookie in 2021 — then withdrew with injury. Became the Warriors' record holder for most points by a rookie in a debut season."),
        (2, "Scored 9 tries and 78 points in 2021 as a 19-year-old debutant — the most points by any Warriors rookie in their debut season. The previous record had stood for years."),
        (3, "Warriors Rookie of the Year 2021. Debuted at 19, became a Queensland Origin selection in his first season. Two seasons (2021–22) at the Warriors before returning to Queensland. Now one of the NRL's best fullbacks."),
        (4, "Fullback. 'Walshy.' Warriors Rookie of Year 2021. 9 tries and 78 points as a 19-year-old rookie. Two seasons at the Warriors, then left for Queensland — Brisbane and later Gold Coast."),
        (5, "Fullback. 'Walshy.' Warriors Rookie of the Year 2021. Left for Queensland after 2022. Now one of the NRL's best fullbacks. The one that got away."),
    ]
),

"Kodi Nikorima": dict(
    era="2019–2022", pos="Halfback/five-eighth", jersey="7",
    aliases=["kodi nikorima","nikorima","kodi"],
    clues=[
        (1, "Born in Brisbane and played 85 games for the Broncos before joining the Warriors in 2019. His brother Brodie also played NRL. Represented Samoa rather than New Zealand or Australia — an interesting eligibility choice given his Queensland roots."),
        (2, "15 rated appearances averaging 6.57/10 across four seasons (2019–22). Played 47 games at five-eighth and 3 at halfback for the Warriors. Formed a combination with Shaun Johnson in 2019."),
        (3, "85 games for Brisbane before crossing to the Warriors. Represented Samoa. Four seasons (2019–22). Half and five-eighth. Averaged 6.57/10 across 15 Will ratings."),
        (4, "Halfback/five-eighth. 85 Brisbane games before joining in 2019. Represented Samoa internationally. Four seasons at the Warriors. A Queensland-born Samoan international."),
        (5, "Halfback/five-eighth. Came from Brisbane in 2019 after 85 NRL games. Represented Samoa. Four seasons at the Warriors (2019–22)."),
    ]
),

}

# Dump to check coverage
have = set(PLAYERS.keys())
print(f"Players defined: {len(have)}")
import json
with open('/home/claude/warriors_who_am_i_v3.json') as f:
    db_data = json.load(f)
db_players = set(x['name'] for x in db_data if x['type'] == 'player')
print(f"Players in DB: {len(db_players)}")
missing = db_players - have
print(f"Not yet rewritten ({len(missing)}):")
for n in sorted(missing):
    p = next(x for x in db_data if x['name'] == n and x['type'] == 'player')
    print(f"  {n}: rated={p['games_rated']}, seasons={p['seasons']}")

# Remaining 62 players — shorter eras, less data
PLAYERS.update({

"Aaron Pene": dict(era="2022", pos="Back-rower", jersey="12", aliases=["aaron pene","pene","aaron"],
    clues=[(1,"A local Auckland product who came through the Warriors' development system. Five rated appearances in 2022 averaging 5.30/10 — Will's assessment of his debut season."),
           (2,"5 rated games in 2022, averaging 5.30/10. A fringe back-rower who got opportunities in 2022 but couldn't hold a spot."),
           (3,"A Warriors development player who made his NRL debut in 2022. Local product from Auckland."),
           (4,"Back-rower. Local product. One NRL season (2022) — 5 rated appearances, averaging 5.30/10."),
           (5,"Back-rower. Local Auckland product. Debuted in 2022. A fringe Warrior who came through the club's development pathway.")]),

"Adam Keighran": dict(era="2019–2020", pos="Five-eighth", jersey="6", aliases=["adam keighran","keighran","adam"],
    clues=[(1,"Never rated by Will in a competitive game — two seasons at the Warriors (2019–20) without a single rated appearance in a competition match. Trial-only presence."),
           (2,"Two seasons at the club (2019–20) as a utility back. Came from the Penrith system. Zero competitive rated appearances in Will's database."),
           (3,"A Queensland-born utility back who spent two seasons at the Warriors without cementing a regular spot. Appeared only in trials."),
           (4,"Five-eighth. Joined from Penrith. Two seasons (2019–20) as a squad member. Never quite broke into regular first-grade action."),
           (5,"Five-eighth. Two seasons at the Warriors (2019–20). A backup spine player who came from the Penrith system.")]),

"Albert Vete": dict(era="2018", pos="Prop", jersey="10", aliases=["albert vete","vete","albert"],
    clues=[(1,"One NRL game in 2018 — one rated appearance, 6.5/10 from Will. A Samoan international prop who had a single-game Warriors stint in the Kearney era's first year."),
           (2,"One rated appearance in 2018, 6.5/10. A Samoan international prop. Brief Warriors stint — then moved on."),
           (3,"A Samoan international who played one game for the Warriors in 2018. A single-game Warrior."),
           (4,"Prop. Samoan international. One Warriors game in 2018. Came and went — but left Will with enough to rate him."),
           (5,"Prop. One Warriors game (2018). A Samoan international prop. The definition of a brief stint.")]),

"Anthony Gelling": dict(era="2018–2019", pos="Centre/wing", jersey="4", aliases=["anthony gelling","gelling","anthony"],
    clues=[(1,"Came to the Warriors from Wigan Warriors in Super League — a dual-code transfer across hemispheres. A New Zealand international centre who brought British rugby league experience to Auckland in 2018."),
           (2,"One rated appearance averaging 5.5/10. Two seasons (2018–19) at the club. A centre/winger known for his pace in British rugby league."),
           (3,"A New Zealand international who played Super League for Wigan before joining the Warriors. Two seasons (2018–19)."),
           (4,"Centre/winger. Joined from Wigan Warriors (Super League) in 2018. New Zealand international. Two seasons, limited first-grade opportunities."),
           (5,"Centre/winger. Came from Wigan (Super League) in 2018. A New Zealand international who had two seasons at the Warriors.")]),

"Ash Taylor": dict(era="2022", pos="Halfback", jersey="7", aliases=["ash taylor","taylor","ash"],
    clues=[(1,"A former Gold Coast Titans and Brisbane Broncos halfback who had a brief stint at the Warriors in 2022. One of the higher-profile halves who didn't quite stick — one rated appearance, 5.5/10."),
           (2,"One rated appearance in 2022, 5.5/10. A former Dally M Medal contender at Gold Coast who joined the Warriors for one season as a backup half."),
           (3,"Joined from the Eels (previously Gold Coast and Brisbane) for one season in 2022. A former top-line NRL halfback who came to the Warriors as a backup."),
           (4,"Halfback. Former Gold Coast and Brisbane half. One season at the Warriors (2022). One of the more recognisable names to pass through without making a major impact."),
           (5,"Halfback. Former Gold Coast Titans and Brisbane Broncos playmaker. One season at the Warriors (2022).")]),

"Ben Farr": dict(era="2022–2023", pos="Winger", jersey="2", aliases=["ben farr","farr","ben"],
    clues=[(1,"One rated appearance averaging 5.5/10. Two seasons (2022–23) in and out of the top squad. A young winger who came through the Warriors' pathway without quite cementing regular first-grade exposure."),
           (2,"Two seasons (2022–23) at the Warriors. Limited NRL exposure. A young winger still developing his game at the time."),
           (3,"A Warriors development player who got limited top-grade opportunities across two seasons. Local product."),
           (4,"Winger. Two seasons (2022–23) at the Warriors. A young fringe player still developing at the time."),
           (5,"Winger. Two seasons at the Warriors (2022–23). A young winger developing through the club's system.")]),

"Ben Murdoch-Masila": dict(era="2020–2022", pos="Prop", jersey="10", aliases=["ben murdoch-masila","murdoch-masila","ben"],
    clues=[(1,"A Samoan international prop who previously played for Warrington Wolves in Super League — came to the Warriors with British rugby league experience. 8 rated appearances averaging 6.12/10."),
           (2,"8 rated appearances averaging 6.12/10. Three seasons (2020–22). A powerful, Samoan international prop who had played Super League before coming to Auckland."),
           (3,"Samoan international. Former Warrington Wolves (Super League) prop. Three seasons at the Warriors (2020–22). Brought British rugby league experience."),
           (4,"Prop. Samoan international. Played Super League for Warrington before joining the Warriors in 2020. Three seasons. A powerful middle forward with a UK pedigree."),
           (5,"Prop. Samoan international. Came from Super League (Warrington Wolves) for three seasons at the Warriors (2020–22).")]),

"Blake Ayshford": dict(era="2019–2020", pos="Winger", jersey="2", aliases=["blake ayshford","ayshford","blake"],
    clues=[(1,"A local Auckland winger who came through the Warriors' development system. One rated appearance (5.5/10) across two seasons (2019–20). Limited first-grade opportunity."),
           (2,"One rated appearance in 2019–20 averaging 5.5/10. A local winger who got limited exposure at NRL level."),
           (3,"A local Auckland product. Two seasons (2019–20) in the Warriors' squad with limited top-grade opportunities."),
           (4,"Winger. Local product. Two seasons (2019–20) at the Warriors. One rated NRL appearance — 5.5/10."),
           (5,"Winger. Local Auckland product. Two seasons at the Warriors (2019–20). Limited top-grade opportunities.")]),

"Brayden Wiliame": dict(era="2022", pos="Winger", jersey="2", aliases=["brayden wiliame","wiliame","brayden"],
    clues=[(1,"A Fijian international winger who played for Toulouse in the French Elite One competition before joining the Warriors. 3 rated appearances averaging 6.83/10 — solid for a one-season stint."),
           (2,"3 rated appearances averaging 6.83/10. One season (2022). A Fijian international who'd played in France before coming to the Warriors."),
           (3,"Fijian international winger. Came from the French competition before joining the Warriors for 2022. Three rated appearances — decent enough averages."),
           (4,"Winger. Fijian international. One season at the Warriors (2022). Came from French rugby league. 3 rated games averaging 6.83/10."),
           (5,"Winger. Fijian international. One season at the Warriors (2022), having previously played in France.")]),

"Chad Townsend": dict(era="2021", pos="Halfback", jersey="7", aliases=["chad townsend","townsend","chad"],
    clues=[(1,"A veteran Queensland halfback who joined the Warriors for one season in 2021 after 100+ games for Cronulla. He scored a hat-trick in Round 23, 2021 — one of the unexpected highlights of a difficult season."),
           (2,"4 rated appearances averaging 6.25/10. Scored a hat-trick in Round 23, 2021. A veteran Cronulla half who gave the Warriors one season of experienced spine leadership."),
           (3,"Over 100 NRL games for Cronulla Sharks before joining the Warriors for 2021. One season. Scored a hat-trick for the club. Left after one year."),
           (4,"Halfback. 100+ games for Cronulla before joining for 2021. Scored a hat-trick in Round 23. A veteran who gave one season of experienced leadership."),
           (5,"Halfback. Veteran Cronulla Sharks half. One season at the Warriors (2021). Scored a hat-trick in Round 23.")]),

"Chris Satae": dict(era="2018–2019", pos="Prop", jersey="10", aliases=["chris satae","satae","chris"],
    clues=[(1,"A Samoan international prop who came through the Sydney system. 5 rated appearances averaging 6.10/10 across two seasons. A rotation prop in the Kearney era's first two years."),
           (2,"5 rated games averaging 6.10/10. Two seasons (2018–19). A Samoan international prop in the Warriors' early Kearney-era rotation."),
           (3,"Samoan international. Two seasons at the Warriors (2018–19). A rotation prop who came through Sydney club ranks."),
           (4,"Prop. Samoan international. Two seasons (2018–19) as a rotation forward in the Warriors' middle."),
           (5,"Prop. Samoan international. Two seasons at the Warriors (2018–19). Part of the Kearney-era prop rotation.")]),

"Daejarn Asi": dict(era="2022", pos="Centre/wing", jersey="3", aliases=["daejarn asi","asi","daejarn"],
    clues=[(1,"2 rated appearances averaging 5.5/10. One season (2022). A local Auckland back who had a brief run in the Warriors' first-grade squad."),
           (2,"Two NRL appearances in 2022, averaging 5.5/10. A local product who got his chance in a difficult season for the Warriors."),
           (3,"A local Auckland product. One NRL season (2022) with two rated appearances."),
           (4,"Centre/wing. Local product. One season at the Warriors (2022). Two rated appearances in the top grade."),
           (5,"Centre/wing. Local product. Two NRL appearances for the Warriors in 2022.")]),

"Daniel Alvaro": dict(era="2020", pos="Prop", jersey="10", aliases=["daniel alvaro","alvaro","daniel"],
    clues=[(1,"A Lebanese-Australian international prop who had played for Parramatta before joining the Warriors for the COVID 2020 season. 5 rated appearances averaging 6.30/10."),
           (2,"5 rated appearances averaging 6.30/10. One season (2020) — the COVID season in Australia. A Lebanese international who'd played for Parramatta."),
           (3,"Lebanese international. Joined from Parramatta for the 2020 COVID season. Five rated appearances in one season."),
           (4,"Prop. Lebanese international. Former Parramatta Eels. One COVID season at the Warriors (2020). Five rated appearances averaging 6.30/10."),
           (5,"Prop. Lebanese international. One season at the Warriors during the 2020 COVID year. Previously at Parramatta.")]),

"Demitric Sifakula": dict(era="2022–2024", pos="Back-rower", jersey="12", aliases=["demitric sifakula","sifakula","demitric"],
    clues=[(1,"3 rated appearances averaging 4.50/10 — one of the lower averages in the database. A local forward who developed through the Warriors' system across three seasons (2022–24)."),
           (2,"Three seasons (2022–24) at the Warriors, 3 rated appearances averaging 4.50/10. A fringe back-rower still developing his game."),
           (3,"A local Auckland product. Three seasons (2022–24). Limited top-grade exposure, with Will's ratings averaging 4.50/10 — below par."),
           (4,"Back-rower. Local product. Three seasons (2022–24). 3 rated appearances averaging 4.50/10. Still developing his NRL game."),
           (5,"Back-rower. Local product. Three seasons at the Warriors (2022–24). A developing young forward from the club's system.")]),

"Dunamis Lui": dict(era="2022", pos="Back-rower", jersey="12", aliases=["dunamis lui","lui","dunamis"],
    clues=[(1,"A Queensland Origin representative (for Queensland) before joining the Warriors — one of the few players to have played State of Origin prior to their Warriors stint. One season (2022), one rated appearance, 6.5/10."),
           (2,"A former Queensland State of Origin player who spent one season at the Warriors in 2022. One rated appearance, 6.5/10. A recognisable Queensland name at the Warriors."),
           (3,"Queensland State of Origin representative. One season at the Warriors (2022). Came with an impressive rep pedigree."),
           (4,"Back-rower. Queensland Origin rep. One season at the Warriors (2022). A big-name recruit who had only one rated appearance."),
           (5,"Back-rower. Queensland State of Origin representative. One season at the Warriors (2022). A veteran of the Origin arena.")]),

"Eddie Ieremia-Toeava": dict(era="2023–2024", pos="Winger", jersey="2", aliases=["eddie ieremia-toeava","ieremia-toeava","eddie"],
    clues=[(1,"His double-barrelled surname reflects both Samoan (Ieremia) and Tokelauan (Toeava) heritage. A local Auckland winger who developed through the Warriors' pathway. 2 rated appearances averaging 7.0/10 — decent when used."),
           (2,"2 rated appearances averaging 7.0/10. Two seasons (2023–24) as a squad member. Local product with Samoan and Tokelauan heritage."),
           (3,"A local Auckland winger with Samoan and Tokelauan heritage. Two seasons (2023–24) at the Warriors with limited first-grade exposure."),
           (4,"Winger. Local product. Two seasons (2023–24). Samoan and Tokelauan heritage. 2 rated appearances averaging 7.0/10 — performed when selected."),
           (5,"Winger. Local product. Two seasons at the Warriors (2023–24). A promising young winger from the club's development pathway.")]),

"Eiden Ackland": dict(era="2022", pos="Winger", jersey="2", aliases=["eiden ackland","ackland","eiden"],
    clues=[(1,"Made his NRL debut for the Warriors in 2022. A local young winger who got one opportunity in a difficult Warriors season. One rated appearance, 6.5/10."),
           (2,"One rated appearance (6.5/10) in 2022. A local winger making his NRL debut. Brief Warriors exposure."),
           (3,"A local Auckland product who made his NRL debut in 2022. One Warriors season."),
           (4,"Winger. Local product. NRL debut with the Warriors in 2022. One rated appearance, 6.5/10."),
           (5,"Winger. Local product. Made his NRL debut with the Warriors in 2022.")]),

"Etuake Fukofuka": dict(era="2023", pos="Back-rower", jersey="12", aliases=["etuake fukofuka","fukofuka","etuake"],
    clues=[(1,"Never rated by Will in a competitive match — a 2023 squad member without a competitive rated appearance. Zero NRL competitive ratings despite being in the Warriors' top squad."),
           (2,"Zero competitive rated appearances despite being part of the 2023 squad. A development player who was in the squad but didn't earn a Will Evans competitive rating."),
           (3,"A development forward in the 2023 Warriors squad. No competitive rated appearances — squad depth without top-grade minutes."),
           (4,"Back-rower. 2023 Warriors squad member. Zero competitive rated appearances. A developing forward in the top squad."),
           (5,"Back-rower. Part of the 2023 Warriors squad without earning competitive first-grade minutes that season.")]),

"George Jennings": dict(era="2020", pos="Winger", jersey="2", aliases=["george jennings","jennings","george"],
    clues=[(1,"A former Brisbane Broncos winger who joined the Warriors for the 2020 COVID season in Australia. 2 rated appearances averaging 5.5/10. His Brisbane background made him a recognisable name."),
           (2,"2 rated appearances averaging 5.5/10. One season (2020) — the COVID year in Australia. A former Brisbane Broncos winger."),
           (3,"Former Brisbane Broncos winger. One COVID season at the Warriors (2020). Two rated appearances."),
           (4,"Winger. Former Brisbane Broncos. One COVID season at the Warriors (2020). 2 rated appearances, 5.5/10 average."),
           (5,"Winger. Former Brisbane Broncos. One season at the Warriors during the 2020 COVID year.")]),

"Gerard Beale": dict(era="2018–2020", pos="Centre/wing", jersey="3", aliases=["gerard beale","beale","gerard"],
    clues=[(1,"A New Zealand (Māori All Stars) representative who played for St George-Illawarra before joining the Warriors. 9 rated appearances averaging 6.28/10. Three seasons (2018–20) as a versatile back."),
           (2,"9 rated games averaging 6.28/10. Three seasons (2018–20). A Māori All Stars representative who came from St George-Illawarra."),
           (3,"New Zealand Māori All Stars representative. Joined from St George-Illawarra. Three seasons (2018–20). A versatile back who could cover centre and wing."),
           (4,"Centre/wing. Māori All Stars representative. Joined from St George-Illawarra in 2018. Three seasons. Versatile and reliable — a useful squad member."),
           (5,"Centre/wing. Māori All Stars representative. Three seasons at the Warriors (2018–20). Joined from St George-Illawarra.")]),

"Geronimo Doyle": dict(era="2023", pos="Utility back", jersey="6", aliases=["geronimo doyle","doyle","geronimo"],
    clues=[(1,"Zero competitive rated appearances — had one trial appearance in 2023 that Will rated 4.5/10, the lowest trial rating on record. His trial rating stands as the worst Will has given in a non-competitive game."),
           (2,"One trial appearance rated 4.5/10 by Will in 2023 — the lowest trial rating on record. Zero competitive appearances."),
           (3,"A 2023 Warriors trialist who received Will's lowest-ever trial rating: 4.5/10. Did not convert to a first-grade start."),
           (4,"Utility back. 2023 Warriors trial. Received the lowest trial rating (4.5/10) in Will's records. Did not play competitive first-grade for the Warriors."),
           (5,"Utility back. Appeared in a 2023 Warriors trial. Did not make the competitive squad.")]),

"Hayze Perham": dict(era="2019–2020", pos="Winger", jersey="2", aliases=["hayze perham","perham","hayze"],
    clues=[(1,"3 rated appearances averaging 6.17/10. Two seasons (2019–20) as a young local winger in the Warriors' development pathway. Limited top-grade exposure."),
           (2,"3 rated games averaging 6.17/10. Two seasons (2019–20) in the Warriors' squad."),
           (3,"A local Auckland winger. Two seasons (2019–20) at the Warriors with limited first-grade exposure."),
           (4,"Winger. Local product. Two seasons (2019–20). 3 rated appearances averaging 6.17/10."),
           (5,"Winger. Local product. Two seasons at the Warriors (2019–20).")]),

"Jack Hetherington": dict(era="2020", pos="Prop", jersey="10", aliases=["jack hetherington","hetherington","jack"],
    clues=[(1,"Received a four-game suspension in 2020 for a high tackle — the longest ban of any Warriors player in recent seasons alongside Charlie Gubb and Marcelo Montoya. A NSW-born prop from the Sydney system. 2 rated appearances, 6.5/10."),
           (2,"Received one of the Warriors' longer recent suspensions — four games in 2020 for a high tackle. 2 rated appearances averaging 6.5/10 in the COVID season."),
           (3,"NSW-born prop. One COVID season at the Warriors (2020). Four-game suspension for a high tackle. 2 rated appearances."),
           (4,"Prop. NSW-born. One COVID season (2020). Received a four-game ban for a high tackle — one of the club's longer recent suspensions."),
           (5,"Prop. NSW-born. One season at the Warriors during the 2020 COVID year. Received a four-game suspension that season.")]),

"Jack Murchie": dict(era="2020–2022", pos="Back-rower", jersey="12", aliases=["jack murchie","murchie","jack"],
    clues=[(1,"A local Auckland back-rower who came through the Warriors' development system. 12 rated appearances averaging 5.67/10 — below par. Three seasons (2020–22) as fringe edge forward."),
           (2,"12 rated appearances averaging 5.67/10. Three seasons (2020–22). A local product who couldn't quite hold a spot despite consistent squad selection."),
           (3,"Local Auckland product. Three seasons (2020–22). 12 rated games — the most among lesser-known Warriors backs of his era."),
           (4,"Back-rower. Local product. Three seasons (2020–22). 12 rated appearances averaging 5.67/10. Consistent squad selection, inconsistent ratings."),
           (5,"Back-rower. Local product. Three seasons at the Warriors (2020–22). A fringe edge forward from the club's development pathway.")]),

"Jackson Frei": dict(era="2021–2022", pos="Prop", jersey="10", aliases=["jackson frei","frei","jackson"],
    clues=[(1,"One rated appearance (5.5/10) across two seasons (2021–22). A local prop who got limited NRL exposure during the Warriors' difficult transition period."),
           (2,"Two seasons (2021–22) in the Warriors' squad. One rated appearance, 5.5/10. A fringe prop who came through the Warriors' system."),
           (3,"A local prop. Two seasons (2021–22) with one NRL appearance. Development player in a tough era."),
           (4,"Prop. Local product. Two seasons (2021–22). One rated appearance — 5.5/10 from Will."),
           (5,"Prop. Local product. Two seasons at the Warriors (2021–22).")]),

"Jamayne Taunoa-Brown": dict(era="2020–2021", pos="Winger", jersey="2", aliases=["jamayne taunoa-brown","taunoa-brown","jamayne"],
    clues=[(1,"Warriors Rookie of the Year 2020 — a significant honour in a COVID-disrupted season played entirely in Australia. 11 rated appearances averaging 6.50/10 across two seasons."),
           (2,"Won the Warriors Rookie of the Year award in 2020. Two seasons (2020–21). 11 rated appearances averaging 6.5/10. A powerful winger who earned his opportunity."),
           (3,"Warriors Rookie of Year 2020 (awarded during the COVID season in Australia). Two seasons, 11 rated appearances. An Indigenous All Stars representative."),
           (4,"Winger. Warriors Rookie of Year 2020. Two seasons (2020–21). Indigenous All Stars representative. 11 rated appearances averaging 6.5/10."),
           (5,"Winger. Warriors Rookie of the Year 2020. Two seasons at the Warriors (2020–21). Won his award during the COVID season played entirely in Australia.")]),

"James Gavet": dict(era="2018–2019", pos="Prop", jersey="10", aliases=["james gavet","gavet","james"],
    clues=[(1,"A New Zealand-born prop who played for Melbourne Storm before joining the Warriors in 2018. 8 rated appearances averaging 6.38/10. Two seasons (2018–19) in the Kearney era."),
           (2,"8 rated appearances averaging 6.38/10. Two seasons (2018–19). Former Melbourne Storm prop who joined for the Kearney era."),
           (3,"Former Melbourne Storm prop. Two seasons at the Warriors (2018–19). 8 rated games — solid middle rotation across both Kearney seasons."),
           (4,"Prop. Former Melbourne Storm. Two seasons (2018–19). 8 rated appearances averaging 6.38/10. Reliable Kearney-era front-row addition."),
           (5,"Prop. Former Melbourne Storm. Two seasons at the Warriors (2018–19) as a middle-rotation prop.")]),

"Jesse Arthars": dict(era="2022", pos="Winger", jersey="2", aliases=["jesse arthars","arthars","jesse"],
    clues=[(1,"A former Brisbane Broncos winger who had a one-season stint at the Warriors in 2022. 5 rated appearances averaging 5.70/10. Quick and direct, with limited consistency."),
           (2,"5 rated appearances averaging 5.70/10. One season (2022). Former Brisbane Broncos winger. Promising pace but couldn't hold a spot."),
           (3,"Former Brisbane Broncos winger. One season at the Warriors (2022). Five rated appearances — below Will's preferred average."),
           (4,"Winger. Former Brisbane Broncos. One season (2022). Five rated games averaging 5.70/10. Fast but inconsistent."),
           (5,"Winger. Former Brisbane Broncos. One season at the Warriors (2022).")]),

"Joseph Vuna": dict(era="2018–2019", pos="Winger", jersey="2", aliases=["joseph vuna","vuna","joseph"],
    clues=[(1,"His uncle is Cooper Vuna — a dual international (rugby union and league) who played for Australia. Joseph is the nephew of a dual international, playing on the Warriors' wing across two seasons (2018–19)."),
           (2,"4 rated appearances. Two seasons (2018–19) as a squad winger. Nephew of Cooper Vuna, who represented Australia in both codes."),
           (3,"Nephew of dual international Cooper Vuna (Australia, rugby union and league). Two seasons at the Warriors (2018–19) as a squad winger."),
           (4,"Winger. Nephew of dual international Cooper Vuna. Two seasons (2018–19) at the Warriors. Four rated appearances."),
           (5,"Winger. Nephew of dual international Cooper Vuna. Two seasons at the Warriors (2018–19).")]),

"Kalani Going": dict(era="2022–2023", pos="Halfback", jersey="7", aliases=["kalani going","going","kalani"],
    clues=[(1,"A New Zealand-born halfback who came through the Warriors' junior pathway. One rated appearance (6.5/10) across two seasons (2022–23). Limited first-grade opportunity."),
           (2,"One rated appearance (6.5/10) across two seasons (2022–23). A local halfback who got limited top-grade exposure."),
           (3,"A local product — New Zealand-born halfback. Two seasons (2022–23) in the squad with limited top-grade minutes."),
           (4,"Halfback. Local product. Two seasons (2022–23). One rated NRL appearance — 6.5/10. A developing local halfback."),
           (5,"Halfback. Local product. Two seasons at the Warriors (2022–23) as a development half.")]),

"Kane Evans": dict(era="2020–2021", pos="Prop", jersey="10", aliases=["kane evans","evans","kane"],
    clues=[(1,"Was sin-binned twice in the same game in 2021 — perhaps the most extraordinary single-game disciplinary record in the Warriors' history. Also sin-binned in a third separate incident. The TWL quote: 'Perhaps the most astonishing aspect was Brown trotted him back out after both binnings.'"),
           (2,"Sin-binned twice in one game in 2021 — then brought back on by coach Nathan Brown. 6 rated appearances averaging 4.83/10 — one of the lower career averages in the database."),
           (3,"Has been sin-binned three times in his Warriors career, including twice in the same game. Two seasons (2020–21). Infamous for his disciplinary record."),
           (4,"Prop. Two seasons (2020–21). Three sin-bins including twice in one game. 6 rated appearances averaging 4.83/10. Will's comment: 'Perhaps the most astonishing aspect was Brown trotted him back out after both binnings.'"),
           (5,"Prop. Two seasons at the Warriors (2020–21). Famous for being sin-binned twice in the same game — and being brought back on. Will wrote the definitive line about him.")]),

"Karl Lawton": dict(era="2018–2020", pos="Hooker", jersey="9", aliases=["karl lawton","lawton","karl"],
    clues=[(1,"The Warriors' starting hooker before Issac Luke arrived — 10 rated appearances averaging 6.50/10 across three seasons. A Queensland-born rake who was the club's first-choice No.9 in the first two Kearney years."),
           (2,"10 rated appearances averaging 6.5/10. Three seasons (2018–20). The Warriors' starting hooker in 2018 before competition from Issac Luke."),
           (3,"Queensland-born hooker. Three seasons (2018–20). The Warriors' starting No.9 through the 2018 finals season."),
           (4,"Hooker. Queensland-born. Three seasons (2018–20). The first-choice No.9 during the 2018 return to finals. 10 rated appearances averaging 6.5/10."),
           (5,"Hooker. Three seasons at the Warriors (2018–20). The starting hooker during the 2018 return to finals.")]),

"King Vuniyayawa": dict(era="2020", pos="Back-rower", jersey="12", aliases=["king vuniyayawa","vuniyayawa","king"],
    clues=[(1,"His first name is King — one of the more distinctive names in the Warriors' history. A local Auckland forward who got his opportunity in the COVID 2020 season. 2 rated appearances, 5.5/10."),
           (2,"2 rated appearances averaging 5.5/10 in 2020. A local product whose name — King — is as memorable as anything he did on the field."),
           (3,"A local Auckland forward named King Vuniyayawa. One COVID season at the Warriors (2020). Two rated appearances."),
           (4,"Back-rower. First name: King. Local Auckland product. One COVID season (2020). 2 rated appearances — 5.5/10."),
           (5,"Back-rower. First name: King. Local Auckland product. One season at the Warriors during the 2020 COVID year.")]),

"Lachlan Burr": dict(era="2019–2020", pos="Back-rower", jersey="12", aliases=["lachlan burr","burr","lachlan"],
    clues=[(1,"A Sydney-born back-rower who came from the Sydney Roosters system before joining the Warriors. 6 rated appearances averaging 6.50/10 across two seasons. Steady if unspectacular."),
           (2,"6 rated appearances averaging 6.5/10. Two seasons (2019–20). Joined from the Sydney Roosters. A Sydney-born edge forward."),
           (3,"Former Sydney Roosters player. Two seasons at the Warriors (2019–20). A Sydney-born edge forward with 6 rated appearances."),
           (4,"Back-rower. Former Sydney Roosters. Two seasons (2019–20). 6 rated appearances averaging 6.5/10. Reliable if unspectacular."),
           (5,"Back-rower. Former Sydney Roosters. Two seasons at the Warriors (2019–20).")]),

"Leeson Ah Mau": dict(era="2019–2021", pos="Prop", jersey="10", aliases=["leeson ah mau","ah mau","leeson"],
    clues=[(1,"A Samoan international prop who played for the Wellington Lions in the New Zealand domestic competition before his NRL career. 10 rated appearances averaging 6.5/10 across three seasons."),
           (2,"10 rated appearances averaging 6.5/10. Three seasons (2019–21). A Samoan international prop from the Wellington Lions system."),
           (3,"Samoan international. Wellington Lions background. Three seasons at the Warriors (2019–21). 10 rated appearances."),
           (4,"Prop. Samoan international. Three seasons (2019–21). Came through the Wellington Lions competition. 10 rated games averaging 6.5/10."),
           (5,"Prop. Samoan international. Three seasons at the Warriors (2019–21). A reliable rotation forward from the Wellington system.")]),

"Leivaha Pulu": dict(era="2018–2019", pos="Back-rower", jersey="12", aliases=["leivaha pulu","pulu","leivaha"],
    clues=[(1,"A Tongan international back-rower who came from the Wests Tigers before joining the Warriors in 2018. 4 rated appearances averaging 6.5/10. Two seasons (2018–19) as an edge forward."),
           (2,"4 rated appearances averaging 6.5/10. Two seasons (2018–19). Tongan international who came from the Wests Tigers."),
           (3,"Tongan international. Former Wests Tigers player. Two seasons at the Warriors (2018–19). Edge back-rower in the first two Kearney years."),
           (4,"Back-rower. Tongan international. Joined from the Wests Tigers in 2018. Two seasons. 4 rated appearances averaging 6.5/10."),
           (5,"Back-rower. Tongan international. Two seasons at the Warriors (2018–19), joining from the Wests Tigers.")]),

"Ligi Sao": dict(era="2018–2020", pos="Prop", jersey="10", aliases=["ligi sao","sao","ligi"],
    clues=[(1,"A Samoan international prop who played for the Newcastle Knights before joining the Warriors. 4 rated appearances averaging 7.0/10 — a solid average for a rotation prop. Three seasons (2018–20)."),
           (2,"4 rated appearances averaging 7.0/10. Three seasons (2018–20). Former Newcastle Knights prop and Samoan international."),
           (3,"Samoan international. Former Newcastle Knights. Three seasons at the Warriors (2018–20). 4 rated games — solid 7.0/10 average."),
           (4,"Prop. Samoan international. Former Newcastle Knights. Three seasons (2018–20). Averaged 7.0/10 from Will across 4 appearances — one of the better rotation prop averages."),
           (5,"Prop. Samoan international. Three seasons at the Warriors (2018–20). Former Newcastle Knights player.")]),

"Luke Hanson": dict(era="2023, 2026", pos="Lock", jersey="13", aliases=["luke hanson","hanson","luke"],
    clues=[(1,"Has appeared for the Warriors in two separate stints — 2023 and again in 2026. A local product who has returned to the top squad at different points in the Webster era. One rated NRL appearance, 5.5/10."),
           (2,"One rated appearance (5.5/10) across two separate Warriors stints — 2023 and 2026. A local lock who has been in and out of the squad."),
           (3,"A local Auckland forward who has been part of the Warriors' squad in two separate seasons (2023 and 2026)."),
           (4,"Lock. Local product. Two separate Warriors stints — 2023 and 2026. One rated NRL appearance, 5.5/10."),
           (5,"Lock. Local product. Has been part of the Warriors' squad in 2023 and 2026 in two separate stints.")]),

"Mason Lino": dict(era="2018–2019", pos="Five-eighth", jersey="6", aliases=["mason lino","lino","mason"],
    clues=[(1,"A Samoan international five-eighth who played for the Newcastle Knights before joining the Warriors in 2018. 3 rated appearances averaging 6.83/10. Two seasons (2018–19) as a spine utility."),
           (2,"3 rated appearances averaging 6.83/10. Two seasons (2018–19). Samoan international who came from Newcastle Knights."),
           (3,"Samoan international. Former Newcastle Knights player. Two seasons at the Warriors (2018–19). A utility back with 3 rated appearances."),
           (4,"Five-eighth. Samoan international. Former Newcastle Knights. Two seasons (2018–19). Averaged 6.83/10 across 3 rated appearances."),
           (5,"Five-eighth. Samoan international. Two seasons at the Warriors (2018–19), joining from the Newcastle Knights.")]),

"Matt Lodge": dict(era="2021–2022", pos="Prop", jersey="10", aliases=["matt lodge","lodge","matt"],
    clues=[(1,"A controversial Queensland prop — had a highly publicised off-field incident in New York in 2015 that derailed his career, before his redemption arc at Brisbane Broncos. Joined the Warriors in 2021. 5 rated appearances averaging 6.72/10."),
           (2,"5 rated appearances averaging 6.72/10. Two seasons (2021–22). A former Broncos prop with a well-documented personal history. Performed solidly when selected."),
           (3,"A Queensland prop with a controversial personal history before his Warriors stint. Former Brisbane Broncos. Two seasons at the Warriors (2021–22)."),
           (4,"Prop. Former Brisbane Broncos. Two seasons (2021–22). A Queensland prop whose career had a complicated early chapter. 5 rated appearances, 6.72/10 average."),
           (5,"Prop. Former Brisbane Broncos. Two seasons at the Warriors (2021–22). A Queensland prop whose career included a significant personal controversy before his rehabilitation.")]),

"Michael Sio": dict(era="2022", pos="Prop", jersey="10", aliases=["michael sio","sio","michael"],
    clues=[(1,"A veteran NSW prop who had played for multiple clubs including Canberra, Manly and the Bulldogs before his one season at the Warriors in 2022. Zero competitive rated appearances in Will's system."),
           (2,"Zero competitive rated appearances despite one season at the Warriors (2022). A veteran who provided depth without earning a Will Evans rating."),
           (3,"Veteran NSW prop. Former Raiders, Manly and Bulldogs player. One season at the Warriors (2022) without earning a competitive rated appearance."),
           (4,"Prop. Former Canberra, Manly and Bulldogs. One season at the Warriors (2022). Zero competitive rated appearances — squad depth only."),
           (5,"Prop. Veteran NSW prop. One season at the Warriors (2022), having previously played for Canberra, Manly and the Bulldogs.")]),

"Moala Graham-Taufa": dict(era="2022–2024", pos="Prop", jersey="10", aliases=["moala graham-taufa","graham-taufa","moala"],
    clues=[(1,"A local Auckland prop who developed through the Warriors' system across three seasons (2022–24). 2 rated appearances averaging 5.5/10. A fringe front-rower still developing."),
           (2,"2 rated appearances averaging 5.5/10. Three seasons (2022–24). A local prop developing through the Warriors' system."),
           (3,"Local Auckland product. Three seasons (2022–24) as a developing prop in the Warriors' squad."),
           (4,"Prop. Local product. Three seasons (2022–24). 2 rated appearances averaging 5.5/10. Still developing through the club's system."),
           (5,"Prop. Local product. Three seasons at the Warriors (2022–24) as a developing front-rower.")]),

"Nate Roache": dict(era="2019", pos="Hooker", jersey="9", aliases=["nate roache","roache","nate","nathaniel roache"],
    clues=[(1,"Brother of Paul Roache — both played for the Warriors. Nate debuted in 2019 as a local hooker, predating his brother's Warriors stint. 2 rated appearances, 6.5/10."),
           (2,"2 rated appearances (6.5/10) in 2019. Brother of Paul Roache. A local hooker who made his NRL debut for the Warriors."),
           (3,"Local product. Brother of Paul Roache — both played for the Warriors. Debuted in 2019 as the club's backup hooker."),
           (4,"Hooker. Local product. Brother of Paul Roache (also a Warrior). One season (2019). 2 rated appearances, 6.5/10."),
           (5,"Hooker. Local product. Brother of Paul Roache — both Warriors. Debuted in 2019.")]),

"Patrick Herbert": dict(era="2019–2020", pos="Winger/centre", jersey="2", aliases=["patrick herbert","herbert","patrick"],
    clues=[(1,"A Queensland-born winger/centre who came through the Manly Sea Eagles system before joining the Warriors. 7 rated appearances averaging 6.79/10 — solid across two seasons (2019–20)."),
           (2,"7 rated appearances averaging 6.79/10. Two seasons (2019–20). Former Manly Sea Eagles player. One of the better fringe back averages in the Kearney era."),
           (3,"Former Manly Sea Eagles player. Queensland-born. Two seasons (2019–20). 7 rated appearances averaging 6.79/10."),
           (4,"Winger/centre. Former Manly Sea Eagles. Two seasons (2019–20). 7 rated appearances averaging 6.79/10 — respectable for a fringe back."),
           (5,"Winger/centre. Former Manly Sea Eagles. Two seasons at the Warriors (2019–20).")]),

"Patrick Moimoi": dict(era="2023", pos="Prop", jersey="10", aliases=["patrick moimoi","moimoi","patrick"],
    clues=[(1,"Zero competitive rated appearances — a 2023 squad prop who didn't earn a competitive game rating from Will. Part of the Warriors' forward depth in a successful season without front-row game time."),
           (2,"Zero competitive rated appearances in 2023 despite being part of the squad. A local prop in a deep Warriors forward rotation."),
           (3,"Local product. 2023 Warriors squad member. Zero competitive rated appearances from Will — squad depth in a successful season."),
           (4,"Prop. Local product. 2023 squad member. Zero competitive rated appearances in a season where the Warriors reached the preliminary final."),
           (5,"Prop. Local product. Part of the 2023 Warriors squad without earning competitive first-grade minutes.")]),

"Paul Roache": dict(era="2022–2024", pos="Hooker", jersey="9", aliases=["paul roache","roache","paul"],
    clues=[(1,"Brother of Nate Roache — both played for the Warriors. Paul's three seasons (2022–24) came later than his brother's 2019 stint. 2 rated appearances averaging 5.5/10 as a backup hooker."),
           (2,"2 rated appearances averaging 5.5/10. Three seasons (2022–24). Brother of Nate Roache. A backup hooker competing with Egan, Lussick and Healey for the No.9 spot."),
           (3,"Brother of Nate Roache — both Warriors. Three seasons (2022–24) as a backup hooker. 2 rated NRL appearances."),
           (4,"Hooker. Brother of Nate Roache. Three seasons (2022–24). 2 rated appearances averaging 5.5/10. A backup hooker in a competitive position."),
           (5,"Hooker. Brother of Nate Roache — both Warriors. Three seasons at the Warriors (2022–24) as a backup hooker.")]),

"Paul Turner": dict(era="2020–2021", pos="Winger", jersey="2", aliases=["paul turner","turner","paul"],
    clues=[(1,"A local Auckland winger who played two seasons (2020–21) at the Warriors. One rated appearance (6.5/10). Part of the COVID-era and early Nathan Brown era squads."),
           (2,"One rated appearance (6.5/10) across two seasons (2020–21). Local winger in the COVID/Nathan Brown era."),
           (3,"Local Auckland product. Two seasons (2020–21) as a fringe winger. One rated NRL appearance."),
           (4,"Winger. Local product. Two seasons (2020–21). One rated appearance — 6.5/10. Squad member during a difficult Warriors era."),
           (5,"Winger. Local product. Two seasons at the Warriors (2020–21) as a fringe squad winger.")]),

"Poasa Faamausili": dict(era="2020", pos="Prop", jersey="10", aliases=["poasa faamausili","faamausili","poasa"],
    clues=[(1,"Zero competitive rated appearances — a 2020 COVID season squad prop who didn't earn a Will Evans competitive game rating. Part of the Warriors' forward depth during the Australia bubble."),
           (2,"Zero competitive rated appearances despite being part of the 2020 COVID squad in Australia. A development prop without top-grade minutes."),
           (3,"Part of the Warriors' 2020 COVID squad in Australia. Zero competitive rated appearances from Will."),
           (4,"Prop. 2020 COVID season squad member. Zero competitive rated appearances. Part of the Warriors' forward depth during the Australia bubble."),
           (5,"Prop. Part of the Warriors' 2020 COVID season squad. Did not earn competitive first-grade minutes.")]),

"Quinnlan Tupou": dict(era="2023", pos="Winger", jersey="2", aliases=["quinnlan tupou","tupou","quinnlan"],
    clues=[(1,"Zero competitive rated appearances — a local winger in the 2023 Warriors squad who didn't earn a competitive rating. Was part of a successful squad season without top-grade minutes."),
           (2,"Zero competitive rated appearances in 2023 despite being in the Warriors' squad. A local winger in the preliminary finalist squad."),
           (3,"Local product. 2023 squad member — the year the Warriors reached the preliminary final. Zero competitive rated appearances."),
           (4,"Winger. Local product. 2023 Warriors squad member. Zero competitive rated appearances from Will in a successful season."),
           (5,"Winger. Local product. Part of the 2023 Warriors squad that reached the preliminary final.")]),

"Ronald Volkman": dict(era="2022–2023", pos="Five-eighth", jersey="6", aliases=["ronald volkman","volkman","ronald"],
    clues=[(1,"A utility back who joined from the Gold Coast Titans system. 2 rated appearances averaging 6.5/10 across two seasons (2022–23). A backup spine option across the early Webster era."),
           (2,"2 rated appearances averaging 6.5/10. Two seasons (2022–23). Joined from the Gold Coast Titans system as a utility spine player."),
           (3,"Former Gold Coast Titans system. Two seasons at the Warriors (2022–23) as a backup half/five-eighth."),
           (4,"Five-eighth. Former Gold Coast Titans. Two seasons (2022–23). 2 rated appearances, 6.5/10. A utility spine player in the early Webster era."),
           (5,"Five-eighth. Former Gold Coast Titans. Two seasons at the Warriors (2022–23) as a utility spine player.")]),

"Sam Cook": dict(era="2018", pos="Prop", jersey="10", aliases=["sam cook","cook","sam"],
    clues=[(1,"One rated appearance (5.5/10) in 2018 — the first year of the Kearney era and the Warriors' return to finals. A one-season prop who got limited opportunities."),
           (2,"One rated appearance (5.5/10) in 2018. A one-season Warrior — the return-to-finals season. A fringe prop with one game in the ratings."),
           (3,"One NRL season at the Warriors (2018). One rated appearance. Part of the squad that ended the Warriors' 10-year finals drought."),
           (4,"Prop. One season (2018). One rated NRL appearance — 5.5/10. Part of the Warriors' return-to-finals squad."),
           (5,"Prop. One season at the Warriors (2018) — the return-to-finals season.")]),

"Sam Lisone": dict(era="2018–2020", pos="Prop", jersey="10", aliases=["sam lisone","lisone","sam"],
    clues=[(1,"A Samoan international prop who played for the Wests Tigers before joining the Warriors. 7 rated appearances averaging 5.93/10 across three seasons (2018–20). An NRL/World All Stars representative."),
           (2,"7 rated appearances averaging 5.93/10. Three seasons (2018–20). Samoan international. Former Wests Tigers. NRL/World All Stars representative in 2017."),
           (3,"Samoan international. NRL World All Stars representative (2017). Former Wests Tigers. Three seasons at the Warriors (2018–20)."),
           (4,"Prop. Samoan international. NRL World All Stars rep. Former Wests Tigers. Three seasons (2018–20). 7 rated games averaging 5.93/10."),
           (5,"Prop. Samoan international. Three seasons at the Warriors (2018–20). Former Wests Tigers. NRL World All Stars representative.")]),

"Sanele Aukusitino": dict(era="2022", pos="Back-rower", jersey="12", aliases=["sanele aukusitino","aukusitino","sanele"],
    clues=[(1,"One rated appearance (5.5/10) in 2022. A local Auckland forward who got his opportunity in a limited way in 2022. Part of the Warriors' development pathway."),
           (2,"One rated appearance (5.5/10) in 2022. A local product who made a brief NRL appearance."),
           (3,"Local Auckland product. One NRL appearance for the Warriors in 2022. Development player."),
           (4,"Back-rower. Local product. One rated NRL appearance (5.5/10) in 2022."),
           (5,"Back-rower. Local product. One NRL appearance for the Warriors in 2022.")]),

"Setu Tu": dict(era="2023", pos="Prop", jersey="10", aliases=["setu tu","tu","setu"],
    clues=[(1,"Zero competitive rated appearances despite being part of the 2023 Warriors squad — the preliminary final season. A local prop in a deep forward rotation without top-grade minutes."),
           (2,"Zero competitive rated appearances in 2023. Part of the Warriors' squad that reached the preliminary final without earning a Will Evans competitive rating."),
           (3,"Local product. 2023 Warriors squad member. Zero competitive rated appearances in a historically successful season."),
           (4,"Prop. Local product. 2023 squad member. Zero competitive rated appearances despite the Warriors' deep finals run."),
           (5,"Prop. Local product. Part of the 2023 Warriors squad. Did not earn competitive first-grade game time.")]),

"Solomon Vasuvulagi": dict(era="2022", pos="Winger", jersey="2", aliases=["solomon vasuvulagi","vasuvulagi","solomon"],
    clues=[(1,"One rated appearance (6.5/10) in 2022 — a debut season for this local winger. Part of a Warriors squad that struggled through a difficult year."),
           (2,"One rated appearance (6.5/10) for the Warriors in 2022. A local winger making his NRL debut."),
           (3,"Local product. Made his NRL debut for the Warriors in 2022. One rated appearance."),
           (4,"Winger. Local product. NRL debut for the Warriors in 2022. One rated appearance — 6.5/10."),
           (5,"Winger. Local product. Made his NRL debut with the Warriors in 2022.")]),

"Solomone Kata": dict(era="2018–2019", pos="Centre/wing", jersey="3", aliases=["solomone kata","kata","solomone"],
    clues=[(1,"A Tongan international who came to the Warriors after playing for the Parramatta Eels and New Zealand Warriors' NSW Cup team. 5 rated appearances averaging 6.5/10. A powerful Tongan-born centre."),
           (2,"5 rated appearances averaging 6.5/10. Two seasons (2018–19). Tongan international. Former Parramatta and Melbourne systems."),
           (3,"Tongan international. Former Parramatta Eels. Two seasons at the Warriors (2018–19). A big, powerful centre with 5 rated games."),
           (4,"Centre/wing. Tongan international. Former Parramatta. Two seasons (2018–19). Averaged 6.5/10 across 5 rated appearances."),
           (5,"Centre/wing. Tongan international. Two seasons at the Warriors (2018–19). A powerful Tongan-born back who came from the Parramatta system.")]),

"Taane Milne": dict(era="2020", pos="Winger", jersey="2", aliases=["taane milne","milne","taane"],
    clues=[(1,"Received 7.5/10 from Will in his only rated appearance — the highest single-game rating for a player with only one rated appearance in the entire database. A one-game wonder who left an impression."),
           (2,"One rated appearance — 7.5/10. The highest-rated player in the database with only a single competitive rating. A 2020 one-game Warrior."),
           (3,"One rated appearance for the Warriors in 2020 — 7.5/10. A speedster winger who impressed in his only opportunity."),
           (4,"Winger. One season (2020). One rated appearance — 7.5/10. A one-game Warrior who holds the distinction of the highest single-game rating among players with only one appearance."),
           (5,"Winger. One season at the Warriors (2020). One rated appearance — 7.5/10. A brief, impressive visit.")]),

"Taniela Otukolo": dict(era="2021–2022", pos="Prop", jersey="10", aliases=["taniela otukolo","otukolo","taniela"],
    clues=[(1,"A Tongan-born prop who came through the Sydney club ranks before joining the Warriors. 3 rated appearances averaging 5.17/10 across two seasons (2021–22). Limited first-grade exposure."),
           (2,"3 rated appearances averaging 5.17/10. Two seasons (2021–22). A Tongan-born prop with limited top-grade exposure."),
           (3,"Tongan-born prop. Two seasons at the Warriors (2021–22). 3 rated appearances in a fringe role."),
           (4,"Prop. Tongan heritage. Two seasons (2021–22). 3 rated appearances averaging 5.17/10. A fringe prop in a Warriors squad going through transition."),
           (5,"Prop. Tongan heritage. Two seasons at the Warriors (2021–22). A fringe prop in the club's squad during a difficult transition period.")]),

"Tanner Stanners-Smith": dict(era="2024", pos="Back-rower", jersey="17", aliases=["tanner stanners-smith","stanners-smith","tanner"],
    clues=[(1,"One rated appearance (5.5/10) in 2024. A local forward who got his opportunity in the Warriors' squad. Part of the club's developing forward depth."),
           (2,"One rated appearance (5.5/10) in 2024. A local product getting his first-grade opportunity."),
           (3,"Local product. One NRL season (2024). One rated appearance in Will's system."),
           (4,"Back-rower. Local product. One season (2024). One rated NRL appearance — 5.5/10."),
           (5,"Back-rower. Local product. One Warriors season (2024). Development forward from the club's pathway.")]),

"Tom Ale": dict(era="2020–2024", pos="Prop/back-rower", jersey="12", aliases=["tom ale","ale","tom"],
    clues=[(1,"A Samoan international who played for the Penrith Panthers and Canberra Raiders before joining the Warriors in 2020. 21 rated appearances averaging 6.26/10 across five seasons."),
           (2,"21 rated appearances averaging 6.26/10. Five seasons (2020–24). Samoan international. Former Penrith and Canberra player. Reliable five-season squad member."),
           (3,"Samoan international. Former Penrith Panthers and Canberra Raiders. Five seasons at the Warriors (2020–24). 21 rated appearances across four coaching regimes."),
           (4,"Prop/back-rower. Samoan international. Former Penrith and Canberra. Five seasons (2020–24). Steady squad presence across the Brown, Jones and early Webster eras."),
           (5,"Prop/back-rower. Samoan international. Five seasons at the Warriors (2020–24). Former Penrith Panthers and Canberra Raiders player.")]),

"Toni Tupouniua": dict(era="2023", pos="Back-rower", jersey="12", aliases=["toni tupouniua","tupouniua","toni"],
    clues=[(1,"A Tongan international back-rower who had played for the Sydney Roosters (with whom he won a 2019 premiership) before his brief Warriors stint in 2023. Zero competitive rated appearances in Will's database."),
           (2,"Zero competitive rated appearances in 2023. A former Sydney Roosters premiership winner (2019) who joined the Warriors for one season without earning a competitive rating."),
           (3,"Tongan international. Former Sydney Roosters — 2019 premiership winner. One season at the Warriors (2023) without earning a competitive Will Evans rating."),
           (4,"Back-rower. Tongan international. Former Sydney Roosters (2019 premiers). One season at the Warriors (2023). Zero competitive rated appearances."),
           (5,"Back-rower. Tongan international. Former Sydney Roosters premiership winner. One season at the Warriors (2023).")]),

"Viliame Vailea": dict(era="2022–2023", pos="Winger", jersey="2", aliases=["viliame vailea","vailea","viliame"],
    clues=[(1,"Cousin of Viliami Vailea — the 'e' versus 'i' distinction is how you tell them apart. Both played for the Warriors simultaneously. 2 rated appearances averaging 5.0/10."),
           (2,"2 rated appearances averaging 5.0/10. Two seasons (2022–23). Cousin of Viliami Vailea — both played for the Warriors at the same time."),
           (3,"Cousin of Viliami Vailea — same surname, different first-name spelling. Two seasons (2022–23) at the Warriors."),
           (4,"Winger. Cousin of Viliami Vailea (different spelling). Two seasons (2022–23). 2 rated appearances averaging 5.0/10."),
           (5,"Winger. Cousin of Viliami Vailea — same surname, different spelling. Two seasons at the Warriors (2022–23).")]),

})

print(f"Total players defined: {len(PLAYERS)}")
