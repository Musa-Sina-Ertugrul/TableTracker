import sys

sys.path.append(".")

from db_scanner.utils.sql_keywords import SQLKeyWords
import tkinter as tk
import string

class ScriptText(metaclass=SQLKeyWords):
    def __init__(self, root) -> None:
        self.__root = root
        self.__button_frame = tk.Frame(self.__root)
        

        self.__button_frame.columnconfigure(0, weight=1)
        self.__button_frame.columnconfigure(1, weight=1)

        self.__button_frame.rowconfigure(0, weight=1)
        
        self.__ai_sending_button = tk.Button(self.__button_frame,text="Send to AI",font=("Ariel", 8))
        self.__sql_sending_button = tk.Button(self.__button_frame,text="Send to DB",font=("Ariel", 8))

        self.__text_box = tk.Text(self.__root, font=("Ariel", 12), wrap="word")
        self.__text_box.grid(padx=5, pady=5)
        self.__button_frame.grid(sticky=tk.E + tk.W, padx=5, pady=5)
        self.__sql_sending_button.grid(sticky=tk.E + tk.W,row=0,column=0,padx=5,pady=5)
        self.__ai_sending_button.grid(sticky=tk.E + tk.W,row=0,column=1,padx=5,pady=5)

        self.__text_box.bind("<KeyPress>", self._coloring_words)

    @property
    def _text_box(self):
        return self.__text_box

    @property
    def text(self) -> str:
        return self._text_box.get("1.0", tk.END)

    def _coloring_words(self, event) -> None:
        for word in self.keywords_dict:
            self.__coloring_words_action(word=word)
            self.__coloring_words_action(word=word.casefold())
    
    def __coloring_words_action(self,word:str,start_index : str = "1.0") -> None:
        while True:
            start_index = self._text_box.search(
                word, start_index, stopindex=tk.END
            )

            if not bool(start_index):
                break

            end_index: str = f"{start_index}+{len(word)}c"
            
            if self.__is_keyword(start_index=start_index,word=word,end_index=end_index):
                self._text_box.tag_add(word, start_index, end_index)
                self._text_box.tag_config(word, foreground=self.keywords_dict[word])
            start_index = end_index
    

    def __is_keyword(self,start_index : str = "1.0",word:str="",end_index : str = tk.END) -> bool:
        post_letters: str = self._text_box.get(end_index,f"{start_index}+{len(word)+1}c")
        if start_index != "1.0":
            pre_word_index : str = f"{start_index}-{1}c"
            pre_letters: str = self._text_box.get(pre_word_index,start_index)
            return bool(set(pre_letters)-set(string.ascii_letters)) and " " in post_letters
        return " " in post_letters