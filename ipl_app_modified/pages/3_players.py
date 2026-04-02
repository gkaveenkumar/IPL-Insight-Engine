"""
pages/3_players.py — Squad list for selected team. Click a player to see their orbit.
"""
import streamlit as st
import os, sys

st.set_page_config(
    page_title="IPL Orbital — Players",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="collapsed",
)

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from data import inject_css, TEAMS, hex_to_rgba, initials, ROLE_SHORT

inject_css()

if "stats" not in st.session_state:
    st.switch_page("pages/1_dataset.py")
if "selected_team" not in st.session_state:
    st.switch_page("pages/2_teams.py")

# ── Page CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.role-header {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 16px; letter-spacing: 2px;
    color: rgba(255,255,255,.4); margin: 18px 0 10px;
}
.role-header b { color: #fff; }
.player-card {
    background: rgba(255,255,255,.05);
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 12px; padding: 12px 6px;
    text-align: center; cursor: pointer;
    transition: all .18s;
}
.player-card:hover {
    background: rgba(255,255,255,.12);
    transform: translateY(-2px);
}
.p-avatar {
    width: 44px; height: 44px; border-radius: 50%;
    margin: 0 auto 6px;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Bebas Neue', sans-serif; font-size: 14px;
}
.p-name { font-size: 10px; font-weight: 600; line-height: 1.3; color: #fff; }
.p-role { font-size: 8px; color: rgba(255,255,255,.38); margin-top: 2px; }
.captain-badge {
    font-size: 8px; padding: 1px 5px;
    border-radius: 8px; margin-left: 3px;
}
</style>
""", unsafe_allow_html=True)

code = st.session_state["selected_team"]
t    = TEAMS[code]
c    = t["color"]

# ── TOPBAR ────────────────────────────────────────────────────────────────────
col_back, col_badge, col_name, col_space = st.columns([1, 0.3, 3, 4])
with col_back:
    if st.button("← Teams", key="back_teams"):
        st.switch_page("pages/2_teams.py")
with col_badge:
    st.markdown(f"""
    <div style="width:36px;height:36px;border-radius:50%;
                background:{hex_to_rgba(c,.2)};border:2px solid {c};
                color:{c};display:flex;align-items:center;justify-content:center;
                font-family:'Bebas Neue',sans-serif;font-size:11px;margin-top:4px">
        {code}
    </div>""", unsafe_allow_html=True)
with col_name:
    st.markdown(f"""
    <div style="font-family:'Bebas Neue',sans-serif;font-size:22px;
                letter-spacing:2px;margin-top:6px">{t['name']}</div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

# ── SQUAD ─────────────────────────────────────────────────────────────────────
for role, players in t["players"].items():
    st.markdown(f'<div class="role-header"><b>{role}</b></div>', unsafe_allow_html=True)

    # Render in rows of 5
    for row_start in range(0, len(players), 5):
        chunk = players[row_start:row_start+5]
        cols  = st.columns(5)
        for col, name in zip(cols, chunk):
            is_captain = "(C)" in name
            clean_name = name.replace(" (C)", "").strip()
            ini        = initials(name)
            short_role = ROLE_SHORT.get(role, role[:3])

            with col:
                st.markdown(f"""
                <div class="player-card">
                  <div class="p-avatar"
                       style="background:{hex_to_rgba(c,.2)};
                              border:2px solid {hex_to_rgba(c,.45)};
                              color:{c}">
                    {ini}
                  </div>
                  <div class="p-name">
                    {clean_name}
                    {"<span class='captain-badge' style='background:" + hex_to_rgba(c,.25) + ";color:" + c + "'>C</span>" if is_captain else ""}
                  </div>
                  <div class="p-role">{short_role}</div>
                </div>
                """, unsafe_allow_html=True)

                if st.button(clean_name[:14], key=f"p_{code}_{name}", use_container_width=True):
                    st.session_state["selected_player"]      = name
                    st.session_state["selected_player_role"] = role
                    st.session_state["selected_player_team"] = code
                    st.switch_page("pages/4_orbit.py")
