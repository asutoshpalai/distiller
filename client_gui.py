from client.executor import Executor
from tkinter import *
from tkinter import Canvas, Entry, Label

root = Tk()
root.title('Distiller client')

ls = Label(text='Server address: ').pack(side=TOP, padx=10, pady=10)
entrys = Entry(root, width=20)
entrys.pack(side=TOP,padx=10,pady=10)

lc = Label(text='Local address: ').pack(side=TOP, padx=10, pady=10)
entryc = Entry(root, width=20)
entryc.pack(side=TOP,padx=10,pady=10)

lcp = Label(text='Port: ').pack(side=TOP, padx=10, pady=10)
entrycp = Entry(root, width=20)
entrycp.pack(side=TOP,padx=10,pady=10)


def onRegister():
    serveraddr = entrys.get()
    clientaddr = entryc.get()
    clientport = entrycp.get()
    Executor(serveraddr, clientport, clientaddr)

Button(root, text='OK', command=onRegister).pack(side=LEFT)
root.mainloop()