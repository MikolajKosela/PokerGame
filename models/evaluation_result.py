from .card import Card


class EvaluationResult:
    def __init__(
        self,
        power: int,
        comment: str = "",
        cards: list[Card] | None = None,
    ) -> None:
        self.power = power
        self.comment = comment
        self.cards = cards if cards is not None else []

    def __lt__(self, other: "EvaluationResult") -> bool:
        if self.power != other.power:
            return self.power < other.power

        if self.power == 0:
            return False

        for card, other_card in zip(self.cards, other.cards):
            if card != other_card:
                return card < other_card

        return False

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, EvaluationResult):
            return NotImplemented

        if self.power != other.power:
            return False

        return self.cards == other.cards

    def to_dict(self) -> dict[str, int | str | list[dict[str, str | bool | None]]]:
        return {
            "power": self.power,
            "comment": self.comment,
            "cards": [card.to_dict() for card in self.cards],
        }

    def __str__(self) -> str:
        cards = ", ".join(str(card) for card in self.cards)
        return f"{self.comment} -> {cards}"