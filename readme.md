# Sensor Dashboard

## Overview
This project is a **sensor dashboard** that visualizes real-time data using interactive charts. Each sensor's data is displayed in a card, ensuring a structured and responsive UI.

## Features
- 📊 **Dynamic Sensor Data Visualization**: Real-time updates for temperature, humidity, and other sensor metrics.
- 🌟 **Interactive UI**: You can add many sensors  and view their data in a structured layout.

## Installation

### Prerequisites
- Python 3.12+
- Docker (optional)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/BloodBoy21/sensorsDashboard.git
   cd sensorsDashboard
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```
4. Open in your browser:
   ```
   http://localhost:5001
   ```

## Docker
You can also run the application using Docker:
```bash
docker compose up
```


## Core Logic
The `view_divs` function generates the **sensor cards** dynamically (/lib/dashboard.py):
```python
def view_divs(self):
    divs = []
    sensors: List[Sensor] = self.sensors.values()
    for sensor in sensors:
        divs.append(
            Div(cls="col-md-6")(  # Ensures two cards per row
                Div(cls="card shadow-lg p-4 mx-auto")(  # Stylish shadow effect
                    Div(
                        id=f"{sensor.name}-chart",
                        cls="chart",
                    )
                )
            )
        )
    return divs
```

To add sensor and their data visualization using plotly at main.py:
```python
from lib.dashboard import my_dashboard
from lib.sensor import Sensor, View, Layout
list_of_sensors = [
    Sensor(
        "temperature",
        "Living Room",
        layout=Layout(
            title="Temperature sensor",
            width=400,
            height=400,
        ),
        view_data=[
            View(
                title="Temperature",
                type="indicator",
                mode="number+gauge",
                domain={"x": [0, 1], "y": [0, 1]},
            )
        ],
    ),
    Sensor(
        "humidity",
        "Living Room",
        layout=Layout( #card configuration
            title="Humidity sensor",
            width=400,
            height=400,
        ),
        view_data=[ #chart configuration
            View(
                title="Humidity",
                type="indicator",
                mode="number+gauge",
                domain={"x": [0, 1], "y": [0, 1]},
            )
        ],
    ),
    # Add more sensors here
]

my_dashboard.add_sensors(list_of_sensors)
```

## Contribution
Feel free to open **issues** or submit **pull requests** for improvements!

## License
MIT License. Use it freely for personal or commercial projects. 🚀

