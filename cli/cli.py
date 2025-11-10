import os
import platform
from blackjack.models.hand import Hand
from blackjack.constants.messages import (
    INVALID_CHOICE,
    BET_PROMPT,
)


class BlackjackCLI:
    """Command-line interface for Blackjack game."""

    CLEAR_CMD = "cls" if platform.system() == "Windows" else "clear"
    TITLE = "🂡  BLACKJACK  🂮"
    WIDTH = 45
    SEP = "="

    def __init__(self):
        self.clear_screen()

    def clear_screen(self):
        os.system(self.CLEAR_CMD)

    def show_message(self, message: str) -> None:
        print(message)

    def show_hands(
        self, player_hand: Hand, dealer_hand: Hand, reveal_dealer: bool = False
    ) -> None:
        self.clear_screen()
        self.show_header()
        self.show_dealer(dealer_hand, reveal_dealer)
        self.show_player(player_hand, reveal_dealer)
        self.show_footer()

    def prompt_bet(self, max_bet: float) -> str:
        bet_input = input(BET_PROMPT.format(max_bet=max_bet)).strip().lower()
        if bet_input in ("q", "quit"):
            return "quit"
        return bet_input

    def prompt_action(self, can_double: bool = False, can_split: bool = False) -> str:
        options = ["(h)it", "(s)tand"]
        if can_double:
            options.append("(d)ouble")
        if can_split:
            options.append("s(p)lit")
        # options.append("(q)uit")

        while True:
            choice = input(" | ".join(options) + ": ").strip().lower()
            match choice:
                case "h" | "hit":
                    return "hit"
                case "s" | "stand":
                    return "stand"
                case "d" | "double" if can_double:
                    return "double"
                case "p" | "split" if can_split:
                    return "split"
                # case "q" | "quit":
                #     return "quit"
                case _:
                    print(INVALID_CHOICE.format(choice))

    def show_header(self):
        print(self.SEP * self.WIDTH)
        print(self.TITLE.center(self.WIDTH))
        print(self.SEP * self.WIDTH)

    def show_dealer(self, dealer_hand: Hand, reveal_dealer: bool):
        cards = f"{dealer_hand}" if reveal_dealer else f"{dealer_hand.cards[0]} ??"
        value = f"{dealer_hand.best_value}" if reveal_dealer else ""
        print(self.format_hand_line("Dealer: ", cards, value))

    def show_player(self, player_hand: Hand, reveal_dealer: bool):
        cards = f"{player_hand}"
        value = (
            f"{player_hand.best_value}" if reveal_dealer else player_hand.display_value
        )
        print(self.format_hand_line("Player: ", cards, value))

    def show_footer(self):
        print(self.SEP * self.WIDTH)

    def format_hand_line(self, label: str, cards: str, value: str) -> str:
        label_cards = f"{label}{cards}"
        space_width = max(self.WIDTH - len(label_cards) - len(value), 1)
        return f"{label_cards}{' ' * space_width}{value}"
