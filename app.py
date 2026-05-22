from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(
    title="MuZero Sports Analytics Engine",
    description="Global predictive engine covering North American Pro Leagues, International Baseball, and College Sports.",
    version="2.2.0"
)

# ==========================================
# 📊 LEAGUE SCHEMAS (DATA INPUT PATTERNS)
# ==========================================

class MLBPredictionInput(BaseModel):
    away_team: str = Field(..., examples=["Atlanta Braves"])
    home_team: str = Field(..., examples=["Miami Marlins"])
    away_pitcher_era: float = Field(..., description="Starting pitcher ERA", examples=[4.20])
    home_pitcher_era: float = Field(..., description="Starting pitcher ERA", examples=[3.57])
    away_fatigue: float = Field(default=0.0, examples=[0.0])
    home_fatigue: float = Field(default=0.0, examples=[0.0])
    market_line: float = Field(default=-110, examples=[-115.0])

class NPBPredictionInput(BaseModel):
    away_team: str = Field(..., examples=["Yomiuri Giants"])
    home_team: str = Field(..., examples=["Hanshin Tigers"])
    away_pitcher_era: float = Field(..., description="NPB Starting Pitcher ERA", examples=[2.45])
    home_pitcher_era: float = Field(..., description="NPB Starting Pitcher ERA", examples=[2.10])
    travel_distance_km: float = Field(default=0.0, description="Travel strain across Japan islands", examples=[450.0])
    market_line: float = Field(default=-110, examples=[-110.0])

class KBOPredictionInput(BaseModel):
    away_team: str = Field(..., examples=["Doosan Bears"])
    home_team: str = Field(..., examples=["SSG Landers"])
    away_pitcher_era: float = Field(..., description="KBO Starting Pitcher ERA", examples=[4.85])
    home_pitcher_era: float = Field(..., description="KBO Starting Pitcher ERA", examples=[3.92])
    foreigner_pitcher_bonus: bool = Field(default=False, description="Is the starting pitcher an elite foreign import?", examples=[True])
    market_line: float = Field(default=-110, examples=[-105.0])

class NBAPredictionInput(BaseModel):
    away_team: str = Field(..., examples=["Boston Celtics"])
    home_team: str = Field(..., examples=["Los Angeles Lakers"])
    away_offensive_rating: float = Field(default=118.4, examples=[118.4])
    home_offensive_rating: float = Field(default=115.6, examples=[115.6])
    away_fatigue: float = Field(default=0.0, description="1.0 if back-to-back night", examples=[0.0])
    home_fatigue: float = Field(default=0.0, description="1.0 if back-to-back night", examples=[1.0])
    market_line: float = Field(default=-110, examples=[-110.0])

class NCAABPredictionInput(BaseModel):
    away_team: str = Field(..., examples=["Duke Blue Devils"])
    home_team: str = Field(..., examples=["North Carolina Tar Heels"])
    away_coaching_rank: int = Field(default=1, description="Scale of 1-5 (5 being Elite tier)", examples=[4])
    home_coaching_rank: int = Field(default=1, description="Scale of 1-5 (5 being Elite tier)", examples=[5])
    home_court_crowd_factor: float = Field(default=1.0, description="Crowd intensity rating (1.0 to 3.0)", examples=[2.5])
    market_line: float = Field(default=-110, examples=[-110.0])

class NFLPredictionInput(BaseModel):
    away_team: str = Field(..., examples=["Kansas City Chiefs"])
    home_team: str = Field(..., examples=["San Francisco 49ers"])
    away_rest_advantage: int = Field(default=0, description="Days of rest difference", examples=[3])
    home_rest_advantage: int = Field(default=0, description="Days of rest difference", examples=[0])
    market_line: float = Field(default=-110, examples=[-110.0])

class EBasketballPredictionInput(BaseModel):
    away_gamer: str = Field(..., description="Name/Handle of the away player", examples=["Gamer_Alpha"])
    home_gamer: str = Field(..., description="Name/Handle of the home player", examples=["Gamer_Prime"])
    away_gamer_winrate: float = Field(..., description="Gamer's recent win %", examples=[64.5])
    home_gamer_winrate: float = Field(..., description="Gamer's recent win %", examples=[58.2])
    away_selected_team: str = Field(default="2023 Lakers", examples=["2023 Lakers"])
    home_selected_team: str = Field(default="2016 Warriors", examples=["2016 Warriors"])
    simulation_difficulty: str = Field(default="HallOfFame", examples=["HallOfFame"])
    market_line: float = Field(default=-110, examples=[-110.0])


# ==========================================
# 🎯 DEDICATED ENGINE ROUTES (SWAGGER TAGS)
# ==========================================

@app.post("/predict/mlb", summary="MLB Game Predictor", tags=["⚾ Major League Baseball"])
async def predict_mlb(data: MLBPredictionInput):
    away_prob = 0.50 - (data.away_pitcher_era * 0.02) + (data.home_pitcher_era * 0.02) - (data.away_fatigue * 0.02)
    away_prob = max(0.01, min(0.99, away_prob))
    home_prob = 1.0 - away_prob
    recommended = data.away_team if away_prob > home_prob else data.home_team
    return {"status": "success", "matchup": f"{data.away_team} @ {data.home_team}", "predictions": {f"{data.away_team}_win_probability": round(away_prob * 100, 2), f"{data.home_team}_win_probability": round(home_prob * 100, 2)}, "recommended_action": f"Bet on {recommended}"}

@app.post("/predict/npb", summary="Japan NPB Game Predictor", tags=["🏯 International Baseball - NPB"])
async def predict_npb(data: NPBPredictionInput):
    # NPB is a lower run-scoring environment, ERAs are weighted heavily. Travel strain added.
    away_prob = 0.50 - (data.away_pitcher_era * 0.04) + (data.home_pitcher_era * 0.04) - (data.travel_distance_km * 0.00005)
    away_prob = max(0.01, min(0.99, away_prob))
    home_prob = 1.0 - away_prob
    recommended = data.away_team if away_prob > home_prob else data.home_team
    return {"status": "success", "league": "Nippon Professional Baseball", "matchup": f"{data.away_team} @ {data.home_team}", "predictions": {f"{data.away_team}_win_probability": round(away_prob * 100, 2), f"{data.home_team}_win_probability": round(home_prob * 100, 2)}, "recommended_action": f"Bet on {recommended}"}

@app.post("/predict/kbo", summary="Korea KBO Game Predictor", tags=["🐯 International Baseball - KBO"])
async def predict_kbo(data: KBOPredictionInput):
    # KBO is high-scoring. Foreign tier-1 pitching imports heavily alter math models.
    away_prob = 0.49 - (data.away_pitcher_era * 0.015) + (data.home_pitcher_era * 0.015)
    if data.foreigner_pitcher_bonus:
        away_prob += 0.05
    away_prob = max(0.01, min(0.99, away_prob))
    home_prob = 1.0 - away_prob
    recommended = data.away_team if away_prob > home_prob else data.home_team
    return {"status": "success", "league": "Korea Baseball Organization", "matchup": f"{data.away_team} @ {data.home_team}", "predictions": {f"{data.away_team}_win_probability": round(away_prob * 100, 2), f"{data.home_team}_win_probability": round(home_prob * 100, 2)}, "recommended_action": f"Bet on {recommended}"}

@app.post("/predict/nba", summary="NBA Game Predictor", tags=["🏀 National Basketball Association"])
async def predict_nba(data: NBAPredictionInput):
    away_prob = 0.48 - (data.away_fatigue * 0.06) + (data.home_fatigue * 0.04) + (data.away_offensive_rating - data.home_offensive_rating) * 0.012
    away_prob = max(0.01, min(0.99, away_prob))
    home_prob = 1.0 - away_prob
    recommended = data.away_team if away_prob > home_prob else data.home_team
    return {"status": "success", "matchup": f"{data.away_team} @ {data.home_team}", "predictions": {f"{data.away_team}_win_probability": round(away_prob * 100, 2), f"{data.home_team}_win_probability": round(home_prob * 100, 2)}, "recommended_action": f"Bet on {recommended}"}

@app.post("/predict/ncaa-basketball", summary="NCAA Men's Basketball Predictor", tags=["🎓 College Sports - NCAA Basketball"])
async def predict_ncaab(data: NCAABPredictionInput):
    # College leans heavily on home court atmosphere and tactical coaching advantages
    away_prob = 0.44 - (data.home_court_crowd_factor * 0.03) + (data.away_coaching_rank - data.home_coaching_rank) * 0.02
    away_prob = max(0.01, min(0.99, away_prob))
    home_prob = 1.0 - away_prob
    recommended = data.away_team if away_prob > home_prob else data.home_team
    return {"status": "success", "league": "NCAA Men's Basketball", "matchup": f"{data.away_team} @ {data.home_team}", "predictions": {f"{data.away_team}_win_probability": round(away_prob * 100, 2), f"{data.home_team}_win_probability": round(home_prob * 100, 2)}, "recommended_action": f"Bet on {recommended}"}

@app.post("/predict/nfl", summary="NFL Game Predictor", tags=["🏈 National Football League"])
async def predict_nfl(data: NFLPredictionInput):
    away_prob = 0.49 + (data.away_rest_advantage * 0.015) - (data.home_rest_advantage * 0.015)
    away_prob = max(0.01, min(0.99, away_prob))
    home_prob = 1.0 - away_prob
    recommended = data.away_team if away_prob > home_prob else data.home_team
    return {"status": "success", "matchup": f"{data.away_team} @ {data.home_team}", "predictions": {f"{data.away_team}_win_probability": round(away_prob * 100, 2), f"{data.home_team}_win_probability": round(home_prob * 100, 2)}, "recommended_action": f"Bet on {recommended}"}

@app.post("/predict/ebasketball", summary="eBasketball Simulation Predictor", tags=["🎮 Esports - eBasketball"])
async def predict_ebasketball(data: EBasketballPredictionInput):
    gamer_diff = (data.away_gamer_winrate - data.home_gamer_winrate) / 100.0
    away_prob = 0.50 + gamer_diff
    if data.simulation_difficulty.lower() == "halloffame":
        away_prob *= 0.98
    away_prob = max(0.01, min(0.99, away_prob))
    home_prob = 1.0 - away_prob
    recommended = data.away_gamer if away_prob > home_prob else data.home_gamer
    return {"status": "success", "esport": "eBasketball Simulation", "matchup": f"{data.away_gamer} ({data.away_selected_team}) @ {data.home_gamer} ({data.home_selected_team})", "predictions": {f"{data.away_gamer}_win_probability": round(away_prob * 100, 2), f"{data.home_gamer}_win_probability": round(home_prob * 100, 2)}, "recommended_action": f"Bet on {recommended}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)