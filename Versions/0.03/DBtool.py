##Imports
import os
import sqlite3
import cv2
from pyzbar.pyzbar import decode


##Fake data for testing porpuses
fakepersonel  = (
                ['c4d36504-adc7-4391-8422-7556a0e2feaf', 'Diana Walters', 'Several truth thought different eye.', '(004)488-8587x87224', 'utaylor@yahoo.com'],
                ['cf3b8568-af9c-4ed6-af1d-fe05cf0e0d5d', 'Tyler Hernandez', 'Community wonder occur strong.', '+1-056-897-8907x0587', 'scottwashington@hayes.com'],
                ['584c449a-45b4-4f68-aa7e-dae44340e928', 'Hannah Brown', 'Go determine agent man course meeting compare.', '(565)117-2820x61892', 'williamskelsey@rodriguez.net'],
                ['c3004b5b-fbc2-41dd-a8d1-caa4c7723e1c', 'Mariah Richardson', 'Say rise collection side.', '071-424-0708', 'swilkinson@hotmail.com'],
                ['c6b7a82d-a109-4e63-9c3c-929b2c3fc28f', 'Steven Chapman', 'Tree visit miss movie ago strategy.', '4289434641', 'johnstondeborah@cook.com'],
                ['12a2035b-ba78-40bc-a920-8787760aff83', 'Jacqueline Johnson MD', 'Senior management black write.', '001-531-810-1696x3227', 'cmartinez@anderson.com'],
                ['a6ed64fb-f80c-45bf-b261-63f8cd2582f4', 'Kelli Kennedy', 'Here position general value garden.', '(570)136-9946x2377', 'bryan68@gmail.com'],
                ['c95adf29-63e5-4a87-8d0a-1333770290d4', 'Mary Wright', 'Tax theory final oil beat guess simply.', '619.501.7486', 'thompsonscott@williams.com'],
                ['ed938b6d-8522-43e1-8280-5232415ea1e4', 'Zachary Mcdonald', 'Upon others character blue effort control town.', '333-808-4624', 'colemanelizabeth@sullivan.com'],
                ['49fe09c4-949f-41f5-adc2-d34e64bc8aeb', 'Keith Rice', 'Season like throughout.', '(473)410-0197x97549', 'oliviagarrison@gonzalez.info']
                )

fakeinventory = (
                ['780239568938', 'Mrs', 61.87032765607118, 22.085528101180536, 697.400414244534],
                ['975257496542', 'very', 75.74416583265199, 144.32537022503365, 557.864152578978],
                ['607838595280', 'skin', 51.73520534276247, 493.09431240607137, 646.9090666526511],
                ['646198514825', 'stand', 17.764006888423648, 165.86202081170805, 776.3031516198196],
                ['786874518145', 'sell', 9.583479591282318, 374.69455818814833, 888.8391013236551],
                ['638150389588', 'he', 96.20218364488537, 268.7137906632864, 800.7597194537658],
                ['655117657886', 'politics', 8.697352254829763, 254.08484914824413, 581.1638995030598],
                ['609522629662', 'key', 79.50999141777059, 104.46891183910833, 526.4172194960905],
                ['576716800197', 'consider', 52.85718635989425, 323.58759341112193, 639.5712885074679],
                ['748393970021', 'movement', 63.04353672035225, 188.26347915192977, 894.8573116652396]
                )

fakebills     = (
                [1, 'Keith Rice', 'very', 75.74416583265199, 496.6224941674386, '1979-03-18', 3],
                [2, 'Keith Rice', 'movement', 63.04353672035225, 269.07729071316834, '1971-12-31', 3],
                [3, 'Diana Walters', 'skin', 51.73520534276247, 440.83389972821675, '2001-10-11', 1],
                [3, 'Kelli Kennedy', 'stand', 17.764006888423648, 152.91658220137128, '1985-12-30', 3],
                [4, 'Kelli Kennedy', 'stand', 17.764006888423648, 223.17884681692894, '1996-03-25', 2],
                [5, 'Hannah Brown', 'sell', 9.583479591282318, 234.95692635473026, '2021-06-08', 0],
                [6, 'Tyler Hernandez', 'skin', 51.73520534276247, 145.42634508944053, '1997-09-02', 3],
                [7, 'Diana Walters', 'skin', 51.73520534276247, 143.0055163748699, '1984-12-05', 0],
                [8, 'Jacqueline Johnson MD', 'Mrs', 61.87032765607118, 437.95649906635225, '1994-01-10', 0],
                [8, 'Jacqueline Johnson MD', 'Mrs', 61.87032765607118, 155.73967913652467, '2016-11-15', 2]
                )

class StartUp : ##Runs once everytime the app starts
    def checklist(): ##A function that works as a checklist to make sure database and tables are in place
        conn = sqlite3.connect("Data.db")
        c    = conn.cursor()

        if os.path.isfile("./Data.db") is True :
            print("Database Data.db already exists !")


            ###Checks for Personel Table and creates it if its not there
            c.execute("SELECT count(*) FROM sqlite_master WHERE type='table' and name='Personel'")

            if c.fetchone()[0] == 1 :
                print("Personel table already exists !")
            else :
                print("Couldn't find Personel")
                c.execute("""CREATE TABLE Personel
                          (
                            ID      TEXT NOT NULL,
                            Name    TEXT,
                            Desc    TEXT,
                            Contact TEXT NOT NULL,
                            Email   TEXT
                          )""")
                
                conn.commit()
                print("Created table : Personel")
            
            

            
            ##Checks for Inventory Table and creates it if its not there
            c.execute("SELECT count(*) FROM sqlite_master WHERE type='table' and name='Inventory'")
            
            if c.fetchone()[0] == 1 :
                print("Inventory table already exists !")
            else :
                print("Couldn't find Inventory")
                c.execute("""CREATE TABLE Inventory
                          (
                            ID      TEXT NOT NULL,
                            Item    TEXT,
                            Qt      REAL,
                            PP      REAL,
                            SP      REAL
                          )""")
                
                conn.commit()
                print("Created table : Inventory")

            
            
            
            ##Checks for Bill Table and creates it if its not there
            c.execute("SELECT count(*) from sqlite_master WHERE type='table' AND name ='Bill'")

            if c.fetchone()[0] == 1 :
                print("Bill table already exists !")
            else :
                print("Couldn't find Bill")
                c.execute("""CREATE TABLE Bill
                          (
                            ID          REAL NOT NULL,
                            Personel    TEXT,
                            Item        TEXT,
                            Qt          REAL,
                            Price       REAL,
                            Date        TEXT,
                            State       INT NOT NULL
                          )""") ##State can be [0,1,2,3] check notes for documentation please <3
                
                conn.commit()
                print("Created table : Bill")
        
        conn.close()


class Select :
    def onerowID (ID,table):
        conn = sqlite3.connect("Data.db")
        c    = conn.cursor()

        c.execute(f"SELECT * FROM {table} WHERE ID = ?",(ID,))
        data = c.fetchone()
        conn.close()

        return data
    
    def manyrow (ID,table,inputtype):
        conn = sqlite3.connect("Data.db")
        c    = conn.cursor()
        
        ID = "%"+ID+"%"

        c.execute(f"SELECT * FROM {table} WHERE {inputtype} LIKE ?",(ID,))
        data = c.fetchall()

        infolist=[]

        for row in data :
            infolist.append(row)

        conn.close()
        return infolist
    
    def lastID():
        try :
            conn = sqlite3.connect("Data.db")
            c    = conn.cursor()

            c.execute("SELECT ID FROM Bill ORDER BY ID DESC LIMIT 1;")
            data = c.fetchone()[0]

            conn.close()

            return data
        
        except :
            return 0
    

class Insert :

    def values (data,destination) :
        placeholder = ",".join(["?"] * len(data))


        conn = sqlite3.connect("Data.db")
        c    = conn.cursor()

        c.execute(f"INSERT INTO {destination} VALUES ({placeholder})",data)
        conn.commit()


class Update :
    def inventory (data):
        conn = sqlite3.connect("Data.db")
        c    = conn.cursor()


        c.execute("SELECT * FROM Inventory WHERE ID = ?",(data[0],))
        currentdata = c.fetchone()
        if currentdata:
            if data[5] == 0:
                quantity = currentdata[2]+data[2]

                c.execute("UPDATE Inventory SET Qt = ?, Pp = ? Where ID = ? ",(quantity,data[4],currentdata[0]))
            
            if data[5] == 1:
                quantity = currentdata[2]-data[2]
                if quantity < 0 :
                    return "False", currentdata[2], "Not enough in inventory"

                c.execute("UPDATE Inventory SET Qt = ?, Pp = ? Where ID = ? ",(quantity,data[4],currentdata[0]))
        
        else :
            if data[5] == 1:
                return "False", data, "You never bought it before"
            
            else :
                c.execute("INSERT INTO Inventory (ID,Item,Qt,Pp,Sp) VALUES (?,?,?,?,?)",data[0:5])
        conn.commit()
        return "True"
                    




class Testing :
    def examplepersonel(): ## Auto populate Personel table with fake data
        conn = sqlite3.connect("Data.db")
        c    = conn.cursor()

        c.executemany("""INSERT INTO Personel (ID,Name,Desc,Contact,Email) VALUES (?,?,?,?,?)""",fakepersonel)
        conn.commit()
        conn.close()

        print("Autopopulated Personel table with fake data")

    def exampleinventory(): ## Autopopulate Bill table with fake data
        conn = sqlite3.connect("Data.db")
        c    = conn.cursor()

        c.executemany("""INSERT INTO Inventory (ID,Item,Qt,Pp,Sp) VALUES (?,?,?,?,?)""",fakeinventory)
        conn.commit()
        conn.close()

        print("Autopopulated Inventory table with fake data")

    def examplebill():
        conn = sqlite3.connect("Data.db")
        c    = conn.cursor()

        c.executemany("""INSERT INTO Bill (ID,Personel,Item,Qt,Price,Date,State) VALUES (?,?,?,?,?,?,?)""",fakebills)
        conn.commit()
        conn.close()

        print("Autopopulated Personel table with fake data")

if __name__ == "__main__":
    StartUp.checklist()
    Testing.examplebill()
    Testing.exampleinventory()
    Testing.examplepersonel()