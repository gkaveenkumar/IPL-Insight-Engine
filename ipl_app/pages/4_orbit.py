"""
pages/4_orbit.py — Player at center, all 10 team logos orbit.
                   Click a team logo → orbit shows opposite-role players.
                   Click a player chip → go to stats page.
Uses an HTML canvas component for the orbital visualization.
"""
import streamlit as st
import streamlit.components.v1 as components
import json, os, sys

st.set_page_config(
    page_title="IPL Orbital — Orbit View",
    page_icon="🔵",
    layout="wide",
    initial_sidebar_state="collapsed",
)

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from data import (inject_css, TEAMS, hex_to_rgba, initials,
                  ROLE_SHORT, ORBIT_ROLES, get_stats, sr_color)

inject_css()

if "stats" not in st.session_state:
    st.switch_page("pages/1_dataset.py")
if "selected_player" not in st.session_state:
    st.switch_page("pages/3_players.py")

# ── Read state ────────────────────────────────────────────────────────────────
player_name = st.session_state["selected_player"]
player_role = st.session_state["selected_player_role"]
player_team = st.session_state["selected_player_team"]
orbit_team  = st.session_state.get("orbit_team")   # set when user picks a team in orbit
clean_name  = player_name.replace(" (C)", "").strip()
t           = TEAMS[player_team]

# ── TOPBAR ────────────────────────────────────────────────────────────────────
col_b1, col_b2, col_crumb = st.columns([1, 1, 6])
with col_b1:
    if st.button("← Squad", key="back_squad"):
        st.session_state.pop("orbit_team", None)
        st.switch_page("pages/3_players.py")
with col_b2:
    if orbit_team:
        if st.button("← Teams orbit", key="back_teams_orbit"):
            st.session_state.pop("orbit_team", None)
            st.rerun()
with col_crumb:
    crumb_parts = [
        f"<span style='color:rgba(255,255,255,.5);cursor:pointer' onclick=''>{player_team}</span>",
        f"<span style='color:rgba(255,255,255,.2)'> › </span>",
        f"<span style='color:rgba(255,255,255,.7)'>{clean_name}</span>",
    ]
    if orbit_team:
        ot = TEAMS[orbit_team]
        roles = ORBIT_ROLES.get(player_role, ["Bowlers"])
        lp = " + ".join(ROLE_SHORT[r] for r in roles)
        crumb_parts += [
            f"<span style='color:rgba(255,255,255,.2)'> › </span>",
            f"<span style='color:{ot['color']}'>{orbit_team} {lp}</span>",
        ]
    st.markdown(
        f"<div style='font-size:11px;margin-top:8px'>{''.join(crumb_parts)}</div>",
        unsafe_allow_html=True
    )

# ── PREPARE ORBIT DATA ────────────────────────────────────────────────────────
if orbit_team is None:
    # Show all 10 team logo chips in orbit
    orbit_items = [
        {
            "code": code,
            "label": code,
            "color": TEAMS[code]["color"],
            "type": "team",
            "logo": TEAMS[code]["logo"],
        }
        for code in TEAMS
    ]
else:
    # Show opposite-role players of orbit_team
    ot = TEAMS[orbit_team]
    roles = ORBIT_ROLES.get(player_role, ["Bowlers"])
    orbit_items = []
    for r in roles:
        for pname in ot["players"].get(r, []):
            st_data = get_stats(player_name, player_role, pname)
            badge_label = ""
            badge_color = "#888"
            if st_data:
                badge_color = sr_color(st_data["sr"], st_data["w"])
                badge_label = f"{st_data['r']}/{st_data['w']}" if st_data["w"] > 0 else str(st_data["r"])
            orbit_items.append({
                "name":        pname,
                "clean":       pname.replace(" (C)", "").strip(),
                "ini":         initials(pname),
                "role":        r,
                "short_role":  ROLE_SHORT.get(r, r[:3]),
                "color":       ot["color"],
                "type":        "player",
                "badge":       badge_label,
                "badge_color": badge_color,
                "is_captain":  "(C)" in pname,
            })

# ── BUILD THE ORBITAL HTML COMPONENT ─────────────────────────────────────────
stats_json    = json.dumps(st.session_state.get("stats", {}), separators=(",",":"))
items_json    = json.dumps(orbit_items, separators=(",",":"))
pt_color      = t["color"]
pt_rgba_22    = hex_to_rgba(pt_color, 0.22)
pt_rgba_18    = hex_to_rgba(pt_color, 0.18)
pt_rgba_38    = hex_to_rgba(pt_color, 0.38)
is_captain    = "(C)" in player_name
ini_str       = initials(player_name)
orbit_team_c  = TEAMS[orbit_team]["color"] if orbit_team else pt_color
rl_text       = ""
if orbit_team:
    roles = ORBIT_ROLES.get(player_role, ["Bowlers"])
    rl_text = f"{TEAMS[orbit_team]['name']} — {' + '.join(roles)} orbiting"

orbital_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@400;600&display=swap" rel="stylesheet">
<style>
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ background:#0d1321; font-family:'DM Sans',sans-serif; overflow:hidden; }}
#arena {{ position:relative; width:100%; height:520px; }}
canvas {{ position:absolute; top:0; left:0; width:100%; height:100%; pointer-events:none; }}
.cpod {{
  position:absolute; left:50%; top:50%; transform:translate(-50%,-50%);
  z-index:20; text-align:center; width:160px;
}}
.cav {{
  width:90px; height:90px; border-radius:50%;
  margin:0 auto 10px;
  display:flex; align-items:center; justify-content:center;
  font-family:'Bebas Neue',sans-serif; font-size:28px;
}}
.cnm {{ font-family:'Bebas Neue',sans-serif; font-size:16px; letter-spacing:1.5px; line-height:1.2; color:#fff; }}
.crole {{ font-size:9px; color:rgba(255,255,255,.4); letter-spacing:1px; text-transform:uppercase; margin-top:2px; }}
.ccap {{ font-size:8px; letter-spacing:1.5px; margin-top:2px; }}
.cbadge {{
  display:inline-block; margin-top:8px; padding:3px 13px;
  border-radius:20px; font-size:10px; font-weight:600; letter-spacing:1px;
}}
.oc {{ position:absolute; transform:translate(-50%,-50%); z-index:15; cursor:pointer; }}
.chip-t {{
  width:60px; height:60px; border-radius:50%;
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  border:2px solid; transition:all .2s; gap:2px;
}}
.chip-t:hover {{ transform:scale(1.18); }}
.chip-code {{ font-family:'Bebas Neue',sans-serif; font-size:13px; }}
.chip-dot {{ width:4px; height:4px; border-radius:50%; opacity:.7; }}
.chip-p {{
  width:64px; height:64px; border-radius:50%;
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  border:2px solid; transition:all .2s; gap:2px; padding:4px; position:relative;
}}
.chip-p:hover {{ transform:scale(1.14); }}
.chip-pav {{
  width:28px; height:28px; border-radius:50%;
  display:flex; align-items:center; justify-content:center;
  font-family:'Bebas Neue',sans-serif; font-size:9px;
}}
.chip-pnm {{
  font-size:7px; font-weight:600; text-align:center; line-height:1.2; color:#fff;
  max-width:56px; overflow:hidden; white-space:nowrap; text-overflow:ellipsis;
}}
.chip-prl {{ font-size:6px; text-align:center; }}
.sring {{
  position:absolute; top:-7px; right:-7px;
  width:22px; height:22px; border-radius:50%;
  display:flex; align-items:center; justify-content:center;
  font-family:'Bebas Neue',sans-serif; font-size:8px; font-weight:700;
  border:1.5px solid rgba(0,0,0,.5); z-index:5;
}}
.hint {{
  position:absolute; bottom:8px; left:50%; transform:translateX(-50%);
  font-size:10px; color:rgba(255,255,255,.22); letter-spacing:1px;
  white-space:nowrap;
}}
.rl {{
  position:absolute; bottom:30px; left:50%; transform:translateX(-50%);
  font-size:9px; letter-spacing:1.2px; text-transform:uppercase; white-space:nowrap;
}}
</style>
</head>
<body>
<div id="arena">
  <canvas id="cv"></canvas>
  <div class="cpod">
    <div class="cav" style="background:{pt_rgba_22};border:3px solid {pt_color};color:{pt_color}">{ini_str}</div>
    <div class="cnm">{clean_name}</div>
    <div class="crole">{player_role.replace('Wicket-Keepers','Wicket Keeper')}</div>
    {"<div class='ccap' style='color:" + pt_color + "'>CAPTAIN</div>" if is_captain else ""}
    <div class="cbadge" style="background:{pt_rgba_18};color:{pt_color};border:1px solid {pt_rgba_38}">{player_team}</div>
  </div>
  <div class="hint" id="hint">{"Click any player to see full stats" if orbit_team else "Click any team logo to see their players orbit"}</div>
  {"<div class='rl' style='color:rgba(255,255,255,.3)'>" + rl_text + "</div>" if rl_text else ""}
</div>

<script>
const ITEMS   = {items_json};
const PT_COL  = "{pt_color}";
const OT_COL  = "{orbit_team_c}";
const IS_TEAM = {"true" if orbit_team is None else "false"};

function rgba(h,a){{
  const r=parseInt(h.slice(1,3),16),g=parseInt(h.slice(3,5),16),b=parseInt(h.slice(5,7),16);
  return `rgba(${{r}},${{g}},${{b}},${{a}})`;
}}

function buildOrbit() {{
  const arena = document.getElementById('arena');
  const cv    = document.getElementById('cv');
  const W = arena.offsetWidth, H = arena.offsetHeight;
  const cx = W/2, cy = H/2;
  const rx = Math.min(W*0.41, 200), ry = Math.min(H*0.40, 190);

  cv.width = W; cv.height = H;
  const ctx = cv.getContext('2d');
  ctx.clearRect(0,0,W,H);

  // Glow
  const grd = ctx.createRadialGradient(cx,cy,5,cx,cy,rx+20);
  grd.addColorStop(0, rgba(PT_COL,.08)); grd.addColorStop(1,'transparent');
  ctx.fillStyle=grd; ctx.fillRect(0,0,W,H);

  // Inner ring
  if(!IS_TEAM) {{
    ctx.save(); ctx.strokeStyle=PT_COL; ctx.lineWidth=.6; ctx.globalAlpha=.12;
    ctx.setLineDash([3,8]);
    ctx.beginPath(); ctx.ellipse(cx,cy,rx-18,ry-18,0,0,Math.PI*2); ctx.stroke(); ctx.restore();
  }}

  // Outer orbit ring
  ctx.save(); ctx.strokeStyle=OT_COL; ctx.lineWidth=1; ctx.globalAlpha=.22; ctx.setLineDash([5,7]);
  ctx.beginPath(); ctx.ellipse(cx,cy,rx,ry,0,0,Math.PI*2); ctx.stroke(); ctx.restore();

  // Remove old chips
  arena.querySelectorAll('.oc').forEach(e=>e.remove());

  const count = ITEMS.length || 1;
  ITEMS.forEach((item, i) => {{
    const angle = (i/count)*2*Math.PI - Math.PI/2;
    const lx = cx + rx*Math.cos(angle);
    const ly = cy + ry*Math.sin(angle);

    // Spoke
    const isCurrent = !IS_TEAM || false;
    ctx.save(); ctx.strokeStyle=item.color; ctx.lineWidth=.6; ctx.globalAlpha=.18; ctx.setLineDash([3,6]);
    ctx.beginPath(); ctx.moveTo(cx,cy); ctx.lineTo(lx,ly); ctx.stroke(); ctx.restore();

    const chip = document.createElement('div');
    chip.className='oc'; chip.style.cssText=`left:${{lx}}px;top:${{ly}}px;`;

    if(item.type === 'team') {{
      chip.innerHTML=`<div class="chip-t" style="background:${{rgba(item.color,.16)}};border-color:${{item.color}}">
        <div class="chip-code" style="color:${{item.color}}">${{item.code}}</div>
        <div class="chip-dot" style="background:${{item.color}}"></div>
      </div>`;
      chip.onclick = () => window.parent.postMessage({{type:'team_click', code:item.code}}, '*');
    }} else {{
      const badge = item.badge
        ? `<div class="sring" style="background:rgba(13,19,33,.9);color:${{item.badge_color}};border-color:${{item.badge_color}}">${{item.badge}}</div>`
        : '';
      chip.innerHTML=`<div class="chip-p" style="background:${{rgba(item.color,.15)}};border-color:${{rgba(item.color,.48)}}">
        ${{badge}}
        <div class="chip-pav" style="background:${{rgba(item.color,.28)}};color:${{item.color}};border:1px solid ${{rgba(item.color,.5)}}">${{item.ini}}</div>
        <div class="chip-pnm">${{item.clean.split(' ')[0]}}${{item.is_captain?' ▲':''}}</div>
        <div class="chip-prl" style="color:${{rgba(item.color,.75)}}">${{item.short_role}}</div>
      </div>`;
      chip.onclick = () => window.parent.postMessage({{
        type:'player_click',
        name: item.name,
        role: item.role,
      }}, '*');
    }}
    arena.appendChild(chip);
  }});
}}

buildOrbit();
window.addEventListener('resize', buildOrbit);
</script>
</body>
</html>"""

# ── RENDER COMPONENT & HANDLE MESSAGES ───────────────────────────────────────
components.html(orbital_html, height=540)

# ── CLICK HANDLERS via selectbox workaround ──────────────────────────────────
# Since postMessage can't trigger st.rerun(), use selectboxes as click proxies
st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

if orbit_team is None:
    # Show team selector below the orbit
    st.markdown("<div style='font-size:11px;color:rgba(255,255,255,.4);letter-spacing:1px;text-align:center;margin-bottom:8px'>SELECT A TEAM TO DRILL INTO</div>", unsafe_allow_html=True)
    cols = st.columns(10)
    for i, (code, team_data) in enumerate(TEAMS.items()):
        c = team_data["color"]
        with cols[i]:
            st.markdown(f"""
            <div style="text-align:center;margin-bottom:4px">
              <div style="width:44px;height:44px;border-radius:50%;
                          background:{hex_to_rgba(c,.18)};border:2px solid {hex_to_rgba(c,.5)};
                          color:{c};margin:0 auto;display:flex;align-items:center;justify-content:center;
                          font-family:'Bebas Neue',sans-serif;font-size:12px">{code}</div>
            </div>""", unsafe_allow_html=True)
            if st.button(code, key=f"oteam_{code}", use_container_width=True):
                st.session_state["orbit_team"] = code
                st.rerun()
else:
    # Show player selector below the orbit for orbit team players
    ot = TEAMS[orbit_team]
    roles = ORBIT_ROLES.get(player_role, ["Bowlers"])
    all_orbit_players = []
    for r in roles:
        for pname in ot["players"].get(r, []):
            all_orbit_players.append((pname, r))

    if all_orbit_players:
        st.markdown(f"<div style='font-size:11px;color:rgba(255,255,255,.4);letter-spacing:1px;text-align:center;margin-bottom:10px'>SELECT A PLAYER TO SEE FULL STATS</div>", unsafe_allow_html=True)

        # Group by role
        for r in roles:
            role_players = [(pn, rr) for pn, rr in all_orbit_players if rr == r]
            if not role_players:
                continue
            c = ot["color"]
            st.markdown(f"<div style='font-size:12px;color:rgba(255,255,255,.4);letter-spacing:1px;margin-bottom:6px'><b style='color:#fff'>{r}</b></div>", unsafe_allow_html=True)

            for row_start in range(0, len(role_players), 5):
                chunk = role_players[row_start:row_start+5]
                cols  = st.columns(5)
                for col, (pname, prole) in zip(cols, chunk):
                    clean = pname.replace(" (C)", "").strip()
                    ini_s = initials(pname)
                    st_data = get_stats(player_name, player_role, pname)
                    badge = ""
                    if st_data:
                        bc = sr_color(st_data["sr"], st_data["w"])
                        badge = f"{st_data['r']}/{st_data['w']}" if st_data["w"] > 0 else str(st_data["r"])

                    with col:
                        st.markdown(f"""
                        <div style="background:rgba(255,255,255,.05);border:1px solid {hex_to_rgba(c,.3)};
                                    border-radius:10px;padding:8px 4px;text-align:center;">
                          <div style="width:36px;height:36px;border-radius:50%;
                                      background:{hex_to_rgba(c,.2)};border:2px solid {hex_to_rgba(c,.5)};
                                      color:{c};margin:0 auto 4px;
                                      display:flex;align-items:center;justify-content:center;
                                      font-family:'Bebas Neue',sans-serif;font-size:11px">{ini_s}</div>
                          <div style="font-size:9px;font-weight:600;color:#fff">{clean[:12]}</div>
                          {"<div style='font-size:9px;color:" + bc + ";font-weight:700'>" + badge + "</div>" if badge else ""}
                        </div>""", unsafe_allow_html=True)

                        if st.button(clean[:12], key=f"op_{orbit_team}_{pname}", use_container_width=True):
                            st.session_state["orbit_player"]      = pname
                            st.session_state["orbit_player_role"] = prole
                            st.session_state["orbit_player_team"] = orbit_team
                            st.switch_page("pages/5_stats.py")
