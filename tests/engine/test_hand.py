from blackjack.engine.card import Suit, Rank, Card
from blackjack.engine.hand import Hand


def _card(rank: Rank, suit: Suit = Suit.SPADES) -> Card:
    return Card(suit, rank)


def test_empty_hand():
    h = Hand()
    assert h.score == 0
    assert h.is_bust is False
    assert h.is_blackjack is False


def test_simple_score():
    h = Hand([_card(Rank.FIVE), _card(Rank.THREE)])
    assert h.score == 8


def test_face_cards():
    h = Hand([_card(Rank.KING), _card(Rank.QUEEN)])
    assert h.score == 20


def test_ace_as_eleven():
    h = Hand([_card(Rank.ACE), _card(Rank.NINE)])
    assert h.score == 20


def test_blackjack():
    h = Hand([_card(Rank.ACE), _card(Rank.KING)])
    assert h.score == 21
    assert h.is_blackjack is True


def test_21_not_blackjack_with_three_cards():
    h = Hand([_card(Rank.SEVEN), _card(Rank.SEVEN), _card(Rank.SEVEN)])
    assert h.score == 21
    assert h.is_blackjack is False


def test_ace_demotion():
    h = Hand([_card(Rank.ACE), _card(Rank.EIGHT), _card(Rank.FIVE)])
    # 11 + 8 + 5 = 24 -> ace becomes 1 -> 14
    assert h.score == 14


def test_double_ace_demotion():
    h = Hand([_card(Rank.ACE), _card(Rank.ACE), _card(Rank.NINE)])
    # 11 + 11 + 9 = 31 -> first ace 1 -> 21 exactly
    assert h.score == 21


def test_bust():
    h = Hand([_card(Rank.KING), _card(Rank.QUEEN), _card(Rank.FIVE)])
    assert h.score == 25
    assert h.is_bust is True


def test_add_card():
    h = Hand()
    h.add(_card(Rank.TWO))
    h.add(_card(Rank.THREE))
    assert h.score == 5
    assert len(h.cards) == 2
