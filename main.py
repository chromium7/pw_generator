from tkinter import *
import random
import string

alphabets_lower = string.ascii_lowercase
alphabets_upper = string.ascii_uppercase
symbols = string.punctuation + " "
digits = string.digits

def generate_pw():
    selection = ""
    if var1.get() == 1:
        selection += alphabets_lower
    if var2.get() == 1:
        selection += alphabets_upper
    if var3.get() == 1:
        selection += digits
    if var4.get() == 1:
        selection += symbols
    password = "".join(random.choices(selection, k=length_scale.get()))
    password_lbl.config(text= password)

root = Tk()
root.title("Pepeg Password Generator")
root.geometry("460x350")
root.iconbitmap("pepeg.ico")
root.configure(background="#B3F4D9")

title_label = Label(root, text="Pepeg Random Generator", font= "Helvetica 24 bold", fg="#456f95", bg="#B3F4D9")
title_label.pack()

frame= LabelFrame(root, padx= 10, pady= 5, bg="#B3F4D9", borderwidth=0, highlightthickness=0)
frame.pack(padx=5, pady=2)

character_label = Label(frame,text="Select characters:", font= "Helvetica 16 bold", fg="#314DB4", bg="#B3F4D9")
character_label.grid()

var1 = IntVar()
var2 = IntVar()
var3 = IntVar()
var4 = IntVar()

char_box_1 = Checkbutton(frame, text="Lowercase Alphabet", variable= var1, font="Helvetica 10",bg="#B3F4D9")
char_box_2 = Checkbutton(frame, text="Uppercase Alphabet", variable= var2, font="Helvetica 10",bg="#B3F4D9")
char_box_3 = Checkbutton(frame, text="Digits", variable= var3, font="Helvetica 10",bg="#B3F4D9")
char_box_4 = Checkbutton(frame, text="Symbols", variable= var4, font="Helvetica 10",bg="#B3F4D9")
char_box_1.grid(stick= W)
char_box_2.grid(stick= W)
char_box_3.grid(stick= W)
char_box_4.grid(stick= W)


length_label = Label(root, text="Password Length", font= "Helvetica 16 bold", fg="#314DB4",bg="#B3F4D9")
length_label.pack()

length_scale = Scale(root, from_= 4, to= 16, orient= HORIZONTAL, length=200,bg="#B3F4D9", borderwidth=0, highlightthickness=0)
length_scale.set(10)
length_scale.pack()

generate_button = Button(root, text="Generate Password", font= "Helvetica 12", command= generate_pw,width= 20, bg="#DAB43D")
generate_button.pack()

password_lbl = Label(root, text="**********", pady=10, font="Helvetica 10",bg="#B3F4D9")
password_lbl.pack()

root.mainloop()