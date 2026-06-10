from card import Card
from pack import Pack
from table import Table
from player import Player
from flask import session
import random


class Game:
    def __init__(self):
        self.players = []
        self.tables = []
        self.idToPlayer = dict()
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
        playerId = session.get("ID")

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

    def check(self):
        return self.nextPlayer()

    def makeBet(self, amount):
        if self.players[session.get("ID")].credits >= amount and amount > 0:
            self.players[session.get("ID")].credits -= amount
            self.players[session.get("ID")].bet += amount
            self.pot += amount
            self.bet = amount
            return self.nextPlayer()

    def call(self):
        cost = self.bet - self.players[session.get("ID")].bet
        print(cost)
        if self.players[session.get("ID")].credits >= cost:
            self.players[session.get("ID")].credits -= cost
            self.players[session.get("ID")].bet += cost
            self.pot += cost
            return self.nextPlayer()

    def raiseBet(self, amount):
        cost = self.bet - self.players[session.get("ID")].bet
        if self.players[session.get("ID")].credits >= amount + cost and amount > 0:
            self.players[session.get("ID")].credits -= amount + cost
            self.players[session.get("ID")].bet += amount + cost
            self.pot += amount + cost
            self.bet += amount
            return self.nextPlayer()

    def fold(self):
        self.players[session.get("ID")].fold = True
        self.playersNum -= 1
        if self.playersNum <= 1:
            for table in self.tables:
                table.show_card(len(table.cards))
            return self.end()
        return self.nextPlayer()

    def allin(self):
        self.players[session.get("ID")].allin = True
        amount = self.players[session.get("ID")].credits
        self.players[session.get("ID")].credits = 0
        self.players[session.get("ID")].bet += amount
        self.pot += amount
        self.bet += amount
        return self.nextPlayer()

    def again(self):
        self.roundNum = 0
        self.tables = []
        self.bet = 1
        self.pack = Pack()
        for player in self.players:
            player.bet = 0
            player.allin = False
            player.fold = False
        return self.start()
