
# =============================================================
# pages/anatomy.py  (원인 해부실)
# =============================================================

from html import escape

import streamlit as st

from common import case_label, crt_frame, find_case, icon, load_cases, page_banner, render_html


# -------------------------------------------------------------
# 초보자용 기초 안내
# -------------------------------------------------------------

def show_beginner_guide():
    """기존 원인 해부실 안에서 선택적으로 펼치는 기초 개념 안내서."""
    with st.expander("📖 처음이라면? 비트·2진수부터 배우는 기초 안내서", expanded=False):
        st.caption("오류 분석 전에 필요한 기초만 모았어요. 이미 알고 있다면 접고 바로 원인 추적을 시작해도 돼요.")
        tabs = st.tabs(["비트와 2진수", "비트 수와 범위", "음수와 2의 보수", "비트 연산", "2진 소수", "IEEE 754", "오류 검출 기초"])
        with tabs[0]:
            st.markdown("""#### 비트는 0 또는 1을 담는 한 칸
**1비트(bit)**에는 0과 1 중 하나가 들어가요. **8비트 = 1바이트(byte)**예요. 비트가 8개라면 0과 1을 나열하는 방법이 $2^8=256$가지 있어요.

우리가 쓰는 **10진수**는 오른쪽부터 1, 10, 100…의 자리 값을 갖고, **2진수**는 오른쪽부터 1, 2, 4, 8, 16…의 자리 값을 가져요.

**예: 13을 8비트 2진수로 나타내기**

| 자리 값 | 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 |
|---|---|---|---|---|---|---|---|---|
| 비트 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 1 |

1이 있는 자리만 더하면 **8 + 4 + 1 = 13**이 돼요. 따라서 13은 `00001101`이에요.

반대로 `00001010`은 8과 2 자리에 1이 있으므로 10이에요. 여기까지 이해하면 비트 그림을 읽을 수 있어요.""")
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
    if "anatomy_case" not in st.session_state:
        st.session_state["anatomy_case"] = st.session_state.get("selected_case", case_ids[0])


def remember_case():
    """선택 상자에서 오류를 바꾸면 그 번호를 저장한다."""
    st.session_state["selected_case"] = st.session_state["anatomy_case"]


def move_to_case(case_id):
    """관련 사례 버튼을 누르면 그 오류로 바꾼다."""
    st.session_state["anatomy_case"] = case_id
    st.session_state["selected_case"] = case_id


def show_case_selector(cases):
    """분석할 사례를 고르는 버튼(라디오)을 보여 준다."""
    case_ids = [case["id"] for case in cases]
    restore_selected_case(case_ids)
    with st.container(key="case_pick", horizontal=True, vertical_alignment="center"):
        render_html('<div class="pick-label">🔎 분석할 사례</div>')
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
    """각 구역 위에 붙는 작은 제목."""
    return f'<div class="sec-label">{icon(icon_name)} {english} · {korean}</div>'


def show_title(case):
    """이름표 + 제목 + 쉬운 이름 + 요약"""
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
    """증상 · 정상이라면 · 실제로는"""
    observed = ""
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
    """입력 → 처리 → 출력"""
    flow = case["flow"]
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
    """단계마다 붙일 근거 이름표."""
    if step["basis"] == "확인" and step["source"] is not None:
        source = case["sources"][step["source"]]
        return (f'<a class="bt-basis bt-basis-ok" href="{escape(source["url"])}" target="_blank" '
                f'title="{escape(source["title"])}">📘 문서로 확인 ↗</a>')
    return '<span class="bt-basis bt-basis-guess">🔎 추정</span>'


def show_steps(case):
    """원인 추적 카드를 나란히 보여 준다."""
    cards = ""
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
    """오류의 핵심 원리를 한 문장으로 보여 준다."""
    render_html(f"""
        <div class="bt-keypoint">
            {icon("lightbulb")}
            <div><div class="bt-keypoint-label">KEY POINT · 이것만 기억하세요</div>
            <div class="bt-keypoint-text">{escape(case['key_point'])}</div></div>
        </div>
    """)


def show_terms(case):
    """먼저 알아 둘 전문용어를 카드로 보여 준다."""
    cards = ""
    for term in case["terms"]:
        cards += f'<div class="bt-term"><div class="bt-term-name">{escape(term["term"])}</div><div class="bt-term-desc">{escape(term["desc"])}</div></div>'
    render_html(f'{section_label("menu_book", "WORDS", "먼저 알아 둘 용어")}<div class="bt-terms">{cards}</div>')


def show_sources(case):
    """근거가 된 공식 문서 목록."""
    items = ""
    for number, source in enumerate(case["sources"], start=1):
        items += f'<li><a href="{escape(source["url"])}" target="_blank">{escape(source["title"])} ↗</a></li>'
    render_html(f'{section_label("library_books", "SOURCES", "출처")}<div class="bt-box"><ol class="an-sources">{items}</ol></div>')


def show_video(case):
    """관련 영상이 있는 사례에서만 보여 준다."""
    video = case["video"]
    render_html(section_label("smart_display", "VIDEO", "영상으로 한 번 더"))
    video_column, guide_column = st.columns([3, 2], vertical_alignment="center")
    with video_column:
        st.video(video["url"])
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
    """이 사례와 연결된 실험실로 이동한다."""
    if st.button("이 원리를 현상 실험실에서 직접 확인하기", icon=":material/science:", type="primary", width="stretch"):
        st.session_state["saved_lab"] = case["lab"]
        st.switch_page("pages/laboratory.py")


# -------------------------------------------------------------
# 4. 아래 탭
# -------------------------------------------------------------

def show_bullets(items):
    """문장 목록을 글머리표 목록으로 보여 준다."""
    for item in items:
        st.markdown(f"- {item}")


def show_related_cases(cases, case):
    """관련 사례 버튼을 보여 준다."""
    columns = st.columns(len(case["related"]))
    for column, related_id in zip(columns, case["related"]):
        related_case = find_case(cases, related_id)
        with column:
            st.button(case_label(related_case), key=f"related_{related_id}",
                      on_click=move_to_case, args=(related_id,), width="stretch")


def show_detail_tabs(cases, case):
    """자세한 정보를 탭으로 나눠서 보여 준다."""
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
        .an-grid3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
        .an-grid3 .bt-box { margin: 0; }
        .an-observed { margin-top: 10px; }
        .an-steps { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 10px; margin-bottom: 16px; }
        .an-step { background: var(--paper); border: 3px solid var(--ink); padding: 10px 12px; }
        .an-step-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px; }
        .an-step-head .bt-step-no { flex: none; width: 50px; height: 32px; line-height: 28px; }
        .an-step-text { font-size: 0.98rem; line-height: 1.7; color: var(--text); }
        .an-sources { margin: 0; padding-left: 22px; line-height: 1.9; }
        .an-sources a { color: #2F6B2A; font-weight: 700; }
        @media (max-width: 800px) { .an-grid3 { grid-template-columns: 1fr; } }
        </style>
    """)


# ----- 실제 실행 순서 -----
all_cases = load_cases()
apply_anatomy_style()

with crt_frame("pages/anatomy.py", "ANATOMY"):
    page_banner("layers", "ROOT CAUSE", "원인 해부실", "오류가 발생하는 내부 처리 과정을 한 단계씩 추적합니다.")
    show_beginner_guide()
    show_case_selector(all_cases)
    current_case = find_case(all_cases, st.session_state["anatomy_case"])

    show_title(current_case)
    show_key_point(current_case)
    show_terms(current_case)
    show_symptom_row(current_case)
    show_flow(current_case)
    show_steps(current_case)
    if current_case["video"]:
        show_video(current_case)
    show_lab_link(current_case)
    show_sources(current_case)
    show_detail_tabs(all_cases, current_case)
