import tkinter as tk

class QuickFunctionTable:

    def __init__(self,root) -> None:
        self.__root = root



class MenuBarTable:

    def __init__(self,root) -> None:
        
        self.__root = root

        self.__menu_bar = tk.Menu(self.__root)
        self.__menu_bar_quickly = tk.Menu(self.__menu_bar,tearoff=0)
        
        self.__menu_bar_quickly.add_command(label="1",command=exit)
        self.__menu_bar_quickly.add_command(label="2",command=exit)
        self.__menu_bar_quickly.add_command(label="3",command=exit)
        self.__menu_bar_quickly.add_command(label="4",command=exit)
        self.__menu_bar_quickly.add_command(label="5",command=exit)
        self.__menu_bar_quickly.add_command(label="6",command=exit)

        self.__menu_bar.add_cascade(menu=self.__menu_bar_quickly,label="Quickly")

        self.__menu_bar.add_command(label="Exit",command=exit)

    @property
    def menu(self):
        return self.__menu_bar


