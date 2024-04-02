##This file is for creating the main GUI and running it !

##Imports
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from functools import partial

##Importing self made libraries
import Commandtool
##Announcing an instance of tkinter window (Main)

#root = Tk()

class Frames :
    def entryframe(root,table):
        ##First frame is for adding entries !
        entryframe = LabelFrame(root, text='Entry')
        #entryframe.pack(fill='x',expand='yes',padx=15)

        ##Creating instances of entry widgets
        IDentry       = Entry(entryframe, width=30, validate='key', validatecommand=(entryframe.register(partial(Commandtool.Window.onlynumbersallowed, decimal = False)),'%S','%P'))
        productentry  = Entry(entryframe, width=100)
        quantityentry = Entry(entryframe, width=10, validate='key', validatecommand=(entryframe.register(partial(Commandtool.Window.onlynumbersallowed)),'%S','%P'))
        sellingentry  = Entry(entryframe, width=10, validate='key', validatecommand=(entryframe.register(partial(Commandtool.Window.onlynumbersallowed)),'%S','%P'))
        buyingentry   = Entry(entryframe, width=10, validate='key', validatecommand=(entryframe.register(partial(Commandtool.Window.onlynumbersallowed)),'%S','%P'))

        ##Creating instances of Label widgets
        productlabel  = Label(entryframe, text="Product")
        quantitylabel = Label(entryframe, text="Quantity")
        sellinglabel  = Label(entryframe, text="Selling price")
        buyinglabel   = Label(entryframe, text="Buying price")

        ##Creating instances of buttons widgets
        instances     = [IDentry,productentry,quantityentry,sellingentry,buyingentry]
        buybutton     = Button(entryframe,text="Buy"    ,command= lambda:Commandtool.Window.insertintotable(table, instances= instances, inputtype="Entry Frame Purchase"))
        sellbutton    = Button(entryframe,text="Sell"   ,command= lambda:Commandtool.Window.insertintotable(table, instances= instances, inputtype="Entry Frame Sale"))
        #updatebutton  = Button(entryframe,text="Update" ,command=Commandtool.Window.updatetable(table = table, instances = [IDentry,productentry,quantityentry,sellingentry,buyingentry])

        ##Placing all instances created for this frame in a grid !
        IDentry.grid       (row=0,column=1,sticky=W)
        productentry.grid  (row=0,column=2,columnspan=5,sticky=W)
        quantityentry.grid (row=1,column=1,sticky=W)
        sellingentry.grid  (row=1,column=3,sticky=W)
        buyingentry.grid   (row=1,column=5,sticky=W)

        productlabel.grid  (row=0,column=0,sticky=W)
        quantitylabel.grid (row=1,column=0,sticky=W)
        sellinglabel.grid  (row=1,column=2,sticky=E)
        buyinglabel.grid   (row=1,column=4,sticky=E)
        buybutton.grid     (row=2,column=0,sticky=W)
        sellbutton.grid    (row=2,column=1,sticky=W)
        #updatebutton.grid  (row=2,column=1,sticky=W)

        ##Binding keyboard functions

        IDentry.bind('Button-1', lambda event: event.widget.focus_force())
        #entryframe.bind('<Return>',partial())
        
        
        return entryframe,instances


class Table: ##Stores all the Tables that will be used in any GUI file upfront
    def billtable(root): ##This is a Table that stores all the info of a bill before transferring it into the database !
        
        billframe  = LabelFrame(root,text="Bill")

        errorlabel = Label(billframe, text= "") 
        billnumber = Commandtool.Window.getinfo(None,"Get next bill ID")
        print(billnumber)
        billnum    = Label(billframe, text='Bill no.'+str(billnumber))


        ##Table design starts here
        bill = ttk.Treeview(billframe
                            ,columns= ("ID","Item","Qt","Pp","Sp","Total")
                            ,show   = 'headings')
        
        bill.heading("ID"   ,text = "ID"            , anchor=W)
        bill.heading("Item" ,text = "Product"       , anchor=W)
        bill.heading("Qt"   ,text = "Quantity"      , anchor=W)
        bill.heading("Pp"   ,text = "Buying price"  , anchor=W)
        bill.heading("Sp"   ,text = "Selling price" , anchor=W)
        bill.heading("Total",text = "Total"         , anchor=W)


        errorlabel.pack(anchor=E)
        bill.pack(fill='both',expand=True,padx=15)
        billnum.pack(anchor=W)


        

        
        return billframe,bill,errorlabel
