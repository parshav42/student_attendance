# gui.py

from tkinter import *
from PIL import Image, ImageTk


windows = Tk()

windows.geometry("750x650")

windows.resizable(False, False)

windows.title("Face Attendance System")

windows.configure(background="white")


# =========================
# IMAGE
# =========================

try:

    images = Image.open("images/attendance.png")

    images = images.resize((200, 200))

    photo = ImageTk.PhotoImage(images)

    lab = Label(windows, image=photo, bg="white")

    lab.pack(pady=10)

except:
    pass


# =========================
# VARIABLES
# =========================

fn = StringVar()

ln = StringVar()

dn = StringVar()

v = StringVar()


# =========================
# TITLE
# =========================

title = Label(
    windows,
    text="Face Attendance System",
    font=("Arial", 24, "bold"),
    bg="white",
    fg="blue"
)

title.pack(pady=10)


# =========================
# NEW USER SECTION
# =========================

Label(
    windows,
    text="Enter Name",
    font=("Arial", 14),
    bg="white"
).place(x=50, y=260)

entry_name = Entry(
    windows,
    textvariable=fn,
    font=("Arial", 14),
    width=25
)

entry_name.place(x=220, y=260)


Label(
    windows,
    text="Enter ID",
    font=("Arial", 14),
    bg="white"
).place(x=50, y=320)

entry_id = Entry(
    windows,
    textvariable=ln,
    font=("Arial", 14),
    width=25
)

entry_id.place(x=220, y=320)


# =========================
# DELETE USER
# =========================

Label(
    windows,
    text="Delete User ID",
    font=("Arial", 14),
    bg="white"
).place(x=50, y=380)

entry_delete = Entry(
    windows,
    textvariable=dn,
    font=("Arial", 14),
    width=25
)

entry_delete.place(x=220, y=380)


# =========================
# STATUS LABEL
# =========================

status = Label(
    windows,
    textvariable=v,
    font=("Arial", 14, "bold"),
    fg="green",
    bg="white"
)

status.place(x=50, y=430)


# =========================
# BUTTONS
# =========================

button_submit = Button(
    windows,
    text="Capture Images",
    font=("Arial", 14, "bold"),
    bg="green",
    fg="white",
    width=18
)

button_submit.place(x=50, y=500)


button_train = Button(
    windows,
    text="Train Images",
    font=("Arial", 14, "bold"),
    bg="blue",
    fg="white",
    width=18
)

button_train.place(x=300, y=500)


button_track = Button(
    windows,
    text="Track User",
    font=("Arial", 14, "bold"),
    bg="orange",
    fg="white",
    width=18
)

button_track.place(x=550, y=500)


button_delete = Button(
    windows,
    text="Delete User",
    font=("Arial", 14, "bold"),
    bg="purple",
    fg="white",
    width=18
)

button_delete.place(x=180, y=570)


button_exit = Button(
    windows,
    text="Exit",
    font=("Arial", 14, "bold"),
    bg="red",
    fg="white",
    width=18
)

button_exit.place(x=430, y=570)
