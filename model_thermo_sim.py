class ThermoSimModel:

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

        self.temperature_final = 0  # initialize Temperature Final to be a global variable
        self.hrsWithSun = 0

        self.temperature_initial = 0
        self.temperature_final = 0
        self.area = 0

        self.entries_black_body = {}

        self.outputs = {}

        self.volume_gal = 0
        self.area_final = 0
        self.volume = 0

        self.mass = 0
        self.surface_area_tank = 0
        self.cost = 0

        self.delT_ambientTemp_wallTemp = 0

