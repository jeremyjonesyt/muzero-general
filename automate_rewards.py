import pandas as pd
import os

def automate_reward_feedback():
    stats_path = 'data/season_2026_stats.csv'
    reward_path = 'data/reward_matrix.csv'
    
    if not os.path.exists(stats_path):
        print("!! Stats file not found.")
        return

    df = pd.read_csv(stats_path, encoding='cp1252')

    # Ensure required columns exist
    for col in ['System_Pick', 'Result']:
        if col not in df.columns:
            df[col] = None
    
    # Calculate Reward: +1 for Hit, -1 for Miss
    # We only calculate if data exists, otherwise report empty status
    if df['System_Pick'].notnull().all() and df['Result'].notnull().all():
        df['Reward'] = df.apply(lambda r: 1 if r['System_Pick'] == r['Result'] else -1, axis=1)
        df.to_csv(reward_path, index=False)
        print("✅ REWARD SYNC COMPLETE: Policy updated based on game outcomes.")
    else:
        print("⚠️ SYNC PENDING: 'System_Pick' and 'Result' columns exist but are missing data. Please update your CSV.")

if __name__ == "__main__":
    automate_reward_feedback()
