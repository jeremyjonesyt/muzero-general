import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import torch
import os

# Try importing your custom deep learning weights, fallback if the files are moving folders
try:
    from models import MuZeroNetwork
    from games.mlb_betting import MuZeroConfig
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False

app = FastAPI(title="MuZero Sports Analytics Engine")

class DynamicGameData(BaseModel):
    away_team: str
    home_team: str
    away_fatigue: float
    home_fatigue: float
    away_pitcher_era: float
    home_pitcher_era: float
    market_line: float

# Initialize network if configurations exist locally
if CONFIG_AVAILABLE:
    try:
        config = MuZeroConfig()
        network = MuZeroNetwork(config)
    except Exception as e:
        network = None
else:
    network = None

@app.post("/muzero_predict")
async def get_prediction(data: DynamicGameData):
    # Error protection path if your deep learning models folder isn't matching pathing
    if not CONFIG_AVAILABLE or network is None:
        raise HTTPException(
            status_code=500, 
            detail="MuZero Model weights or modules ('models' / 'games') not found in this desktop directory. Please verify your folder placement."
        )
        
    try:
        tensor_input = np.array([[[
            data.away_fatigue, 
            data.home_fatigue, 
            data.away_pitcher_era, 
            data.home_pitcher_era,
            data.market_line
        ]]], dtype="float32")
        
        observation = torch.as_tensor(tensor_input)
        
        with torch.no_grad():
            value, reward, policy_logits_tensor, hidden_state = network.initial_inference(observation)
        
        policy_logits = policy_logits_tensor.numpy()[0]
        
        exp_logits = np.exp(policy_logits - np.max(policy_logits))
        probabilities = exp_logits / np.sum(exp_logits)
        
        away_prob = float(round(probabilities[0] * 100, 2))
        home_prob = float(round(probabilities[1] * 100, 2))
        
        recommended_target = data.away_team if away_prob > home_prob else data.home_team
        
        return {
            "status": "success",
            "matchup": f"{data.away_team} @ {data.home_team}",
            f"{data.away_team}_win_probability": away_prob,
            f"{data.home_team}_win_probability": home_prob,
            "recommended_action": f"Bet on {recommended_target}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8005)