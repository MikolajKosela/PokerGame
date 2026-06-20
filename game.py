from card import Card
from pack import Pack
from table import Table
from player import Player
import random

class Game:
    def __init__(self):
        self.players = []
        self.tables = []
        self.tokenToPlayer = dict()
        self.sidToPlayer = dict()
        self.pack = Pack()
        self.pot = 0
        self.bet = 1
        self.playersNum = 0
        self.roundNum = 0
        self.isEnd = False
        self.whoseRoundIs = -1

    def start(self):
        self.pack.shuffle_cards()
        for _ in self.players:
            self.tables.append(Table(self.pack, 2))
        self.tables.append(Table(self.pack, 5))
        self.whoseRoundIs = 0

    def end(self):
        self.isEnd = True
        self.whoseRoundIs = -2

    def nextRound(self):
        self.whoseRoundIs = 0

        callNeded = False
        if (
            self.roundNum % 2 == 0 
            and any(player.bet < self.bet for player in self.players)
            ):
            callNeded = True

        if not callNeded:
            for player in self.players:
                player.bet = 0
            self.bet = 0

        #Jeżeli wszyscy gracze wyrównali swoje zaklady, to
        #można pominąć turę wyrównywania 
        if not callNeded and self.roundNum % 2 == 0:
            self.roundNum += 1
        self.roundNum += 1

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

        #Odkryj karty na stosach graczy
        #(z pominięciem ostatniego [:-1], wspólnego stołu)
        if self.roundNum == 2:
            for table in self.tables[:-1]:
                for card in table.cards:
                    card.makeVisible()

        #Odkryj trzy wspólne karty
        elif self.roundNum == 4:
            for i in range(0, 3):
                self.tables[-1].cards[i].makeVisible()

        #Odkryj po jednej wspólnej karcie
        elif self.roundNum == 6 or self.roundNum == 8:
            self.tables[-1].cards[int(self.roundNum / 2)].makeVisible()

        #Zakończ rozgrywkę
        elif self.roundNum == 10:
            return self.end()

    def nextPlayer(self):
        self.whoseRoundIs += 1
        if self.whoseRoundIs >= len(self.players):
            return self.nextRound()

    def canICheck(self, sid):
        playerData = self.players[self.sidToPlayer[sid]]

        if playerData.allin or self.bet == playerData.bet:
            return 1
        return 0

    def canIBet(self, sid):
        playerData = self.players[self.sidToPlayer[sid]]

        if not playerData.allin and self.roundNum % 2 == 0 and self.bet == 0 and playerData.credits > 0:
            return 1
        return 0

    def canICall(self, sid):
        playerData = self.players[self.sidToPlayer[sid]]
        cost = self.bet - playerData.bet

        if not playerData.allin and self.bet > playerData.bet and playerData.credits >= cost:
            return 1
        return 0

    def canIRaise(self, sid):
        playerData = self.players[self.sidToPlayer[sid]]

        if not playerData.allin and self.roundNum % 2 == 0 and self.bet > 0 and playerData.credits > self.bet:
            return 1
        return 0

    def canIFold(self, sid):
        playerData = self.players[self.sidToPlayer[sid]]

        if not playerData.allin:
            return 1
        return 0

    def canIAllin(self, sid):
        playerData = self.players[self.sidToPlayer[sid]]

        if not playerData.allin and playerData.credits > 0 and (self.roundNum % 2 == 0 or self.bet > playerData.bet):
            return 1
        return 0

    def check(self, sid):
        playerData = self.players[self.sidToPlayer[sid]]

        if self.canICheck(sid):
            return self.nextPlayer()
        else:
            return 2

    def makeBet(self, sid, amount):
        playerData = self.players[self.sidToPlayer[sid]]

        if self.canIBet(sid) and amount > 0 and playerData.credits >= amount:
            playerData.credits -= amount
            playerData.bet += amount

            self.pot += amount
            self.bet = amount
            return self.nextPlayer()
        else:
            return 2

    def call(self, sid):
        playerData = self.players[self.sidToPlayer[sid]]
        cost = self.bet - playerData.bet

        if self.canICall(sid):
            playerData.credits -= cost
            playerData.bet += cost

            self.pot += cost
            return self.nextPlayer()
        else:
            return 2

    def raiseBet(self, sid, amount):
        playerData = self.players[self.sidToPlayer[sid]]
        cost = self.bet - playerData.bet

        if self.canIRaise(sid) and amount > 0 and playerData.credits >= cost + amount:
            playerData.credits -= amount + cost
            playerData.bet += amount + cost

            self.pot += amount + cost
            self.bet += amount
            return self.nextPlayer()
        else:
            return 2

    def fold(self, sid):
        playerData = self.players[self.sidToPlayer[sid]]

        if self.canIFold(sid):
            playerData.fold = True
            self.playersNum -= 1

            if self.playersNum <= 1:
                for table in self.tables:
                    table.show_card(len(table.cards))
                return self.end()
            return self.nextPlayer()
        else:
            return 2

    def allin(self, sid):
        playerData = self.players[self.sidToPlayer[sid]]
        amount = playerData.credits
        cost = self.bet - playerData.bet

        if self.canIAllin(sid):
            playerData.allin = True
            playerData.credits = 0
            playerData.bet += amount

            self.pot += amount
            self.bet += amount - cost
            return self.nextPlayer()
        else:
            return 2

    def again(self):
        self.roundNum = 0
        self.tables = []
        self.bet = 1
        self.pack = Pack()
        self.isEnd = False
        for player in self.players:
            player.bet = 0
            player.allin = False
            player.fold = False
        return self.start()
