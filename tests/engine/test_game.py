from blackjack.engine.game import GameState, Phase
from blackjack.engine.rules import Rules


def test_initial_state():
    g = GameState()
    assert g.money == 100
    assert g.phase == Phase.BETTING


def test_place_bet():
    g = GameState()
    assert g.place_bet(25) is True
    assert g.bet == 25
    assert len(g.player.cards) == 2
    assert len(g.dealer.cards) == 2
    # Phase should be player_turn or round_over (if blackjack)
    assert g.phase in (Phase.PLAYER_TURN, Phase.ROUND_OVER)


def test_bet_too_large():
    g = GameState(money=50)
    assert g.place_bet(100) is False
    assert g.phase == Phase.BETTING


def test_bet_zero():
    g = GameState()
    assert g.place_bet(0) is False


def test_bet_negative():
    g = GameState()
    assert g.place_bet(-10) is False


def test_hit_adds_card():
    g = GameState()
    g.place_bet(10)
    if g.phase == Phase.PLAYER_TURN:
        initial_count = len(g.player.cards)
        g.hit()
        assert len(g.player.cards) == initial_count + 1


def test_stand_reveals_dealer():
    g = GameState()
    g.place_bet(10)
    if g.phase == Phase.PLAYER_TURN:
        g.stand()
        assert g.dealer_revealed is True
        assert g.phase == Phase.ROUND_OVER


def test_new_round():
    g = GameState()
    g.place_bet(10)
    # Play through to completion
    if g.phase == Phase.PLAYER_TURN:
        g.stand()
    assert g.phase == Phase.ROUND_OVER
    assert g.new_round() is True
    assert g.phase == Phase.BETTING


def test_game_over_no_money():
    g = GameState(money=10)
    g.place_bet(10)
    if g.phase == Phase.PLAYER_TURN:
        g.stand()
    if g.money <= 0:
        assert g.new_round() is False


def test_history_recorded():
    g = GameState()
    g.place_bet(10)
    if g.phase == Phase.PLAYER_TURN:
        g.stand()
    assert len(g.history) == 1
    assert g.history[0].bet == 10


def test_to_dict():
    g = GameState()
    d = g.to_dict()
    assert d["phase"] == "betting"
    assert d["money"] == 100
    assert isinstance(d["history"], list)


def test_blackjack_payout():
    """Blackjack should pay 3:2."""
    assert Rules.calculate_payout("blackjack", 10) == 15
    assert Rules.calculate_payout("blackjack", 20) == 30


def test_win_payout():
    assert Rules.calculate_payout("win", 10) == 10
    assert Rules.calculate_payout("dealer_bust", 10) == 10


def test_lose_payout():
    assert Rules.calculate_payout("lose", 10) == -10
    assert Rules.calculate_payout("player_bust", 10) == -10


def test_push_payout():
    assert Rules.calculate_payout("push", 10) == 0
