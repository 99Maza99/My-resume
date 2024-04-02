##This file is for creating the main GUI and running it !

##Imports
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from functools import partial

##Importing self made libraries
import Commandtool
import DBtool
##Announcing an instance of tkinter window (Main)

#some global variables
originaldata = []
searchdata   = []
sidedata     = None
counter      = -1

#root = Tk()

class Organize :
    def fromdatabase(list,framename):
        if framename == "Personel":
            order = [0,1,4,3,2]
            data  = [list[i] for i in order]

            return data


class Buttons : ##Basic buttons that work on their own
    def buy(table,instances): 
        Commandtool.Insert.intotable(table, Commandtool.Select.allfromentry(instances=instances,inputtype="Purchase"))
        Commandtool.Delete.clear(instances=instances)

    def sell(table,instances):
        Commandtool.Insert.intotable(table, Commandtool.Select.allfromentry(instances=instances,inputtype="Sale"))
        Commandtool.Delete.clear(instances=instances)

    def search(frame,instances,table):
        global searchdata
        global originaldata
        global counter    
        focus = frame[0].focus_get()

        originaldata = []
        searchdata   = []
        sidedata     = None

        for name, widget in instances.items():
            if widget == focus:
                inputtype = name
                ID  = widget.get()
                focusedwidget = widget        

        searchdata   = DBtool.Select.manyrow(table=table, ID=ID, inputtype=inputtype)

        originaldata.append(ID)
        originaldata.append(inputtype)
        originaldata.append(focusedwidget)

        frame[1].config(text="Searching using: "+originaldata[1])
        frame[2].config(text="for the word: "+originaldata[0])
        frame[3].config(text="0/"+str(len(searchdata)))

        frame[0].pack(fill="both",expand=True)
        
        counter = -1
            


        
class Autofillcycle:##Buttons that rely on each other to make the functionality of a search cycle
    def next(instances,table,frame):
        global counter

        counter = (counter+1)% len(searchdata)
        buffer = searchdata[counter]

        if table == "Personel":
            data = Organize.fromdatabase(buffer,table)

        Commandtool.Insert.autofill(data=data,instances=instances)
        frame[3].config(text=f"{str(counter+1)}/{str(len(searchdata))}")
        frame[0].update()
        
    def previous(instances,table,frame):
        global counter
        counter = (counter-1)% len(searchdata)
        buffer = searchdata[counter]

        if table == "Personel":
            data = Organize.fromdatabase(buffer,table)

        Commandtool.Insert.autofill(data=data,instances=instances)
        frame[3].config(text=f"{str(counter+1)}/{str(len(searchdata))}")
        frame[0].update()

    def cancel(instances,frame):
        frame[0].pack_forget()
        Commandtool.Delete.clear(instances=instances)
        Commandtool.Insert.autofill(data=[originaldata[0]],instances=[originaldata[2]])

    def confirm(frame):
        frame[0].pack_forget()
        
        return None
            
         
    


class Frames : ##All entry frames !
    def entryframe(root,table,tab="Entry"):
        ##Frame is for adding and editing entries !
        entryframe = LabelFrame(root, text='Entry')

        ##Creating instances of entry widgets
        IDentry       = Entry(entryframe, width=30, validate='key', validatecommand=(entryframe.register(partial(Commandtool.Window.onlynum, decimal = False)),'%S','%P'))
        productentry  = Entry(entryframe, width=100)
        quantityentry = Entry(entryframe, width=10, validate='key', validatecommand=(entryframe.register(partial(Commandtool.Window.onlynum)),'%S','%P'))
        buyingentry   = Entry(entryframe, width=10, validate='key', validatecommand=(entryframe.register(partial(Commandtool.Window.onlynum)),'%S','%P'))
        sellingentry  = Entry(entryframe, width=10, validate='key', validatecommand=(entryframe.register(partial(Commandtool.Window.onlynum)),'%S','%P'))

        ##Creating instances of Label widgets
        productlabel  = Label(entryframe, text="Product")
        quantitylabel = Label(entryframe, text="Quantity")
        buyinglabel   = Label(entryframe, text="Buying price")
        sellinglabel  = Label(entryframe, text="Selling price")


        ##Creating instances of buttons widgets
        instances     = [IDentry,productentry,quantityentry,buyingentry,sellingentry]


        buybutton     = Button(entryframe,text="Buy"    ,command= lambda:Buttons.buy(table=table,instances=instances))
        sellbutton    = Button(entryframe,text="Sell"   ,command= lambda:Buttons.sell(table=table,instances=instances))

        ##Placing all instances created for this frame in a grid !
        IDentry.grid       (row=0,column=1,sticky=W)
        productentry.grid  (row=0,column=2,columnspan=5,sticky=W)
        quantityentry.grid (row=1,column=1,sticky=W)
        buyingentry.grid   (row=1,column=3,sticky=W)
        sellingentry.grid  (row=1,column=5,sticky=W)


        productlabel.grid  (row=0,column=0,sticky=W)
        quantitylabel.grid (row=1,column=0,sticky=W)
        buyinglabel.grid   (row=1,column=2,sticky=E)
        sellinglabel.grid  (row=1,column=4,sticky=E)
        sellbutton.grid    (row=2,column=2,sticky=W)
        buybutton.grid     (row=2,column=1,sticky=W)

        
        
        return entryframe,instances

    def personelframe(root): 
        ##this frame contains useful information about the person you're buying from or selling to
        personelframe = LabelFrame(root,text="Person Info")
        
        infoframe1     = Frame(personelframe)
        infoframe2     = Frame(personelframe)
        autofillframe  = LabelFrame(personelframe,text="Searching")

        ##creating instances to define the infoframe
        namelabel        = Label(infoframe1,text="Name")
        IDentry          = Entry(infoframe1,width = 30)
        nameentry        = Entry(infoframe1,width = 60)


        emaillabel       = Label(infoframe2,text="E-mail")
        phonenumberlabel = Label(infoframe2,text="Phone")
        descriptionlabel = Label(infoframe2,text="Description")
        emailentry       = Entry(infoframe2,width = 60)
        phonenumberentry = Entry(infoframe2,width = 60)
        descriptionentry = Text (infoframe2,width = 130, height=15)




        instances = [IDentry, nameentry,emailentry,phonenumberentry,descriptionentry]
        entries   = {"ID": IDentry,
                     "Name": nameentry,
                     "Email": emailentry,
                     "Contact":phonenumberentry,
                     "Desc":descriptionentry,}

        
        ##placing the instances
        namelabel.grid        (row=0,column=0,columnspan=2,sticky=W)

        IDentry.grid          (row=1,column=0,sticky="ew", padx=5, pady=5)
        nameentry.grid        (row=1,column=1,sticky="ew", padx=5, pady=5)

        emaillabel.grid       (row=0,column=0,sticky=W)
        phonenumberlabel.grid (row=0,column=1,sticky=W)
        descriptionlabel.grid (row=2,column=0,sticky=W)

        emailentry.grid       (row=1,column=0,sticky="ew", padx=5, pady=5)
        phonenumberentry.grid (row=1,column=1,sticky="ew", padx=5, pady=5)
        descriptionentry.grid (row=3,column=0,columnspan=2,sticky="nsew", padx=5, pady=5)

        
        
        ## Equal weight to both columns for proportional horizontal resize
        infoframe1.grid_columnconfigure(0, weight=1)
        infoframe1.grid_columnconfigure(1, weight=9)

        infoframe2.grid_columnconfigure(0, weight=1)
        infoframe2.grid_columnconfigure(1, weight=1)
        ##Packing the info frame
        infoframe1.pack(fill='both', expand=True)
        infoframe2.pack(fill='both', expand=True)

        ##autofill frame instances
        
        searchlabel    = Label(autofillframe, text="Searching using :")
        keywordlabel   = Label(autofillframe, text="for the world :")
        indexlabel     = Label(autofillframe, text="0/0")

        previousbutton = Button(autofillframe, text="<",            command= lambda:Autofillcycle.previous(instances,"Personel",frame))
        nextbutton     = Button(autofillframe, text=">",            command= lambda:Autofillcycle.next(instances,"Personel",frame))
        cancelbutton   = Button(autofillframe, text="Cancel",       command= lambda:Autofillcycle.cancel(instances,frame))
        confirmbutton  = Button(autofillframe, text="Confirm",      command= lambda:Autofillcycle.confirm(frame))

        ##Search button that activates autofill frame instances
        frame = [autofillframe,searchlabel,keywordlabel,indexlabel]
        Searchbutton = Button(infoframe2,text="Search",command= lambda:Buttons.search(frame,entries,"Personel"))
        Searchbutton.grid    (row=6,column=0,sticky=W, padx=5, pady=5)

        ##Placing these instances

        searchlabel.grid     (row=0,column=0,columnspan=5,sticky=W)
        keywordlabel.grid    (row=1,column=0,columnspan=5,sticky=W)
        indexlabel.grid      (row=2,column=2)

        previousbutton.grid  (row=2,column=1)
        nextbutton.grid      (row=2,column=3)
        cancelbutton.grid    (row=2,column=0)
        confirmbutton.grid   (row=2,column=4)
    
        return personelframe,instances


class Table: ##Stores all the Tables that will be used in any GUI file upfront
    def billtable(root): ##This is a Table that stores all the info of a bill before transferring it into the database !
        
        billframe  = LabelFrame(root,text="Bill")

        errorlabel = Label(billframe, text= "") 
        billnumber = Commandtool.Select.billID()
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
