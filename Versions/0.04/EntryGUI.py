#Imported libraries (Some maybe downloaded)
from tkinter import *
from tkinter import messagebox
from datetime import datetime
import tkinter as tk
from tkinter import ttk

#Self made libraries
import GUItool
import Commandtool
import DBtool
from Scantool import Scanner


DBtool.Connection.checklist()##Runs a checklist for the DB to make sure it exists


root = Tk()##Creates instance for Tkinter window

conn = DBtool.Connection.start()##Starts a connection to the database


class UIfunctions : 
    def build(conn): ##Builds the window
        ##Bill table instances
        billblock        = GUItool.Table.billtable(conn,root)
        bill_frame       = billblock[0]
        bill_table       = billblock[1]
        errorlabel       = billblock[2]

        ##Item entry instances
        entryblock       = GUItool.Frames.entryframe(conn,root,bill_table)
        entry_frame      = entryblock[0]
        entry_entries    = entryblock[1]

        ##Personel entry instances
        personelblock    = GUItool.Frames.personelframe(conn,root)
        personel_frame   = personelblock[0]
        personel_entries = personelblock[1]

        ##Scanner instances
        labelscanner = Scanner(entry_widget= [entry_entries[0],personel_entries[0]], scantype="EntryGUI")
        labelscanner.start()

        ##Keybinds for quality of life functions
        bill_table.bind           ('<<TreeviewSelect>>', lambda event : Controller.fillfromtable  (entry_entries,bill_table))
        bill_table.bind           ('<Delete>'          , lambda event : Controller.deletefromtable(entry_entries,bill_table))

        entry_entries[0].bind     ('<Tab>'             , lambda event : Controller.fillfromdb(conn,entry_entries,"Item"))
        personel_entries[0].bind  ('<Tab>'             , lambda event : Controller.fillfromdb(conn,personel_entries,"Personel"))

        ##Exclusive buttons for the window
        confirm_button = Button(root, text="Save bill", command= lambda : Controller.savebill(bill_table,personel_entries[1]))

        ##Packing all the instances into the window
        entry_frame.pack(fill='both', expand=True)
        bill_frame.pack(fill='both', expand=True)
        personel_frame.pack(fill='both', expand=True)
        confirm_button.pack(anchor=W)
    
    def reset(conn,window): ##Destroyes all items within the window and rebuilds it
        DBtool.Connection.end(conn)
        conn = DBtool.Connection.start()
        for widget in window.winfo_children(): ##Destroys all instances in the current window
            widget.destroy()
        
        UIfunctions.build(conn) ##Rebuilds items



##Acts like a small base of operations for the blocks within the window
class Controller :
    def fillfromtable(instances,table): ##Instances are the message boxes that need to be filled in, and an instance of table
        data = Commandtool.Select.fromtable(table=table)
        print(data)
        Commandtool.Insert.autofill(instances=instances,data=data)
        return

    def deletefromtable(instances,table): ##Instances are message boxes that needs to be cleared and the table instance inwhich one item needs to be cleared
        Commandtool.Delete.fromtable(table=table)
        Commandtool.Delete.clear(instances=instances)
        return

    def errorupdates(instance,message=""): ##Takes an instance, usually the error function, and writes in the error for it
        Commandtool.Update.updatelabel(instance,message=message)
        return
    
    def savebill(table,personel): ##Double checks if there is any error first, and saves data.
        billnumber = str(float(DBtool.Select.lastID(conn))+1)
        if personel.get() == "":
            personel = "Annon"
        else :
            personel = personel.get()
        columns    = []
        subtotal   = 0
        for column in table.get_children():
            item = table.item(column)['values']
            columns.append(item)
            subtotal = subtotal + float(item[5])
        
        ###Confirms that saving this bill to database###
        confirmsave = messagebox.askyesno("Confirm","Do you want to save bill no."+ billnumber 
                                          +"\nWith a subtotal of: " + str(subtotal)
                                          +"\nFor: "+ str(personel))
        if confirmsave == False: ###Not confirming, lets you edit the data before saving
            return
        
        else : ###Confirming means the code will run as if nothing happened
            print("Bill confirmed, saving")
        
        for item in columns:
            print(item)
            barcode  = item[0]
            itemname = item[1]
            quantity = item[2]
            ##Checks if total is negative to see what price will be updated, the selling or buying
            if item[5][0] == "-": 
                price = -1*item[3]
                state = 0
            else:
                price = item[4]
                state = 1
            totalperitem = item[5]
            date = datetime.now().strftime("%d-%m-%Y %H:%M")

            ##List to insert into queries
            listforbill         = [billnumber,
                                   personel,
                                   barcode,
                                   quantity,
                                   price,
                                   date,
                                   state]

            listforinventory    = [barcode,
                                   itemname,
                                   quantity,
                                   item[3],
                                   item[4],
                                   state]
            
            updateinventorycheck = DBtool.Update.inventory(conn=conn,data=tuple(listforinventory))
            if updateinventorycheck is False: ##Checks if there is enough of the item in bill in inventory, and returns for edits if not
                print("Error at: ")
                print(listforinventory)
                messagebox.showwarning("Error","You don't have enough of "+itemname+" in your inventory")
                return

            else :
                DBtool.Insert.values(conn=conn,data = tuple(listforbill),destination="Bill")

        DBtool.Connection.commit(conn)
        UIfunctions.reset(conn,root)

    def fillfromdb(conn,instances,database) : ##Autofills data from DB according to which entry widget
        ID = instances[0].get()
        if database == "Item":
            data = DBtool.Select.onerowID(conn,ID,"Inventory")
            if data == None :
                messagebox.showwarning("Warning !","You have zero record of this barcode ! We will be adding it so make sure of the data you input")
            organizeddata = Commandtool.Organize.fromdatabase(data,"Item")

            Commandtool.Delete.clear(instances=instances)
            Commandtool.Insert.autofill(instances=instances,data=data)
        
        if database == "Personel":
            data = DBtool.Select.onerowID(conn,ID,"Personel")
            organizeddata = Commandtool.Organize.fromdatabase(data,"Personel")

            Commandtool.Delete.clear(instances=instances)
            Commandtool.Insert.autofill(instances=instances,data=organizeddata)
        
        return

UIfunctions.build(conn)



root.mainloop()