import time
import streamlit as st

# ------------------------------
# 기본 설정
# ------------------------------
STUDY_MINUTES = 55
BREAK_MINUTES = 5

st.set_page_config(page_title="공부 타이머", page_icon="⏰", layout="centered")

# ------------------------------
# 세션 상태 초기화
# ------------------------------
if "mode" not in st.session_state:
    st.session_state.mode = "study"          # "study" 또는 "break"
if "remaining" not in st.session_state:
    st.session_state.remaining = STUDY_MINUTES * 60
if "running" not in st.session_state:
    st.session_state.running = False
if "study_count" not in st.session_state:
    st.session_state.study_count = 0
if "last_tick" not in st.session_state:
    st.session_state.last_tick = None


def get_duration(mode: str) -> int:
    return STUDY_MINUTES * 60 if mode == "study" else BREAK_MINUTES * 60


def switch_mode():
    """현재 모드가 끝났을 때 다음 모드로 전환"""
    if st.session_state.mode == "study":
        st.session_state.study_count += 1
        st.session_state.mode = "break"
    else:
        st.session_state.mode = "study"
    st.session_state.remaining = get_duration(st.session_state.mode)


def tick():
    """실행 중이면 흐른 시간만큼 남은 시간을 갱신"""
    if st.session_state.running:
        now = time.time()
        if st.session_state.last_tick is not None:
            elapsed = now - st.session_state.last_tick
            st.session_state.remaining -= elapsed
        st.session_state.last_tick = now

        if st.session_state.remaining <= 0:
            st.session_state.remaining = 0
            switch_mode()
            st.session_state.last_tick = time.time()


def start_timer():
    st.session_state.running = True
    st.session_state.last_tick = time.time()


def pause_timer():
    # 정지 직전까지 흐른 시간 반영
    tick()
    st.session_state.running = False
    st.session_state.last_tick = None


def reset_timer():
    st.session_state.running = False
    st.session_state.mode = "study"
    st.session_state.remaining = get_duration("study")
    st.session_state.study_count = 0
    st.session_state.last_tick = None


# ------------------------------
# 시간 갱신
# ------------------------------
tick()

remaining = max(0, int(st.session_state.remaining))
minutes, seconds = divmod(remaining, 60)
time_str = f"{minutes:02d}:{seconds:02d}"

mode_label = "📖 공부 시간" if st.session_state.mode == "study" else "☕ 휴식 시간"
mode_color = "#2563EB" if st.session_state.mode == "study" else "#16A34A"

# ------------------------------
# 화면 렌더링
# ------------------------------
st.markdown(
    "<h2 style='text-align:center;'>⏰ 공부 타이머</h2>",
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div style='text-align:center; margin-top:10px; margin-bottom:10px;'>
        <span style='font-size:32px; font-weight:bold; color:{mode_color};'>
            {mode_label}
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div style='text-align:center; margin:30px 0;'>
        <span style='font-size:120px; font-weight:800; font-family:monospace; color:{mode_color};'>
            {time_str}
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div style='text-align:center; margin-bottom:30px;'>
        <span style='font-size:20px;'>✅ 완료한 공부 횟수: <b>{st.session_state.study_count}</b>회</span>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("▶️ 시작", use_container_width=True, disabled=st.session_state.running):
        start_timer()
        st.rerun()
with col2:
    if st.button("⏸️ 일시정지", use_container_width=True, disabled=not st.session_state.running):
        pause_timer()
        st.rerun()
with col3:
    if st.button("🔄 초기화", use_container_width=True):
        reset_timer()
        st.rerun()

# ------------------------------
# 1초마다 자동 갱신 (실행 중일 때만)
# ------------------------------
if st.session_state.running:
    time.sleep(1)
    st.rerun()
