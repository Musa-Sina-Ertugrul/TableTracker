import tkinterDnD
import customtkinter
import string
import sqlite3

from ..utils import SQLKeyWords

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk,metaclass=SQLKeyWords):

    PASS_UNNECASSARY_LAST_LETTERS : int = 2

    ON_OFF: dict[str, bool] = {"On": True,"Off":False}

    def __init__(self):
        super().__init__()

        self._last_syntax_error_index = customtkinter.END
        self.__syntax_error_highlight : bool = True
        # configure window
        self.title("TableTracker")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure((1,1,1), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="TableTracker", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.quick_label = customtkinter.CTkLabel(self.sidebar_frame, text="QuickTable", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 0))
        self.quick_label.grid(row=1,column=0,padx=20, pady=(10, 0))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=4, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 0))

        self.syntax_error_label = customtkinter.CTkLabel(self.sidebar_frame, text="Syntax Error", anchor="w")
        self.syntax_error_label.grid(row=10, column=0, padx=20, pady=(10, 0))

        self.syntax_error_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["On", "Off"],
                                                                    command=self.change_syntax_on_off)
        self.syntax_error_optionmenu.grid(row=11, column=0, padx=20, pady=(10, 20))

        self.main_button_1 = customtkinter.CTkButton(master=self,text="Execute", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=4, column=1,columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=425,wrap="word")
        self.textbox.bind("<space>",self._analyze_text)
        self.textbox.grid(row=1, column=1,rowspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.output_frame = customtkinter.CTkScrollableFrame(self, width=425)
        self.output_label = customtkinter.CTkLabel(self.output_frame, width=425)
        self.output_label.grid(sticky="nsew")
        self.output_frame.grid(row=1, column=2,rowspan=3,columnspan=2, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.enter_db = customtkinter.CTkEntry(self,placeholder_text="Enter DB")
        self.enter_db.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.enter_db_button = customtkinter.CTkButton(master=self,text="Enter DB", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.enter_db_button.grid(row=0, column=2,columnspan=2, padx=(20, 20), pady=(20, 0), sticky="nsew")

        # set default values
        self.appearance_mode_optionemenu.set("System")
        self.scaling_optionemenu.set("100%")
        self.syntax_error_optionmenu.set("On")
        self.textbox.insert("0.0", "Enter SQL Lite Queries Here")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def change_syntax_on_off(self,curren_state:str):
        self.__syntax_error_highlight = self.ON_OFF[curren_state]

    def sidebar_button_event(self):
        print("sidebar_button click")

    @property
    def get_textbox_text(self) -> str:
        return self.textbox.get("1.0","end")
    
    def _add_final_space(self):
        textbox_text : str = self.get_textbox_text.strip("\n")
        self.textbox.delete("1.0",customtkinter.END)
        textbox_text += " "
        self.textbox.insert("1.0",textbox_text)

    def _add_syntax_error_sign(self):
        self._last_syntax_error_index : int = (len(self.get_textbox_text.strip("\n")) - self.PASS_UNNECASSARY_LAST_LETTERS 
                                               if self._last_syntax_error_index == customtkinter.END 
                                               or self._last_syntax_error_index >= len(self.get_textbox_text.strip("\n"))
                                               else self._last_syntax_error_index)
        parsed_tk_len : str = f"1.0+{self._last_syntax_error_index}c"
        self.textbox.tag_add(self.__SYNTAX_ERROR_TAG_NAME, parsed_tk_len, customtkinter.END)
        self.textbox.tag_config(self.__SYNTAX_ERROR_TAG_NAME, underline=True,underlinefg="red")
    
    @property
    def __SYNTAX_ERROR_TAG_NAME(self) -> str:
        return "syntax_error_tag_name"

    def _analyze_text(self, event) -> None:

        if self.get_textbox_text[-1] != " ":
            self._add_final_space()

        for word in self.keywords_dict:
            self.__coloring_words(word=word)
            self.__coloring_words(word=word.casefold())
        
        if self.__syntax_error_highlight:
            if not sqlite3.complete_statement(self.get_textbox_text):
                self._add_syntax_error_sign()
            else:
                self.textbox.tag_delete(self.__SYNTAX_ERROR_TAG_NAME)
                self._last_syntax_error_index = customtkinter.END

    def __coloring_words(self,word:str,start_index : str = "1.0") -> None:
        while True:
            start_index = self.textbox.search(
                word, start_index, stopindex=customtkinter.END
            )

            if not bool(start_index):
                break

            end_index: str = f"{start_index}+{len(word)}c"
            
            if self.__is_keyword(start_index=start_index,word=word):
                self.textbox.tag_add(word, start_index, end_index)
                self.textbox.tag_config(word, foreground=self.keywords_dict[word.upper()])
            start_index = end_index
    

    def __is_keyword(self,start_index : str = "1.0",word:str="") -> bool:
        post_letters: str = self.textbox.get(start_index,f"{start_index}+{len(word)+1}c")
        if start_index != "1.0":
            pre_word_index : str = f"{start_index}-{1}c"
            pre_letters: str = self.textbox.get(pre_word_index,start_index)
            return bool(set(pre_letters)-set(string.ascii_letters)) and " " in post_letters
        return " " in post_letters

if __name__ == "__main__":
    app = App()
    app.mainloop()