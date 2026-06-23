from models import Card
import random

class Pack:
    def __init__(self):
        colors = ["Pik", "Kier", "Trefl", "Karo"]
        ranks = ["4", "5", "6", "7", "8", "9", "10", "J", "K", "Q", "A"]
        self.cards = [Card(color, rank, False) for color in colors for rank in ranks]

    def shuffle_cards(self):
        random.shuffle(self.cards)

    def get_cards(self, num):
        return [self.cards.pop() for _ in range(num)]
