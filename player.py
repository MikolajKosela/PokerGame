class Player:
    def __init__(self, nickname, credits, ID, sid):
        self.nickname = nickname
        self.ID = ID
        self.sid = sid
        self.credits = credits
        self.bet = 0
        self.allin = False
        self.fold = False
    
    def can_check(self, game):
        return (self.allin or self.bet == game.bet)
    
    def can_bet(self, game):
        return (
            not self.allin
            and game.round_num % 2 == 0
            and game.bet == 0
            and self.credits > 0
        )
    
    def can_call(self, game):
        cost = game.bet - self.bet
        return (
            not self.allin
            and game.bet > self.bet
            and self.credits >= cost
        )

    def can_raise(self, game):
        return (
            not self.allin 
            and game.round_num % 2 == 0
            and game.bet > 0
            and self.credits > self.bet
        )
    
    def can_fold(self, game):
        return (not self.allin)

    def can_allin(self, game):
        return (
            not self.allin
            and self.credits > 0
            and (
                game.round_num % 2 == 0
                or game.bet > self.bet + self.credits
            )
        )

    def to_dict(self):
        return {
            "nickname": self.nickname,
            "credits": self.credits,
            "allin": self.allin,
            "fold": self.fold,
            "id": self.ID,
        }
