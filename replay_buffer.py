import os
import pickle
import uuid

# Force the directory to a hard-coded absolute path
BUFFER_DIR = r'C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system\replay_buffer'

if not os.path.exists(BUFFER_DIR):
    os.makedirs(BUFFER_DIR)

def save_trajectory(trajectory):
    # Print the save path to console so we can see where it tries to write
    filename = os.path.join(BUFFER_DIR, f'traj_{uuid.uuid4()}.pkl')
    print(f'Attempting to save to: {filename}')
    with open(filename, 'wb') as f:
        pickle.dump(trajectory, f)
    print('File saved successfully.')
