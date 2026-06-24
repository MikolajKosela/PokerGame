from enum import IntEnum

class Round(IntEnum):
    PRE_START = -1

    PRE_FLOP_BET = 0
    PRE_FLOP_CALL = 1

    FLOP_BET = 2
    FLOP_CALL = 3

    TURN_BET = 4
    TURN_CALL = 5

    RIVER_BET = 6
    RIVER_CALL = 7

    SHOWDOWN_BET = 8
    SHOWDOWN_CALL = 9

    END = 10

def is_game_round(round_num: Round) -> bool:
    return round_num >= 0 and round_num <= 9

def is_betting_round(round_num: Round) -> bool:
    return is_game_round(round_num) and round_num % 2 == 0

def is_calling_round(round_num: Round) -> bool:
    return is_game_round(round_num) and round_num % 2 == 1

def game_started(round_num: Round) -> bool:
    return round_num > -1