"""
pages/5_stats.py — Full head-to-head stats: delivery type, shots, line map, wicket details.
"""
import streamlit as st
import streamlit.components.v1 as components
import os, sys

st.set_page_config(
    page_title="IPL Orbital — Head-to-Head Stats",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from data import (inject_css, TEAMS, hex_to_rgba, initials,
                  get_stats, sr_color, dominance_label, ROLE_SHORT)

inject_css()

if "stats" not in st.session_state:
    st.switch_page("pages/1_dataset.py")
if "selected_player" not in st.session_state:
    st.switch_page("pages/3_players.py")
if "orbit_player" not in st.session_state:
    st.switch_page("pages/4_orbit.py")

# ── Page CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.hero {
    display:flex; align-items:stretch; border-radius:18px; overflow:hidden;
    border:1px solid rgba(255,255,255,.08); margin-bottom:22px;
    background:rgba(255,255,255,.04);
}
.hero-side {
    flex:1; padding:22px 24px; display:flex; flex-direction:column;
    align-items:center; text-align:center;
}
.hero-av {
    width:78px; height:78px; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-family:'Bebas Neue',sans-serif; font-size:26px; margin-bottom:9px;
}
.hero-nm { font-family:'Bebas Neue',sans-serif; font-size:19px; letter-spacing:2px; }
.hero-role { font-size:10px; letter-spacing:1.5px; text-transform:uppercase; color:rgba(255,255,255,.4); margin-top:3px; }
.hero-badge {
    display:inline-block; margin-top:7px; padding:3px 13px;
    border-radius:20px; font-size:10px; font-weight:600; letter-spacing:1px;
}
.hero-vs {
    width:44px; flex-shrink:0; display:flex; align-items:center; justify-content:center;
    font-family:'Bebas Neue',sans-serif; font-size:22px; color:rgba(255,255,255,.15);
    border-left:1px solid rgba(255,255,255,.05); border-right:1px solid rgba(255,255,255,.05);
}
.stat-bar { display:flex; border-radius:14px; overflow:hidden; border:1px solid rgba(255,255,255,.08); margin-bottom:22px; }
.sb-item { flex:1; padding:13px 8px; text-align:center; background:rgba(255,255,255,.04); }
.sb-item+.sb-item { border-left:1px solid rgba(255,255,255,.08); }
.sb-val { font-family:'Bebas Neue',sans-serif; font-size:26px; line-height:1; }
.sb-lbl { font-size:9px; color:rgba(255,255,255,.35); letter-spacing:1px; text-transform:uppercase; margin-top:3px; }
.sec-title {
    font-family:'Bebas Neue',sans-serif; font-size:13px; letter-spacing:2px;
    color:rgba(255,255,255,.45); margin-bottom:10px; text-transform:uppercase;
    padding-bottom:6px; border-bottom:1px solid rgba(255,255,255,.07);
}
.dt-row { display:grid; grid-template-columns:160px 1fr 130px; align-items:center; gap:10px; margin-bottom:7px; }
.dt-label { font-size:12px; font-weight:500; }
.dt-bar-bg { height:7px; background:rgba(255,255,255,.07); border-radius:4px; overflow:hidden; }
.dt-bar { height:100%; border-radius:4px; }
.dt-stat { font-size:11px; color:rgba(255,255,255,.45); text-align:right; white-space:nowrap; }
.shot-wrap { display:flex; flex-wrap:wrap; gap:7px; margin-bottom:4px; }
.shot-pill {
    padding:5px 11px; border-radius:20px; font-size:11px;
    display:flex; align-items:center; gap:5px; border:1px solid;
}
.sp-runs { font-family:'Bebas Neue',sans-serif; font-size:15px; }
.sp-out {
    font-size:9px; padding:1px 5px; border-radius:10px;
    background:rgba(239,68,68,.3); color:#fca5a5;
}
.line-grid { display:flex; flex-wrap:wrap; gap:8px; }
.line-card {
    background:rgba(255,255,255,.05); border-radius:10px; padding:10px 12px;
    border:1px solid rgba(255,255,255,.08); min-width:110px;
}
.line-nm { font-size:9px; color:rgba(255,255,255,.45); text-transform:uppercase; letter-spacing:.8px; margin-bottom:3px; }
.line-runs { font-family:'Bebas Neue',sans-serif; font-size:22px; }
.line-detail { font-size:10px; color:rgba(255,255,255,.38); margin-top:2px; }
.wk-block {
    background:rgba(239,68,68,.07); border:1px solid rgba(239,68,68,.18);
    border-radius:12px; padding:13px 16px;
}
.wk-row { display:flex; align-items:center; gap:8px; margin-top:7px; flex-wrap:wrap; }
.wk-tag {
    padding:3px 9px; border-radius:20px; font-size:9px; font-weight:600;
    background:rgba(239,68,68,.2); color:#fca5a5; white-space:nowrap;
}
.dom-badge {
    display:inline-block; padding:6px 18px; border-radius:20px;
    font-size:12px; font-weight:600; letter-spacing:.5px;
    border:1px solid; margin-bottom:16px;
}
.no-data { text-align:center; padding:56px 20px; color:rgba(255,255,255,.3); }
</style>
""", unsafe_allow_html=True)

# ── Resolve batter / bowler ───────────────────────────────────────────────────
center_name = st.session_state["selected_player"]
center_role = st.session_state["selected_player_role"]
center_team = st.session_state["selected_player_team"]
orbit_name  = st.session_state["orbit_player"]
orbit_role  = st.session_state["orbit_player_role"]
orbit_team  = st.session_state["orbit_player_team"]

if center_role in ("Batters", "Wicket-Keepers"):
    batter_name, batter_team = center_name, center_team
    bowler_name, bowler_team = orbit_name,  orbit_team
elif center_role == "Bowlers":
    batter_name, batter_team = orbit_name,  orbit_team
    bowler_name, bowler_team = center_name, center_team
else:
    stats_check = st.session_state.get("stats", {})
    from data import normalize
    bat_side = stats_check.get("bat", {}).get(normalize(center_name), {}).get(normalize(orbit_name))
    if bat_side:
        batter_name, batter_team = center_name, center_team
        bowler_name, bowler_team = orbit_name,  orbit_team
    else:
        batter_name, batter_team = orbit_name,  orbit_team
        bowler_name, bowler_team = center_name, center_team

bt   = TEAMS[batter_team]
bwt  = TEAMS[bowler_team]
bN   = batter_name.replace(" (C)", "").strip()
bwN  = bowler_name.replace(" (C)", "").strip()
st_d = get_stats(center_name, center_role, orbit_name)

# ── TOPBAR ────────────────────────────────────────────────────────────────────
col_b1, col_b2, col_crumb = st.columns([1, 1, 5])
with col_b1:
    if st.button("← Orbit", key="back_orbit"):
        st.switch_page("pages/4_orbit.py")
with col_b2:
    if st.button("← Squad", key="back_squad_stats"):
        st.session_state.pop("orbit_team", None)
        st.session_state.pop("orbit_player", None)
        st.switch_page("pages/3_players.py")
with col_crumb:
    ot_c = TEAMS[orbit_team]["color"]
    st.markdown(f"""
    <div style='font-size:11px;margin-top:8px;color:rgba(255,255,255,.5)'>
      <span style='color:{bt["color"]}'>{bN}</span>
      <span style='color:rgba(255,255,255,.2)'> vs </span>
      <span style='color:{ot_c}'>{bwN}</span>
    </div>""", unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <div class="hero-side">
    <div class="hero-av"
         style="background:{hex_to_rgba(bt['color'],.22)};border:3px solid {bt['color']};color:{bt['color']}">
      {initials(batter_name)}
    </div>
    <div class="hero-nm">{bN}</div>
    <div class="hero-role">Batter</div>
    <div class="hero-badge"
         style="background:{hex_to_rgba(bt['color'],.18)};color:{bt['color']};border:1px solid {hex_to_rgba(bt['color'],.4)}">
      {batter_team}
    </div>
  </div>
  <div class="hero-vs">VS</div>
  <div class="hero-side">
    <div class="hero-av"
         style="background:{hex_to_rgba(bwt['color'],.22)};border:3px solid {bwt['color']};color:{bwt['color']}">
      {initials(bowler_name)}
    </div>
    <div class="hero-nm">{bwN}</div>
    <div class="hero-role">Bowler</div>
    <div class="hero-badge"
         style="background:{hex_to_rgba(bwt['color'],.18)};color:{bwt['color']};border:1px solid {hex_to_rgba(bwt['color'],.4)}">
      {bowler_team}
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── NO DATA ───────────────────────────────────────────────────────────────────
if not st_d:
    st.markdown("""
    <div class="no-data">
      <div style="font-size:44px;margin-bottom:10px">🏏</div>
      <div style="font-size:14px">No IPL 2025 data for this matchup.</div>
      <div style="font-size:11px;margin-top:6px;color:rgba(255,255,255,.25)">These two haven't faced each other in the loaded dataset.</div>
    </div>""", unsafe_allow_html=True)
    st.stop()

# ── DOMINANCE BADGE ───────────────────────────────────────────────────────────
dom_label, dom_bg = dominance_label(st_d["sr"], st_d["w"])
sc = sr_color(st_d["sr"], st_d["w"])
st.markdown(f"""
<div style="text-align:center;margin-bottom:16px">
  <span class="dom-badge" style="background:{dom_bg};color:{sc};border-color:{hex_to_rgba(sc,.35)}">
    {dom_label}
  </span>
</div>""", unsafe_allow_html=True)

# ── SUMMARY BAR ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="stat-bar">
  <div class="sb-item"><div class="sb-val" style="color:{bt['color']}">{st_d['r']}</div><div class="sb-lbl">Runs</div></div>
  <div class="sb-item"><div class="sb-val">{st_d['b']}</div><div class="sb-lbl">Balls</div></div>
  <div class="sb-item"><div class="sb-val" style="color:#ef4444">{st_d['w']}</div><div class="sb-lbl">Wickets</div></div>
  <div class="sb-item"><div class="sb-val" style="color:#60a5fa">{st_d['4s']}</div><div class="sb-lbl">Fours</div></div>
  <div class="sb-item"><div class="sb-val" style="color:#a78bfa">{st_d['6s']}</div><div class="sb-lbl">Sixes</div></div>
  <div class="sb-item"><div class="sb-val" style="color:{sc}">{st_d['sr']}</div><div class="sb-lbl">Strike Rate</div></div>
</div>
""", unsafe_allow_html=True)

# ── LENGTH × LINE COMBINED BREAKDOWN ─────────────────────────────────────────
st.markdown('<div class="sec-title">Length × Line — Where He Hit</div>', unsafe_allow_html=True)
ll_data   = st_d.get("length_line", {})
bowl_data = st_d.get("bowl", {})

if ll_data:
    # Gather all unique lengths and lines
    all_lengths = sorted(set(k.split("|||")[0] for k in ll_data))
    all_lines   = sorted(set(k.split("|||")[1] for k in ll_data))

    # Build grid HTML
    col_w   = 110
    row_h   = 68
    pad_l   = 148   # left label width
    pad_t   = 32    # top header height
    gw      = pad_l + col_w * len(all_lines) + 16
    gh      = pad_t + row_h * len(all_lengths) + 16

    # find max balls for intensity scaling
    max_b = max(v[1] for v in ll_data.values()) if ll_data else 1

    cells_html = ""

    # Column headers (lines)
    for ci, ln in enumerate(all_lines):
        x = pad_l + ci * col_w + col_w // 2
        cells_html += (
            f'<div style="position:absolute;left:{pad_l + ci*col_w}px;top:0;'
            f'width:{col_w}px;height:{pad_t}px;display:flex;align-items:center;'
            f'justify-content:center;font-size:9px;letter-spacing:.8px;'
            f'text-transform:uppercase;color:rgba(255,255,255,.35);">{ln}</div>'
        )

    for ri, dt in enumerate(all_lengths):
        # Row label
        cells_html += (
            f'<div style="position:absolute;left:0;top:{pad_t + ri*row_h}px;'
            f'width:{pad_l - 8}px;height:{row_h}px;display:flex;align-items:center;'
            f'font-size:11px;font-weight:500;color:rgba(255,255,255,.55);">{dt}</div>'
        )
        for ci, ln in enumerate(all_lines):
            key = f"{dt}|||{ln}"
            v   = ll_data.get(key)
            if v:
                runs, balls, wkts = v[0], v[1], v[2]
                shots_dict = v[3] if len(v) > 3 else {}
                top_shot = max(shots_dict, key=shots_dict.get) if shots_dict else ""
                sr_val = runs / balls * 100 if balls else 0
                col    = sr_color(sr_val, wkts)
                intens = balls / max_b        # 0→1 for bg opacity
                bg     = hex_to_rgba(col, round(0.08 + intens * 0.28, 2))
                bdr    = hex_to_rgba(col, round(0.25 + intens * 0.35, 2))
                out_dot = '<span style="position:absolute;top:4px;right:5px;width:6px;height:6px;border-radius:50%;background:#ef4444;"></span>' if wkts else ""
                shot_html = (f'<span style="font-size:8px;color:rgba(255,255,255,.5);'
                             f'margin-top:2px;text-transform:uppercase;letter-spacing:.4px;'
                             f'white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'
                             f'max-width:{col_w-14}px;display:block;text-align:center;">'
                             f'🏏 {top_shot}</span>') if top_shot else ""
                cells_html += (
                    f'<div style="position:absolute;left:{pad_l + ci*col_w + 4}px;'
                    f'top:{pad_t + ri*row_h + 4}px;'
                    f'width:{col_w - 8}px;height:{row_h - 8}px;'
                    f'background:{bg};border:1px solid {bdr};border-radius:8px;'
                    f'display:flex;flex-direction:column;align-items:center;'
                    f'justify-content:center;position:absolute;">'
                    f'{out_dot}'
                    f'<span style="font-family:Bebas Neue,sans-serif;font-size:18px;'
                    f'color:{col};line-height:1;">{runs}</span>'
                    f'<span style="font-size:9px;color:rgba(255,255,255,.38);margin-top:1px;">'
                    f'{balls}b · SR {round(sr_val)}</span>'
                    f'{shot_html}'
                    f'</div>'
                )
            else:
                # Empty cell
                cells_html += (
                    f'<div style="position:absolute;left:{pad_l + ci*col_w + 4}px;'
                    f'top:{pad_t + ri*row_h + 4}px;'
                    f'width:{col_w - 8}px;height:{row_h - 8}px;'
                    f'background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.05);'
                    f'border-radius:8px;">'
                    f'</div>'
                )

    components.html(
        f"""<!DOCTYPE html><html><head>
        <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap" rel="stylesheet">
        <style>* {{ box-sizing:border-box; margin:0; padding:0; }}</style>
        </head>
        <body style="background:transparent;overflow:hidden;">
        <div style="position:relative;width:{gw}px;height:{gh}px;">
          {cells_html}
        </div>
        </body></html>""",
        height=gh + 8,
        scrolling=False,
    )
else:
    # fallback: show old bar breakdown if no combined data
    if bowl_data:
        max_balls = max(v[1] for v in bowl_data.values()) if bowl_data else 1
        for dt, v in sorted(bowl_data.items(), key=lambda x: -x[1][1]):
            runs, balls, wkts, fours, sixes = v
            pct  = round(balls / max_balls * 100)
            col  = sr_color(runs/balls*100 if balls else 0, wkts)
            stat_txt = f"{runs}r / {balls}b"
            st.markdown(f"""
            <div class="dt-row">
              <div class="dt-label" style="color:{col}">{dt}</div>
              <div class="dt-bar-bg"><div class="dt-bar" style="width:{pct}%;background:{col}"></div></div>
              <div class="dt-stat">{stat_txt}</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div style="color:rgba(255,255,255,.3);font-size:12px">No delivery data</div>', unsafe_allow_html=True)

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

# ── SHOTS PLAYED ──────────────────────────────────────────────────────────────
st.markdown('<div class="sec-title">Shots Played</div>', unsafe_allow_html=True)
shot_data = st_d.get("shot", {})
if shot_data:
    pills_html = ""
    for shot, v in sorted(shot_data.items(), key=lambda x: -x[1][0]):
        runs, balls, wkts = v
        col  = sr_color(runs/balls*100 if balls else 0, wkts)
        out_tag = '<span style="font-size:9px;padding:1px 5px;border-radius:10px;background:rgba(239,68,68,.3);color:#fca5a5;">OUT</span>' if wkts else ""
        pills_html += (
            f'<div style="padding:5px 11px;border-radius:20px;font-size:11px;'
            f'display:flex;align-items:center;gap:5px;border:1px solid;'
            f'background:{hex_to_rgba(col,.1)};border-color:{hex_to_rgba(col,.3)};">'
            f'<span style="font-family:\'Bebas Neue\',sans-serif;font-size:15px;color:{col};">{runs}</span>'
            f'<span style="color:rgba(255,255,255,.65);">{shot}</span>'
            f'<span style="font-size:10px;color:rgba(255,255,255,.35);">({balls}b)</span>'
            f'{out_tag}'
            f'</div>'
        )
    full_html = (
        f'<div style="display:flex;flex-wrap:wrap;gap:7px;margin-bottom:4px;">'
        f'{pills_html}'
        f'</div>'
    )
    components.html(
        f"""<!DOCTYPE html><html><head>
        <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap" rel="stylesheet">
        <style>* {{ box-sizing: border-box; margin: 0; padding: 0; }}</style>
        </head><body style="background:transparent;padding:2px 0;">
        {full_html}
        </body></html>""",
        height=max(60, (len(shot_data) // 3 + 1) * 48),
        scrolling=False,
    )
else:
    st.markdown('<div style="color:rgba(255,255,255,.3);font-size:12px">No shot data</div>', unsafe_allow_html=True)

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

# ── WICKET DETAILS ────────────────────────────────────────────────────────────
out_list = st_d.get("out", [])
if out_list:
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Wicket Details</div>', unsafe_allow_html=True)
    rows_html = ""
    for w in out_list:
        rows_html += f"""
        <div class="wk-row">
          <span class="wk-tag">OUT</span>
          <span style="font-size:12px">{w.get('bt','—')} delivery</span>
          <span style="font-size:11px;color:rgba(255,255,255,.45)">on {w.get('ln','—')} line</span>
          {"<span style='font-size:11px;color:rgba(255,255,255,.45)'>playing " + w['st'] + "</span>" if w.get('st') else ""}
        </div>"""
    st.markdown(f'<div class="wk-block"><div style="font-size:11px;color:rgba(255,255,255,.4);margin-bottom:4px">How the batter was dismissed:</div>{rows_html}</div>', unsafe_allow_html=True)