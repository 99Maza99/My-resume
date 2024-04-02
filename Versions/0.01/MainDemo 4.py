import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import threading
import funckyfuncs
import cv2
from pyzbar.pyzbar import decode
from threading import Thread
from functools import partial

num = 0


def scanbarcode(frame) :
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    barcodes = decode(gray)

    for barcode in barcodes :
        ID       = barcode.data.decode('utf-8')
        datatype = barcode.type
        print(f"Detected {datatype}: {ID}")
        data = funckyfuncs.database.getinfo((str(ID)))

        windowfunc.autofillentry(data,"Database")

def barcodescanner():
    cap = cv2.VideoCapture(0)

    framecount = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret :
            break

        framecount += 1

        if framecount %5 == 0:
            scanbarcode(frame)
            framecount = 0


class windowfunc :
    def autofillperson(event,direc):
        global num
        global currenttext
        if direc == "Esc":
            num = 0
            nameentry.delete(0,END)
            nameentry.insert(0,currenttext)
            return
        
        if direc == "Enter":
            num = 0
            currenttext = ""
            row = funckyfuncs.database.getperson(nameentry.get())
            IDnentry.delete(0,END)
            IDnentry.insert(0,row[0][0]) 
            
            return
                          

        else :
            if nameentry.get():
                if num == 0 :
                    print("Num is zero")
                    currenttext = nameentry.get()
                if direc == "Up":
                    if num == -1 :
                        num = num+3
                    else :
                        num = num + 1
                if direc == "Down":
                    if num == 1 :
                        num = num - 3
                    else :
                        num = num - 1 

                
                rows = funckyfuncs.database.getperson(currenttext)
                suggestions = [item[1] for item in rows]
                print(suggestions)
                matches = [s for s in suggestions if s.startswith(currenttext)]

            if matches:
                index = num % len(matches)
                text = matches[index]
                nameentry.delete(0,END)
                nameentry.insert(0,text)

    def autofillentry(event,data,type):
        print(data)
        if data[0] == "Null":
            if IDentry.get()=="":
                IDentry.insert(0,data[1])
                windowfunc.error("New item detected !")
                return
        
        else :
            if type == "Treeview" :
                if IDentry.        get()=="":
                    IDentry.       insert(0,data[0])
                if productentry.   get()=="":
                    productentry.  insert(0,data[1])
                if quantityentry.  get()=="":
                    quantityentry. insert(0,data[2])
                if sellingentry.   get()=="":
                    sellingentry.  insert(0,data[3])
                if buyingentry.    get()=="":
                    buyingentry.   insert(0,data[4])
                return

            if type == "Database" :
                if IDentry.        get()=="":
                    IDentry.       insert(0,data[0])
                if productentry.   get()=="":
                    productentry.  insert(0,data[1])
                if quantityentry.  get()=="":
                    quantityentry. insert(0,"0")
                if sellingentry.   get()=="":
                    sellingentry.  insert(0,data[3])
                if buyingentry.    get()=="":
                    buyingentry.   insert(0,data[4])
                return

    def error(errmsg):
        errorlabel.config(text=errmsg)
        entryframe.update()

    def clearall():
        IDentry.      delete(0,END)
        productentry. delete(0,END)
        quantityentry.delete(0,END)
        sellingentry. delete(0,END)
        buyingentry.  delete(0,END)

        entryframe.update()

    def deleteitem():
        row = table.selection()
        table.delete(row)
    
    def getdata():
        entry = (IDentry.get(),
                productentry.get(),
                quantityentry.get(),
                sellingentry.get(),
                buyingentry.get())
        return(entry)
        


class buttonfunc :
    def purchase():
        print("Place holder 1")
        windowfunc.error("")

    def sell():
        print("Place holder 2")
        funckyfuncs.testingdb.fakedata()
        windowfunc.error("")

    def addtobill():
        for item in table.get_children():

            values = table.item(item,'value')
            
            if values[1] == productentry.get():
                print(values[1])
                windowfunc.error("Error : Item already exist, update required")
                return
        
        wd  = windowfunc.getdata()
        dbd = funckyfuncs.database.getinfo(wd[0])
        if windowfunc.getdata()[1] == dbd[1] or dbd[0] == "Null":
            table.insert(parent='', index=tkinter.END,values=windowfunc.getdata())
            windowfunc.clearall()
            windowfunc.error("")
        else :
            windowfunc.error("Error : ID and name missmatch")
        return
        


    def updateentry():
        for item in table.get_children():
            values = table.item(item,'value')
            if values[1] == productentry.get():
                wd  = windowfunc.getdata()
                dbd = funckyfuncs.database.getinfo(wd[0])
                if windowfunc.getdata()[1] == dbd[1] or dbd[0]=="Null" :
                    table.insert(parent='', index=tkinter.END,values=windowfunc.getdata())
                    windowfunc.clearall()
                    windowfunc.error("")
                    return
                else:
                    windowfunc.error("Error : ID and name missmatch")
                    return
            else :
                windowfunc.error("Error : Item doesn't exist to update")

        

    def select(_):
        try :
            windowfunc.clearall()
            data = table.item(table.selection())['values']

            windowfunc.autofillentry(data,"Treeview")

            entryframe.update()
        except :
            windowfunc.error("Error : Item no longer exist !")

    def deleteitem(_):
        row = table.selection()
        table.delete(row)
        windowfunc.error("")
       






###############################################
####################GUI########################
###############################################
root = Tk()


########## Entry Frame ###############
entryframe = LabelFrame(root, text='Entry')
entryframe.pack(fill='x',expand='yes',padx=15)

IDentry       = Entry(entryframe, width=30)
productentry  = Entry(entryframe, width=100)
quantityentry = Entry(entryframe, width=10)
sellingentry  = Entry(entryframe, width=10)
buyingentry   = Entry(entryframe, width=10)

productlabel  = Label(entryframe, text="Product")
quantitylabel = Label(entryframe, text="Quantity")
sellinglabel  = Label(entryframe, text="Selling price")
buyinglabel   = Label(entryframe, text="Buying price")

addbutton     = Button(entryframe,text="Add"    ,command=buttonfunc.addtobill)
updatebutton  = Button(entryframe,text="Update" ,command=buttonfunc.updateentry)

IDentry.grid       (row=0,column=1,sticky=W)
productentry.grid  (row=0,column=2,columnspan=5,sticky=W)
quantityentry.grid (row=1,column=1,sticky=W)
sellingentry.grid  (row=1,column=3,sticky=W)
buyingentry.grid   (row=1,column=5,sticky=W)

productlabel.grid  (row=0,column=0,sticky=W)
quantitylabel.grid (row=1,column=0,sticky=W)
sellinglabel.grid  (row=1,column=2,sticky=E)
buyinglabel.grid   (row=1,column=4,sticky=E)
addbutton.grid     (row=2,column=0,sticky=W)
updatebutton.grid  (row=2,column=1,sticky=W)

IDentry.bind('<Button-1>', lambda event: event.widget.focus_set())
entryframe.bind('<Return>',partial(windowfunc.autofillentry, data = "0036000291452", type = "database" ))


########## Bill Frame ###############
billframe  = LabelFrame(root,text="Bill")
errorlabel = Label(billframe,text='')
billnum    = Label(billframe,text='Bill no.')

billframe.pack(fill='x',expand='yes',padx=15)
errorlabel.pack(anchor=E)



table = ttk.Treeview(billframe
                    ,columns = ("ID","Product","Quantity","Selling","Buying")
                    ,show    = 'headings')


table.heading('ID'      , text ='ID'           , anchor=W)
table.heading('Product' , text ='Product'      , anchor=W)
table.heading('Quantity', text = 'Quantity'    , anchor=W)
table.heading('Selling' , text = 'Selling prc' , anchor=W)
table.heading('Buying'  , text = 'Buying prc'  , anchor=W)

table.pack(fill='both',expand=True,padx=15)

table.bind('<<TreeviewSelect>>',buttonfunc.select)
table.bind('<Delete>', buttonfunc.deleteitem)


############# Info Frame ###############
billinfoframe = LabelFrame(root,text="Info")
billinfoframe.pack(fill='x',expand='yes',padx=15)


namelabel     = Label(billinfoframe,text="Personelle :")
tsellinglabel = Label(billinfoframe,text="Total sale :")
tbuyinglabel  = Label(billinfoframe,text="Total purchase:")
tsellingval   = Label(billinfoframe,text="0")
tbuyingval    = Label(billinfoframe,text="0")

IDnentry      = Entry(billinfoframe,width = 30)
nameentry     = Entry(billinfoframe,width = 100)

buybutton  = Button(billinfoframe,text="Purchase",command=buttonfunc.purchase)
sellbutton = Button(billinfoframe,text="Sale"    ,command=buttonfunc.sell)

namelabel.grid     (row=0,column=0)
IDnentry.grid      (row=0,column=1,columnspan=3)
nameentry.grid     (row=0,column=4,columnspan=3)

tsellinglabel.grid (row=1,column=0,sticky=W)
tsellingval.grid   (row=1,column=1)
tbuyinglabel.grid  (row=1,column=2,sticky=W)
tbuyingval.grid    (row=1,column=3)
buybutton.grid     (row=2,column=0)
sellbutton.grid    (row=2,column=1)

nameentry.bind('<Up>',partial(windowfunc.autofillperson, direc = "Up"))
nameentry.bind('<Down>',partial(windowfunc.autofillperson, direc = "Down"))
nameentry.bind('<Escape>',partial(windowfunc.autofillperson, direc = "Esc"))
nameentry.bind('<Return>',partial(windowfunc.autofillperson, direc = "Enter"))

########################Threading and starting the main loop

#####Start of code

funckyfuncs.database.checkfordb()

thread1 = Thread(target=barcodescanner)
thread1.daemon = True
thread1.start()

root.mainloop()


###Database shizzle

class database:
    def checkfordb():
        conn = sqlite3.connect('Data.db')
        c = conn.cursor()
        if os.path.isfile('./Data.db') is True:
            c.execute("SELECT count(*) from sqlite_master WHERE type='table' AND name ='Personel'")
            if c.fetchone()[0]==1:
                print("Personel table already exist")
            else :
                print("Couldn't find Personel")
                c.execute("""CREATE TABLE Personel
                        (
                        ID text NOT NULL,
                        Name text,
                        Desc text,
                        Contact text NOT NULL,
                        Email text
                        )""")
                conn.commit()
                print("Created table : Personel")
            
            c.execute("SELECT count(*) from sqlite_master WHERE type='table' AND name ='Inventory'")
            if c.fetchone()[0]==1:
                print("Inventory table already exist")
            else :
                print("Couldn't find Inventory")
                c.execute("""CREATE TABLE Inventory
                        (
                        ID TEXT NOT NULL,
                        Item text,
                        Qt real,
                        PP real,
                        SP real
                        )""")
                conn.commit()
                print("Created table : Inventory")


            c.execute("SELECT count(*) from sqlite_master WHERE type='table' AND name ='Bill'")
            if c.fetchone()[0]==1:
                print("Bill table already exist")
            else :
                print("Couldn't find Bill")
                c.execute("""CREATE TABLE Bill
                        (
                        ID text NOT NULL,
                        Personel text,
                        Item text,
                        Qt real,
                        Price real,
                        Date text,
                        State int NOT NULL
                        )""")
                conn.commit()
                print("Created table : Bill")


        conn.close()



            #State can be 0 1 2 or 3, where 0 = Purchases, 1 = Sale, 2 = Return to seller, 3 = Return to inventory.
    def getinfo(ID):
        try :
            conn = sqlite3.connect('Data.db')
            c = conn.cursor()

            c.execute("SELECT * from Inventory WHERE ID = ?", (ID,))
            data = c.fetchone()
            conn.close()
            if data == None :
                data = ["Null",ID]
                return data
            else :
                return data
            
        except:
            return
        
    def getperson(ID):
        conn = sqlite3.connect('Data.db')
        c = conn.cursor()

        if ID.isdigit():
            c.execute("SELECT * from Personel WHERE ID = ?",(f'{ID}%',))
            data = c.fetchone()
            conn.close()
            if data == None :
                data = ["Null",ID]
                return data
            else :
                return data
        
        else :
            c.execute("SELECT * from Personel WHERE Name LIKE ?",(f'{ID}%',))
            data = c.fetchall()
            return data



class testingdb():
    def fakedata():
        conn = sqlite3.connect('Data.db')
        c = conn.cursor()
        personelle = ([1,"Maza","They programmed the software", "0102255" , 0],
                      [2,"Hozaifa","He helps with the outputs", "0102255" , 0],
                      [3,"Mohammed","He approves of the GUI", "010225" , 0])
        inventory  = (["0036000291452","Spiro Spates",0,0,0],
                      ["2","Big Cola",0,0,0],
                      ["3","Coffee beans",0,0,0])
        
        c.executemany("""INSERT INTO Personel (ID,Name,Desc,Contact,Email) VALUES (?,?,?,?,?)""",personelle)
        conn.commit
        c.executemany("""INSERT INTO Inventory (ID,Item,Qt,PP,SP) VALUES (?,?,?,?,?)""",inventory)
        conn.commit()
        conn.close()