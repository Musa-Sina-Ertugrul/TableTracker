import tkinter as tk
from itertools import cycle
import string

class KeyWords(type):
    
    keywords : set = {
        "ABORT",
        "ACTION",
        "ADD",
        "AFTER",
        "ALL",
        "ALTER",
        "ALWAYS",
        "ANALYZE",
        "AND",
        "AS",
        "ASC",
        "ATTACH",
        "AUTOINCREMENT",
        "BEFORE",
        "BEGIN",
        "BETWEEN",
        "BY",
        "CASCADE",
        "CASE",
        "CAST",
        "CHECK",
        "COLLATE",
        "COLUMN",
        "COMMIT",
        "CONFLICT",
        "CONSTRAINT",
        "CREATE",
        "CROSS",
        "CURRENT",
        "CURRENT_DATE",
        "CURRENT_TIME",
        "CURRENT_TIMESTAMP",
        "DATABASE",
        "DEFAULT",
        "DEFERRABLE",
        "DEFERRED",
        "DELETE",
        "DESC",
        "DETACH",
        "DISTINCT",
        "DO",
        "DROP",
        "EACH",
        "ELSE",
        "END",
        "ESCAPE",
        "EXCEPT",
        "EXCLUDE",
        "EXCLUSIVE",
        "EXISTS",
        "EXPLAIN",
        "FAIL",
        "FILTER",
        "FIRST",
        "FOLLOWING",
        "FOR",
        "FOREIGN",
        "FROM",
        "FULL",
        "GENERATED",
        "GLOB",
        "GROUP",
        "GROUPS",
        "HAVING",
        "IF",
        "IGNORE",
        "IMMEDIATE",
        "IN",
        "INDEX",
        "INDEXED",
        "INITIALLY",
        "INNER",
        "INSERT",
        "INSTEAD",
        "INTERSECT",
        "INTO",
        "IS",
        "ISNULL",
        "JOIN",
        "KEY",
        "LAST",
        "LEFT",
        "LIKE",
        "LIMIT",
        "MATCH",
        "MATERIALIZED",
        "NATURAL",
        "NO",
        "NOT",
        "NOTHING",
        "NOTNULL",
        "NULL",
        "NULLS",
        "OF",
        "OFFSET",
        "ON",
        "OR",
        "ORDER",
        "OTHERS",
        "OUTER",
        "OVER",
        "PARTITION",
        "PLAN",
        "PRAGMA",
        "PRECEDING",
        "PRIMARY",
        "QUERY",
        "RAISE",
        "RANGE",
        "RECURSIVE",
        "REFERENCES",
        "REGEXP",
        "REINDEX",
        "RELEASE",
        "RENAME",
        "REPLACE",
        "RESTRICT",
        "RETURNING",
        "RIGHT",
        "ROLLBACK",
        "ROW",
        "ROWS",
        "SAVEPOINT",
        "SELECT",
        "SET",
        "TABLE",
        "TEMP",
        "TEMPORARY",
        "THEN",
        "TIES",
        "TO",
        "TRANSACTION",
        "TRIGGER",
        "UNBOUNDED",
        "UNION",
        "UNIQUE",
        "UPDATE",
        "USING",
        "VACUUM",
        "VALUES",
        "VIEW",
        "VIRTUAL",
        "WHEN",
        "WHERE",
        "WINDOW",
        "WITH",
        "WITHOUT"
    }
    
    @classmethod
    def __prepare__(mcls,name,base):
        cls_dict : dict = super().__prepare__(mcls,name,base)
        keywords : dict = dict()

        for keyword,color in zip(mcls.keywords,cycle(("magenta4",))):
            keywords[keyword]=color

        for punctuation, color in zip(string.punctuation,cycle(("steel blue",))):
            keywords[punctuation] = color

        for number,color in zip(range(10),cycle(("blue4",))):
            keywords[str(number)] = color

        keywords[";"] = "gray26"

        cls_dict["keywords"] = keywords
        return cls_dict
    
    def __new__(mcls,name,bases,namespace):
        return super().__new__(mcls,name,bases,namespace)     

class ScriptText(metaclass=KeyWords):
    
    def __init__(self,root) -> None:
        self.__root = root
        self.__text_box = tk.Text(self.__root, font=("Ariel", 12), wrap="word")
        self.__text_box.grid(padx=5,pady=5)
        self.__text_box.bind("<KeyPress>",self.__coloring_words)
        
    @property
    def _text_box(self):
        return self.__text_box
    
    @property
    def text(self) -> str:
        return self._text_box.get("1.0",tk.END)

    def __coloring_words(self,event):
        
        for word in self.keywords:
            
            start_index : str = "1.0"
            
            while True:
                start_index = self._text_box.search(word.casefold(),start_index,stopindex=tk.END)
                if not bool(start_index):
                    break
                
                end_index : str = f"{start_index}+{len(word)}c"
                self._text_box.tag_add(word,start_index,end_index)
                self._text_box.tag_config(word,foreground=self.keywords[word])
                start_index = end_index
                
            
            