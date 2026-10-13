# 🎞️ moneyvie

> **money + movie** — 금융 레벨 테스트

금융 상식 10문제로 나의 금융 레벨을 확인하고, 레벨에 맞는 영화·드라마를 추천받는 Streamlit 웹앱입니다.

## 기능
- 23문항 문제은행에서 8개 분야(기초 개념, 예금·저축, 투자, 경제 지표, 신용·대출, 세금·제도, 금융 안전, 경제사)가 고르게 섞이도록 10문항 출제
- 객관식 · OX · 계산 · 상황형 문제, 난이도별 가중 점수
- 결과: 금융 새싹 / 금융 탐험가 / 금융 고수
- 추천: 작품 33편(영화·드라마·다큐·애니, 6개국, 1987~2023) 중 형식·국가·분위기·시대가 겹치지 않게 4편, 틀린 분야를 보완하는 작품 우선 + 한 단계 위 도전작
- 전체 작품 둘러보기 (형식·레벨 필터)
- 오답 노트(해설 + 관련 작품), 공유 링크(`?lv=0~2`)

## 실행
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 파일 구조
```
app.py                 화면 흐름 (시작 → 문제 → 결과)
data.py                문제은행, 레벨, 출제 로직
works.py               추천 작품 33편, 다양성 추천 로직
style.css              필름 포스터 디자인
static/                SUIT 글꼴 (woff2, SIL OFL)
requirements.txt
.streamlit/config.toml 테마 색상, 글꼴 등록, static 서빙 설정
```

## 배포 (Streamlit Community Cloud)
1. 이 저장소를 GitHub에 Public으로 올리기
2. share.streamlit.io → Create app → 저장소 / `main` / `app.py` 선택 → Deploy
3. 발급된 주소를 `app.py`의 `APP_URL`에 넣고 다시 push

## 안내
재미와 학습을 위한 테스트이며 투자 권유가 아닙니다.
제도 관련 문항(예: 예금자보호 한도 1억 원, 2025.9.1 시행)은 바뀔 수 있으니 주기적으로 확인하세요.

## 글꼴
[SUIT](https://sun.fo/suit/) (SIL Open Font License) — `static/SUIT-LICENSE.txt`
