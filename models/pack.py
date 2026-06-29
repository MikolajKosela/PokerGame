import random

from .card import Card


class Pack:
    def __init__(self) -> None:
        colors = ["Pik", "Kier", "Trefl", "Karo"]
        ranks = ["4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

        self.cards: list[Card] = [
            Card(color, rank, False)
            for color in colors
            for rank in ranks
        ]

    def shuffle_cards(self) -> None:
        random.shuffle(self.cards)

    def get_cards(self, num: int) -> list[Card]:
        return [self.cards.pop() for _ in range(num)]