import random
import numpy as np
import torch
from fastapi import FastAPI, HTTPException
from app.routers import nba  # Your new NBA router
# Ensure these imports match your actual project paths:
from app.schemas.mlb_data import MLBGameData 

app = FastAPI(title="MuZero Multi-Sport Engine")

# --- NBA ROUTER REGISTRATION ---
# This adds the NBA track without touching MLB
app.include_router(nba.router, prefix="/nba", tags=["NBA"])

# --- EXISTING MLB PREDICTION ENDPOINT (UNCHANGED) ---
@app.post("/mlb_predict")
async def get_mlb_prediction(data: MLBGameData):
    try:
        # 1. Run your existing MuZero inference
        tensor_input = np.array([[[data.away_pitcher_era, data.home_pitcher_era, 
                                   data.travel_distance_km, data.market_line]]], dtype="float32")
        observation = torch.as_tensor(tensor_input)
        
        with torch.no_grad():
            _, _, policy_logits_tensor, _ = network.initial_inference(observation)
        
        policy_logits = policy_logits_tensor.numpy()[0]
        exp_logits = np.exp(policy_logits - np.max(policy_logits))
        probabilities = exp_logits / np.sum(exp_logits)
        
        # 2. Add Stochastic Variance (The "Chaos Factor")
        variance = random.uniform(-0.07, 0.07)
        home_prob = (probabilities[1] + variance) * 100
        away_prob = 100 - home_prob
        
        # 3. Constrain probabilities
        home_prob = max(20.0, min(80.0, home_prob))
        away_prob = 100 - home_prob
        
        recommended_target = data.home_team if home_prob > away_prob else data.away_team
        
        return {
            "status": "success",
            "matchup": f"{data.away_team} @ {data.home_team}",
            f"{data.away_team}_win_probability": round(away_prob, 2),
            f"{data.home_team}_win_probability": round(home_prob, 2),
            "recommended_action": f"Bet on {recommended_target}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))