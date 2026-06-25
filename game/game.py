from models import Pack, Table, Player, Result, Log
from .hand_evaluator import evaluate_hand 
from .round_state import Round, is_betting_round, is_calling_round, is_game_round, game_started

class Game:
    def __init__(self):
        self.players = []
        self.tables = []
        self.event_queue = []
        self.history = []
        self.token_to_player = dict()
        self.sid_to_player = dict()
        self.pack = Pack()
        self.pot = 0
        self.bet = 1
        self.round = Round.PRE_START
        self.whose_round_is = -1
        self.last_round_skipped = False
        self.adminID = 0

    def create_log(self, message):
        self.event_queue.append(Log.create(message))
        self.history.append(Log.create(message))

    def append_player(self, nickname, credits, sid):
        self.players.append(Player(nickname, credits, self.players_num(), sid))
    
    def get_player_by_sid(self, sid):
        if sid in self.sid_to_player.keys():
            return self.players[self.sid_to_player[sid]]
        return None

    def players_num(self):
        return len(self.players) 
    
    def active_players(self):
        return [player for player in self.players if not player.fold]

    def started(self):
        return game_started(self.round)

    def is_end(self):
        return self.round == Round.END
    
    def current_player(self):
        if self.whose_round_is < 0 or self.whose_round_is >= len(self.players):
            return None
        return self.players[self.whose_round_is]

    def bet_to_zero(self):
        for player in self.players:
            player.bet = 0
        self.bet = 0

    def start(self):
        if self.started():
            return
        self.pack.shuffle_cards()
        for _ in self.players:
            self.tables.append(Table(self.pack, 2))

        self.tables.append(Table(self.pack, 5))
        self.whose_round_is = 0
        self.round = Round.PRE_FLOP_BET
        self.create_log("Rozgrywka się rozpoczęła")

    def end(self):
        self.round = Round.END
        for table in self.tables:
            table.show_cards(5)
        self.whose_round_is = -2

        self.create_log("Rozgrywka się skończyła")
        for player in self.players:
            result = evaluate_hand(self.tables[player.ID].cards + self.tables[-1].cards)
            player.result = str(result)

        for log in self.event_queue:
            print(log.display_time, log.timestamp, log.message)
        
    def next_round(self):
        self.whose_round_is = 0
        self.last_round_skipped = False
        self.round = Round(self.round + 1) 

        if (is_betting_round(self.round)):
            self.bet_to_zero()
        
        if is_calling_round(self.round) and all(player.bet == self.bet for player in self.active_players()):
            self.bet_to_zero()
            # Jeżeli wszyscy gracze wyrównali swoje zaklady, to
            # można pominąć turę wyrównywania 
            self.last_round_skipped = True
            self.create_log("Runda nr. " + str(self.round) + " została pominięta")
            self.round = Round(self.round + 1) 

        if is_game_round(self.round):
            self.create_log("Rozgrywka przechodzi w rundę nr. " + str(self.round))

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
        if self.round == Round.FLOP_BET:
            for table in self.tables[:-1]:
                table.show_cards(2)

        # Odkryj trzy wspólne karty
        elif self.round == Round.TURN_BET:
            self.tables[-1].show_cards(3)

        # Odkryj po jednej wspólnej karcie
        elif self.round == Round.RIVER_BET or self.round == Round.SHOWDOWN_BET:
            self.tables[-1].show_cards(1)

        # Zakończ rozgrywkę
        elif self.round == Round.END:
            return self.end()

    def next_player(self):
        while not self.is_end():
            self.whose_round_is += 1
            if self.whose_round_is >= self.players_num():
                self.next_round()
                self.whose_round_is -= 1
                continue

            player = self.players[self.whose_round_is]
            player.last_round_skipped = False

            if player.can_skip_round(self):
                player.last_round_skipped = True
                self.create_log("Kolejka gracza " + player.nickname + " została pominięta")
            else:
                break
  
    def check(self, sid):
        player = self.current_player()

        if player.can_check(self):
            self.create_log("Gracz " + player.nickname + " czeka")
            self.next_player()
        else:
            return Result(False, "Permission denied", "Nie możesz wykonać tej akcji")

    def make_bet(self, sid, amount):
        player = self.current_player()

        if player.can_bet(self) and amount > 0 and player.credits >= amount:
            player.credits -= amount
            player.bet += amount

            self.pot += amount
            self.bet = amount
            self.create_log("Gracz " + player.nickname + " założył się o " + str(amount))
            self.next_player()
        else:
            return Result(False, "Permission denied", "Nie możesz wykonać tej akcji")

    def call(self, sid):
        player = self.current_player()

        cost = self.bet - player.bet

        if player.can_call(self):
            player.credits -= cost
            player.bet += cost

            self.pot += cost
            self.create_log("Gracz " + player.nickname + " sprawdza")
            self.next_player()
        else:
            return Result(False, "Permission denied", "Nie możesz wykonać tej akcji")

    def raiseBet(self, sid, amount):
        player = self.current_player()

        cost = self.bet - player.bet
        amount -= self.bet

        if player.can_raise(self) and amount > 0 and player.credits >= cost + amount:
            player.credits -= amount + cost
            player.bet += amount + cost

            self.pot += amount + cost
            self.bet += amount
            self.create_log("Gracz " + player.nickname + " podbił zakład o " + str(amount))
            self.next_player()
        else:
            return Result(False, "Permission denied", "Nie możesz wykonać tej akcji")

    def fold(self, sid):
        player = self.current_player()

        if player.can_fold(self):
            player.fold = True
            if len(self.active_players()) <= 1:
                return self.end()
            self.create_log("Gracz " + player.nickname + " pasuje")
            self.next_player()
        else:
            return Result(False, "Permission denied", "Nie możesz wykonać tej akcji")

    def allin(self, sid):
        player = self.current_player()

        amount = player.credits
        cost = self.bet - player.bet

        if player.can_allin(self):
            player.allin = True
            player.credits = 0
            player.bet += amount

            self.pot += amount
            self.bet += amount - cost
            self.create_log("Gracz " + player.nickname + " idzie all-in")
            self.next_player()
        else:
            return Result(False, "Permission denied", "Nie możesz wykonać tej akcji")

    def again(self):
        self.round = Round.PRE_START
        self.tables = []
        self.bet = 1
        self.last_round_skipped = False
        self.pack = Pack()
        self.event_queue = []
        self.history = []

        for player in self.players:
            player.bet = 0
            player.allin = False
            player.fold = False
        return self.start()
