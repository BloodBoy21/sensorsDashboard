from .dashboard import my_dashboard


class Sensor:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.value = 0

    def update(self, value):
        self.value = value

    def get(self):
        return self.value


list_of_sensors = [
    Sensor("humidity", "Living Room"),
    Sensor("light", "Bedroom"),
    Sensor("temperature", "Living Room"),
]

my_dashboard.add_sensors(list_of_sensors)
