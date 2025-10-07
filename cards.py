"""Card representations for the Blackjack game."""

from termcolor import colored


class card:
    """Represents a single playing card."""

    def __init__(self, card_suit_num):
        self.card_suit, self.card_num = card_suit_num[0], card_suit_num[1]

    def card_score(self):
        if self.card_num == 1:
            return 11
        if self.card_num > 10:
            return 10
        return self.card_num

    def card_num_image(self):
        if self.card_num == 1:
            return "A "
        if self.card_num == 10:
            return "10"
        if self.card_num == 11:
            return "J "
        if self.card_num == 12:
            return "Q "
        if self.card_num == 13:
            return "K "
        return str(self.card_num) + " "

    def card_suit_image(self):
        if self.card_suit == "heart":
            return b"\xe2\x99\xa5".decode("utf-8", "ignore")
        if self.card_suit == "spade":
            return b"\xe2\x99\xa0".decode("utf-8", "ignore")
        if self.card_suit == "club":
            return b"\xe2\x99\xa3".decode("utf-8", "ignore")
        if self.card_suit == "diamond":
            return b"\xe2\x99\xa6".decode("utf-8", "ignore")
        return ""

    def card_image(self):
        num_image = self.card_num_image()
        suit_image = self.card_suit_image()

        if self.card_suit in ["heart", "diamond"]:
            r1 = colored("  _____ ", "red")
            r2 = colored(" |     |", "red")
            r3 = colored(f" |{num_image}  {suit_image}|", "red")
            r4 = colored(" |_____|", "red")
        else:
            r1 = "  _____ "
            r2 = " |     |"
            r3 = f" |{num_image}  {suit_image}|"
            r4 = " |_____|"

        return [r1, r2, r3, r4]

    def __str__(self):
        str_of_card = ""
        for line in self.card_image():
            str_of_card += line + "\n"
        return str(str_of_card)


class Hidden_card:
    """Represents the dealer's hidden card placeholder."""

    card_num = 0

    def card_image(self):
        r1 = "  _____ "
        r2 = " |     |"
        r3 = " |     |"
        r4 = " |_____|"
        return [r1, r2, r3, r4]


class Empty_space:
    """Represents an empty spot on the table."""

    card_num = 0

    def card_image(self):
        r1 = r2 = r3 = r4 = 10 * " "
        return [r1, r2, r3, r4]

    def card_score(self):
        return 0
