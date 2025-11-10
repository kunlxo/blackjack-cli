from dataclasses import dataclass


@dataclass(frozen=True)
class Card:
    """Represents a single playing card in a standard deck."""

    rank: str
    suit: str

    RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    SUITS = ["♠", "♥", "♦", "♣"]

    VALUES = {
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 10,
        "Q": 10,
        "K": 10,
        "A": 11,
    }

    @property
    def value(self) -> int:
        return self.VALUES[self.rank]

    @property
    def is_ace(self) -> bool:
        return self.rank == "A"

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

    def __repr__(self) -> str:
        return f"Card(rank={self.rank!r}, suit={self.suit!r})"
