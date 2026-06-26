import pandas as pd
import os

def log_result():
    stats_path = 'data/season_2026_stats.csv'
    df = pd.read_csv(stats_path, encoding='cp1252')
    
    print("--- 14-0 System: Log Game Result ---")
    game_id = int(input("Enter Game_ID: "))
    winner = input("Enter Winner (e.g., CWS): ")
    pick = input("Enter System_Pick: ")
    
    # Update the dataframe
    if game_id in df['Game_ID'].values:
        df.loc[df['Game_ID'] == game_id, 'Result'] = winner
        df.loc[df['Game_ID'] == game_id, 'System_Pick'] = pick
        df.to_csv(stats_path, index=False)
        print(f"✅ Game {game_id} updated: Result={winner}, Pick={pick}")
    else:
        print("!! Game_ID not found in system.")

if __name__ == "__main__":
    log_result()
