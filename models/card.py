class Card:
    def __init__(self, color, rank, visibility=True):
        self.color = color
        self.rank = rank 
        self.visibility = visibility

    def __lt__(self, other):
        return self.get_value() < other.get_value()

    def __eq__(self, other):
        return self.get_value() == other.get_value()

    def get_value(self):
        match self.rank:
            case "J":
                return 11
            case "Q":
                return 12
            case "K":
                return 13
            case "A":
                return 14
            case _:
                return int(self.rank)
    
    def color_to_number(self):
        match self.color:
            case "Pik":
                return 0
            case "Kier":
                return 1
            case "Karo":
                return 2
            case "Trefl":
                return 3
            case _:
                return -1

    def is_visible(self):
        return self.visibility

    def make_visible(self):
        self.visibility = True

    def __str__(self):
        if self.visibility:
            symbol = None
            match self.color:
                case "Pik":
                    symbol = "♠"
                case "Kier":
                    symbol = "♥"
                case "Karo":
                    symbol = "♦"
                case "Trefl":
                    symbol = "♣"
                case _:
                    symbol = self.color
            return symbol + " " + self.rank
        else:
            return "???"

    def to_dict(self):
        return {
            "color": self.color if self.visibility else None,
            "rank": self.rank if self.visibility else None,
            "visible": self.visibility,
        }
