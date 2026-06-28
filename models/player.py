from game.round_state import is_betting_round

class Player:
    def __init__(self, nickname, credits, ID, sid):
        self.nickname = nickname
        self.ID = ID
        self.sid = sid
        self.credits = credits
        self.bet = 0
        self.allin = False
        self.fold = False
        self.last_round_skipped = False
        self.result = None
    
    def can_check(self, game):
        return (
            not self.allin
            and not self.fold
            and self.bet == game.bet 
        )
    
    def can_bet(self, game):
        return (
            not self.allin
            and not self.fold
            and is_betting_round(game.round)
            and game.bet == 0
            and self.credits > 0
        )
    
    def can_call(self, game):
        cost = game.bet - self.bet
        return (
            not self.allin
            and not self.fold
            and game.bet > self.bet
            and self.credits >= cost
        )

    def can_raise(self, game):
        return (
            not self.allin 
            and not self.fold
            and is_betting_round(game.round)
            and game.bet > 0
            and self.credits > self.bet + game.bet
        )
    
    def can_fold(self, game):
        return (
            not self.allin
        )

    def can_allin(self, game):
        return (
            not self.allin
            and not self.fold
            and self.credits > 0
            and (
                is_betting_round(game.round)
                or game.bet > self.bet + self.credits
            )
        )
    
    def can_skip_round(self, game):
        return (
            not self.can_bet(game)
            and not self.can_call(game)
            and not self.can_raise(game)
            and not self.can_allin(game)
        )
    
    def is_admin(self, game):
        return self.ID == game.adminID

    def to_dict(self):
        return {
            "nickname": self.nickname,
            "credits": self.credits,
            "allin": self.allin,
            "fold": self.fold,
            "id": self.ID,
        }
