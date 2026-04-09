"""
pages/2_teams.py — All 10 IPL team cards. Click a team to see its squad.
"""
import streamlit as st
import os, sys

st.set_page_config(
    page_title="IPL Orbital — Teams",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed",
)

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from data import inject_css, TEAMS, hex_to_rgba, initials

inject_css()

# Redirect if no data loaded
if "stats" not in st.session_state:
    st.switch_page("pages/1_dataset.py")

# ── Page CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.page-header { margin-bottom: 28px; }
.page-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 42px; letter-spacing: 4px; display: inline;
}
.data-label {
    font-size: 11px; color: rgba(255,255,255,.3);
    letter-spacing: 1px; margin-top: 4px;
}
.team-card {
    border-radius: 18px; overflow: hidden;
    border: 1.5px solid rgba(255,255,255,.1);
    cursor: pointer; transition: all .22s;
    height: 200px; display: flex; flex-direction: column;
    text-decoration: none;
}
.team-card:hover { transform: translateY(-5px); border-color: rgba(255,255,255,.3); }
.tc-top {
    flex: 1; display: flex; align-items: center; justify-content: center;
    position: relative; overflow: hidden;
}
.tc-top::after {
    content: ''; position: absolute;
    bottom: 0; left: 0; right: 0; height: 45%;
    background: linear-gradient(transparent, rgba(0,0,0,.6));
}
.tc-logo {
    width: 86px; height: 86px; object-fit: contain;
    z-index: 1; position: relative;
    filter: drop-shadow(0 3px 10px rgba(0,0,0,.5));
}
.tc-logo-fb {
    width: 86px; height: 86px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Bebas Neue', sans-serif; font-size: 22px;
    z-index: 1; position: relative;
    border: 3px solid rgba(255,255,255,.35);
}
.tc-bot {
    padding: 10px; background: rgba(0,0,0,.5); text-align: center;
}
.tc-name { font-size: 11px; font-weight: 600; color: #fff; line-height: 1.3; }
.chg-btn-wrap { display: flex; justify-content: flex-end; margin-bottom: 16px; }
</style>
""", unsafe_allow_html=True)

# ── TOP BAR ───────────────────────────────────────────────────────────────────
col_title, col_ph, col_btn = st.columns([5, 1.3, 1])
with col_title:
    st.markdown(f"""
    <div class="page-header">
      <div class="page-title">IPL ORBITAL</div>
      <div class="data-label">{st.session_state.get('data_label','')}</div>
    </div>
    """, unsafe_allow_html=True)
with col_ph:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    if st.button("📈 Phase Analysis", key="ph_nav", use_container_width=True):
        st.switch_page("pages/6_phase.py")
with col_btn:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    if st.button("⇄ Change Dataset", key="chg"):
        del st.session_state["stats"]
        st.session_state.pop("data_label", None)
        st.switch_page("pages/1_dataset.py")

st.markdown("<div style='font-size:11px;color:rgba(255,255,255,.28);letter-spacing:2px;text-transform:uppercase;margin-bottom:24px'>Select a team to explore</div>", unsafe_allow_html=True)

# ── TEAM GRID (5 + 5) ─────────────────────────────────────────────────────────
team_codes = list(TEAMS.keys())
rows = [team_codes[:5], team_codes[5:]]

for row in rows:
    cols = st.columns(5)
    for col, code in zip(cols, row):
        t = TEAMS[code]
        c = t["color"]
        bg = hex_to_rgba(c, 0.18)
        grad = f"linear-gradient(160deg, {hex_to_rgba(c, 0.25)} 0%, rgba(13,19,33,.95) 100%)"

        with col:
            st.markdown(f"""
            <div class="team-card" style="background:{grad}">
              <div class="tc-top" style="background:{bg}">
                <img class="tc-logo" src="{t['logo']}" alt="{code}"
                     onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
                <div class="tc-logo-fb" style="display:none;background:{hex_to_rgba(c,.25)};color:{c}">{code}</div>
              </div>
              <div class="tc-bot"><div class="tc-name">{t['name']}</div></div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Select {code}", key=f"team_{code}", use_container_width=True):
                st.session_state["selected_team"] = code
                st.switch_page("pages/3_players.py")

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
