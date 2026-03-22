from dataclasses import dataclass, field
from .card import Card


@dataclass
class Hand:
    cards: list[Card] = field(default_factory=list)

    def add(self, card: Card) -> None:
        self.cards.append(card)

    @property
    def score(self) -> int:
        values = [c.rank.score_value for c in self.cards]
        while sum(values) > 21 and 11 in values:
            idx = values.index(11)
            values[idx] = 1
        return sum(values)

    @property
    def is_bust(self) -> bool:
        return self.score > 21

    @property
    def is_blackjack(self) -> bool:
        return len(self.cards) == 2 and self.score == 21

    def to_dict_list(self) -> list[dict]:
        return [c.to_dict() for c in self.cards]
