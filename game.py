"""Core Blackjack game loop and supporting helpers."""

from sys import exit
from time import sleep

from art import text2art

from cards import Empty_space, Hidden_card, card
from deck import new_deck, pick_a_card


def display_banner() -> None:
    """Display the game banner."""
    print(100 * "\n")
    welcome = text2art("Welcome")
    to = text2art(10 * " " + "to")
    blackjack = text2art(20 * " " + "Black Jack")
    print(welcome + to + blackjack)


def prompt_ready() -> None:
    """Prompt the user to start the game."""
    print("You play against the computer dealer.\nYour starting money is = 100$")

    while True:
        ready_or_not = input("\n\n Are you ready to Play? (y/n) ")

        if ready_or_not == "y":
            break
        if ready_or_not == "n":
            exit("\n\n   ------ Come back when you are ready! ------ \n\n")
        print('\nPlease chose only "y" or "n"!')

    print(100 * "\n")


def score(hand):
    score_list = []
    for card_obj in hand:
        score_list.append(card_obj.card_score())
    while sum(score_list) > 21 and 11 in score_list:
        score_list.remove(11)
        score_list.append(1)
    return sum(score_list)


def print_hand(hand):
    print_list = []

    for x in range(4):
        print_row = []
        for card_obj in hand:
            print_row.append(card_obj.card_image()[x])
        print_list.append(print_row)

    for row in print_list:
        rendered_row = ""
        for column in row:
            rendered_row += column
        print(rendered_row)


def print_table(dealer, player, player_money, bet):
    print(100 * "\n")
    print(" " * 10, "Dealer's hand: ")
    print_hand(dealer)
    print(f"\n\n Money: {player_money}$\n BET: {bet}$\n Your Hand:")
    print_hand(player)


def prompt_bet(player_money):
    while True:
        try:
            print(f"\nBank :{player_money}$")
            bet = int(input("\nPlace your bet: "))
        except ValueError:
            print("Please place a valid bet")
            continue

        if bet <= 0:
            print("Please place a valid bet")
            continue
        if bet <= player_money:
            return bet

        print(f"You don't have enough money to bet {bet}$")


def run_game():
    display_banner()
    prompt_ready()

    player_money = 100
    game_deck = new_deck()

    while player_money > 0:
        bet = prompt_bet(player_money)
        player = [card(pick_a_card(game_deck)), card(pick_a_card(game_deck))]
        dealer = [Empty_space(), card(pick_a_card(game_deck)), Hidden_card()]

        while True:
            print_table(dealer, player, player_money, bet)
            player_score = score(player)

            if player_score == 21:
                print(f"\nBLACKJACK! You just won {bet}$!")
                player_money += bet
                break

            if player_score > 21:
                print(f"\nBUST! You just lost {bet}$!")
                player_money -= bet
                break

            while True:
                request = input("\nHit or Stand: ")
                if request.lower() in ["hit", "stand", "h", "s"]:
                    break
                print("Please enter only Hit or Stand!!!\n")

            if request.lower() in ["hit", "h"]:
                player.append(card(pick_a_card(game_deck)))
                continue

            if request.lower() in ["stand", "s"]:
                dealer.pop()
                dealer.append(card(pick_a_card(game_deck)))

                while True:
                    sleep(1)
                    print_table(dealer, player, player_money, bet)
                    dealer_score = score(dealer)

                    if dealer_score > 21:
                        sleep(1)
                        print(f"\nYou just won {bet}$!")
                        player_money += bet
                        break

                    if 16 < dealer_score == player_score:
                        sleep(1)
                        print("\nPUSH!")
                        break

                    if dealer_score > player_score:
                        sleep(1)
                        print(f"\nYou just lost {bet}$!")
                        player_money -= bet
                        break

                    dealer.append(card(pick_a_card(game_deck)))

            break

    print(text2art("YOU    LOST!"))


if __name__ == "__main__":
    run_game()
