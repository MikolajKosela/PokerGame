from card import Card
import random


class Pack:
    def __init__(self):
        self.cards = []
        colors = ["Pik", "Kier", "Trefl", "Karo"]
        numbers = ["4", "5", "6", "7", "8", "9", "10", "J", "K", "Q", "A"]
        for i in colors:
            for j in numbers:
                self.cards.append(Card(i, j, False))

    def shuffle_cards(self):
        random.shuffle(self.cards)

    def get_cards(self, num):
        taken_cards = []
        for _ in range(num):
            taken_cards.append(self.cards.pop())
        return taken_cards
