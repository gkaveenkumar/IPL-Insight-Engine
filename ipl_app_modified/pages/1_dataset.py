"""
pages/1_dataset.py — Dataset upload / selection page.
"""
import streamlit as st
import pandas as pd
import os, sys

st.set_page_config(
    page_title="IPL Orbital — Load Data",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from data import inject_css, build_stats, build_phase_stats, hex_to_rgba, GLOBAL_CSS

inject_css()

# ── Extra page CSS ────────────────────────────────────────────────────────────
st.markdown("""
<style>
.up-hero { text-align:center; padding: 60px 20px 40px; }
.up-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 56px; letter-spacing: 6px;
    background: linear-gradient(135deg, #fff 0%, rgba(255,255,255,.5) 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
}
.up-sub {
    font-size: 12px; color: rgba(255,255,255,.3);
    letter-spacing: 3px; text-transform: uppercase; margin-bottom: 52px;
}
.up-zone {
    max-width: 500px; margin: 0 auto 20px;
    background: rgba(255,255,255,.04);
    border: 1.5px dashed rgba(255,255,255,.18);
    border-radius: 20px; padding: 48px 36px; text-align: center;
    cursor: pointer; transition: all .22s;
}
.up-zone:hover { border-color: rgba(255,255,255,.4); background: rgba(255,255,255,.07); }
.up-icon { font-size: 48px; margin-bottom: 14px; }
.up-main { font-size: 16px; font-weight: 600; margin-bottom: 6px; }
.up-hint { font-size: 12px; color: rgba(255,255,255,.35); }
.or-sep {
    font-size: 12px; color: rgba(255,255,255,.2);
    letter-spacing: 3px; text-align: center; margin: 24px 0;
}
.req-note {
    font-size: 11px; color: rgba(255,255,255,.22);
    text-align: center; line-height: 2; margin-top: 32px;
}
.req-note strong { color: rgba(255,255,255,.5); }
.demo-card {
    max-width: 500px; margin: 0 auto;
    background: rgba(255,255,255,.05);
    border: 1px solid rgba(255,255,255,.12);
    border-radius: 16px; padding: 24px 28px;
    display: flex; align-items: center; justify-content: space-between;
    gap: 16px;
}
.demo-info { flex: 1; }
.demo-title { font-size: 15px; font-weight: 600; margin-bottom: 4px; }
.demo-meta { font-size: 11px; color: rgba(255,255,255,.4); }
</style>
""", unsafe_allow_html=True)

# ── PAGE HEADER ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="up-hero">
  <div class="up-title">IPL ORBITAL</div>
  <div class="up-sub">Ball-by-Ball Head-to-Head Stats Explorer</div>
</div>
""", unsafe_allow_html=True)

# ── BUILT-IN DATA OPTION ──────────────────────────────────────────────────────
st.markdown("""
<div class="demo-card">
  <div class="demo-info">
    <div class="demo-title">📊 IPL 2025 Built-in Dataset</div>
    <div class="demo-meta">11,574 balls · All 10 teams · Full season data</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

col_btn, col_space = st.columns([1, 3])
with col_btn:
    if st.button("▶  Use IPL 2025 Data", use_container_width=True):
        builtin_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ipl_2025.xlsx")
        if not os.path.exists(builtin_path):
            builtin_path = "/mnt/user-data/uploads/ipl_2025.xlsx"
        with st.spinner("Loading built-in dataset..."):
            try:
                df = pd.read_excel(builtin_path)
                st.session_state["stats"] = build_stats(df)
                st.session_state["phase_stats"] = build_phase_stats(df)
                st.session_state["data_label"] = f"📊 IPL 2025 Built-in · {len(df):,} balls"
                st.switch_page("pages/2_teams.py")
            except Exception as e:
                st.error(f"Could not load built-in data: {e}")

# ── DIVIDER ───────────────────────────────────────────────────────────────────
st.markdown('<div class="or-sep">— OR UPLOAD YOUR OWN —</div>', unsafe_allow_html=True)

# ── FILE UPLOADER ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="up-zone">
  <div class="up-icon">📁</div>
  <div class="up-main">Upload Your Dataset</div>
  <div class="up-hint">Supports .xlsx / .xls / .csv</div>
</div>
""", unsafe_allow_html=True)

uploaded = st.file_uploader(
    "Drop your file here",
    type=["xlsx", "xls", "csv"],
    label_visibility="collapsed",
)

if uploaded:
    with st.spinner(f"Processing {uploaded.name}..."):
        try:
            df = pd.read_csv(uploaded) if uploaded.name.endswith(".csv") else pd.read_excel(uploaded)
            required = {"batsman", "bowler", "event", "bowling_type", "shot_type", "line"}
            missing  = required - set(df.columns)
            if missing:
                st.error(f"❌ Missing required columns: **{', '.join(sorted(missing))}**")
                st.info("Your file must contain: " + " · ".join(sorted(required)))
            else:
                prog = st.progress(0, "Reading rows...")
                prog.progress(30, "Computing matchup stats...")
                stats = build_stats(df)
                prog.progress(70, "Computing phase stats...")
                phase_stats = build_phase_stats(df)
                prog.progress(100, "Done!")
                st.session_state["stats"] = stats
                st.session_state["phase_stats"] = phase_stats
                st.session_state["data_label"] = f"📂 {uploaded.name} · {len(df):,} balls"
                st.success(f"✅ Loaded **{len(df):,}** balls. Redirecting...")
                st.switch_page("pages/2_teams.py")
        except Exception as e:
            st.error(f"Error reading file: {e}")

# ── REQUIRED COLUMNS NOTE ─────────────────────────────────────────────────────
st.markdown("""
<div class="req-note">
  Required columns in your file:<br>
  <strong>batsman &nbsp;·&nbsp; bowler &nbsp;·&nbsp; event &nbsp;·&nbsp; bowling_type &nbsp;·&nbsp; shot_type &nbsp;·&nbsp; line</strong>
</div>
""", unsafe_allow_html=True)
