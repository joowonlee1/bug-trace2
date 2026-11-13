# =============================================================
# common.py
# 여러 페이지에서 함께 쓰는 데이터와 함수를 모아 둔 파일
# - 같은 코드를 페이지마다 반복해서 쓰지 않으려고 한곳에 모았다.
# - 각 페이지는 맨 위에서 "from common import ..."로 필요한 것만 가져다 쓴다.
# =============================================================

import json                      # JSON 파일(오류 데이터)을 파이썬 자료로 바꾸는 모듈
from html import escape          # 글자 속 <, > 같은 기호를 안전하게 바꿔 주는 함수
from pathlib import Path         # 파일 경로를 운영체제와 상관없이 다루는 도구

import streamlit as st           # 웹앱을 만드는 라이브러리


# -------------------------------------------------------------
# 1. 상수(바뀌지 않는 값) 정의
# -------------------------------------------------------------

# 오류 데이터 파일 위치
# __file__ = 지금 이 파일(common.py)의 위치
# .parent  = 그 파일이 들어 있는 폴더
# 즉 "common.py와 같은 폴더 안의 data/cases.json"을 가리킨다.
DATA_PATH = Path(__file__).parent / "data" / "cases.json"

# 오류 분류 목록 (오류 도감의 분류 버튼, 막대그래프에 사용)
CATEGORIES = ["입력", "숫자", "문자", "이미지", "파일", "화면", "시간"]

# 원인 유형 이름과 설명 (딕셔너리: "이름": "설명")
# 오류 비교실에서 두 오류의 원인 유형을 설명할 때 사용한다.
CAUSE_TYPES = {
    "상태 불일치": "두 곳이 기억하는 정보가 서로 달라서 생기는 오류",
    "표현의 한계": "컴퓨터가 정보를 완벽하게 저장할 수 없어서 생기는 오류",
    "규칙 불일치": "저장할 때와 읽을 때 쓰는 규칙이 달라서 생기는 오류",
    "보이지 않는 정보": "화면에 안 보이는 정보 때문에 생기는 오류",
    "자동 해석": "컴퓨터가 데이터의 종류를 스스로 짐작하다가 생기는 오류",
    "환경 차이": "기기나 지역 같은 환경이 달라서 생기는 오류",
}


# -------------------------------------------------------------
# 2. 데이터 관련 함수
# -------------------------------------------------------------

# @st.cache_data: 한 번 읽은 결과를 저장(캐시)해 두는 기능
# → 페이지를 이동할 때마다 파일을 다시 읽지 않아서 빠르다.
@st.cache_data
def load_cases():
    """cases.json 파일을 읽어서 오류 목록(딕셔너리들의 리스트)으로 돌려준다."""
    # encoding="utf-8": 한글이 깨지지 않도록 UTF-8 규칙으로 읽는다. (CASE 03과 관련!)
    with open(DATA_PATH, encoding="utf-8") as file:
        return json.load(file)


def find_case(cases, case_id):
    """오류 목록에서 번호(id)가 같은 오류 하나를 찾아 돌려준다. 없으면 None."""
    for case in cases:                 # 목록을 처음부터 하나씩 확인
        if case["id"] == case_id:      # 번호가 같으면
            return case                # 그 오류를 바로 돌려준다
    return None                        # 끝까지 못 찾으면 None


def case_label(case):
    """선택 상자나 버튼에 보여 줄 이름을 만든다. 예) CASE 01 · 완선이 완완으로 바뀜"""
    # :02d → 숫자를 두 자리로 맞춘다. (1 → 01)
    return f"CASE {case['id']:02d} · {case['title']}"


def search_cases(cases, keyword, category):
    """검색어(keyword)와 분류(category)로 오류 목록을 걸러 낸다."""
    # 앞뒤 공백을 지우고 소문자로 바꿔서 "IME"와 "ime"를 같은 검색어로 본다.
    keyword = keyword.strip().lower()
    results = []

    for case in cases:
        # 조건 1) 분류: "전체"가 아니고 분류가 다르면 건너뛴다.
        if category != "전체" and case["category"] != category:
            continue

        # 조건 2) 검색어: 제목, 기술, 요약, 증상, 키워드를 한 문장으로 합친 뒤 검색한다.
        searchable_text = " ".join(
            [case["title"], case["tech"], case["summary"], case["symptom"]]
            + case["keywords"]
        ).lower()

        # 검색어가 비어 있으면 ""는 모든 글자 안에 있으므로 전부 통과한다.
        if keyword in searchable_text:
            results.append(case)

    return results


# -------------------------------------------------------------
# 3. 페이지 이동 함수
# -------------------------------------------------------------

def open_case(case_id):
    """선택한 오류 번호를 기억해 두고 원인 해부실 페이지로 이동한다."""
    # st.session_state: 페이지를 옮겨도 사라지지 않는 저장 공간 (상태 관리)
    st.session_state["selected_case"] = case_id
    st.switch_page("pages/anatomy.py")


# -------------------------------------------------------------
# 4. 화면 그리기 함수
# -------------------------------------------------------------

def render_html(code):
    """HTML 코드를 화면에 그린다."""
    # 줄 앞의 공백이 4칸 이상이면 마크다운이 '코드 블록'으로 착각해서
    # HTML이 글자 그대로 보인다. 그래서 줄마다 앞뒤 공백을 지우고,
    # 빈 줄도 지워서 HTML이 중간에 끊기지 않게 한다.
    lines = [line.strip() for line in code.splitlines()]
    clean_code = "\n".join(line for line in lines if line)
    # unsafe_allow_html=True: 마크다운 안에서 HTML 태그를 쓸 수 있게 허용
    st.markdown(clean_code, unsafe_allow_html=True)


def page_header(path, title, description):
    """내부 페이지 맨 위에 터미널 스타일 제목을 그린다."""
    # escape(): 글자 속 <, > 같은 기호가 HTML 태그로 오해되지 않게 바꾼다.
    render_html(f"""
        <div class="bt-header">
            <div class="bt-path">bug-trace:~/{escape(path)}$</div>
            <h1 class="bt-title">{escape(title)}</h1>
            <p class="bt-desc">{escape(description)}</p>
        </div>
    """)


def case_card(case):
    """오류 카드 한 장의 내용(번호, 분류, 제목, 기술, 요약)을 그린다."""
    render_html(f"""
        <div class="bt-card">
            <div class="bt-card-top">
                <span class="bt-no">CASE {case['id']:02d}</span>
                <span class="bt-tag">{escape(case['category'])}</span>
            </div>
            <div class="bt-card-title">{escape(case['title'])}</div>
            <div class="bt-card-tech">{escape(case['tech'])}</div>
            <div class="bt-card-summary">{escape(case['summary'])}</div>
        </div>
    """)


def apply_style():
    """앱 전체에 적용할 디자인(CSS)을 넣는다. → 현대적인 다크 터미널 스타일"""
    render_html("""
        <style>
        /* 1) 글꼴 불러오기: 코딩용 한글 글꼴, 본문 한글 글꼴, 레트로 영문 글꼴 */
        @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic+Coding:wght@400;700&family=Noto+Sans+KR:wght@400;500;700&family=VT323&display=swap');

        /* 2) 자주 쓰는 색을 변수로 정해 둔다. */
        :root {
            --bt-bg: #0a0e14;        /* 배경 */
            --bt-panel: #111821;     /* 상자 배경 */
            --bt-line: #1f2a37;      /* 테두리 */
            --bt-text: #d7e0ea;      /* 기본 글자 */
            --bt-dim: #8393a7;       /* 흐린 글자 */
            --bt-lime: #B7E66B;      /* 대표 강조 색(라임) - B안 확정 색 */
            --bt-lime-soft: rgba(183, 230, 107, 0.14);   /* 라임색 옅은 배경 */
            --bt-lime-line: rgba(183, 230, 107, 0.45);   /* 라임색 옅은 테두리 */
            --bt-red: #ff5c7a;       /* 오류(빨강) */
            --bt-yellow: #ffd166;    /* 핵심·추정(노랑) */
            --bt-sky: #8fc7ff;       /* 직접 관찰(하늘색) */
        }

        /* 3) 본문 글꼴, 제목 글꼴 */
        .stMarkdown p, .stMarkdown li, .stTextInput input, .stTabs button p {
            font-family: 'Noto Sans KR', sans-serif;
        }
        code, pre, .bt-path, .bt-no, .bt-tag {
            font-family: 'Nanum Gothic Coding', monospace !important;
        }
        h1, h2, h3, h4 {
            font-family: 'Nanum Gothic Coding', monospace !important;
            letter-spacing: -0.5px;
        }
        .block-container { padding-top: 2.5rem; max-width: 1100px; }

        /* 4) 페이지 제목 (bug-trace:~/catalog$ 부분) */
        .bt-header { border-bottom: 1px solid var(--bt-line); padding-bottom: 14px; margin-bottom: 22px; }
        .bt-path { color: var(--bt-lime); font-size: 0.9rem; }
        .bt-title { color: var(--bt-text); font-size: 2.1rem; margin: 4px 0 6px 0; padding: 0; }
        .bt-desc { color: var(--bt-dim); margin: 0; }

        /* 5) 오류 카드 */
        .bt-card { min-height: 150px; }
        .bt-card-top { display: flex; justify-content: space-between; align-items: center; }
        .bt-no { color: var(--bt-lime); font-size: 0.85rem; }
        .bt-tag {
            color: var(--bt-lime); font-size: 0.75rem;
            border: 1px solid var(--bt-lime-line); border-radius: 4px; padding: 1px 8px;
        }
        .bt-card-title { color: var(--bt-text); font-size: 1.15rem; font-weight: 700; margin-top: 8px; }
        .bt-card-tech { color: var(--bt-lime); font-size: 0.85rem; margin: 2px 0 8px 0; opacity: 0.85; }
        .bt-card-summary { color: var(--bt-dim); font-size: 0.9rem; line-height: 1.55; }

        /* 6) 설명 상자 (정상 = 라임, 오류 = 빨강, 핵심 = 노랑, 직접 관찰 = 하늘) */
        .bt-box {
            background: var(--bt-panel); border: 1px solid var(--bt-line);
            border-radius: 8px; padding: 16px 18px; margin-bottom: 12px; color: var(--bt-text);
        }
        .bt-box-label { font-family: 'Nanum Gothic Coding', monospace; font-size: 0.8rem; margin-bottom: 6px; }
        .bt-ok { border-left: 3px solid var(--bt-lime); }
        .bt-ok .bt-box-label { color: var(--bt-lime); }
        .bt-obs { border-left: 3px solid var(--bt-sky); }
        .bt-obs .bt-box-label { color: var(--bt-sky); }
        .bt-err { border-left: 3px solid var(--bt-red); }
        .bt-err .bt-box-label { color: var(--bt-red); }
        .bt-key { border-left: 3px solid var(--bt-yellow); }
        .bt-key .bt-box-label { color: var(--bt-yellow); }

        /* 7) 발생 과정 단계 (01 → 02 → 03 흐름) */
        .bt-step { display: flex; gap: 14px; align-items: flex-start; margin-bottom: 0; }
        .bt-step-no {
            flex: 0 0 34px; height: 34px; border-radius: 6px; text-align: center; line-height: 34px;
            background: var(--bt-lime-soft); color: var(--bt-lime);
            font-family: 'Nanum Gothic Coding', monospace; font-weight: 700;
        }
        .bt-step-text { line-height: 1.65; padding-top: 4px; }
        .bt-arrow { color: var(--bt-lime); opacity: 0.5; padding: 2px 0 2px 26px; font-size: 0.9rem; line-height: 1.1; }

        /* 7-1) 단계별 근거 이름표 (문서로 확인 = 라임, 추정 = 노랑) */
        .bt-basis {
            display: inline-block; font-family: 'Nanum Gothic Coding', monospace; font-size: 0.75rem;
            border-radius: 4px; padding: 1px 8px; margin-bottom: 4px;
        }
        .bt-basis-ok { color: var(--bt-lime); border: 1px solid var(--bt-lime-line); }
        .bt-basis-guess { color: var(--bt-yellow); border: 1px solid rgba(255, 209, 102, 0.5); }

        /* 8) 작은 이름표 (CASE 01, 분류, 기술 등) */
        .bt-badge {
            display: inline-block; font-family: 'Nanum Gothic Coding', monospace; font-size: 0.8rem;
            border: 1px solid var(--bt-line); border-radius: 4px; padding: 2px 10px; margin: 0 6px 6px 0;
            color: var(--bt-dim);
        }
        .bt-badge-on { color: var(--bt-lime); border-color: var(--bt-lime-line); }

        /* 9) 테두리 있는 상자와 버튼 */
        div[data-testid="stVerticalBlockBorderWrapper"] { background: var(--bt-panel); }
        .stButton > button { font-family: 'Nanum Gothic Coding', monospace; }
        /* 라임색 버튼 위의 글자는 어두운 색으로 (밝은 배경에 흰 글자는 잘 안 보임) */
        .stButton > button[kind="primary"], .stButton > button[kind="primary"] p { color: #0a0e14; }
        /* 링크 색도 라임으로 통일 */
        .stMarkdown a { color: var(--bt-lime); }

        /* =====================================================
           BUG TRACE / CRT ACCESSIBLE DESIGN UPGRADE
           CSS only: data, copy, calculations and event logic unchanged.
           ===================================================== */
        :root {
            --bt-bg: #101417;
            --bt-panel: #1C2529;
            --bt-line: #46554A;
            --bt-text: #E9EDE7;
            --bt-dim: #BFCBC1;
        }
        html, body, [data-testid="stAppViewContainer"] {
            background: var(--bt-bg);
        }
        [data-testid="stAppViewContainer"] > .main {
            background-image: radial-gradient(ellipse at 60% -25%, rgba(183,230,107,.075), transparent 55%);
        }
        .block-container { max-width: 1280px; padding: 2.2rem 2.6rem 5rem; }
        .stMarkdown p, .stMarkdown li, .stCaption, [data-testid="stWidgetLabel"] p,
        [data-testid="stMarkdownContainer"] p { font-size: 1rem; line-height: 1.72; }
        h1,h2,h3,h4,.bt-title { font-family: 'Noto Sans KR',sans-serif !important; font-weight: 800 !important; line-height: 1.35 !important; }
        .bt-title { font-size: clamp(1.8rem, 3vw, 2.5rem); }
        .bt-desc { color: var(--bt-dim); font-size: 1.05rem; line-height: 1.7; }
        .bt-header { border-bottom: 1px solid #42543e; padding-bottom: 22px; margin-bottom: 28px; }
        .bt-path { font-size: .94rem; font-weight: 700; letter-spacing: .035em; }
        .bt-card { min-height: 175px; }
        .bt-card-title { font-size: 1.22rem; font-weight: 800; line-height: 1.45; }
        .bt-card-tech { font-size: .94rem; font-weight: 700; opacity: 1; }
        .bt-card-summary { font-size: 1rem; color: var(--bt-dim); line-height: 1.7; }
        .bt-no,.bt-tag,.bt-badge { font-size: .9rem; font-weight: 700; }
        .bt-tag { padding: 5px 10px; border-radius: 8px; }
        .bt-box { padding: 20px 22px; border-radius: 13px; line-height: 1.75; }
        .bt-box-label,.bt-basis { font-size: .9rem; font-weight: 700; }
        .bt-step-no { flex-basis: 42px; height: 42px; line-height: 42px; border-radius: 9px; }
        .bt-step-text { font-size: 1rem; }

        /* Real Streamlit controls: large click targets, bold readable labels */
        div.stButton > button, div.stLinkButton > a,
        div[data-testid="stFormSubmitButton"] button {
            min-height: 54px; padding: 11px 20px; border-radius: 12px;
            font-family: 'Noto Sans KR',sans-serif !important;
            font-size: 1.07rem !important; font-weight: 800 !important;
            letter-spacing: -.015em; border: 1.5px solid #6c8a58;
            background: #202b27; color: #eef4e8;
            transition: background-color .14s ease, border-color .14s ease, box-shadow .14s ease;
        }
        div.stButton > button p, div.stLinkButton > a p,
        div[data-testid="stFormSubmitButton"] button p {
            font-size: 1.07rem !important; font-weight: 800 !important;
            line-height: 1.4 !important;
        }
        div.stButton > button:hover, div.stLinkButton > a:hover {
            border-color: #B7E66B; background: #2d3c2d;
            box-shadow: 0 0 0 2px rgba(183,230,107,.12);
        }
        div.stButton > button[kind="primary"],
        div.stButton > button[data-testid="stBaseButton-primary"],
        div[data-testid="stFormSubmitButton"] button[kind="primary"] {
            background: #B7E66B; border-color: #B7E66B; color: #101417;
        }
        div.stButton > button[kind="primary"] p,
        div.stButton > button[data-testid="stBaseButton-primary"] p { color: #101417 !important; }
        div.stButton > button[kind="primary"]:hover { background: #cef48d; }
        button:focus-visible, input:focus-visible, textarea:focus-visible {
            outline: 3px solid #B7E66B !important; outline-offset: 3px;
        }

        /* Radio choices rendered as large segmented filter chips, not tiny circles */
        div[data-testid="stRadio"] > div[role="radiogroup"] {
            display: flex; flex-wrap: wrap; gap: 10px 12px;
            align-items: stretch;
        }
        div[data-testid="stRadio"] > div[role="radiogroup"] > label {
            display: inline-flex; align-items: center; justify-content: center;
            min-height: 49px; min-width: 88px; padding: 9px 17px;
            border: 1.5px solid #5b7654; border-radius: 12px;
            background: #1c2923; cursor: pointer; margin: 0;
            transition: background-color .14s ease, border-color .14s ease;
        }
        div[data-testid="stRadio"] > div[role="radiogroup"] > label:hover {
            background: #2a3c2d; border-color: #B7E66B;
        }
        div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) {
            background: #B7E66B; border-color: #B7E66B;
        }
        div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) p {
            color: #101417 !important;
        }
        div[data-testid="stRadio"] > div[role="radiogroup"] > label p {
            font-size: 1.02rem !important; font-weight: 800 !important;
            color: #E9EDE7; line-height: 1.4 !important;
        }
        div[data-testid="stRadio"] > div[role="radiogroup"] > label > div:first-child {
            width: 0; height: 0; overflow: hidden; margin: 0; padding: 0;
        }
        div[data-testid="stRadio"] > div[role="radiogroup"] > label:focus-within {
            outline: 2px solid #e3f8bb; outline-offset: 2px;
        }

        /* Inputs and select controls */
        div[data-baseweb="input"] > div, div[data-baseweb="select"] > div,
        div[data-baseweb="textarea"] > div {
            min-height: 50px; border-radius: 11px;
            background-color: #18211f; border-color: #61745e;
        }
        div[data-baseweb="input"] input, div[data-baseweb="select"] *,
        div[data-baseweb="textarea"] textarea {
            font-family: 'Noto Sans KR',sans-serif !important;
            font-size: 1.04rem !important;
        }
        [data-testid="stWidgetLabel"] p { font-weight: 700 !important; color: #E9EDE7; }
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 14px; border-color: #46554A;
        }
        div[data-testid="stCodeBlock"], pre {
            border-radius: 12px; font-size: 1rem !important;
        }
        [data-testid="stSidebar"] { background: #121c19; border-right: 1px solid #354b35; }
        [data-testid="stSidebarNav"] a { min-height: 48px; border-radius: 9px; }
        [data-testid="stSidebarNav"] a span { font-size: 1rem; font-weight: 700; }
        [data-testid="stSidebarNav"] a[aria-current="page"] { background: #30462a; }
        [data-testid="stTabs"] button { min-height: 52px; }
        [data-testid="stTabs"] button p { font-weight: 800 !important; font-size: 1rem !important; }
        @media (max-width: 800px) {
            .block-container { padding: 1.4rem 1rem 4rem; }
            .bt-title { font-size: 1.75rem; }
            .bt-card-title { font-size: 1.12rem; }
            div[data-testid="stRadio"] > div[role="radiogroup"] > label { min-width: 78px; padding: 9px 12px; }
            div.stButton > button { min-height: 52px; }
        }
        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after { transition-duration: 0.01ms !important; animation-duration: 0.01ms !important; }
        }
        </style>
    """)
