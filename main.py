from tkinter import *
from tkinter import messagebox
import sqlite3
import string

root = Tk()
root.title("Login")
root.geometry("376x220+500+250")
root.resizable(False, False)
# create database
'''
acc_db = sqlite3.connect("accounts.db")
c = acc_db.cursor()
c.execute("""CREATE TABLE account(
            name text,
            email text,
            password text)""")
acc_db.commit()
acc_db.close()'''


def login():
    with sqlite3.connect("accounts.db") as acc_db:
        c = acc_db.cursor()
        c.execute("SELECT name,password FROM account")
        acc = c.fetchall()
        res = (identry.get(), pwentry.get())
        if res in acc:
            mainframe.destroy()
            welcome = Label(root, text="WELCOME \nTO \nTHE \nLEATHERCLUB \n{}!".format(res[0]), font="Helvetica 24")
            welcome.pack()


def signup():
    def createacc():
        try:
            if not name_entry.get() or not email_entry.get() or not pw_entry.get() or not pw2_entry.get():
                messagebox.showerror("Error", "Don't leave any box empty!")
                raise ValueError
            if len(pw_entry.get()) < 6:
                messagebox.showerror("Error", "Password should be at least 6 characters")
                raise ValueError
            if "@" not in email_entry.get():
                messagebox.showerror("Error", "Please enter a valid email")
                raise ValueError
            if pw_entry.get() != pw2_entry.get():
                messagebox.showerror("Error", "Inconsistent Password")
                raise ValueError
            with sqlite3.connect("accounts.db") as acc_db:
                c = acc_db.cursor()
                c.execute("SELECT name,email FROM account")
                acc = c.fetchall()
                if email_entry.get() in str(acc).lower():
                    messagebox.showerror("Error", "Account already exists")
                    raise ValueError
                if name_entry.get() in str(acc).lower():
                    messagebox.showerror("Error", "Username is taken")
                    raise ValueError
            response = messagebox.askyesno("Confirm", "Is everything good?")
            if response == 1:
                with sqlite3.connect("accounts.db") as acc_db:
                    c = acc_db.cursor()
                    c.execute("INSERT INTO account VALUES(:name, :email, :password)",
                              {"name": name_entry.get(),
                               "email": email_entry.get(),
                               "password": pw_entry.get()})
                    acc_db.commit()
                suwin.destroy()
            else:
                pass
        except ValueError:
            pass

    def countscore(x):
        score = 1
        upper = ""
        symbols = ""
        digits = ""
        for char in x:
            if char in string.ascii_uppercase:
                upper += char
            if char in string.digits:
                digits += char
            if char in string.punctuation:
                symbols += char
        if len(upper) >= 1:
            score += 1
        if len(upper) >= 2:
            score += 1
        if len(digits) >= 1:
            score += 1
        if len(digits) >= 2:
            score += 1
        if len(symbols) >= 1:
            score += 1
        if len(symbols) >= 2:
            score += 1
        if len(x) >= 6:
            score += 1
        if len(x) >= 9:
            score += 1
        return score

    def strength(*args):
        pw_input = pw_var.get()
        score = countscore(pw_input)
        if score <= 3:
            str_lbl.configure(text="Password Strength: Weak", bg="red")
        elif 3 < score <= 6:
            str_lbl.configure(text="Password Strength: Moderate", bg="orange")
        elif score > 6:
            str_lbl.configure(text="Password Strength: Strong", bg="green")

    def showpw():
        if show_var.get() == 1:
            pw_entry.configure(show="")
        elif show_var.get() == 0:
            pw_entry.configure(show="*")
        if show_var2.get() == 1:
            pw2_entry.configure(show="")
        elif show_var2.get() == 0:
            pw2_entry.configure(show="*")

    suwin = Toplevel()
    suwin.title("Sign Up")
    suwin.geometry("260x280+{}+{}".format(root.winfo_screenwidth() // 2 - 130, root.winfo_screenheight() // 2 - 140))
    suwin.resizable(False, False)

    sutitle_lbl = Label(suwin, text="Create an account", font="Helvetica 20 bold")
    sutitle_lbl.grid(row=0, column=0, columnspan=2, sticky=EW)
    name_lbl = Label(suwin, text="Enter your name:")
    name_lbl.grid(row=1, column=0, sticky=W)
    name_entry = Entry(suwin, width=38)
    name_entry.grid(row=2, column=0, columnspan=2, sticky=W)
    email_lbl = Label(suwin, text="Enter your email:")
    email_lbl.grid(row=3, column=0, sticky=W)
    email_entry = Entry(suwin, width=38)
    email_entry.grid(row=4, column=0, columnspan=2, sticky=W)
    pw_lbl = Label(suwin, text="Enter a password:")
    pw_lbl.grid(row=5, column=0, sticky=W)
    pw_var = StringVar()
    pw_entry = Entry(suwin, show="*", textvariable=pw_var)
    pw_var.trace("w", strength)
    pw_entry.grid(row=6, column=0)
    show_var = IntVar()
    show_box1 = Checkbutton(suwin, text="Show password", variable=show_var, command=showpw)
    show_box1.grid(row=6, column=1)
    str_lbl = Label(suwin, text="Password Strength", bg="grey")
    str_lbl.grid(row=7, column=0, columnspan=2, sticky=W)
    pw2_lbl = Label(suwin, text="Confirm your password:")
    pw2_lbl.grid(row=8, column=0, sticky=W)
    pw2_entry = Entry(suwin, show="*")
    pw2_entry.grid(row=9, column=0)
    show_var2 = IntVar()
    show_box2 = Checkbutton(suwin, text="Show password", variable=show_var2, command=showpw)
    show_box2.grid(row=9, column=1)
    subutton = Button(suwin, text="Create an account!", command=createacc)
    subutton.grid(row=10, column=0, columnspan=2)


def deleteacc():
    def sub():
        def delete():
            with sqlite3.connect("accounts.db") as acc_db:
                c = acc_db.cursor()
                c.execute("DELETE from account where oid= " + id_entry.get())
                id_entry.delete(0, END)
                acc_db.commit()

        def show():
            with sqlite3.connect("accounts.db") as acc_db:
                c = acc_db.cursor()
                c.execute("SELECT *,oid FROM account")
                accs = c.fetchall()
                print_accs = ""
                for acc in accs:
                    print_accs += f"ID: {acc[3]}, username: {acc[0]}, email: {acc[1]}, password: {acc[2]}\n"
                rec_lbl.configure(text=print_accs)

        if pw_entry.get() == "password123":
            pw_window.destroy()
            n = Toplevel()
            n.title("Delete an account")
            n.geometry(
                "500x300+{}+{}".format(root.winfo_screenwidth() // 2 - 250, root.winfo_screenheight() // 2 - 150))
            id_lbl = Label(n, text="ID Number:")
            id_lbl.pack(ipadx=15)
            id_entry = Entry(n)
            id_entry.pack()
            delete_btn = Button(n, text="Delete", command=delete)
            delete_btn.pack()
            show_btn = Button(n, text="Show accounts", command=show)
            show_btn.pack()
            rec_lbl = Label(n)
            rec_lbl.pack()

    pw_window = Toplevel()
    pw_window.title("Enter Password")
    pw_window.geometry("150x60+{}+{}".format(root.winfo_screenwidth() // 2 - 75, root.winfo_screenheight() // 2 - 30))
    pw_entry = Entry(pw_window, show="*")
    pw_entry.pack()
    sub_btn = Button(pw_window, text="submit", command=sub)
    sub_btn.pack()


mainframe = Frame(root)
mainframe.pack()
titlelbl = Label(mainframe, text="Login to the Leatherclub", font="Arial 26")
titlelbl.grid(row=0, column=0, columnspan=2, pady=7, ipady=10)

idlbl = Label(mainframe, text="ID")
idlbl.grid(row=1, column=0, sticky=W, padx=5, ipadx=7)
pwlbl = Label(mainframe, text="Password")
pwlbl.grid(row=2, column=0, sticky=W, padx=5, ipadx=7)

identry = Entry(mainframe, width=36)
identry.grid(row=1, column=1)
pwentry = Entry(mainframe, show="*", width=36)
pwentry.grid(row=2, column=1)

loginbutton = Button(mainframe, text="Log in", command=login)
loginbutton.grid(row=3, column=0, columnspan=2, pady=(15, 0))

signupbutton = Button(mainframe, text="Sign Up", command=signup)
signupbutton.grid(row=4, column=0, columnspan=2)

adminbutton = Button(mainframe, text="Admin", font="Arial 8", fg="red", command=deleteacc)
adminbutton.grid(row=5, column=0, columnspan=2, sticky=E)

root.mainloop()
