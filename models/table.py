from .card import Card
from .pack import Pack


class Table:
    def __init__(self, pack: Pack, num: int) -> None:
        self.cards: list[Card] = pack.get_cards(num)

    def __str__(self) -> str:
        return " ".join(str(card) for card in self.cards)

    def show_cards(self, num: int) -> None:
        for card in self.cards:
            if not card.is_visible():
                card.make_visible()
                num -= 1

            if num == 0:
                break

    def to_dict(self) -> dict[str, list[dict[str, str | bool | None]]]:
        return {"cards": [card.to_dict() for card in self.cards]}