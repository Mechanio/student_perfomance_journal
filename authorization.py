from tkinter import *
import tkinter.messagebox
import sqlite3
import windows_for_users


def button_func():
    conn = sqlite3.connect('data.sqlite') # connect to database
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM Students WHERE login = ? ', (entry_login.get(),))
        data = cur.fetchone() # check if student's login is exist
        if data == None:      # else check if teacher login is exist
            cur.execute('SELECT * FROM Teachers WHERE login = ? ', (entry_login.get(),))
            data = cur.fetchone()
            if data[3] == entry_password.get():
                tkinter.messagebox.showinfo("Log in", "You have successfully logged in as a teacher")
                root.destroy()
                windows_for_users.Teacher_window(data)
                return
            else:
                tkinter.messagebox.showerror("Warning", "Password is incorrect")
                return
        if data[4] == entry_password.get():
            tkinter.messagebox.showinfo("Log in", "You have successfully logged in as a student")
            root.destroy()
            windows_for_users.Student_window(data)
            return
        else:
            tkinter.messagebox.showerror("Warning", "Password is incorrect")
            return
    except TypeError:
        tkinter.messagebox.showerror("Warning", "Login is incorrect")
        return


root = Tk()  # create a window (frame)
root.title("Authorization")
root.geometry("250x180+600+300")
root.resizable(width=False, height=False)

frame1 = Frame(root)
frame1.pack()

label_login = Label(frame1, text="Login:")
label_login.pack()

entry_login = Entry(frame1)
entry_login.pack(padx=10, pady=10)

label_password = Label(frame1, text="Password:")
label_password.pack(padx=5, pady=5)

entry_password = Entry(frame1)
entry_password.pack(padx=5, pady=5)
# button of authorization
button_submit = Button(frame1, text="Log in", command=button_func)
button_submit.pack(padx=5, pady=5)

root.mainloop()
