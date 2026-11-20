# =============================================================
# pages/anatomy.py  (원인 해부실)
# 오류 하나를 골라 위에서 아래로 '추적 순서'대로 분석한다.
#   ① 제목 → ② 핵심 원리(가장 크게) → ③ 먼저 알아 둘 용어 → ④ 증상 · 정상이라면 · 실제로는 (+ 직접 관찰)
#   → ⑤ 처리 과정(입력 → 처리 → 출력) → ⑥ 원인 추적 기록 #01~#05 (문서로 확인 = 누르면 문서가 열림 / 추정)
#   → ⑦ 관련 영상(있을 때만) → ⑧ 실험실 버튼 → ⑨ 출처 → ⑩ 탭: 자주 생기는 곳 / 해결 방법 / 관련 사례
# =============================================================

from html import escape           # 글자 속 <, > 기호를 안전하게 바꾸는 함수

import streamlit as st

from common import case_label, crt_frame, find_case, icon, load_cases, page_banner, render_html


# -------------------------------------------------------------
# 초보자용 기초 안내: 오류 사례를 반복하지 않고 저장 원리만 설명한다.
# -------------------------------------------------------------

def show_beginner_guide():
    """기초 학습 안내서: 읽기 편한 교재형 레이아웃, 기존 7개 탭 유지."""
    with st.container(key="beginner_guide"):
        with st.expander("▣ 처음이라면? 기초부터 시작하기", expanded=False):
            st.caption("비트와 2진수부터 오류 검출까지 · 필요한 주제만 선택해서 읽어 보세요.")
            tabs = st.tabs([
                "비트와 2진수", "비트 수와 범위", "음수와 2의 보수",
                "비트 연산", "2진 소수", "IEEE 754", "오류 검출 기초",
            ])

            with tabs[0]:
                st.markdown("### 비트는 0 또는 1을 담는 한 칸")
                st.markdown(
                    "**1비트(bit)**는 0 또는 1을 저장하는 한 칸이에요. "
                    "**8비트 = 1바이트(byte)**이고, 8비트로 만들 수 있는 조합은 **256가지**예요.\\n\\n"
                    "10진수는 오른쪽부터 1, 10, 100…의 자리 값을 사용하지만, "
                    "2진수는 오른쪽부터 **1, 2, 4, 8, 16…**의 자리 값을 사용해요."
                )
                st.markdown("#### 13을 8비트 2진수로 표현하기")
                st.markdown("""
<div class="btg-bits">
  <div><small>128</small><span>0</span></div>
  <div><small>64</small><span>0</span></div>
  <div><small>32</small><span>0</span></div>
  <div><small>16</small><span>0</span></div>
  <div class="active"><small>8</small><span>1</span></div>
  <div class="active"><small>4</small><span>1</span></div>
  <div><small>2</small><span>0</span></div>
  <div class="active"><small>1</small><span>1</span></div>
</div>
<div class="btg-result">8 + 4 + 1 = <strong>13</strong> <span>→ 00001101₂</span></div>
""", unsafe_allow_html=True)
                st.markdown("반대로 `00001010`은 8과 2 자리에 1이 있으므로 **10**이에요.")

            with tabs[1]:
                st.markdown("### 비트가 늘어나면 표현할 수 있는 조합도 늘어나요")
                st.markdown("비트 하나에는 0과 1, 두 가지 상태가 있어요. 따라서 **n비트의 전체 조합 수는 2ⁿ가지**예요.")
                st.markdown("""
<div class="btg-table-wrap"><table class="btg-table">
<thead><tr><th>비트 수</th><th>가능한 조합 수</th></tr></thead>
<tbody>
<tr><td>8비트</td><td>256가지 (2⁸)</td></tr>
<tr><td>32비트</td><td>4,294,967,296가지 (2³²)</td></tr>
<tr><td>64비트</td><td>18,446,744,073,709,551,616가지 (2⁶⁴)</td></tr>
</tbody></table></div>
""", unsafe_allow_html=True)
                st.markdown(
                    "하지만 **조합 수가 곧 양수의 최댓값은 아니에요.** "
                    "같은 8비트라도 부호 없는 정수는 **0~255**, 2의 보수로 표현한 부호 있는 정수는 "
                    "**−128~127**을 나타내요. 모두 256가지 값이에요.\\n\\n"
                    "또한 32비트 정수와 32비트 실수는 저장 규칙이 달라요. "
                    "비트 수만 보고 정확도나 범위를 단정하면 안 돼요."
                )

            with tabs[2]:
                st.markdown("### 음수는 어떻게 비트로 저장할까요?")
                st.markdown(
                    "비트에는 `−` 기호를 직접 적지 않아요. 그래서 부호 있는 정수는 보통 "
                    "**2의 보수(two's complement)** 규칙으로 해석해요. "
                    "8비트에서 맨 앞 비트가 0이면 0 이상, 1이면 음수로 해석돼요."
                )
                st.markdown("#### 5를 −5로 바꾸기")
                st.code("5의 8비트 표현   00000101\\n0과 1 뒤집기    11111010\\n1 더하기        11111011  →  −5", language=None)
                st.markdown(
                    "8비트 2의 보수에서 맨 앞 자리의 값은 **−128**, 나머지는 64, 32, 16, 8, 4, 2, 1이에요.\\n\\n"
                    "`11111011` = −128 + 64 + 32 + 16 + 8 + 2 + 1 = **−5**\\n\\n"
                    "따라서 8비트 부호 있는 정수의 범위는 **−128~127**이에요. 0이 포함되므로 음수 쪽이 한 개 더 많아요."
                )

            with tabs[3]:
                st.markdown("### 비트 연산은 0과 1을 직접 다루는 계산이에요")
                st.markdown(
                    "**AND (`&`)** — 두 비트가 모두 1일 때만 1이에요. `1100 & 1010 = 1000`\\n\\n"
                    "**XOR (`^`)** — 두 비트가 다를 때만 1이에요. `1100 ^ 1010 = 0110`\\n\\n"
                    "**NOT (`~`)** — 비트를 뒤집어요. 4비트 기준 `1100 → 0011`\\n\\n"
                    "**왼쪽 시프트 (`<<`)** — 비트를 왼쪽으로 옮겨요. `0011 << 1 = 0110`"
                )
                st.markdown(
                    "Python의 `~` 연산은 정수의 비트 폭을 고정하지 않으므로, "
                    "4비트 결과를 얻으려면 별도 마스크가 필요해요. "
                    "고정 비트 폭에서 시프트하면 범위를 벗어난 상위 비트가 잘릴 수 있어요.\\n\\n"
                    "특히 XOR은 뒤쪽 **오류 검출** 내용을 이해하는 기초예요."
                )

            with tabs[4]:
                st.markdown("### 소수점 아래에도 2진수 자리가 있어요")
                st.markdown(
                    "10진수는 소수점 아래가 1/10, 1/100… 순서이고, "
                    "2진수는 **1/2, 1/4, 1/8…** 순서예요."
                )
                st.markdown("""
<div class="btg-table-wrap"><table class="btg-table btg-table-small">
<thead><tr><th>2진수</th><th>10진수</th></tr></thead>
<tbody>
<tr><td>0.1₂</td><td>0.5</td></tr>
<tr><td>0.01₂</td><td>0.25</td></tr>
<tr><td>0.11₂</td><td>0.75</td></tr>
</tbody></table></div>
""", unsafe_allow_html=True)
                st.markdown(
                    "반면 **10진수 0.1**은 2진수로 `0.0001100110011…`처럼 끝없이 반복돼요. "
                    "유한한 비트로 저장할 때는 가까운 값으로 반올림해야 하므로 작은 오차가 생길 수 있어요."
                )
                st.markdown("#### 그런데 왜 평소에는 오류가 잘 안 보일까요?")
                st.markdown(
                    "컴퓨터가 내부적으로 근삿값을 저장해도, 출력할 때 반올림되어 "
                    "정상적인 숫자처럼 보이는 경우가 많기 때문이에요."
                )
                st.code(
                    "print(0.5 + 0.25)       # 0.75\\n"
                    "print(0.1 + 0.3)        # 0.4\\n"
                    "print(0.1 + 0.2)        # 0.30000000000000004\\n"
                    "print(0.1 + 0.2 == 0.3) # False",
                    language="python",
                )
                st.markdown(
                    "`0.5`와 `0.25`는 2진수로 정확하게 저장할 수 있어요. "
                    "`0.1`과 `0.3`은 정확히 저장되지 않지만 합계가 `0.4`로 표시돼요. "
                    "반면 `0.1 + 0.2`는 작은 차이가 화면에도 드러나요.\\n\\n"
                    "**중요:** 모든 소수 계산에서 오류가 나타나는 것은 아니며, "
                    "작은 오차가 있더라도 눈에 띄지 않을 수 있어요. "
                    "특히 `==`로 실수를 정확히 비교할 때 예상과 다른 결과가 나올 수 있어요."
                )

            with tabs[5]:
                st.markdown("### IEEE 754는 실수를 저장하는 대표적인 규칙이에요")
                st.markdown(
                    "실수는 정수와 달리 **부호·지수·가수 저장 영역(fraction 필드)**으로 나눠 저장해요. "
                    "과학 시간의 `1.23 × 10⁴` 같은 표기법을 2진수로 적용한 것과 비슷해요."
                )
                st.markdown("""
<div class="btg-table-wrap"><table class="btg-table">
<thead><tr><th>64비트 배정밀도</th><th>비트 수</th><th>역할</th></tr></thead>
<tbody>
<tr><td>부호</td><td>1</td><td>양수·음수 표시</td></tr>
<tr><td>지수</td><td>11</td><td>수의 크기 조절</td></tr>
<tr><td>가수 저장 영역</td><td>52</td><td>유효숫자 정보 저장</td></tr>
</tbody></table></div>
""", unsafe_allow_html=True)
                st.markdown(
                    "일반적인 **정규 수**는 저장하지 않은 선행 1비트를 포함해 "
                    "**53비트 유효 정밀도**를 사용해요. 0에 아주 가까운 **비정규 수(subnormal)**는 "
                    "유효 정밀도가 줄어들 수 있어요.\\n\\n"
                    "실수의 부호 비트는 정수의 2의 보수와 다르게 작동해요. "
                    "이제 현상 실험실에서 부호·지수·가수 그림을 보면 각 부분의 역할을 이해할 수 있어요."
                )

            with tabs[6]:
                st.markdown("### 숫자 표현 오차와 데이터 전달 오류는 달라요")
                st.markdown(
                    "앞에서 배운 것은 제한된 비트로 **숫자를 표현하는 방법**이에요. "
                    "반면 데이터를 전송하거나 저장할 때 비트가 바뀌는 문제도 있어요. "
                    "이때는 검사 값을 덧붙여 오류를 찾아낼 수 있어요."
                )
                st.markdown(
                    "#### 짝수 패리티\\n"
                    "데이터와 패리티 비트를 합쳐 **1의 개수가 짝수**가 되도록 만드는 방식이에요.\\n\\n"
                    "데이터 `1011`에는 1이 3개이므로 패리티 비트 `1`을 붙여 `10111`로 보내요. "
                    "도착했을 때 1의 개수가 홀수라면 오류가 발생했음을 알 수 있어요."
                )
                st.markdown(
                    "하지만 **두 비트가 동시에 바뀌면** 짝수·홀수가 그대로라서 놓칠 수 있어요. "
                    "체크섬과 CRC는 다른 규칙으로 검사 값을 만들어요. "
                    "자세한 내용은 기존 **오류 검출** 페이지에서 실험할 수 있어요."
                )


# -------------------------------------------------------------
# 1. 선택한 오류 기억하기 (상태 관리)
# -------------------------------------------------------------

def restore_selected_case(case_ids):
    """홈이나 도감에서 고른 오류가 있으면 그 오류를 선택 상자에 넣는다."""
    # "anatomy_case"가 아직 없을 때(이 페이지에 처음 들어왔을 때)만 실행된다.
    # 저장된 번호가 없으면 첫 번째 오류(BUG-001)를 보여 준다.
    if "anatomy_case" not in st.session_state:
        st.session_state["anatomy_case"] = st.session_state.get("selected_case", case_ids[0])


def remember_case():
    """선택 상자에서 오류를 바꾸면 그 번호를 저장한다."""
    st.session_state["selected_case"] = st.session_state["anatomy_case"]


def move_to_case(case_id):
    """관련 사례 버튼을 누르면 그 오류로 바꾼다."""
    # 버튼의 on_click으로 실행되는 함수라서, 화면을 다시 그리기 전에 값이 바뀐다.
    st.session_state["anatomy_case"] = case_id
    st.session_state["selected_case"] = case_id


def show_case_selector(cases):
    """분석할 사례를 고르는 버튼(라디오)을 보여 준다. 사례가 2개라 펼쳐 놓아야 한눈에 보인다."""
    case_ids = [case["id"] for case in cases]   # [1, 2]
    restore_selected_case(case_ids)
    # key="case_pick": 라임색 띠 상자 (CSS로 눈에 띄게 꾸민다)
    # 안내 글과 사례 버튼을 한 줄에 놓아서 세로 공간을 아낀다.
    with st.container(key="case_pick", horizontal=True, vertical_alignment="center"):
        render_html('<div class="pick-label">🔎 분석할 사례</div>')
        # format_func: 선택지에 번호 대신 "BUG-001 · 제목"처럼 보여 준다.
        st.radio(
            "분석할 사례",
            case_ids,
            key="anatomy_case",
            format_func=lambda case_id: case_label(find_case(cases, case_id)),
            on_change=remember_case,
            horizontal=True,
            label_visibility="collapsed",
        )


# -------------------------------------------------------------
# 2. 화면 위쪽: 제목, 증상 비교, 처리 과정
# -------------------------------------------------------------

def section_label(icon_name, english, korean):
    """각 구역 위에 붙는 작은 제목. 예) ⚙ PROCESS · 처리 과정"""
    return f'<div class="sec-label">{icon(icon_name)} {english} · {korean}</div>'


def show_title(case):
    """① 이름표(번호·분류·기술·원인 유형) + 전문용어 제목 + 쉬운 이름 + 한 줄 요약"""
    render_html(f"""
        <div class="an-title">
            <div>
                <span class="bt-badge bt-badge-on">BUG-{case['id']:03d}</span>
                <span class="bt-badge">분류 · {escape(case['category'])}</span>
                <span class="bt-badge">기술 · {escape(case['tech'])}</span>
                <span class="bt-badge">원인 유형 · {escape(case['cause_type'])}</span>
            </div>
            <h2>{escape(case['title'])}</h2>
            <div class="bt-card-nick">“{escape(case['nickname'])}”</div>
            <div class="an-summary">{escape(case['summary'])}</div>
        </div>
    """)


def show_symptom_row(case):
    """② 증상 · 정상이라면 · 실제로는 → 같은 높이의 3칸으로 나란히 비교 (+ 직접 관찰은 아래 한 줄)"""
    # CSS 격자(grid)로 3칸을 만들면 글 길이가 달라도 세 상자의 높이가 똑같아진다.
    observed = ""
    # observation이 null(None)이 아닐 때만 직접 관찰 줄을 만든다.
    if case["observation"]:
        observed = f"""
            <div class="bt-box bt-obs an-observed">
                <div class="bt-box-label">{icon("visibility")} OBSERVED · 직접 관찰</div>{escape(case['observation'])}
            </div>
        """
    render_html(f"""
        {section_label("search", "SYMPTOM", "어떤 현상인가")}
        <div class="an-grid3">
            <div class="bt-box"><div class="bt-box-label">증상</div>{escape(case['symptom'])}</div>
            <div class="bt-box bt-ok"><div class="bt-box-label">EXPECTED · 정상이라면</div>{escape(case['expected'])}</div>
            <div class="bt-box bt-err"><div class="bt-box-label">ACTUAL · 실제로는</div>{escape(case['actual'])}</div>
        </div>
        {observed}
    """)


def show_flow(case):
    """③ 오류가 생기는 흐름을 '입력 → 처리 → 출력' 세 칸 그림으로 보여 준다."""
    flow = case["flow"]       # {"input": "...", "process": "...", "output": "..."}
    # 출력 칸(bt-flow-out)은 벽돌색으로 그려서 '이상한 결과'임을 강조한다.
    render_html(f"""
        {section_label("route", "PROCESS", "컴퓨터 안에서 일어난 일")}
        <div class="bt-flow">
            <div class="bt-flow-box">{icon("keyboard")}<div class="bt-flow-name">입력</div><div class="bt-flow-text">{escape(flow['input'])}</div></div>
            <div class="bt-flow-arrow">▶</div>
            <div class="bt-flow-box">{icon("settings")}<div class="bt-flow-name">처리</div><div class="bt-flow-text">{escape(flow['process'])}</div></div>
            <div class="bt-flow-arrow">▶</div>
            <div class="bt-flow-box bt-flow-out">{icon("error")}<div class="bt-flow-name">출력</div><div class="bt-flow-text">{escape(flow['output'])}</div></div>
        </div>
    """)


# -------------------------------------------------------------
# 3. 원인 추적 기록과 핵심 원리
# -------------------------------------------------------------

def basis_badge(case, step):
    """단계마다 붙일 근거 이름표. 확인 = 누르면 그 근거 문서가 새 탭에서 열린다 / 추정 = 아직 확인되지 않은 설명"""
    if step["basis"] == "확인" and step["source"] is not None:
        source = case["sources"][step["source"]]          # 이 단계의 근거 문서 (출처 목록에서 몇 번째인지 데이터에 적혀 있음)
        # target="_blank": 새 탭에서 열기 / title: 마우스를 올리면 문서 이름이 보인다
        return (f'<a class="bt-basis bt-basis-ok" href="{escape(source["url"])}" target="_blank" '
                f'title="{escape(source["title"])}">📘 문서로 확인 ↗</a>')
    return '<span class="bt-basis bt-basis-guess">🔎 추정</span>'


def show_steps(case):
    """④ 원인을 #01 → #02 … 순서의 추적 카드로 가로로 나란히 보여 준다. (타임라인)"""
    cards = ""
    # enumerate(목록, start=1): 번호(1, 2, 3...)와 단계 내용을 함께 꺼낸다.
    # 단계 하나는 {"basis": "확인" 또는 "추정", "text": "설명"} 형태의 딕셔너리다.
    for step_number, step in enumerate(case["steps"], start=1):
        cards += f"""
            <div class="an-step">
                <div class="an-step-head"><span class="bt-step-no">#{step_number:02d}</span>{basis_badge(case, step)}</div>
                <div class="an-step-text">{escape(step['text'])}</div>
            </div>
        """
    render_html(f"""
        {section_label("troubleshoot", "TRACE", "원인 추적 기록")}
        <div class="an-steps">{cards}</div>
    """)


def show_key_point(case):
    """② 오류의 핵심 원리를 한 문장으로, 페이지에서 가장 눈에 띄게 보여 준다."""
    render_html(f"""
        <div class="bt-keypoint">
            {icon("lightbulb")}
            <div><div class="bt-keypoint-label">KEY POINT · 이것만 기억하세요</div>
            <div class="bt-keypoint-text">{escape(case['key_point'])}</div></div>
        </div>
    """)


def show_terms(case):
    """③ 설명을 읽기 전에 먼저 알아 둘 전문용어를 카드로 보여 준다."""
    cards = ""
    for term in case["terms"]:               # term = {"term": "용어", "desc": "쉬운 설명"}
        cards += f'<div class="bt-term"><div class="bt-term-name">{escape(term["term"])}</div><div class="bt-term-desc">{escape(term["desc"])}</div></div>'
    render_html(f'{section_label("menu_book", "WORDS", "먼저 알아 둘 용어")}<div class="bt-terms">{cards}</div>')


def show_sources(case):
    """⑧ 근거가 된 공식 문서 목록 (누르면 새 탭에서 열린다)"""
    items = ""
    for number, source in enumerate(case["sources"], start=1):
        items += f'<li><a href="{escape(source["url"])}" target="_blank">{escape(source["title"])} ↗</a></li>'
    render_html(f'{section_label("library_books", "SOURCES", "출처")}<div class="bt-box"><ol class="an-sources">{items}</ol></div>')


def show_video(case):
    """⑦ 관련 영상: 데이터에 video가 있는 사례에서만 YouTube 영상을 바로 재생할 수 있게 넣는다."""
    video = case["video"]               # {"title": "...", "url": "..."} 또는 None
    render_html(section_label("smart_display", "VIDEO", "영상으로 한 번 더"))
    video_column, guide_column = st.columns([3, 2], vertical_alignment="center")
    with video_column:
        st.video(video["url"])          # st.video: YouTube 주소를 넣으면 화면 안에서 재생된다
    with guide_column:
        render_html(f"""
            <div class="bt-box bt-obs">
                <div class="bt-box-label">{icon("play_circle")} {escape(video['title'])}</div>
                이 영상에서 확인할 것<br>
                ① 유닉스 시간이 무엇인지<br>
                ② 왜 2038년 1월 19일에 문제가 생기는지<br>
                ③ 64비트로 바꾸는 해결 방법
            </div>
        """)


def show_lab_link(case):
    """실험실로 가는 버튼: 이 사례와 연결된 실험을 열어 둔 채로 이동한다."""
    if st.button("이 원리를 현상 실험실에서 직접 확인하기", icon=":material/science:", type="primary", width="stretch"):
        # 어떤 실험을 열지 저장해 두고 실험실로 이동한다.
        st.session_state["saved_lab"] = case["lab"]
        st.switch_page("pages/laboratory.py")


# -------------------------------------------------------------
# 4. 아래 탭: 자주 생기는 곳 / 해결 방법 / 출처 / 관련 사례
# -------------------------------------------------------------

def show_bullets(items):
    """문장 목록을 글머리표 목록으로 보여 준다."""
    for item in items:
        st.markdown(f"- {item}")


def show_related_cases(cases, case):
    """관련 사례 버튼을 보여 주고, 누르면 그 오류로 바뀐다."""
    columns = st.columns(len(case["related"]))
    for column, related_id in zip(columns, case["related"]):
        related_case = find_case(cases, related_id)
        with column:
            # on_click=함수, args=(함수에 넘길 값,) → 버튼을 누르면 move_to_case(번호) 실행
            st.button(case_label(related_case), key=f"related_{related_id}",
                      on_click=move_to_case, args=(related_id,), width="stretch")


def show_detail_tabs(cases, case):
    """⑨ 자세한 정보를 탭으로 나눠서 한 화면에 담는다."""
    where_tab, fix_tab, related_tab = st.tabs(["📍 자주 생기는 곳", "🛠️ 해결 방법", "🔗 관련 사례"])
    with where_tab:
        show_bullets(case["where"])
    with fix_tab:
        user_column, developer_column = st.columns(2)
        with user_column:
            st.markdown("**사용자가 할 수 있는 것**")
            show_bullets(case["fix_user"])
        with developer_column:
            st.markdown("**개발자가 할 수 있는 것**")
            show_bullets(case["fix_dev"])
    with related_tab:
        show_related_cases(cases, case)


def apply_anatomy_style():
    """원인 해부실에만 쓰는 배치 디자인"""
    render_html("""
        <style>
        .an-title h2 { margin: 2px 0 0 !important; }
        .pick-label { font-family: 'Galmuri11', sans-serif; font-weight: 700; color: var(--ink); font-size: 1.05rem; white-space: nowrap; margin-right: 10px; }
        .st-key-case_pick > div { width: auto !important; flex: none !important; }
        .an-summary { color: var(--text); font-size: 1.02rem; line-height: 1.7; }
        /* 같은 높이의 3칸 격자 (증상 · 정상이라면 · 실제로는) */
        .an-grid3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
        .an-grid3 .bt-box { margin: 0; }
        .an-observed { margin-top: 10px; }
        /* 원인 추적 카드: 화면 폭에 맞춰 한 줄에 최대 4장, 높이는 모두 같게 */
        .an-steps { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 10px; margin-bottom: 16px; }
        .an-step { background: var(--paper); border: 3px solid var(--ink); padding: 10px 12px; }
        .an-step-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px; }
        .an-step-head .bt-step-no { flex: none; width: 50px; height: 32px; line-height: 28px; }
        .an-step-text { font-size: 0.98rem; line-height: 1.7; color: var(--text); }
        .an-sources { margin: 0; padding-left: 22px; line-height: 1.9; }
        .an-sources a { color: #2F6B2A; font-weight: 700; }
        @media (max-width: 800px) { .an-grid3 { grid-template-columns: 1fr; } }

        /* 기초 학습 안내서: 읽기 중심, 형광펜·불필요한 상자 제거 */
        .st-key-beginner_guide [data-testid="stExpander"] {
            background: #F7F8E9 !important;
            border: 2px solid #234C2A !important;
            border-radius: 5px !important;
            overflow: hidden;
            margin: 6px 0 16px;
            box-shadow: none !important;
        }
        .st-key-beginner_guide [data-testid="stExpander"] summary {
            background: #214A2A !important;
            padding: 13px 20px !important;
            min-height: 54px !important;
        }
        .st-key-beginner_guide [data-testid="stExpander"] summary:hover {
            background: #2B5C34 !important;
        }
        .st-key-beginner_guide [data-testid="stExpander"] summary p {
            color: #F4F8E8 !important;
            font-size: 1.16rem !important;
            font-weight: 750 !important;
            line-height: 1.4 !important;
            background: transparent !important;
            box-shadow: none !important;
        }
        .st-key-beginner_guide [data-testid="stExpander"] summary svg {
            color: #E8F1CE !important;
        }
        .st-key-beginner_guide [data-testid="stExpanderDetails"] {
            background: #F7F8E9 !important;
            padding: 14px 20px 22px !important;
        }
        .st-key-beginner_guide [data-testid="stExpanderDetails"] .stMarkdown,
        .st-key-beginner_guide [data-testid="stExpanderDetails"] .stCaptionContainer {
            max-width: 850px;
        }
        .st-key-beginner_guide [data-testid="stExpanderDetails"] p,
        .st-key-beginner_guide [data-testid="stExpanderDetails"] li {
            background: transparent !important;
            box-shadow: none !important;
            color: #24382A !important;
            font-size: 1.04rem !important;
            line-height: 1.75 !important;
            word-break: keep-all;
            overflow-wrap: anywhere;
        }
        .st-key-beginner_guide [data-testid="stExpanderDetails"] strong {
            color: #193D23 !important;
            background: transparent !important;
            box-shadow: none !important;
            padding: 0 !important;
        }
        .st-key-beginner_guide [data-testid="stExpanderDetails"] h3 {
            font-size: 1.5rem !important;
            color: #1F4D25 !important;
            margin: 16px 0 12px !important;
        }
        .st-key-beginner_guide [data-testid="stExpanderDetails"] h4 {
            font-size: 1.12rem !important;
            color: #1F4D25 !important;
            margin: 18px 0 8px !important;
        }
        .st-key-beginner_guide [data-testid="stTabs"] button {
            background: transparent !important;
            border: 0 !important;
            border-bottom: 2px solid #B9C5AA !important;
            border-radius: 0 !important;
            padding: 9px 13px !important;
            margin: 0 !important;
            box-shadow: none !important;
        }
        .st-key-beginner_guide [data-testid="stTabs"] button[aria-selected="true"] {
            background: #E3EACD !important;
            border-bottom: 3px solid #1F4D25 !important;
        }
        .st-key-beginner_guide [data-testid="stExpanderDetails"] code {
            background: #E9EDDD !important;
            color: #1F4D25 !important;
            box-shadow: none !important;
            font-weight: 600;
        }
        .btg-table-wrap { max-width: 680px; margin: 14px 0 18px; overflow-x: auto; }
        .btg-table {
            border-collapse: collapse;
            width: 100%;
            background: transparent;
            font-size: 1rem;
            color: #24382A;
        }
        .btg-table th {
            color: #1F4D25;
            background: #DCE6C9;
            font-weight: 750;
        }
        .btg-table th, .btg-table td {
            border: 1px solid #9BAE91;
            padding: 10px 14px;
            text-align: center;
            overflow-wrap: anywhere;
        }
        .btg-table-small { max-width: 460px; }
        .btg-bits {
            display: grid;
            grid-template-columns: repeat(8, minmax(0, 1fr));
            gap: 4px;
            max-width: 640px;
            margin: 12px 0 6px;
        }
        .btg-bits > div { text-align: center; min-width: 0; }
        .btg-bits small {
            display: block; color: #315338; font-weight: 700;
            font-size: .78rem; margin-bottom: 4px;
        }
        .btg-bits span {
            display: block; border: 1px solid #789373;
            padding: 9px 0; background: #F0F3E8;
            font-weight: 750; color: #193D23;
        }
        .btg-bits .active span { background: #C6EA4E; }
        .btg-result {
            max-width: 640px; padding: 7px 0;
            font-size: .96rem; color: #23482C;
        }
        .btg-result span { margin-left: 14px; }
        @media (max-width: 800px) {
            .st-key-beginner_guide [data-testid="stExpanderDetails"] {
                padding: 12px !important;
            }
            .btg-table th, .btg-table td { padding: 8px 6px; }
            .btg-bits { gap: 2px; }
            .btg-bits small { font-size: .68rem; }
            .btg-bits span { padding: 7px 0; }
        }
        </style>
    """)


# ----- 실제 실행 순서 -----
all_cases = load_cases()
apply_anatomy_style()

with crt_frame("pages/anatomy.py", "ANATOMY"):
    page_banner("layers", "ROOT CAUSE", "원인 해부실", "오류가 발생하는 내부 처리 과정을 한 단계씩 추적합니다.")
    show_beginner_guide()                                                       # 기초 개념 (선택적으로 펼치기)
    show_case_selector(all_cases)                                               # 오류 고르기
    current_case = find_case(all_cases, st.session_state["anatomy_case"])       # 고른 오류 데이터

    show_title(current_case)                  # ① 제목
    show_key_point(current_case)              # ② 핵심 원리 (가장 크게)
    show_terms(current_case)                  # ③ 먼저 알아 둘 용어
    show_symptom_row(current_case)            # ④ 증상 · 정상이라면 · 실제로는 (+ 직접 관찰)
    show_flow(current_case)                   # ⑤ 처리 과정
    show_steps(current_case)                  # ⑥ 원인 추적 기록
    if current_case["video"]:                 # ⑦ 관련 영상이 있는 사례만
        show_video(current_case)
    show_lab_link(current_case)               # ⑧ 실험실 버튼
    show_sources(current_case)                # ⑨ 출처 (누르면 문서가 열린다)
    show_detail_tabs(all_cases, current_case) # ⑩ 아래 탭
