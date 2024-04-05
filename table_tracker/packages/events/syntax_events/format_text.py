from itertools import tee
import sqlite3
from ..event_handler import EventHandler
from ..sql_event_handler import SQLEventHandler

class FormatTextHandler(EventHandler):

    def __init__(self,root: "App" ,sql_handler: SQLEventHandler) -> None:
        self._root : "App" = root
        self._sql_handler : SQLEventHandler = sql_handler
    @property
    def _itrs(self) -> tuple[sqlite3.Cursor]:
        return tuple(tee(itr,1)[0] for itr in self._sql_handler.divaded_itrs)

    def get_one_line(self,itr):
        for line in itr:
            line_text : str = ""
            for attr in line:
                line_text += str(attr[0])
            yield line_text+"\n"

    def handle(self):
        itrs: tuple[sqlite3.Cursor] = self._itrs
        self._root._add_page(*[f"Page {i}" for i in range(len(itrs)+1)])
        self._root.select_page_menu.set("Page 1")
        label_text :str = ""
        for line in self.get_one_line(itrs[0]):
            label_text += line
        # TODO: Continue from here