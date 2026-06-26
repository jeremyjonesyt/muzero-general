import os

def apply_reward_normalization(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    # Add the import if not present
    import_stmt = 'from src.muzero.utils.reward_scaler import normalize_reward'
    if import_stmt not in content:
        content = import_stmt + '\n' + content

    # Replace the standard reward assignment with the normalized one
    # Note: This looks for common patterns; check your file after running!
    new_content = content.replace('reward = environment.step(action)', 
                                  'reward = normalize_reward(environment.step(action))')
    
    with open(file_path, 'w') as f:
        f.write(new_content)
    print(f'Successfully updated {file_path}. Please verify the changes manually.')

if __name__ == '__main__':
    target = input('Enter the path to your training file (e.g., train.py): ')
    if os.path.exists(target):
        apply_reward_normalization(target)
    else:
        print('File not found.')
