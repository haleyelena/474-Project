from tkinter import *
import serial as sr

text = "Press the Button!"

root = Tk()
root.geometry('400x300')
root.title('Rythmic Auditory Device')
root['bg'] = '#5d8a82'

f = ("Times bold", 14)


def next_page():
    root.destroy()
    import mainprogram


def listen():
    global text

    a = s.readline()
    output = a.decode()
    if output == "400\r\n":
        text = "WAIT"
    elif output == "500\r\n":
        text = "Breathe Out As Hard As You Can!"
    elif output == "600\r\n":
        text = "Breathe In As Hard As You Can!"
    elif output == "700\r\n":
        text = "Calibration is complete. Press Next."
    testing.config(text=text)
    root.update()
    root.after(1, listen)



Label(
    root,
    text="CALIBRATION",
    padx=20,
    pady=20,
    bg='#5d8a82',
    font=f).pack(expand=True, fill=BOTH)


testing = Label(root, text="Press the Button", padx=20, pady=20, bg='#5d8a82',
                font=f)
testing.pack(expand=True, fill=BOTH)

Button(
    root,
    text="Next",
    font=f,
    command=next_page
).pack(fill=X, expand=TRUE, side=LEFT)


# initialize serial port
s = sr.Serial('/dev/cu.usbmodem144101', 9600)
s.reset_input_buffer()


root.after(1, listen)
root.mainloop()
