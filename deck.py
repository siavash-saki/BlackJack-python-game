"""Deck helpers for the Blackjack game."""

from random import choice
from typing import List, Tuple

CardSpec = Tuple[str, int]


def new_deck() -> List[CardSpec]:
    """Create a fresh deck of cards."""
    return [(suit, value) for suit in ["heart", "spade", "club", "diamond"] for value in range(1, 14)]


def pick_a_card(deck: List[CardSpec]) -> CardSpec:
    """Pick a card from the deck, replenishing it if empty."""
    if not deck:
        deck.extend(new_deck())

    card_suit_num = choice(deck)
    deck.remove(card_suit_num)
    return card_suit_num
