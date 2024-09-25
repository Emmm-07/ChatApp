import socket
import threading
import tkinter as tk
from tkinter import scrolledtext 
from tkinter import messagebox

HOST = '127.0.0.1'
PORT = 1234

root = tk.Tk()
root.geometry("600x600")
root.title("My Chat app")
root.resizable("False","False") 

DARK_GREY = "#121212"
MEDIUM_GREY = "#1f1b24"
OCEAN_BLUE = "#464EB8"
FONT = ("Helvetica",17)
# creating the socket class object
# AF_INET: uses IPV4 address
# SOCK_STREAM: TCP , SOCK_DGRAM: UDP
client= socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def connect(): 
    username = username_textbox.get()
    try:
        client.connect((HOST,PORT))
        #add_message(f"[SERVER]: {username} joined the chat")
    except:
        messagebox.showerror("Connection error",f"Unable to connect to server {HOST} {PORT}")
         
    
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid username","Username cannot be empty")
         
    threading.Thread(target=listen_for_msgs_from_server,args=(client, )).start()

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END,message + '\n')
    message_box.config(state=tk.DISABLED)

def send_button():
    msg= message_textbox.get()
    print(msg)
    if msg != '':
        client.sendall(msg.encode())
        message_textbox.delete(0,len(msg))
    else:
        messagebox.showerror("Empty message","Message cannot be empty")


root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root,width="600",height="100",bg=DARK_GREY)
top_frame.grid(row=0,column=0,sticky=tk.NSEW)

mid_frame = tk.Frame(root,width="600",height="400",bg=MEDIUM_GREY)
mid_frame.grid(row=1,column=0,sticky=tk.NSEW)

bot_frame = tk.Frame(root,width="600",height="100",bg=DARK_GREY)
bot_frame.grid(row=2,column=0,sticky=tk.NSEW)

username_label = tk.Label(top_frame,text = "Enter username:",font=FONT,bg=DARK_GREY, fg="white")
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame,font=FONT,bg=MEDIUM_GREY, fg="white", width=23)
username_textbox.pack(side=tk.LEFT)

username_button =  tk.Button(top_frame,text="Join Chat",font=("Helvetica",10),bg=OCEAN_BLUE, fg="white",command=connect)
username_button.pack(side=tk.LEFT,padx=15)

message_textbox = tk.Entry(bot_frame, font=FONT,bg=MEDIUM_GREY, fg="white", width=38)
message_textbox.pack(side=tk.LEFT, padx=10)

message_button =  tk.Button(bot_frame,text="Send",font=("Helvetica",15),bg=OCEAN_BLUE, fg="white",command=send_button)
message_button.pack(side=tk.LEFT,padx=13)

message_box = scrolledtext.ScrolledText(mid_frame, font=("Helvetica",13), bg=MEDIUM_GREY, fg="white", width=67, height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)




def listen_for_msgs_from_server(client):
    while True:
        message =  client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split(":")[0]
            content = message.split(":")[1]
            add_message(f"{username}: {content}")
        else:
            messagebox.showerror("Empty message",f"Message received from {username}is empty")


def main():
    root.mainloop()

if __name__ == '__main__':
    main()
    