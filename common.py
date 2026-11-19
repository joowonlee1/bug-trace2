        div[data-testid="stRadio"] > div[role="radiogroup"] > label p { font-family: 'Galmuri11', sans-serif !important; font-size: 0.98rem !important; font-weight: 700 !important; color: var(--ink) !important; }
        div[data-testid="stRadio"] > div[role="radiogroup"] > label [data-testid="stIconMaterial"] { color: var(--ink) !important; }
        div[data-testid="stRadio"] > div[role="radiogroup"] > label > div:first-child { width: 0; height: 0; overflow: hidden; margin: 0; padding: 0; }   /* 동그란 라디오 표시 숨기기 */

        /* ===== 11) 설명 상자 (정상 = 초록, 오류 = 벽돌, 핵심 = 황토, 관찰 = 파랑) ===== */
        .bt-box { background: var(--paper); border: 2px solid var(--ink); padding: 12px 16px; margin-bottom: 8px; color: var(--text); line-height: 1.75; font-size: 1rem; }
        .bt-box-label { font-family: 'Galmuri11', monospace; font-size: 0.92rem; font-weight: 700; margin-bottom: 5px; }
        .bt-ok { border-left: 8px solid #2F6B2A; } .bt-ok .bt-box-label { color: #2F6B2A; }
        .bt-obs { border-left: 8px solid var(--sky); } .bt-obs .bt-box-label { color: var(--sky); }
        .bt-err { border-left: 8px solid var(--red); } .bt-err .bt-box-label { color: var(--red); }
        .bt-key { border-left: 8px solid var(--yellow); } .bt-key .bt-box-label { color: var(--yellow); }

        /* 처리 과정 그림 (입력 → 처리 → 출력) */
        .bt-flow { display: flex; align-items: stretch; gap: 8px; margin: 2px 0 6px 0; }
        .bt-flow-box { flex: 1; text-align: center; padding: 8px 8px; border: 3px solid var(--ink); background: var(--lime-soft); }
        .bt-flow-box .bt-icon { font-size: 1.6rem; color: var(--ink); }
        .bt-flow-name { font-family: 'Galmuri11', sans-serif; color: var(--ink); font-weight: 700; margin: 2px 0; }
        .bt-flow-text { color: var(--text); font-size: 0.97rem; line-height: 1.55; }
        .bt-flow-out { border-color: var(--red); background: #FBE7DF; }
        .bt-flow-out .bt-icon, .bt-flow-out .bt-flow-name { color: var(--red); }
        .bt-flow-arrow { align-self: center; color: var(--ink); font-size: 1.4rem; font-weight: 800; }

        /* 단계 번호표 (#01 → #02 …) */
        .bt-step-no { flex: 0 0 44px; height: 36px; text-align: center; line-height: 32px; background: var(--lime); color: var(--ink); border: 2px solid var(--ink); font-family: 'Galmuri11', monospace; font-weight: 700; }
        .bt-basis { display: inline-block; font-family: 'Galmuri11', monospace; font-size: 0.78rem; font-weight: 700; padding: 0 6px; margin-bottom: 2px; background: var(--paper); }
        .bt-basis-ok { color: #2F6B2A; border: 2px solid #2F6B2A; }
        .bt-basis-guess { color: var(--yellow); border: 2px solid var(--yellow); }

        /* 0과 1을 픽셀 칸으로 (현상 실험실 · 오류 검출에서 함께 사용)
           .one = 1(라임) / .zero = 0 / .sign = 부호 비트(빨간 테두리) / .flip = 뒤집힌 칸(빨강) / .par = 패리티 칸(파랑) */
        .bits-label { font-family: 'Galmuri11', sans-serif; font-weight: 700; color: var(--ink); margin: 8px 0 4px; }
        .bits { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 6px; }
        .bits .byte { display: flex; gap: 2px; }
        .bits span { width: 20px; height: 28px; line-height: 24px; text-align: center; border: 2px solid var(--ink);
                     font-family: 'Galmuri11', monospace; font-weight: 700; color: var(--ink); }
        .bits .one { background: var(--lime); }
        .bits .zero { background: var(--paper); }
        .bits .sign { outline: 3px solid var(--red); outline-offset: 1px; }
        .bits .flip { background: var(--red); color: #FFFFFF; }
        .bits .par { background: #D6E8F7; border-color: var(--sky); color: var(--sky); margin-left: 6px; }

        /* 작은 이름표 (BUG-001, 분류, 기술 등) */
        .bt-badge { display: inline-block; font-family: 'Galmuri11', monospace; font-size: 0.82rem; font-weight: 700; border: 2px solid var(--ink); padding: 1px 8px; margin: 0 4px 4px 0; color: var(--ink); background: var(--paper); }
        .bt-badge-on { background: var(--lime); }

        /* ===== 11-1) 고정된 모니터 안에서만 스크롤 =====
           모니터 틀·창 제목 줄·메뉴는 그대로 두고, 페이지 내용 상자(win_body)만 정해진 높이 안에서 스크롤한다.
           예전에는 '위아래 고정 부분 = 340px'로 숫자를 정해 두어서, 화면을 확대하거나 노트북처럼 세로가 짧으면 내용 칸이 너무 작아졌다.
           그래서 모니터 전체를 브라우저 높이(100vh)에 맞추고, 내용 상자가 '남은 공간'을 자동으로 채우게 바꿨다.
           flex: 1 1 0 = 남은 공간을 모두 차지 / min-height: 0 = 내용이 길어도 상자가 늘어나지 않고 안에서 스크롤 */
        html, body { overflow: hidden; }                                   /* 페이지 전체는 스크롤하지 않는다 */
        [data-testid="stMain"] { overflow: hidden; }
        /* Streamlit은 상자를 한 겹 더 감싸므로(stLayoutWrapper), 높이는 그 감싼 상자에 준다. 26px = 페이지 위아래 여백 */
        [data-testid="stLayoutWrapper"]:has(> .st-key-crt), [data-testid="stLayoutWrapper"]:has(> .st-key-crt_max) { height: calc(100vh - 26px); flex: none; }
        .st-key-crt, .st-key-crt_max { flex: 1 1 0; min-height: 0; }
        .st-key-crt > [data-testid="stLayoutWrapper"]:has(> .st-key-crt_screen),
        .st-key-crt_max > [data-testid="stLayoutWrapper"]:has(> .st-key-crt_screen) { flex: 1 1 0; min-height: 0; }
        .st-key-crt_screen { flex: 1 1 0; min-height: 0; }
        .st-key-crt_screen > [data-testid="stLayoutWrapper"]:has(> .st-key-win_body) { flex: 1 1 0; min-height: 0; }
        /* !important: Streamlit이 상자에 자동으로 넣는 높이 설정보다 우선하게 한다 */
        .st-key-win_body { flex: 1 1 0 !important; min-height: 0 !important; height: auto !important; max-height: none !important;
                           overflow-y: auto !important; overflow-x: hidden; padding: 4px 14px 24px 4px; }
        /* 최소화 중에는 내용이 없으니 모니터를 내용 높이만큼만 */
        [data-testid="stLayoutWrapper"]:has(> .st-key-crt .st-key-win_hidden) { height: auto; }
        .st-key-crt:has(.st-key-win_hidden), .st-key-crt:has(.st-key-win_hidden) .st-key-crt_screen,
        .st-key-crt:has(.st-key-win_hidden) [data-testid="stLayoutWrapper"]:has(> .st-key-crt_screen) { flex: none; }
        /* 스크롤 막대도 픽셀 느낌으로 */
        .st-key-win_body::-webkit-scrollbar { width: 14px; }
        .st-key-win_body::-webkit-scrollbar-track { background: var(--lime-soft); border-left: 3px solid var(--ink); }
        .st-key-win_body::-webkit-scrollbar-thumb { background: var(--ink); border: 3px solid var(--lime-soft); }

        /* ===== 11-2) 핵심 원리 강조 상자 (가장 눈에 띄게) ===== */
        .bt-keypoint { display: flex; gap: 14px; align-items: center; background: var(--lime); color: var(--ink); padding: 16px 20px; margin: 10px 6px 14px;
                       box-shadow: 0 -5px 0 0 var(--ink), 0 5px 0 0 var(--ink), -5px 0 0 0 var(--ink), 5px 0 0 0 var(--ink), 0 10px 0 0 rgba(31,77,37,.25); }
        .bt-keypoint .bt-icon { font-size: 2.4rem; }
        .bt-keypoint-label { font-family: 'Galmuri11', monospace; font-weight: 700; font-size: 0.9rem; }
        .bt-keypoint-text { font-family: 'Noto Sans KR', sans-serif; font-weight: 800; font-size: 1.18rem; line-height: 1.55; }

        /* ===== 11-3) 먼저 알아 둘 용어 (화면 폭에 맞춰 카드가 여러 줄로 놓인다) ===== */
        .bt-terms { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 10px; margin-bottom: 6px; }
        .bt-term { background: var(--paper); border: 2px solid var(--ink); border-top: 6px solid var(--ink); padding: 10px 12px; }
        .bt-term-name { font-family: 'Galmuri11', sans-serif; font-weight: 700; color: var(--ink); font-size: 1rem; margin-bottom: 4px; }
        .bt-term-desc { font-size: 0.95rem; line-height: 1.6; color: var(--text); }

        /* ===== 11-4) 구역 제목 (SYMPTOM · 어떤 현상인가 등) ===== */
        .sec-label { font-family: 'Galmuri11', sans-serif; font-weight: 700; color: var(--ink); font-size: 1.08rem;
                     border-bottom: 3px solid var(--ink); padding-bottom: 4px; margin: 22px 0 10px; }

        /* ===== 11-5) 사례 선택 상자: 눈에 잘 띄게 (라임색 띠 + 큰 글자) ===== */
        .st-key-case_pick { background: var(--lime); padding: 2px 14px 4px; margin: 4px 6px 10px;
                            box-shadow: 0 -4px 0 0 var(--ink), 0 4px 0 0 var(--ink), -4px 0 0 0 var(--ink), 4px 0 0 0 var(--ink); }
        .st-key-case_pick [data-testid="stWidgetLabel"] p { font-family: 'Galmuri11', sans-serif !important; font-size: 1.05rem !important; }
        .st-key-case_pick div[data-baseweb="select"] > div { min-height: 52px; border-width: 4px; }
        .st-key-case_pick div[data-baseweb="select"] div { font-size: 1.1rem; font-weight: 700; color: var(--ink); }

        /* ===== 11-6) '문서로 확인' 이름표 = 누르면 공식 문서가 새 탭에서 열리는 링크 ===== */
        a.bt-basis-ok { text-decoration: none !important; cursor: pointer; }
        a.bt-basis-ok:hover { background: var(--lime); }

        /* ===== 11-7) 오류 도감의 넓은 사례 카드 ===== */
        .cat-head { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; }
        .cat-title { font-family: 'Noto Sans KR', sans-serif; font-weight: 800; color: var(--ink); font-size: 1.3rem; margin: 6px 0 2px; }
        .cat-summary { font-size: 1rem; line-height: 1.7; color: var(--text); margin: 4px 0 8px; }
        .cat-terms { display: flex; flex-wrap: wrap; gap: 6px; }
        .cat-terms span { font-size: 0.9rem; background: var(--lime-soft); border: 2px solid var(--ink); padding: 2px 8px; color: var(--ink); cursor: help; }   /* cursor: help = 마우스 모양이 물음표로 바뀌어 설명이 있음을 알려 준다 */
        .cat-terms span:hover { background: var(--lime); }
        .cat-terms b { font-family: 'Galmuri11', sans-serif; }
        .cat-flow { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; margin: 6px 0 12px; font-family: 'Galmuri11', sans-serif; color: var(--ink); }
        .cat-flow span { background: var(--paper); border: 2px solid var(--ink); padding: 3px 10px; font-weight: 700; }
        /* ===== 12) 좁은 화면(휴대폰) ===== */
        @media (max-width: 800px) {
            .st-key-crt { padding: 10px 8px 6px; border-radius: 18px; }
            .st-key-crt_screen { padding: 8px 8px 12px; border-width: 4px; border-radius: 14px; }
            .win-title { font-size: 0.95rem; } .win-path { display: none; }
            .win-logo .px-computer { width: 40px; }
            .bt-banner-en { font-size: 0.9rem; } .bt-banner-ko { font-size: 1rem; }
            .px-grill, .px-floppy { display: none; }
            .bt-flow { flex-direction: column; } .bt-flow-arrow { transform: rotate(90deg); }
            html, body, [data-testid="stMain"] { overflow: auto; }          /* 휴대폰은 화면이 작아서 페이지 전체 스크롤 */
            /* 휴대폰: 높이를 맞추지 않고 내용만큼 길게, 페이지 전체를 스크롤한다 */
            [data-testid="stLayoutWrapper"]:has(> .st-key-crt), [data-testid="stLayoutWrapper"]:has(> .st-key-crt_max) { height: auto; }
            .st-key-crt, .st-key-crt_max, .st-key-crt_screen, .st-key-win_body,
            [data-testid="stLayoutWrapper"]:has(> .st-key-crt_screen), [data-testid="stLayoutWrapper"]:has(> .st-key-win_body) { flex: none !important; }
            .st-key-win_body { height: auto !important; max-height: none !important; overflow: visible !important; }
        }
        @media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; } }
        </style>
    """)
