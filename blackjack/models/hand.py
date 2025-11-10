from blackjack.models.card import Card


class Hand:
    def __init__(self, cards: list[Card] | None = None):
        self._cards = cards.copy() if cards else []

    @property
    def cards(self) -> list[Card]:
        return self._cards.copy()

    @property
    def value(self) -> tuple[int, int]:
        total = sum(card.value for card in self._cards if not card.is_ace)
        aces = sum(1 for c in self._cards if c.is_ace)

        low = total + aces
        high = total + (aces - 1) + 11 if aces else total

        return (low, low) if high > 21 else (low, high)

    @property
    def best_value(self) -> int:
        low, high = self.value
        return high if high <= 21 else low

    @property
    def display_value(self) -> str:
        low, high = self.value
        if low == high or high > 21:
            return str(low)
        return f"{low}/{high}"

    @property
    def is_blackjack(self) -> bool:
        return len(self._cards) == 2 and self.best_value == 21

    @property
    def is_bust(self) -> bool:
        return self.best_value > 21

    @property
    def is_soft(self) -> bool:
        low, high = self.value
        return high != low and high <= 21

    @property
    def can_hit(self) -> bool:
        return self.best_value < 21

    @property
    def is_pair(self) -> bool:
        return len(self) == 2 and self._cards[0].rank == self._cards[1].rank

    def add_card(self, card: Card) -> None:
        self._cards.append(card)

    def reset(self):
        self._cards = []

    def __len__(self) -> int:
        return len(self._cards)

    def __iter__(self):
        return iter(self._cards)

    def __getitem__(self, index: int) -> Card:
        return self._cards[index]

    def __str__(self) -> str:
        return " ".join(str(card) for card in self._cards)

    def __repr__(self) -> str:
        return f"Hand(cards={self._cards!r})"
