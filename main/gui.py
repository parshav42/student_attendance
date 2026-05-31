
from tkinter import *

from PIL import ImageTk

# ── Import all back-end functions from main.py ──────────────
from main import insert_user, train_image, track_user, del_user


window = Tk()
window.geometry('600x600')
window.resizable(width=False, height=False)
window.title("My Attendance Portal")
window.configure(background='#D0D3D4')

# ── Status message variable (shared with main.py) ───────────
v = StringVar()

try:

    images = Image.open("images/attendance.png")

    images = images.resize((200, 200))

    photo = ImageTk.PhotoImage(images)

    lab = Label(window, image=photo, bg="white")

    lab.pack(pady=10)

except:
    pass
fn = StringVar()
ln = StringVar()
dn = StringVar()

Label(window, text="Note : To exit the frame window press 'q'",
      fg='red',     bg='#D0D3D4', font=("roboto", 15)             ).place(x=20,  y=100)

Label(window, textvariable=v,
      fg='red',     bg='#D0D3D4', font=("roboto", 15, "italic")   ).place(x=20,  y=150)

Label(window, text="New User",
      fg='#717D7E', bg='#D0D3D4', font=("roboto", 20, "bold")     ).place(x=20,  y=200)

Label(window, text="Enter Name :",
      fg='black',   bg='#D0D3D4', font=("roboto", 15)             ).place(x=20,  y=250)

Label(window, text="Enter Roll Number :",
      fg='black',   bg='#D0D3D4', font=("roboto", 15)             ).place(x=275, y=252)

Label(window, text="Already a User ?",
      fg='#717D7E', bg='#D0D3D4', font=("roboto", 20, "bold")     ).place(x=20,  y=350)

Label(window, text="Delete a users information",
      fg='#717D7E', bg='#D0D3D4', font=("roboto", 20, "bold")     ).place(x=20,  y=450)

Label(window, text="Enter Id :",
      fg='black',   bg='#D0D3D4', font=("roboto", 15)             ).place(x=20,  y=500)


entry_name     = Entry(window, textvar=fn)
entry_name.place(x=150, y=257)

entry_id       = Entry(window, textvar=ln)
entry_id.place(x=455,  y=257)

entry_name_del = Entry(window, textvar=dn)
entry_name_del.place(x=150, y=507)


Button(window, text="Submit",
       width=5, fg='#fff', bg='#27AE60', relief=RAISED,
       font=("roboto", 15, "bold"),
       command=lambda: insert_user(fn, ln, v)          ).place(x=20,  y=300)

Button(window, text="Train Images",
       fg='#fff', bg='#5DADE2', relief=RAISED,
       font=("roboto", 15, "bold"),
       command=lambda: train_image(v)                   ).place(x=100, y=300)

Button(window, text="Track User",
       fg='#fff', bg='#E67E22', relief=RAISED,
       font=("roboto", 15, "bold"),
       command=lambda: track_user(v)                    ).place(x=20,  y=400)

Button(window, text="Delete User",
       fg='#fff', bg='#8E44AD', relief=RAISED,
       font=("roboto", 15, "bold"),
       command=lambda: del_user(dn, v)                  ).place(x=20,  y=550)

Button(window, text="Exit",
       width=5, fg='#fff', bg='red', relief=RAISED,
       font=("roboto", 15, "bold"),
       command=window.destroy                           ).place(x=500, y=550)

window.mainloop()