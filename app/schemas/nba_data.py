from pydantic import BaseModel, Field

class NbaGameData(BaseModel):
    away_team: str
    home_team: str
    away_is_b2b: bool = Field(..., description="True if away team played yesterday")
    home_is_b2b: bool = Field(..., description="True if home team played yesterday")
    away_net_rating: float = Field(..., description="Offensive minus Defensive Rating")
    home_net_rating: float = Field(..., description="Offensive minus Defensive Rating")
    pace_factor: float
    market_line: float