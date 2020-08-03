from model_thermo_sim import ThermoSimModel
from view_thermo_sim import ThermoSimView
from controller_thermo_sim import ThermoSimController

model = ThermoSimModel()
view = ThermoSimView()
controller = ThermoSimController()
view.controller = controller
view.model = model
controller.model = model


if __name__ == '__main__':
    view.build_gui()

