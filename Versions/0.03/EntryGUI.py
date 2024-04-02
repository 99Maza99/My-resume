##Imports
import tkinter
from tkinter import *
from tkinter import messagebox
from datetime import datetime

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
    
    def savebill(bill_table,name):
        data = []

        for column in bill_table.get_children():
            item = bill_table.item(column)['values']
            data.append(item)
            
        billid = int(DBtool.Select.lastID())+1

        confirmsave = messagebox.askyesno("Confirm","Do you want to save bill no."+str(billid))
        if confirmsave == False :
            return
        else :
            print("We're saving this")
        for point in data :
            print(point)
            barcode = point[0]
            itemname = point[1]
            quantity = point[2]
            
            if point[5][0] == "-":
                price = -1*point[3]
                state = 0
            else :
                price = point[4]
                state = 1

            total = point[5]
            personel = name.get()
            date = datetime.now().strftime("%d/%m/%Y %H:%M")

            forbill = [billid,personel,barcode,quantity,price,date,state]
            forinventory = [barcode,itemname,quantity,point[3],point[4],state]

            DBtool.Insert.values (data = tuple(forbill),destination= "Bill")
            updater = DBtool.Update.inventory (data = tuple(forinventory))

            if updater[0] == "False" :
                print(itemname)
                print("There is only: "+str(updater[2]))
                print("You were issuing: "+str(updater[1]))



        



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
personel_frame   = personel[0]
personel_entries = personel[1]



confirm_button = Button(root, text="Save bill", command= lambda : Controller.savebill(bill_table,personel_entries[1]))





entry_frame.pack(fill='both', expand=True)
bill_frame.pack(fill='both', expand=True)
personel_frame.pack(fill='both', expand=True)
confirm_button.pack(anchor=W)

root.mainloop()