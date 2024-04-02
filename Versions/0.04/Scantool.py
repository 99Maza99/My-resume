# barcode_scanner.py
"""import tkinter
import cv2
from pyzbar.pyzbar import decode
import threading

class Scanner:
    def __init__(self, entry_widget=None, scantype = "Barcode"): ##Creates an instance of barcode scanner
        self.entry_widget = entry_widget  #Takes in entry widget instance
        self.scantype     = scantype      #Takes in the type of search
        self.running      = True          #Sets the standard of instance to be running

    def read_codes(self, frame):
        codes = decode(frame)
        for barcode in codes:
            code_data = barcode.data.decode('utf-8')
            data_type = barcode.type

            if data_type in ["EAN-13", "EAN-8", "UPC-A", "UPC-E"] and self.scantype == "Barcode":
                if self.entry_widget:
                    if self.entry_widget.get()=="":
                        self.entry_widget.insert(0,code_data)
                        print(f"Found barcode: {data_type} {code_data}")
                        return frame
                    else :
                        print(f"Found barcode: {data_type} {code_data}")
                        return frame
            
            if data_type == "QR code" and self.scantype == "QR code":
                if self.entry_widget:
                    if self.entry_widget.get()=="":
                        self.entry_widget.insert(0,code_data)
                        print(f"Found barcode: {data_type} {code_data}")
                        return frame
                    else :
                        print(f"Found barcode: {data_type} {code_data}")
                        return frame


        return frame

    def start_scanning(self):
        print("Running")
        self.running = True
        camera = cv2.VideoCapture(0)
        while self.running:
            ret, frame = camera.read()
            if ret:
                self.read_barcodes(frame)
            if cv2.waitKey(1) & 0xFF == 27:  # Optional: Exit loop with ESC key
                break
        camera.release()
        cv2.destroyAllWindows()

    def start(self):
        if not self.running:
            threading.Thread(target=self.start_scanning).start()

    def stop(self):
        self.running = False"""


# barcode_scanner.py
import cv2
from pyzbar.pyzbar import decode
import threading

class Scanner:
    def __init__(self, entry_widget=None, scantype="EntryGUI"):
        self.entry_widget = entry_widget
        self.scantype = scantype
        self.running = False  # Note: Changed to False to align with start method logic
    
    def read_codes(self, frame):
        codes = decode(frame)
        for barcode in codes:
            code_data = barcode.data.decode('utf-8')
            data_type = barcode.type
            print(code_data)
            print(data_type)

            # Corrected condition
            if self.scantype == "EntryGUI" :
                if data_type in ["EAN13", "EAN8"]:
                    if self.entry_widget[0].get()=="":
                        self.entry_widget[0].insert(0,code_data)
            
                if data_type == "QRCODE":
                    if self.entry_widget[1].get()=="":
                        self.entry_widget[1].insert(0,code_data)
            


    def start_scanning(self):
        self.running = True
        for index in range(0,2): ##Checks for secondary camera if it exists
            cap = cv2.VideoCapture(index)
            if cap.isOpened():
                cap.release()
                num = index
                print(num)
        
        camera = cv2.VideoCapture(num) ##Connects to secondary cam, if its not there it connects to the main one

        while self.running:
            ret, frame = camera.read()
            if ret:
                self.read_codes(frame)
            if cv2.waitKey(1) & 0xFF == 27:  # Optional: ESC key stops the loop
                self.stop()
                break
        camera.release()
        cv2.destroyAllWindows()

    def start(self):
        if not self.running:
            self.thread = threading.Thread(target=self.start_scanning)
            self.thread.daemon = True  # This makes the thread a daemon thread
            self.thread.start()

    def stop(self):
        self.running = False
