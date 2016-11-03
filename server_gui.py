from server.manager import Manager
from server.parser import Parser
import threading
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from time import sleep

top = Tk()

def GoCallBack():
	if len(man.clients)>0:
		filename = askopenfilename()
		par.exec_file(filename)
	else:
		messagebox.showinfo( "Warning", "No clients connected")

B = Button(top, text ="Enter", command = GoCallBack)
B.pack()

client_cont =  Frame(top)
client_label = Label(client_cont, text='Number of clients: ').pack(side=LEFT)
clien_count = Entry(client_cont, width=20)
clien_count.pack(side=RIGHT)
client_cont.pack()

text = Text(top)
text.pack()

def update():
    while True:
        count = len(man.clients)
        clien_count.delete(0, END)
        clien_count.insert(0, str(count))
        sleep(1)

class Std_redirector(object):
    def __init__(self,widget):
        self.widget = widget

    def write(self,string):
        self.widget.insert(END,string)
        self.widget.see(END)

import sys
sys.stdout = Std_redirector(text)

man = Manager()
par = Parser(man)

thread1 = threading.Thread(target=update)
thread1.start()

top.mainloop()
