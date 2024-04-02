##This is the file responsible for the camera/barcodescanner##

##Imports
import cv2
from pyzbar.pyzbar import 

##Personal Libraries
import GUItool
import Commandtool
import DBtool

def scanbarcode(frame):

    ## Turns one frame gray, then checks for any barcode/qr code in the image
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    barcodes = decode(gray)

    for barcode in barcodes:
        ID       = barcode.data.decode('utf-8')
        datatype = barcode.type
        data = DBtool.getinfo.item((str(ID)))

        GUItool.autofill.entry(data)

def barcodescanner():
    
    ## Turns on default camera in computer
    camera = cv2.VideoCapture(0)

    framecount = 0

    ##Ensures camera is running, breaks if its turned off, and captures one frame every five frames
    while camera.isOpened():
        ret, frame = camera.read()
        if not ret :
            break
        
        framecount += 1
        if framecount %5 == 0:
            scanbarcode(frame)


if __name__ == '__main__' :
    barcodescanner()
    