from card import Card
from pack import Pack
from table import Table
from player import Player
import random

class Game:
    def __init__(self):
        self.players = []
        self.tables = []
        self.token_to_player = dict()
        self.sid_to_player = dict()
        self.pack = Pack()
        self.pot = 0
        self.bet = 1
        self.round_num = -1
        self.whose_round_is = -1

    def append_player(self, nickname, credits, sid):
        # return codes: 
        # 2 -> invalid character in nick 
        # 3 -> a player with this nick exists
        if len(nickname) == 0 or not all(char.isalnum() or char == "_" for char in nickname):
            return 2
        elif any(player.nickname == nickname for player in self.players):
            return 3
        else :
            self.players.append(Player(nickname, credits, self.players_num(), sid))

    def players_num(self):
        return len(self.players) 
    
    def active_players(self):
        return [player for player in self.players if not player.fold]

    def started(self):
        return self.round_num > -1

    def start(self):
        self.pack.shuffle_cards()
        for _ in self.players:
            self.tables.append(Table(self.pack, 2))
        self.tables.append(Table(self.pack, 5))
        self.whose_round_is = 0
        self.round_num = 0

    def is_end(self):
        return self.round_num == 10

    def end(self):
        self.round_num = 10
        for table in self.tables:
            table.show_cards(5)
        self.whose_round_is = -2

    def next_round(self):
        self.whose_round_is = 0

        call_needed = False
        if (
            self.round_num % 2 == 0 
            and any(player.bet < self.bet for player in self.players)
            ):
            call_needed = True

        if not call_needed:
            for player in self.players:
                player.bet = 0
            self.bet = 0

        # Jeżeli wszyscy gracze wyrównali swoje zaklady, to
        # można pominąć turę wyrównywania 
        if not call_needed and self.round_num % 2 == 0:
            self.round_num += 1
        self.round_num += 1

        # 0 Wchodzenie i podbijanie wejściowego zakładu
        # 1 Wyrównywanie do zakładu wejścia
        # 2 Pokazanie kart graczy i przyjmowanie zakładów 
        # 3 Wyrównywanie/ czekanie
        # 4 Odkrycie 3 kart i przyjmowanie zakładów 
        # 5 Wyrównywanie/ czekanie
        # 6 Odkrycie karty i przyjmowanie zakładów
        # 7 Wyrównywanie/ czekanie
        # 8 Odkrycie karty i przyjmowanie zakładów 
        # 9 Wyrównywanie/ czekanie
        # 10 Podsumowanie i wybór zwycięzców

        # Odkryj karty na stosach graczy
        # (z pominięciem ostatniego [:-1], wspólnego stołu)
        if self.round_num == 2:
            for table in self.tables[:-1]:
                table.show_cards(2)

        # Odkryj trzy wspólne karty
        elif self.round_num == 4:
            self.tables[-1].show_cards(3)

        # Odkryj po jednej wspólnej karcie
        elif self.round_num == 6 or self.round_num == 8:
            self.tables[-1].show_cards(1)

        # Zakończ rozgrywkę
        elif self.round_num == 10:
            return self.end()

    def next_player(self):
        self.whose_round_is += 1
        if self.whose_round_is >= len(self.players):
            return self.next_round()
            
    # pdata = player's data
    def can_i_check(self, sid):
        pdata = self.players[self.sid_to_player[sid]]

        if pdata.allin or self.bet == pdata.bet:
            return 1
        return 0

    def can_i_bet(self, sid):
        pdata = self.players[self.sid_to_player[sid]]

        if not pdata.allin and self.round_num % 2 == 0 and self.bet == 0 and pdata.credits > 0:
            return 1
        return 0

    def can_i_call(self, sid):
        pdata = self.players[self.sid_to_player[sid]]
        cost = self.bet - pdata.bet

        if not pdata.allin and self.bet > pdata.bet and pdata.credits >= cost:
            return 1
        return 0

    def can_i_raise(self, sid):
        pdata = self.players[self.sid_to_player[sid]]

        if not pdata.allin and self.round_num % 2 == 0 and self.bet > 0 and pdata.credits > self.bet:
            return 1
        return 0

    def can_i_fold(self, sid):
        pdata = self.players[self.sid_to_player[sid]]

        if not pdata.allin:
            return 1
        return 0

    def can_i_allin(self, sid):
        pdata = self.players[self.sid_to_player[sid]]

        if not pdata.allin and pdata.credits > 0 and (self.round_num % 2 == 0 or self.bet > pdata.bet):
            return 1
        return 0

    def check(self, sid):
        pdata = self.players[self.sid_to_player[sid]]

        if self.can_i_check(sid):
            return self.next_player()
        else:
            return 2

    def make_bet(self, sid, amount):
        pdata = self.players[self.sid_to_player[sid]]

        if self.can_i_bet(sid) and amount > 0 and pdata.credits >= amount:
            pdata.credits -= amount
            pdata.bet += amount

            self.pot += amount
            self.bet = amount
            return self.next_player()
        else:
            return 2

    def call(self, sid):
        pdata = self.players[self.sid_to_player[sid]]
        cost = self.bet - pdata.bet

        if self.can_i_call(sid):
            pdata.credits -= cost
            pdata.bet += cost

            self.pot += cost
            return self.next_player()
        else:
            return 2

    def raiseBet(self, sid, amount):
        pdata = self.players[self.sid_to_player[sid]]
        cost = self.bet - pdata.bet

        if self.can_i_raise(sid) and amount > 0 and pdata.credits >= cost + amount:
            pdata.credits -= amount + cost
            pdata.bet += amount + cost

            self.pot += amount + cost
            self.bet += amount
            return self.next_player()
        else:
            return 2

    def fold(self, sid):
        pdata = self.players[self.sid_to_player[sid]]

        if self.can_i_fold(sid):
            pdata.fold = True
            if len(self.active_players()) <= 1:
                return self.end()
            return self.next_player()
        else:
            return 2

    def allin(self, sid):
        pdata = self.players[self.sid_to_player[sid]]
        amount = pdata.credits
        cost = self.bet - pdata.bet

        if self.can_i_allin(sid):
            pdata.allin = True
            pdata.credits = 0
            pdata.bet += amount

            self.pot += amount
            self.bet += amount - cost
            return self.next_player()
        else:
            return 2

    def again(self):
        self.round_num = 0
        self.tables = []
        self.bet = 1
        self.pack = Pack()

        for player in self.players:
            player.bet = 0
            player.allin = False
            player.fold = False
        return self.start()
