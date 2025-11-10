from blackjack.models.participant import Participant


class Player(Participant):
    """Represents a player with betting capabilities."""

    def __init__(self, name: str, chips: float = 1000.0):
        super().__init__(name)
        if chips < 0:
            raise ValueError("Chips must be a non-negative number.")
        self._chips = float(chips)
        self._bet = 0.0

    @property
    def chips(self) -> float:
        return self._chips

    @property
    def bet(self) -> float:
        return self._bet

    @property
    def has_chips(self) -> bool:
        return self._chips > 0

    def place_bet(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Bet must be a positive number.")
        if amount > self._chips:
            raise ValueError("Insufficient chips.")
        self._chips -= amount
        self._bet = amount

    def double_bet(self) -> None:
        if not self.can_double():
            raise ValueError("Cannot double.")
        self._chips -= self._bet
        self._bet *= 2

    def _payout(self, multiplier: float = 1.0) -> None:
        self._chips += self._bet * multiplier
        self._bet = 0.0

    def win_bet(self) -> None:
        self._payout(2.0)

    def win_blackjack(self) -> None:
        self._payout(2.5)

    def push_bet(self) -> None:
        self._payout(1.0)

    def lose_bet(self) -> None:
        self._payout(0.0)

    def can_double(self) -> bool:
        """Check if player can double down (enough chips and first two cards)."""
        return len(self.hand) == 2 and self._chips >= self._bet

    def can_split(self) -> bool:
        """Check if player can split (enough chips and pair)."""
        return self.hand.is_pair and self._chips >= self._bet
