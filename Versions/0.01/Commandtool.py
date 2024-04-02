##Imports
from tkinter import *
import DBtool


##Functions usable !
class Window :
    def autofillinfo (instances,data):
        counter = 0
        Window.clearall(instances=instances)
        for instance in instances :
            instance.insert(0,data[counter])
            counter += 1


    def getinfo(instances,inputtype): #this takes all entry instances provided, and gets data inside it and returns it as a list
        infolist = []


        if inputtype == "Entry Frame Sale" :
            for instance in instances :
                infolist.append(instance.get())


            total = float(infolist[2]) * float(infolist[4])
            infolist.append(str(total))
            return infolist

        if inputtype == "Entry Frame Purchase":
            for instance in instances :
                infolist.append(instance.get())


            total = -1 * float(infolist[2]) * float(infolist[3])
            infolist.append(str(total))
            return infolist
        

        if inputtype == "Bill":
            for entry in instances.get_children():
                data = instances.item(entry)["values"]
                infolist.append(data)
            return infolist

        if inputtype == "Get next bill ID":
            data = DBtool.Database.getbill(None,"Get last ID")
            if data == None:
                data = 1
            else :
                data = 1+float(data)
            return data
    
    def errormessage(instance,message): #this takes a tuple where 0 in the tuple is the error label, and 1 is the frame that the label is in
        instance(0).config(text=message)
        instance(1).update()

    def clearall(instances):
        for instance in instances :
            instance.delete(0,END)
    
    def insertintotable(table,instances,inputtype): #this takes the table instance, and entry instances, and inserts the entry instances into the table
        infolist = Window.getinfo(instances=instances,inputtype=inputtype)
        table.insert(parent='', index=END,values=infolist)
        Window.clearall(instances=instances)
    
    def getfromtable(_,table): #this takes a table instance, and returns value of a selected row in a list
        infolist = table.item(table.selection())['values']
        return infolist
    
    def deletefromtable(table): #this takes a table instance, and deletes a selected row
        try :
            row = table.selection()
            table.delete(row)
        except:
            return
        
    def selectfromtable(table): #this selects a row from a table and returns a list

        data = table.item(table.selection())['values']
        return data
    
    def onlynumbersallowed(character, entryvalue,decimal=True): #this checks if the value being put into an entry is a number
        if character.isdigit():
            return True
            
        if decimal == True : #Sees if a decimal would be needed (ie calculating weight would need decimals but not an ID)
            if character == ".":
                if entryvalue.count(".") < 2 :
                    return True
            
        
        return False



