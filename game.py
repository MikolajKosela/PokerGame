from card import Card
from pack import Pack
from table import Table
from player import Player

from result import Result

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
        self.last_round_skipped = False

    def append_player(self, nickname, credits, sid):
        if len(nickname) == 0 :
            return Result(False, "Invalid data", "Nick nie moży być pusty")
        elif not all(char.isalnum() or char == "_" for char in nickname):
            return Result(False,  "Invalid data", "Nick może składać się z tylko z znaków a-z, 0-9, _")
        elif any(player.nickname == nickname for player in self.players):
            return Result(False, "Invalid query", "Gracz o takim nicku istnieje")
        else :
            self.players.append(Player(nickname, credits, self.players_num(), sid))
            return Result(True)

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
        self.last_round_skipped = False

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
            self.last_round_skipped = True
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
        while True:
            self.whose_round_is += 1
            if self.whose_round_is >= self.players_num():
                return self.next_round()

            player = self.players[self.whose_round_is]
            player.last_round_skipped = False

            if player.can_skip_round(self):
                player.last_round_skipped = True
            else:
                break
  
    def check(self, sid):
        player = self.players[self.sid_to_player[sid]]

        if player.can_check(self):
            return self.next_player()
        else:
            return 2

    def make_bet(self, sid, amount):
        player = self.players[self.sid_to_player[sid]]

        if player.can_bet(self) and amount > 0 and player.credits >= amount:
            player.credits -= amount
            player.bet += amount

            self.pot += amount
            self.bet = amount
            return self.next_player()
        else:
            return 2

    def call(self, sid):
        player = self.players[self.sid_to_player[sid]]
        cost = self.bet - player.bet

        if player.can_call(self):
            player.credits -= cost
            player.bet += cost

            self.pot += cost
            return self.next_player()
        else:
            return 2

    def raiseBet(self, sid, amount):
        player = self.players[self.sid_to_player[sid]]
        cost = self.bet - player.bet

        if player.can_raise(self) and amount > 0 and player.credits >= cost + amount:
            player.credits -= amount + cost
            player.bet += amount + cost

            self.pot += amount + cost
            self.bet += amount
            return self.next_player()
        else:
            return 2

    def fold(self, sid):
        player = self.players[self.sid_to_player[sid]]

        if player.can_fold(self):
            player.fold = True
            if len(self.active_players()) <= 1:
                return self.end()
            return self.next_player()
        else:
            return 2

    def allin(self, sid):
        player = self.players[self.sid_to_player[sid]]
        amount = player.credits
        cost = self.bet - player.bet

        if player.can_allin(self):
            player.allin = True
            player.credits = 0
            player.bet += amount

            self.pot += amount
            self.bet += amount - cost
            return self.next_player()
        else:
            return 2

    def again(self):
        self.round_num = 0
        self.tables = []
        self.bet = 1
        self.last_round_skipped = False
        self.pack = Pack()

        for player in self.players:
            player.bet = 0
            player.allin = False
            player.fold = False
        return self.start()
