# Tuned MuZero Flywheel Stability Profiles
LEARNING_RATE = 2e-4         # Dropping further to prevent the 30+ initial loss spikes
VALUE_LOSS_COEFF = 0.25      # Scale value updates down so they don't overpower representation
GRAD_CLIP_NORM = 0.5         # Strict clipping barrier to eliminate late-burst explosions
EXPERT_SEEDS = 20            # Anchor heavily on stable expert steps
EXPLORATORY_SEEDS = 10       # Keep noise minimal
