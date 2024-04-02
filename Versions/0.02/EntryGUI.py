##Imports
import tkinter
from tkinter import *

##Libraries I made
import GUItool
import Commandtool
import DBtool


DBtool.StartUp.checklist()


root = Tk()

class Controller :
    def fillfromtable(instances,table):
        data = Commandtool.Select.fromtable(table=table)
        Commandtool.Insert.autofill(instances=instances,data=data)

    def deletefromtable(instances,table):
        Commandtool.Delete.fromtable(table=table)
        Commandtool.Delete.clear(instances=instances)

    def errorupdates(instance,message=""):
        Commandtool.Update.updatelabel(instance,message=message)
        return


##Creates an object for the bill table, from the GUI library, and defines its returns
bill = GUItool.Table.billtable(root)
bill_frame = bill[0]
bill_table = bill[1]
errorlabel = bill[2]


##Keyboard binds for the bill table
bill_table.bind('<<TreeviewSelect>>', lambda event : Controller.fillfromtable  (entry_entries,bill_table))
bill_table.bind('<Delete>'          , lambda event : Controller.deletefromtable(entry_entries,bill_table))


##Creates an object for the entry frame, from the GUI library and links it to the bill and defines its returns
entry = GUItool.Frames.entryframe(root,bill_table)
entry_frame   = entry[0]
entry_entries = entry[1]

##Creates an instance of personel frame
personel = GUItool.Frames.personelframe(root)








entry_frame.pack(fill='both', expand=True)
bill_frame.pack(fill='both', expand=True)
personel.pack(fill='both', expand=True)


root.mainloop()