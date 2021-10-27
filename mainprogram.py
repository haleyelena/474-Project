import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import serial as sr
import pygame
import time

# global variables
data = np.array([])
cond = False
cond2 = False
selected_song = ""
f = ("Times bold", 14)


def add_song():
    global selected_song
    song = tk.filedialog.askopenfilename(
        initialdir='/Users/haley/Desktop/test/', title='Choose a Song',
        filetypes=(('mp3 Files', "*.mp3"),))

    song = song.replace('/Users/haley/Desktop/test/', '')
    song = song.replace('.mp3', '')
    print(song)
    selected_song = song


def program_screen():
    global data, cond, cond2, selected_song, f

    def cancel_command():
        """H Function to control cancel button

        This function destroys the gui, to be called when the cancel button is
        pressed. It also prints cancel to the consul when this occurs.
        """
        print("Cancel")
        top.destroy()
        return

    def open_popup2():
        # this is end session popup
        p2 = tk.Toplevel(top)
        p2.geometry("750x250")
        p2.title("Session Ended")
        title1 = ttk.Label(p2, text="Summary", font='Mistral 18 bold')
        title1.grid(column=0, row=0, columnspan=2, sticky='w')
        title2 = ttk.Label(p2, text="Session Duration: X Minutes")
        title2.grid(column=0, row=20, columnspan=2, sticky='w')
        title3 = ttk.Label(p2, text="Inhalation", font='Mistral 12 bold')
        title3.grid(column=0, row=30, columnspan=2, sticky='w')
        title4 = ttk.Label(p2, text="Exhalation", font='Mistral 12 bold')
        title4.grid(column=30, row=30, columnspan=2, sticky='w')
        title5 = ttk.Label(p2, text="# Great Inhales: X")
        title5.grid(column=0, row=31, columnspan=2, sticky='w')
        title6 = ttk.Label(p2, text="Avg Max: X mL/kg")
        title6.grid(column=0, row=32, columnspan=2, sticky='w')
        title7 = ttk.Label(p2, text="Avg Duration: X sec")
        title7.grid(column=0, row=33, columnspan=2, sticky='w')
        title8 = ttk.Label(p2, text="# Great Exhales: X")
        title8.grid(column=30, row=31, columnspan=2, sticky='w')
        title9 = ttk.Label(p2, text="Avg min: X mL/kg")
        title9.grid(column=30, row=32, columnspan=2, sticky='w')
        title10 = ttk.Label(p2, text="Avg Duration: X Sec")
        title10.grid(column=30, row=33, columnspan=2, sticky='w')
        title11 = ttk.Label(p2, text="Share results with:",
                            font='Mistral 12 bold')
        title11.grid(column=0, row=40, columnspan=2, sticky='w')
        email = ttk.Entry(p2)
        email.grid(column=10, row=40, columnspan=2)
        send_button = ttk.Button(p2, text="Send")  # change command
        send_button.grid(column=20, row=40)
        save_button = ttk.Button(p2,
                                 text="Save results as...")  # change command
        save_button.grid(column=0, row=50)
        send_button = ttk.Button(p2, text="RETRY",
                                 command=p2.destroy)  # change command
        send_button.grid(column=50, row=60)
        send_button = ttk.Button(p2, text="RESTART",
                                 command=p2.destroy)  # change command
        send_button.grid(column=51, row=60)

    def plot_data():
        global cond, data

        if cond:
            a = s.readline()
            a.decode()
            if len(data) < 100:
                data = np.append(data, float(a[0:4]))
            else:
                data[0:99] = data[1:100]
                data[99] = float(a[0:4])
            lines.set_xdata(np.arange(0, len(data)))
            lines.set_ydata(data)
            canvas.draw()
        root.after(1, plot_data)

    def plot_start():
        global cond
        cond = True
        s.reset_input_buffer()

    def plot_start2():
        global cond2
        cond2 = True

    def plot_stop():
        global cond
        cond = False

    def play():
        song = f"/Users/haley/Desktop/test/{selected_song}.mp3"
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)

    def stop():
        pygame.mixer.music.stop()

    def pause():
        pygame.mixer.music.pause()

    top = tk.Toplevel(root)
    top.title("Mock Patient Interface")
    top['bg'] = '#5d8a82'
    top.geometry("1200x800")

    # initiate media player
    pygame.mixer.init()

    top_label = ttk.Label(top, text="Welcome!")
    top_label.grid(column=0, row=0, columnspan=2, sticky='w')

    ttk.Label(top, text="Pick Patient Name:").grid(column=0, row=1)
    patient_ids = tk.StringVar()
    patient = ttk.Combobox(top, textvariable=patient_ids)
    patient.grid(column=1, row=1)
    test = ["haley", "rachel", "phoebe", "claire"]
    patient["values"] = test
    ttk.Label(top, text="Click Menu to enter preferences, "
                     "then Start to begin session!").grid(column=0, row=20)

    end_button = ttk.Button(top, text="End Session", command=lambda: [
        open_popup2(), stop()])
    end_button.grid(column=5, row=20)
    cancel_button = ttk.Button(top, text="Cancel",
                           command=cancel_command)
    cancel_button.grid(column=6, row=20)
    menu_button = ttk.Button(top, text="Menu", command=top.destroy)
    menu_button.grid(column=2, row=20)
    ttk.Label(top, text="Current Song:").grid(column=0, row=25)
    # selected_song = tk.StringVar()
    current_song = ttk.Label(top, text=selected_song)
    current_song.grid(column=1, row=25)

    # initial plot figure created
    fig = Figure()
    ax = fig.add_subplot(111)

    ax.set_title('Fake Plot')
    ax.set_xlabel('Time')
    ax.set_ylabel('Volume in Lungs (mL/kg)')
    ax.set_xlim(0, 50)
    ax.set_ylim(0, 6)
    lines = ax.plot([], [])[0]

    canvas = FigureCanvasTkAgg(fig, master=top)
    canvas.get_tk_widget().place(x=10, y=100, width=600, height=400)
    canvas.draw()

    # second plot for breathing instructions created
    fig2 = Figure()
    ax2 = fig2.add_subplot(111)
    ax2.set_title('Breathing Instructions')
    ax2.set_xlabel('Time')
    ax2.set_xlim(0, 50)
    ax2.get_yaxis().set_visible(False)

    canvas2 = FigureCanvasTkAgg(fig2, master=top)
    canvas2.get_tk_widget().place(x=10, y=550, width=600, height=200)
    canvas2.draw()

    # loading csv data that is synched with when to breath in/out
    df = pd.read_csv('testdata.csv', header=None)
    h = df.to_numpy()
    times = h[:, 0]
    t = []
    beat = h[:, 1]
    b = []
    color = h[:, 2]
    c = []


    def animate(i):
        global cond2

        if cond2:
            # for i in range(len(times)):
            t.append(times[i])
            b.append(beat[i])
            c.append(color[i])
            ax2.scatter(t, b, c=c)

            # canvas2.draw()

    ani = FuncAnimation(fig2, animate, frames=68, interval=1000, blit=False)

    top.update()
    start_button = ttk.Button(top, text="Start", command=lambda: [
        plot_start2(), play()])
    start_button.grid(column=3, row=20)

    top.update()
    pause_button = ttk.Button(top, text="Pause", command=lambda: [
        plot_stop(), pause()])
    pause_button.grid(column=4, row=20)

    # initialize serial port
    s = sr.Serial('/dev/cu.URT2', 9600)
    s.reset_input_buffer()

    top.after(1, plot_data)


# initialize gui main window --MENU
root = tk.Tk()
root.title("Rythmic Auditory Device")
root['bg'] = '#5d8a82'
root.geometry("1000x400")

title1 = ttk.Label(root, text="Instructions", font='Mistral 18 bold')
title1.grid(column=0, row=0, columnspan=2, sticky='w')
blue = ttk.Label(root, text="Blue = inhale")
blue.grid(column=0, row=20, columnspan=2, sticky='w')
green = ttk.Label(root, text="Green = exhale")
green.grid(column=10, row=20, columnspan=2, sticky='w')
brown = ttk.Label(root, text="Brown = rest")
brown.grid(column=20, row=20, columnspan=2, sticky='w')
line1 = ttk.Label(root, text="Go above the blue threshold to earn a "
                            "'GREAT INHALE!'")
line1.grid(column=0, row=40, columnspan=2, sticky='w')
line2 = ttk.Label(root, text="Go below the green threshold to earn a "
                            "'GREAT EXHALE!'")
line2.grid(column=0, row=60, columnspan=2, sticky='w')
title2 = ttk.Label(root, text="Music", font='Mistral 18 bold')
title2.grid(column=0, row=90, columnspan=2, sticky='w')
title3 = ttk.Label(root, text="User", font='Mistral 18 bold')
title3.grid(column=0, row=200, columnspan=2, sticky='w')
title4 = ttk.Label(root, text="Song:")
title4.grid(column=0, row=100, columnspan=2, sticky='w')
title5 = ttk.Label(root, text="BPM:")
title5.grid(column=35, row=100, columnspan=2, sticky='w')
bpm = ttk.Entry(root)
bpm.grid(column=40, row=100)
# songs = tk.StringVar()
# song = ttk.Combobox(top, textvariable=songs)
# song["values"] = ["Happy Birthday", "Don't Stop Believin",
# "Bohemian Rhapsody"]
song = ttk.Button(root, text="Choose Song", command=add_song)
song.grid(column=10, row=100)
c_song = ttk.Label(root, text=selected_song)
c_song.grid(column=20, row=100, columnspan=2, sticky='w')
title7 = ttk.Label(root, text="Weight:")
title7.grid(column=0, row=210, columnspan=2, sticky='w')
weight = ttk.Entry(root)
weight.grid(column=10, row=210, columnspan=2)
title8 = ttk.Label(root, text="kg")
title8.grid(column=15, row=210, columnspan=2, sticky='w')
title9 = ttk.Label(root, text="Resistance Level:")
title9.grid(column=35, row=210, columnspan=2, sticky='w')
levels = tk.StringVar()
level = ttk.Combobox(root, textvariable=levels)
level["values"] = [1, 2, 3]
level.grid(column=40, row=210)
title10 = ttk.Label(root, text="Great Inhale Threshold:")
title10.grid(column=0, row=300, columnspan=2, sticky='w')
title11 = ttk.Label(root, text="Great Exhale Threshold:")
title11.grid(column=0, row=310, columnspan=2, sticky='w')
inhale = ttk.Combobox(root)
inhale["values"] = ["High", "Medium", "Low"]
inhale.grid(column=10, row=300)
exhale = ttk.Combobox(root)
exhale["values"] = ["High", "Medium", "Low"]
exhale.grid(column=10, row=310)
update_button = ttk.Button(root, text="Next", command=program_screen)
update_button.grid(column=40, row=350)
cancel = ttk.Button(root, text="END PROGRAM", command=root.destroy)
cancel.grid(column=40, row=450)


root.mainloop()


