import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import torch
from models import MuZeroNetwork
from games.mlb_betting import MuZeroConfig

app = FastAPI(title="MuZero Sports Analytics Engine")

# =====================================================================
# 📊 DATA SCHEMAS
# =====================================================================
class DynamicGameData(BaseModel):
    away_team: str
    home_team: str
    away_fatigue: float
    home_fatigue: float
    away_pitcher_era: float
    home_pitcher_era: float
    market_line: float

class NpbGameData(BaseModel):
    away_team: str
    home_team: str
    away_fatigue: float
    home_fatigue: float
    away_pitcher_era: float
    home_pitcher_era: float
    market_line: float

class NbaGameData(BaseModel):
    away_team: str
    home_team: str
    away_fatigue: float
    home_fatigue: float
    away_offensive_rating: float
    home_defensive_rating: float
    market_line: float

class EsportsGameData(BaseModel):
    away_team: str
    home_team: str
    away_offensive_rating: float
    home_defensive_rating: float
    market_line: float
    total_line: float 

class TennisGameData(BaseModel):
    player_1: str          
    player_2: str          
    p1_surface_win_pct: float  
    p2_surface_win_pct: float  
    p1_fatigue_index: float    
    p2_fatigue_index: float    
    market_line: float         

# =====================================================================
# 🧠 MODEL INITIALIZATION
# =====================================================================
config = MuZeroConfig()
network = MuZeroNetwork(config)
network.eval()

def logits_to_probabilities(logits):
    flat_logits = logits.flatten()
    exp_logits = np.exp(flat_logits - np.max(flat_logits))
    return exp_logits / np.sum(exp_logits)

# =====================================================================
# 1. MLB ENDPOINT
# =====================================================================
@app.post("/muzero_predict")
async def get_prediction(data: DynamicGameData):
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
        policy_logits = policy_logits_tensor.cpu().numpy()
        probabilities = logits_to_probabilities(policy_logits)
        away_prob = float(probabilities[0].item() * 100)
        home_prob = float(probabilities[1].item() * 100)
        recommended_action = f"Bet on {data.away_team}" if away_prob > home_prob else f"Bet on {data.home_team}"
        return {
            "status": "success",
            "sport": "MLB (Baseball)",
            "matchup": f"{data.away_team} @ {data.home_team}",
            f"{data.away_team}_win_probability": away_prob,
            f"{data.home_team}_win_probability": home_prob,
            "recommended_action": recommended_action
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# =====================================================================
# 2. NPB ENDPOINT
# =====================================================================
@app.post("/muzero_predict_npb")
async def get_npb_prediction(data: NpbGameData):
    try:
        tensor_input = np.array([[[data.away_fatigue, data.home_fatigue, data.away_pitcher_era, data.home_pitcher_era, data.market_line]]], dtype="float32")
        observation = torch.as_tensor(tensor_input)
        with torch.no_grad():
            value, reward, policy_logits_tensor, hidden_state = network.initial_inference(observation)
        policy_logits = policy_logits_tensor.cpu().numpy()
        probabilities = logits_to_probabilities(policy_logits)
        away_prob = float(probabilities[0].item() * 100)
        home_prob = float(probabilities[1].item() * 100)
        recommended_action = f"Bet on {data.away_team}" if away_prob > home_prob else f"Bet on {data.home_team}"
        return {"status": "success", "sport": "NPB", "matchup": f"{data.away_team} @ {data.home_team}", f"{data.away_team}_win_probability": away_prob, f"{data.home_team}_win_probability": home_prob, "recommended_action": recommended_action}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

# =====================================================================
# 3. NBA ENDPOINT
# =====================================================================
@app.post("/muzero_predict_nba")
async def get_nba_prediction(data: NbaGameData):
    try:
        tensor_input = np.array([[[data.away_fatigue, data.home_fatigue, data.away_offensive_rating, data.home_defensive_rating, data.market_line]]], dtype="float32")
        observation = torch.as_tensor(tensor_input)
        with torch.no_grad():
            value, reward, policy_logits_tensor, hidden_state = network.initial_inference(observation)
        policy_logits = policy_logits_tensor.cpu().numpy()
        probabilities = logits_to_probabilities(policy_logits)
        away_prob = float(probabilities[0].item() * 100)
        home_prob = float(probabilities[1].item() * 100)
        recommended_action = f"Bet on {data.away_team}" if away_prob > home_prob else f"Bet on {data.home_team}"
        return {"status": "success", "sport": "NBA", "matchup": f"{data.away_team} @ {data.home_team}", f"{data.away_team}_win_probability": away_prob, f"{data.home_team}_win_probability": home_prob, "recommended_action": recommended_action}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

# =====================================================================
# 4. ESPORTS ENDPOINT
# =====================================================================
@app.post("/muzero_predict_esports")
async def get_esports_prediction(data: EsportsGameData):
    try:
        tensor_input = np.array([[[0.0, 0.0, data.away_offensive_rating, data.home_defensive_rating, data.market_line]]], dtype="float32")
        observation = torch.as_tensor(tensor_input)
        with torch.no_grad():
            value, reward, policy_logits_tensor, hidden_state = network.initial_inference(observation)
        policy_logits = policy_logits_tensor.cpu().numpy()
        probabilities = logits_to_probabilities(policy_logits)
        away_prob = float(probabilities[0].item() * 100)
        home_prob = float(probabilities[1].item() * 100)
        recommended_action = f"Bet on {data.away_team}" if away_prob > home_prob else f"Bet on {data.home_team}"
        return {"status": "success", "sport": "Esports", "matchup": f"{data.away_team} @ {data.home_team}", f"{data.away_team}_win_probability": away_prob, f"{data.home_team}_win_probability": home_prob, "recommended_action": recommended_action}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

# =====================================================================
# 5. TENNIS ENDPOINT
# =====================================================================
@app.post("/muzero_predict_tennis")
async def get_tennis_prediction(data: TennisGameData):
    try:
        tensor_input = np.array([[[data.p1_fatigue_index, data.p2_fatigue_index, data.p1_surface_win_pct, data.p2_surface_win_pct, data.market_line]]], dtype="float32")
        observation = torch.as_tensor(tensor_input)
        with torch.no_grad():
            value, reward, policy_logits_tensor, hidden_state = network.initial_inference(observation)
        policy_logits = policy_logits_tensor.cpu().numpy()
        probabilities = logits_to_probabilities(policy_logits)
        p1_prob = float(probabilities[0].item() * 100)
        p2_prob = float(probabilities[1].item() * 100)
        recommended_action = f"Bet on {data.player_1}" if p1_prob > p2_prob else f"Bet on {data.player_2}"
        return {"status": "success", "sport": "Tennis", "matchup": f"{data.player_1} vs {data.player_2}", f"{data.player_1}_win_probability": p1_prob, f"{data.player_2}_win_probability": p2_prob, "recommended_action": recommended_action}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)