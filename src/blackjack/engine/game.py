from __future__ import annotations

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional
from .card import Card
from .deck import Deck
from .hand import Hand
from .rules import Rules


class Phase(Enum):
    BETTING = "betting"
    PLAYER_TURN = "player_turn"
    DEALER_TURN = "dealer_turn"
    ROUND_OVER = "round_over"


@dataclass
class RoundResult:
    outcome: str
    player_score: int
    dealer_score: int
    payout: int
    bet: int


class GameState:
    def __init__(self, money: int = Rules.STARTING_MONEY) -> None:
        self.deck = Deck()
        self.player = Hand()
        self.dealer = Hand()
        self.money = money
        self.bet = 0
        self.phase = Phase.BETTING
        self.message = ""
        self.result: RoundResult | None = None
        self.history: list[RoundResult] = []
        self.dealer_revealed = False

    def place_bet(self, amount: int) -> bool:
        if self.phase != Phase.BETTING:
            return False
        if amount <= 0 or amount > self.money:
            return False
        self.bet = amount
        self._deal_initial()
        return True

    def _deal_initial(self) -> None:
        self.player = Hand()
        self.dealer = Hand()
        self.result = None
        self.dealer_revealed = False
        self.message = ""

        self.player.add(self.deck.draw())
        self.dealer.add(self.deck.draw())
        self.player.add(self.deck.draw())
        self.dealer.add(self.deck.draw())

        # Check for immediate blackjack
        if self.player.is_blackjack or self.dealer.is_blackjack:
            self._resolve_round()
        else:
            self.phase = Phase.PLAYER_TURN

    def hit(self) -> bool:
        if self.phase != Phase.PLAYER_TURN:
            return False
        self.player.add(self.deck.draw())
        if self.player.is_bust:
            self._resolve_round()
        return True

    def stand(self) -> bool:
        if self.phase != Phase.PLAYER_TURN:
            return False
        self.phase = Phase.DEALER_TURN
        self.dealer_revealed = True
        self._play_dealer()
        return True

    def dealer_draw_one(self) -> bool:
        """Draw one card for the dealer. Returns True if dealer needs more cards."""
        if self.phase != Phase.DEALER_TURN:
            return False
        if Rules.dealer_should_hit(self.dealer):
            self.dealer.add(self.deck.draw())
            if not Rules.dealer_should_hit(self.dealer) or self.dealer.is_bust:
                self._resolve_round()
                return False
            return True
        self._resolve_round()
        return False

    def _play_dealer(self) -> None:
        """Play out the entire dealer hand at once."""
        while Rules.dealer_should_hit(self.dealer):
            self.dealer.add(self.deck.draw())
        self._resolve_round()

    def _resolve_round(self) -> None:
        self.dealer_revealed = True
        outcome = Rules.determine_outcome(self.player, self.dealer)
        payout = Rules.calculate_payout(outcome, self.bet)
        self.money += payout
        self.result = RoundResult(
            outcome=outcome,
            player_score=self.player.score,
            dealer_score=self.dealer.score,
            payout=payout,
            bet=self.bet,
        )
        self.history.append(self.result)
        self.phase = Phase.ROUND_OVER

        messages = {
            "blackjack": f"BLACKJACK! You win ${abs(payout)}!",
            "win": f"You win ${abs(payout)}!",
            "dealer_bust": f"Dealer busts! You win ${abs(payout)}!",
            "lose": f"You lose ${abs(payout)}.",
            "player_bust": f"Bust! You lose ${abs(payout)}.",
            "push": "Push! Bet returned.",
        }
        self.message = messages.get(outcome, "")

    def new_round(self) -> bool:
        if self.money <= 0:
            return False
        self.phase = Phase.BETTING
        self.player = Hand()
        self.dealer = Hand()
        self.bet = 0
        self.message = ""
        self.result = None
        self.dealer_revealed = False
        return True

    def to_dict(self) -> dict:
        return {
            "phase": self.phase.value,
            "money": self.money,
            "bet": self.bet,
            "player_cards": self.player.to_dict_list(),
            "dealer_cards": self._dealer_cards_dict(),
            "player_score": self.player.score,
            "dealer_score": self.dealer.score if self.dealer_revealed else None,
            "dealer_revealed": self.dealer_revealed,
            "message": self.message,
            "result": {
                "outcome": self.result.outcome,
                "payout": self.result.payout,
            } if self.result else None,
            "history": [
                {
                    "outcome": r.outcome,
                    "payout": r.payout,
                    "bet": r.bet,
                    "player_score": r.player_score,
                    "dealer_score": r.dealer_score,
                }
                for r in self.history[-10:]
            ],
        }

    def _dealer_cards_dict(self) -> list[dict]:
        cards = []
        for i, c in enumerate(self.dealer.cards):
            if i == 1 and not self.dealer_revealed:
                cards.append({"hidden": True})
            else:
                cards.append(c.to_dict())
        return cards
