from muzero.data.loader import MLBDataLoader
import pandas as pd

def test_dataloader_initialization():
    loader = MLBDataLoader()
    assert loader.name == 'MLB_Data_Loader'

def test_get_team_stats_structure():
    loader = MLBDataLoader()
    # Using 108 (Angels) as a standard test case
    stats = loader.get_team_stats(108)
    assert isinstance(stats, pd.DataFrame)
    assert not stats.empty
