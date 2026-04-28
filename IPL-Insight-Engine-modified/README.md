# IPL Orbital Explorer – Streamlit Application

IPL Orbital Explorer is a multi-page Streamlit web application designed to explore IPL teams, players, datasets, and statistics through interactive visualizations and structured navigation. The application loads IPL data from an Excel dataset and allows users to navigate between teams, players, orbit visualization, statistics, and phase analysis pages using Streamlit session state.

This project demonstrates multi-page Streamlit architecture, session state management, data visualization, and structured Python project organization.

## Features

- Load IPL dataset from Excel file
- Explore IPL teams
- View players by team
- Player categorization (Batters, Bowlers, All-Rounders, Wicket Keepers)
- Orbit visualization of teams/players
- Statistics and data insights
- **Phase Analysis** – per-player and team-level breakdown across Powerplay, Middle, and Death overs
- Multi-page Streamlit navigation
- Session state data management

## Application Workflow

1. Application starts from `app.py`
2. Checks whether dataset statistics are loaded in session state
3. If not loaded → Redirect to Dataset Page
4. After loading dataset → Redirect to Teams Page
5. User can navigate to:
   - Players Page
   - Orbit Visualization Page
   - Statistics Page
   - **Phase Analysis Page**
6. All pages share common data from `data.py`

## Phase Analysis

The Phase Analysis page (`pages/6_phase.py`) provides a detailed breakdown of player and team performance split across the three T20 phases:

- **Powerplay** (Overs 1–6)
- **Middle Overs** (Overs 7–14)
- **Death Overs** (Overs 15–20)

### Batter Mode
- Key metrics per phase: Runs, Balls, Strike Rate, Average, Fours, Sixes, Boundary %, Dot %
- Shots played breakdown with SR per shot type
- Delivery types faced (e.g. "good length on outside off", "wide on wide outside off") with runs, balls, and dismissal info

### Bowler Mode
- Key metrics per phase: Runs Given, Balls, Economy, Wickets, Bowling Average, Bowling SR, Dot %
- Delivery variations bowled (bowling type: inswinger, yorker, googly, etc.)
- Delivery types bowled (full delivery description: line + length combination)

### Team Compare Mode
- Side-by-side phase comparison between any two squads
- Metrics: Batting Strike Rate, Bowling Economy, Batting Average, Bowling Average
- Visual bar comparison with phase-by-phase winner insight

## Installation

Install dependencies:

```
pip install -r requirements.txt
```

## Usage

Run the Streamlit application:

```
streamlit run app.py
```

## Technologies Used

- Python
- Streamlit
- Pandas
- Excel Dataset
- Data Visualization
- Session State Navigation

## Future Improvements

- Add match predictions using Machine Learning
- Add database integration
- Deploy on Streamlit Cloud
- Add authentication/login system
