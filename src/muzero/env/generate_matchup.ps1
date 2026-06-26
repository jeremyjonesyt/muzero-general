param(
    [string]$away,
    [string]$home_team,
    [float]$awayFatigue,
    [float]$homeFatigue,
    [float]$awayERA,
    [float]$homeERA,
    [float]$line
)

$data = [PSCustomObject]@{
    away_team = $away
    home_team = $home_team
    away_fatigue = $awayFatigue
    home_fatigue = $homeFatigue
    away_pitcher_era = $awayERA
    home_pitcher_era = $homeERA
    market_line = $line
}

$fullPath = "C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system\data\queue\" + $away + "_vs_" + $home_team + ".json"
$data | ConvertTo-Json | Set-Content $fullPath
Write-Host "Matchup data generated: $fullPath" -ForegroundColor Green
