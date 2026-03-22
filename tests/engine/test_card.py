from blackjack.engine.card import Suit, Rank, Card


def test_suit_symbols():
    assert Suit.HEARTS.symbol == "\u2665"
    assert Suit.SPADES.symbol == "\u2660"
    assert Suit.CLUBS.symbol == "\u2663"
    assert Suit.DIAMONDS.symbol == "\u2666"


def test_suit_color():
    assert Suit.HEARTS.is_red is True
    assert Suit.DIAMONDS.is_red is True
    assert Suit.SPADES.is_red is False
    assert Suit.CLUBS.is_red is False


def test_rank_display():
    assert Rank.ACE.display == "A"
    assert Rank.TWO.display == "2"
    assert Rank.TEN.display == "10"
    assert Rank.JACK.display == "J"
    assert Rank.QUEEN.display == "Q"
    assert Rank.KING.display == "K"


def test_rank_score():
    assert Rank.ACE.score_value == 11
    assert Rank.TWO.score_value == 2
    assert Rank.TEN.score_value == 10
    assert Rank.JACK.score_value == 10
    assert Rank.QUEEN.score_value == 10
    assert Rank.KING.score_value == 10


def test_card_frozen():
    c = Card(Suit.HEARTS, Rank.ACE)
    assert c.suit == Suit.HEARTS
    assert c.rank == Rank.ACE


def test_card_to_dict():
    c = Card(Suit.SPADES, Rank.KING)
    d = c.to_dict()
    assert d["suit"] == "spades"
    assert d["rank"] == 13
    assert d["display"] == "K"
    assert d["symbol"] == "\u2660"
    assert d["is_red"] is False
