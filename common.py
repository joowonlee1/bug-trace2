# =============================================================
# common.py
# 여러 페이지에서 함께 쓰는 데이터와 함수를 모아 둔 파일
# - 같은 코드를 페이지마다 반복해서 쓰지 않으려고 한곳에 모았다.
# - 각 페이지는 맨 위에서 "from common import ..."로 필요한 것만 가져다 쓴다.
# - 모든 페이지는 crt_frame() 안에 그려져서, 레트로 CRT 모니터 화면 속에 보인다.
# =============================================================

import json                                  # JSON 파일(오류 데이터)을 파이썬 자료로 바꾸는 모듈
from contextlib import contextmanager        # "with 함수():" 형태로 쓸 수 있는 함수를 만드는 도구
from html import escape                      # 글자 속 <, > 같은 기호를 안전하게 바꿔 주는 함수
from pathlib import Path                     # 파일 경로를 운영체제와 상관없이 다루는 도구

import streamlit as st                       # 웹앱을 만드는 라이브러리


# -------------------------------------------------------------
# 1. 상수(바뀌지 않는 값) 정의
# -------------------------------------------------------------

# 오류 데이터 파일 위치
# __file__ = 지금 이 파일(common.py)의 위치, .parent = 그 파일이 들어 있는 폴더
# 즉 "common.py와 같은 폴더 안의 data/cases.json"을 가리킨다.
DATA_PATH = Path(__file__).parent / "data" / "cases.json"

# 사례 분류 목록 (오류 도감의 분류 버튼에 사용) — 탐구 순서: 정수 → 실수
CATEGORIES = ["정수", "실수"]

# 분류마다 붙일 아이콘 (Streamlit이 제공하는 Material 아이콘 이름)
CATEGORY_ICONS = {
    "전체": "layers",
    "정수": "pin",
    "실수": "percent",
}

# 원인 유형 이름과 설명 (딕셔너리: "이름": "설명") — 오류 도감 카드와 오류 비교실에서 사용
CAUSE_TYPES = {
    "범위의 한계": "칸 수가 정해져 있어서 담을 수 있는 가장 큰 수와 가장 작은 수가 있다",
    "정밀도의 한계": "칸 수가 정해져 있어서 끝없이 이어지는 수나 아주 작은 수를 정확히 담지 못한다",
}

# 모니터 화면 위쪽 메뉴: (페이지 파일, 메뉴 이름, 아이콘)
# 첫 화면(홈)으로는 창의 × 버튼과 전원 버튼으로 돌아가므로 메뉴에는 넣지 않는다.
NAV_PAGES = [
    ("pages/catalog.py", "오류 도감", ":material/menu_book:"),
    ("pages/anatomy.py", "원인 해부실", ":material/layers:"),
    ("pages/laboratory.py", "현상 실험실", ":material/science:"),
    ("pages/compare.py", "오류 비교실", ":material/compare_arrows:"),
    ("pages/detection.py", "오류 검출", ":material/fact_check:"),
]

# 픽셀 아트 컴퓨터 그림 (웃는 얼굴 모니터) - 창 제목 줄과 홈 화면에서 사용
# SVG의 <rect>(사각형)를 1칸짜리 픽셀처럼 쌓아서 그린다.
# shape-rendering="crispEdges": 사각형 가장자리를 흐리지 않고 또렷하게 그린다.
PIXEL_COMPUTER_SVG = """
<svg class="px-computer" viewBox="0 0 40 30" shape-rendering="crispEdges" xmlns="http://www.w3.org/2000/svg">
<g fill="#1F4D25">
<rect x="2" y="9" width="4" height="1"/><rect x="3" y="5" width="2" height="1"/><rect x="5" y="6" width="1" height="1"/>
<rect x="3" y="13" width="2" height="1"/><rect x="5" y="12" width="1" height="1"/>
<rect x="34" y="9" width="4" height="1"/><rect x="35" y="5" width="2" height="1"/><rect x="34" y="6" width="1" height="1"/>
<rect x="35" y="13" width="2" height="1"/><rect x="34" y="12" width="1" height="1"/>
<rect x="10" y="1" width="20" height="18"/><rect x="8" y="20" width="24" height="7"/>
</g>
<rect x="11" y="2" width="18" height="16" fill="#E9F2C4"/>
<rect x="13" y="4" width="14" height="11" fill="#1F4D25"/>
<rect x="14" y="5" width="12" height="9" fill="#C6EA4E"/>
<g fill="#1F4D25">
<rect x="17" y="7" width="1" height="2"/><rect x="22" y="7" width="1" height="2"/>
<rect x="17" y="10" width="1" height="1"/><rect x="18" y="11" width="4" height="1"/><rect x="22" y="10" width="1" height="1"/>
</g>
<rect x="9" y="21" width="22" height="5" fill="#E9F2C4"/>
<g fill="#1F4D25"><rect x="11" y="23" width="1" height="1"/><rect x="13" y="23" width="1" height="1"/><rect x="22" y="23" width="7" height="1"/></g>
</svg>
"""


# -------------------------------------------------------------
# 2. 데이터 관련 함수
# -------------------------------------------------------------

# @st.cache_data: 한 번 읽은 결과를 저장(캐시)해 두는 기능
# → 페이지를 이동할 때마다 파일을 다시 읽지 않아서 빠르다.
@st.cache_data
def load_cases():
    """cases.json 파일을 읽어서 사례 목록(딕셔너리들의 리스트)으로 돌려준다."""
    # encoding="utf-8": 한글이 깨지지 않도록 UTF-8 규칙으로 읽는다.
    with open(DATA_PATH, encoding="utf-8") as file:
        return json.load(file)


def find_case(cases, case_id):
    """오류 목록에서 번호(id)가 같은 오류 하나를 찾아 돌려준다. 없으면 None."""
    for case in cases:                 # 목록을 처음부터 하나씩 확인
        if case["id"] == case_id:      # 번호가 같으면
            return case                # 그 오류를 바로 돌려준다
    return None                        # 끝까지 못 찾으면 None
