import tkinter as tk
from tkinter import ttk, messagebox

from matplotlib import patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import serial as sr
import pygame
import time
from tkinter import filedialog
import pickle
import logging

#logging.basicConfig(filename="server.log", filemode="w", level=logging.INFO)


# global variables
data = np.array([])
cond = False
cond2 = False
selected_song = ""
f = ("Times bold", 24)
xmin = 0
xmax = 10
x2max = 50
x = 0
x2 = 0
threshold_hi = 0
threshold_low = 0
hi_thresh = np.empty(300)
low_thresh = np.empty(300)
good_in = 0
above = False
good_out = 0
below = False
good_in_message = ""
good_out_message = ""
r_level = 1


def add_song():
    global selected_song
    song = tk.filedialog.askopenfilename(
        initialdir='/Users/haley/Desktop/test/', title='Choose a Song',
        filetypes=(('mp3 Files', "*.mp3"),))
    song = song.replace('/Users/haley/Desktop/test/', '')
    song = song.replace('.mp3', '')
    print(song)
    selected_song = song
    c_song.config(text=selected_song)
    root.update()


def program_screen():
    global data, cond, cond2, selected_song, f, xmin, xmax, x, threshold_hi, \
        threshold_low, low_thresh, hi_thresh, good_in, good_out, above, below, \
        good_in_message, good_out_message, interval

    def cancel_command():
        """H Function to control cancel button

        This function destroys the gui, to be called when the cancel button is
        pressed. It also prints cancel to the consul when this occurs.
        """
        print("Cancel")
        top.destroy()
        return

    def open_save():
        file = tk.filedialog.asksaveasfilename(filetypes=(('Text Document',
                                                           "*.txt"),))
        p = "Patient Name: "
        p2 = p + str(p_name.get()) + "\n"
        r = "Resistance Level: "
        r2 = r + str(r_level) + "\n"
        i = "# Great Inhales: "
        e = "# Great Exhales: "
        i2 = i + str(good_in) + "\n"
        e2 = e + str(good_out) + "\n"
        len = "Desired Length of Breath (sec): "
        len2 = len + str(breath_length.get()) + "\n"
        output_file = open(file, 'w')
        output_file.write(p2)
        output_file.write(r2)
        output_file.write(i2)
        output_file.write(e2)
        output_file.write(len2)
        output_file.close()

    def open_popup2():
        # this is end session popup
        p2 = tk.Toplevel(top)
        p2.geometry("1000x250")
        p2.title("Session Ended")
        title1 = ttk.Label(p2, text="Summary", font='Mistral 28 bold')
        title1.grid(column=0, row=0, columnspan=2, sticky='w')
        title3 = ttk.Label(p2, text="Inhalation", font='Mistral 25 bold')
        title3.grid(column=0, row=30, columnspan=2, sticky='w')
        title4 = ttk.Label(p2, text="Exhalation", font='Mistral 25 bold')
        title4.grid(column=30, row=30, columnspan=2, sticky='w')
        title5 = ttk.Label(p2, text="# Great Inhales:", font=f)
        title5.grid(column=0, row=31, columnspan=2, sticky='w')
        title5a = ttk.Label(p2, text=good_in)
        title5a.grid(column=3, row=31, columnspan=2, sticky='w')
        title8 = ttk.Label(p2, text="# Great Exhales:", font=f)
        title8.grid(column=30, row=31, columnspan=2, sticky='w')
        title8a = ttk.Label(p2, text=good_out)
        title8a.grid(column=33, row=31, columnspan=2, sticky='w')
        title6 = ttk.Label(p2, text="Resistance Level:", font=f)
        title6.grid(column=0, row=35, columnspan=2, sticky='w')
        title6a = ttk.Label(p2, text=r_level)
        title6a.grid(column=3, row=35, columnspan=2, sticky='w')
        title6c = ttk.Label(p2, text="Desired Length of Breath (sec) :", font=f)
        title6c.grid(column=0, row=35, columnspan=2, sticky='w')
        title6b = ttk.Label(p2, text=breath_length.get())
        title6b.grid(column=3, row=35, columnspan=2, sticky='w')
        # title11 = ttk.Label(p2, text="Share results with:", font='Mistral 25 bold')
        # title11.grid(column=0, row=40, columnspan=2, sticky='w')
        # email = ttk.Entry(p2)
        # email.grid(column=10, row=40, columnspan=2)
        # send_button = ttk.Button(p2, text="Send", style='my.TButton')  # change command
        # send_button.grid(column=20, row=40)
        save_button = ttk.Button(p2, text="Save results as...",
                                 style='my.TButton', command=open_save)
        save_button.grid(column=0, row=50)
        cancel_button = ttk.Button(p2, text="CANCEL", style='my.TButton',
                                 command=p2.destroy)  # change command
        cancel_button.grid(column=50, row=60)
        restart_button = ttk.Button(p2, text="RESTART", style='my.TButton',
                                 command=top.destroy)
        restart_button.grid(column=51, row=60)

    def read_serial():
        global data
        a = s.readline()
        a.decode()
        if len(data) < 300:
            data = np.append(data, float(a[0:4]))
        else:
            data[0:299] = data[1:300]
            data[299] = float(a[0:4])

    def plot_data():
        global cond, data, good_in_message, good_in, threshold_low, \
            threshold_hi, above, below, good_out, good_out_message, x2, \
            r_level, f

        if cond:
            x2 += 1
            read_serial()
            if len(data) > 2:
                if float(data[-1]) > float(threshold_hi):
                    above = True
                    below = False
                    if float(data[-2]) < float(threshold_hi):
                        good_in += 1
                elif float(data[-1]) < float(threshold_low):
                    below = True
                    above = False
                    if float(data[-2]) > float(threshold_low):
                        good_out += 1
                else:
                    above = False
                    below = False
            lines.set_xdata(np.arange(0, len(data)))
            lines.set_ydata(data)
            if x2 >= x2max - 1.00:
                lines.axes.set_xlim(x2 - x2max + 1.0, x2 + 1.0)
            canvas.draw()
            if above is True:
                good_in_message = "GREAT INHALE!"
                good_job.config(text=good_in_message)
                root.update()
            elif below is True:
                good_out_message = "GREAT EXHALE!"
                good_job.config(text=good_out_message)
                root.update()  # or just root update
            else:
                good_job.config(text="")
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

    def plot_stop2():
        global cond2
        cond2 = False

    def play():
        song = f"/Users/haley/Desktop/test/{selected_song}.mp3"
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)

    def stop():
        pygame.mixer.music.stop()

    def pause():
        pygame.mixer.music.pause()

    top = tk.Toplevel(root)
    top.title("Patient Interface")
    top['bg'] = '#5d8a82'
    top.geometry("1600x800")

    # initiate media player
    pygame.mixer.init()

    top_label = ttk.Label(top, text="Welcome!", font=f)
    top_label.grid(column=0, row=0, columnspan=2, sticky='w')
    ttk.Label(top, text="Click Menu to return to entering preferences, or "
                        "Start to begin session!",
              font=f).grid(column=0, row=20)
    top.update()
    end_button = ttk.Button(top, text="End Session", style='my.TButton',
                            command=lambda: [open_popup2(), stop(),
                                             plot_stop(), plot_stop2()])
    end_button.grid(column=5, row=20)
    cancel_button = ttk.Button(top, text="Cancel", style='my.TButton', command=cancel_command)
    cancel_button.grid(column=6, row=20)
    menu_button = ttk.Button(top, text="Menu", style='my.TButton', command=top.destroy)
    menu_button.grid(column=2, row=20)
    ttk.Label(top, text="Current Song:", font=f).grid(column=0, row=25)
    # selected_song = tk.StringVar()
    root.update()
    current_song = ttk.Label(top, text=selected_song, font="Times 15")
    current_song.grid(column=1, row=25)
    good_job = ttk.Label(top, text="", font=f)
    good_job.grid(column=5, row=25)

    # initial plot figure created
    fig = Figure()
    ax = fig.add_subplot(111)

    ax.set_title('Breath Visualization')
    ax.set_xlabel('Time')
    ax.set_ylabel('Volume in Lungs (mL/kg)')
    ax.set_xlim(0, 50)
    ax.set_ylim(-5, 5)
    lines = ax.plot([], [])[0]
    xs = range(300)
    threshold_hi = inhale.get()
    threshold_low = exhale.get()
    r_level = level.get()
    hi_thresh.fill(threshold_hi)
    low_thresh.fill(threshold_low)
    upper_line = ax.plot(xs, hi_thresh, color="b")
    lower_line = ax.plot(xs, low_thresh, color="g")

    canvas = FigureCanvasTkAgg(fig, master=top)
    canvas.get_tk_widget().place(x=10, y=95, width=1000, height=500)
    canvas.draw()

    # second plot for breathing instructions created
    fig2 = Figure()
    ax2 = fig2.add_subplot(111)
    ax2.set_title('Breathing Instructions')
    ax2.set_xlabel('Time')
    ax2.set_xlim(0, 10)
    ax2.get_yaxis().set_visible(False)

    canvas2 = FigureCanvasTkAgg(fig2, master=top)
    canvas2.get_tk_widget().place(x=10, y=600, width=1000, height=200)
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
    scat = ax2.scatter(t, b, c=c, s=200)
    interval = 100
    if selected_song == "icanfly":
        interval = 1000
    elif selected_song == "billiejean":
        interval = 500

    def animate(i):
        global cond2, x

        if cond2:
            # for i in range(len(times)):
            x += 1
            if len(t) < 10:
                t.append(times[i])
                b.append(beat[i])
                c.append(color[i])
            else:
                t[0:9] = t[1:10]
                t[9] = times[i]
                b[0:9] = b[1:10]
                b[9] = beat[i]
                c[0:9] = c[1:10]
                c[9] = color[i]
            # scat.set_xdata(np.arange(0, len(t)))
            # scat.set_ydata(b)
            # canvas2.draw()
            # top.after(1, animate)
            # ax2.scatter(t, b, c=c, s=200)
            # need to have shifting x axis
            # scat.set_data(t, b)
            # x2 = np.meshgrid(t, b)
            # scat.set_offsets(x2)
            # scat.set_array(c)

            if x >= xmax - 1.00:
                scat.axes.set_xlim(x - xmax + 1.0, x + 1.0)

            ax2.scatter(t, b, c=c, s=200)
            ax2.add_patch(patches.Rectangle(
                    xy=(x-0.5, 2),  # point of origin.
                    width=1, height=2, linewidth=1,
                    color='red', fill=False))
            ax2.add_patch(patches.Rectangle(
                xy=(x - 1.5, 2),  # point of origin.
                width=1, height=2, linewidth=1,
                color='white', fill=False))
            # return scat
            # canvas2.draw()
    # top.update()
    ani = FuncAnimation(fig2, animate, frames=255, interval=interval, blit=False)
    canvas2.draw()

    top.update()
    start_button = ttk.Button(top, text="Start", style='my.TButton', command=lambda: [
        plot_start2(), play(), plot_start()])
    start_button.grid(column=3, row=20)

    top.update()
    pause_button = ttk.Button(top, text="Pause", style='my.TButton', command=lambda: [
        plot_stop(), plot_stop2(), pause()])
    pause_button.grid(column=4, row=20)

    # initialize serial port
    # CHANGE S BASED ON CURRENT PORT
    s = sr.Serial('/dev/cu.usbmodem146101', 9600)
    s.reset_input_buffer()

    # top.after(1, animate)
    top.after(1, plot_data)
    top.mainloop()


def warning():
    warning = tk.Toplevel(root)
    warning.geometry("1000x100")
    warning.title("WAIT")
    title1 = ttk.Label(warning, text="DID YOU CHOOSE A RESITANCE LEVEL FOR "
                                     "THIS SESSION?", font='Mistral 28 bold')
    title1.grid(column=0, row=0, columnspan=2, sticky='w')
    no_button = ttk.Button(warning, text="NO", style='my.TButton',
                             command=warning.destroy)
    no_button.grid(column=0, row=50)
    yes_button = ttk.Button(warning, text="YES", style='my.TButton',
                            command=program_screen)
    yes_button.grid(column=50, row=50)


# initialize gui main window --MENU
root = tk.Tk()
root.title("Rythmic Auditory Device")
root['bg'] = '#5d8a82'
root.geometry("1500x500")

s = ttk.Style()
s.configure('my.TButton', font=f)

title1 = ttk.Label(root, text="Instructions", font='Mistral 28 bold')
title1.grid(column=0, row=0, columnspan=2, sticky='w')
blue = ttk.Label(root, text="Blue = inhale", font=f)
blue.grid(column=0, row=20, columnspan=2, sticky='w')
green = ttk.Label(root, text="Green = exhale", font=f)
green.grid(column=1, row=20, columnspan=2, sticky='w')
brown = ttk.Label(root, text="Black = rest", font=f)
brown.grid(column=2, row=20, columnspan=2, sticky='w')
line1 = ttk.Label(root, text="Go above the blue threshold to earn a "
                             "'GREAT INHALE!'", font=f)
line1.grid(column=0, row=40, columnspan=2, sticky='w')
line2 = ttk.Label(root, text="Go below the green threshold to earn a "
                             "'GREAT EXHALE!'", font=f)
line2.grid(column=0, row=60, columnspan=2, sticky='w')
title2 = ttk.Label(root, text="Music", font='Mistral 28 bold')
title2.grid(column=0, row=90, columnspan=2, sticky='w')
title3 = ttk.Label(root, text="User Specs", font='Mistral 28 bold')
title3.grid(column=0, row=200, columnspan=2, sticky='w')
title4 = ttk.Label(root, text="Song:", font=f)
title4.grid(column=0, row=100, columnspan=2, sticky='w')
title5 = ttk.Label(root, text="Desired Length of Breath (sec) :", font=f)
title5.grid(column=23, row=100, columnspan=2, sticky='w')
breath_length = ttk.Entry(root)
breath_length.grid(column=25, row=100)
title50 = ttk.Label(root, text="Patient Name:", font=f)
title50.grid(column=0, row=210, columnspan=2, sticky='w')
p_name = ttk.Entry(root)
p_name.grid(column=1, row=210)
song = ttk.Button(root, text="Choose Song", style='my.TButton',
                  command=add_song)
song.grid(column=1, row=100)
c_song = ttk.Label(root, text=selected_song)
c_song.grid(column=2, row=100, columnspan=2, sticky='w')
title9 = ttk.Label(root, text="Resistance Level:", font=f)
title9.grid(column=23, row=300, columnspan=2, sticky='w')
levels = tk.StringVar()
level = ttk.Combobox(root, textvariable=levels)
level["values"] = [0, 1, 2, 3, 4, 5]
level.grid(column=25, row=300)
title10 = ttk.Label(root, text="Great Inhale Threshold:", font=f)
title10.grid(column=0, row=300, columnspan=2, sticky='w')
title11 = ttk.Label(root, text="Great Exhale Threshold:", font=f)
title11.grid(column=0, row=310, columnspan=2, sticky='w')
inhale = ttk.Combobox(root)
inhale["values"] = [1, 2, 3]
inhale.grid(column=1, row=300)
exhale = ttk.Combobox(root)
exhale["values"] = [-1, -2, -3]
exhale.grid(column=1, row=310)
update_button = ttk.Button(root, text="Next", style='my.TButton',
                           command=warning)
update_button.grid(column=25, row=350)
cancel = ttk.Button(root, text="END PROGRAM", style='my.TButton',
                    command=root.destroy)
cancel.grid(column=25, row=450)

root.mainloop()
