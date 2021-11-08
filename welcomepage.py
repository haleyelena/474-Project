from tkinter import *

root = Tk()
root.geometry('800x800')
root.title('Rythmic Auditory Device')
root['bg'] = '#5d8a82'

f = ("Times bold", 54)


def next_page():
    root.destroy()
    import calibration


Label(
    root,
    text="WELCOME",
    padx=20,
    pady=20,
    bg='#5d8a82',
    font=f
).pack(expand=True, fill=BOTH)


Button(
    root,
    text="Next",
    font=f,
    command=next_page
).pack(fill=X, expand=TRUE, side=LEFT)

root.mainloop()
