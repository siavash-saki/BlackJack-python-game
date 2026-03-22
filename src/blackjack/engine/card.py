from enum import Enum
from dataclasses import dataclass


class Suit(Enum):
    HEARTS = "hearts"
    DIAMONDS = "diamonds"
    CLUBS = "clubs"
    SPADES = "spades"

    @property
    def symbol(self) -> str:
        return {
            "hearts": "\u2665",
            "diamonds": "\u2666",
            "clubs": "\u2663",
            "spades": "\u2660",
        }[self.value]

    @property
    def is_red(self) -> bool:
        return self in (Suit.HEARTS, Suit.DIAMONDS)


class Rank(Enum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

    @property
    def display(self) -> str:
        names = {1: "A", 11: "J", 12: "Q", 13: "K"}
        return names.get(self.value, str(self.value))

    @property
    def score_value(self) -> int:
        if self.value == 1:
            return 11
        return min(self.value, 10)


@dataclass(frozen=True)
class Card:
    suit: Suit
    rank: Rank

    def to_dict(self) -> dict:
        return {
            "suit": self.suit.value,
            "rank": self.rank.value,
            "display": self.rank.display,
            "symbol": self.suit.symbol,
            "is_red": self.suit.is_red,
        }
