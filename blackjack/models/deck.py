import random
from blackjack.models.card import Card


class Deck:
    """Represents one or more shuffled decks of standard playing cards."""

    def __init__(self, num_decks: int = 1) -> None:
        if num_decks < 1:
            raise ValueError("Number of decks must be at least 1")

        self.num_decks = num_decks
        self._cards: list[Card] = []
        self._build()

    def draw(self) -> Card:
        if not self._cards:
            self._build()
        return self._cards.pop()

    def _build(self) -> None:
        self._cards = [
            Card(rank, suit)
            for _ in range(self.num_decks)
            for suit in Card.SUITS
            for rank in Card.RANKS
        ]
        random.shuffle(self._cards)

    def __len__(self) -> int:
        return len(self._cards)

    def __repr__(self) -> str:
        return f"Deck(num_decks={self.num_decks}, remaining={len(self)})"

    def __str__(self) -> str:
        return f"Deck with {len(self)} cards"
