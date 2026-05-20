class Player:
    def __init__ (self, nickname, credits, ID):
        self.nickname=nickname
        self.ID=ID
        self.credits=credits
        self.bet=0
        self.allin=False
        self.fold=False

    def to_dict(self):
        return {
            "nickname": self.nickname,
            "credits": self.credits,
            "allin": self.allin,
            "fold": self.fold,
            "id": self.ID,
        }
