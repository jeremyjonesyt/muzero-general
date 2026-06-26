import os

def get_latest_loss(log_file='training_log.txt'):
    """Reads the last line of the log file to get current loss."""
    if not os.path.exists(log_file):
        return 1.0 # Default high loss if no log exists
    
    with open(log_file, 'r') as f:
        lines = f.readlines()
        if not lines:
            return 1.0
        # Assumes log format: "loss: 0.045"
        last_line = lines[-1].strip()
        try:
            return float(last_line.split(':')[-1])
        except:
            return 1.0
