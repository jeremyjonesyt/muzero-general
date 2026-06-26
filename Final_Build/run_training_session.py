import sys
# Set path for imports BEFORE the package import
sys.path.append(r"C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system\src")

from muzero.training.orchestrator import TrainingOrchestrator

if __name__ == "__main__":
    print("Orchestrator loaded successfully. Starting training loop...")
    orchestrator = TrainingOrchestrator()
    
    # Run 100 training episodes
    for i in range(100):
        print(f"Running episode {i+1}...")
        orchestrator.run_full_episode(team_id=0)
