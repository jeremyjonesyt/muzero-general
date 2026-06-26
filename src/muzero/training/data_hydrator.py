import json
import pandas as pd

class MLBDataHydrator:
    def __init__(self, historical_data_path):
        self.df = pd.read_csv(historical_data_path)
        
    def hydrate_game_state(self, game_json):
        # Extracts seasonal regression features
        park_factor = self.df.get('park_factor', 1.0)
        pitcher_regression = self.df.get('pitcher_era_regression', 3.5)
        return [park_factor, pitcher_regression]
