from tkinter import *
import serial as sr
import pygame
from datetime import date
import logging

text = "Press the Button!"
selected_song = ""
today = date.today()
d1 = today.strftime("%d-%m-%Y")

root = Tk()
root.geometry('800x800')
root.title('Rhythmic Auditory Device')
root['bg'] = '#5d8a82'

f = ("Times bold", 54)
pygame.mixer.init()


def log(d1):
    """Create saved logging file for calibration data

    Function creates a logging file of specified name to log info,
    warning, and errors for calibration data. Also logs an info statement that
    a new calibration analysis has begun.

    :param d1: date of current calibration, used to calculate name of
    logging output file
    """
    filename = "calibration_" + d1 + ".log"
    logging.basicConfig(filename=filename, filemode='w', level=logging.INFO)
    message = "Starting calibration for " + d1
    logging.info(message)


def next_page():
    """Go to next page of GUI

    Function destroys current calibration page and moves on to next main page.
    """
    root.destroy()
    import mainprogram


def play():
    """Plays audio file

    Function plays selected audio file using the pygame mixer plugin. Audio
    file must be in mp3 format and located in specified folder on users
    computer, in this case a test folder on the users Desktop.
    """
    global selected_song
    song = f"/Users/haley/Desktop/test/{selected_song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)


def listen():
    """Listens to serial monitor for serial data instructions

    Function listens to the serial monitor in order to receive instructions
    being sent from the arduino to the serial port in order to perform a
    successful calibration. The output codes of the serial port are decoded and
    matched to specified calibration instructions in both visual and auditory
    format.
    """
    global text, selected_song

    a = s.readline()
    output = a.decode()
    if output == "400\r\n":
        text = "WAIT"
        log(d1)
    elif output == "500\r\n":
        text = "Breathe Out As Hard As You Can!"
        selected_song = "exhale"
        play()
        logging.info("User was instructed to Breath Out as hard as they can")
    elif output == "600\r\n":
        text = "Breathe In As Hard As You Can!"
        selected_song = "inhale"
        play()
        logging.info("User was instructed to Breath In as hard as they can")
    elif output == "700\r\n":
        text = "Calibration is complete. Press Next."
        logging.info("Calibration is complete. User was instructed to continue "
                     "to the next page of the program")
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
s = sr.Serial('/dev/cu.usbmodem146101', 9600)  # CHANGE BASED ON CURRENT PORT
s.reset_input_buffer()


root.after(1, listen)
root.mainloop()
