# =============================================================
# pages/anatomy.py  (원인 해부실)
# 오류 하나를 골라 위에서 아래로 '추적 순서'대로 분석한다.
#   ① 제목 → ② 핵심 원리(가장 크게) → ③ 먼저 알아 둘 용어 → ④ 증상 · 정상이라면 · 실제로는 (+ 직접 관찰)
#   → ⑤ 처리 과정(입력 → 처리 → 출력) → ⑥ 원인 추적 기록 #01~#05 (문서로 확인 = 누르면 문서가 열림 / 추정)
#   → ⑦ 관련 영상(있을 때만) → ⑧ 실험실 버튼 → ⑨ 출처 → ⑩ 탭: 자주 생기는 곳 / 해결 방법 / 관련 사례
# =============================================================

import re                         # 글자 규칙(정규식): **굵게** 표시를 찾을 때 사용
from html import escape           # 글자 속 <, > 기호를 안전하게 바꾸는 함수

import streamlit as st

from common import case_label, crt_frame, find_case, icon, load_cases, page_banner, render_html


# -------------------------------------------------------------
# 용어 카드의 '자세히 보기' 내용: 오류 사례를 반복하지 않고 저장 원리만 설명한다.
# (예전에는 아래쪽 '원리 이해하기' 접기 상자에 따로 있었는데, 용어 카드와 내용이 겹쳐서 카드 안 팝업으로 합쳤다)
# -------------------------------------------------------------

# **굵게** 표시를 찾는 규칙. (.+?) = 별표 사이의 글자를 가능한 한 짧게 찾는다
BOLD_PATTERN = re.compile(r"\*\*(.+?)\*\*")


def write_text(text):
    """문장을 보여 준다. **굵게**는 HTML <b>로 바꿔서, 한글 바로 앞에서도 별표가 그대로 보이지 않게 한다."""
    text = text.replace("~", "&#126;")   # 마크다운은 ~ 두 개 사이 글자에 취소선을 그어서, ~를 그대로 보이는 HTML 글자로 바꾼다
    st.markdown(BOLD_PATTERN.sub(r"<b>\1</b>", text), unsafe_allow_html=True)


def topic_bits():
    """자세히 보기 ① 비트와 2진수: 2진수 자리 값과 13을 2진수로 바꾸는 예"""
    write_text(
        "**8비트 = 1바이트**이고, 8비트로 만들 수 있는 조합은 **256가지**예요.\n\n"
        "10진수는 오른쪽부터 1, 10, 100…의 자리 값을 쓰지만, "
        "2진수는 오른쪽부터 **1, 2, 4, 8, 16…**의 자리 값을 써요."
    )
    st.markdown("#### 13을 8비트 2진수로 표현하기")
    render_html("""
        <div class="btg-bits">
          <div><small>128</small><span>0</span></div><div><small>64</small><span>0</span></div>
          <div><small>32</small><span>0</span></div><div><small>16</small><span>0</span></div>
          <div class="active"><small>8</small><span>1</span></div><div class="active"><small>4</small><span>1</span></div>
          <div><small>2</small><span>0</span></div><div class="active"><small>1</small><span>1</span></div>
        </div>
        <div class="btg-result">8 + 4 + 1 = <strong>13</strong> <span>→ 00001101₂</span></div>
    """)
    write_text("반대로 `00001010`은 8과 2 자리에 1이 있으므로 **10**이에요.")
    st.markdown("#### 글자 하나는 몇 비트일까요?")
    write_text(
        "오늘날 우리가 쓰는 컴퓨터나 UTF-8(글자를 바이트로 바꾸는 규칙)에서는 **1바이트 = 8비트**라고 보면 돼요. "
        "다만 글자 하나가 몇 바이트인지는 글자마다 달라요.\n\n"
        "예) UTF-8에서 영어 'B'는 1바이트(8비트), 한글 '가'는 3바이트이므로 **24비트**예요."
    )


def bit_steps(rows):
    """비트가 바뀌는 과정을 한 줄씩 보여 주는 작은 표. rows = [(설명, 비트 글자, 읽은 값), ...]"""
    body = "".join(f"<tr><td>{label}</td><td><code>{bits}</code></td><td>{value}</td></tr>" for label, bits, value in rows)
    render_html(f"""
        <div class="btg-table-wrap"><table class="btg-table">
        <thead><tr><th>단계</th><th>8비트</th><th>읽은 값</th></tr></thead>
        <tbody>{body}</tbody></table></div>
    """)


def topic_sign_bit():
    """자세히 보기: 부호 비트 = 맨 앞 칸 하나로 양수·음수를 나눈다"""
    write_text(
        "**부호 비트**는 부호 있는 정수의 **맨 앞 칸 하나**예요. 이 칸이 0이면 0 이상, 1이면 음수로 읽어요.\n\n"
        "부호 비트도 다른 칸처럼 자리 값을 가져요. 부호 없는 수에서는 맨 앞 칸이 128을 뜻하지만, "
        "2의 보수로 저장하는 부호 있는 수에서는 같은 칸을 **−128**로 계산해요. 그래서 맨 앞 칸이 1이면 −128에서 시작해 나머지 칸의 값을 더해요.\n\n"
        "예) `10000101` = −128 + 4 + 1 = **−123**"
    )
    bit_steps([
        ("부호 비트 0", "00000101", "5"),
        ("부호 비트 0, 나머지 모두 1", "01111111", "127 (가장 큰 수)"),
        ("부호 비트 1, 나머지 모두 0", "10000000", "−128 (가장 작은 수)"),
        ("부호 비트 1, 나머지 모두 1", "11111111", "−128 + 127 = −1"),
    ])
    write_text(
        "같은 `11111111`도 부호 없는 정수로 읽으면 **255**, 부호 있는 정수로 읽으면 **−1**이에요. "
        "그래서 부호 없는 8비트는 **0~255**, 부호 있는 8비트는 **−128~127**을 담아요. 둘 다 256가지예요."
    )


def topic_overflow():
    """자세히 보기: 정수 오버플로 = 가장 큰 수에 1을 더하면 1이 왼쪽으로 계속 넘어가 부호 비트까지 간다"""
    write_text("비트 하나에는 0과 1, 두 가지 상태가 있어요. 그래서 **n비트로 만들 수 있는 수는 2ⁿ가지**뿐이에요.")
    render_html("""
        <div class="btg-table-wrap"><table class="btg-table">
        <thead><tr><th>비트 수</th><th>부호 있는 정수의 범위</th></tr></thead>
        <tbody>
        <tr><td>8비트</td><td>−128 부터 127 까지</td></tr>
        <tr><td>32비트</td><td>−2,147,483,648 부터 2,147,483,647 까지</td></tr>
        <tr><td>64비트</td><td>약 −922경 부터 922경 까지</td></tr>
        </tbody></table></div>
    """)
    st.markdown("#### 8비트로 보는 오버플로: 127 + 1")
    bit_steps([
        ("가장 큰 수", "01111111", "127"),
        ("1 더하기 (1이 맨 앞 칸까지 넘어감)", "10000000", "−128"),
    ])
    write_text(
        "1을 더하면 오른쪽 끝부터 1이 왼쪽 칸으로 계속 넘어가서 **맨 앞 부호 비트가 1**이 돼요. "
        "컴퓨터는 이걸 음수로 읽기 때문에 **가장 큰 수 + 1 = 가장 작은 수**가 돼요. 32비트에서도 똑같이 2,147,483,647 + 1이 −2,147,483,648이 돼요."
    )


def topic_underflow():
    """자세히 보기: 정수 언더플로 = 가장 작은 수에서 1을 빼면 왼쪽 칸에서 1을 계속 가져오다 부호 비트가 0이 된다"""
    write_text(
        "**정수 언더플로**는 오버플로의 반대 방향이에요. 가장 작은 수보다 더 작아지면 **가장 큰 양수 쪽으로** 넘어가요."
    )
    st.markdown("#### 8비트로 보는 언더플로: −128 − 1")
    bit_steps([
        ("가장 작은 수", "10000000", "−128"),
        ("1 빼기 (맨 앞 칸의 1까지 가져옴)", "01111111", "127"),
    ])
    write_text(
        "10진수에서 100 − 1을 하면 0인 칸들이 왼쪽 칸에서 1을 가져와 99가 되죠. 2진수도 끝 칸이 0이면 왼쪽 칸에서 1을 가져와야 하고, "
        "왼쪽 칸도 0이면 또 그 왼쪽에서 가져와요. 그래서 결국 **맨 앞 부호 비트의 1까지 가져가 0**이 돼요. "
        "부호 비트가 0이니 양수로 읽혀서 −128 − 1이 **127**이 돼요.\n\n"
        "※ 실수(부동소수점)에서 말하는 언더플로는 뜻이 달라요. 실수는 0에 너무 가까워져 0이 되는 현상이에요."
    )


def topic_twos():
    """자세히 보기: 2의 보수 = 뒤집고 1 더하기로 부호 바꾸기(양수↔음수), 맨 끝이 1일 때, 예외 −128, 비트 연산"""
    write_text(
        "비트에는 `−` 기호를 직접 적을 수 없어요. 그래서 음수는 **2의 보수** 규칙으로 만들어요. "
        "양수의 모든 칸을 **뒤집고(0↔1) 1을 더하면** 그 수의 음수가 돼요."
    )
    st.markdown("#### 5를 −5로 바꾸기")
    render_html("""
        <div class="btg-twos">
          <div><b>① +5의 8비트</b><code>00000101</code></div>
          <div><b>② 0과 1 뒤집기</b><code>11111010</code></div>
          <div><b>③ 1 더하기</b><code>11111011</code></div>
        </div>
    """)
    write_text(
        "8비트 2의 보수에서 맨 앞 자리의 값은 **−128**, 나머지는 64, 32, 16, 8, 4, 2, 1이에요.\n\n"
        "예) `11111011` = −128 + 64 + 32 + 16 + 8 + 2 + 1 = **−5**\n\n"
        "이 규칙 덕분에 컴퓨터는 빼기를 따로 만들지 않고 **음수를 더하는 것**으로 계산할 수 있어요.\n\n예) 7 − 5 = 7 + (−5)"
    )
    write_text(
        "**모든 비트를 뒤집고 1을 더하면 수의 부호가 반대로 바뀌어요.** "
        "양수를 음수로, 음수를 양수로 바꿀 때 모두 같은 규칙을 사용할 수 있어요."
    )
    st.markdown("#### −5를 다시 5로 바꾸기")
    bit_steps([
        ("① −5의 8비트", "11111011", "−5"),
        ("② 0과 1 뒤집기", "00000100", "4"),
        ("③ 1 더하기", "00000101", "5"),
    ])
    write_text("1을 먼저 빼고 뒤집어도 결과는 같아요. 예) `11111011` − 1 = `11111010` → 뒤집기 `00000101` = 5")
    st.markdown("#### 1을 더할 때 맨 끝이 이미 1이면?")
    write_text(
        "10진수에서 9 + 1을 하면 그 칸은 0이 되고, 왼쪽 칸으로 1이 넘어가 **10**이 되죠. "
        "2진수는 0과 1만 쓰기 때문에 **1 + 1**에서 똑같은 일이 생겨요. 그 칸은 0이 되고 왼쪽 칸으로 1이 넘어가요. "
        "넘어간 칸도 1이면 또 0이 되고 다시 왼쪽으로 넘어가요. 그래서 **끝에서부터 이어진 1은 모두 0**이 되고, **처음 만나는 0이 1**이 돼요."
    )
    render_html("""
        <div class="btg-table-wrap"><table class="btg-table">
        <thead><tr><th>경우</th><th>원래 수</th><th>뒤집기</th><th>1 더하기</th><th>읽은 값</th></tr></thead>
        <tbody>
        <tr><td>맨 끝에 1이 하나</td><td><code>00000110</code> (6)</td><td><code>11111001</code></td><td><code>11111010</code></td><td>−6</td></tr>
        <tr><td>맨 끝에 1이 여러 개</td><td><code>00001000</code> (8)</td><td><code>11110111</code></td><td><code>11111000</code></td><td>−8</td></tr>
        <tr><td>모든 칸이 1</td><td><code>00000000</code> (0)</td><td><code>11111111</code></td><td><code>00000000</code></td><td>0</td></tr>
        </tbody></table></div>
    """)
    write_text(
        "모든 칸이 1이면 1이 맨 앞 칸 밖(9번째 칸)까지 넘어가는데, 8비트에는 그 칸이 없어서 버려져요. "
        "그래서 0의 부호를 바꿔도 그대로 0이에요."
    )
    st.markdown("#### 예외: −128은 부호를 바꿀 수 없어요")
    bit_steps([
        ("① −128의 8비트", "10000000", "−128"),
        ("② 0과 1 뒤집기", "01111111", "127"),
        ("③ 1 더하기", "10000000", "−128"),
    ])
    write_text(
        "8비트 부호 있는 정수는 **−128~127**만 담을 수 있어서 **+128**을 만들 수 없어요. "
        "127에 1을 더하면 다시 −128이 되는 **정수 오버플로**와 같은 원리예요. 32비트의 −2,147,483,648도 똑같아요."
    )
    st.markdown("#### 비트 연산: 0과 1을 직접 다루는 계산")
    write_text(
        "**AND (`&`)** — 두 비트가 모두 1일 때만 1 · `1100 & 1010 = 1000`\n\n"
        "**XOR (`^`)** — 두 비트가 다를 때만 1 · `1100 ^ 1010 = 0110`\n\n"
        "**NOT (~)** — 0과 1을 모두 뒤집기 · `1100 → 0011` (2의 보수 ②단계)\n\n"
        "**왼쪽 밀기 (`<<`)** — 비트를 왼쪽으로 한 칸씩 옮기기 = 2를 곱하기 · `0011 << 1 = 0110`"
    )


def topic_fraction():
    """자세히 보기 ④ 2진 소수: 0.1이 2진수로 끝나지 않는 이유와 오차가 눈에 안 띄는 경우"""
    write_text("10진수는 소수점 아래가 1/10, 1/100… 순서이고, 2진수는 **1/2, 1/4, 1/8…** 순서예요.")
    render_html("""
        <div class="btg-table-wrap"><table class="btg-table btg-table-small">
        <thead><tr><th>2진수</th><th>10진수</th></tr></thead>
        <tbody><tr><td>0.1₂</td><td>0.5</td></tr><tr><td>0.01₂</td><td>0.25</td></tr><tr><td>0.11₂</td><td>0.75</td></tr></tbody>
        </table></div>
    """)
    write_text(
        "분모가 2, 4, 8…인 소수는 2진수로 딱 떨어져요. 반면 **10진수 0.1**(= 1/10)은 분모에 5가 있어서 2진수로 끝없이 반복돼요.\n\n"
        "예) 0.1 = 0.0001100110011…₂ (0011이 끝없이 되풀이)\n\n"
        "10진수에서 1/3 = 0.3333…이 끝나지 않는 것과 같은 이유예요."
    )
    st.markdown("#### 2진수로 딱 끝나는 소수의 조건")
    write_text("2진수에서 소수가 유한하게 끝나려면, **기약분수로 나타냈을 때 분모가 2의 거듭제곱**(2, 4, 8, 16…)이어야 해요.")
    render_html("""
        <div class="btg-table-wrap"><table class="btg-table">
        <thead><tr><th>10진수</th><th>기약분수</th><th>분모</th><th>2진수</th></tr></thead>
        <tbody>
        <tr><td>0.375</td><td>3/8</td><td>8 = 2³</td><td>0.011₂ (끝남)</td></tr>
        <tr><td>0.75</td><td>3/4</td><td>4 = 2²</td><td>0.11₂ (끝남)</td></tr>
        <tr><td>0.1</td><td>1/10</td><td>10 = 2 × 5</td><td>0.000110011…₂ (끝없음)</td></tr>
        <tr><td>0.2</td><td>1/5</td><td>5</td><td>0.00110011…₂ (끝없음)</td></tr>
        </tbody></table></div>
    """)
    write_text("분모에 2가 아닌 소인수(5, 3 등)가 하나라도 있으면 끝없이 이어져서, 정해진 칸에 담을 때 반올림 오차가 생겨요.")


def topic_rounding():
    """자세히 보기: 반올림 오차 = 끝없는 2진 소수를 정해진 칸에서 자르며 생기는 차이"""
    write_text(
        "끝없이 이어지는 2진 소수는 정해진 칸(가수 52칸)에 다 담을 수 없어서, **가장 가까운 값으로 반올림**해 저장해요. "
        "이때 생기는 아주 작은 차이가 **반올림 오차**예요."
    )
    render_html("""
        <div class="btg-table-wrap"><table class="btg-table">
        <thead><tr><th>입력한 수</th><th>컴퓨터에 실제로 저장된 값</th></tr></thead>
        <tbody>
        <tr><td>0.1</td><td>0.1000000000000000055511151231257827…</td></tr>
        <tr><td>0.2</td><td>0.2000000000000000111022302462515654…</td></tr>
        <tr><td>0.5</td><td>0.5 (2진수로 딱 떨어져 오차 없음)</td></tr>
        </tbody></table></div>
    """)
    st.markdown("#### 그런데 왜 평소에는 오차가 잘 안 보일까요?")
    st.code(
        "print(0.5 + 0.25)       # 0.75\n"
        "print(0.1 + 0.3)        # 0.4\n"
        "print(0.1 + 0.2)        # 0.30000000000000004\n"
        "print(0.1 + 0.2 == 0.3) # False",
        language="python",
    )
    write_text(
        "`0.5`와 `0.25`는 2진수로 정확하게 저장돼요. `0.1`과 `0.3`은 정확하지 않지만, 출력할 때 반올림되어 `0.4`로 보여요. "
        "반면 `0.1 + 0.2`는 작은 차이가 화면에도 드러나요. 그래서 실수를 `==`로 비교하면 예상과 다른 결과가 나올 수 있어요."
    )


def topic_floating():
    """자세히 보기: 부동소수점 = 소수점 위치를 움직여(지수) 큰 수와 작은 수를 함께 나타내는 방식"""
    st.markdown("#### 부동소수점(浮動小數點) — 소수점 위치를 움직이는 표현")
    write_text(
        "**부(浮)**는 뜨다, **동(動)**은 움직이다, **소수점(小數點)**은 숫자의 점을 뜻해요. "
        "소수점 위치를 옮기고 지수를 조정해 큰 수와 작은 수를 함께 나타내는 방식이에요."
    )
    render_html("""
        <div class="btg-table-wrap"><table class="btg-table">
        <thead><tr><th>수</th><th>소수점을 옮긴 모양</th></tr></thead>
        <tbody>
        <tr><td>123.45</td><td>1.2345 × 10²</td></tr>
        <tr><td>0.00012345</td><td>1.2345 × 10⁻⁴</td></tr>
        <tr><td>6.5 (2진수 110.1₂)</td><td>1.101₂ × 2²</td></tr>
        </tbody></table></div>
    """)
    write_text(
        "같은 '1.2345'를 지수만 바꿔서 아주 큰 수도, 아주 작은 수도 나타내요. "
        "컴퓨터는 이 원리를 **2진수**에 적용해서, 유효숫자와 '2의 몇 제곱인지'를 따로 저장해요."
    )


def topic_ieee():
    """자세히 보기: IEEE 754 = 64비트를 부호 1 · 지수 11 · 가수 52칸으로 나누는 국제 표준"""
    write_text("**IEEE 754**는 실수를 저장하는 국제 표준이에요. 64비트 실수는 칸을 **부호 · 지수 · 가수** 세 부분으로 나눠 저장해요.")
    render_html("""
        <div class="btg-table-wrap"><table class="btg-table">
        <thead><tr><th>부분</th><th>칸 수</th><th>하는 일</th></tr></thead>
        <tbody>
        <tr><td>부호</td><td>1</td><td>양수·음수 표시</td></tr>
        <tr><td>지수</td><td>11</td><td>수의 크기 조절 (2의 몇 제곱인지)</td></tr>
        <tr><td>가수</td><td>52</td><td>유효숫자 저장</td></tr>
        </tbody></table></div>
    """)
    write_text(
        "가수의 맨 앞자리는 항상 1이라서 저장하지 않고 생략해요. 그래서 52칸에 숨은 1칸을 더해 **53비트의 정밀도**를 써요.\n\n"
        "예) 0.1을 저장하면 `부호 0 · 지수 01111111011 · 가수 1001 1001 1001 …1010`"
    )


def topic_float_overflow():
    """자세히 보기: 부동소수점 오버플로 = 지수 칸이 꽉 차서 무한대(inf)가 된다"""
    write_text(
        "지수 칸은 11칸이라 나타낼 수 있는 '2의 몇 제곱'에 한계가 있어요. "
        "그래서 64비트 실수의 가장 큰 수는 **약 1.8 × 10³⁰⁸**이에요. 이보다 커지면 지수 칸이 모두 1로 꽉 차고, 값은 **inf(무한대)**가 돼요."
    )
    st.code(
        "print(1.8 * 10.0 ** 308)    # inf  (1.8 × 10³⁰⁸ : 가장 큰 수를 넘음)\n"
        "print(10.0 ** 308 * 10)     # inf  (10³⁰⁸ × 10)\n"
        "print(10 ** 309)            # Python 정수는 칸 제한이 없어서 그대로 계산됨",
        language="python",
    )
    write_text(
        "정수 오버플로는 **반대쪽 끝(음수)으로 넘어가지만**, 실수 오버플로는 **무한대에 멈춰요**. "
        "한 번 inf가 되면 다시 더하거나 빼도 원래 값으로 돌아오지 않아요."
    )


def topic_float_underflow():
    """자세히 보기: 부동소수점 언더플로 = 0에 너무 가까워 정밀도를 잃다가 0이 된다"""
    write_text(
        "**부동소수점 언더플로**는 수가 0에 너무 가까워져서 지수 칸으로 나타낼 수 없게 되는 현상이에요. "
        "정수 언더플로처럼 반대쪽 끝으로 넘어가는 게 아니라, **점점 정밀도를 잃다가 0이 돼요.**"
    )
    render_html("""
        <div class="btg-table-wrap"><table class="btg-table">
        <thead><tr><th>단계</th><th>크기</th><th>상태</th></tr></thead>
        <tbody>
        <tr><td>① 정상 수</td><td>약 2.2 × 10⁻³⁰⁸ 이상</td><td>53비트 정밀도 그대로</td></tr>
        <tr><td>② 비정규 수</td><td>약 2.2 × 10⁻³⁰⁸ 보다 작음</td><td>정밀도가 1비트씩 줄어듦</td></tr>
        <tr><td>③ 0</td><td>약 4.9 × 10⁻³²⁴ 의 절반 이하</td><td>담을 칸이 없어 0이 됨</td></tr>
        </tbody></table></div>
    """)
    write_text("예) 가장 작은 수(약 4.9 × 10⁻³²⁴) ÷ 2 → 0.0 (반으로 나누자 사라짐)")


def topic_subnormal():
    """자세히 보기: 비정규 수 = 지수 칸이 바닥(모두 0)일 때 가수의 앞자리를 0으로 채워 억지로 담은 수"""
    write_text(
        "정상 수는 가수의 맨 앞에 숨은 **1**이 있어요. 그런데 지수 칸이 바닥(모두 0)에 닿으면 더 작은 지수를 쓸 수 없어요. "
        "그래서 숨은 1을 **0으로 바꾸고, 가수의 앞자리를 0으로 채워** 더 작은 수를 담아요. 이것이 **비정규 수**예요."
    )
    render_html("""
        <div class="btg-table-wrap"><table class="btg-table">
        <thead><tr><th>값 (2로 계속 나누기)</th><th>남은 유효 비트</th></tr></thead>
        <tbody>
        <tr><td>약 2.2 × 10⁻³⁰⁸ (가장 작은 정상 수)</td><td>53비트</td></tr>
        <tr><td>약 1.1 × 10⁻³⁰⁸</td><td>52비트</td></tr>
        <tr><td>약 1.3 × 10⁻³¹⁵</td><td>29비트</td></tr>
        <tr><td>약 4.9 × 10⁻³²⁴ (가장 작은 비정규 수)</td><td>1비트</td></tr>
        </tbody></table></div>
    """)
    write_text(
        "덕분에 갑자기 0이 되지 않고 **천천히** 0에 가까워지지만, 그만큼 정밀도가 줄어서 계산 오차가 커져요."
    )


def topic_unix():
    """자세히 보기 ⑥ 유닉스 시간: 날짜를 초 하나로 세는 방식과 32비트의 끝(2038년)"""
    write_text(
        "**유닉스 시간**은 날짜를 '연·월·일'로 따로 저장하지 않고, "
        "**1970년 1월 1일 0시(UTC, 세계 표준시)부터 몇 초가 지났는지**를 정수 하나로 세는 방식이에요. "
        "숫자 하나라서 저장하고 비교하기 쉬워서 많은 컴퓨터가 써요."
    )
    render_html("""
        <div class="btg-table-wrap"><table class="btg-table">
        <thead><tr><th>유닉스 시간 (초)</th><th>날짜와 시각 (UTC)</th></tr></thead>
        <tbody>
        <tr><td>0</td><td>1970-01-01 00:00:00</td></tr>
        <tr><td>86,400</td><td>1970-01-02 00:00:00 (하루 = 86,400초)</td></tr>
        <tr><td>2,147,483,647</td><td>2038-01-19 03:14:07 (부호 있는 32비트의 최댓값)</td></tr>
        <tr><td>−2,147,483,648</td><td>1901-12-13 20:45:52 (1초 더 지나 넘친 값)</td></tr>
        </tbody></table></div>
    """)
    write_text(
        "이 초를 **부호 있는 32비트**에 담으면 2,147,483,647초까지만 셀 수 있어요. "
        "1초가 더 지나면 **오버플로**가 일어나 가장 작은 음수가 되고, 1970년보다 앞선 **1901년**으로 읽혀요. "
        "이것이 **2038년 문제**예요. 64비트로 늘리면 약 2,920억 년 뒤까지 셀 수 있어요."
    )
    st.markdown("#### 처음에는 왜 64비트가 아니라 32비트였을까요?")
    write_text(
        "유닉스가 만들어진 **1970년대**에는 메모리와 저장 공간이 아주 비쌌고, 컴퓨터가 한 번에 다루기 편한 데이터 크기(워드)도 작았어요. "
        "32비트는 4바이트, 64비트는 8바이트라서 64비트를 쓰면 시간 하나에 **두 배의 공간**이 필요했어요.\n\n"
        "또 32비트로도 1970년부터 **약 68년**(2038년까지)을 셀 수 있어서, 당시 개발자들에게는 충분히 긴 시간으로 느껴졌어요. "
        "그런데 그 방식이 수많은 프로그램과 파일 형식에 그대로 퍼지면서, 지금 64비트로 바꾸는 작업이 필요해진 거예요."
    )


# 자세히 보기 주제: 이름표 → (팝업 제목, 내용을 그리는 함수)
# 용어마다 하나씩, 서로 다른 내용이 열리도록 만들었다 (같은 팝업이 여러 용어에서 반복되지 않게)
TOPICS = {
    "bits": ("비트와 2진수", topic_bits),
    "sign": ("부호 비트", topic_sign_bit),
    "twos": ("2의 보수와 비트 연산", topic_twos),
    "overflow": ("정수 오버플로", topic_overflow),
    "underflow": ("정수 언더플로", topic_underflow),
    "unix": ("유닉스 시간과 2038년 문제", topic_unix),
    "fraction": ("2진 소수", topic_fraction),
    "rounding": ("반올림 오차", topic_rounding),
    "floating": ("부동소수점", topic_floating),
    "ieee": ("IEEE 754", topic_ieee),
    "f_overflow": ("부동소수점 오버플로", topic_float_overflow),
    "f_underflow": ("부동소수점 언더플로", topic_float_underflow),
    "subnormal": ("비정규 수", topic_subnormal),
}

# 용어 이름 → 열어 줄 자세히 보기 주제
TERM_TOPICS = {
    "비트": "bits", "부호 비트": "sign", "2의 보수": "twos",
    "정수 오버플로": "overflow", "정수 언더플로": "underflow", "유닉스 시간": "unix",
    "2진 소수": "fraction", "반올림 오차": "rounding",
    "부동소수점": "floating", "IEEE 754": "ieee", "부동소수점 오버플로": "f_overflow",
    "부동소수점 언더플로": "f_underflow", "비정규 수": "subnormal",
}


@st.dialog("자세히 보기", width="large")
def show_topic_dialog(topic_key):
    """용어 카드의 '자세히 보기'를 누르면 뜨는 팝업 창: 주제 제목과 내용을 보여 준다."""
    title, draw_topic = TOPICS[topic_key]
    st.markdown(f"### {title}")
    draw_topic()


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

def section_label(icon_name, title):
    """각 구역 위에 붙는 작은 제목. 예) ⚙ 컴퓨터 안에서 일어난 일"""
    return f'<div class="sec-label">{icon(icon_name)} {title}</div>'


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
                <div class="bt-box-label">{icon("visibility")} 직접 관찰</div>{escape(case['observation'])}
            </div>
        """
    render_html(f"""
        {section_label("search", "어떤 현상인가")}
        <div class="an-grid3">
            <div class="bt-box"><div class="bt-box-label">증상</div>{escape(case['symptom'])}</div>
            <div class="bt-box bt-ok"><div class="bt-box-label">정상이라면</div>{escape(case['expected'])}</div>
            <div class="bt-box bt-err"><div class="bt-box-label">실제로는</div>{escape(case['actual'])}</div>
        </div>
        {observed}
    """)


def show_flow(case):
    """③ 오류가 생기는 흐름을 '입력 → 처리 → 출력' 세 칸 그림으로 보여 준다."""
    flow = case["flow"]       # {"input": "...", "process": "...", "output": "..."}
    # 출력 칸(bt-flow-out)은 벽돌색으로 그려서 '이상한 결과'임을 강조한다.
    render_html(f"""
        {section_label("route", "컴퓨터 안에서 일어난 일")}
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


def group_steps(steps):
    """같은 근거 문서를 가리키는 단계를 한 카드로 합친다. 결과: [[단계, 단계], [단계], ...]
    예) BUG-002의 #01과 #03이 둘 다 'Python 공식 문서' → 카드 하나에 두 문장"""
    groups = []
    for step in steps:
        same_source = groups and groups[-1][-1]["source"] == step["source"] and groups[-1][-1]["basis"] == step["basis"]
        if same_source and step["source"] is not None:
            groups[-1].append(step)              # 앞 묶음과 같은 문서 → 그 묶음에 붙인다
        else:
            groups.append([step])                # 처음 나온 문서 → 새 묶음을 시작한다
    return groups


def show_steps(case):
    """④ 원인을 #01 → #02 … 순서의 추적 카드로 가로로 나란히 보여 준다. 같은 문서를 근거로 한 단계는 한 카드로 합친다."""
    cards = ""
    groups = group_steps(case["steps"])
    # enumerate(목록, start=1): 번호(1, 2, 3...)와 단계 묶음을 함께 꺼낸다.
    # 단계 하나는 {"basis": "확인" 또는 "추정", "source": 문서 번호, "text": "설명"} 형태의 딕셔너리다.
    for step_number, group in enumerate(groups, start=1):
        texts = "".join(f'<p>{escape(step["text"])}</p>' for step in group)
        cards += f"""
            <div class="an-step">
                <div class="an-step-head"><span class="bt-step-no">#{step_number:02d}</span>{basis_badge(case, group[0])}</div>
                <div class="an-step-text">{texts}</div>
            </div>
        """
    render_html(f"""
        {section_label("troubleshoot", "원인 추적 기록")}
        <div class="an-steps" style="--cols: {min(len(groups), 5)}">{cards}</div>
    """)   # --cols = 카드 수만큼 칸을 나눠서 5장까지는 한 줄에 다 놓는다 (아랫줄에 1장만 남아 빈 공간이 생기지 않게)


def show_key_point(case):
    """② 오류의 핵심 원리를 한 문장으로, 페이지에서 가장 눈에 띄게 보여 준다."""
    render_html(f"""
        <div class="bt-keypoint">
            {icon("lightbulb")}
            <div><div class="bt-keypoint-label">이것만 기억하세요</div>
            <div class="bt-keypoint-text">{escape(case['key_point'])}</div></div>
        </div>
    """)


def show_terms(case):
    """③ 먼저 알아 둘 용어를 한 줄 카드로 보여 준다. 설명이 더 필요한 용어는 '자세히 보기'로 팝업을 연다."""
    render_html(section_label("menu_book", "먼저 알아 둘 용어 · 더 궁금하면 '자세히 보기'"))
    terms = case["terms"]
    with st.container(key="term_row"):
        columns = st.columns(len(terms), gap="small")          # 용어 수만큼 칸을 만들어 한 줄에 놓는다
        for number, (column, term) in enumerate(zip(columns, terms)):
            with column, st.container(key=f"term_card_{number}"):
                render_html(f'<div class="bt-term-name">{escape(term["term"])}</div>'
                            f'<div class="bt-term-desc">{escape(term["desc"])}</div>')
                topic = TERM_TOPICS.get(term["term"])            # 이 용어와 연결된 자세히 보기 주제 (없으면 None)
                if topic and st.button("자세히 보기", key=f"term_more_{number}", width="stretch"):
                    show_topic_dialog(topic)


def show_sources(case):
    """⑧ 근거가 된 공식 문서 목록 (누르면 새 탭에서 열린다)"""
    items = ""
    for number, source in enumerate(case["sources"], start=1):
        items += f'<li><a href="{escape(source["url"])}" target="_blank">{escape(source["title"])} ↗</a></li>'
    render_html(f'{section_label("library_books", "출처")}<div class="bt-box"><ol class="an-sources">{items}</ol></div>')


def show_video(case):
    """⑦ 관련 영상: 데이터에 video가 있는 사례에서만 YouTube 영상을 바로 재생할 수 있게 넣는다."""
    video = case["video"]               # {"title": "...", "url": "..."} 또는 None
    render_html(section_label("smart_display", "영상으로 한 번 더"))
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
        # 영상 옆 빈 공간을 쓰려고 실험실 버튼을 안내 상자 바로 아래에 놓는다
        show_lab_link(case)


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
        .an-grid3 .bt-box { margin: 0; white-space: pre-line; }   /* pre-line: 데이터 속 줄바꿈(\n)을 화면에서도 줄바꿈으로 보여 준다 */
        .an-observed { margin-top: 10px; }
        /* 원인 추적 카드: 화면 폭에 맞춰 한 줄에 최대 4장, 높이는 모두 같게 */
        .an-steps { display: grid; grid-template-columns: repeat(var(--cols, 4), minmax(0, 1fr)); gap: 10px; margin-bottom: 16px; }
        @media (max-width: 900px) { .an-steps { grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); } }   /* 좁은 화면에서는 자동으로 줄바꿈 */
        .an-step { background: var(--paper); border: 3px solid var(--ink); padding: 10px 10px; }
        .an-step-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px; }
        .an-step-head .bt-step-no { flex: none; width: 42px; height: 32px; line-height: 28px; padding: 0; text-align: center; }
        /* 카드 5장이 한 줄에 들어가 폭이 좁아져도 '문서로 확인 ↗'이 두 줄로 깨지지 않게 */
        .an-step-head .bt-basis { white-space: nowrap; padding: 0 3px; margin-left: 4px; letter-spacing: -0.02em; }
        .an-step-text { font-size: 0.98rem; line-height: 1.7; color: var(--text); }
        .an-step-text p { margin: 0 0 6px; }   /* 한 카드에 합쳐진 문장 사이 간격 */
        .an-sources { margin: 0; padding-left: 22px; line-height: 1.9; }
        .an-sources a { color: #2F6B2A; font-weight: 700; }
        @media (max-width: 800px) { .an-grid3 { grid-template-columns: 1fr; } }

        /* 용어 카드: 한 줄에 나란히, 높이는 모두 같게, '자세히 보기' 버튼은 카드 맨 아래 */
        .st-key-term_row [data-testid="stHorizontalBlock"] { align-items: stretch; }
        .st-key-term_row [data-testid="stColumn"] > [data-testid="stVerticalBlock"] { height: 100%; }
        .st-key-term_row [data-testid="stLayoutWrapper"]:has(> [class*="st-key-term_card_"]) { flex: 1 1 auto; }
        [class*="st-key-term_card_"] { height: 100%; gap: 4px; background: var(--paper); border: 2px solid var(--ink);
                                       border-top: 6px solid var(--ink); padding: 10px 10px 2px; }
        [class*="st-key-term_card_"] > [data-testid="stElementContainer"]:has(.stButton) { margin-top: auto; }
        [class*="st-key-term_card_"] div.stButton { padding-top: 2px; }
        [class*="st-key-term_card_"] div.stButton button { min-height: 32px; padding: 2px 6px; margin: 4px 4px 8px; }
        [class*="st-key-term_card_"] div.stButton button p { font-size: 0.88rem !important; }
        /* 자세히 보기 팝업 안의 글 */
        div[role="dialog"] p, div[role="dialog"] li { font-size: 1.02rem; line-height: 1.75; word-break: keep-all; }
        div[role="dialog"] h4 { margin: 14px 0 6px !important; }
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
            .btg-table th, .btg-table td { padding: 8px 6px; }
            .btg-bits { gap: 2px; }
            .btg-bits small { font-size: .68rem; }
            .btg-bits span { padding: 7px 0; }
        }
        .btg-twos { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:10px; margin:10px 0; }
        .btg-twos > div { display:flex; flex-direction:column; gap:10px; padding:14px 10px; border:2px solid #1F4D25; background:#F6F9E8; text-align:center; }
        .btg-twos code { font-size:clamp(.85rem,1.5vw,1.15rem); overflow-wrap:anywhere; }
        @media(max-width:680px){.btg-twos{grid-template-columns:1fr;}}
        </style>
    """)


# ----- 실제 실행 순서 -----
all_cases = load_cases()
apply_anatomy_style()

with crt_frame("pages/anatomy.py", "ANATOMY"):
    page_banner("layers", "ROOT CAUSE", "원인 해부실", "오류가 발생하는 내부 처리 과정을 한 단계씩 추적합니다.")
    show_case_selector(all_cases)                                               # 오류 고르기
    current_case = find_case(all_cases, st.session_state["anatomy_case"])       # 고른 오류 데이터

    show_title(current_case)                  # ① 제목
    show_key_point(current_case)              # ② 핵심 원리 (가장 크게)
    show_terms(current_case)                  # ③ 먼저 알아 둘 용어 (+ 자세히 보기 팝업)
    show_symptom_row(current_case)            # ④ 증상 · 정상이라면 · 실제로는 (+ 직접 관찰)
    show_flow(current_case)                   # ⑤ 처리 과정
    show_steps(current_case)                  # ⑥ 원인 추적 기록
    if current_case["video"]:                 # ⑦ 관련 영상이 있는 사례: 영상 + 옆에 안내와 실험실 버튼
        show_video(current_case)
    else:
        show_lab_link(current_case)           # ⑧ 영상이 없으면 실험실 버튼만 한 줄로
    show_sources(current_case)                # ⑨ 출처 (누르면 문서가 열린다)
    show_detail_tabs(all_cases, current_case) # ⑩ 아래 탭
