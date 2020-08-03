import numpy as np
from tkinter import *
import tkinter as tk
from tkinter import ttk
from constants_thermo_sim import CP, KELVIN, WATERDENSITY, SIGMA, EP, H


class RunThermoSim:

    def __init__(self):
        self.entriesTank = {}
        self.outputFields = ('Required Area (m^2): ', 'Morning Temperature: (ºC)')
        self.fieldsTank = ('Tank Thickness (m)', 'Thermal Conductivity (k of Tank, W/(m*K))',
                           'Thermal Conductivity (k of Insulation, W/(m*K))',
                           'Insulation Thickness (m)', 'Surface Area of Tank (m^2)',
                           'Average Nightly Air Temperature (ºC)',
                           'Hours Overnight')
        self.fieldsBB = (
            'Solar Index', 'Average Daytime Air Temperature (ºC)', 'Initial Water Temperature (ºC)',
            'Final Water Temperature (ºC)', 'Volume of Water (Gal)', 'Hours Per Day')

        self.Tf = 0  # initialize Temperature Final to be a global variable
        self.hrsWithSun = 0

        self.Ti = 0
        self.Tf = 0
        self.A = 0

        self.entriesBB = {}

        self.outputs = {}

        self.V_gal = 0
        self.Af = 0
        self.V = 0

        self.m = 0
        self.sa_tank = 0
        self.cost = 0

        self.delT_ambientTemp_wallTemp = 0

        self.build_gui()

    def calculate_area_black_body(self):

        # Calculations based on heat transfer principles

        # solar index:
        solar_index = float(self.entriesBB['Solar Index'].get())
        print("Solar Index", solar_index)

        # ambient temperature aka average outside temperature, units: celsius (ºC)
        ambient_temperature_black_body = float(self.entriesBB['Average Daytime Air Temperature (ºC)'].get())
        temperature_infinite = ambient_temperature_black_body + KELVIN  # units: converted ºC to Kelvin (K)

        # initial water temperature, units: celsius (ºC), 20 for our test
        initial_temperature = float(self.entriesBB['Initial Water Temperature (ºC)'].get())
        self.Ti = initial_temperature + KELVIN  # units: converted celsius (ºC) to Kelvin (K)

        # final water temperature in celsius (ºC), 50 for our test
        final_temperature = float(self.entriesBB['Final Water Temperature (ºC)'].get())
        # Tf = finalTemp + kelvin  # units: converted celsius (ºC) to Kelvin (K)
        self.Tf = final_temperature + KELVIN

        # volume, units: gallons (Gal), 134 gallons in our test
        self.V_gal = float(self.entriesBB['Volume of Water (Gal)'].get())

        # volume, units: converted into m^3
        self.V = self.V_gal / 264.17

        # mass of water in tank, units: kg
        self.m = self.V * WATERDENSITY

        # delT_bb = Tf - T_gnd_bb

        # number of hours (hrs) to heat water
        hours_in_sun: float = float(self.entriesBB['Hours Per Day'].get())
        time = hours_in_sun * 3600  # units: converted hrs to seconds

        delta_temperature_glass_and_black_body = -2.5  # temperature difference glass and black body

        # solve for area and output it.
        self.A = (self.m * CP * (self.Tf - self.Ti)) / (
                (solar_index - EP * SIGMA * ((self.Tf ** 4) - (temperature_infinite ** 4)) -
                 (H * delta_temperature_glass_and_black_body)) * time)
        self.Af = np.round(self.A, 2)
        print(f'The final required area is {self.Af} m^2 to achieve {final_temperature}ºC under the conditions')

        self.outputs['Required Area (m^2): '].delete(0, tk.END)
        self.outputs['Required Area (m^2): '].insert(0, self.Af)

    def ins_tank(self):

        # tank thickness, 0.005 for our test
        t_tank = float(self.entriesTank['Tank Thickness (m)'].get())

        # thermal conductivity tank, 0.3 for our test
        k_tank = float(self.entriesTank['Thermal Conductivity (k of Tank, W/(m*K))'].get())

        # thermal conductivity of insulation used to calculate R (thermal conductivity)
        k_ins = float(self.entriesTank['Thermal Conductivity (k of Insulation, W/(m*K))'].get())

        # thickness of insulation used to calculate R (thermal conductivity)
        t_ins = float(self.entriesTank['Insulation Thickness (m)'].get())

        heat_transfer_coefficient = 7
        # surface area of tank, units: m^2
        self.sa_tank = float(self.entriesTank['Surface Area of Tank (m^2)'].get())

        # thermal resistance, units: (m^2 * K)/W
        # resistance value of heat transfer crossing boundaries
        # for standard fiberglass: R_ins = 15
        r_ins = t_ins / (k_ins * self.sa_tank)
        r_tank = t_tank / (k_tank * self.sa_tank)  # units: (m^2 * K)/W
        r_total = r_ins + r_tank  # units: (m^2 * K)/W, 16 for our test

        # the temperature of what is surrounding the tank overnight
        # ambient temperature for tank, avg night temperature
        ambient_tank_temperature = float(self.entriesTank['Average Nightly Air Temperature (ºC)'].get())
        ambient_tank_temperature_kelvin = ambient_tank_temperature + KELVIN  # units: converted

        self.Ti = self.Tf

        delta_tank_temperature_kelvin = self.Ti - ambient_tank_temperature_kelvin  # units: Kelvin (K)

        # energy, units: W
        q = ((
                     delta_tank_temperature_kelvin * self.sa_tank) / r_total) + \
            heat_transfer_coefficient * self.sa_tank * self.delT_ambientTemp_wallTemp

        # number of hours spent w/o energy coming in from the sun, 18 for our test
        # this is the time in hours that the water begins to loose energy
        hours_without_sun = float(self.entriesTank['Hours Overnight'].get())
        hours_without_sun_tank = 24 - hours_without_sun
        time = hours_without_sun_tank * 3600  # conversion of time into seconds

        # total energy coming into tank, units: Joules (J)
        energy_gain = delta_tank_temperature_kelvin * self.m * CP
        # total energy lost, units: Joules (J)
        energy_loss = q * time

        # percentage of energy lost, units: %
        loss_ratio = (1 - ((energy_gain - energy_loss) / energy_gain)) * 100
        # morning temperature of water, units: celsius (ºC)
        morning_water_temperature = (energy_gain - energy_loss) / (self.m * CP) + ambient_tank_temperature

        t_morn = round(morning_water_temperature, 2)

        print(
            f"The morning water temperature will be: {t_morn}ºC with {round(loss_ratio, 2)}% energy lost")

        # outputs
        self.outputs['Morning Temperature: (ºC)'].delete(0, tk.END)
        self.outputs['Morning Temperature: (ºC)'].insert(0, t_morn)

    def make_form(self, root):  # fieldsBB, fieldsTank, outputFields:

        entries_frame = ttk.Frame(root)
        entries_frame.grid(row=0, column=0, rowspan=5, columnspan=6, sticky=W + E + N + S)

        count_black_body = int(0)
        count_tank = int(0)

        for field in self.fieldsBB:
            print(field)
            label_black_body = ttk.Label(entries_frame, width=27, text=field + ": ", style="GP.TLabel")
            entry_black_body = ttk.Entry(entries_frame, width=15)
            entry_black_body.insert(0, "0")
            label_black_body.grid(row=count_black_body, column=0)
            entry_black_body.grid(row=count_black_body, column=1)
            self.entriesBB[field] = entry_black_body
            count_black_body += int(1)

        for field in self.fieldsTank:
            print(field)
            label_temperature = ttk.Label(entries_frame, width=33, text=field + ": ", style="GP.TLabel")
            entry_temperature = ttk.Entry(entries_frame, width=15)
            entry_temperature.insert(0, "0")

            label_temperature.grid(row=count_tank, column=2)
            entry_temperature.grid(row=count_tank, column=3)
            self.entriesTank[field] = entry_temperature
            count_tank += int(1)

        labels_column_count = int(0)
        entries_column_count = int(1)
        for output in self.outputFields:
            result_labels = ttk.Label(entries_frame, width=20, text=output, foreground='Purple3')
            result_labels.grid(row=10, column=labels_column_count, padx=5, pady=5)

            result_entries = ttk.Entry(entries_frame, width=15)
            result_entries.grid(row=10, column=entries_column_count, padx=5, pady=5)
            labels_column_count += int(2)
            entries_column_count += int(2)

            self.outputs[output] = result_entries

    def build_gui(self):
        root = tk.Tk()
        root.geometry("1260x800")
        root.title("Thermo Sim for Passive Logic")
        self.make_form(root)

        style = ttk.Style()
        style.theme_use('classic')
        style.configure("GP.TLabel", foreground="goldenrod", background='blanched almond')

        ttk.Button(root, text='Calculate Area',
                   command=(lambda e: self.calculate_area_black_body())).grid(row=9, column=0, padx=5, pady=5)

        ttk.Button(root, text='Calculate Morning Temperature',
                   command=(lambda e: self.ins_tank())).grid(row=9, column=3, padx=5, pady=5)

        ttk.Button(root, text='Quit', command=root.quit).grid(row=12, column=5, padx=5, pady=5)

        root.mainloop()


if __name__ == '__main__':
    RunThermoSim()
