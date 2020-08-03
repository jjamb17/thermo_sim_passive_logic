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

        self.Ti = 0
        self.temperature_final = 0
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

