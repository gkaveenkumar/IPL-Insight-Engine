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
.req-note {
    font-size: 11px; color: rgba(255,255,255,.22);
    text-align: center; line-height: 2; margin-top: 32px;
}
.req-note strong { color: rgba(255,255,255,.5); }

/* ── File uploader — big styled zone ── */
[data-testid="stFileUploader"] {
    max-width: 500px;
    margin: 0 auto 20px !important;
}
[data-testid="stFileUploaderDropzone"] {
    background: rgba(255,255,255,.04) !important;
    border: 1.5px dashed rgba(255,255,255,.35) !important;
    border-radius: 20px !important;
    padding: 48px 36px !important;
    text-align: center !important;
    transition: all .22s !important;
}
[data-testid="stFileUploaderDropzone"]:hover {
    border-color: rgba(255,255,255,.55) !important;
    background: rgba(255,255,255,.07) !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    gap: 6px !important;
}
[data-testid="stFileUploaderDropzoneInstructions"]::before {
    content: "📁";
    font-size: 48px;
    display: block;
    margin-bottom: 10px;
}
[data-testid="stFileUploaderDropzoneInstructions"] span {
    color: rgba(255,255,255,.85) !important;
    font-size: 16px !important;
    font-weight: 600 !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] small {
    color: rgba(255,255,255,.4) !important;
    font-size: 12px !important;
}
[data-testid="stFileUploader"] button {
    background: rgba(255,255,255,.12) !important;
    color: rgba(255,255,255,.9) !important;
    border: 1px solid rgba(255,255,255,.25) !important;
    border-radius: 8px !important;
    margin-top: 8px !important;
}
[data-testid="stFileUploader"] button:hover {
    background: rgba(255,255,255,.22) !important;
    border-color: rgba(255,255,255,.5) !important;
}
</style>
""", unsafe_allow_html=True)

# ── PAGE HEADER ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="up-hero">
  <div class="up-title">IPL ORBITAL</div>
  <div class="up-sub">Ball-by-Ball Head-to-Head Stats Explorer</div>
</div>
""", unsafe_allow_html=True)

# ── FILE UPLOADER ─────────────────────────────────────────────────────────────
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
