# code for POC

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import serial
import matplotlib.pyplot as plt
from idlelib.tooltip import Hovertip
import tkinter.font as tkFont


root = tk.Tk()
root.title("servo motor controller")
#arduino = serial.Serial(port='COM3', baudrate=9600, timeout=0.1)
my_font = tkFont.Font(size=10)

def resizer(event):
   if event.width in range(300,325):
      my_font.configure(size=10)   
   elif event.width in range(450,500):
      my_font.configure(size=20)
   elif event.width > 600:
      my_font.configure(size=30)

#functions
def start():
    arduino.write(b's')
    msg=bytearray(6)
    
    temp=0
    if func.get()=='Sinusodial':
        temp=1
    elif func.get()=='Saw tooth':
        temp=2
    elif func.get()=='Linear':
        temp=3    
    elif func.get()=='Rectangular':
        temp=4    
        
    msg[0]=temp
    msg[1]=o.get()
    msg[2]=a.get()
    msg[3]=tp.get()
    msg[4]=d.get()
    msg[5]=c.get()
    
    arduino.write(msg)
    
    if g.get()=="ON":
        #draw_graph(temp)
        i=1
        
def pause():
    arduino.write(b'p') 
    
def stop():
    arduino.write(b'e')  



    
# labels
label1 = tk.Label(root, text="Input Function", bg="orange", relief="raised",font=my_font)
label1.grid(row=0, column=0, pady=10,padx=10, sticky='NSEW')
label2 = tk.Label(root, text="Offset", bg="orange", relief="raised",font=my_font)
label2.grid(row=1, column=0, pady=10,padx=10, sticky='NSEW')
label3 = tk.Label(root, text="Amplitude", bg="orange", relief="raised",font=my_font)
label3.grid(row=2, column=0, pady=10,padx=10, sticky='NSEW')
label4 = tk.Label(root, text="Time Period (s)", bg="orange", relief="raised",font=my_font)
label4.grid(row=3, column=0, pady=10,padx=10, sticky='NSEW')
label5 = tk.Label(root, text="Duty Cycle %", bg="orange", relief="raised",font=my_font)
label5.grid(row=4, column=0, pady=10,padx=10, sticky='NSEW')
label6 = tk.Label(root, text="Total cycles", bg="orange", relief="raised",font=my_font)
label6.grid(row=5, column=0, pady=10,padx=10, sticky='NSEW')
label7 = tk.Label(root, text="Graph_on", bg="orange", relief="raised",font=my_font)
label7.grid(row=6, column=0, pady=10,padx=10, sticky='NSEW')


# variables
o = tk.IntVar()
a = tk.IntVar()
tp = tk.IntVar()
c = tk.IntVar()
d=tk.IntVar()
g = tk.StringVar()
func = tk.StringVar()


# entries

action = ttk.Combobox(root, textvariable=func,font=my_font)
action['values'] = ('Sinusodial', 'Saw tooth', 'Linear', 'Rectangular')
action.grid(row=0, column=2, sticky='NSEW', pady=10,padx=10)

offset = tk.Entry(root, textvariable=o,font=my_font)
offset.grid(row=1, column=2, sticky='NSEW', pady=10,padx=10,)

amplitude = tk.Entry(root, textvariable=a,font=my_font)
amplitude.grid(row=2, column=2, sticky='NSEW',padx=10, pady=10)

Time_period = tk.Entry(root, textvariable=tp,font=my_font)
Time_period.grid(row=3, column=2, sticky='NSEW',padx=10, pady=10)

duty_cycle = tk.Entry(root, textvariable=d,font=my_font)
duty_cycle.grid(row=4, column=2, sticky='NSEW',padx=10, pady=10)

cycles = tk.Entry(root, textvariable=c,font=my_font)
cycles.grid(row=5, column=2, sticky='NSEW',padx=10, pady=10)

graph_on = ttk.Combobox(root, textvariable=g,font=my_font)
graph_on['values'] = ('ON', 'OFF')
graph_on.grid(row=6, column=2, sticky='NSEW',padx=10, pady=10)

myTip1 = Hovertip(offset,'Should be between 0 and 180 degree.')
myTip2 = Hovertip(amplitude,'Should be between 0 and min(offset, 180-offset) degree.')
myTip3 = Hovertip(duty_cycle,'Neccessary Only for rectangular wave')
myTip4 = Hovertip(cycles,'Should be integer')

# buttons
pause = tk.Button(root, text="PAUSE", command=pause,bg="yellow",font=my_font)
pause.grid(row=7, column=0, pady=10,padx=10, sticky='NSEW')

start = tk.Button(root, text="START", command=start,bg="green",font=my_font)
start.grid(row=7, column=1, pady=10,padx=10, sticky='NSEW')

stop= tk.Button(root, text="STOP", command=stop, bg="red",font=my_font)
stop.grid(row=7, column=2, pady=10,padx=10, sticky='NSEW')

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)
root.rowconfigure(4, weight=1)
root.rowconfigure(5, weight=1)
root.rowconfigure(6, weight=1)
root.rowconfigure(7, weight=1)


root.bind("<Configure>", resizer)
root.mainloop()
