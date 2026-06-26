class BankrollManager:
    def __init__(self, total_bankroll=1000):
        self.total = total_bankroll
    
    def get_ev(self, true_prob, decimal_odds):
        # EV = (True_Win_Prob * Payout) - Stake
        payout = decimal_odds  # Decimal odds already include stake
        return (true_prob * payout) - 1.0
    
    def calculate_bet(self, true_prob, decimal_odds):
        # Only bet if EV > 0
        if self.get_ev(true_prob, decimal_odds) <= 0:
            return 0
        
        b = decimal_odds - 1
        fraction = (true_prob * b - (1 - true_prob)) / b
        return max(0, min(0.2, fraction)) * self.total
