from tkinter import *
import serial as sr
import pygame

text = "Press the Button!"
selected_song = ""

root = Tk()
root.geometry('800x800')
root.title('Rhythmic Auditory Device')
root['bg'] = '#5d8a82'

f = ("Times bold", 54)
pygame.mixer.init()


def next_page():
    root.destroy()
    import mainprogram


def play():
    global selected_song
    song = f"/Users/haley/Desktop/test/{selected_song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)


def listen():
    global text, selected_song

    a = s.readline()
    output = a.decode()
    if output == "400\r\n":
        text = "WAIT"
    elif output == "500\r\n":
        text = "Breathe Out As Hard As You Can!"
        selected_song = "exhale"
        play()
    elif output == "600\r\n":
        text = "Breathe In As Hard As You Can!"
        selected_song = "inhale"
        play()
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
s = sr.Serial('/dev/cu.usbmodem146101', 9600)
s.reset_input_buffer()


root.after(1, listen)
root.mainloop()
