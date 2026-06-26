import statsapi

try:
    print('Testing connection to MLB Stats API...')
    mariners = statsapi.lookup_team('Mariners')
    print(f'Connection Successful! Data retrieved: {mariners}')
except Exception as e:
    print(f'Connection failed: {e}')
