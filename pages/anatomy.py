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
    """기존 원인 해부실 안에서 선택적으로 펼치는 기초 개념 안내서."""
    with st.container(key="beginner_guide"):
        with st.expander("📖 처음이라면? 기초부터 시작하기", expanded=False):
            st.caption("오류 분석 전에 필요한 기초만 모았어요. 이미 알고 있다면 접고 바로 원인 추적을 시작해도 돼요.")
            tabs = st.tabs(["비트와 2진수", "비트 수와 범위", "음수와 2의 보수", "비트 연산", "2진 소수", "IEEE 754", "오류 검출 기초"])
            with tabs[0]:
                st.markdown("""#### 비트는 0 또는 1을 담는 한 칸""")
            render_html("""
                <div class="guide-key">
                    <div class="guide-eyebrow">💡 핵심 개념</div>
                    <div class="guide-key-title">1비트 = 0 또는 1을 저장하는 한 칸</div>
                    <div>8비트가 모이면 <strong>1바이트(byte)</strong>가 돼요. 8비트로 만들 수 있는 조합은 <strong>256가지</strong>예요.</div>
                </div>
            """)
            st.markdown("""우리가 쓰는 **10진수**는 오른쪽부터 1, 10, 100…의 자리 값을 보고, **2진수**는 오른쪽부터 1, 2, 4, 8, 16…의 자리 값을 가져요.""")
            st.markdown("**예: 13을 8비트 2진수로 나타내기**")
            render_html("""
                <div class="guide-example">
                    <div class="guide-eyebrow">🔢 자리 값과 비트</div>
                    <div class="guide-bits">
                        <div><b>128</b><span>0</span></div>
                        <div><b>64</b><span>0</span></div>
                        <div><b>32</b><span>0</span></div>
                        <div><b>16</b><span>0</span></div>
                        <div class="on"><b>8</b><span>1</span></div>
                        <div class="on"><b>4</b><span>1</span></div>
                        <div><b>2</b><span>0</span></div>
                        <div class="on"><b>1</b><span>1</span></div>
                    </div>
                    <div class="guide-answer"><strong>8 + 4 + 1 = 13</strong><span>따라서 13은 <code>00001101</code>이에요.</span></div>
                </div>
            """)
            st.markdown("반대로 `00001010`은 8과 2 자리에 1이 있으므로 **10**이에요. 여기까지 이해하면 비트 그림을 읽을 수 있어요.")
            with tabs[1]:
                st.markdown("""#### 8비트·32비트·64비트는 칸의 개수예요
    **8비트**는 8칸, **32비트**는 32칸, **64비트**는 64칸을 사용한다는 뜻이에요. 칸이 늘어나면 가능한 비트 조합 수도 늘어나요.

    | 비트 수 | 가능한 조합 수 |
    |---|---|
    | 8비트 | $2^8=256$가지 |
    | 32비트 | $2^{32}=4,294,967,296$가지 |
    | 64비트 | $2^{64}$가지 |

    **중요:** 조합의 개수가 곧 '표현 가능한 양수의 최댓값'은 아니에요. 음수까지 표현할지, 정수를 저장할지, 실수를 저장할지에 따라 같은 칸도 다르게 해석해요.

    예를 들어 **부호 없는 8비트 정수**는 0부터 255까지, **2의 보수 방식의 부호 있는 8비트 정수**는 −128부터 127까지 나타내요. 둘 다 256가지 값이에요.

    또한 **32비트 정수**와 **32비트 실수**는 저장 규칙이 서로 달라요. 비트 수만 보고 정확도나 범위를 단정하면 안 돼요.""")
            with tabs[2]:
                st.markdown("""#### 음수 기호 없이 음수를 저장하는 방법
    컴퓨터의 비트에는 `−` 기호를 직접 적을 수 없어요. 그래서 **부호 있는 정수**는 보통 **2의 보수(two's complement)** 규칙으로 비트를 해석해요.

    8비트에서 맨 앞 비트가 **0이면 0 이상의 수**, **1이면 음수**로 해석돼요. 단순히 맨 앞 칸만 부호로 떼어 놓는 방식과는 달라요.

    **예: 5를 −5로 바꾸기**

    1. 5를 8비트로 쓰기: `00000101`
    2. 0과 1을 모두 뒤집기: `11111010`
    3. 1을 더하기: `11111011` → **−5**

    왜 −5일까요? 8비트 2의 보수에서는 맨 앞 자리의 값이 **−128**이고 나머지는 64, 32, 16, 8, 4, 2, 1이에요.

    `11111011` = −128 + 64 + 32 + 16 + 8 + 2 + 1 = **−5**

    그래서 8비트의 범위는 **−128부터 127**까지예요. 0이 포함되므로 음수 쪽이 한 개 더 많아요.""")
            with tabs[3]:
                st.markdown("""#### 비트 연산은 0과 1을 직접 다루는 계산이에요
    **AND (`&`)**: 두 비트가 모두 1일 때만 1이에요. 예: `1100 & 1010 = 1000`

    **XOR (`^`)**: 두 비트가 서로 다를 때만 1이에요. 예: `1100 ^ 1010 = 0110`

    **NOT (`~`)**: 각 비트를 반대로 뒤집어요. 4비트만 놓고 보면 `1100 → 0011`이에요. *Python의 `~` 연산은 정수의 비트 폭을 고정하지 않으므로, 4비트 결과를 얻으려면 별도로 4비트 마스크를 적용해야 해요.*

    **왼쪽 시프트 (`<<`)**: 비트를 왼쪽으로 옮겨요. 예: `0011 << 1 = 0110` (4비트 안에서는 3에서 6으로 바뀜). 단, 고정된 비트 수를 벗어나면 상위 비트가 잘릴 수 있어요.

    이 연산들은 컴퓨터가 저장한 비트를 읽고 검사하는 데 쓰여요. 특히 XOR은 뒤쪽 **오류 검출** 페이지를 이해하는 기초예요.""")
            with tabs[4]:
                st.markdown("""#### 소수점 아래에도 2진수 자리 값이 있어요
    10진수 소수점 아래가 1/10, 1/100…이라면, **2진수 소수점 아래**는 오른쪽부터 **1/2, 1/4, 1/8, 1/16…**이에요.

    - `0.1₂` = 1/2 = **0.5₁₀**
    - `0.01₂` = 1/4 = **0.25₁₀**
    - `0.11₂` = 1/2 + 1/4 = **0.75₁₀**

    그런데 **10진수 0.1**은 2진수로 `0.0001100110011…`처럼 끝없이 이어져요. 10진수에서 1/3이 0.3333…으로 끝나지 않는 것과 비슷해요.

    따라서 저장 칸이 유한하면 이런 소수는 **가장 가까운 표현 가능한 값으로 반올림**해야 해요. 이 개념을 이해하면 기존 정밀도 오차 실험이 훨씬 쉬워져요.""")
            with tabs[5]:
                st.markdown("""#### IEEE 754는 실수를 저장하는 대표적인 규칙이에요
    정수와 달리 실수는 **부호·지수·가수(정확히는 fraction 필드)**로 나누어 저장해요. 과학 시간에 배운 $1.23\times10^4$ 같은 표기법을 2진수로 적용한 것과 비슷해요.

    **64비트 배정밀도(binary64)**에서는 다음과 같이 나눠요.

    | 부분 | 칸 수 | 역할 |
    |---|---:|---|
    | 부호 | 1비트 | 양수인지 음수인지 표시 |
    | 지수 | 11비트 | 수의 크기 조절 |
    | 가수 저장 영역 | 52비트 | 유효숫자의 세부 정보 저장 |

    보통의 **정규 수**는 저장하지 않은 선행 1비트를 포함해 **53비트의 유효 정밀도**를 사용해요. 반면 0에 아주 가까운 **비정규 수(subnormal)**는 유효 정밀도가 점점 줄어들어요.

    여기서 **부호 비트는 정수의 2의 보수와 다르게 작동**해요. 같은 64비트라도 정수와 실수의 저장 규칙은 같지 않아요.

    이제 현상 실험실에서 64비트 실수의 부호·지수·가수 그림을 보면 각각 어떤 역할인지 알 수 있어요.""")
            with tabs[6]:
                st.markdown("""#### 숫자의 표현 오류와 데이터 전달 오류는 달라요
    앞에서 배운 내용은 **숫자를 제한된 칸에 표현하는 방법**이에요. 반면 데이터를 전송하거나 저장할 때 비트가 우연히 바뀌는 문제도 있어요. 이를 알아채려면 **검사용 값**을 덧붙일 수 있어요.

    **짝수 패리티**는 데이터와 패리티 비트를 합쳐 1의 개수가 짝수가 되도록 만드는 방법이에요.

    예: 데이터 `1011`에는 1이 3개 있으므로 패리티 비트 `1`을 덧붙여 **`10111`**로 보내요. 도착했을 때 1의 개수가 홀수라면 오류가 났음을 알 수 있어요.

    하지만 **두 비트가 동시에 바뀌면** 짝수·홀수가 그대로라 놓칠 수 있어요. XOR 체크섬이나 CRC는 다른 방식으로 확인값을 만들어요.

    자세한 패리티·체크섬·CRC 실험은 기존 **오류 검출** 페이지에서 이어서 확인하면 돼요.""")


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

        /* ===== 기초 학습 안내서: 다른 페이지에 영향 없는 전용 스타일 ===== */
        .st-key-beginner_guide [data-testid="stExpander"] {
            border: 3px solid #1F4D25 !important; border-radius: 8px !important;
            background: #FBFDF1 !important; overflow: hidden;
            box-shadow: 5px 5px 0 #9DBD68; margin: 8px 5px 18px;
        }
        .st-key-beginner_guide [data-testid="stExpander"] summary {
            background: #1F4D25 !important; padding: 18px 22px !important;
            min-height: 82px; border-radius: 0 !important;
        }
        .st-key-beginner_guide [data-testid="stExpander"] summary:hover { background: #2D6634 !important; }
        .st-key-beginner_guide [data-testid="stExpander"] summary p {
            color: #FFFFFF !important; font-family: 'Noto Sans KR', sans-serif !important;
            font-size: clamp(1.15rem, 1.6vw, 1.4rem) !important; font-weight: 800 !important;
            line-height: 1.5 !important; word-break: keep-all;
        }
        .st-key-beginner_guide [data-testid="stExpander"] summary svg { color: #C6EA4E !important; }
        .st-key-beginner_guide [data-testid="stExpanderDetails"] {
            background: #FBFDF1 !important; padding: 16px 22px 26px !important;
        }
        .st-key-beginner_guide [data-testid="stExpanderDetails"] p,
        .st-key-beginner_guide [data-testid="stExpanderDetails"] li {
            color: #1E3322 !important; line-height: 1.85 !important;
            font-size: 1.02rem !important; word-break: keep-all; overflow-wrap: anywhere;
        }
        .st-key-beginner_guide [data-testid="stTabs"] button {
            background: #E7F3C2 !important; border: 2px solid #1F4D25 !important;
            border-radius: 4px !important; margin: 3px; padding: 8px 12px;
        }
        .st-key-beginner_guide [data-testid="stTabs"] button[aria-selected="true"] {
            background: #C6EA4E !important;
        }
        .st-key-beginner_guide [data-testid="stExpanderDetails"] code {
            background: #E7F3C2 !important; color: #1F4D25 !important;
            padding: 2px 5px; font-weight: 700;
        }
        .st-key-beginner_guide [data-testid="stExpanderDetails"] table {
            background: #FFFFFF; border-collapse: collapse;
        }
        .st-key-beginner_guide [data-testid="stExpanderDetails"] th {
            background: #E7F3C2 !important; color: #1F4D25 !important;
        }
        .st-key-beginner_guide [data-testid="stExpanderDetails"] th,
        .st-key-beginner_guide [data-testid="stExpanderDetails"] td {
            border: 1px solid #A7BD8D; padding: 9px 12px; text-align: center;
        }
        .guide-key, .guide-example {
            background: #FFFFFF; border: 2px solid #1F4D25;
            padding: 14px 16px; margin: 12px 0; color: #1E3322;
            font-family: 'Noto Sans KR', sans-serif; line-height: 1.75;
        }
        .guide-key { background: #E7F3C2; border-left: 8px solid #1F4D25; }
        .guide-eyebrow { font-weight: 800; color: #1F4D25; margin-bottom: 7px; }
        .guide-key-title { font-size: 1.2rem; font-weight: 800; margin-bottom: 6px; }
        .guide-bits { display: grid; grid-template-columns: repeat(8, minmax(0, 1fr)); gap: 5px; }
        .guide-bits > div { min-width: 0; text-align: center; }
        .guide-bits b { display: block; font-size: 0.85rem; color: #1F4D25; }
        .guide-bits span { display: block; background: #F2F6E7; border: 2px solid #1F4D25;
            padding: 8px 0; font-family: 'Galmuri11', monospace; font-weight: 800; }
        .guide-bits .on span { background: #C6EA4E; }
        .guide-answer { display: flex; gap: 8px 20px; flex-wrap: wrap; margin-top: 14px;
            padding: 10px 12px; background: #E7F3C2; color: #1F4D25; }
        @media (max-width: 800px) {
            .st-key-beginner_guide [data-testid="stExpander"] summary { padding: 14px !important; min-height: 70px; }
            .st-key-beginner_guide [data-testid="stExpanderDetails"] { padding: 12px !important; }
            .guide-bits { gap: 2px; } .guide-bits b { font-size: 0.7rem; }
            .guide-bits span { padding: 6px 0; }
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
