from typing import TYPE_CHECKING

from game.round_state import is_betting_round

if TYPE_CHECKING:
    from game import Game


class Player:
    def __init__(self, nickname: str, credits: int, player_id: int, sid: str) -> None:
        self.nickname = nickname
        self.id = player_id
        self.sid = sid
        self.credits = credits
        self.bet = 0
        self.all_in = False
        self.fold = False
        self.last_round_skipped = False
        self.result: str | None = None

    def can_check(self, game: "Game") -> bool:
        return (
            not self.all_in
            and not self.fold
            and self.bet == game.bet
        )

    def can_bet(self, game: "Game") -> bool:
        return (
            not self.all_in
            and not self.fold
            and is_betting_round(game.round)
            and game.bet == 0
            and self.credits > 0
        )

    def can_call(self, game: "Game") -> bool:
        cost = game.bet - self.bet

        return (
            not self.all_in
            and not self.fold
            and game.bet > self.bet
            and self.credits >= cost
        )

    def can_raise(self, game: "Game") -> bool:
        return (
            not self.all_in
            and not self.fold
            and is_betting_round(game.round)
            and game.bet > 0
            and self.credits > game.bet - self.bet
        )

    def can_fold(self, game: "Game") -> bool:
        return not self.all_in and not self.fold

    def can_all_in(self, game: "Game") -> bool:
        return (
            not self.all_in
            and not self.fold
            and self.credits > 0
            and (
                is_betting_round(game.round)
                or game.bet > self.bet
            )
        )

    def can_skip_round(self, game: "Game") -> bool:
        return (
            not self.can_bet(game)
            and not self.can_call(game)
            and not self.can_raise(game)
            and not self.can_all_in(game)
        )

    def is_admin(self, game: "Game") -> bool:
        return self.id == game.admin_id

    def to_dict(self) -> dict[str, str | int | bool]:
        return {
            "nickname": self.nickname,
            "credits": self.credits,
            "all_in": self.all_in,
            "fold": self.fold,
            "id": self.id,
        }