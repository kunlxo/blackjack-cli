from enum import Enum


class GameResult(Enum):
    PLAYER_BUST = "player_bust"
    DEALER_BUST = "dealer_bust"
    PLAYER_BLACKJACK = "player_blackjack"
    DEALER_BLACKJACK = "dealer_blackjack"
    BOTH_BLACKJACK = "both_blackjack"
    PUSH = "push"
    PLAYER_WIN = "player_win"
    PLAYER_LOSE = "player_lose"


class Action(Enum):
    HIT = "hit"
    STAND = "stand"
    DOUBLE = "double"
    SPLIT = "split"
    QUIT = "quit"
