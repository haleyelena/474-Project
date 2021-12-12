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
time_list_in = []
time_list_ex = []
start_time = 0
end_time = 0
start_time2 = 0
end_time2 = 0


def add_song():
    """Function to choose song to play in gui

    This function allows the user to pick a song from a specified folder on
    users computer, in this case a test folder on the users Desktop. It then
    sets this song name as the selected song global variable.
    """
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


def average(list):
    """Find the average of a list of floats.

    Function takes the average of a list of floats and returns it with two
    decimal places.

    :param list: list of time durations of inhales or exhales

    :return avg2: string of calculated average number with 2 decimal places
    """
    sum = 0
    for x in list:
        sum += x
    if len(list) > 0:
        avg = sum / len(list)
        avg2 = "{:.2f}".format(avg)
        return avg2


def program_screen():
    """Main session page of GUI

    Function opens main session page of GUI.
    """
    global data, cond, cond2, selected_song, f, xmin, xmax, x, threshold_hi, \
        threshold_low, low_thresh, hi_thresh, good_in, good_out, above, below,\
        good_in_message, good_out_message, interval, time_list_in, start_time,\
        end_time, time_list_ex, start_time2, end_time2

    def cancel_command():
        """Function to control cancel button

        This function destroys the gui, to be called when the cancel button is
        pressed. It also prints cancel to the consul when this occurs.
        """
        print("Cancel")
        top.destroy()
        return

    def open_save():
        """Save function

        Function writes a text file containing all of the summary metrics
        displayed in the end session popup. The file is saved in the location
        and to the name of the users choice.
        """
        file = tk.filedialog.asksaveasfilename(filetypes=(('Text Document',
                                                           "*.txt"),))
        p = "Patient Name: "
        p2 = p + str(p_name.get()) + "\n"
        r = "Resistance Level: "
        r2 = r + str(r_level) + "\n"
        ithresh = "Inhale Threshold: "
        ithresh2 = ithresh + str(inhale.get()) + "\n"
        ethresh = "Exhale Threshold: "
        ethresh2 = ethresh + str(exhale.get()) + "\n"
        i = "# Great Inhales: "
        e = "# Great Exhales: "
        i2 = i + str(good_in) + "\n"
        e2 = e + str(good_out) + "\n"
        len = "Desired Length of Breath (sec): "
        len2 = len + str(breath_length.get()) + "\n"
        alen = "Average Length of Actual Inhale (sec): "
        alen2 = alen + str(average(time_list_in)) + "\n"
        alen3 = "Average Length of Actual Exhale (sec): "
        alen4 = alen3 + str(average(time_list_ex)) + "\n"
        output_file = open(file, 'w')
        output_file.write(p2)
        output_file.write(r2)
        output_file.write(ithresh2)
        output_file.write(ethresh2)
        output_file.write(i2)
        output_file.write(e2)
        output_file.write(len2)
        output_file.write(alen2)
        output_file.write(alen4)
        output_file.close()

    def open_popup2():
        """End Session popup page of GUI

        Function opens end session popup page of GUI.
        """
        p2 = tk.Toplevel(top)
        p2.geometry("1200x500")
        p2.configure(background="#ececec")
        p2.title("Session Ended")
        title1 = ttk.Label(p2, text="Summary", font='Mistral 28 bold')
        title1.grid(column=0, row=0, columnspan=1, sticky='w', pady=[10])
        title3 = ttk.Label(p2, text="Inhalation", font='Mistral 25 bold')
        title3.grid(column=0, row=30, columnspan=1, sticky='w')
        title4 = ttk.Label(p2, text="Exhalation", font='Mistral 25 bold')
        title4.grid(column=30, row=30, columnspan=1, sticky='w')
        title5 = ttk.Label(p2, text="# Great Inhales:", font=f)
        title5.grid(column=0, row=31, columnspan=1, sticky='w')
        title5a = ttk.Label(p2, text=good_in)
        title5a.grid(column=1, row=31, columnspan=1, sticky='w')
        title8 = ttk.Label(p2, text="# Great Exhales:", font=f)
        title8.grid(column=30, row=31, columnspan=1, sticky='w')
        title8a = ttk.Label(p2, text=good_out)
        title8a.grid(column=33, row=31, columnspan=1, sticky='w')
        title6 = ttk.Label(p2, text="Inhale Threshold:", font=f)
        title6.grid(column=0, row=35, columnspan=1, sticky='w')
        in_hale = inhale.get()
        title6a = ttk.Label(p2, text=in_hale)
        title6a.grid(column=3, row=35, columnspan=1, sticky='w')
        ex_hale = exhale.get()
        title6 = ttk.Label(p2, text="Exhale Threshold:", font=f)
        title6.grid(column=30, row=35, columnspan=1, sticky='w')
        title6a = ttk.Label(p2, text=ex_hale)
        title6a.grid(column=33, row=35, columnspan=1, sticky='w')
        title3 = ttk.Label(p2, text="General Parameters",
                           font='Mistral 25 bold')
        title3.grid(column=0, row=40, columnspan=1, sticky='w', pady=[10, 0])
        title6 = ttk.Label(p2, text="Resistance Level:", font=f)
        title6.grid(column=0, row=44, columnspan=1, sticky='w')
        title6a = ttk.Label(p2, text=r_level)
        title6a.grid(column=3, row=44, columnspan=1, sticky='w')
        title6c = ttk.Label(p2, text="Desired Length of Breath (sec) :", font=f)
        title6c.grid(column=0, row=42, columnspan=2, sticky='w')
        blength = breath_length.get()
        title6b = ttk.Label(p2, text=blength)
        title6b.grid(column=3, row=42, columnspan=1, sticky='w')
        title6d = ttk.Label(p2, text="Average Length of Actual Inhale (sec) :",
                            font=f)
        title6d.grid(column=0, row=37, columnspan=1, sticky='w')
        title6e = ttk.Label(p2, text=average(time_list_in))
        title6e.grid(column=3, row=37, columnspan=1, sticky='w')
        title6d = ttk.Label(p2, text="Average Length of Actual Exhale (sec) :",
                            font=f)
        title6d.grid(column=30, row=37, columnspan=1, sticky='w')
        title6e = ttk.Label(p2, text=average(time_list_ex))
        title6e.grid(column=33, row=37, columnspan=1, sticky='w')
        save_button = ttk.Button(p2, text="Save results as...",
                                 style='my.TButton', command=open_save)
        save_button.grid(column=0, row=60)
        cancel_button = ttk.Button(p2, text="CANCEL", style='my.TButton',
                                   command=p2.destroy)
        cancel_button.grid(column=50, row=60)
        restart_button = ttk.Button(p2, text="RESTART", style='my.TButton',
                                    command=top.destroy)
        restart_button.grid(column=51, row=60)

    def read_serial():
        """Listens to serial monitor for serial data instructions

        Function listens to the serial monitor in order to receive wind-speeds
        being sent from the arduino to the serial port.
        """
        global data
        a = s.readline()
        a.decode()
        if len(data) < 300:  # potentially unnecessary if/else statement
            data = np.append(data, float(a[0:4]))
        else:
            data[0:299] = data[1:300]
            data[299] = float(a[0:4])

    def plot_data():
        """Displays and interprets wind-speed data

        Function starts if a global variable cond is set to true and
        initializes serial port data being received and displayed on the main
        graph. Along with displaying the wind-speed from the arduino in real
        time, the data is compared to the thresholds set by the user in the
        menu page. If the data is above the top threshold, "GOOD INHALE" is
        displayed, and if the data is below the bottom threshold, "GOOD EXHALE"
        is displayed. A count of number of good inhales/exhales is also stored.
        Additional, each good inhale and exhale is timed and stored.
        """
        global cond, data, good_in_message, good_in, threshold_low, \
            threshold_hi, above, below, good_out, good_out_message, x2, \
            r_level, f, time_list_in, start_time, end_time, time_list_ex, \
            start_time2, end_time2

        if cond:
            x2 += 1
            read_serial()
            if len(data) > 2:
                if float(data[-1]) > float(threshold_hi):
                    above = True
                    below = False
                    if float(data[-2]) <= float(threshold_hi):
                        good_in += 1
                        start_time = time.time()
                elif float(data[-1]) < float(threshold_low):
                    below = True
                    above = False
                    if float(data[-2]) > float(threshold_low):
                        good_out += 1
                        start_time2 = time.time()
                else:
                    above = False
                    below = False
                    if float(data[-2]) > float(threshold_hi):
                        end_time = time.time()
                    if float(data[-2]) < float(threshold_low):
                        end_time2 = time.time()
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
                root.update()
            else:
                good_job.config(text="")
                if start_time != 0:
                    if end_time != 0:
                        new_length_in = end_time - start_time
                        time_list_in.append(new_length_in)
                        start_time = 0
                        end_time = 0
                        print(new_length_in)
                if start_time2 != 0:
                    if end_time2 != 0:
                        new_length_ex = end_time2 - start_time2
                        time_list_ex.append(new_length_ex)
                        start_time2 = 0
                        end_time2 = 0
        root.after(1, plot_data)

    def plot_start():
        """Starts serial monitor plot

        Function sets a global variable cond to true in order to initialize
        serial port data being recieved and displayed on the main graph.
        """
        global cond
        cond = True
        s.reset_input_buffer()

    def plot_start2():
        """Starts animated scatter plot

        Function sets a global variable cond2 to true in order to initialize
        scatter plot animation with breathing instructions.
        """
        global cond2
        cond2 = True

    def plot_stop():
        """Stops serial monitor plot

        Function sets a global variable cond to false in order to stop
        serial port data being recieved and displayed on the main graph.
        """
        global cond
        cond = False

    def plot_stop2():
        """Stops animated scatter plot

        Function sets a global variable cond2 to false in order to stop the
        scatter plot animation with breathing instructions.
        """
        global cond2
        cond2 = False

    def play():
        """Plays audio file

        Function plays selected audio file using the pygame mixer plugin. Audio
        file must be in mp3 format and located in specified folder on users
        computer, in this case a test folder on the users Desktop.
        """
        song = f"/Users/haley/Desktop/test/{selected_song}.mp3"
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)

    def stop():
        """Stops audio file

        Function stops selected audio file using the pygame mixer plugin.
        """
        pygame.mixer.music.stop()

    def pause():
        """Pauses audio file

        Function pauses selected audio file using the pygame mixer plugin.
        """
        pygame.mixer.music.pause()

    # create main page
    top = tk.Toplevel(root)
    top.title("Patient Interface")
    # top['bg'] = '#ff60cb'
    top.configure(background="#ececec")
    top.geometry("1600x800")

    # initiate media player
    pygame.mixer.init()

    # initiate main page gui labels
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
    cancel_button = ttk.Button(top, text="Cancel", style='my.TButton',
                               command=cancel_command)
    cancel_button.grid(column=6, row=20)
    menu_button = ttk.Button(top, text="Menu", style='my.TButton',
                             command=top.destroy)
    menu_button.grid(column=2, row=20)
    ttk.Label(top, text="Current Song:", font=f).grid(column=0, row=25)
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
    ax.set_ylabel('Relative Breath Speed')
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
    lower_line = ax.plot(xs, low_thresh, color="#cd5e77")

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
        """Create animated scatter plot

        Function creates an animated scatter plot according to file of test
        data that has three columns that program breathing instructions.
        The data is 3 columns: time in seconds, beat (this is y
        axis of the graph and purely visual so are all the same), and color
        code to correspond to selected in/out/resting instruction colors.

        :param i: iteration index for the animation
        """
        global cond2, x

        if cond2:
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

    ani = FuncAnimation(fig2, animate, frames=255, interval=interval,
                        blit=False)
    canvas2.draw()

    top.update()
    start_button = ttk.Button(top, text="Start", style='my.TButton',
                              command=lambda: [plot_start2(), play(),
                                               plot_start()])
    start_button.grid(column=3, row=20)

    top.update()
    pause_button = ttk.Button(top, text="Pause", style='my.TButton',
                              command=lambda: [plot_stop(), plot_stop2(),
                                               pause()])
    pause_button.grid(column=4, row=20)

    # initialize serial port
    # CHANGE S BASED ON CURRENT PORT
    s = sr.Serial('/dev/cu.usbmodem144101', 9600)
    s.reset_input_buffer()

    # top.after(1, animate)
    top.after(1, plot_data)
    top.mainloop()


def warning():
    """Warning popup page of GUI

    Function opens warning popup page of GUI as risk management when the user
    tries to move to the main program page as a check in on if they have
    entered the resistance level for this session yet.
    """
    warning = tk.Toplevel(root)
    warning.geometry("1000x100")
    warning.configure(background="#ececec")
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
root.configure(background="#ececec")
root.geometry("1500x500")

s = ttk.Style()
s.configure('my.TButton', font=f)

title1 = ttk.Label(root, text="Instructions", font='Mistral 28 bold')
title1.grid(column=0, row=0, columnspan=2, sticky='w')
blue = ttk.Label(root, text="Blue = inhale", font=f)
blue.grid(column=0, row=20, columnspan=1, sticky='w', pady=10)
green = ttk.Label(root, text="Pink = exhale                   ", font=f)
green.grid(column=1, row=20, columnspan=1, sticky='w', pady=10)
brown = ttk.Label(root, text="Black = rest", font=f)
brown.grid(column=2, row=20, columnspan=1, sticky='w', pady=10, padx=[10, 0])
line1 = ttk.Label(root, text="Go above the blue threshold to earn a "
                             "'GREAT INHALE!'", font=f)
line1.grid(column=0, row=40, columnspan=3, sticky='w')
line2 = ttk.Label(root, text="Go below the pink threshold to earn a "
                             "'GREAT EXHALE!'", font=f)
line2.grid(column=0, row=60, columnspan=3, sticky='w')
title2 = ttk.Label(root, text="Music", font='Mistral 28 bold')
title2.grid(column=0, row=90, columnspan=2, sticky='w', pady=[20, 0])
title3 = ttk.Label(root, text="User Specs", font='Mistral 28 bold')
title3.grid(column=0, row=200, columnspan=2, sticky='w', pady=[20, 0])
title4 = ttk.Label(root, text="Song:", font=f)
title4.grid(column=0, row=100, columnspan=2, sticky='w')
title5 = ttk.Label(root, text="Desired Length of Breath (sec) :", font=f)
title5.grid(column=23, row=210, columnspan=2, sticky='w')
breath_length = ttk.Entry(root)
breath_length.grid(column=25, row=210)
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
title10.grid(column=0, row=300, columnspan=1, sticky='w')
title11 = ttk.Label(root, text="Great Exhale Threshold:", font=f)
title11.grid(column=0, row=310, columnspan=1, sticky='w')
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
