import tkinter


from card_shop_frame.repository.card_shop_repository_impl import CardShopMenuFrameRepositoryImpl
from card_shop_frame.service.card_shop_service import CardShopMenuFrameService
from card_shop_frame.frame.buy_check_frame.service.buy_check_service_impl import BuyCheckServiceImpl
from card_shop_frame.frame.buy_check_frame.repository.buy_check_repository_impl import BuyCheckRepositoryImpl
from my_game_money_frame.service.my_game_money_frame_service_impl import MyGameMoneyFrameServiceImpl
from buy_random_card_frame.entity.buy_random_card_frame import BuyRandomCardFrame


class CardShopMenuFrameServiceImpl(CardShopMenuFrameService):
    __instance = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__cardShopMenuFrameRepository = CardShopMenuFrameRepositoryImpl.getInstance()
            cls.__instance.__myGameMoneyFrameService = MyGameMoneyFrameServiceImpl.getInstance()
            cls.__instance.__buyCheckService = BuyCheckServiceImpl.getInstance()
            cls.__instance.__buyCheckRepository = BuyCheckRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance



    def createCardShopUiFrame(self, rootWindow, switchFrameWithMenuName):
        cardShopMenuFrame = self.__cardShopMenuFrameRepository.createCardShopMenuFrame(rootWindow)

        def on_button_click(event):
            self.__buyCheckService.createBuyCheckUiFrame(cardShopMenuFrame, switchFrameWithMenuName)

        def lobby_click_button():
            switchFrameWithMenuName("lobby-menu")

        label_text = "상점"
        label = tkinter.Label(cardShopMenuFrame, text=label_text, font=("Helvetica", 64), fg="black",
                              anchor="center", justify="center")

        label.place(relx=0.5, rely=0.1, anchor="center", bordermode="outside")  # 가운데 정렬


        my_money_frame = self.__myGameMoneyFrameService.createMyGameMoneyUiFrame(cardShopMenuFrame, 10000)
        my_money_frame.place(relx=0.91, rely=0.06, relwidth=0.09, relheight=0.02, anchor="center")



        get_new_all_cards_button = tkinter.Button(cardShopMenuFrame, text="전체 카드 뽑기", bg="#2E2BE2", fg="white",
                                                width=36, height=4)
        get_new_all_cards_button.place(relx=0.5, rely=0.2, anchor="center")
        get_new_all_cards_button.bind("<Button-1>", on_button_click)


        get_new_undead_cards_button = tkinter.Button(cardShopMenuFrame, text="언데드 카드 뽑기", bg="#2E2BE2", fg="white",
                                              command=lambda: switchFrameWithMenuName("buy-random-card"), width=36,
                                              height=4)
        get_new_undead_cards_button.place(relx=0.5, rely=0.4, anchor="center")

        get_new_trant_cards_button = tkinter.Button(cardShopMenuFrame, text="트랜트 카드 뽑기", bg="#2E2BE2", fg="white",
                                              command=lambda: switchFrameWithMenuName("buy-random-card"), width=36,
                                              height=4)
        get_new_trant_cards_button.place(relx=0.5, rely=0.6, anchor="center")

        get_new_human_cards_button = tkinter.Button(cardShopMenuFrame, text="휴먼 카드 뽑기", bg="#2E2BE2", fg="white",
                                              command=lambda: switchFrameWithMenuName("buy-random-card"), width=36,
                                              height=4)
        get_new_human_cards_button.place(relx=0.5, rely=0.8, anchor="center")

        go_back_to_lobby_button = tkinter.Button(cardShopMenuFrame, text="로비로 돌아가기", bg="#2E2BE2", fg="white",
                                        command=lambda: lobby_click_button
                                                 , width=24,height=2)
        go_back_to_lobby_button.place(relx=0.2, rely=0.9, anchor="center")

        my_card_button = tkinter.Button(cardShopMenuFrame, text="내 카드 바로가기", bg="#2E2BE2", fg="white",
                                                 command=lambda: switchFrameWithMenuName("my-card-main"), width=24,
                                                 height=2)
        my_card_button.place(relx=0.8, rely=0.9, anchor="center")


        return cardShopMenuFrame
