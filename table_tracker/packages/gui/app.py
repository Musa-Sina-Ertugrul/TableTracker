import tkinterDnD
import customtkinter
import string
import sqlite3
import sys
import os

from ..utils import SQLKeyWords
from packages.events.syntax_events import SytanxErrorHandler
from packages.events.syntax_events import TextColoringHandler
from packages.events import SQLEventHandler

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):    

    def __init__(self):
        super().__init__()

        self._syntax_error_handler : SytanxErrorHandler = SytanxErrorHandler(self)
        self._text_coloring_handler : TextColoringHandler = TextColoringHandler(self)
        self._main_cursor : sqlite3.Cursor = None
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
                                                                    command=self._syntax_error_handler.change_syntax_on_off)
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

        self.enter_db_button = customtkinter.CTkButton(master=self,text="Enter DB", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),command=self._connect_db)
        self.enter_db_button.grid(row=0, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.select_page_menu = customtkinter.CTkOptionMenu(master=self, values= ["Page 1"])
        self.select_page_menu.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")

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

    def sidebar_button_event(self):
        print("sidebar_button click")

    @property
    def get_textbox_text(self) -> str:
        return self.textbox.get("1.0","end")
    
    def _add_page(self,*args):
        if any([type(arg) is not str for arg in args]):
            raise TypeError("Page values are not str")
        self.select_page_menu.configure(values=args)
    
    @property
    def get_db_name(self):
        return self.enter_db.get()

    @property
    def _output_label(self) -> customtkinter.CTkLabel:
        return self.output_label
    
    @_output_label.setter
    def set_result_label(self,text:str):
        self.output_label.configure(text=text)

    def _check_db_file_ishere(self) -> bool:
        if self.get_db_name not in set(os.listdir(".")) and ".db" not in self.get_db_name:
            self.set_result_label = f"There is no such db named {self.get_db_name}"
            return False
        return True

    def _connect_db(self):

        if self._check_db_file_ishere():
            try:
                connection : sqlite3.Connection =sqlite3.connect(self.get_db_name)
                self._main_cursor = connection.cursor()
            except sqlite3.Error:
                self.set_result_label = f"There is no such db named {self.get_db_name}"
                if connection is not None:
                    connection.close()
                if self._main_cursor is not None:
                    self._main_cursor.close()

    def _create_sql_event(self):
        if self._main_cursor is None:
            self.set_result_label = "As first connect db"
            return
        event : SQLEventHandler = SQLEventHandler(self.get_textbox_text,self._main_cursor,self.output_label)
        event.handle()

    def _add_final_space(self):
        textbox_text : str = self.get_textbox_text.strip("\n")
        self.textbox.delete("1.0",customtkinter.END)
        textbox_text += " "
        self.textbox.insert("1.0",textbox_text)

    def _analyze_text(self, event) -> None:

        if self.get_textbox_text[-1] != " ":
            self._add_final_space()

        self._text_coloring_handler.handle()
        self._syntax_error_handler.handle()

if __name__ == "__main__":
    app = App()
    app.mainloop()