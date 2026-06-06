class Card:
    def __init__(self, color, number, visibility):
        self.color = color
        self.number = number
        self.visibility = visibility

    def isVisible(self):
        return self.visibility

    def makeVisible(self):
        self.visibility = True

    def __str__(self):
        if self.visibility:
            return f"{self.color} {self.number}"
        else:
            return f"???"

    def to_dict(self):
        return {
            "color": self.color if self.visibility else None,
            "number": self.number if self.visibility else None,
            "visible": self.visibility,
        }
