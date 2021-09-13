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
        return

    def open_popup():
        top = tk.Toplevel(root)
        top.geometry("750x250")
        top.title("Menu")
        title1 = ttk.Label(top, text="Instructions", font='Mistral 18 bold')
        title1.grid(column=0, row=0, columnspan=2, sticky='w')
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
        song["values"] = ["Happy Birthday", "Don't Stop Believin", "Bohemian Rhapsody"]
        song.grid(column=10, row=100)
        title7 = ttk.Label(top, text="Weight:")
        title7.grid(column=0, row=210, columnspan=2, sticky='w')
        weight = ttk.Entry(top)
        weight.grid(column=10, row=210, columnspan=2)
        title8 = ttk.Label(top, text="kg")
        title8.grid(column=15, row=210, columnspan=2, sticky='w')
        title8 = ttk.Label(top, text="Resistance Level:")
        title8.grid(column=35, row=210, columnspan=2, sticky='w')
        levels = tk.StringVar()
        level = ttk.Combobox(top, textvariable=levels)
        level["values"] = [1, 2, 3]
        level.grid(column=40, row=210)

    root = tk.Tk()
    root.title("Mock Patient Interface")

    top_label = ttk.Label(root, text="Patient Interface")
    top_label.grid(column=0, row=0, columnspan=2, sticky='w')

    ttk.Label(root, text="Pick Patient Name:").grid(column=0, row=1)
    patient_ids = tk.StringVar()
    patient = ttk.Combobox(root, textvariable=patient_ids)
    patient.grid(column=1, row=1)
    # r = requests.get(server + "/patientids")
    # patient["values"] = json.loads(r.text)
    test = ["haley", "rachel", "phoebe", "claire"]
    patient["values"] = test
    # this will be request to server to get
    # list of patient names from server
    # patient.state(["readonly"])  # can only chose ids that exist

    cancel_button = ttk.Button(root, text="End Session", command=cancel_command)
    cancel_button.grid(column=4, row=20)
    menu_button = ttk.Button(root, text="Menu", command=open_popup)
    menu_button.grid(column=2, row=20)
    pause_button = ttk.Button(root, text="Pause", command=open_popup)
    pause_button.grid(column=3, row=20)

    # root.after(3000, data_refresh)
    root.mainloop()


if __name__ == '__main__':
    design_window()
