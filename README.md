# IPL Orbital Explorer – Streamlit Application

IPL Orbital Explorer is a multi-page Streamlit web application designed to explore IPL teams, players, datasets, and statistics through interactive visualizations and structured navigation. The application loads IPL data from an Excel dataset and allows users to navigate between teams, players, orbit visualization, and statistics pages using Streamlit session state.

This project demonstrates multi-page Streamlit architecture, session state management, data visualization, and structured Python project organization.
## Features

- Load IPL dataset from Excel file
- Explore IPL teams
- View players by team
- Player categorization (Batters, Bowlers, All-Rounders, Wicket Keepers)
- Orbit visualization of teams/players
- Statistics and data insights
- Multi-page Streamlit navigation
- Session state data management
## Application Workflow

1. Application starts from app.py
2. Checks whether dataset statistics are loaded in session state
3. If not loaded → Redirect to Dataset Page
4. After loading dataset → Redirect to Teams Page
5. User can navigate to:
   - Players Page
   - Orbit Visualization Page
   - Statistics Page
6. All pages share common data from data.py
## Installation

Install dependencies:
pip install -r requirements.txt
## Usage

Run the Streamlit application:
streamlit run app.py
## Technologies Used

- Python
- Streamlit
- Pandas
- Excel Dataset
- Data Visualization
- Session State Navigation
## Future Improvements

- Add player statistics dashboard
- Add match predictions using Machine Learning
- Add database integration
- Deploy on Streamlit Cloud
- Add authentication/login system