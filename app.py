import random
from pathlib import Path
from urllib.parse import quote

import streamlit as st
from data import LEVELS, get_level, pick_questions
from works import COUNTRY_FLAG, FORMAT_ICON, WORKS, recommend

# 배포 후 받은 주소로 바꾸세요 (공유 링크에 쓰임)
APP_URL = "https://your-app-name.streamlit.app"
N_QUESTIONS = 10
TYPE_LABEL = {"choice": "객관식", "ox": "OX", "calc": "계산", "situation": "상황"}
FORMAT_EN = {"영화": "FILM", "드라마": "SERIES", "다큐": "DOCUMENTARY", "애니": "ANIMATION"}
FORMAT_SHORT = {"영화": "FILM", "드라마": "SERIES", "다큐": "DOCU", "애니": "ANIME"}
LEVEL_EN = ["the beginner", "the explorer", "the master"]

st.set_page_config(page_title="moneyvie | 금융 레벨로 고르는 영화·드라마", page_icon="🎞️", layout="centered")
st.markdown(f"<style>{(Path(__file__).parent / 'style.css').read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True)


def html(s):
    st.markdown(s, unsafe_allow_html=True)


# ── 상태 ──────────────────────────────────────
def init_state():
    st.session_state.step = 0                      # 0: 시작, 1~N: 문제, N+1: 결과
    st.session_state.questions = pick_questions(N_QUESTIONS)
    st.session_state.answers = []                  # 고른 보기 인덱스
    st.session_state.rec_seed = random.random()    # 결과 화면을 다시 그려도 추천이 바뀌지 않게


def start():
    st.query_params.clear()
    st.session_state.step = 1


def choose(idx):
    st.session_state.answers.append(idx)
    st.session_state.step += 1


def restart():
    st.query_params.clear()
    init_state()


if "step" not in st.session_state:
    init_state()


# ── 조각들 ─────────────────────────────────────
# 시작 화면의 하프톤 모자이크 (6 x 4). (클래스, 글자)
MOSAIC = [
    ("dot-m", ""), ("blank", ""), ("paper", "₩"), ("dot-s", ""), ("fade", ""), ("ink", "%"),
    ("blank", ""), ("dot-l", ""), ("lines", ""), ("blank", ""), ("dot-m", ""), ("blank", ""),
    ("dot-s", "$"), ("paper", ""), ("dot-m", ""), ("ink", "▶"), ("blank", ""), ("dot-l", ""),
    ("fade", ""), ("blank", ""), ("dot-s", ""), ("paper", "↗"), ("lines", ""), ("dot-m", ""),
]


def mosaic():
    tiles = "".join(f"<div class='tile {c}'>{f'<span class=g>{g}</span>' if g else ''}</div>"
                    for c, g in MOSAIC)
    return f"<div class='mosaic'>{tiles}</div>"


def credits(lines):
    return "<div class='credits'>" + "<br>".join(
        "<span class='sep'>|</span>".join(parts) for parts in lines) + "</div>"


def work_film(w, tag, no):
    orig = f"<div class='o'>{w['original']}</div>" if w["original"] else ""
    tag_html = f"<div class='tag'>{tag}</div>" if tag else ""
    html(
        "<div class='film'>"
        f"<div class='edge'><span>MONEYVIE 400</span><span>▸ {no:02d}A</span></div>"
        "<div class='frame'>"
        f"{tag_html}"
        f"<div class='meta'>{FORMAT_EN[w['format']]} · {COUNTRY_FLAG[w['country']]} {w['country']} · {w['year']} · {w['mood']}</div>"
        f"<div class='t'>{w['title']}</div>{orig}"
        f"<div class='d'>{w['desc']}</div>"
        f"<div class='p'>— {w['point']}</div>"
        "</div></div>")


def work_ticket(w):
    html(
        "<div class='ticket'>"
        f"<div class='stub'><span>{FORMAT_ICON[w['format']]}</span><span class='y'>{w['year']}</span>"
        f"<span class='f'>{FORMAT_SHORT[w['format']]}</span></div>"
        "<div class='body'>"
        f"<div class='t'>{w['title']}</div>"
        f"<div class='m'>{COUNTRY_FLAG[w['country']]} {w['country']} · {w['mood']} · {LEVELS[w['level'] - 1]['name']}</div>"
        f"<div class='d'>{w['desc']}</div>"
        "</div></div>")


def browse_works():
    fmts = st.pills("형식", list(FORMAT_ICON), selection_mode="multi", key="f_fmt")
    lvls = st.pills("레벨", [lv["name"] for lv in LEVELS], selection_mode="multi", key="f_lv")
    shown = [w for w in WORKS
             if (not fmts or w["format"] in fmts)
             and (not lvls or LEVELS[w["level"] - 1]["name"] in lvls)]
    st.caption(f"{len(shown)}편 · 관람 등급은 각 플랫폼에서 확인하세요")
    for w in sorted(shown, key=lambda w: (w["level"], -w["year"])):
        work_ticket(w)


def level_poster(lv, level_idx, kicker):
    html(
        f"<div class='script'>now showing</div>"
        f"<div class='cap center' style='margin-top:6px'>{kicker}</div>"
        f"<div class='big-emoji'>{lv['emoji']}</div>"
        f"<div class='level-en'>{LEVEL_EN[level_idx]}</div>"
        f"<div class='level-kr'>{lv['name']}</div>"
        f"<div class='tagline'>{lv['desc']}</div>")


# ── 화면: 시작 ────────────────────────────────
def reel_svg():
    """가운데 작은 필름 조각 그림 (포스터 상단 일러스트 자리)"""
    holes = "".join(f"<rect x='{4 + i * 10}' y='{y}' width='5' height='3' rx='1' fill='#ECE8DF'/>"
                    for i in range(13) for y in (2, 29))
    frames = "".join(f"<rect x='{6 + i * 31}' y='8' width='27' height='18' fill='url(#ht{i % 2})'/>"
                     for i in range(4))
    return ("<svg viewBox='0 0 132 34' xmlns='http://www.w3.org/2000/svg'><defs>"
            "<pattern id='ht0' width='3' height='3' patternUnits='userSpaceOnUse'>"
            "<rect width='3' height='3' fill='#D6D0C2'/><circle cx='1.5' cy='1.5' r='.9' fill='#1D1C1A'/></pattern>"
            "<pattern id='ht1' width='3' height='3' patternUnits='userSpaceOnUse'>"
            "<rect width='3' height='3' fill='#E2DDD1'/><circle cx='1.5' cy='1.5' r='.55' fill='#1D1C1A'/></pattern>"
            "</defs><rect width='132' height='34' fill='#1D1C1A'/>" + holes + frames + "</svg>")


def start_view():
    # 1) 타이틀
    html(
        "<div class='marquee'><span>a test by moneyvie</span>"
        f"{reel_svg()}<span>original motion picture — 2026</span></div>"
        "<div class='title-block'>"
        "<div class='coord-r'>37.5665° N - 126.9780° E</div>"
        "<div class='tl l1'><span class='sw'>M</span><span class='px'>ONEY</span>"
        "<span class='spark'>✦</span></div>"
        "<div class='tl l2'><span class='sw'>V</span><span class='px'>IE</span>"
        "<span class='spark small'>✦</span></div>"
        "</div>"
        # 2) 소개
        "<div class='kr-title'>나의 금융 레벨로 고르는<br>인생 영화 · 드라마</div>"
        f"<div class='kr-sub'>예금부터 투자, 신용, 경제사까지 {N_QUESTIONS}개의 장면.<br>"
        "당신의 레벨에 맞는 상영작을 골라 드립니다.</div>")
    # 3) 모자이크 섹션
    html(
        "<hr class='rule' style='margin-top:22px'>"
        "<div class='coords' style='margin-bottom:12px'>SEOUL, KOREA</div>"
        "<div class='spaced'>isn't every film about money<br>a story worth a closer look?</div>"
        f"{mosaic()}"
        "<div class='kr-quote'>✱ 돈을 아는 만큼, 영화는 다르게 보인다.</div>")
    # 4) 시작 버튼 (맨 아래) + 크레딧
    st.write("")
    st.button("▶  상영 시작", on_click=start, type="primary", width="stretch")
    html(credits([
            ["moneyvie <b>presents</b>", f"{N_QUESTIONS} scenes", "8 genres of money"],
            [f"featuring <b>{len(WORKS)} films & series</b> from 6 countries"],
            ["written by <b>your answers</b>", "directed by <b>you</b>"],
        ]) + "<div class='fineprint'>※ 재미와 학습을 위한 테스트이며 투자 권유가 아닙니다.</div>")


# ── 화면: 공유 링크로 들어온 경우 ─────────────────
def shared_view(level_idx):
    level_poster(LEVELS[level_idx], level_idx, "친구의 금융 레벨은")
    st.write("")
    st.button("▶  나도 상영 시작", on_click=start, type="primary", width="stretch")
    html(credits([["moneyvie <b>presents</b>", f"{N_QUESTIONS} scenes", f"{len(WORKS)} films"]]))


# ── 화면: 문제 ────────────────────────────────
def question_view(step):
    q = st.session_state.questions[step - 1]
    frames = "".join(
        f"<i class='{'done' if i < step - 1 else 'now' if i == step - 1 else ''}'></i>"
        for i in range(N_QUESTIONS))
    html(
        "<div class='scene-head'>"
        f"<span class='no'>scene {step:02d}</span>"
        f"<span class='cat'>{q['category']}</span>"
        f"<span class='cnt'>{step:02d} / {N_QUESTIONS}</span>"
        "</div>"
        f"<div class='strip'>{frames}</div>"
        "<div class='q-card'>"
        f"<span class='corner'>TAKE {step}</span>"
        f"<div class='take'>{TYPE_LABEL[q['type']]} · 난이도 {'★' * q['level']}{'☆' * (3 - q['level'])}</div>"
        f"<div class='q'>{q['q']}</div>"
        "</div>")

    if q["type"] == "ox":
        with st.container(key="ox"):
            cols = st.columns(2)
            for i, opt in enumerate(q["options"]):
                with cols[i]:
                    st.button(opt, key=f"q{step}_{i}", on_click=choose, args=(i,), width="stretch")
    else:
        for i, opt in enumerate(q["options"]):
            st.button(f"{'ABCD'[i]}.  {opt}", key=f"q{step}_{i}", on_click=choose, args=(i,),
                      width="stretch")


# ── 화면: 결과 ────────────────────────────────
def result_view():
    qs, ans = st.session_state.questions, st.session_state.answers
    correct = [a == q["answer"] for q, a in zip(qs, ans)]
    score = sum(q["level"] for q, ok in zip(qs, correct) if ok)
    max_score = sum(q["level"] for q in qs)
    lv = get_level(score, max_score)
    level_idx = LEVELS.index(lv)
    st.query_params["lv"] = str(level_idx)

    level_poster(lv, level_idx, "당신의 금융 레벨은")
    html("<div class='stats'>"
         f"<div><div class='cap'>정답</div><div class='v'>{sum(correct)}<small>/{len(qs)}</small></div></div>"
         f"<div><div class='cap'>난이도 반영 점수</div><div class='v'>{score}<small>/{max_score}</small></div></div>"
         "</div>")

    html("<div class='section'>lineup <b>추천 상영작</b></div>")
    weak = [q["category"] for q, ok in zip(qs, correct) if not ok]
    for no, (w, tag) in enumerate(recommend(level_idx + 1, weak, k=4, seed=st.session_state.rec_seed), 1):
        work_film(w, tag, no)

    with st.expander("전체 상영 목록 둘러보기"):
        browse_works()

    html("<div class='section'>retake <b>오답 노트</b></div>")
    wrong = [(i, q, a) for i, (q, a, ok) in enumerate(zip(qs, ans, correct), 1) if not ok]
    if not wrong:
        st.success("전 장면 NG 없이 완벽한 원테이크! 👏")
    for i, q, a in wrong:
        with st.expander(f"SCENE {i:02d}.  {q['q']}"):
            html(f"<div class='note-row'><span class='k'>MY ANSWER</span>{q['options'][a]}</div>"
                 f"<div class='note-row'><span class='k'>ANSWER</span><b>{q['options'][q['answer']]}</b></div>")
            st.info(q["explain"])
            if q["link"]:
                st.caption(f"🎞 이 장면이 나오는 작품 — {q['link']}")

    html("<div class='section'>share <b>결과 공유</b></div>")
    share_url = f"{APP_URL}/?lv={level_idx}"
    st.code(share_url, language=None)   # 오른쪽 아이콘으로 복사
    tweet = f"[moneyvie] 나의 금융 레벨은 {lv['emoji']} {lv['name']}! 너도 해봐"
    st.link_button("X(트위터)에 공유", f"https://twitter.com/intent/tweet?text={quote(tweet)}&url={quote(share_url)}",
                   width="stretch")
    st.button("↺  다시 상영 (새 문제)", on_click=restart, width="stretch")
    html(credits([["the end"], ["moneyvie <b>presents</b>", "thanks for watching"]])
         + "<div class='fineprint'>※ 재미와 학습을 위한 테스트이며 투자 권유가 아닙니다.</div>")


# ── 라우팅 ────────────────────────────────────
step = st.session_state.step
lv_param = st.query_params.get("lv")

if step == 0 and lv_param in {str(i) for i in range(len(LEVELS))}:
    shared_view(int(lv_param))
elif step == 0:
    start_view()
elif step <= N_QUESTIONS:
    question_view(step)
else:
    result_view()
