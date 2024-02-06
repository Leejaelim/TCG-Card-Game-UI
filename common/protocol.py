from enum import Enum
from enum import Enum


class CustomProtocol(Enum):
    ACCOUNT_REGISTER = 1
    ACCOUNT_LOGIN = 2

    SESSION_LOGIN = 3

    BATTLE_WAIT_QUEUE_FOR_MATCH = 11
    BATTLE_READY = 12
    CANCEL_MATCH = 13 #13
    CHECK_BATTLE_PREPARE = 14 #14
    WHAT_IS_THE_ROOM_NUMBER = 15 #15
    BATTLE_DECK_LIST = 16 #16
    BATTLE_DECK_CARD = 17 #17



    ACCOUNT_DECK_REGISTER = 41

    BUY_CARD = 71

    SURRENDER = 4443
    PROGRAM_EXIT = 4444



