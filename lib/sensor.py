from pydantic import BaseModel
from typing import List, Optional, Dict


class View(BaseModel):
    title: str = ""
    value: float = 0
    type: Optional[str] = "indicator"
    mode: Optional[str] = ""
    domain: Optional[Dict[str, List[int]]] = {"x": [0, 1], "y": [0, 1]}


class Layout(BaseModel):
    title: str = ""
    width: int = 400
    height: int = 400


class Sensor:
    def __init__(
        self,
        name: str,
        location: str,
        layout: Layout = Layout(),
        view_data: List[View] = [View()],
    ):
        self.name = name
        self.location = location
        self.value = 0
        self.layout = layout
        self.view_data = view_data

    def update(self, value: float):
        self.value = value

    def get(self) -> float:
        return self.value
