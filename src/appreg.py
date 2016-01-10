
from apps.datedisp import DateTimeApp
from apps.cycle import CycleIndicatorApp
from apps.rpitemp import RPiTemperature

def init_apps(scrman):
    scrman.add_app(height=1, width=45, y=0, x=0, app=DateTimeApp())
    scrman.add_app(height=1, width=2, y=0, x=52, app=CycleIndicatorApp())
    scrman.add_app(height=1, width=52, y=3, x=0, app=RPiTemperature())

