import numpy as np
import tkinter as tk
from constants_thermo_sim import CP, KELVIN, WATERDENSITY, SIGMA, EP, H


class ThermoSimController:
    def __init__(self):
        self.model = None

    def calculate_area_black_body(self):
        # this function calculates how much energy will be transferred from the sun into the water

        # Calculations based on heat transfer principles

        # solar index:
        solar_index = float(self.model.entries_black_body['Solar Index'].get())
        print("Solar Index", solar_index)

        # ambient temperature aka average outside temperature, units: celsius (ºC)
        ambient_temperature_black_body = float(self.model.entries_black_body['Average Daytime Air Temperature (ºC)'].get())
        temperature_infinite = ambient_temperature_black_body + KELVIN  # units: converted ºC to Kelvin (K)

        # initial water temperature, units: celsius (ºC), 20 for our test
        initial_temperature = float(self.model.entries_black_body['Initial Water Temperature (ºC)'].get())
        self.model.temperature_initial = initial_temperature + KELVIN  # units: converted celsius (ºC) to Kelvin (K)

        # final water temperature in celsius (ºC), 50 for our test
        final_temperature = float(self.model.entries_black_body['Final Water Temperature (ºC)'].get())
        # Tf = finalTemp + kelvin  # units: converted celsius (ºC) to Kelvin (K)
        self.model.temperature_final = final_temperature + KELVIN

        # volume, units: gallons (Gal), 134 gallons in our test
        self.model.volume_gal = float(self.model.entries_black_body['Volume of Water (Gal)'].get())

        # volume, units: converted into m^3
        self.model.volume = self.model.volume_gal / 264.17

        # mass of water in tank, units: kg
        self.model.mass = self.model.volume * WATERDENSITY

        # delT_bb = Tf - T_gnd_bb

        # number of hours (hrs) to heat water
        hours_in_sun: float = float(self.model.entries_black_body['Hours Per Day'].get())
        time = hours_in_sun * 3600  # units: converted hrs to seconds

        delta_temperature_glass_and_black_body = -2.5  # temperature difference glass and black body

        # solve for area and output it.
        self.model.area = (self.model.mass * CP * (self.model.temperature_final - self.model.temperature_initial)) / (
                (solar_index - EP * SIGMA * ((self.model.temperature_final ** 4) - (temperature_infinite ** 4)) -
                 (H * delta_temperature_glass_and_black_body)) * time)
        self.model.area_final = np.round(self.model.area, 2)
        print(f'The final required area is {self.model.area_final} m^2 to achieve {final_temperature}ºC under the conditions')

        self.model.outputs['Required Area (m^2): '].delete(0, tk.END)
        self.model.outputs['Required Area (m^2): '].insert(0, self.model.area_final)

    def ins_tank(self):
        # this function calculates the heat transfer for the tank while the water is being stored overnight

        # tank thickness, 0.005 for our test
        t_tank = float(self.model.entriesTank['Tank Thickness (m)'].get())

        # thermal conductivity tank, 0.3 for our test
        k_tank = float(self.model.entriesTank['Thermal Conductivity (k of Tank, W/(m*K))'].get())

        # thermal conductivity of insulation used to calculate R (thermal conductivity)
        k_ins = float(self.model.entriesTank['Thermal Conductivity (k of Insulation, W/(m*K))'].get())

        # thickness of insulation used to calculate R (thermal conductivity)
        t_ins = float(self.model.entriesTank['Insulation Thickness (m)'].get())

        heat_transfer_coefficient = 7
        # surface area of tank, units: m^2
        self.model.surface_area_tank = float(self.model.entriesTank['Surface Area of Tank (m^2)'].get())

        # thermal resistance, units: (m^2 * K)/W
        # resistance value of heat transfer crossing boundaries
        # for standard fiberglass: R_ins = 15
        r_ins = t_ins / (k_ins * self.model.surface_area_tank)
        r_tank = t_tank / (k_tank * self.model.surface_area_tank)  # units: (m^2 * K)/W
        r_total = r_ins + r_tank  # units: (m^2 * K)/W

        # the temperature of what is surrounding the tank overnight
        # ambient temperature for tank, avg night temperature
        ambient_tank_temperature = float(self.model.entriesTank['Average Nightly Air Temperature (ºC)'].get())
        ambient_tank_temperature_kelvin = ambient_tank_temperature + KELVIN  # units: converted

        self.model.temperature_initial = self.model.temperature_final

        delta_tank_temperature_kelvin = self.model.temperature_initial - ambient_tank_temperature_kelvin  # units: Kelvin (K)

        # energy, units: W
        q = ((
                     delta_tank_temperature_kelvin * self.model.surface_area_tank) / r_total) + \
            heat_transfer_coefficient * self.model.surface_area_tank * self.model.delT_ambientTemp_wallTemp

        hours_without_sun = float(self.model.entriesTank['Hours Overnight'].get())
        hours_without_sun_tank = 24 - hours_without_sun
        time = hours_without_sun_tank * 3600  # conversion of time into seconds

        # total energy coming into tank, units: Joules (J)
        energy_gain = delta_tank_temperature_kelvin * self.model.mass * CP
        # total energy lost, units: Joules (J)
        energy_loss = q * time

        # percentage of energy lost, units: %
        loss_ratio = (1 - ((energy_gain - energy_loss) / energy_gain)) * 100
        # morning temperature of water, units: celsius (ºC)
        morning_water_temperature = (energy_gain - energy_loss) / (self.model.mass * CP) + ambient_tank_temperature

        t_morn = round(morning_water_temperature, 2)

        print(
            f"The morning water temperature will be: {t_morn}ºC with {round(loss_ratio, 2)}% energy lost")

        # outputs
        self.model.outputs['Morning Temperature: (ºC)'].delete(0, tk.END)
        self.model.outputs['Morning Temperature: (ºC)'].insert(0, t_morn)