# =============================================================
# streamlit_app.py  (시작 파일)
# BUG TRACE 웹앱이 실행되면 가장 먼저 이 파일이 실행된다.
# 하는 일: 기본 설정 → 공통 디자인 적용 → 페이지 목록 등록 → 선택한 페이지 실행
# =============================================================

import streamlit as st

from common import apply_style   # 공통 디자인(CSS)을 넣는 함수


def setup_page():
    """브라우저 탭 제목, 아이콘, 화면 너비를 설정한다."""
    # set_page_config는 반드시 다른 Streamlit 명령보다 먼저 실행해야 한다.
    st.set_page_config(
        page_title="BUG TRACE",   # 브라우저 탭에 보이는 제목
        page_icon="🐞",           # 브라우저 탭 아이콘
        layout="wide",            # 화면을 넓게 사용
    )


def create_pages():
    """pages 폴더 안의 파일들을 페이지로 등록하고 목록으로 돌려준다."""
    # st.Page(파일 경로, title=메뉴 이름, icon=메뉴 아이콘)
    # default=True → 처음 접속했을 때 보여 줄 페이지
    return [
        st.Page("pages/home.py", title="홈", icon=":material/terminal:", default=True),
        st.Page("pages/catalog.py", title="오류 도감", icon=":material/menu_book:"),
        st.Page("pages/anatomy.py", title="원인 해부실", icon=":material/biotech:"),
        st.Page("pages/laboratory.py", title="현상 실험실", icon=":material/science:"),
        st.Page("pages/compare.py", title="오류 비교실", icon=":material/compare_arrows:"),
    ]


def show_sidebar_info():
    """왼쪽 사이드바에 앱 이름과 소개 문구를 보여 준다."""
    with st.sidebar:
        st.markdown("### 🐞 BUG TRACE")
        st.caption("컴퓨터는 왜 이런 행동을 할까?")


# ----- 실제 실행 순서 -----
setup_page()                              # 1) 기본 설정
apply_style()                             # 2) 모든 페이지에 공통 디자인 적용
show_sidebar_info()                       # 3) 사이드바 소개 문구
current_page = st.navigation(create_pages())  # 4) 메뉴를 만들고, 사용자가 고른 페이지를 받는다
current_page.run()                        # 5) 고른 페이지의 코드를 실행한다
