from client.executor import Executor
from tkinter import *
from tkinter import Canvas, Entry, Label

class Connector():
    def __init__(self):
        root = Tk()
        root.title('Distiller client')

        ls = Label(text='Server address: ').pack(side=TOP, padx=10, pady=10)
        self.entrys = Entry(root, width=20)
        self.entrys.pack(side=TOP,padx=10,pady=10)

        lc = Label(text='Local address: ').pack(side=TOP, padx=10, pady=10)
        self.entryc = Entry(root, width=20)
        self.entryc.pack(side=TOP,padx=10,pady=10)

        lcp = Label(text='Port: ').pack(side=TOP, padx=10, pady=10)
        self.entrycp = Entry(root, width=20)
        self.entrycp.pack(side=TOP,padx=10,pady=10)

        Button(root, text='OK', command=self.onRegister).pack(side=LEFT)
        self.root = root

    def start(self):
        self.root.mainloop()

    def onRegister(self):
        serveraddr = self.entrys.get()
        clientaddr = self.entryc.get()
        clientport = self.entrycp.get()

        self.root.destroy()

        MainGUI(serveraddr, clientport, clientaddr).start()

class MainGUI():
    def __init__(self, serveraddr, clientport, clientaddr):
        self.exe = Executor(serveraddr, clientport, clientaddr)

        top = Tk()
        text = Text(top)
        text.pack()

        import sys
        sys.stdout = Std_redirector(text)
        top.mainloop()

class Std_redirector(object):
    def __init__(self,widget):
        self.widget = widget

    def write(self,string):
        self.widget.insert(END,string)
        self.widget.see(END)

Connector().start()
