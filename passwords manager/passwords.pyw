###Imports
from base64 import encode
import os
import sqlite3
from sqlite3.dbapi2 import connect
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk



###Imports cryptography, and downloads it if is not exitent
try :
    from cryptography import fernet
    from cryptography.fernet import Fernet

except:
    os.system('pip install cryptography')
    from cryptography import fernet
    from cryptography.fernet import Fernet

###Has __init__ function that make sure that the key, and database are created.
class Startup :
    def __init__(self):
        if os.path.isfile('C:\Program Files\passwords\key.key'):
            print (os.path.isfile('C:\Program Files\passwords\key.key'))
            if os.path.isfile('C:\Program Files\passwords\key.key'):
                file = open('C:\Program Files\passwords\key.key','rb')
                self.key = file.read()
            
            else :
                self.key = Fernet.generate_key()
                os.makedirs('C:\Program Files\passwords')
                file = open('C:\Program Files\passwords\key.key','wb')
                file.write(self.key)
                print("Created key")


                
            if os.path.isfile('C:\Program Files\passwords\Data.db') :
                return

            else :    
                conn = sqlite3.connect('C:\Program Files\passwords\Data.db')
                c = conn.cursor()
                c.execute("""CREATE IF NOT EXISTS TABLE Passwords
                (type text NOT NULL,
                desc text,
                email text NOT NULL,
                user text NOT NULL,
                password blob NOT NULL)""")
                conn.commit()
                conn.close()
            
            
        else :
            print(os.path.isfile('C:\Program Files\passwords\key.key'))
            self.key = Fernet.generate_key()
            os.makedirs('C:\Program Files\passwords')
            file = open('C:\Program Files\passwords\key.key','wb')
            file.write(self.key)
            print("Created key")


            
            if os.path.isfile('C:\Program Files\passwords\Data.db') :
                return

            else :
                conn = sqlite3.connect('C:\Program Files\passwords\Data.db')
                c = conn.cursor()    
                c.execute("""CREATE TABLE Passwords
                (type text NOT NULL,
                desc text,
                email text NOT NULL,
                user text NOT NULL,
                password blob NOT NULL)""")
                conn.commit()
                conn.close()
        
        
        
    def GetKey() :
            file = open('C:\Program Files\passwords\key.key','rb')
            key = file.read()
            return key

###Has functions that Encrypt strings, use Encrypt.do(key,string) where key, is the key saved in the keyfile, and string is the string needed to be encrypted
class Encrypt :
    def do (key, password):
        f = Fernet(key)
        encoded = password.encode()
        encrypted = f.encrypt(encoded)
        return encrypted

###Has function that Decrypts arrays, use Decrypt.do(key,string) where key, is the key saved in the keyfile, and string is the array needed to be decrypted
class Decrypt :
    def do (key, password):
        f = Fernet(key)
        password = password
        decrypt = f.decrypt(password)
        decrypt = decrypt.decode()
        return decrypt        

###Has all the functions for the keybinds, and buttons inside the app.
class Functions :
    ###Clears entry boxes
    def clear(e):
        Typeentry.delete(0,END)
        Descentry.delete(0,END)
        Userentry.delete(0,END)
        Emailentry.delete(0,END)
        Passwordentry.delete(0,END)
    ###Refreshes the treeview
    def refresh(e):
        conn = sqlite3.connect('C:\Program Files\passwords\Data.db')
        c = conn.cursor()

        try :
            for i in mytree.get_children():
                mytree.delete(i)
        except :
            return       
        count = 0
        
        c.execute("""SELECT rowid, * FROM Passwords""")
        data = c.fetchall()
        for record in data:
            records = (record[0],record[1],record[2],record[3],record[4],record[5])
            if record[0] % 2 == 0:
                mytree.insert(parent='',index='end', iid=count, text='', values=records, tags=('evenrow',))
            else:
                mytree.insert(parent='',index='end', iid=count, text='', values=records, tags=('oddrow',))
            count +=1
        conn.close()
    ###Copy the password into clipboard
    def copy(e,data):
        values = Functions.getval("id")
        conn = sqlite3.connect("C:\Program Files\passwords\Data.db")
        c = conn.cursor()
        root.clipboard_clear()
        key = Startup.GetKey()
        password = c.execute("SELECT password FROM Passwords WHERE rowid = ?",[values[0]]).fetchone()[0]
        print(password)
        password = password.encode()
        password = Decrypt.do(key,password)
        print(password)
        root.clipboard_append(password)
    ###Selects record, using mouse or keyboard
    def selectrecord(e):
        try :
            Functions.clear(1)
            
            selected = mytree.focus()
            values = mytree.item(selected, "values")

            Typeentry.insert(0,values[1])
            Descentry.insert(0,values[2])
            Emailentry.insert(0,values[3])
            Userentry.insert(0,values[4])
            Passwordentry.insert(0,values[5])

            id = values[0]

            return id,values[5]
            
        except :
            return
    ###Add a record into database
    def addrecord(e):
        conn = sqlite3.connect("C:\Program Files\passwords\Data.db")
        key = Startup.GetKey()
        c = conn.cursor()
        encryptedpassword = Encrypt.do(key,Passwordentry.get())
        values = Functions.getval("add")
        c.execute("INSERT INTO Passwords (type,desc,email,user,password) VALUES (?,?,?,?,?)",(values))

        confirm = messagebox.askyesno(title= "Confrim", message= f"Are you sure of the data you're adding ? \nPassword provided : {Passwordentry.get()}")
        if confirm :
            conn.commit()
            conn.close()
            Functions.refresh(1)
            Functions.clear(1)
        
        else :
            return
    ###Gets values from entry boxes
    def getval(stuff):
        if stuff == "update" :
            values = (Typeentry.get(),Descentry.get(),Emailentry.get(),Userentry.get(),Passwordentry.get(),Functions.selectrecord(0)[0])
            return values
        
        if stuff == "add" :
            values = (Typeentry.get(),Descentry.get(),Emailentry.get(),Userentry.get(),Encrypt.do(Startup.GetKey(),Passwordentry.get()).decode())
            return values
        
        if stuff == "id" :
            values = Functions.selectrecord(0)[0]
            return values
    ###Update the selected record within the database
    def updaterecord(e):
        print (id)
        
        values = Functions.getval("update")
        key = Startup.GetKey()        
        
        conn = sqlite3.connect("C:\Program Files\passwords\Data.db")
        c = conn.cursor()
        c.execute("SELECT password FROM Passwords WHERE rowid = ?",[values[5]])
        password = c.fetchone()
        print(password[0])
        print(values[4])
        if str(password[0]) == str(values[4]):
            c.execute("SELECT rowid, * FROM Passwords")
            c.execute("UPDATE Passwords SET type = ?, desc = ?, email = ?, user = ?, password = ?  WHERE rowid = ?",(values))
            conn.commit()
            Functions.refresh(2)
            conn.close()
            Functions.clear(2)

        else :
            encryptedpassword = Encrypt.do(key,values[4])
            encryptedpassword = encryptedpassword.decode()
            c.execute("SELECT rowid, * FROM Passwords")
            c.execute("UPDATE Passwords SET type = ?, desc = ?, email = ?, user = ?, password = ?  WHERE rowid = ?",(values[0],values[1],values[2],values[3],encryptedpassword,values[5],))
            conn.commit()
            Functions.refresh(2)
            conn.close()
            Functions.clear(2)
    ###Deletes a record from the database
    def deleterecord(e):
        row = Functions.getval("id")
        conn = sqlite3.connect("C:\Program Files\passwords\Data.db")
        c = conn.cursor()
    
        c.execute("""DELETE FROM Passwords WHERE rowid = ?""",[row])

        confirm = messagebox.askyesno(title="Confirm deletion", message=f"Are you sure you want to delete this entry ? \n{Descentry.get()}")
        if confirm :
            conn.commit()
            conn.close()
            Functions.refresh(1)
            Functions.clear(1)
        
        else :
            return
    ###Unselects from treeview
    def unselect(e):
        mytree.selection_remove(mytree.focus())
        Functions.clear(1)


Startup()

root = Tk()
root.title("Password cypher")
id = StringVar()


###Styles the treeview
style = ttk.Style()
style.theme_use('default')
style.configure("Treeview",
                background = "#D3D3D3",
                foreground = "black",
                rowheight=30,
                feildbackground = "#D3D3D3",
                font=('Calibri',12))
style.configure("Treeview.Heading",
                font=('Calibri', 13),
                rowheight= 30)
style.map("Treeview",
          background=[('selected','#347083')],)

###Creates a frame for the treeview
treeframe = LabelFrame(text = "Data")
treeframe.pack(padx= 10,pady=10,expand=True, fill='x', anchor=N)

###Creates scrollers both x and y for treeview
treescroll = Scrollbar(treeframe)
treescroll.pack(side=RIGHT, fill=Y)
treescrollx = Scrollbar(treeframe, orient='horizontal')
treescrollx.pack(side=BOTTOM, fill=X)


###Initiates the treeview
mytree = ttk.Treeview(treeframe, yscrollcommand=treescroll.set, xscrollcommand=treescrollx.set, selectmode= 'extended')
mytree.pack(expand=True, fill='x')


treescroll.config(command=mytree.yview)
treescrollx.config(command=mytree.xview)

columns = ["ID","Type","Describtion","E-mail","User","Password"]
mytree['columns'] = (columns)

mytree.column("#0"      , width=0, stretch=NO)
mytree.column("ID"      , anchor=W, width=40, minwidth=30)
mytree.column("Type"    , anchor=W, width=90, minwidth=80)
mytree.column("Describtion",anchor=W, width=100, minwidth=75)
mytree.column("E-mail"  , anchor=W, width=150, minwidth=125)
mytree.column("User"    , anchor=W, width=90, minwidth=80)
mytree.column("Password", anchor=W, width=125, minwidth=100)


mytree.heading("0"          ,text="",anchor=CENTER)
mytree.heading("ID"         ,text="No",anchor=CENTER)
mytree.heading("Type"       ,text="Social media",anchor=CENTER)
mytree.heading("Describtion",text="Describtion",anchor=CENTER)
mytree.heading("E-mail"     ,text="E-mail",anchor=CENTER)
mytree.heading("User"       ,text="Username",anchor=CENTER)
mytree.heading("Password"   ,text="Password",anchor=CENTER)

mytree.tag_configure('oddrow',background="White")
mytree.tag_configure('evenrow', background="lightblue")

#Refreshes the treeview, to put in data from database
Functions.refresh(1)


#Creates a frame for the data to be displyed
dataframe = LabelFrame(root, text='Records')
dataframe.pack(fill='x',expand='yes',padx = 10)


#Creates labels, entry boxes and buttons for the dataframe
Emaillabel = Label(dataframe, text = "E-mail :", anchor=W)
Emailentry = Entry(dataframe, width= 100 , justify='left')
Emaillabel.grid(row=0,column=0, sticky=W)
Emailentry.grid(row=0,column=1,columnspan=3,sticky=W)


Typelabel = Label(dataframe, text = "Social media :", anchor=W)
Typeentry = Entry(dataframe, width= 30 , justify='left')
Typelabel.grid(row=1,column=0, sticky=W)
Typeentry.grid(row=1,column=1, sticky=W)

Userlabel = Label(dataframe, text = "User :", anchor=W)
Userentry = Entry(dataframe, width= 30 , justify='left')
Userlabel.grid(row=1,column=2, sticky=E)
Userentry.grid(row=1,column=3, sticky=W)

Desclabel = Label(dataframe, text = "Describtion :", anchor=W)
Descentry = Entry(dataframe, width= 100 , justify='left')
Desclabel.grid(row=2,column=0, sticky=W)
Descentry.grid(row=2,column=1,columnspan=3, sticky=W)

decryptedpassword = "Hello"
Passwordlabel = Label(dataframe, text = "Password :", anchor=W)
Passwordentry = Entry(dataframe, width= 30 , justify='left')
Thepassword = Button(dataframe, text="Copy to clipboard",command = lambda : Functions.copy(1,Functions.selectrecord(1)[1]))
Passwordlabel.grid(row=3,column=0, sticky=W)
Passwordentry.grid(row=3,columns=1, columnspan=2,sticky=E)
Thepassword.grid(row=3,column=2,columnspan=2, sticky=W)


#Creates a frame for the commands buttons
commandframe = LabelFrame(root, text="Commands")
commandframe.pack(fill='x',expand='yes',padx = 10)

clearbotton = Button(commandframe, text="Clear", command = lambda : Functions.clear(1))
clearbotton.grid(row = 0, column = 1, padx = 50)

addrecordbutton = updatebutton = Button(commandframe, text="Add", command = lambda : Functions.addrecord(1))
addrecordbutton.grid(row=0, column=2, padx=50)


updatebutton = Button(commandframe, text="Update", command = lambda : Functions.updaterecord(1))
updatebutton.grid(row=0, column=3, padx=50)

removebutton = Button(commandframe, text="Delete", command = lambda : Functions.deleterecord(1))
removebutton.grid(row= 0, column = 4, padx = 50)

unselectbutton = Button(commandframe, text="Unselect", command = lambda : Functions.unselect(1))
unselectbutton.grid(row = 0, column = 5, padx = 50)


#Creating binds
mytree.bind('<ButtonRelease-1>',Functions.selectrecord)
mytree.bind('<KeyRelease-Up>',Functions.selectrecord)
mytree.bind('<KeyRelease-Down>',Functions.selectrecord)

root.bind('<Return>', Functions.updaterecord)

root.bind('<Control-x>',Functions.unselect)
root.bind('<Control-z>',Functions.clear)
root.bind('<Shift-Return>',Functions.addrecord)

root.mainloop()
