##Imports
from tkinter import *
import DBtool


##Functions usable !
class Window : ##Functions that has direct relations with the GUI experience.

    def onlynum(character,entryvalue,decimal=True): ##Checks if the entry is only digits and allows decimals, you can disallow decimanls
        if character.isdigit():
            return True
        
        if decimal == True : ##Makes sure you only add one dot in the text !
            if character == "." and entryvalue.count(".")<2:
                return True
        
        return False
    
    def enableframe(frame):
        if frame.winfo_viewable():
            frame.pack_forget()
        else:
            frame.pack(fill='both', expand=True)

class Select : ##This is used to select, and return data to the controller to later insert it somewhere else

    def allfromentry(instances,inputtype=""): ##Entry instances ---> info in these entries (optional input type helps add extra information to the returned data)
        infolist = [] 
        for instance in instances :
            infolist.append(instance.get())
        
        if inputtype == "Sale" : ##This option adds the total in positive
            total = float(infolist[2])*float(infolist[4])
            infolist.append(str(total))
        
        if inputtype == "Purchase" : ##This function adds the total in negative
            total = float(infolist[2])*float(infolist[3])
            infolist.append(str(total))
        
        return infolist
    
    def allfromtable(table): ##Table instance ---> all items within that table
        infolist = []
        for entry in table.get_children():
            data = entry.item(entry)["values"]
            infolist.apped(data)
        return infolist
    
    def billID(): ## Nothing ---> ID number of next bill
        data = DBtool.Select.lastID()
        if data == None:
            data = 1
        else :
            data =1+int(data)
        
        return data
    
    def fromtable(table): ##Table instance ---> selected row
        infolist = table.item(table.selection())["values"]
        return infolist


    


class Insert : ##Anything that involves inserting info into entries or tables etc would be through here

    def autofill(instances,data): ##Inserts data into instance
        counter = 0
        Delete.clear(instances=instances)
        for instance in instances :
            try :
                instance.insert(0,data[counter])
                counter += 1
            except :
                try :
                    instance.insert(1.0,data[counter])
                    counter +=1
                
                except :
                    print("I did not insert")

    def intotable(table,data):
        table.insert(parent='',index=END, values=data)
        

class Delete : ##Anything that involves deleting or clearing entries goes through here

    def fromtable(table): ##Deletes a row in a table
        try :
            row = table.selection()
            table.delete(row)
        except :
            return
        
    def clear(instances): ##Clears all instances provided
        for instance in instances :
            try :
                instance.delete(0,END)
            except:
                try :
                    instance.delete(1.0,'end')
                except:
                    print("I didn't clear something ")


class Update : ##Updates Labels and tables

    def updatelabel (instance,message=""): ##Updates a label instance and clears out any messages as default
        instance.config(text = message)