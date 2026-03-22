"""Bridge between Flask session and GameState."""
from __future__ import annotations

import json
import random
from flask import session
from blackjack.engine import GameState, Phase, Card, Suit, Rank, Hand, Deck
from blackjack.engine.game import RoundResult


def _hand_to_json(hand: Hand) -> list:
    return [(c.suit.value, c.rank.value) for c in hand.cards]


def _hand_from_json(data: list) -> Hand:
    h = Hand()
    for suit_val, rank_val in data:
        h.add(Card(Suit(suit_val), Rank(rank_val)))
    return h


def _deck_to_json(deck: Deck) -> list:
    return [(c.suit.value, c.rank.value) for c in deck._cards]


def _deck_from_json(data: list) -> Deck:
    d = Deck.__new__(Deck)
    d._cards = [Card(Suit(s), Rank(r)) for s, r in data]
    return d


def save_game(game: GameState) -> None:
    session["game"] = {
        "deck": _deck_to_json(game.deck),
        "player": _hand_to_json(game.player),
        "dealer": _hand_to_json(game.dealer),
        "money": game.money,
        "bet": game.bet,
        "phase": game.phase.value,
        "dealer_revealed": game.dealer_revealed,
        "message": game.message,
        "result": {
            "outcome": game.result.outcome,
            "player_score": game.result.player_score,
            "dealer_score": game.result.dealer_score,
            "payout": game.result.payout,
            "bet": game.result.bet,
        } if game.result else None,
        "history": [
            {
                "outcome": r.outcome,
                "payout": r.payout,
                "bet": r.bet,
                "player_score": r.player_score,
                "dealer_score": r.dealer_score,
            }
            for r in game.history[-20:]
        ],
    }
    session.modified = True


def load_game() -> GameState:
    data = session.get("game")
    if not data:
        return GameState()

    game = GameState.__new__(GameState)
    game.deck = _deck_from_json(data["deck"])
    game.player = _hand_from_json(data["player"])
    game.dealer = _hand_from_json(data["dealer"])
    game.money = data["money"]
    game.bet = data["bet"]
    game.phase = Phase(data["phase"])
    game.dealer_revealed = data["dealer_revealed"]
    game.message = data["message"]

    if data.get("result"):
        r = data["result"]
        game.result = RoundResult(
            outcome=r["outcome"],
            player_score=r["player_score"],
            dealer_score=r["dealer_score"],
            payout=r["payout"],
            bet=r["bet"],
        )
    else:
        game.result = None

    game.history = []
    for h in data.get("history", []):
        game.history.append(RoundResult(
            outcome=h["outcome"],
            player_score=h["player_score"],
            dealer_score=h["dealer_score"],
            payout=h["payout"],
            bet=h["bet"],
        ))

    return game
