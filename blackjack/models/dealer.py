from blackjack.models.participant import Participant


class Dealer(Participant):
    """Represents the blackjack dealer and their drawing rules."""

    def __init__(self, stand_on_soft_17: bool = True):
        super().__init__(name="Dealer")
        self._stand_on_soft_17 = stand_on_soft_17

    def should_hit(self) -> bool:
        total = self.hand.best_value
        if total < 17:
            return True
        return total == 17 and not self._stand_on_soft_17 and self.hand.is_soft
