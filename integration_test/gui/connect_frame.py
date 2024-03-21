import tkinter as tk

# TODO: Add functionality to buttons


class ConnectFrame:
    def __init__(self, root) -> None:
        self.__root = root

        self.__connect_frame = tk.Frame(self.__root)
        self.__connect_frame.grid(row=1, sticky=tk.E + tk.W, padx=5, pady=5)

        self.__connect_frame.columnconfigure(0, weight=1)
        self.__connect_frame.columnconfigure(1, weight=1)

        self.__connect_frame.rowconfigure(0, weight=1)
        self.__connect_frame.rowconfigure(1, weight=1)

        self.__label = tk.Label(
            self.__connect_frame,
            text="Enter DB Name",
            height=1,
            width=25,
            font=("Ariel", 8),
        )

        self.__label.grid(row=0, column=0, sticky=tk.E + tk.W, padx=5, pady=0)

        self.__text_box = tk.Text(
            self.__connect_frame, height=1, width=25, font=("Ariel", 8)
        )
        self.__text_box.grid(row=1, column=0, sticky=tk.E + tk.W, padx=5, pady=5)

        self.__button = tk.Button(
            self.__connect_frame, text="connect", font=("Ariel", 8)
        )
        self.__button.grid(row=1, column=1, sticky=tk.E + tk.W, padx=5, pady=5)

    @property
    def text(self) -> str | bool:
        result: str = self.__text_box.get(1.0, tk.END).strip(" ").strip("\n")

        if " " in set(result):
            return False

        return result


if __name__ == "__main__":
    root = tk.Tk()

    ConnectFrame(root)

    root.mainloop()
