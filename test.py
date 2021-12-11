#
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
# from tkinter import Tk, Canvas
# import time
#
# def mainloop():
#     root = Tk()
# # you can do geometry and title if you want
#     def func():
#         c.itemconfig(line, state="normal")
#         time.sleep(1)
#         c.itemconfig(line, state="hidden")
#         root.after(10000, func)
#     c = Canvas(root, width=800, height=500) # you can change height and width
#     line = c.create_line(0, 0, 400, 250, fill="", state="hidden")
#     root.after(1, func)
#
#     root.mainloop()
#
#
# if __name__ == '__main__':
#     mainloop()

# fig, ax = plt.subplots(figsize=(5, 3))
#
# x = np.linspace(-3, 3, 91)
# t = np.linspace(1, 25, 30)
# X2, T2 = np.meshgrid(x, t)
#
# sinT2 = np.sin(2 * np.pi * T2 / T2.max())
# F = 0.9 * sinT2 * np.sinc(X2 * (1 + sinT2))
#
# ax.set(xlim=(-3, 3), ylim=(-1, 1))
# scat = ax.scatter(x[::3], F[0, ::3])
#
#
# def animate(i):
#     y_i = F[i, ::3]
#     scat.set_offsets(np.c_[x[::3], y_i])
#
#
# anim = FuncAnimation(
#     fig, animate, interval=100, frames=len(t) - 1)
#
# plt.draw()
# plt.show()

# import numpy as np
# import matplotlib.pyplot as plt
# x=0
# for i in range(100):
#     x=x+0.04
#     y = np.sin(x)
#     plt.scatter(x, y)
#     plt.title("Real Time plot")
#     plt.xlabel("x")
#     plt.ylabel("sinx")
#     plt.pause(0.05)
#
# plt.show()

import tkinter as tk
from tkinter import ttk

LARGEFONT = ("Verdana", 35)


class tkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, Page1, Page2):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# first window frame startpage

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # label of frame Layout 2
        label = ttk.Label(self, text="Startpage", font=LARGEFONT)

        # putting the grid in its place by using
        # grid
        label.grid(row=0, column=4, padx=10, pady=10)

        button1 = ttk.Button(self, text="Page 1",
                             command=lambda: controller.show_frame(Page1))

        # putting the button in its place by
        # using grid
        button1.grid(row=1, column=1, padx=10, pady=10)

        ## button to show frame 2 with text layout2
        button2 = ttk.Button(self, text="Page 2",
                             command=lambda: controller.show_frame(Page2))

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=1, padx=10, pady=10)


# second window frame page1
class Page1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page 1", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="StartPage",
                             command=lambda: controller.show_frame(StartPage))

        # putting the button in its place
        # by using grid
        button1.grid(row=1, column=1, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button2 = ttk.Button(self, text="Page 2",
                             command=lambda: controller.show_frame(Page2))

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=1, padx=10, pady=10)


# third window frame page2
class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page 2", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="Page 1",
                             command=lambda: controller.show_frame(Page1))

        # putting the button in its place by
        # using grid
        button1.grid(row=1, column=1, padx=10, pady=10)

        # button to show frame 3 with text
        # layout3
        button2 = ttk.Button(self, text="Startpage",
                             command=lambda: controller.show_frame(StartPage))

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=1, padx=10, pady=10)


# Driver Code
app = tkinterApp()
app.mainloop()
