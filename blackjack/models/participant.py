from blackjack.models.hand import Hand


class Participant:
    """Base class for any blackjack participant (player or dealer)."""

    def __init__(self, name: str):
        if not name.strip():
            raise ValueError("Name must be a non-empty string.")
        self._name = name
        self._hand = Hand()

    @property
    def name(self) -> str:
        return self._name

    @property
    def hand(self) -> Hand:
        return self._hand

    def __str__(self) -> str:
        return f"{self._name}: {self._hand} ({self._hand.best_value})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self._name!r}, hand={self._hand!r})"
