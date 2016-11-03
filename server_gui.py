from server.manager import Manager
from server.parser import Parser
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

man = Manager()
top = Tk()

def GoCallBack():
	if len(man.clients)>0:
		filename = askopenfilename()
		par = Parser(man)
		par.exec_file(filename)
		import os
		os.kill(os.getpid(), 9)
	else:
		messagebox.showinfo( "Warning", "No clients connected")
B = Button(top, text ="Enter", command = GoCallBack)
B.pack()

top.mainloop()

