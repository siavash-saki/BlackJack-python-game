from flask import Blueprint, render_template, request
from .state import load_game, save_game
from blackjack.engine import Phase

bp = Blueprint("game", __name__)


def _render_table(game):
    return render_template("partials/table.html", game=game.to_dict())


@bp.route("/")
def index():
    game = load_game()
    save_game(game)
    return render_template("base.html", game=game.to_dict())


@bp.route("/bet", methods=["POST"])
def bet():
    game = load_game()
    try:
        amount = int(request.form.get("amount", 0))
    except (ValueError, TypeError):
        amount = 0

    if not game.place_bet(amount):
        game.message = "Invalid bet."

    save_game(game)
    return _render_table(game)


@bp.route("/hit", methods=["POST"])
def hit():
    game = load_game()
    game.hit()
    save_game(game)
    return _render_table(game)


@bp.route("/stand", methods=["POST"])
def stand():
    game = load_game()
    game.stand()
    save_game(game)
    return _render_table(game)


@bp.route("/new-round", methods=["POST"])
def new_round():
    game = load_game()
    if not game.new_round():
        game.message = "Game over! Reset to play again."
    save_game(game)
    return _render_table(game)


@bp.route("/reset", methods=["POST"])
def reset():
    from blackjack.engine import GameState
    game = GameState()
    save_game(game)
    return _render_table(game)
