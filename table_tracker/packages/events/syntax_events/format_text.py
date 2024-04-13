from functools import cache
from typing import Iterator
import sqlite3
from typing import Any, Generator
from ..event_handler import EventHandler
from ..sql_event_handler import SQLEventHandler
from packages.utils import QUERY_ERROR_NONE_OBJECT,strip_triple


class FormatTextHandler(EventHandler):

    def __init__(self, root: "App", sql_handler: SQLEventHandler) -> None:
        self._root: "App" = root
        self._sql_handler: SQLEventHandler = sql_handler
        self._isfirst: bool = True
        self._max_len = self.get_max_len_on_page()

    @property
    def _itrs(self) -> tuple[sqlite3.Cursor]:
        try:
            return tuple(self._sql_handler.divaded_itrs)
        except TypeError as error:
            print(error)
            return QUERY_ERROR_NONE_OBJECT

    def get_max_len_on_page(self) -> int:
        max_len: int = 0
        if self._sql_handler.get_query_result_itr is not None:
            for column in self._sql_handler.get_query_result_itr:
                max_len = max(len(str(column[0])), max_len)
            for line in self._sql_handler.get_query_result_itr:
                for atrr in line:
                    max_len = max(max_len, len(str(atrr)))
        return max_len + 10

    def get_one_line(self, itr: Iterator) -> Generator[str, Any, None]:
        for line in self._sql_handler.get_query_result_itr:
            line_text: str = ""
            for attr in line:
                line_text += f"{str(attr):>{self._max_len}}"
            yield line_text + "\n"

    def handle(self, page_name: str = "Page 1") -> None:
        if self._isfirst:
            self._handle_first_call()
            return
        self._root.select_page_menu.set(page_name)
        itr_index: int = int(page_name[-2:].strip()) - 1
        try:
            self._handle_tables(itr_index)
        except TypeError:
            self._root.set_result_label = "Query executed"
        except BaseException as error:
            print(error)
            self._root.set_result_label = (
                f"{self._sql_handler.get_query}\n\n\n\nThis query is wrong"
            )


    def _handle_first_call(self) -> None:

        try:
            itrs: tuple[sqlite3.Cursor] = self._itrs
            self._root._add_page(*[f"Page {i}" for i in range(1, len(itrs) + 1)])
            self._root.select_page_menu.set("Page 1")
            self._handle_tables(0)
            self._isfirst = False
        except TypeError:
            self._isfirst = False
            self._root.set_result_label = "Query executed"
        except BaseException as error:
            print(error)
            self._root.set_result_label = (
                f"{self._sql_handler.get_query}\n\n\n\nThis query is wrong"
            )

    def _handle_tables(self,index : int) -> None:
        self._change_text(self._itrs[index])
        self._root.sheet.headers([str(col[0]) for col in self._sql_handler._cursor.description])
        self._root.sheet.data = [[str(atr) for atr in row] for row in iter(self._itrs[index])]

    def _change_text(self, itr: sqlite3.Cursor) -> None:

        label_text: str = "\n"
        for column in self._sql_handler._cursor.description:
            label_text += f"{str(column[0]):>{self._max_len}}"
        label_text += "\n\n\n"
        for line in self.get_one_line(self._sql_handler.get_query_result_itr):
            label_text += line
        
        self._root.set_result_label = strip_triple(label_text)
