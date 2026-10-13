"""
추천 작품 풀 + 다양성 추천 로직

다양성 축
- format : 영화 / 드라마 / 다큐 / 애니
- country: 한국, 미국, 일본, 영국, 스페인, 인도
- mood   : 감동, 실화, 스릴러, 코미디, 범죄, 판타지, 직장
- year   : 1980년대 ~ 2020년대
- topics : 퀴즈 분야(data.CATEGORIES)와 같은 이름 -> 틀린 분야를 보완하는 작품을 우선 추천
- level  : 1 새싹 / 2 탐험가 / 3 고수 (금융 내용의 난이도)

desc, point는 직접 쓴 한 줄 소개입니다. 관람 등급은 플랫폼마다 다르니 확인 후 보세요.
"""
import random

FORMAT_ICON = {"영화": "🎬", "드라마": "📺", "다큐": "🎥", "애니": "🎨"}
COUNTRY_FLAG = {"한국": "🇰🇷", "미국": "🇺🇸", "일본": "🇯🇵", "영국": "🇬🇧",
                "스페인": "🇪🇸", "인도": "🇮🇳"}

WORKS = [
    # ── 레벨 1: 금융 새싹 ─────────────────────────
    {"title": "행복을 찾아서", "original": "The Pursuit of Happyness",
     "format": "영화", "country": "미국", "year": 2006, "mood": "감동", "level": 1,
     "topics": ["예금·저축", "기초 개념"],
     "desc": "통장 잔고 0원에서 증권사 인턴에 도전하는 아버지의 실화.",
     "point": "돈이 없을 때 생활이 어떻게 무너지는지, 그리고 금융업계의 입구"},
    {"title": "덤 머니", "original": "Dumb Money",
     "format": "영화", "country": "미국", "year": 2023, "mood": "코미디", "level": 1,
     "topics": ["투자"],
     "desc": "개인 투자자들이 커뮤니티로 뭉쳐 헤지펀드와 맞붙은 게임스탑 사태.",
     "point": "공매도, 숏스퀴즈가 무엇인지 쉽게 이해"},
    {"title": "머니볼", "original": "Moneyball",
     "format": "영화", "country": "미국", "year": 2011, "mood": "실화", "level": 1,
     "topics": ["투자", "기초 개념"],
     "desc": "가난한 야구단이 데이터로 '저평가된 선수'를 사 모으는 이야기.",
     "point": "가치투자의 핵심인 '싸고 좋은 것 찾기'를 야구로 체험"},
    {"title": "캐치 미 이프 유 캔", "original": "Catch Me If You Can",
     "format": "영화", "country": "미국", "year": 2002, "mood": "범죄", "level": 1,
     "topics": ["금융 안전"],
     "desc": "위조 수표로 은행을 속이는 천재 사기꾼과 그를 쫓는 FBI 요원.",
     "point": "금융 사기가 어떤 허점을 파고드는지"},
    {"title": "종이의 집", "original": "La casa de papel",
     "format": "드라마", "country": "스페인", "year": 2017, "mood": "스릴러", "level": 1,
     "topics": ["경제 지표"],
     "desc": "조폐국을 점거하고 돈을 직접 '찍어내는' 강도단.",
     "point": "돈을 찍으면 왜 문제가 되는지, 화폐와 인플레이션 감각"},
    {"title": "늑대와 향신료", "original": "狼と香辛料",
     "format": "애니", "country": "일본", "year": 2008, "mood": "판타지", "level": 1,
     "topics": ["경제 지표", "기초 개념"],
     "desc": "떠돌이 상인과 늑대 신이 은화 시세와 거래로 승부하는 중세 판타지.",
     "point": "화폐 가치, 환전, 신용 거래를 이야기로 익히기"},
    {"title": "작은 아씨들", "original": None,
     "format": "드라마", "country": "한국", "year": 2022, "mood": "스릴러", "level": 1,
     "topics": ["예금·저축", "금융 안전"],
     "desc": "가난한 세 자매 앞에 거액의 돈이 나타나며 벌어지는 미스터리.",
     "point": "돈이 사람의 선택을 어떻게 바꾸는지"},
    {"title": "쩐의 전쟁", "original": None,
     "format": "드라마", "country": "한국", "year": 2007, "mood": "범죄", "level": 1,
     "topics": ["신용·대출"],
     "desc": "사채 빚에 무너진 주인공이 사채업자가 되어 돌아오는 복수극.",
     "point": "고금리 빚과 이자가 불어나는 무서움"},
    {"title": "오징어 게임", "original": None,
     "format": "드라마", "country": "한국", "year": 2021, "mood": "스릴러", "level": 1,
     "topics": ["신용·대출"],
     "desc": "빚에 몰린 사람들이 상금을 걸고 목숨을 건 게임에 참가한다. (청소년 관람불가)",
     "point": "빚이 사람을 어디까지 몰아붙이는지"},

    # ── 레벨 2: 금융 탐험가 ───────────────────────
    {"title": "국가부도의 날", "original": None,
     "format": "영화", "country": "한국", "year": 2018, "mood": "실화", "level": 2,
     "topics": ["경제사", "경제 지표"],
     "desc": "1997년 외환위기 직전 일주일, 각자 다른 선택을 한 사람들.",
     "point": "환율, 외환보유액, IMF 구제금융"},
    {"title": "재벌집 막내아들", "original": None,
     "format": "드라마", "country": "한국", "year": 2022, "mood": "판타지", "level": 2,
     "topics": ["경제사", "투자"],
     "desc": "과거로 돌아간 주인공이 한국 경제사의 큰 사건들을 미리 알고 투자한다.",
     "point": "IMF, 닷컴 버블 등 한국 경제사 한 바퀴"},
    {"title": "돈", "original": None,
     "format": "영화", "country": "한국", "year": 2019, "mood": "범죄", "level": 2,
     "topics": ["투자", "금융 안전"],
     "desc": "신입 주식 브로커가 거액의 작전에 휘말리는 여의도 이야기.",
     "point": "증권사 브로커의 일, 주가조작의 구조"},
    {"title": "블랙머니", "original": None,
     "format": "영화", "country": "한국", "year": 2019, "mood": "실화", "level": 2,
     "topics": ["경제사", "세금·제도"],
     "desc": "은행 헐값 매각 의혹을 파헤치는 검사의 추적극. 실제 사건에서 모티브를 얻었다.",
     "point": "금융당국, 외국계 펀드, 은행 매각의 쟁점"},
    {"title": "작전", "original": None,
     "format": "영화", "country": "한국", "year": 2009, "mood": "범죄", "level": 2,
     "topics": ["투자", "금융 안전"],
     "desc": "개미 투자자가 주가조작 세력의 작전에 끼어들게 된다.",
     "point": "작전주와 시세조종이 개인 투자자에게 남기는 것"},
    {"title": "미생", "original": None,
     "format": "드라마", "country": "한국", "year": 2014, "mood": "직장", "level": 2,
     "topics": ["기초 개념"],
     "desc": "바둑만 두던 청년이 종합상사 인턴으로 들어가 버티는 이야기.",
     "point": "회사가 돈을 버는 방식, 무역과 사업 손익의 감각"},
    {"title": "한자와 나오키", "original": "半沢直樹",
     "format": "드라마", "country": "일본", "year": 2013, "mood": "직장", "level": 2,
     "topics": ["신용·대출"],
     "desc": "부실 대출의 책임을 뒤집어쓴 은행원이 '배로 갚아주는' 반격극.",
     "point": "은행 대출 심사와 부실채권이 생기는 과정"},
    {"title": "99 홈즈", "original": "99 Homes",
     "format": "영화", "country": "미국", "year": 2014, "mood": "스릴러", "level": 2,
     "topics": ["신용·대출", "경제사"],
     "desc": "금융위기 때 집을 압류당한 가장이 압류 업자 밑에서 일하게 된다.",
     "point": "주택담보대출을 못 갚으면 벌어지는 일"},
    {"title": "머니 몬스터", "original": "Money Monster",
     "format": "영화", "country": "미국", "year": 2016, "mood": "스릴러", "level": 2,
     "topics": ["투자"],
     "desc": "투자 추천으로 전 재산을 잃은 시청자가 생방송 스튜디오를 점거한다.",
     "point": "방송·유튜브 종목 추천을 그대로 믿으면 안 되는 이유"},
    {"title": "더 울프 오브 월 스트리트", "original": "The Wolf of Wall Street",
     "format": "영화", "country": "미국", "year": 2013, "mood": "실화", "level": 2,
     "topics": ["금융 안전", "투자"],
     "desc": "싸구려 주식을 팔아 거부가 된 브로커의 화려한 몰락. (청소년 관람불가)",
     "point": "과장 영업과 투자 사기가 굴러가는 방식"},
    {"title": "Madoff: The Monster of Wall Street", "original": None,
     "format": "다큐", "country": "미국", "year": 2023, "mood": "실화", "level": 2,
     "topics": ["금융 안전"],
     "desc": "수십 년간 이어진 역대급 폰지 사기를 추적하는 넷플릭스 다큐 시리즈.",
     "point": "'꾸준한 고수익'이 왜 위험 신호인지"},
    {"title": "Eat the Rich: The GameStop Saga", "original": None,
     "format": "다큐", "country": "미국", "year": 2022, "mood": "실화", "level": 2,
     "topics": ["투자"],
     "desc": "게임스탑 사태를 당사자 인터뷰로 되짚는 넷플릭스 다큐 시리즈.",
     "point": "덤 머니와 같이 보면 좋은 실제 기록"},

    # ── 레벨 3: 금융 고수 ─────────────────────────
    {"title": "빅쇼트", "original": "The Big Short",
     "format": "영화", "country": "미국", "year": 2015, "mood": "실화", "level": 3,
     "topics": ["경제사", "투자", "신용·대출"],
     "desc": "주택시장 붕괴를 먼저 알아챈 괴짜들이 시장 전체에 반대로 베팅한다.",
     "point": "서브프라임, MBS, CDO, CDS"},
    {"title": "마진콜", "original": "Margin Call",
     "format": "영화", "country": "미국", "year": 2011, "mood": "스릴러", "level": 3,
     "topics": ["투자", "경제사"],
     "desc": "금융위기 전날 밤, 한 투자은행 안에서 벌어지는 24시간.",
     "point": "레버리지와 리스크 관리가 무너지는 순간"},
    {"title": "인사이드 잡", "original": "Inside Job",
     "format": "다큐", "country": "미국", "year": 2010, "mood": "실화", "level": 3,
     "topics": ["경제사", "세금·제도"],
     "desc": "2008 금융위기가 왜 일어났는지 관계자 인터뷰로 파고드는 다큐.",
     "point": "규제 완화, 신용평가사, 금융위기의 구조"},
    {"title": "투 빅 투 페일", "original": "Too Big to Fail",
     "format": "영화", "country": "미국", "year": 2011, "mood": "실화", "level": 3,
     "topics": ["경제사", "세금·제도"],
     "desc": "리먼 파산 전후, 미국 재무부가 금융시스템을 살리려 뛰어다닌 몇 주.",
     "point": "구제금융과 '대마불사' 논쟁"},
    {"title": "머니게임", "original": None,
     "format": "드라마", "country": "한국", "year": 2020, "mood": "직장", "level": 3,
     "topics": ["경제 지표", "세금·제도"],
     "desc": "금융위기를 막으려는 경제 관료들이 국익과 소신 사이에서 부딪힌다.",
     "point": "금융정책, 경제 관료가 하는 일"},
    {"title": "빌리언스", "original": "Billions",
     "format": "드라마", "country": "미국", "year": 2016, "mood": "범죄", "level": 3,
     "topics": ["투자", "금융 안전"],
     "desc": "천재 헤지펀드 매니저와 그를 노리는 검사의 두뇌 싸움.",
     "point": "헤지펀드 전략과 내부자 거래"},
    {"title": "인더스트리", "original": "Industry",
     "format": "드라마", "country": "영국", "year": 2020, "mood": "직장", "level": 3,
     "topics": ["투자"],
     "desc": "런던 투자은행에 입사한 신입들의 살벌한 생존기.",
     "point": "트레이딩 데스크와 투자은행의 실제 업무"},
    {"title": "하게타카", "original": "ハゲタカ",
     "format": "드라마", "country": "일본", "year": 2007, "mood": "직장", "level": 3,
     "topics": ["투자", "경제사"],
     "desc": "버블 붕괴 후 일본 기업을 사들이는 사모펀드 매니저.",
     "point": "기업 인수합병(M&A)과 부실기업 구조조정"},
    {"title": "스캠 1992", "original": "Scam 1992: The Harshad Mehta Story",
     "format": "드라마", "country": "인도", "year": 2020, "mood": "실화", "level": 3,
     "topics": ["투자", "금융 안전", "경제사"],
     "desc": "인도 증시를 뒤흔든 '빅불' 브로커의 실화.",
     "point": "은행 시스템의 허점을 이용한 증시 조작"},
    {"title": "로그 트레이더", "original": "Rogue Trader",
     "format": "영화", "country": "영국", "year": 1999, "mood": "실화", "level": 3,
     "topics": ["투자", "금융 안전"],
     "desc": "한 명의 트레이더가 손실을 숨기다 200년 넘은 은행을 무너뜨린 실화.",
     "point": "파생상품 손실과 내부통제 실패"},
    {"title": "월 스트리트", "original": "Wall Street",
     "format": "영화", "country": "미국", "year": 1987, "mood": "범죄", "level": 3,
     "topics": ["투자", "금융 안전"],
     "desc": "야심 찬 젊은 브로커가 전설적인 기업 사냥꾼의 세계에 빠져든다.",
     "point": "기업 사냥, 내부자 거래가 문제인 이유"},
    {"title": "Enron: The Smartest Guys in the Room", "original": None,
     "format": "다큐", "country": "미국", "year": 2005, "mood": "실화", "level": 3,
     "topics": ["금융 안전", "세금·제도"],
     "desc": "미국 대표 에너지 기업이 회계 부정으로 한순간에 무너진 과정.",
     "point": "분식회계, 감사와 공시의 중요성"},
]

TITLES = {w["title"] for w in WORKS}


def _decade(w):
    return w["year"] // 10 * 10


def recommend(level, weak_topics=(), k=4, seed=None):
    """
    level: 1~3
    weak_topics: 틀린 문제의 분야들
    - 같은 레벨에서 k-1개를 고르되, 고를 때마다 이미 뽑힌 것과 형식·국가·분위기·시대가
      다를수록, 약한 분야를 새로 채울수록 점수를 더 줌
    - 마지막 1개는 한 단계 위 레벨의 '도전작' (고수는 아래 레벨의 '쉬어가기')
    반환: [(작품, 추천이유)]
    """
    rng = random.Random(seed)
    weak = set(weak_topics)
    picks, covered = [], set()

    def gain(w):
        g = 0
        g += 3 if w["format"] not in {p["format"] for p in picks} else 0
        g += 2 if w["country"] not in {p["country"] for p in picks} else 0
        g += 1.5 if w["mood"] not in {p["mood"] for p in picks} else 0
        g += 1 if _decade(w) not in {_decade(p) for p in picks} else 0
        g += 2.5 * len((set(w["topics"]) & weak) - covered)
        return g + rng.random() * 1.5          # 다시 할 때마다 조합이 조금씩 바뀜

    candidates = [w for w in WORKS if w["level"] == level]
    while len(picks) < k - 1 and candidates:
        best = max(candidates, key=gain)
        picks.append(best)
        candidates.remove(best)
        covered |= set(best["topics"]) & weak

    bonus_level = level + 1 if level < 3 else 2
    bonus_pool = [w for w in WORKS if w["level"] == bonus_level]
    bonus = max(bonus_pool, key=gain)

    def reason(w):
        hit = [t for t in w["topics"] if t in weak]
        return f"틀린 '{hit[0]}' 분야를 채워줘요" if hit else None

    result = [(w, reason(w)) for w in picks]
    tag = "🚀 한 단계 위 도전작" if level < 3 else "☕ 가볍게 쉬어가기"
    result.append((bonus, tag))
    return result
