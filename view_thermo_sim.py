from tkinter import *
import tkinter as tk
from tkinter import ttk


class ThermoSimView:
    def __init__(self):
        self.controller = None
        self.model = None

    def make_form(self, root):  # fields black body, fieldsTank, outputFields:

        entries_frame = ttk.Frame(root)
        entries_frame.grid(row=0, column=0, rowspan=5, columnspan=6, sticky=W + E + N + S)

        count_black_body = int(0)
        count_tank = int(0)

        for field in self.model.fieldsBB:
            print(field)
            label_black_body = ttk.Label(entries_frame, width=27, text=field + ": ", style="GP.TLabel")
            entry_black_body = ttk.Entry(entries_frame, width=15)
            entry_black_body.insert(0, "0")
            label_black_body.grid(row=count_black_body, column=0)
            entry_black_body.grid(row=count_black_body, column=1)
            self.model.entries_black_body[field] = entry_black_body
            count_black_body += int(1)

        for field in self.model.fieldsTank:
            print(field)
            label_temperature = ttk.Label(entries_frame, width=33, text=field + ": ", style="GP.TLabel")
            entry_temperature = ttk.Entry(entries_frame, width=15)
            entry_temperature.insert(0, "0")

            label_temperature.grid(row=count_tank, column=2)
            entry_temperature.grid(row=count_tank, column=3)
            self.model.entriesTank[field] = entry_temperature
            count_tank += int(1)

        labels_column_count = int(0)
        entries_column_count = int(1)
        for output in self.model.outputFields:
            result_labels = ttk.Label(entries_frame, width=20, text=output, foreground='Purple3')
            result_labels.grid(row=10, column=labels_column_count, padx=5, pady=5)

            result_entries = ttk.Entry(entries_frame, width=15)
            result_entries.grid(row=10, column=entries_column_count, padx=5, pady=5)
            labels_column_count += int(2)
            entries_column_count += int(2)

            self.model.outputs[output] = result_entries

    def build_gui(self):
        root = tk.Tk()
        root.title("Thermo Sim for Passive Logic")
        self.make_form(root)

        style = ttk.Style()
        style.theme_use('classic')
        style.configure("GP.TLabel", foreground="goldenrod", background='blanched almond')

        ttk.Button(root, text='Calculate Area',
                   command=self.controller.calculate_area_black_body).grid(row=9, column=0, padx=5, pady=5)

        ttk.Button(root, text='Calculate Morning Temperature',
                   command=self.controller.ins_tank).grid(row=9, column=3, padx=5, pady=5)

        ttk.Button(root, text='Quit', command=root.quit).grid(row=12, column=5, padx=5, pady=5)

        root.mainloop()