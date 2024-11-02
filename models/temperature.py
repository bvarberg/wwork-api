from enum import StrEnum
from pydantic import BaseModel


class TemperatureUnit(StrEnum):
    Celsius = "Celsius"
    Fahrenheit = "Fahrenheit"


class Temperature(BaseModel):
    value: float
    unit: TemperatureUnit = TemperatureUnit.Fahrenheit


class RequestBodyEMC(BaseModel):
    temperature: Temperature
    relative_humidity: float
