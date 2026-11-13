# =============================================================
# pages/home.py  (홈)
# 레트로 컴퓨터 화면으로 BUG TRACE를 소개하고,
# 대표 오류 3개와 각 페이지 이용 방법을 보여 준다.
# =============================================================

import streamlit as st

from common import CATEGORIES, case_card, find_case, load_cases, open_case, render_html

# 홈에서 보여 줄 대표 오류 번호 (가장 많이 겪는 오류 3개)
FEATURED_CASE_IDS = [1, 2, 3]

# 페이지 안내 내용: (페이지 이름, 설명)
PAGE_GUIDE = [
    ("오류 도감", "12가지 오류를 검색하고 분류별로 찾아봐요."),
    ("원인 해부실", "오류가 생기는 과정을 단계별로 해부해요."),
    ("현상 실험실", "설명한 원리를 실제 계산 결과로 확인해요."),
    ("오류 비교실", "두 오류의 원인과 공통점을 나란히 비교해요."),
]


def apply_retro_style():
    """홈에만 쓰는 레트로 컴퓨터(CRT 모니터) 디자인을 넣는다."""
    render_html("""
        <style>
        /* 모니터 전체를 가운데 정렬 */
        .crt-wrap { display: flex; flex-direction: column; align-items: center; margin: 10px 0 30px 0; }

        /* 모니터 바깥 틀 (베이지·회색 플라스틱 느낌) */
        .crt-body {
            width: 100%; max-width: 820px; padding: 22px; border-radius: 22px;
            background: linear-gradient(180deg, #3a382f 0%, #2a2922 100%);
            box-shadow: 0 18px 40px rgba(0, 0, 0, 0.55), inset 0 2px 0 rgba(255, 255, 255, 0.08);
        }

        /* 모니터 화면 (라임색 형광 글자 + 가운데가 밝은 화면) */
        .crt-screen {
            position: relative; overflow: hidden; border-radius: 14px; padding: 28px 32px; min-height: 300px;
            background: radial-gradient(ellipse at center, #1d2a10 0%, #10180a 70%, #060904 100%);
            color: #B7E66B; text-shadow: 0 0 6px rgba(183, 230, 107, 0.65);
            box-shadow: inset 0 0 50px rgba(0, 0, 0, 0.9);
        }

        /* 화면 위에 가로줄(주사선)을 덮어서 옛날 모니터처럼 보이게 한다. */
        .crt-screen::after {
            content: ""; position: absolute; inset: 0; pointer-events: none;
            background: repeating-linear-gradient(0deg, rgba(0, 0, 0, 0.25) 0px, rgba(0, 0, 0, 0.25) 1px, transparent 2px, transparent 4px);
        }

        /* 큰 로고와 부제목 */
        .crt-logo { font-family: 'VT323', monospace; font-size: 4rem; line-height: 1; margin-bottom: 4px; letter-spacing: 4px; }
        .crt-sub { font-family: 'Nanum Gothic Coding', monospace; font-size: 1rem; opacity: 0.85; margin-bottom: 18px; }

        /* 부팅 메시지: 처음엔 안 보이다가(opacity 0) 차례대로 나타난다. */
        .crt-line {
            font-family: 'Nanum Gothic Coding', monospace; font-size: 1rem; line-height: 1.9;
            opacity: 0; animation: crt-show 0.1s forwards;
        }
        .crt-line:nth-child(3) { animation-delay: 0.4s; }
        .crt-line:nth-child(4) { animation-delay: 0.9s; }
        .crt-line:nth-child(5) { animation-delay: 1.4s; }
        .crt-line:nth-child(6) { animation-delay: 1.9s; }
        .crt-line:nth-child(7) { animation-delay: 2.4s; }

        /* 오류 메시지는 빨간색 */
        .crt-err { color: #ff5c7a; text-shadow: 0 0 6px rgba(255, 92, 122, 0.7); }

        /* 깜빡이는 커서 */
        .crt-cursor { display: inline-block; width: 10px; height: 1.1em; background: #B7E66B; vertical-align: middle; animation: crt-blink 1s steps(1) infinite; }

        /* 모니터 받침대 */
        .crt-neck { width: 120px; height: 26px; background: #2a2922; }
        .crt-base { width: 300px; height: 16px; border-radius: 8px 8px 4px 4px; background: #3a382f; }

        /* 애니메이션 정의: 나타나기, 깜빡이기 */
        @keyframes crt-show { to { opacity: 1; } }
        @keyframes crt-blink { 50% { opacity: 0; } }
        </style>
    """)


def show_retro_computer(case_count):
    """레트로 컴퓨터 화면에 부팅 메시지처럼 앱을 소개한다."""
    # &gt; 는 HTML에서 '>' 기호를 뜻한다.
    render_html(f"""
        <div class="crt-wrap">
            <div class="crt-body">
                <div class="crt-screen">
                    <div class="crt-logo">BUG TRACE</div>
                    <div class="crt-sub">컴퓨터는 왜 이런 행동을 할까?</div>
                    <div class="crt-line">&gt; SYSTEM CHECK ............ OK</div>
                    <div class="crt-line">&gt; LOADING ERROR DATABASE .. {case_count} CASES FOUND</div>
                    <div class="crt-line">&gt; INPUT : 완선 → [Backspace] → ㅅ ㅓ ㅇ</div>
                    <div class="crt-line crt-err">&gt; OUTPUT: 완완성 &nbsp;!! UNEXPECTED BEHAVIOR DETECTED</div>
                    <div class="crt-line">&gt; 원인 분석을 시작합니다 <span class="crt-cursor"></span></div>
                </div>
            </div>
            <div class="crt-neck"></div>
            <div class="crt-base"></div>
        </div>
    """)


def show_introduction(case_count):
    """BUG TRACE가 어떤 웹앱인지 소개하고, 숫자 요약을 보여 준다."""
    st.markdown("## 디지털 오류 도감")
    st.markdown(
        "글자가 갑자기 두 번 써지고, 0.1과 0.2를 더했는데 0.3이 아니고, 사진이 옆으로 눕는 일. "
        "컴퓨터를 쓰다 보면 한 번쯤 겪는 이상한 현상들이에요.\n\n"
        "**BUG TRACE**는 이런 현상을 단순히 해결하는 데서 끝나지 않고, "
        "컴퓨터가 데이터를 **저장하고 처리하는 방식**과 연결해서 **왜** 그런 일이 생기는지 파헤치는 웹앱이에요."
    )

    # 화면을 3칸으로 나누고 칸마다 숫자 하나씩 보여 준다.
    count_column, category_column, page_column = st.columns(3)
    count_column.metric("수록된 오류", f"{case_count}개")
    category_column.metric("오류 분류", f"{len(CATEGORIES)}가지")
    page_column.metric("분석 페이지", f"{len(PAGE_GUIDE)}개")


def show_featured_cases(cases):
    """대표 오류 3개를 카드로 보여 주고, 버튼을 누르면 원인 해부실로 이동한다."""
    st.markdown("## 대표 오류")
    st.caption("가장 많이 겪는 오류부터 살펴보세요.")

    columns = st.columns(len(FEATURED_CASE_IDS))
    # zip(): 칸 목록과 오류 번호 목록을 하나씩 짝지어 반복한다.
    for column, case_id in zip(columns, FEATURED_CASE_IDS):
        case = find_case(cases, case_id)
        with column:
            with st.container(border=True):     # 테두리 있는 상자
                case_card(case)                 # 카드 내용 그리기
                # key: 버튼마다 서로 다른 이름을 붙여야 Streamlit이 구별할 수 있다.
                if st.button("원인 분석 →", key=f"home_open_{case_id}", use_container_width=True):
                    open_case(case_id)          # 번호를 기억하고 원인 해부실로 이동


def show_page_guide():
    """각 페이지가 무슨 일을 하는지 안내하고, 오류 도감으로 가는 버튼을 보여 준다."""
    st.markdown("## 이렇게 이용하세요")

    columns = st.columns(len(PAGE_GUIDE))
    for column, (page_name, description) in zip(columns, PAGE_GUIDE):
        with column:
            with st.container(border=True):
                st.markdown(f"**{page_name}**")
                st.caption(description)

    st.write("")  # 빈 줄(간격)
    if st.button("전체 오류 도감 열기 →", type="primary", use_container_width=True):
        st.switch_page("pages/catalog.py")


# ----- 실제 실행 순서 -----
all_cases = load_cases()                 # 오류 데이터 불러오기
apply_retro_style()                      # 레트로 디자인 적용
show_retro_computer(len(all_cases))      # 레트로 컴퓨터 화면
show_introduction(len(all_cases))        # 소개 + 숫자 요약
st.divider()                             # 구분선
show_featured_cases(all_cases)           # 대표 오류 3개
st.write("")
show_page_guide()                        # 페이지 안내
