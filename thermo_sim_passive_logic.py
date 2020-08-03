import numpy as np
from tkinter import *
import tkinter as tk
from tkinter import ttk


class RunThermoSim:

    def __init__(self):

        self.outputFields = ('Required Area (m^2): ', 'Morning Temperature: (ºC)')
        self.fieldsTank = ('Tank Thickness (m)', 'Thermal Conductivity (k of Tank, W/(m*K))',
                           'Thermal Conductivity (k of Insulation, W/(m*K))',
                           'Insulation Thickness (m)', 'Surface Area of Tank (m^2)',
                           'Average Nightly Air Temperature (ºC)',
                           'Hours Overnight')
        self.fieldsBB = (
            'Solar Index', 'Average Daytime Air Temperature (ºC)', 'Initial Water Temperature (ºC)',
            'Final Water Temperature (ºC)', 'Volume of Water (Gal)', 'Hours Per Day')
        self.initialize_variables()
        self.build_gui()
        self.Tf = 0  # initialize Temperature Final to be a global variable
        self.hrsWithSun = 0

        self.Ti = 0
        self.Tf = 0
        self.A = 0

        self.entriesBB = {}
        self.entriesTank = {}
        self.outputs = {}

        self.V_gal = 0

        self.V = 0

        self.m = 0

        self.cost = 0

        self.delT_ambientTemp_wallTemp = 0

    def initialize_variables(self) -> None:
        # Calculations based on heat transfer principles

        # solar index:
        solar_index = float(self.entriesBB['Solar Index'].get())
        print("Solar Index", solar_index)

        # ambient temperature aka average outside temperature, units: celsius (ºC)
        ambient_temperature_black_body: float = float(self.entriesBB['Average Daytime Air Temperature (ºC)'].get())
        temperature_infinite = ambient_temperature_black_body + self.kelvin  # units: converted ºC to Kelvin (K)

        # initial water temperature, units: celsius (ºC), 20 for our test
        initial_temperature = float(self.entriesBB['Initial Water Temperature (ºC)'].get())
        self.Ti = initial_temperature + self.kelvin  # units: converted celsius (ºC) to Kelvin (K)

        # final water temperature in celsius (ºC), 50 for our test
        final_temperature = float(self.entriesBB['Final Water Temperature (ºC)'].get())
        # Tf = finalTemp + kelvin  # units: converted celsius (ºC) to Kelvin (K)
        self.Tf = final_temperature + self.kelvin

        # volume, units: gallons (Gal), 134 gallons in our test
        self.V_gal = float(self.entriesBB['Volume of Water (Gal)'].get())

        # volume, units: converted into m^3
        self.V = self.V_gal / 264.17

        # mass of water in tank, units: kg
        self.m = self.V * self.densityOfWater

        # delT_bb = Tf - T_gnd_bb
        h = 3  # worst case convective heat transfer coefficient

        # number of hours (hrs) to heat water, 5.5 for our test
        hours_in_sun: float = float(self.entriesBB['Hours Per Day'].get())
        time = hours_in_sun * 3600  # units: converted hrs to seconds

        deltaT_airPlexiAndBB_waterTempBB = -2.5
        # solve for area and output it.
        self.A = (self.m * self.Cp * (self.Tf - self.Ti)) / (
                (solar_index - e * sigma * ((self.Tf ** 4) - (temperature_infinite ** 4)) - (h * deltaT_airPlexiAndBB_waterTempBB)) * time)
        self.Af = np.round(self.A, 2)
        print(f'The final required area is {self.Af} m^2 to achieve {final_temperature}ºC under the conditions')  # check boxes:

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

        h = 7
        # surface area of tank, units: m^2, 8.7 for our test
        self.sa_tank = float(self.entriesTank['Surface Area of Tank (m^2)'].get())

        # thermal resistance, units: (m^2 * K)/W
        # resistance value of heat transfer crossing boundaries
        # for standard fiberglass: R_ins = 15
        R_ins = t_ins / (k_ins * self.sa_tank)
        R_tank = t_tank / (k_tank * self.sa_tank)  # units: (m^2 * K)/W
        R_total = R_ins + R_tank  # units: (m^2 * K)/W, 16 for our test

        # the temperature of what is surrounding the tank overnight
        # ambient temperature for tank, avg night temperature
        ambientTemp_tank = float(self.entriesTank['Average Nightly Air Temperature (ºC)'].get())
        ambientTemp_tank_K = ambientTemp_tank + self.kelvin  # units: converted

        self.Ti = self.Tf

        delT_tank = self.Ti - ambientTemp_tank_K  # units: Kelvin (K)

        # energy, units: W
        q = ((delT_tank * self.sa_tank) / R_total) + h * self.sa_tank * self.delT_ambientTemp_wallTemp

        # number of hours spent w/o energy coming in from the sun, 18 for our test
        # hrs_tank = float(entries['Hours Overnight'].get())
        # this is the time in hours that the water begins to loose energy
        hrsWithoutSun = float(self.entriesTank['Hours Overnight'].get())
        hrsWithoutSun_tank = 24 - hrsWithoutSun
        time = hrsWithoutSun_tank * 3600  # conversion of time into seconds

        # total energy coming into tank, units: Joules (J)
        energyGained = delT_tank * self.m * self.Cp
        # total energy lost, units: Joules (J)
        energyLost = q * time

        # percentage of energy lost, units: %
        lossRatio = (1 - ((energyGained - energyLost) / energyGained)) * 100
        # morning temperature of water, units: celsius (ºC)
        morningWaterTemp = (energyGained - energyLost) / (self.m * self.Cp) + ambientTemp_tank

        tMorn = round(morningWaterTemp, 2)

        print(
            f'The morning water temperature will be: {tMorn}ºC with {round(lossRatio, 2)}% energy lost')
        ######### outputs #########
        self.outputs['Morning Temperature: (ºC)'].delete(0, tk.END)
        self.outputs['Morning Temperature: (ºC)'].insert(0, tMorn)


    def make_form(self, root):  # fieldsBB, fieldsTank, outputFields):

        entriesFrame = ttk.Frame(root)
        entriesFrame.grid(row=0, column=0, rowspan=5, columnspan=6, sticky=W + E + N + S)

        countBB = int(0)
        countTank = int(0)
        countHL = int(0)

        for field in self.fieldsBB:
            print(field)
            labBB = ttk.Label(entriesFrame, width=27, text=field + ": ", style="GP.TLabel")
            entBB = ttk.Entry(entriesFrame, width=15)
            entBB.insert(0, "0")
            labBB.grid(row=countBB, column=0)
            entBB.grid(row=countBB, column=1)
            self.entriesBB[field] = entBB
            countBB += int(1)

        for field in self.fieldsTank:
            print(field)
            labT = ttk.Label(entriesFrame, width=33, text=field + ": ", style="GP.TLabel")
            entT = ttk.Entry(entriesFrame, width=15)
            entT.insert(0, "0")

            labT.grid(row=countTank, column=2)
            entT.grid(row=countTank, column=3)
            self.entriesTank[field] = entT
            countTank += int(1)

        labelsColCount = int(0)
        entriesColCount = int(1)
        for output in self.outputFields:
            resultLabels = ttk.Label(entriesFrame, width=20, text=output, foreground='Purple3')
            resultLabels.grid(row=10, column=labelsColCount, padx=5, pady=5)

            resultEntries = ttk.Entry(entriesFrame, width=15)
            resultEntries.grid(row=10, column=entriesColCount, padx=5, pady=5)
            labelsColCount += int(2)
            entriesColCount += int(2)

            self.outputs[output] = resultEntries

    def build_gui(self):
        root = tk.Tk()
        root.geometry("1260x800")
        root.title("Thermo Sim for Passive Logic")
        ents = self.make_form(root)

        style = ttk.Style()
        style.theme_use('classic')
        style.configure("GP.TLabel", foreground="darkgoldenrod", background='blanched almond')

        b1 = ttk.Button(root, text='Calculate Area',
                        command=(lambda e=ents: self.calculate_area_bb())).grid(row=9, column=0, padx=5, pady=5)

        b2 = ttk.Button(root, text='Calculate Morning Temperature',
                        command=(lambda e=ents: self.ins_tank())).grid(row=9, column=3, padx=5, pady=5)

        b4 = ttk.Button(root, text='Quit', command=root.quit).grid(row=12, column=5, padx=5, pady=5)

        root.mainloop()


if __name__ == '__main__':
    RunThermoSim()
