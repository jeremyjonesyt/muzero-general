import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="14-0 System: MuZero Slate Engine", layout="wide")

st.title("14-0 System: MuZero Unrestricted Inference Dashboard")
st.subheader("June 2026 Full Slate - Forced Choice Selections")

team_mapping = {
    401: {"teams": ("CWS", "DET"), "dk_odds": "+102"},
    402: {"teams": ("CIN", "NYY"), "dk_odds": "+170"},
    403: {"teams": ("TOR", "CHC"), "dk_odds": "+114"},
    404: {"teams": ("NYM", "PHI"), "dk_odds": "+152"},
    405: {"teams": ("CLE", "HOU"), "dk_odds": "+120"},
    406: {"teams": ("SD", "TEX"),  "dk_odds": "+105"},
    407: {"teams": ("PIT", "COL"), "dk_odds": "-222"},
    408: {"teams": ("LAA", "ATH"), "dk_odds": "+138"},
    409: {"teams": ("BAL", "LAD"), "dk_odds": "+198"},
    410: {"teams": ("BOS", "SEA"), "dk_odds": "+106"},
    411: {"teams": ("MIN", "AZ"),  "dk_odds": "+110"}
}

def logit_to_prob(logit):
    return 1 / (1 + np.exp(-logit))

try:
    stats_df = pd.read_csv('data/season_2026_stats.csv')
    preds_df = pd.read_csv('season_2026_predictions.csv')

    stats_df['Game_ID'] = stats_df['Game_ID'].astype(int)
    merged = pd.concat([stats_df, preds_df['prediction']], axis=1).dropna()

    merged['Team'] = merged['Game_ID'].map(lambda x: team_mapping.get(x, {"teams": ("UNK","UNK")})["teams"][0])
    merged['Opponent'] = merged['Game_ID'].map(lambda x: team_mapping.get(x, {"teams": ("UNK","UNK")})["teams"][1])
    merged['DK_Odds'] = merged['Game_ID'].map(lambda x: team_mapping.get(x, {"dk_odds": "N/A"})["dk_odds"])
    
    merged['Win_Probability'] = merged['prediction'].apply(logit_to_prob)
    merged['Matchup'] = merged.apply(lambda r: f"{r['Team']} vs {r['Opponent']}" if r['Home_Away'] == 1 else f"{r['Team']} @ {r['Opponent']}", axis=1)

    merged['System_Pick'] = merged.apply(lambda r: r['Team'] if r['Win_Probability'] >= 0.50 else r['Opponent'], axis=1)

    st.markdown("## FORCED SYSTEM DIRECTIVES (ALL MATCHUPS)")
    
    for idx, row in merged.sort_values(by='Game_ID').iterrows():
        st.success(f"GAME {row['Game_ID']} SELECTION: PICK {row['System_Pick']} TO WIN | Matchup: {row['Matchup']} | Model Prob: {row['Win_Probability']:.1%} | DK Odds: {row['DK_Odds']}")

    st.markdown("---")
    st.markdown("### Complete Slate Evaluation Matrix")
    display_df = merged[['Game_ID', 'Matchup', 'DK_Odds', 'Run_Differential', 'Opponent_Win_Pct', 'Win_Probability']].copy()
    display_df['Win_Probability'] = display_df['Win_Probability'].map(lambda x: f"{x:.1%}")
    st.dataframe(display_df, use_container_width=False, width="content")

except Exception as e:
    st.error(f"Dashboard runtime error: {e}")
