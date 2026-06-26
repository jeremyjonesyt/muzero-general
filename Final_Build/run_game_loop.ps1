# Game Loop Orchestrator: DynamicGameData Processing
Write-Host "--- Initiating DynamicGameData Loop ---" -ForegroundColor Yellow

# Define game queue (You can link this to a folder of game files or a master list)
$games = Get-ChildItem -Path "C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system\data\queue\*.json"

foreach ($game in $games) {
    Write-Host "Processing Game: $(game_825070.json.Name)" -ForegroundColor Cyan
    
    # 1. Scrape Market Lines and Update DynamicGameData
    python C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system\src\muzero\env\market_scraper.py --game $game.FullName
    
    # 2. MuZero Policy Inference
    python C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system\src\muzero\inference\muzero_inference.py --data $game.FullName
    
    # 3. Decision Logic & Edge Verification
    python C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system\src\muzero\inference\edge_checker.py
    
    Write-Host "Game $(game_825070.json.Name) processed." -ForegroundColor Green
}

Write-Host "--- All Games Processed. System Standing By. ---" -ForegroundColor Yellow
