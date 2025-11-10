from blackjack.models.deck import Deck
from blackjack.models.player import Player
from blackjack.models.dealer import Dealer
from blackjack.models.enums import GameResult, Action
from cli.cli import BlackjackCLI
from blackjack.models.config import (
    DEFAULT_CHIPS,
    DEFAULT_DECKS,
    OPENING_CARDS,
    DEALER_STAND_ON_SOFT_17,
)
from blackjack.constants import messages


class BlackjackGame:
    """Core blackjack game engine managing state and round flow."""

    def __init__(
        self, name: str, chips: float = DEFAULT_CHIPS, decks: int = DEFAULT_DECKS
    ):
        self.deck = Deck(decks)
        self.player = Player(name, chips)
        self.dealer = Dealer(DEALER_STAND_ON_SOFT_17)
        self.cli = BlackjackCLI()

    def play(self) -> None:
        """Main game entry point."""
        self.cli.show_message(messages.WELCOME)

        while self.player.has_chips:
            if not self._betting_phase():
                return

            self._setup_round()
            self._play_round()
            self._end_round()

        self.cli.show_message(messages.OUT_OF_CHIPS)

    # --- Round phases ---

    def _betting_phase(self) -> bool:
        """Prompt player for a valid bet. Returns False if the player quits."""
        while True:
            bet_str = self.cli.prompt_bet(self.player.chips)

            if bet_str == Action.QUIT.value:
                self.cli.show_message(messages.GOODBYE)
                return False

            try:
                bet = float(bet_str)
            except ValueError:
                self.cli.show_message(messages.INVALID_BET)
                continue

            try:
                self.player.place_bet(bet)
                return True
            except ValueError as e:
                self.cli.show_message(str(e))

    def _setup_round(self) -> None:
        """Prepare new round."""
        self._reset_hands()
        self._deal_opening_cards()

    def _play_round(self) -> None:
        """Handle turns."""
        self.cli.show_hands(self.player.hand, self.dealer.hand)

        if self.player.hand.is_blackjack or self.dealer.hand.is_blackjack:
            return

        if self.player.hand.can_hit:
            self._player_turn()

        if not self.player.hand.is_bust:
            self._dealer_turn()

    def _end_round(self) -> None:
        """Resolve results and show final results."""
        self.cli.show_hands(self.player.hand, self.dealer.hand, reveal_dealer=True)
        self._settle_bets(self._determine_outcome())
        self.cli.show_message(messages.CHIPS.format(self.player.chips))

    # --- Helpers ---

    def _reset_hands(self) -> None:
        """Clear both hands."""
        self.player.hand.reset()
        self.dealer.hand.reset()

    def _deal_opening_cards(self) -> None:
        """Deal two cards to both player and dealer."""
        for _ in range(OPENING_CARDS):
            self.player.hand.add_card(self.deck.draw())
            self.dealer.hand.add_card(self.deck.draw())

    # --- Turns ---

    def _player_turn(self) -> None:
        """Handle the player's decision loop."""
        while self.player.hand.can_hit:
            action = Action(
                self.cli.prompt_action(
                    can_double=self.player.can_double(),
                    can_split=self.player.can_split(),
                )
            )

            match action:
                case Action.HIT:
                    self._hit()

                case Action.STAND:
                    break

                case Action.DOUBLE if self.player.can_double():
                    self._double()
                    break

                case Action.SPLIT if self.player.can_split():
                    self._split()

                # TODO: implement quitting game
                # case Action.QUIT:
                #     self.cli.show_message(messages.QUIT_ROUND)
                #     break

                case _:
                    self.cli.show_message(messages.INVALID_CHOICE.format(action))

            self.cli.show_hands(self.player.hand, self.dealer.hand)

    def _dealer_turn(self) -> None:
        """Dealer draws according to standard rules."""
        while self.dealer.should_hit():
            self.dealer.hand.add_card(self.deck.draw())

    # --- Player actions ---

    def _hit(self) -> None:
        self.player.hand.add_card(self.deck.draw())

    def _double(self) -> None:
        self.player.double_bet()
        self.player.hand.add_card(self.deck.draw())

    def _split(self) -> None:
        # TODO: implement split logic
        self.cli.show_message(messages.SPLIT_NOT_IMPLEMENTED)

    # --- Outcome ---

    def _settle_bets(self, result: GameResult) -> None:
        """Apply bet outcome based on game result."""
        match result:
            case GameResult.PLAYER_BUST:
                message, action = messages.PLAYER_BUST, self.player.lose_bet

            case GameResult.DEALER_BUST:
                message, action = messages.DEALER_BUST, self.player.win_bet

            case GameResult.PLAYER_BLACKJACK:
                message, action = messages.PLAYER_BLACKJACK, self.player.win_blackjack

            case GameResult.DEALER_BLACKJACK:
                message, action = messages.DEALER_BLACKJACK, self.player.lose_bet

            case GameResult.BOTH_BLACKJACK:
                message, action = messages.BOTH_BLACKJACK, self.player.push_bet

            case GameResult.PUSH:
                message, action = messages.PUSH, self.player.push_bet

            case GameResult.PLAYER_WIN:
                message, action = messages.PLAYER_WIN, self.player.win_bet

            case GameResult.PLAYER_LOSE:
                message, action = messages.PLAYER_LOSE, self.player.lose_bet
        action()
        self.cli.show_message(message)

    def _determine_outcome(self) -> GameResult:
        """Compare hands and return game outcome."""
        p, d = self.player.hand, self.dealer.hand

        if p.is_bust:
            return GameResult.PLAYER_BUST

        if d.is_bust:
            return GameResult.DEALER_BUST

        if p.is_blackjack and d.is_blackjack:
            return GameResult.BOTH_BLACKJACK

        if p.is_blackjack:
            return GameResult.PLAYER_BLACKJACK

        if d.is_blackjack:
            return GameResult.DEALER_BLACKJACK

        if p.best_value == d.best_value:
            return GameResult.PUSH

        if p.best_value > d.best_value:
            return GameResult.PLAYER_WIN

        else:
            return GameResult.PLAYER_LOSE
