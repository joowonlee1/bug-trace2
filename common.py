import json                                  # JSON 파일(오류 데이터)을 파이썬 자료로 바꾸는 모듈
from contextlib import contextmanager        # "with 함수():" 형태로 쓸 수 있는 함수를 만드는 도구
from html import escape                      # 글자 속 <, > 같은 기호를 안전하게 바꿔 주는 함수
from pathlib import Path                     # 파일 경로를 운영체제와 상관없이 다루는 도구
import streamlit as st                       # 웹앱을 만드는 라이브러리
DATA_PATH = Path(__file__).parent / "data" / "cases.json"
CATEGORIES = ["정수", "실수"]
CATEGORY_ICONS = {
    "전체": "layers",
    "정수": "pin",
    "실수": "percent",
}
CAUSE_TYPES = {
    "범위의 한계": "칸 수가 정해져 있어서 담을 수 있는 가장 큰 수와 가장 작은 수가 있다",
    "정밀도의 한계": "칸 수가 정해져 있어서 끝없이 이어지는 수나 아주 작은 수를 정확히 담지 못한다",
}
NAV_PAGES = [
    ("pages/catalog.py", "오류 도감", ":material/menu_book:"),
    ("pages/anatomy.py", "원인 해부실", ":material/layers:"),
    ("pages/laboratory.py", "현상 실험실", ":material/science:"),
    ("pages/compare.py", "오류 비교실", ":material/compare_arrows:"),
    ("pages/detection.py", "오류 검출", ":material/fact_check:"),
]
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
@st.cache_data
def load_cases():
    """cases.json 파일을 읽어서 사례 목록(딕셔너리들의 리스트)으로 돌려준다."""
    with open(DATA_PATH, encoding="utf-8") as file:
        return json.load(file)
def find_case(cases, case_id):
    """오류 목록에서 번호(id)가 같은 오류 하나를 찾아 돌려준다. 없으면 None."""
    for case in cases:                 # 목록을 처음부터 하나씩 확인
        if case["id"] == case_id:      # 번호가 같으면
            return case                # 그 오류를 바로 돌려준다
    return None                        # 끝까지 못 찾으면 None
def case_label(case):
    """선택 상자나 버튼에 보여 줄 이름을 만든다. 예) BUG-001 · 정수 오버플로 · 언더플로"""
    return f"BUG-{case['id']:03d} · {case['title']}"
def search_cases(cases, keyword, category):
    """검색어(keyword)와 분류(category)로 오류 목록을 걸러 낸다."""
    keyword = keyword.strip().lower()
    results = []
    for case in cases:
        if category != "전체" and case["category"] != category:
            continue
        term_names = [term["term"] for term in case["terms"]]
        searchable_text = " ".join(
            [case["title"], case["nickname"], case["tech"], case["summary"], case["symptom"]]
            + case["keywords"] + term_names
        ).lower()
        if keyword in searchable_text:
            results.append(case)
    return results
def open_case(case_id):
    """선택한 오류 번호를 기억해 두고 원인 해부실 페이지로 이동한다."""
    st.session_state["selected_case"] = case_id
    st.switch_page("pages/anatomy.py")
def render_html(code):
    """HTML 코드를 화면에 그린다."""
    lines = [line.strip() for line in code.splitlines()]
    clean_code = "\n".join(line for line in lines if line)
    st.markdown(clean_code, unsafe_allow_html=True)
def icon(name):
    """HTML 안에서 쓸 Material 아이콘 하나를 만든다. 예) icon("science") → 플라스크 모양"""
    return f'<span class="bt-icon">{escape(name)}</span>'
def toggle_window(state_name):
    """창 상태(최소화 'win_min' / 최대화 'win_max')를 켜고 끈다. True ↔ False"""
    st.session_state[state_name] = not st.session_state.get(state_name, False)
def show_window_buttons():
    """창 버튼 3개(— □ ×)를 진짜로 동작하게 만든다."""
    is_max = st.session_state.get("win_max", False)
    with st.container(key="win_btns", horizontal=True):
        st.button("—", key="win_min_btn", help="최소화 (내용 접기)", on_click=toggle_window, args=("win_min",))
        st.button("❐" if is_max else "□", key="win_max_btn", help="최대화 / 원래 크기", on_click=toggle_window, args=("win_max",))
        if st.button("×", key="win_close_btn", help="닫고 첫 화면으로"):
            st.session_state["win_min"] = False
            st.switch_page("pages/home.py")
