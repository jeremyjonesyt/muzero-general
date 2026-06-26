import pandas as pd
import statsapi

class MLBDataLoader:
    def __init__(self):
        self.name = 'MLB_Data_Loader'

    def get_team_stats(self, team_id):
        """Fetches basic team information using statsapi."""
        try:
            team_data = statsapi.get('team', {'teamId': team_id})
            return pd.DataFrame([team_data])
        except Exception as e:
            return pd.DataFrame({'error': [str(e)]})
