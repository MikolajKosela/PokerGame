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
        if self.roundNum % 2 == 0:
            for player in self.players:
                if player.bet < self.bet:
                    callNeded = True
                    break

        if not callNeded:
            for player in self.players:
                player.bet = 0
            self.bet = 0

        if not callNeded and self.roundNum % 2 == 0:
            self.roundNum += 1
        self.roundNum += 1

        # 0 Wchodzenie i podbijanie wejścia
        # 1 Wyrównywanie wejścia
        # 2 Pokazanie kart graczy i betowanie
        # 3 Sprawdzanie/czekanie
        # 4 Odkrycie 3 kart i betowanie
        # 5 Sprawdzanie/czekanie
        # 6 Odkrycie karty i betowanie
        # 7 Sprawdzanie/czekanie
        # 8 Odkrycie karty i betowanie
        # 9 Sprawdzanie/czekanie
        # 10 Podsumowanie

        if self.roundNum == 2:
            for i in range(0, len(self.players)):
                for card in self.tables[i].cards:
                    card.makeVisible()
        elif self.roundNum == 4:
            for i in range(0, 3):
                self.tables[-1].cards[i].makeVisible()
        elif self.roundNum == 6 or self.roundNum == 8:
            self.tables[-1].cards[int(self.roundNum / 2)].makeVisible()

        if self.roundNum == 10:
            return self.end()

    def nextPlayer(self):
        self.whoseRoundIs += 1
        if self.whoseRoundIs >= len(self.players):
            return self.nextRound()

    def check(self, sid):
        return self.nextPlayer()

    def makeBet(self, sid, amount):
        playerData = self.players[self.sidToPlayer[sid]]
        if playerData.credits >= amount and amount > 0:
            playerData.credits -= amount
            playerData.bet += amount
            self.pot += amount
            self.bet = amount
            return self.nextPlayer()

    def call(self, sid):
        playerData = self.players[self.sidToPlayer[sid]]
        cost = self.bet - playerData.bet
        print(cost)
        if playerData.credits >= cost:
            playerData.credits -= cost
            playerData.bet += cost
            self.pot += cost
            return self.nextPlayer()

    def raiseBet(self, sid, amount):
        playerData = self.players[self.sidToPlayer[sid]]
        cost = self.bet - playerData.bet
        if playerData.credits >= amount + cost and amount > 0:
            playerData.credits -= amount + cost
            playerData.bet += amount + cost
            self.pot += amount + cost
            self.bet += amount
            return self.nextPlayer()

    def fold(self, sid):
        playerData = self.players[self.sidToPlayer[sid]]
        playerData.fold = True
        self.playersNum -= 1
        if self.playersNum <= 1:
            for table in self.tables:
                table.show_card(len(table.cards))
            return self.end()
        return self.nextPlayer()

    def allin(self, sid):
        playerData = self.players[self.sidToPlayer[sid]]
        playerData.allin = True
        amount = playerData.credits
        cost = self.bet - playerData.bet
        playerData.credits = 0
        playerData.bet += amount
        self.pot += amount
        self.bet += amount - cost
        return self.nextPlayer()

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
