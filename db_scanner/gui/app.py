from gui.connect_frame import ConnectFrame
import tkinter as tk


class App:

    def __init__(self) -> None:
        self.__root = tk.Tk()

        self.__connect_frame = ConnectFrame(self.__root)

        self.__root.mainloop()
