import pandas as pd
import json
import os

# AUTOMATED DATA INGESTION
# This script automatically detects the data folder in the current directory
def get_system_data():
    base_path = os.path.join(os.getcwd(), 'data')
    data = {}
    try:
        with open(os.path.join(base_path, 'MLB_Schedule.json'), 'r') as f:
            data['schedule'] = json.load(f)
        data['averages'] = pd.read_csv(os.path.join(base_path, 'League_Averages_2026.csv'))
        data['hfa'] = pd.read_csv(os.path.join(base_path, 'Stadium_HFA_Key.csv'))
        data['records'] = pd.read_csv(os.path.join(base_path, 'system_records.csv'))
        data['perf'] = pd.read_csv(os.path.join(base_path, 'Performance_History.csv'))
        print('System Ready: All data streams loaded.')
    except Exception as e:
        print(f'Error loading system: {e}')
    return data

# Automatically load into a global variable if this script is executed
system_data = get_system_data()
