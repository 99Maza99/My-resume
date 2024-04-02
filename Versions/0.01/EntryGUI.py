##Imports
import tkinter
from tkinter import *

##Libraries I made
import GUItool
import Commandtool
import DBtool


root = Tk()

class Controller :
    def fillfromtable(instances,table):
        data = Commandtool.Window.selectfromtable(table=table)
        Commandtool.Window.autofillinfo(instances=instances,data=data)


bill = GUItool.Table.billtable(root)
bill_frame = bill[0]
bill_table = bill[1]
errorlabel = bill[2]


entry = GUItool.Frames.entryframe(root,bill_table)
entry_frame   = entry[0]
entry_entries = entry[1]



bill_table.bind('<<TreeviewSelect>>', lambda event : Controller.fillfromtable(entry_entries,bill_table) )
bill_table.bind('<Delete>'          , lambda event : Commandtool.Window.deletefromtable(table=bill_table))





entry_frame.pack()
bill_frame.pack()



root.mainloop()