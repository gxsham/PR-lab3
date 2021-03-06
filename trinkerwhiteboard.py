from Tkinter import *
from Tkinter import Tk
import time
import threading
import select
import random
import os, binascii
from socket import *

PORT = 4444

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(('', 0))
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
sock.setblocking(0)


s = socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
s.bind(('', PORT))
s.setblocking(0)

lastx, lasty = 0, 0
canvasWidth = 500
canvasHeight = 500

color ='#'+ binascii.b2a_hex(os.urandom(3))

def doFoo(*args):
    print "Virtual event was generated"

def xy(event):
    global lastx, lasty
    lastx, lasty = event.x, event.y
    

    
def addLine(event):
    global lastx, lasty
    canvas.create_line(lastx, lasty, event.x, event.y)
    
    sock.sendto(str(lastx) + ' ' + str(lasty) + ' ' + str(event.x) + ' ' + str(event.y) + ' ' + color, ('<broadcast>', PORT))
    print lastx , lasty, color
    lastx, lasty = event.x, event.y
    

def worker(root, canvas):
	while True:
		result = select.select([s],[],[])      
		msg = result[0][0].recv(1024) 
		points = msg.split(' ') 
              
		canvas.create_line(int(points[0]), int(points[1]), int(points[2]), int(points[3]),fill = points[4])
       
        


root = Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.bind("<<Foo>>",doFoo) #event, custom (not tied to the mouse/keyboard)

canvas = Canvas(root, width=canvasWidth, height=canvasHeight, bg = "black")
canvas.grid(column=0, row=0, sticky=(N, W, E, S))
canvas.bind("<Button-1>", xy) #event, mouse-click
canvas.bind("<B1-Motion>", addLine) #event, move mouse with a clicked button


#txt = canvas.create_text(10,10, fill = "white")

def press_Yes():
    canvas.delete("all")


b = Button(canvas, text="Delete Canvas", command=press_Yes)

b.pack(side = TOP)


#start another thread, it will read stuff from the socket
#and update the canvas if needed
t = threading.Thread(target=worker, args=(root, canvas) )
t.start()

#drawing the canvas itself
root.mainloop()