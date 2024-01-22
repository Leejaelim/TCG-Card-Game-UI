import tkinter

from battle_lobby_frame.entity.battle_lobby_frame import BattleLobbyFrame
from battle_lobby_frame.repository.battle_lobby_frame_repository import BattleLobbyFrameRepository
from utility.image_generator import ImageGenerator


class BattleLobbyFrameRepositoryImpl(BattleLobbyFrameRepository):
    __instance = None
    __decks = []

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createBattleLobbyFrame(self, rootWindow):
        print("BattleLobbyFrameRepositoryImpl: createBattleLobbyFrame()")
        battleLobbyFrame = BattleLobbyFrame(rootWindow)

        return battleLobbyFrame

    def getDeckList(self):
        return self.__decks

    def addDeckToDeckList(self, deck):
        self.__decks.append(deck)
        print(f"decks: {self.__decks}")

    def setDeckToDeckList(self, i, deck):
        self.__decks[i] = deck

    def removeDeckFromDeckList(self, deck):
        self.__decks.remove(deck)

    def selectDeck(self, deck):
        for d in self.__decks:
            if d == deck:
                d.config(highlightthickness=5)
            else:
                d.config(highlightthickness=0)

    # TODO : 입장 버튼 클릭 시 실행 될 이벤트. 서버로 무작위 매칭을 요청합니다.
    def enterToRandomMatchingBattle(self):
        pass