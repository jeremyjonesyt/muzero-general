import pandas as pd
import os

def batch_update_results():
    master_path = 'data/season_2026_stats.csv'
    batch_path = 'daily_results_input.csv'
    
    if not os.path.exists(batch_path):
        print("!! No daily_results_input.csv found to sync.")
        return

    # Load master and new batch
    df = pd.read_csv(master_path, encoding='cp1252')
    batch = pd.read_csv(batch_path)
    
    # Update master with new data
    for _, row in batch.iterrows():
        game_id = row['Game_ID']
        df.loc[df['Game_ID'] == game_id, 'Result'] = row['Result']
        df.loc[df['Game_ID'] == game_id, 'System_Pick'] = row['System_Pick']
        
    df.to_csv(master_path, index=False)
    print("✅ Batch Update Successful.")
    # Remove the batch file after processing
    os.remove(batch_path)

if __name__ == "__main__":
    batch_update_results()
