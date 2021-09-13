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
        title1 = ttk.Label(top, text="Instructions")
        title1.grid(column=0, row=0, columnspan=2, sticky='w')

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
