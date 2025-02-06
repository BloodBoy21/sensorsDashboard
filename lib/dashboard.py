from .sensor import Sensor
from typing import List
import json
from fasthtml.common import (
    Div,
    Script,
)


class Dashboard:
    def __init__(self, sensors={}):
        self.sensors: List[Sensor] = sensors

    def add_sensor(self, sensor: Sensor):
        self.sensors[sensor.name] = sensor

    def add_sensors(self, sensors: List[Sensor]):
        for sensor in sensors:
            self.add_sensor(sensor)

    def get_sensor(self, name) -> Sensor:
        return self.sensors.get(name)

    def update_sensor(self, name: str, value: float):
        sensor = self.get_sensor(name)
        if sensor:
            sensor.update(value)
            return True
        return False

    def read_all(self) -> dict[str, float]:
        sensors: List[Sensor] = self.sensors.values()
        return {sensor.name: sensor.get() for sensor in sensors}

    def view_divs(self):
        divs = []
        sensors: List[Sensor] = self.sensors.values()
        for sensor in sensors:
            divs.append(
                Div(cls="col-md-6")(
                    Div(
                        cls="card shadow-lg p-4 mx-auto d-flex justify-content-center align-items-center"
                    )(
                        Div(
                            id=f"{sensor.name}-chart",
                            cls="chart",
                        )
                    )
                )
            )
        return divs

    def __generate_script(self, sensor: Sensor):
        data = [view.model_dump() for view in sensor.view_data]
        return f"""
        const {sensor.name}Source = (data) => {{
            const graphData = {json.dumps(data)};
            graphData[0].value = data.{sensor.name};
            const layout = {json.dumps(sensor.layout.model_dump())};
            Plotly.newPlot('{sensor.name}-chart', graphData, layout);
        }}
        """

    def view_script(self):
        sensors: List[Sensor] = self.sensors.values()
        chart_functions = [self.__generate_script(sensor) for sensor in sensors]
        chart_functions_name = [f"{sensor.name}Source(jsonData)" for sensor in sensors]
        chart_functions_call = "\n".join(chart_functions_name)
        script = f"""
            const source = new EventSource("/data-stream");
            {"\n".join(chart_functions)}
            source.onmessage = function(event) {{
            let data = event.data;
            const parser = new DOMParser();
            const decodedData = parser.parseFromString(data, "text/html").documentElement.textContent;
            const jsonData = JSON.parse(decodedData);
            {chart_functions_call}
            }};
            """
        return Script(script)


my_dashboard = Dashboard()
