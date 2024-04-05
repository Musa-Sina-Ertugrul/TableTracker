from ..event_handler import EventHandler
import customtkinter
import sqlite3

class SytanxErrorHandler(EventHandler):

    PASS_UNNECASSARY_LAST_LETTERS : int = 2
    ON_OFF: dict[str, bool] = {"On": True,"Off":False}

    def __init__(self,root : "App") -> None:
        self._root : "App" = root
        self._last_syntax_error_index = customtkinter.END
        self.__syntax_error_highlight : bool = True

    def add_syntax_error_sign(self):
        self._last_syntax_error_index = (len(self._root.get_textbox_text.strip("\n")) - self.PASS_UNNECASSARY_LAST_LETTERS 
                                               if self._last_syntax_error_index == customtkinter.END 
                                               or self._last_syntax_error_index >= len(self._root.get_textbox_text.strip("\n"))
                                               else self._last_syntax_error_index)
        parsed_tk_len : str = f"1.0+{self._last_syntax_error_index}c"
        self._root.textbox.tag_add(self.__SYNTAX_ERROR_TAG_NAME, parsed_tk_len, customtkinter.END)
        self._root.textbox.tag_config(self.__SYNTAX_ERROR_TAG_NAME, underline=True,underlinefg="red")
    
    def change_syntax_on_off(self,curren_state:str):
        self.__syntax_error_highlight = self.ON_OFF[curren_state]

    def handle(self):
        if self.__syntax_error_highlight:
            if not sqlite3.complete_statement(self._root.get_textbox_text):
                self.add_syntax_error_sign()
            else:
                self._root.textbox.tag_delete(self.__SYNTAX_ERROR_TAG_NAME)
                self._last_syntax_error_index = customtkinter.END

    @property
    def __SYNTAX_ERROR_TAG_NAME(self) -> str:
        return "syntax_error_tag_name"