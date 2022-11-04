import random
import time
import tkinter
import tkinter.messagebox
from tkinter import scrolledtext
from tkinter import *
import socket
import threading
from tkinter import simpledialog
import diffie
import RSA
import encryption
import steg

HOST = '127.0.0.1'
PORT = 8080


class User:
    receiver_name = ''
    key_dict = {}
    a = 4
    p=1
    r=1
    sym_key_enc_dict = {}
    busy = False
    num_of_peopele =0
    def __init__(self):
        self.win = tkinter.Tk()
        self.win.withdraw()
        self.names = ["pick a name"]
        self.name = simpledialog.askstring(title="name", prompt="what is you name?")
        self.s = socket.socket()
        self.s.connect((HOST, PORT))
        self.recv_thread = threading.Thread(target=self.listen)
        self.gui_thread = threading.Thread(target=self.gui)
        self.gui_thread.start()
        time.sleep(1)
        self.recv_thread.start()

    def gui(self):
        self.window = tkinter.Tk()
        self.namevar = StringVar(self.window)
        self.namevar.set(self.names[0])
        self.namevar.trace('w', self.name_select)
        self.nameList = OptionMenu(self.window, self.namevar, *self.names)
        self.nameList.pack(side=RIGHT)
        self.msghist = tkinter.scrolledtext.ScrolledText(self.window, height="20")
        self.msghist.pack()
        self.msghist.config(state="disabled")
        self.msgbox = tkinter.Text(self.window, height="5")
        self.msgbox.pack()
        self.sendbtn = tkinter.Button(self.window, text="send message", command=self.send_message)
        self.sendbtn.pack()
        self.window.winfo_toplevel().title(f"{self.name}")
        self.window.protocol("WM_DELETE_WINDOW", self.closing)
        self.window.mainloop()

    def closing(self):
        self.s.close()
        self.window.destroy()
    def listen(self):
        while True:
            if self.busy == True:
                time.sleep(2)
            rec_msg = self.s.recv(1024).decode()
            self.busy = True
            #print(rec_msg)
            if rec_msg == "name":
                self.s.send(self.name.encode())
            elif "pub_key:" in rec_msg:
                try:
                    my_name = rec_msg[:rec_msg.find(",")]
                    their_name = rec_msg[rec_msg.find(",")+1:rec_msg.find("\'")]
                    p = int(rec_msg[rec_msg.find(":")+1:rec_msg.find(";")])
                    r = int(rec_msg[rec_msg.find(";")+1:rec_msg.find(".")])
                    A = int(rec_msg[rec_msg.find(".")+1:])
                    b = random.randint(1,50)

                    B = diffie.calc_pub_key(p,r,b)

                    secretkey = diffie.calc_secret_key(p,A,b)
                    self.key_dict[their_name] = secretkey

                    key_msg2 = f"{their_name},{self.name}'pubkey:{B}"
                    #print(key_msg2)
                    self.s.send(key_msg2.encode())

                except:
                    print("error in receiving key")
            elif "pubkey" in rec_msg:
                try:
                    my_name = rec_msg[:rec_msg.find(",")]
                    their_name = rec_msg[rec_msg.find(",") + 1:rec_msg.find("\'")]
                    B = int(rec_msg[rec_msg.find(":")+1:])
                    self.key_dict[their_name] = diffie.calc_secret_key(self.p,B,self.a)
                except:
                    print("error in key2")

            elif "new user:" in rec_msg:
                name = rec_msg[rec_msg.find(":")+1:]
                try:
                    if name != self.name:
                        self.p = diffie.get_prime()
                        self.r = random.randint(1, 50)
                        self.a = random.randint(1,50)
                        A = diffie.calc_pub_key(self.p,self.r,self.a)
                        time.sleep(random.randint(0,self.num_of_peopele))
                        key_msg = f"{name},{self.name}'pub_key:{self.p};{self.r}.{A}"
                        self.s.send(key_msg.encode())

                except:
                    pass

            elif "LON" in rec_msg:
                self.names = rec_msg[7:-1].replace("'", "")
                self.names = self.names.split(",")
                menu = self.nameList["menu"]
                menu.delete(0, "end")
                self.num_of_peopele = len(self.names)
                #print(self.names)
                for name in self.names:
                    if name.strip(" ") != self.name:
                        menu.add_command(label=name.strip(" "), command=lambda value=name: self.namevar.set(value))
            else:


                try:
                    my_name = rec_msg[:rec_msg.find(',')]
                    their_name = rec_msg[rec_msg.find(',') + 1: rec_msg.find("\'")]
                    rec_msg = rec_msg[rec_msg.find("\'"):]
                    rec_msg = encryption.decrypt_text(rec_msg.encode(), self.key_dict[self.receiver_name])
                    rec_msg = steg.extract(rec_msg)
                    rec_msg = encryption.decrypt_text(rec_msg.encode(), self.key_dict[self.receiver_name])
                    if their_name == self.receiver_name:
                        self.msghist.config(state="normal")
                        self.msghist.insert(tkinter.END, f"{their_name}: {rec_msg}")
                        self.msghist.yview(tkinter.END)
                        self.msghist.config(state="disabled")
                except:
                    pass
            self.busy = False
            #print(self.key_dict)
    def send_message(self):
        msg = self.msgbox.get("1.0", tkinter.END)
        self.msgbox.delete("1.0", tkinter.END)
        self.msghist.config(state="normal")
        self.msghist.insert(tkinter.END, f"{self.name}: {msg}")
        self.msghist.yview(tkinter.END)
        self.msghist.config(state="disabled")
        msg = encryption.encrypt_text(f"{msg}", self.key_dict[self.receiver_name]).decode()
        filename = steg.embedTxt(msg, "audios/handel.wav")
        msg = f"{filename}"
        msg = encryption.encrypt_text(f"{msg}", self.key_dict[self.receiver_name]).decode()
        msg = f"{self.receiver_name},{self.name}\'{msg}"
        self.s.send(msg.encode())

        self.msghist.config(state="normal")
        msghist = self.msghist.get("1.0", tkinter.END)
        self.msghist.config(state="disabled")

        msghist_enc = encryption.encrypt_text(f"{msghist}", self.key_dict[self.receiver_name]).decode()
        steg.embedTxtHist(msghist_enc, "audios/handel.wav", self.name, self.receiver_name)

    def get_names(self):
        self.s.send("LON".encode())

    def name_select(self, *args):
        self.receiver_name = self.namevar.get().strip(" ")
        #self.s.send(f"new receiver,{self.receiver_name}".encode())

        #self.sym_key_enc = RSA.encrypt(self.sym_key.decode(), self.receiver_name)
        #self.s.send(f"{self.receiver_name},{self.name},key: {self.sym_key_enc}".encode())
        try:
            names = [self.name, self.receiver_name]
            names.sort()
            filename = f"audios/{names[0]},{names[1]}embedded.wav"
            #print(filename)
            msg = steg.extract(filename)
            #print("here")
            msg = encryption.decrypt_text(msg.encode(), self.key_dict[self.receiver_name])
           # print(msg)
            msg = msg.rstrip("\n ")
            self.msghist.config(state="normal")
            self.msghist.delete("1.0", END)
            self.msghist.insert(tkinter.END, f"{msg}\n")
            self.msghist.yview(tkinter.END)
            self.msghist.config(state="disabled")
        except:
            self.msghist.config(state="normal")
            self.msghist.delete("1.0", END)
            self.msghist.yview(tkinter.END)
            self.msghist.config(state="disabled")


if __name__ == '__main__':
    u = User()



