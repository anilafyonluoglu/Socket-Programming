# import all the required  modules
import socket
import threading
from tkinter import *
from tkinter import font
from tkinter import ttk
from asynchat import *

PORT = 52345
SERVER = "172.20.10.6"

FORMAT = "utf-8"

# Creating a new TCP socket
# connected to the server
client = socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM)
client.connect((SERVER, PORT))


# Graphic part
class GUI:
    # constructor method
    def __init__(self):

        # chat window but hidden right now
        self.Root = Tk()
        self.Root.withdraw()

        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        self.login.resizable(width=False,
                             height=False)
        self.login.configure(width=400,
                             height=300)
        # create a Label
        self.pls = Label(self.login,
                         text="Please login to continue",
                         justify=CENTER,
                         font="Arial 14 bold")

        self.pls.place(relheight=0.15,
                       relx=0.2,
                       rely=0.07)
        # create a Label
        self.labelName = Label(self.login,
                               text="Name: ",
                               font="Arial 12")

        self.labelName.place(relheight=0.2,
                             relx=0.1,
                             rely=0.2)

        # create an input
        # typing the message
        self.entryName = Entry(self.login,
                               font="Helvetica 14")

        self.entryName.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.35,
                             rely=0.2)


        self.entryName.focus()

        # create a Continue Button
        # along with action
        self.go = Button(self.login,
                         text="CONTINUE",
                         font="Helvetica 14 bold",
                         command=lambda: self.goAhead(self.entryName.get()))

        self.go.place(relx=0.4,
                      rely=0.55)
        self.Root.mainloop()

    def goAhead(self, name):
        self.login.destroy()
        self.edit(name)

        # the thread to receive messages
        rcv = threading.Thread(target=self.receive)
        rcv.start()

    # editing part
    def edit(self, name):
#Every color has a different codes.
        self.id = name
        # to show chat window
        self.Root.deiconify()
        self.Root.title("CHATBOX")
        self.Root.resizable(width=False,
                            height=False)
        self.Root.configure(width=470,
                            height=550,
                            bg="#17202A")
        self.labelHead = Label(self.Root,
                               bg="#17202A",
                               fg="#EAECEE",
                               text=self.id,
                               font="Helvetica 13 bold",
                               pady=5)

        self.labelHead.place(relwidth=1)
        self.line = Label(self.Root,
                          width=450,
                          bg="#ABB2B9")

        self.line.place(relwidth=1,
                        rely=0.07,
                        relheight=0.012)

        self.textCons = Text(self.Root,
                             width=20,
                             height=2,
                             bg="blue",  ##TEXT EKRANI
                             font="Helvetica 14",
                             padx=5,
                             pady=5)

        self.textCons.place(relheight=0.745,
                            relwidth=1,
                            rely=0.08)

        self.labelBottom = Label(self.Root,
                                 bg="white",
                                 height=80)

        self.labelBottom.place(relwidth=1,
                               rely=0.825)

        self.entryMsg = Entry(self.labelBottom,
                              bg="#2C3E50",
                              font="Arial 13")

        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth=0.74,
                            relheight=0.06,
                            rely=0.008,
                            relx=0.011)

        self.entryMsg.focus()

        #Creating a send button
        self.buttonMsg = Button(self.labelBottom,
                                text="Send",
                                font="Arial 10 bold",
                                width=20,
                                bg="#ABB2B9",
                                command=lambda: self.sendButton(self.entryMsg.get()))

        self.buttonMsg.place(relx=0.77,
                             rely=0.008,
                             relheight=0.12,
                             relwidth=0.25)

        self.textCons.config(cursor="arrow")

        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)

        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight=1,
                        relx=0.974)

        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state=DISABLED)

    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        snd = threading.Thread(target=self.sendMessage)
        snd.start()

    # function to receive messages
    def receive(self):
        while True:
            try:
                message = client.recv(1024).decode(FORMAT)

                # if the messages from the server is NAME send the client's name
                if message == 'NAME':
                    client.send(self.id.encode(FORMAT))
                else:
                    # insert messages to text box
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END,
                                         message + "\n\n")

                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
            except:
                # an error will be printed on the command line or console if there's an error
                print("An error occured!")
                client.close()
                break

    # function to send messages
    def sendMessage(self):
        self.textCons.config(state=DISABLED)
        while True:
            message = (f"{self.id}: {self.msg}")
            client.send(message.encode(FORMAT))
            break


# create a GUI class object
g = GUI()