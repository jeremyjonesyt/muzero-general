import os

def check_readiness():
    files = ['run_mission.py', 'batch_sync.py', 'automate_rewards.py', 'data/season_2026_stats.csv']
    print("--- 🚀 14-0 System: Pre-Flight Check ---")
    
    # Check for missing scripts/data
    for file in files:
        if os.path.exists(file):
            print(f"✅ Found: {file}")
        else:
            print(f"❌ Missing: {file}")
            
    # Check for batch data
    if os.path.exists('daily_results_input.csv'):
        print("💡 Status: Ready for 2 AM Sync (Batch file detected).")
    else:
        print("⚠️ Status: No batch file found. System will run diagnostics only.")

if __name__ == "__main__":
    check_readiness()
