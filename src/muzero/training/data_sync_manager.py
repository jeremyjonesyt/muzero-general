import pandas as pd
import os

class DataSyncManager:
    def __init__(self, base_path="data/supplemental"):
        self.base_path = base_path

    def load_all_metrics(self):
        # Load all supplemental datasets into a single combined feature map
        metrics = {
            "umpire": pd.read_csv(os.path.join(self.base_path, "umpire_history.csv")),
            "bullpen": pd.read_csv(os.path.join(self.base_path, "bullpen_index.csv")),
            "bvp": pd.read_csv(os.path.join(self.base_path, "bvp_history.csv")),
            "travel": pd.read_csv(os.path.join(self.base_path, "travel_2026.csv"))
        }
        return metrics
