from tkinter import *

root = Tk()
root.geometry('800x800')
root.title('Rythmic Auditory Device')
root.configure(background="#ececec")

f = ("Times bold", 54)


def next_page():
    """Go to next page of GUI

    Function destroys current calibration page and moves on to next main page.
    """
    root.destroy()
    import calibration


Label(
    root,
    text="WELCOME",
    padx=20,
    pady=20,
    bg='#ffc0cb',
    font=f
).pack(expand=True, fill=BOTH)


Button(
    root,
    text="Next",
    font=f,
    command=next_page
).pack(fill=X, expand=TRUE, side=LEFT)

root.mainloop()
