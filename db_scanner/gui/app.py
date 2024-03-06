from gui.connect_frame import ConnectFrame
from .menubar_table import MenuBarTable
import tkinter as tk


class App:

    def __init__(self) -> None:
        self.__root = tk.Tk()
        self.__root.geometry("800x800")
        self.__menu_bar = MenuBarTable(self.__root)
        self.__root.config(menu=self.__menu_bar.menu)
        self.__connect_frame = ConnectFrame(self.__root)

        self.__root.mainloop()
