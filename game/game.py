from models import Log, Pack, Player, Result, Table

from .hand_evaluator import evaluate_hand
from .round_state import (
    Round,
    game_started,
    is_betting_round,
    is_calling_round,
    is_game_round,
)


class Game:
    def __init__(self) -> None:
        self.players: list[Player] = []
        self.tables: list[Table] = []
        self.event_queue: list[Log] = []
        self.history: list[Log] = []

        self.token_to_player: dict[str, int] = {}
        self.sid_to_player: dict[str, int] = {}

        self.pack: Pack = Pack()
        self.pot: int = 0
        self.bet: int = 1
        self.round: Round = Round.PRE_START
        self.whose_round_is: int = -1
        self.last_round_skipped: bool = False

        self.admin_id: int = 0

    def create_log(self, message: str) -> None:
        log = Log.create(message)
        self.event_queue.append(log)
        self.history.append(log)

    def append_player(self, nickname: str, credits: int, sid: str) -> None:
        player = Player(nickname, credits, self.players_num(), sid)
        self.players.append(player)
        self.sid_to_player[sid] = player.id

    def get_player_by_sid(self, sid: str) -> Player | None:
        player_id = self.sid_to_player.get(sid)

        if player_id is None:
            return None

        return self.players[player_id]

    def players_num(self) -> int:
        return len(self.players)

    def active_players(self) -> list[Player]:
        return [
            player
            for player in self.players
            if not player.fold and not player.all_in and player.credits != 0
        ]

    def can_end_game(self) -> bool:
        return len(self.active_players()) <= 1

    def started(self) -> bool:
        return game_started(self.round)

    def is_end(self) -> bool:
        return self.round == Round.END

    def current_player(self) -> Player | None:
        if self.whose_round_is < 0 or self.whose_round_is >= len(self.players):
            return None

        return self.players[self.whose_round_is]

    def bet_to_zero(self) -> None:
        for player in self.players:
            player.bet = 0

        self.bet = 0

    def start(self) -> None:
        if self.started():
            return

        self.pack.shuffle_cards()

        for _ in self.players:
            self.tables.append(Table(self.pack, 2))

        self.tables.append(Table(self.pack, 5))

        self.whose_round_is = -1
        self.round = Round.PRE_FLOP_BET

        self.create_log("Rozgrywka się rozpoczęła")
        self.next_player()

    def end(self) -> None:
        self.round = Round.END

        for table in self.tables:
            table.show_cards(5)

        self.whose_round_is = -2
        self.create_log("Rozgrywka się skończyła")

        for player in self.players:
            result = evaluate_hand(self.tables[player.id].cards + self.tables[-1].cards)
            player.result = str(result)

        for log in self.event_queue:
            print(log.display_time, log.timestamp, log.message)

    def next_round(self) -> None:
        self.whose_round_is = 0
        self.last_round_skipped = False
        self.round = Round(self.round + 1)

        if is_betting_round(self.round):
            self.bet_to_zero()

        if is_calling_round(self.round) and all(
            player.bet == self.bet for player in self.active_players()
        ):
            self.bet_to_zero()

            # Jeżeli wszyscy gracze wyrównali swoje zakłady,
            # to można pominąć turę wyrównywania.
            self.last_round_skipped = True
            self.create_log(f"Runda nr. {self.round} została pominięta")
            self.round = Round(self.round + 1)

        if is_game_round(self.round):
            self.create_log(f"Rozgrywka przechodzi w rundę nr. {self.round}")

        if self.round == Round.FLOP_BET:
            for table in self.tables[:-1]:
                table.show_cards(2)

        elif self.round == Round.TURN_BET:
            self.tables[-1].show_cards(3)

        elif self.round in (Round.RIVER_BET, Round.SHOWDOWN_BET):
            self.tables[-1].show_cards(1)

        elif self.round == Round.END:
            self.end()

    def next_player(self) -> None:
        if self.can_end_game():
            self.create_log(
                "Rozgrywka została zakończona, ponieważ nikt nie mógł już "
                "podjąć żadnej decyzji"
            )
            self.end()
            return

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
                self.create_log(f"Kolejka gracza {player.nickname} została pominięta")
            else:
                break

    def check(self, sid: str) -> Result:
        player = self.current_player()

        if player is None:
            return Result(False, "No current player", "Nie ma aktywnego gracza")

        if not player.can_check(self):
            return Result(False, "Permission denied", "Nie możesz wykonać tej akcji")

        self.create_log(f"Gracz {player.nickname} czeka")
        self.next_player()
        return Result(True)

    def make_bet(self, sid: str, amount: int) -> Result:
        player = self.current_player()

        if player is None:
            return Result(False, "No current player", "Nie ma aktywnego gracza")

        if not (player.can_bet(self) and amount > 0 and player.credits >= amount):
            return Result(False, "Permission denied", "Nie możesz wykonać tej akcji")

        player.credits -= amount
        player.bet += amount
        self.pot += amount
        self.bet = amount

        self.create_log(f"Gracz {player.nickname} założył się o {amount}")
        self.next_player()
        return Result(True)

    def call(self, sid: str) -> Result:
        player = self.current_player()

        if player is None:
            return Result(False, "No current player", "Nie ma aktywnego gracza")

        cost = self.bet - player.bet

        if not player.can_call(self):
            return Result(False, "Permission denied", "Nie możesz wykonać tej akcji")

        player.credits -= cost
        player.bet += cost
        self.pot += cost

        self.create_log(f"Gracz {player.nickname} sprawdza")
        self.next_player()
        return Result(True)

    def raise_bet(self, sid: str, amount: int) -> Result:
        player = self.current_player()

        if player is None:
            return Result(False, "No current player", "Nie ma aktywnego gracza")

        cost = self.bet - player.bet
        raise_amount = amount - self.bet

        if not (
            player.can_raise(self)
            and raise_amount > 0
            and player.credits >= cost + raise_amount
        ):
            return Result(False, "Permission denied", "Nie możesz wykonać tej akcji")

        player.credits -= raise_amount + cost
        player.bet += raise_amount + cost
        self.pot += raise_amount + cost
        self.bet += raise_amount

        self.create_log(f"Gracz {player.nickname} podbił zakład o {raise_amount}")
        self.next_player()
        return Result(True)

    def fold(self, sid: str) -> Result:
        player = self.current_player()

        if player is None:
            return Result(False, "No current player", "Nie ma aktywnego gracza")

        if not player.can_fold(self):
            return Result(False, "Permission denied", "Nie możesz wykonać tej akcji")

        player.fold = True

        if len(self.active_players()) <= 1:
            self.end()
            return Result(True)

        self.create_log(f"Gracz {player.nickname} pasuje")
        self.next_player()
        return Result(True)

    def all_in(self, sid: str) -> Result:
        player = self.current_player()

        if player is None:
            return Result(False, "No current player", "Nie ma aktywnego gracza")

        amount = player.credits
        cost = self.bet - player.bet

        if not player.can_all_in(self):
            return Result(False, "Permission denied", "Nie możesz wykonać tej akcji")

        player.all_in = True
        player.credits = 0
        player.bet += amount
        self.pot += amount
        self.bet += amount - cost

        self.create_log(f"Gracz {player.nickname} idzie all-in")
        self.next_player()
        return Result(True)

    def again(self) -> None:
        self.round = Round.PRE_START
        self.tables = []
        self.bet = 1
        self.last_round_skipped = False
        self.pack = Pack()
        self.event_queue = []
        self.history = []

        for player in self.players:
            player.bet = 0
            player.all_in = False
            player.fold = False

        self.start()