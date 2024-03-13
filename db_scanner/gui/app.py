from .connect_frame import ConnectFrame
from .menubar_table import MenuBarTable
from .result_label import ResultLabel
from .script_text import ScriptText
import tkinter as tk


class App:
    def __init__(self) -> None:
        self.__root = tk.Tk()
        self.__root.geometry("735x1000")
        self.__root.title("DBScanner")
        self.__menu_bar = MenuBarTable(self.__root)
        self.__root.config(menu=self.__menu_bar.menu)
        self.__connect_frame = ConnectFrame(self.__root)
        self.__script_box = ScriptText(self.__root)
        self.__result_label = ResultLabel(self.__root)
        self.__root.mainloop()
