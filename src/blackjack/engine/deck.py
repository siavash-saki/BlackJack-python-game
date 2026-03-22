import random
from .card import Card, Suit, Rank


class Deck:
    def __init__(self) -> None:
        self._cards: list[Card] = []
        self._reshuffle()

    def _reshuffle(self) -> None:
        self._cards = [
            Card(suit, rank) for suit in Suit for rank in Rank
        ]
        random.shuffle(self._cards)

    def draw(self) -> Card:
        if not self._cards:
            self._reshuffle()
        return self._cards.pop()

    @property
    def remaining(self) -> int:
        return len(self._cards)
