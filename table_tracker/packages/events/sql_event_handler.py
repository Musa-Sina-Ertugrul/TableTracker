import sqlite3
from itertools import tee
from functools import cache, reduce
from sys import getsizeof
from psutil import virtual_memory
import customtkinter
from .event_handler import EventHandler
from ..utils import QUERY_ERROR_NONE_OBJECT



class SQLEventHandler(metaclass=EventHandler):

    def __init__(self, textbox : customtkinter.CTkTextbox,cursor:sqlite3.Cursor,result_label:customtkinter.CTkLabel) -> None:
        self._textbox : customtkinter.CTkTextbox = textbox
        self._cursor : sqlite3.Cursor = cursor
        self._result_label : customtkinter.CTkLabel = result_label
        self.__col_len : int = 0
        self.__row_len : int = 0
        self.__total_size : int = 0

    @property
    def get_query(self) -> str:
        return self._textbox.get("1.0","end")
    
    @property
    def get_formatted_text(self):
        # TODO: Implement This
        return ""
    
    @property
    def get_query_result_itr(self) -> sqlite3.Cursor | None:
        try:
            return self._cursor.execute(self.get_query)
        except sqlite3.ProgrammingError:
            self._cursor.close()
            return QUERY_ERROR_NONE_OBJECT

    @staticmethod
    def _sizeof_row(row : list[tuple]) -> int:
        return reduce(getsizeof,( str(*atr) for atr in row))
    
    @property
    def row_len(self) -> int:
        return self.__row_len or len(self)

    @cache
    def __len__(self) -> int:

        try:
            row_itr : sqlite3.Cursor = self.get_query_result_itr
            row : list[tuple] = next(row_itr)
            self.__col_len = len(row)
            self.__total_size += self._sizeof_row(row)
            for row_count, row in enumerate(row_itr):
                self.__total_size += self._sizeof_row(row)
            self.__row_len = row_count+1
            return self.__row_len
        except (sqlite3.ProgrammingError,StopIteration,TypeError):
            self._cursor.close()
            return 0
    
    @property
    @cache
    def col_len(self) -> int:
        return self.__col_len
    
    @property
    def divaded_itrs(self) -> tuple[sqlite3.Cursor]:
        len(self)
        avaible_memory : int = int(virtual_memory()[1])

        page_count : int = ( self.__total_size // (avaible_memory / 4.0)) or 1
        row_count : int = self.__total_size // page_count

        itrs : sqlite3.Cursor = tee(self.get_query_result_itr,page_count)

        try:
            for current_page,itr in enumerate(itrs[1:],1):
                for _ in range(current_page*row_count):
                    next(itr)
        except (IndexError):
            return itrs

        
    

    

            
        
    
