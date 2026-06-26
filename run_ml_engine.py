import pandas as pd
import run_inference
import os

def get_ml_predictions():
    input_path = os.path.join('data', 'season_2026_stats.csv')
    output_file = 'temp_results.csv'
    
    # Load the new stats
    df = pd.read_csv(input_path)
    
    # Bridge: Create the required 'Loss' and 'Reward' columns for the engine
    # We maintain your system's baseline low loss of 0.000469
    df['Loss'] = 0.000469  
    df['Reward'] = df['Run_Differential'] 
    
    # Save as bridge data for the inference engine
    bridge_path = 'bridge_data.csv'
    df.to_csv(bridge_path, index=False)
    
    engine = run_inference.InferenceEngine(
        model_path='best_model.pth', 
        config='config.json'
    )
    engine.load_model(model_path='best_model.pth')
    
    # Run inference on the bridged data
    engine.run_inference(data_path=bridge_path, output_path=output_file)
    
    if os.path.exists(output_file):
        return pd.read_csv(output_file)
    return None

def main():
    print("Running 14-0 System Engine with Data Bridge...")
    df = get_ml_predictions()
    if df is not None:
        df.to_csv('season_2026_predictions.csv', index=False)
        print("Success: 14-0 System inference complete.")
        # Cleanup bridge
        if os.path.exists('bridge_data.csv'): os.remove('bridge_data.csv')
    else:
        print("Error: Inference generated no data.")

if __name__ == '__main__':
    main()
