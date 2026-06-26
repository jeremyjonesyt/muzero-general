import pandas as pd
import torch
import os

def parse_game_to_tensor(csv_path="daily_results_input.csv"):
    df = pd.read_csv(csv_path)
    mapping = pd.read_csv("team_mapping.csv")
    mapping_dict = dict(zip(mapping['external_name'], mapping['internal_id']))

    # Use mapping to set IDs; default to -1 if not found
    df['away_id'] = df['away_name'].map(mapping_dict).fillna(-1)
    df['home_id'] = df['home_name'].map(mapping_dict).fillna(-1)
    
    # Fill remaining required features
    df['home_adv'] = 1.0
    df['away_streak'] = 0.0
    df['home_streak'] = 0.0
    
    features = df[['away_id', 'home_id', 'home_adv', 'away_streak', 'home_streak']].values
    return torch.tensor(features, dtype=torch.float32)
