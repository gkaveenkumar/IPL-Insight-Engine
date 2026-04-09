"""
pages/6_phase.py — Phase Analysis
  · Pick team → pick player (batters incl. WK & AR; bowlers incl. AR)
  · Full per-phase breakdown: Powerplay / Middle / Death
  · Batter: avg, SR, runs, balls-per-boundary, boundary%, dot%, shots, deliveries faced
  · Bowler: avg, economy, SR, wickets, dot%, boundary%, delivery variations, lines
  · Team Compare: side-by-side phase SR or economy between two teams
"""
import streamlit as st
import streamlit.components.v1 as components
import os, sys

st.set_page_config(
    page_title="IPL Orbital — Phase Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from data import inject_css, TEAMS, hex_to_rgba, initials, sr_color, normalize, ROLE_SHORT

inject_css()

if "stats" not in st.session_state:
    st.switch_page("pages/1_dataset.py")
if "phase_stats" not in st.session_state:
    st.warning("Phase stats not loaded. Please reload the dataset.")
    if st.button("Reload Dataset"):
        st.switch_page("pages/1_dataset.py")
    st.stop()

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.ph-title{font-family:'Bebas Neue',sans-serif;font-size:36px;letter-spacing:5px;text-align:center;margin:20px 0 2px}
.ph-sub{font-size:10px;color:rgba(255,255,255,.3);letter-spacing:2px;text-transform:uppercase;text-align:center;margin-bottom:20px}
.pc{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);border-radius:18px;padding:18px 20px;margin-bottom:18px}
.pc-head{font-family:'Bebas Neue',sans-serif;font-size:19px;letter-spacing:3px;margin-bottom:12px;display:flex;align-items:center;gap:10px}
.pc-overs{font-size:10px;color:rgba(255,255,255,.35);font-family:'DM Sans',sans-serif;font-weight:400}
.kpi-grid{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}
.kpi{flex:1;min-width:72px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08);border-radius:11px;padding:9px 6px;text-align:center}
.kv{font-family:'Bebas Neue',sans-serif;font-size:24px;line-height:1}
.kl{font-size:8px;color:rgba(255,255,255,.32);letter-spacing:.9px;text-transform:uppercase;margin-top:3px}
.st2{font-size:9px;letter-spacing:1.5px;text-transform:uppercase;color:rgba(255,255,255,.32);margin-bottom:8px;border-bottom:1px solid rgba(255,255,255,.06);padding-bottom:4px}
.phero{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);border-radius:16px;padding:16px 20px;display:flex;align-items:center;gap:16px;margin-bottom:20px}
.phero-av{width:60px;height:60px;border-radius:50%;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-family:'Bebas Neue',sans-serif;font-size:20px}
.phero-name{font-family:'Bebas Neue',sans-serif;font-size:22px;letter-spacing:2px}
.phero-role{font-size:10px;color:rgba(255,255,255,.4);letter-spacing:1px;text-transform:uppercase;margin-top:2px}
.phero-badge{display:inline-block;margin-top:6px;padding:2px 11px;border-radius:20px;font-size:10px;font-weight:600}
.ov-strip{display:flex;gap:0;border-radius:14px;overflow:hidden;border:1px solid rgba(255,255,255,.08);margin-bottom:20px}
.ov-item{flex:1;padding:11px 6px;text-align:center;background:rgba(255,255,255,.03);border-right:1px solid rgba(255,255,255,.07)}
.ov-item:last-child{border-right:none}
.ov-v{font-family:'Bebas Neue',sans-serif;font-size:22px;line-height:1}
.ov-l{font-size:8px;color:rgba(255,255,255,.32);letter-spacing:.8px;text-transform:uppercase;margin-top:2px}
.empty-ph{background:rgba(255,255,255,.02);border:1px dashed rgba(255,255,255,.07);border-radius:10px;padding:14px;text-align:center;color:rgba(255,255,255,.2);font-size:11px}
.wkt-tag{font-size:9px;padding:1px 5px;border-radius:8px;background:rgba(34,197,94,.25);color:#86efac}
.out-tag{font-size:9px;padding:1px 5px;border-radius:8px;background:rgba(239,68,68,.3);color:#fca5a5}
</style>
""", unsafe_allow_html=True)

# ── CONSTANTS ─────────────────────────────────────────────────────────────────
PHASES = [
    ("powerplay", "⚡ POWERPLAY",  "Overs 1–6",   "#F59E0B"),
    ("middle",    "🔄 MIDDLE",     "Overs 7–14",  "#60A5FA"),
    ("death",     "💀 DEATH",      "Overs 15–20", "#F87171"),
]
BAT_ROLES = ["Batters", "Wicket-Keepers", "All-Rounders"]
BOW_ROLES = ["Bowlers", "All-Rounders"]
TEAM_CODES = list(TEAMS.keys())

def econ_color(e):
    if e <= 6:  return "#22c55e"
    if e <= 8:  return "#84cc16"
    if e <= 10: return "#eab308"
    if e <= 12: return "#f97316"
    return "#ef4444"

def get_team_players(team_code, include_roles):
    team = TEAMS[team_code]
    result = []
    for role in include_roles:
        for p in team["players"].get(role, []):
            clean = p.replace(" (C)", "").strip()
            result.append((clean, role))
    return result

def wrap_html(body):
    return (f'<!DOCTYPE html><html><head>'
            f'<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap" rel="stylesheet">'
            f'<style>*{{box-sizing:border-box;margin:0;padding:0}}</style>'
            f'</head><body style="background:transparent;padding:2px 0">{body}</body></html>')

def bar_chart_html(rows):
    """rows = list of (label, bar_val, max_val, display_str, color, tag_html)"""
    html = ""
    for label, bv, mv, disp, col, tag in rows:
        pct = round(bv / mv * 100) if mv else 0
        html += f"""
        <div style="margin-bottom:7px">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px">
            <span style="font-size:11px;font-weight:500;color:{col}">{label}</span>
            <span style="display:flex;align-items:center;gap:5px;font-size:10px;color:rgba(255,255,255,.38)">{tag}{disp}</span>
          </div>
          <div style="height:5px;background:rgba(255,255,255,.07);border-radius:3px;overflow:hidden">
            <div style="width:{pct}%;height:100%;background:{col};border-radius:3px"></div>
          </div>
        </div>"""
    return html

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown('<div class="ph-title">PHASE ANALYSIS</div>', unsafe_allow_html=True)
st.markdown('<div class="ph-sub">Powerplay · Middle Overs · Death Overs</div>', unsafe_allow_html=True)

cb1, cb2, cb3, _ = st.columns([1, 1, 1, 4])
with cb1:
    if st.button("← Teams"):   st.switch_page("pages/2_teams.py")
with cb2:
    if st.button("← Players"): st.switch_page("pages/3_players.py")
with cb3:
    if st.button("← Orbit"):   st.switch_page("pages/4_orbit.py")

st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

# ── MODE TOGGLE ───────────────────────────────────────────────────────────────
if "ph_mode" not in st.session_state:
    st.session_state["ph_mode"] = "batter"

mc1, mc2, mc3, _ = st.columns([1.1, 1.1, 1.4, 4])
with mc1:
    if st.button("🏏 Batter", use_container_width=True,
                 type="primary" if st.session_state["ph_mode"] == "batter" else "secondary"):
        st.session_state["ph_mode"] = "batter"; st.rerun()
with mc2:
    if st.button("🎯 Bowler", use_container_width=True,
                 type="primary" if st.session_state["ph_mode"] == "bowler" else "secondary"):
        st.session_state["ph_mode"] = "bowler"; st.rerun()
with mc3:
    if st.button("⚔️ Team Compare", use_container_width=True,
                 type="primary" if st.session_state["ph_mode"] == "compare" else "secondary"):
        st.session_state["ph_mode"] = "compare"; st.rerun()

mode = st.session_state["ph_mode"]
phase_stats = st.session_state["phase_stats"]
st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# BATTER MODE
# ════════════════════════════════════════════════════════════════════════════
if mode == "batter":
    default_team = st.session_state.get("selected_player_team",
                   st.session_state.get("selected_team", TEAM_CODES[0]))
    if default_team not in TEAM_CODES: default_team = TEAM_CODES[0]

    col_tc, col_pc, _ = st.columns([1.5, 2, 4])
    with col_tc:
        team_code = st.selectbox("Team", TEAM_CODES,
            index=TEAM_CODES.index(default_team),
            format_func=lambda c: TEAMS[c]["name"], key="ph_bat_team")
    team_color = TEAMS[team_code]["color"]

    team_players = get_team_players(team_code, BAT_ROLES)
    player_names = [p[0] for p in team_players]
    player_roles = {p[0]: p[1] for p in team_players}

    default_player = player_names[0] if player_names else ""
    if "selected_player" in st.session_state:
        sp = st.session_state["selected_player"].replace(" (C)", "").strip()
        if sp in player_names: default_player = sp

    with col_pc:
        chosen = st.selectbox("Player", player_names,
            index=player_names.index(default_player) if default_player in player_names else 0,
            format_func=lambda n: f"{n}  [{ROLE_SHORT.get(player_roles.get(n,''),'?')}]",
            key="ph_bat_player")

    ds_name = normalize(chosen)
    p_data  = phase_stats.get("batsman", {}).get(ds_name, {})
    role_label = player_roles.get(chosen, "")
    ini = "".join(w[0] for w in chosen.split()).upper()[:2]

    st.markdown(f"""
    <div class="phero" style="border-color:{hex_to_rgba(team_color,.25)}">
      <div class="phero-av" style="background:{hex_to_rgba(team_color,.2)};
           border:3px solid {team_color};color:{team_color}">{ini}</div>
      <div>
        <div class="phero-name">{chosen}</div>
        <div class="phero-role">{role_label}</div>
        <div class="phero-badge" style="background:{hex_to_rgba(team_color,.18)};
             color:{team_color};border:1px solid {hex_to_rgba(team_color,.4)}">{team_code}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if not p_data:
        st.markdown(f'<div class="empty-ph">No IPL 2025 batting data found for <b>{chosen}</b></div>',
                    unsafe_allow_html=True)
        st.stop()

    # ── Overall strip ────────────────────────────────────────────────────────
    total_runs  = sum(d.get("runs",    0) for d in p_data.values())
    total_balls = sum(d.get("balls",   0) for d in p_data.values())
    total_wkts  = sum(d.get("wickets", 0) for d in p_data.values())
    total_4s    = sum(d.get("fours",   0) for d in p_data.values())
    total_6s    = sum(d.get("sixes",   0) for d in p_data.values())
    ov_sr  = round(total_runs / total_balls * 100, 1) if total_balls else 0
    ov_avg = round(total_runs / total_wkts, 2)        if total_wkts  else total_runs
    sc     = sr_color(ov_sr, 0)
    # 50s / 100s: approximate from per-phase runs
    innings_runs = [d.get("runs", 0) for d in p_data.values() if d.get("balls", 0) > 0]
    fifties  = sum(1 for r in innings_runs if 50 <= r < 100)
    hundreds = sum(1 for r in innings_runs if r >= 100)

    st.markdown(f"""
    <div class="ov-strip">
      <div class="ov-item"><div class="ov-v" style="color:{team_color}">{total_runs}</div><div class="ov-l">Total Runs</div></div>
      <div class="ov-item"><div class="ov-v">{total_balls}</div><div class="ov-l">Balls</div></div>
      <div class="ov-item"><div class="ov-v" style="color:{sc}">{ov_sr}</div><div class="ov-l">Strike Rate</div></div>
      <div class="ov-item"><div class="ov-v" style="color:#84cc16">{ov_avg}</div><div class="ov-l">Batting Avg</div></div>
      <div class="ov-item"><div class="ov-v" style="color:#60a5fa">{total_4s}</div><div class="ov-l">Fours</div></div>
      <div class="ov-item"><div class="ov-v" style="color:#a78bfa">{total_6s}</div><div class="ov-l">Sixes</div></div>
      <div class="ov-item"><div class="ov-v" style="color:#fbbf24">{fifties}</div><div class="ov-l">50s</div></div>
      <div class="ov-item"><div class="ov-v" style="color:#f59e0b">{hundreds}</div><div class="ov-l">100s</div></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Phase cards ───────────────────────────────────────────────────────────
    for ph_key, ph_label, ph_overs, ph_color in PHASES:
        d = p_data.get(ph_key)
        st.markdown(f'<div class="pc" style="border-color:{hex_to_rgba(ph_color,.22)}">'
                    f'<div class="pc-head" style="color:{ph_color}">{ph_label}'
                    f'<span class="pc-overs">{ph_overs}</span></div>',
                    unsafe_allow_html=True)

        if not d or d.get("balls", 0) == 0:
            st.markdown('<div class="empty-ph">No data for this phase</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            continue

        runs  = d["runs"];  balls = d["balls"];  wkts = d["wickets"]
        f4    = d["fours"]; f6   = d["sixes"];   dot_p = d["dot_pct"]
        sr_v  = d["sr"]
        avg_v = round(runs / wkts, 2)             if wkts  else runs
        bdry  = f4 + f6
        bpb   = round(balls / bdry, 1)            if bdry  else "—"
        bdry_pct = round(bdry / balls * 100, 1)   if balls else 0
        sc    = sr_color(sr_v, 0)

        st.markdown(f"""
        <div class="kpi-grid">
          <div class="kpi"><div class="kv" style="color:{ph_color}">{runs}</div><div class="kl">Runs</div></div>
          <div class="kpi"><div class="kv">{balls}</div><div class="kl">Balls</div></div>
          <div class="kpi"><div class="kv" style="color:{sc}">{sr_v}</div><div class="kl">Strike Rate</div></div>
          <div class="kpi"><div class="kv" style="color:#84cc16">{avg_v}</div><div class="kl">Avg</div></div>
          <div class="kpi"><div class="kv" style="color:#60a5fa">{f4}</div><div class="kl">Fours</div></div>
          <div class="kpi"><div class="kv" style="color:#a78bfa">{f6}</div><div class="kl">Sixes</div></div>
          <div class="kpi"><div class="kv" style="color:#f59e0b">{bdry_pct}%</div><div class="kl">Boundary %</div></div>
          <div class="kpi"><div class="kv" style="color:rgba(255,255,255,.5)">{bpb}</div><div class="kl">Balls/Bdry</div></div>
          <div class="kpi"><div class="kv" style="color:rgba(255,255,255,.38)">{dot_p}%</div><div class="kl">Dot %</div></div>
          <div class="kpi"><div class="kv" style="color:#ef4444">{wkts}</div><div class="kl">Times Out</div></div>
        </div>
        """, unsafe_allow_html=True)

        col_sh, col_dl = st.columns(2)

        with col_sh:
            st.markdown('<div class="st2">🏏 Shots Played</div>', unsafe_allow_html=True)
            shots = d.get("top_shots", [])
            if shots:
                max_sr = max((s[1]/s[2]*100 if s[2] else 0) for s in shots) or 1
                rows = []
                for s in shots[:9]:
                    shot_sr = round(s[1]/s[2]*100) if s[2] else 0
                    tag = '<span class="out-tag">OUT</span>' if s[3] > 0 else ""
                    rows.append((s[0], shot_sr, max_sr,
                                 f"{s[1]}r / {s[2]}b · SR {shot_sr}",
                                 sr_color(shot_sr, s[3]), tag))
                html = bar_chart_html(rows)
                components.html(wrap_html(html), height=len(rows)*40+10, scrolling=False)
            else:
                st.markdown('<div style="color:rgba(255,255,255,.28);font-size:11px">No shot data</div>', unsafe_allow_html=True)

        with col_dl:
            st.markdown('<div class="st2">🎳 Delivery Types Faced</div>', unsafe_allow_html=True)
            deliveries = d.get("bowl_faced", [])
            if deliveries:
                max_b = max(x[2] for x in deliveries) or 1
                rows = []
                for x in deliveries:
                    d_sr = round(x[1]/x[2]*100) if x[2] else 0
                    tag  = '<span class="out-tag">OUT</span>' if x[3] > 0 else ""
                    rows.append((x[0], x[2], max_b,
                                 f"{x[1]}r / {x[2]}b · SR {d_sr}",
                                 sr_color(d_sr, x[3]), tag))
                html = bar_chart_html(rows)
                components.html(wrap_html(html), height=len(rows)*40+10, scrolling=False)
            else:
                st.markdown('<div style="color:rgba(255,255,255,.28);font-size:11px">No delivery data</div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# BOWLER MODE
# ════════════════════════════════════════════════════════════════════════════
elif mode == "bowler":
    default_team = st.session_state.get("selected_player_team",
                   st.session_state.get("selected_team", TEAM_CODES[0]))
    if default_team not in TEAM_CODES: default_team = TEAM_CODES[0]

    col_tc, col_pc, _ = st.columns([1.5, 2, 4])
    with col_tc:
        team_code = st.selectbox("Team", TEAM_CODES,
            index=TEAM_CODES.index(default_team),
            format_func=lambda c: TEAMS[c]["name"], key="ph_bow_team")
    team_color = TEAMS[team_code]["color"]

    team_players = get_team_players(team_code, BOW_ROLES)
    player_names = [p[0] for p in team_players]
    player_roles = {p[0]: p[1] for p in team_players}

    default_player = player_names[0] if player_names else ""
    if "selected_player" in st.session_state:
        sp = st.session_state["selected_player"].replace(" (C)", "").strip()
        if sp in player_names: default_player = sp

    with col_pc:
        chosen = st.selectbox("Player", player_names,
            index=player_names.index(default_player) if default_player in player_names else 0,
            format_func=lambda n: f"{n}  [{ROLE_SHORT.get(player_roles.get(n,''),'?')}]",
            key="ph_bow_player")

    ds_name = normalize(chosen)
    p_data  = phase_stats.get("bowler", {}).get(ds_name, {})
    role_label = player_roles.get(chosen, "")
    ini = "".join(w[0] for w in chosen.split()).upper()[:2]

    st.markdown(f"""
    <div class="phero" style="border-color:{hex_to_rgba(team_color,.25)}">
      <div class="phero-av" style="background:{hex_to_rgba(team_color,.2)};
           border:3px solid {team_color};color:{team_color}">{ini}</div>
      <div>
        <div class="phero-name">{chosen}</div>
        <div class="phero-role">{role_label}</div>
        <div class="phero-badge" style="background:{hex_to_rgba(team_color,.18)};
             color:{team_color};border:1px solid {hex_to_rgba(team_color,.4)}">{team_code}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if not p_data:
        st.markdown(f'<div class="empty-ph">No IPL 2025 bowling data found for <b>{chosen}</b></div>',
                    unsafe_allow_html=True)
        st.stop()

    # ── Overall strip ────────────────────────────────────────────────────────
    tot_r   = sum(d.get("runs_given", 0) for d in p_data.values())
    tot_b   = sum(d.get("balls",      0) for d in p_data.values())
    tot_w   = sum(d.get("wickets",    0) for d in p_data.values())
    ov_econ = round(tot_r / tot_b * 6, 2)  if tot_b else 0
    ov_avg  = round(tot_r / tot_w, 2)      if tot_w else "—"
    ov_sr   = round(tot_b / tot_w, 1)      if tot_w else "—"
    dot_sum = sum(d.get("dot_pct", 0) * d.get("balls", 0) / 100 for d in p_data.values())
    ov_dot  = round(dot_sum / tot_b * 100, 1) if tot_b else 0
    ec_c    = econ_color(ov_econ)

    st.markdown(f"""
    <div class="ov-strip">
      <div class="ov-item"><div class="ov-v" style="color:#ef4444">{tot_r}</div><div class="ov-l">Runs Given</div></div>
      <div class="ov-item"><div class="ov-v">{tot_b}</div><div class="ov-l">Balls</div></div>
      <div class="ov-item"><div class="ov-v" style="color:{ec_c}">{ov_econ}</div><div class="ov-l">Economy</div></div>
      <div class="ov-item"><div class="ov-v" style="color:#22c55e">{tot_w}</div><div class="ov-l">Wickets</div></div>
      <div class="ov-item"><div class="ov-v" style="color:#84cc16">{ov_avg}</div><div class="ov-l">Bowl Avg</div></div>
      <div class="ov-item"><div class="ov-v" style="color:#60a5fa">{ov_sr}</div><div class="ov-l">Bowl SR (b/w)</div></div>
      <div class="ov-item"><div class="ov-v" style="color:rgba(255,255,255,.45)">{ov_dot}%</div><div class="ov-l">Dot %</div></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Phase cards ───────────────────────────────────────────────────────────
    for ph_key, ph_label, ph_overs, ph_color in PHASES:
        d = p_data.get(ph_key)
        st.markdown(f'<div class="pc" style="border-color:{hex_to_rgba(ph_color,.22)}">'
                    f'<div class="pc-head" style="color:{ph_color}">{ph_label}'
                    f'<span class="pc-overs">{ph_overs}</span></div>',
                    unsafe_allow_html=True)

        if not d or d.get("balls", 0) == 0:
            st.markdown('<div class="empty-ph">No data for this phase</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            continue

        runs  = d["runs_given"]; balls = d["balls"]; wkts = d["wickets"]
        econ  = d["economy"];    dot_p = d["dot_pct"]
        bpw   = round(balls / wkts, 1) if wkts else "—"
        avg_v = round(runs / wkts, 2)  if wkts else "—"
        ec_c  = econ_color(econ)
        top_deliveries = d.get("top_deliveries", [])
        top_lines      = d.get("top_lines", [])

        # boundary % from lines data (4s+6s / total balls)
        # approximate: runs given / balls * some factor — use delivery data
        total_bdry_b = sum(x[2] for x in top_deliveries)  # x[2] = balls, correct
        bdry_pct_approx = "—"  # phase_stats doesn't store 4s/6s for bowlers yet; show dot% instead

        st.markdown(f"""
        <div class="kpi-grid">
          <div class="kpi"><div class="kv" style="color:#ef4444">{runs}</div><div class="kl">Runs Given</div></div>
          <div class="kpi"><div class="kv">{balls}</div><div class="kl">Balls</div></div>
          <div class="kpi"><div class="kv" style="color:{ec_c}">{econ}</div><div class="kl">Economy</div></div>
          <div class="kpi"><div class="kv" style="color:#22c55e">{wkts}</div><div class="kl">Wickets</div></div>
          <div class="kpi"><div class="kv" style="color:#84cc16">{avg_v}</div><div class="kl">Bowl Avg</div></div>
          <div class="kpi"><div class="kv" style="color:#60a5fa">{bpw}</div><div class="kl">Balls/Wkt (SR)</div></div>
          <div class="kpi"><div class="kv" style="color:rgba(255,255,255,.45)">{dot_p}%</div><div class="kl">Dot %</div></div>
        </div>
        """, unsafe_allow_html=True)

        col_dv, col_ln = st.columns(2)

        with col_dv:
            st.markdown('<div class="st2">🎳 Delivery Variations</div>', unsafe_allow_html=True)
            if top_deliveries:
                max_b = max(int(x[2]) for x in top_deliveries) or 1  # x[2]=balls
                rows = []
                for x in top_deliveries:
                    # tuple: (name, runs, balls, wickets)
                    _name, _runs, _balls_d, _wkts = x[0], int(x[1]), int(x[2]), int(x[3])
                    d_econ = round(_runs / _balls_d * 6, 1) if _balls_d else 0
                    usage  = round(_balls_d / balls * 100) if balls else 0
                    tag    = f'<span class="wkt-tag">{_wkts}W</span>' if _wkts else ""
                    rows.append((_runs, _balls_d, max_b,
                                 f"{_name} · {_balls_d}b ({usage}%) · Econ {d_econ}",
                                 econ_color(d_econ), tag))
                html = bar_chart_html(rows)
                components.html(wrap_html(html), height=len(rows)*42+10, scrolling=False)
            else:
                st.markdown('<div style="color:rgba(255,255,255,.28);font-size:11px">No data</div>', unsafe_allow_html=True)

        with col_ln:
            st.markdown('<div class="st2">📍 Delivery Types</div>', unsafe_allow_html=True)
            if top_lines:
                max_b = max(int(x[2]) for x in top_lines) or 1
                rows = []
                for x in top_lines:
                    # tuple: (name, runs, balls, wickets)
                    _name, _runs, _balls_l, _wkts = x[0], int(x[1]), int(x[2]), int(x[3])
                    b_sr = round(_runs / _balls_l * 100) if _balls_l else 0
                    tag  = f'<span class="wkt-tag">{_wkts}W</span>' if _wkts else ""
                    # colour: green if good batter SR, red if high
                    col  = sr_color(b_sr, _wkts)
                    rows.append((_runs, _balls_l, max_b,
                                 f"{_name} · {_balls_l}b · Batter SR {b_sr}",
                                 col, tag))
                html = bar_chart_html(rows)
                components.html(wrap_html(html), height=len(rows)*42+10, scrolling=False)
            else:
                st.markdown('<div style="color:rgba(255,255,255,.28);font-size:11px">No data</div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# TEAM COMPARE MODE
# ════════════════════════════════════════════════════════════════════════════
elif mode == "compare":
    st.markdown("""
    <div style="text-align:center;font-size:11px;color:rgba(255,255,255,.35);
    letter-spacing:1.5px;text-transform:uppercase;margin-bottom:16px">
    Compare phase averages between two squads
    </div>""", unsafe_allow_html=True)

    cc1, cc2, cc3, _ = st.columns([1.5, 1.5, 1.6, 2])
    with cc1:
        team_a = st.selectbox("Team A", TEAM_CODES, index=0,
            format_func=lambda c: TEAMS[c]["name"], key="cmp_a")
    with cc2:
        team_b = st.selectbox("Team B", TEAM_CODES, index=min(1, len(TEAM_CODES)-1),
            format_func=lambda c: TEAMS[c]["name"], key="cmp_b")
    with cc3:
        cmp_type = st.selectbox("Metric", ["Batting Strike Rate", "Bowling Economy",
                                            "Batting Average", "Bowling Average"], key="cmp_metric")

    ca = TEAMS[team_a]["color"]
    cb_col = TEAMS[team_b]["color"]

    stat_map = {
        "Batting Strike Rate": ("bat", "sr",        "SR"),
        "Bowling Economy":     ("bow", "economy",   "Econ"),
        "Batting Average":     ("bat", "avg",        "Avg"),
        "Bowling Average":     ("bow", "bowl_avg",   "Avg"),
    }
    stat_type, val_key, unit = stat_map[cmp_type]
    ds_key   = "batsman" if stat_type == "bat" else "bowler"
    roles    = BAT_ROLES if stat_type == "bat" else BOW_ROLES

    def team_phase_val(team_code):
        players = get_team_players(team_code, roles)
        result = {}
        for ph_key, _, _, _ in PHASES:
            vals = []
            for name, _ in players:
                ds  = normalize(name)
                d   = phase_stats.get(ds_key, {}).get(ds, {}).get(ph_key)
                if d and d.get("balls", 0) >= 6:
                    if val_key == "sr":
                        vals.append(d["sr"])
                    elif val_key == "economy":
                        vals.append(d["economy"])
                    elif val_key == "avg":
                        r, w = d.get("runs", 0), d.get("wickets", 0)
                        if w: vals.append(r / w)
                    elif val_key == "bowl_avg":
                        r, w = d.get("runs_given", 0), d.get("wickets", 0)
                        if w: vals.append(r / w)
            result[ph_key] = round(sum(vals)/len(vals), 1) if vals else 0
        return result

    a_stats = team_phase_val(team_a)
    b_stats = team_phase_val(team_b)

    # Higher = better for batting; lower = better for bowling
    bat_metric = stat_type == "bat"

    for ph_key, ph_label, ph_overs, ph_color in PHASES:
        va = a_stats.get(ph_key, 0)
        vb = b_stats.get(ph_key, 0)
        max_v = max(va, vb, 1)
        if bat_metric:
            winner = team_a if va > vb else team_b
            insight = f"🏏 {TEAMS[winner]['name']} scores faster in this phase"
        else:
            winner = team_a if va < vb else team_b
            insight = f"🎯 {TEAMS[winner]['name']} is more economical in this phase"
        wc = TEAMS[winner]["color"]

        st.markdown(f"""
        <div class="pc" style="border-color:{hex_to_rgba(ph_color,.22)}">
          <div class="pc-head" style="color:{ph_color}">{ph_label}<span class="pc-overs">{ph_overs}</span></div>
          <div style="margin-bottom:8px">
            <div style="display:flex;justify-content:space-between;margin-bottom:4px">
              <span style="font-size:12px;font-weight:600;color:{ca}">{TEAMS[team_a]['name']}</span>
              <span style="font-family:'Bebas Neue';font-size:18px;color:{ca}">{va} {unit}</span>
            </div>
            <div style="height:8px;background:rgba(255,255,255,.07);border-radius:4px;overflow:hidden;margin-bottom:10px">
              <div style="width:{round(va/max_v*100)}%;height:100%;background:{ca};border-radius:4px"></div>
            </div>
            <div style="display:flex;justify-content:space-between;margin-bottom:4px">
              <span style="font-size:12px;font-weight:600;color:{cb_col}">{TEAMS[team_b]['name']}</span>
              <span style="font-family:'Bebas Neue';font-size:18px;color:{cb_col}">{vb} {unit}</span>
            </div>
            <div style="height:8px;background:rgba(255,255,255,.07);border-radius:4px;overflow:hidden">
              <div style="width:{round(vb/max_v*100)}%;height:100%;background:{cb_col};border-radius:4px"></div>
            </div>
          </div>
          <div style="font-size:10px;color:{wc};text-align:center;padding:6px;background:{hex_to_rgba(wc,.08)};border-radius:8px">{insight}</div>
        </div>
        """, unsafe_allow_html=True)
