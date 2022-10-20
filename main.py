import time
import tkinter
import tkinter.messagebox
from tkinter import scrolledtext
from tkinter import *
import socket
import threading
from tkinter import simpledialog

import RSA
import encryption
import steg

HOST = '127.0.0.1'
PORT = 8080


class User:
    receiver_name = ''
    key_dict = {}
    sym_key_enc_dict = {}
    sent_key = False
    def __init__(self):
        self.win = tkinter.Tk()
        self.win.withdraw()
        self.names = ["pick a name"]
        self.name = simpledialog.askstring(title="name", prompt="what is you name?")
        self.private_key = RSA.gen_keys(self.name)
        self.sym_key = encryption.gen_sym_key()
        #self.sym_key_enc = RSA.encrypt(self.sym_key.decode(), self.name)
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
        self.window.mainloop()

    def listen(self):
        while True:
            msg = self.s.recv(1024).decode()
            print(msg)
            if msg == "name":
                self.s.send(self.name.encode())
            elif "key:" in msg:
                try:
                    msg = msg[msg.find(",")+1:]
                    print(msg)
                    name = msg[:msg.find(",")]
                    key = (msg[msg.find(":")+4:-1]).encode().decode('unicode_escape').encode("raw_unicode_escape")
                    key = RSA.decrypt(key, self.private_key)
                    self.sym_key_enc_dict[name] = key

                except:
                    pass
            elif "new user:" in msg:
                name = msg[msg.find(":")+1:]
                try:
                    self.sym_key_enc = RSA.encrypt(self.sym_key.decode(), name)
                    self.s.send(f"{name},{self.name},key: {self.sym_key_enc}".encode())
                except:
                    pass
            elif "LON" in msg:
                self.names = msg[7:-1].replace("'", "")
                self.names = self.names.split(",")
                menu = self.nameList["menu"]
                menu.delete(0, "end")
                print(self.names)
                for name in self.names:
                    menu.add_command(label=name.strip(" "),
                                     command=lambda value=name: self.namevar.set(value))
            else:

                name = msg[:msg.find(",")]
                try:
                    msg = encryption.decrypt_text(msg.encode(), self.sym_key_enc_dict[self.receiver_name])
                    msg = msg[msg.find(',')+1:]
                    msg = steg.extract(msg)
                    msg = encryption.decrypt_text(msg.encode(), self.sym_key_enc_dict[self.receiver_name])
                    if msg[:msg.find(":")] == self.receiver_name:
                        self.msghist.config(state="normal")
                        self.msghist.insert(tkinter.END, f"{msg}")
                        self.msghist.yview(tkinter.END)
                        self.msghist.config(state="disabled")
                except:
                    pass

    def send_message(self):
        msg = self.msgbox.get("1.0", tkinter.END)
        self.msgbox.delete("1.0", tkinter.END)
        self.msghist.config(state="normal")
        self.msghist.insert(tkinter.END, f"{self.name}: {msg}")
        self.msghist.yview(tkinter.END)
        self.msghist.config(state="disabled")
        msg = encryption.encrypt_text(f"{self.name}: {msg}", self.sym_key).decode()
        filename = steg.embedTxt(msg, "audios/handel.wav")
        msg = f"{self.receiver_name},{filename}"
        msg = encryption.encrypt_text(f"{self.name}: {msg}", self.sym_key).decode()
        self.s.send(msg.encode())

        self.msghist.config(state="normal")
        msghist = self.msghist.get("1.0", tkinter.END)
        self.msghist.config(state="disabled")

        msghist_enc = encryption.encrypt_text(f"{msghist}", self.sym_key).decode()
        steg.embedTxtHist(msghist_enc, "audios/handel.wav", self.name, self.receiver_name)

    def get_names(self):
        self.s.send("LON".encode())

    def name_select(self, *args):
        self.receiver_name = self.namevar.get().strip(" ")
        #self.s.send(f"new receiver,{self.receiver_name}".encode())

        self.sym_key_enc = RSA.encrypt(self.sym_key.decode(), self.receiver_name)
        self.s.send(f"{self.receiver_name},{self.name},key: {self.sym_key_enc}".encode())
        try:
            names = [self.name, self.receiver_name]
            names.sort()
            filename = f"audios/{names[0]},{names[1]}embedded.wav"
            print(filename)
            msg = steg.extract(filename)
            print("here")
            msg = encryption.decrypt_text(msg.encode(), self.sym_key_enc_dict[self.receiver_name])
            print(msg)
            msg = msg.rstrip("\n ")
            self.msghist.config(state="normal")
            self.msghist.delete("1.0", END)
            self.msghist.insert(tkinter.END, f"{msg}\n")
            self.msghist.yview(tkinter.END)
            self.msghist.config(state="disabled")
        except:
            self.msghist.config(state="normal")
            self.msghist.delete("1.0", END)
            self.msghist.insert(tkinter.END, f"start chatting with {self.receiver_name}\n")
            self.msghist.yview(tkinter.END)
            self.msghist.config(state="disabled")


if __name__ == '__main__':
    u = User()



