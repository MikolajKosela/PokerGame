from pack import Pack
from card import Card

class Table:
    def __init__(self, pack, num):
        self.cards=pack.get_cards(num)

    def __str__(self):
        return " ".join(str(card) for card in self.cards)

    def show_card(self, num):
        for card in self.cards:
            if not card.isVisible():
                card.makeVisible()
                num-=1
            if num==0:
                break

    def to_dict(self):
        return {
            "cards": [card.to_dict() for card in self.cards]
        }
