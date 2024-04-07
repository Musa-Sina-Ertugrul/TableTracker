import sys
import customtkinter
import tkinterDnD
from packages import App

customtkinter.set_ctk_parent_class(tkinterDnD.Tk)
sys.path.append("./tmp_files/")

if __name__ == "__main__":
    app = App()
    app.mainloop()
