from muzero.training.orchestrator import TrainingOrchestrator

def main():
    print("Initializing Training Orchestrator...")
    orchestrator = TrainingOrchestrator()
    
    total_episodes = 100 
    target_team_id = 1 
    
    print(f"Starting training for {total_episodes} episodes...")
    
    try:
        for episode in range(total_episodes):
            loss, reward = orchestrator.run_full_episode(target_team_id)
            if episode % 10 == 0:
                print(f"Episode {episode} complete. Loss: {loss:.4f}, Reward: {reward:.4f}")
                
    except KeyboardInterrupt:
        print("\nTraining interrupted by user.")
    finally:
        print("Finalizing training and saving weights...")
        orchestrator.save_checkpoint("model_weights/final_production_v1.pth")
        print("Training session concluded.")

if __name__ == "__main__":
    main()
