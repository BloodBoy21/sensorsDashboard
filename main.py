from fasthtml.common import (
    Titled,
    P,
    Script,
    Link,
    Meta,
    EventStream,
    serve,
    sse_message,
    fast_app,
    signal_shutdown,
    Div,
)
from lib.mqtt import init_mqtt
from asyncio import sleep
import json
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
        layout=Layout(
            title="Humidity sensor",
            width=400,
            height=400,
        ),
        view_data=[
            View(
                title="Humidity",
                type="indicator",
                mode="number+gauge",
                domain={"x": [0, 1], "y": [0, 1]},
            )
        ],
    ),
]

my_dashboard.add_sensors(list_of_sensors)


favicons = (
    Link(
        rel="icon",
        type="image/png",
        href="/static/favicon/favicon-96x96.png",
        sizes="96x96",
    ),
    Link(rel="icon", type="image/svg+xml", href="/static/favicon/favicon.svg"),
    Link(rel="shortcut icon", href="/static/favicon/favicon.ico"),
    Link(
        rel="apple-touch-icon",
        sizes="180x180",
        href="/static/favicon/apple-touch-icon.png",
    ),
    Meta(name="apple-mobile-web-app-title", content="MySensors"),
    Link(rel="manifest", href="/static/favicon/site.webmanifest"),
)


cdn_scripts = (
    Script(src="https://cdn.plot.ly/plotly-2.32.0.min.js"),
    Link(rel="stylesheet", href="/static/style.css"),
    Link(
        rel="stylesheet",
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css",
    ),
    *favicons,
)

app, rt = fast_app(
    hdrs=cdn_scripts,
    on_startup=[init_mqtt],
)

shutdown_event = signal_shutdown()


@rt("/")
def get():
    return Titled(
        "My sensors",
        P("Watch real time sensor update", cls="text-body-secondary"),
        Div(cls="container my-2")(Div(cls="row g-4")(*my_dashboard.view_divs())),
        my_dashboard.view_script(),
    )


async def data_stream():
    while not shutdown_event.is_set():
        sensors_data = my_dashboard.read_all()
        yield sse_message(json.dumps(sensors_data))
        await sleep(10)  # Update every 10 second


@rt("/data-stream")
async def get():
    return EventStream(data_stream())


serve()
