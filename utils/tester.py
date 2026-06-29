from game.hand_evaluator import evaluate_hand, print_result
from models import Card


def test_hand_evaluator() -> None:
    cards = [
        Card("Trefl", "8"),
        Card("Trefl", "9"),
        Card("Karo", "4"),
        Card("Karo", "7"),
        Card("Kier", "K"),
        Card("Karo", "Q"),
        Card("Trefl", "A"),
    ]

    print_result(evaluate_hand(cards))


if __name__ == "__main__":
    test_hand_evaluator()