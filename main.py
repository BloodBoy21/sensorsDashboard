from fasthtml.common import *
from lib.mqtt import init_mqtt
from asyncio import sleep
import json
from lib.sensors import my_dashboard

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
        Div(id="temperature-chart", cls="chart"),
        Script(
            """
            var source = new EventSource("/temperature-stream");
            source.onmessage = function(event) {
                let data = event.data;
                const parser = new DOMParser();
            const decodedData = parser.parseFromString(data, "text/html").documentElement.textContent;
            const jsonData = JSON.parse(decodedData);
            const graphData = [{
                    domain: {x: [0, 1], y: [0, 1]},
                    value: jsonData.temperature,
                    title: {text: "Temperature"},
                    type: "indicator",
                    mode: "number+gauge"
                }];
            const layout = {
                "title": "Temperature sensor",
                "width": 400,
                "height": 400,
            }
                Plotly.newPlot('temperature-chart', graphData);
            };
            """
        ),
    )


# SSE data stream for temperature updates
async def temperature_stream():
    while not shutdown_event.is_set():
        sensors_data = my_dashboard.read_all()
        yield sse_message(json.dumps(sensors_data))
        await sleep(1)  # Update every second


@rt("/temperature-stream")
async def get():
    return EventStream(temperature_stream())


serve()
