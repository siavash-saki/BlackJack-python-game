from .hand import Hand


class Rules:
    DEALER_STAND_THRESHOLD = 17
    BLACKJACK_PAYOUT = 1.5
    STARTING_MONEY = 100

    @staticmethod
    def dealer_should_hit(hand: Hand) -> bool:
        return hand.score < Rules.DEALER_STAND_THRESHOLD

    @staticmethod
    def determine_outcome(player: Hand, dealer: Hand) -> str:
        """Returns one of: 'blackjack', 'player_bust', 'dealer_bust', 'win', 'lose', 'push'."""
        if player.is_bust:
            return "player_bust"
        if player.is_blackjack and not dealer.is_blackjack:
            return "blackjack"
        if dealer.is_blackjack and not player.is_blackjack:
            return "lose"
        if player.is_blackjack and dealer.is_blackjack:
            return "push"
        if dealer.is_bust:
            return "dealer_bust"
        if player.score > dealer.score:
            return "win"
        if dealer.score > player.score:
            return "lose"
        return "push"

    @staticmethod
    def calculate_payout(outcome: str, bet: int) -> int:
        """Returns the net change to player money."""
        if outcome == "blackjack":
            return int(bet * Rules.BLACKJACK_PAYOUT)
        if outcome in ("win", "dealer_bust"):
            return bet
        if outcome in ("lose", "player_bust"):
            return -bet
        return 0  # push
