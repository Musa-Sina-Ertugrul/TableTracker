import tkinter as tk

# TODO: Add ScrollBar


class ResultLabel:
    def __init__(self, root) -> None:
        self.__root = root

        self.__label = tk.Label(
            self.__root,
            text="Result Label\nResult Label\nResult Label\nResult Label\nResult Label\nResult Label\nResult Label\nResult Label\nResult Label\nResult Label\n",
            width=25,
            font=("Ariel", 8),
        )
        self.__label.grid(padx=5, pady=5)

    @property
    def text(self):
        return self.__label.cget("text") or "Nothing Found"

    @text.setter
    def text(self, input_text: str):
        self.__label.config(text=input_text)
