class Dashboard:
    def __init__(self, sensors={}):
        self.sensors = sensors

    def add_sensor(self, sensor):
        self.sensors[sensor.name] = sensor

    def add_sensors(self, sensors):
        for sensor in sensors:
            self.add_sensor(sensor)

    def get_sensor(self, name):
        return self.sensors.get(name)

    def update_sensor(self, name, value):
        sensor = self.get_sensor(name)
        if sensor:
            sensor.update(value)
            return True
        return False

    def read_all(self):
        return {sensor.name: sensor.get() for sensor in self.sensors.values()}


my_dashboard = Dashboard()
