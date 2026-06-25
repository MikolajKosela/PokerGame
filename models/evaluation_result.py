class Evaluation_result:
    def __init__(self, power, comment=None, cards=None):
        self.power = power
        self.comment = comment
        self.cards = cards

    def __lt__(self, other):
        if self.power == other.power and self.power != 0:
            for card, other_card in self.cards, other.cards:
                if card != other.card:
                    return card < other_card
        else:
            return self.power < other.power
    
    def __eq__(self, other):
        if self.power == other.power:
            for card, other_card in self.cards, other.cards:
                if card != other.card:
                    return False
            return True
        else :
            return False
    
    def to_dict(self):
        return {
            "power": self.power,
            "comment": self.comment,
            "cards": self.cards
        }
    
    def __str__(self):
        result = self.comment + " -> "
        for card in self.cards:
            result += str(card) + ", "
        return result
