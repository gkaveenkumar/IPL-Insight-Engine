"""
data.py — Shared team data, stats helpers, and session utilities.
All pages import from here.
"""

import streamlit as st
import pandas as pd

# ── TEAM DEFINITIONS ──────────────────────────────────────────────────────────
TEAMS = {
    "CSK": {
        "name": "Chennai Super Kings",
        "color": "#F9CF00",
        "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2b/Chennai_Super_Kings_Logo.svg/200px-Chennai_Super_Kings_Logo.svg.png",
        "players": {
            "Batters": ["Ruturaj Gaikwad (C)", "Dewald Brevis", "Ayush Mhatre", "Sarfaraz Khan", "Matthew Short"],
            "Wicket-Keepers": ["MS Dhoni", "Sanju Samson", "Kartik Sharma", "Urvil Patel"],
            "All-Rounders": ["Shivam Dube", "Aman Hakim Khan", "Prashant Veer", "Jamie Overton", "Akeal Hosein"],
            "Bowlers": ["Noor Ahmad", "Rahul Chahar", "Shreyas Gopal", "Matt Henry", "Khaleel Ahmed",
                        "Mukesh Choudhary", "Spencer Johnson", "Anshul Kamboj", "Gurjapneet Singh", "Zak Foulkes"],
        },
    },
    "MI": {
        "name": "Mumbai Indians",
        "color": "#004BA0",
        "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/c/cd/Mumbai_Indians_Logo.svg/200px-Mumbai_Indians_Logo.svg.png",
        "players": {
            "Batters": ["Rohit Sharma", "Suryakumar Yadav", "Tilak Varma", "Sherfane Rutherford", "Naman Dhir", "Danish Malewar"],
            "Wicket-Keepers": ["Quinton de Kock", "Ryan Rickelton", "Robin Minz"],
            "All-Rounders": ["Hardik Pandya (C)", "Mitchell Santner", "Will Jacks", "Raj Bawa", "Corbin Bosch", "Atharva Ankolekar", "Mayank Rawat"],
            "Bowlers": ["Jasprit Bumrah", "Trent Boult", "Deepak Chahar", "Shardul Thakur", "Mayank Markande",
                        "Ashwani Kumar", "Raghu Sharma", "Allah Ghazanfar", "Mohammad Izhar"],
        },
    },
    "RCB": {
        "name": "Royal Challengers Bengaluru",
        "color": "#EC1C24",
        "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2a/Royal_Challengers_Bangalore_2020.svg/200px-Royal_Challengers_Bangalore_2020.svg.png",
        "players": {
            "Batters": ["Virat Kohli", "Rajat Patidar (C)", "Devdutt Padikkal"],
            "Wicket-Keepers": ["Phil Salt", "Jitesh Sharma", "Jordan Cox"],
            "All-Rounders": ["Krunal Pandya", "Tim David", "Romario Shepherd", "Swapnil Singh", "Jacob Bethell",
                             "Venkatesh Iyer", "Satvik Deswal", "Mangesh Yadav", "Vicky Ostwal", "Vihaan Malhotra", "Kanishk Chouhan"],
            "Bowlers": ["Josh Hazlewood", "Bhuvneshwar Kumar", "Yash Dayal", "Nuwan Thushara",
                        "Rasikh Salam", "Suyash Sharma", "Jacob Duffy", "Abhinandan Singh"],
        },
    },
    "KKR": {
        "name": "Kolkata Knight Riders",
        "color": "#6B3FA0",
        "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/4/4c/Kolkata_Knight_Riders_Logo.svg/200px-Kolkata_Knight_Riders_Logo.svg.png",
        "players": {
       
    "Batters": [
        "Ajinkya Rahane (C)",
        "Rinku Singh (VC)",
        "Manish Pandey",
        "Rahul Tripathi"
    ],
    
    "Wicket-Keepers": [
        "Finn Allen",
        "Tim Seifert",
        "Tejasvi Singh",
        "Angkrish Raghuvanshi"
    ],
    
    "All-Rounders": [
        "Cameron Green",
        "Rachin Ravindra",
        "Sunil Narine",
        "Rovman Powell",
        "Ramandeep Singh",
        "Anukul Roy"
    ],
    
    "Bowlers": [
        "Varun Chakaravarthy",
        "Vaibhav Arora",
        "Navdeep Saini",
        "Umran Malik",
        "Kartik Tyagi",
        "Prashant Solanki",
        "Matheesha Pathirana",
        "Blessing Muzarabani",
        "Sarthak Ranjan",
        "Daksh Kamra",
        "Saurabh Dubey"
    ]
},
    },
    "SRH": {
        "name": "Sunrisers Hyderabad",
        "color": "#FF822A",
        "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/8/81/Sunrisers_Hyderabad.svg/200px-Sunrisers_Hyderabad.svg.png",
        "players": {
           "Batters": [
        "Travis Head",
        "Aniket Verma",
        "R. Smaran"
    ],
    
    "Wicket-Keepers": [
        "Ishan Kishan",
        "Heinrich Klaasen"
    ],
    
    "All-Rounders": [
        "Pat Cummins (C)",
        "Abhishek Sharma",
        "Nitish Kumar Reddy",
        "Kamindu Mendis",
        "Harsh Dubey",
        "Brydon Carse",
        "Liam Livingstone",
        "Jack Edwards"
    ],
    
    "Bowlers": [
        "Harshal Patel",
        "Jaydev Unadkat",
        "Eshan Malinga",
        "Zeeshan Ansari",
        "Shivam Mavi",
        "Shivang Kumar",
        "Sakib Hussain",
        "Omkar Tarmale",
        "Amit Kumar",
        "Praful Hinge",
        "Krains Fuletra",
        "Salil Arora"
    ],
        },
    },
    "DC": {
        "name": "Delhi Capitals",
        "color": "#0078BC",
        "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f5/Delhi_Capitals_Logo.svg/200px-Delhi_Capitals_Logo.svg.png",
        "players": {
            "Batters": [
        "Prithvi Shaw",
        "Karun Nair",
        "Nitish Rana",
        "Sahil Parakh",
        "Pathum Nissanka",
        "David Miller"
    ],
    
    "Wicket-Keepers": [
        "KL Rahul",
        "Abishek Porel",
        "Ben Duckett",
        "Tristan Stubbs"
    ],
    
    "All-Rounders": [
        "Axar Patel (C)",
        "Ajay Mandal",
        "Sameer Rizvi",
        "Ashutosh Sharma",
        "Madhav Tiwari",
        "Vipraj Nigam",
        "Kyle Jamieson"
    ],
    
    "Bowlers": [
        "Kuldeep Yadav",
        "Auqib Nabi",
        "Mukesh Kumar",
        "T Natarajan",
        "Tripurana Vijay",
        "Lungi Ngidi",
        "Dushmantha Chameera",
        "Mitchell Starc"
    ],
        }
        ,
    },
    "RR": {
        "name": "Rajasthan Royals",
        "color": "#FF69B4",
        "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/6/60/Rajasthan_Royals_Logo.svg/200px-Rajasthan_Royals_Logo.svg.png",
        "players": {
            "Batters": ["Yashasvi Jaiswal", "Shimron Hetmyer", "Shubham Dubey", "Vaibhav Suryavanshi", "Aman Rao"],
            "Wicket-Keepers": ["Dhruv Jurel", "Donovan Ferreira", "Ravi Singh", "Lhuan-dre Pretorius"],
            "All-Rounders": ["Riyan Parag (C)", "Ravindra Jadeja", "Sam Curran", "Dasun Shanaka", "Yudhvir Singh Charak"],
            "Bowlers": ["Jofra Archer", "Tushar Deshpande", "Kwena Maphaka", "Ravi Bishnoi", "Sandeep Sharma",
                        "Kuldeep Sen", "Adam Milne", "Nandre Burger", "Sushant Mishra", "Yash Raj Punja",
                        "Vignesh Puthur", "Brijesh Sharma"],
        },
    },
    "LSG": {
        "name": "Lucknow Super Giants",
        "color": "#A72B2A",
        "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/1/17/Lucknow_Super_Giants_IPL_Logo.svg/200px-Lucknow_Super_Giants_IPL_Logo.svg.png",
        "players": {
            "Batters": [
        "Aiden Markram",
        "Abdul Samad",
        "Ayush Badoni",
        "Akshat Raghuvanshi",
        "Matthew Breetzke",
        "Mukul Choudhary"
    ],
    
    "Wicket-Keepers": [
        "Rishabh Pant (C)",
        "Nicholas Pooran",
        "Josh Inglis"
    ],
    
    "All-Rounders": [
        "Mitchell Marsh",
        "Shahbaz Ahmed",
        "Digvesh Singh Rathi",
        "Wanindu Hasaranga",
        "Naman Tiwari",
        "Arjun Tendulkar"
    ],
    
    "Bowlers": [
        "Avesh Khan",
        "Anrich Nortje",
        "Prince Yadav",
        "Mohsin Khan",
        "Mohammed Shami"
    ],
        },
    },
    "GT": {
        "name": "Gujarat Titans",
        "color": "#C8A84B",
        "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/0/09/Gujarat_Titans_Logo.svg/200px-Gujarat_Titans_Logo.svg.png",
        "players": {
             "Batters": [
        "Shubman Gill (C)",
        "Sai Sudharsan"
    ],
    
    "Wicket-Keepers": [
        "Jos Buttler",
        "Kumar Kushagra",
        "Anuj Rawat",
        "Tom Banton"
    ],
    
    "All-Rounders": [
        "Glenn Phillips",
        "Nishant Sindhu",
        "Washington Sundar",
        "Mohammed Arshad Khan",
        "Sai Kishore",
        "Jayant Yadav",
        "Jason Holder",
        "Rahul Tewatia",
        "Shahrukh Khan"
    ],
    
    "Bowlers": [
        "Kagiso Rabada",
        "Mohammed Siraj",
        "Prasidh Krishna",
        "Manav Suthar",
        "Gurnoor Singh Brar",
        "Ishant Sharma",
        "Ashok Sharma",
        "Luke Wood",
        "Kulwant Khejroliya",
        "Rashid Khan"
    ],
        },
    },
    "PBKS": {
        "name": "Punjab Kings",
        "color": "#D4173A",
        "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/d/d4/Punjab_Kings_Logo.svg/200px-Punjab_Kings_Logo.svg.png",
        "players": {
             "Batters": [
        "Shreyas Iyer (C)",
        "Priyansh Arya",
        "Shashank Singh",
        "Nehal Wadhera",
        "Vishal Nishad"
    ],
    
    "Wicket-Keepers": [
        "Prabhsimran Singh"
    ],
    
    "All-Rounders": [
        "Marcus Stoinis",
        "Azmatullah Omarzai",
        "Marco Jansen",
        "Harpreet Brar",
        "Cooper Connolly",
        "Ben Dwarshuis"
    ],
    
    "Bowlers": [
        "Yuzvendra Chahal",
        "Arshdeep Singh",
        "Lockie Ferguson",
        "Xavier Bartlett",
        "Pravin Dubey"
    ],
        },
    },
}

# ── ORBIT RULES ───────────────────────────────────────────────────────────────
ORBIT_ROLES = {
    "Batters":        ["Bowlers", "All-Rounders"],
    "Bowlers":        ["Batters", "All-Rounders", "Bowlers", "Wicket-Keepers"],
    "All-Rounders":   ["Batters", "Bowlers", "Wicket-Keepers"],
    "Wicket-Keepers": ["Bowlers"],
}

ROLE_SHORT = {
    "Batters": "BAT",
    "Wicket-Keepers": "WK",
    "All-Rounders": "AR",
    "Bowlers": "BWL",
}

# ── NAME NORMALIZER (our names → dataset names) ───────────────────────────────
NAME_NORM = {
    "MS Dhoni":          "Ms Dhoni",
    "KL Rahul":          "K L Rahul",
    "Suryakumar Yadav":  "Surya Kumar Yadav",
    "Tilak Varma":       "N Tilak Varma",
    "B Sai Sudharsan":   "Sai Sudharsan",
    "Jake Fraser-McGurk":"Jake Fraser - Mcgurk",
    "Quinton de Kock":   "Quinton De Kock",
    "Mohammed Shami":    "Mohammad Shami",
    "Nitish Kumar Reddy":"Nitish Kumar Reddy",
}

def normalize(name: str) -> str:
    clean = name.replace(" (C)", "").strip()
    return NAME_NORM.get(clean, clean)


# ── SR COLOR ──────────────────────────────────────────────────────────────────
def sr_color(sr: float, wickets: int = 0) -> str:
    if wickets > 0: return "#ef4444"
    if sr >= 200:   return "#22c55e"
    if sr >= 150:   return "#84cc16"
    if sr >= 100:   return "#eab308"
    if sr >= 60:    return "#f97316"
    return "#ef4444"


def dominance_label(sr: float, wickets: int) -> tuple:
    """Returns (label, bg_color)"""
    if wickets > 0:    return "🎯 Bowler Dominates",       "rgba(239,68,68,.15)"
    if sr >= 200:      return "🔥 Batter Completely Dominates", "rgba(34,197,94,.15)"
    if sr >= 150:      return "🏏 Batter Has Upper Hand",   "rgba(34,197,94,.15)"
    if sr >= 100:      return "⚔️ Evenly Contested",        "rgba(234,179,8,.15)"
    if sr >= 60:       return "🎯 Bowler Has Edge",         "rgba(239,68,68,.15)"
    return                    "🎯 Bowler Dominates",        "rgba(239,68,68,.15)"


# ── STATS LOOKUP ──────────────────────────────────────────────────────────────
def get_stats(center_name: str, center_role: str, orbit_name: str) -> dict | None:
    stats = st.session_state.get("stats")
    if not stats:
        return None
    cn = normalize(center_name)
    on = normalize(orbit_name)
    if center_role in ("Batters", "Wicket-Keepers"):
        return stats.get("bat", {}).get(cn, {}).get(on)
    if center_role == "Bowlers":
        return stats.get("bow", {}).get(cn, {}).get(on)
    # All-Rounders: try both
    return (stats.get("bat", {}).get(cn, {}).get(on)
            or stats.get("bow", {}).get(cn, {}).get(on))


# ── BUILD STATS FROM DATAFRAME ────────────────────────────────────────────────
def build_stats(df: pd.DataFrame) -> dict:
    def is_extra(e):
        s = str(e).strip()
        return "WD" in s or "NB" in s

    def run_val(e):
        try: return int(str(e).strip().split()[0])
        except: return 0

    df = df.copy()
    df["rv"]         = df["event"].apply(run_val)
    df["is_extra"]   = df["event"].apply(is_extra)
    df["is_wicket"]  = df["event"].apply(lambda e: str(e).strip() == "W")
    df["is_ball"]    = ~df["is_extra"]

    bat_stats, bow_stats = {}, {}

    for (bat, bow), grp in df.groupby(["batsman", "bowler"]):
        balls = grp[grp["is_ball"]]
        if len(balls) < 3:
            continue
        tr = int(grp["rv"].sum())
        tb = int(grp["is_ball"].sum())
        tw = int(grp["is_wicket"].sum())
        f4 = int((balls["rv"] == 4).sum())
        f6 = int((balls["rv"] == 6).sum())
        sr = round(tr / tb * 100, 1) if tb > 0 else 0.0
        bm, sm, lm, llm, out = {}, {}, {}, {}, []

        for _, row in balls.iterrows():
            dt  = str(row.get("delivery_type", row.get("bowling_type", ""))).strip()
            sh  = str(row.get("shot_type",   "")).strip()
            ln  = str(row.get("line",        "")).strip()
            rv  = int(row["rv"])
            wk  = bool(row["is_wicket"])

            if dt and dt != "nan":
                if dt not in bm: bm[dt] = [0,0,0,0,0]
                bm[dt][0] += rv; bm[dt][1] += 1
                if wk:    bm[dt][2] += 1
                if rv==4: bm[dt][3] += 1
                if rv==6: bm[dt][4] += 1
            if sh and sh != "nan":
                if sh not in sm: sm[sh] = [0,0,0]
                sm[sh][0] += rv; sm[sh][1] += 1
                if wk: sm[sh][2] += 1
            if ln and ln != "nan":
                if ln not in lm: lm[ln] = [0,0,0]
                lm[ln][0] += rv; lm[ln][1] += 1
                if wk: lm[ln][2] += 1
            if dt and dt != "nan" and ln and ln != "nan":
                key = f"{dt}|||{ln}"
                if key not in llm: llm[key] = [0, 0, 0, {}]
                llm[key][0] += rv; llm[key][1] += 1
                if wk: llm[key][2] += 1
                if sh and sh != "nan":
                    llm[key][3][sh] = llm[key][3].get(sh, 0) + 1
            if wk:
                out.append({"bt": dt, "ln": ln, "st": sh})

        entry = {"r":tr,"b":tb,"w":tw,"4s":f4,"6s":f6,"sr":sr,
                 "bowl":bm,"shot":sm,"line":lm,"length_line":llm,"out":out}
        if bat not in bat_stats: bat_stats[bat] = {}
        bat_stats[bat][bow] = entry
        if bow not in bow_stats: bow_stats[bow] = {}
        bow_stats[bow][bat] = entry

    return {"bat": bat_stats, "bow": bow_stats}


# ── CSS HELPERS ───────────────────────────────────────────────────────────────
def hex_to_rgba(hex_color: str, alpha: float) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return f"rgba({r},{g},{b},{alpha})"


def initials(name: str) -> str:
    clean = name.replace(" (C)", "").strip()
    parts = clean.split()
    return "".join(p[0] for p in parts).upper()[:2]


# ── GLOBAL DARK CSS (injected once per page) ──────────────────────────────────
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@400;500;600&display=swap');
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"],
.main, section.main > div {
    background: #0d1321 !important;
    color: #fff !important;
}
#MainMenu, header, footer,
[data-testid="stToolbar"],
[data-testid="stSidebarNav"],
[data-testid="collapsedControl"],
[data-testid="stDecoration"] { display: none !important; }
.block-container { padding: 1rem 1.5rem !important; max-width: 1200px !important; }
button[kind="secondary"], button[kind="primary"] {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: rgba(255,255,255,0.75) !important;
    border-radius: 20px !important;
    font-family: 'DM Sans', sans-serif !important;
}
button[kind="secondary"]:hover, button[kind="primary"]:hover {
    background: rgba(255,255,255,0.14) !important;
    color: #fff !important;
}
.stFileUploader label { color: rgba(255,255,255,0.5) !important; }
</style>
"""


def inject_css():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


# ── NAVIGATION ────────────────────────────────────────────────────────────────
def nav_to(page: str, **kwargs):
    """Set session state and switch page."""
    st.session_state["page"] = page
    for k, v in kwargs.items():
        st.session_state[k] = v
    st.switch_page(f"pages/{page}.py")

# ── BUILD PHASE STATS FROM DATAFRAME ─────────────────────────────────────────
def build_phase_stats(df: pd.DataFrame) -> dict:
    """
    Returns a dict with two top-level keys: 'batsman' and 'bowler'.
    Each maps player_name → phase ('powerplay'|'middle'|'death') → stats dict.
    
    Batter stats per phase:
        runs, balls, sr, fours, sixes, dot_pct,
        top_shots: [(shot, runs, balls, wkts), ...],
        bowl_faced: [(delivery_type, runs, balls, wkts), ...]
    
    Bowler stats per phase:
        runs_given, balls, economy, wickets,
        top_deliveries: [(delivery_type, runs, balls, wkts), ...],
        top_lines: [(line, runs, balls, wkts), ...]
    """
    def is_extra(e):
        s = str(e).strip()
        return "WD" in s or "NB" in s

    def run_val(e):
        try: return int(str(e).strip().split()[0])
        except: return 0

    df = df.copy()
    df["rv"]        = df["event"].apply(run_val)
    df["is_extra"]  = df["event"].apply(is_extra)
    df["is_wicket"] = df["event"].apply(lambda e: str(e).strip() == "W")
    df["is_ball"]   = ~df["is_extra"]
    df["over_num"]  = df["ball"].apply(lambda x: int(str(x).split(".")[0]))

    def phase_label(o):
        if o <= 5:  return "powerplay"
        if o <= 13: return "middle"
        return "death"

    df["phase"] = df["over_num"].apply(phase_label)

    bat_phase = {}
    bow_phase = {}

    phases = ["powerplay", "middle", "death"]

    # ── BATTER PHASE STATS ──
    for bat, grp in df.groupby("batsman"):
        bat_phase[bat] = {}
        for ph in phases:
            pg = grp[grp["phase"] == ph]
            balls = pg[pg["is_ball"]]
            if len(balls) == 0:
                continue
            tr = int(pg["rv"].sum())
            tb = int(pg["is_ball"].sum())
            tw = int(pg["is_wicket"].sum())
            f4 = int((balls["rv"] == 4).sum())
            f6 = int((balls["rv"] == 6).sum())
            dots = int((balls["rv"] == 0).sum())
            sr = round(tr / tb * 100, 1) if tb else 0.0
            dot_pct = round(dots / tb * 100, 1) if tb else 0.0

            # shots breakdown
            sm = {}
            for _, row in balls.iterrows():
                sh = str(row.get("shot_type", "")).strip()
                rv = int(row["rv"])
                wk = bool(row["is_wicket"])
                if sh and sh != "nan":
                    if sh not in sm: sm[sh] = [0, 0, 0]
                    sm[sh][0] += rv; sm[sh][1] += 1
                    if wk: sm[sh][2] += 1

            # delivery types faced
            bm = {}
            for _, row in balls.iterrows():
                dt = str(row.get("delivery_type", row.get("bowling_type", ""))).strip()
                rv = int(row["rv"])
                wk = bool(row["is_wicket"])
                if dt and dt != "nan":
                    if dt not in bm: bm[dt] = [0, 0, 0]
                    bm[dt][0] += rv; bm[dt][1] += 1
                    if wk: bm[dt][2] += 1

            top_shots = sorted(
                [(sh, v[0], v[1], v[2]) for sh, v in sm.items()],
                key=lambda x: -x[1]
            )[:8]
            bowl_faced = sorted(
                [(dt, v[0], v[1], v[2]) for dt, v in bm.items()],
                key=lambda x: -x[1]
            )

            bat_phase[bat][ph] = {
                "runs": tr, "balls": tb, "sr": sr,
                "fours": f4, "sixes": f6, "dot_pct": dot_pct,
                "wickets": tw,
                "top_shots": top_shots,
                "bowl_faced": bowl_faced,
            }

    # ── BOWLER PHASE STATS ──
    for bow, grp in df.groupby("bowler"):
        bow_phase[bow] = {}
        for ph in phases:
            pg = grp[grp["phase"] == ph]
            balls = pg[pg["is_ball"]]
            if len(balls) == 0:
                continue
            tr = int(pg["rv"].sum())
            tb = int(pg["is_ball"].sum())
            tw = int(pg["is_wicket"].sum())
            dots = int((balls["rv"] == 0).sum())
            econ = round(tr / tb * 6, 2) if tb else 0.0
            dot_pct = round(dots / tb * 100, 1) if tb else 0.0

            # delivery types bowled (bowling_type: e.g. "inswinger", "yorker")
            dm = {}
            for _, row in balls.iterrows():
                dt = str(row.get("bowling_type", row.get("delivery_type", ""))).strip()
                rv = int(row["rv"])
                wk = bool(row["is_wicket"])
                if dt and dt != "nan":
                    if dt not in dm: dm[dt] = [0, 0, 0]
                    dm[dt][0] += rv; dm[dt][1] += 1
                    if wk: dm[dt][2] += 1

            # delivery type breakdown (delivery_type: e.g. "wide on wide outside off")
            lm = {}
            for _, row in balls.iterrows():
                ln = str(row.get("delivery_type", row.get("line", ""))).strip()
                rv = int(row["rv"])
                wk = bool(row["is_wicket"])
                if ln and ln != "nan":
                    if ln not in lm: lm[ln] = [0, 0, 0]
                    lm[ln][0] += rv; lm[ln][1] += 1
                    if wk: lm[ln][2] += 1

            top_deliveries = sorted(
                [(dt, v[0], v[1], v[2]) for dt, v in dm.items()],
                key=lambda x: -x[1]
            )
            top_lines = sorted(
                [(ln, v[0], v[1], v[2]) for ln, v in lm.items()],
                key=lambda x: -x[1]
            )

            bow_phase[bow][ph] = {
                "runs_given": tr, "balls": tb, "economy": econ,
                "wickets": tw, "dot_pct": dot_pct,
                "top_deliveries": top_deliveries,
                "top_lines": top_lines,
            }

    return {"batsman": bat_phase, "bowler": bow_phase}
