#Tester for hand evaluator
from game.hand_evaluator import evaluate_hand, print_result
from models import Card

def test():
    a = Card("Trefl", "8")
    b = Card("Trefl", "9")
    c = Card("Karo", "4")
    d = Card("Karo", "7")
    e = Card("Kier", "K")
    f = Card("Karo", "Q")
    g = Card("Trefl", "A")
    cards = [a, b, c, d, e, f, g]

    print_result(evaluate_hand(cards))
    
test()
    