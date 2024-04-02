##Imported Libraries
from threading import Thread

##Imported Libraries made by myself uwu
import DBtool
import EntryGUI
import Scantool


if __name__ == "__main__":
    DBtool.Database.checklist()

    ## Starts threads for the phone scanner and the main GUI
    scanner   = Thread(target= Scantool.barcodescanner)
    scanner.daemon = True

    
    scanner.start()

    EntryGUI
