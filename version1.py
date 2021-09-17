import tkinter as tk
from tkinter import ttk, messagebox


def design_window():
    def cancel_command():
        """H Function to control cancel button

        This function destroys the gui, to be called when the cancel button is
        pressed. It also prints cancel to the consul when this occurs.
        """
        print("Cancel")
        root.destroy()
        return

    def ok_command():
        """H Function to control ok button 1

        This function retrieves the selected patient id number from the
        dropdown menu after one is selected and the OK button is pressed.
        After being pressed, requests are made to the server to retrieve
        and display that patient's name, most recent heart rate, most recent
        ecg image, and most recent ecg download timestamp. If the patient gui
        is working (as set by the global variable patient_side_working) the
        ecg image retrieval request is made for the b64 string and if not, a
        test acl image from the local directory is encoded to a b64 string.
        The b64 string (whether real or "fake") is then converted to an ndarry
        and displayed. The ecg and medical image dropdowns are then populated
        with the specified patient's available ecg images (labeled by
        timestamp) and medical images (labeled by index number).
        """
        # Get Data From GUI
        p_id = str(patient.get())
        # this will be where ok button of menu updates preferences
        return

    def open_popup():
        top = tk.Toplevel(root)
        top.geometry("1000x400")
        top.title("Menu")
        title1 = ttk.Label(top, text="Instructions", font='Mistral 18 bold')
        title1.grid(column=0, row=0, columnspan=2, sticky='w')
        blue = ttk.Label(top, text="Blue = inhale")
        blue.grid(column=0, row=20, columnspan=2, sticky='w')
        green = ttk.Label(top, text="Green = exhale")
        green.grid(column=10, row=20, columnspan=2, sticky='w')
        brown = ttk.Label(top, text="Brown = rest")
        brown.grid(column=20, row=20, columnspan=2, sticky='w')
        line1 = ttk.Label(top, text="Go above the blue threshold to earn a "
                                    "'GREAT INHALE!'")
        line1.grid(column=0, row=40, columnspan=2, sticky='w')
        line2 = ttk.Label(top, text="Go below the green threshold to earn a "
                                    "'GREAT EXHALE!'")
        line2.grid(column=0, row=60, columnspan=2, sticky='w')
        title2 = ttk.Label(top, text="Music", font='Mistral 18 bold')
        title2.grid(column=0, row=90, columnspan=2, sticky='w')
        title3 = ttk.Label(top, text="User", font='Mistral 18 bold')
        title3.grid(column=0, row=200, columnspan=2, sticky='w')
        title4 = ttk.Label(top, text="Song:")
        title4.grid(column=0, row=100, columnspan=2, sticky='w')
        title5 = ttk.Label(top, text="BPM:")
        title5.grid(column=35, row=100, columnspan=2, sticky='w')
        bpm = ttk.Entry(top)
        bpm.grid(column=40, row=100)
        songs = tk.StringVar()
        song = ttk.Combobox(top, textvariable=songs)
        song["values"] = ["Happy Birthday", "Don't Stop Believin",
                          "Bohemian Rhapsody"]
        song.grid(column=10, row=100)
        title7 = ttk.Label(top, text="Weight:")
        title7.grid(column=0, row=210, columnspan=2, sticky='w')
        weight = ttk.Entry(top)
        weight.grid(column=10, row=210, columnspan=2)
        title8 = ttk.Label(top, text="kg")
        title8.grid(column=15, row=210, columnspan=2, sticky='w')
        title9 = ttk.Label(top, text="Resistance Level:")
        title9.grid(column=35, row=210, columnspan=2, sticky='w')
        levels = tk.StringVar()
        level = ttk.Combobox(top, textvariable=levels)
        level["values"] = [1, 2, 3]
        level.grid(column=40, row=210)
        title10 = ttk.Label(top, text="Great Inhale Threshold:")
        title10.grid(column=0, row=300, columnspan=2, sticky='w')
        title11 = ttk.Label(top, text="Great Exhale Threshold:")
        title11.grid(column=0, row=310, columnspan=2, sticky='w')
        units1 = ttk.Label(top, text="mL/kg")
        units1.grid(column=15, row=300, columnspan=2, sticky='w')
        units2 = ttk.Label(top, text="mL/kg")
        units2.grid(column=15, row=310, columnspan=2, sticky='w')
        inhale = ttk.Entry(top)
        inhale.grid(column=10, row=300, columnspan=2)
        exhale = ttk.Entry(top)
        exhale.grid(column=10, row=310, columnspan=2)
        update_button = ttk.Button(top, text="Update", command=ok_command())
        update_button.grid(column=40, row=350)

    def open_popup2():
        p2 = tk.Toplevel(root)
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

    root = tk.Tk()
    root.title("Mock Patient Interface")

    top_label = ttk.Label(root, text="Welcome!")
    top_label.grid(column=0, row=0, columnspan=2, sticky='w')

    ttk.Label(root, text="Pick Patient Name:").grid(column=0, row=1)
    patient_ids = tk.StringVar()
    patient = ttk.Combobox(root, textvariable=patient_ids)
    patient.grid(column=1, row=1)
    test = ["haley", "rachel", "phoebe", "claire"]
    patient["values"] = test
    ttk.Label(root, text="Click Menu to enter preferences, "
                         "then Start to begin session!").grid(column=0, row=20)

    end_button = ttk.Button(root, text="End Session", command=open_popup2)
    end_button.grid(column=5, row=20)
    cancel_button = ttk.Button(root, text="Cancel",
                               command=cancel_command)
    cancel_button.grid(column=6, row=20)
    menu_button = ttk.Button(root, text="Menu", command=open_popup)
    menu_button.grid(column=2, row=20)
    start_button = ttk.Button(root, text="Start")  # change command
    start_button.grid(column=3, row=20)
    pause_button = ttk.Button(root, text="Pause")  # change command
    pause_button.grid(column=4, row=20)

    # root.after(3000, data_refresh)
    root.mainloop()


if __name__ == '__main__':
    design_window()
