import subprocess
from typing import Annotated
from fastapi import FastAPI, Body, HTTPException

from models.temperature import Climate, TemperatureUnit

app = FastAPI(
    title="wwork-api",
    version="0.1.0",
)


@app.get("/")
def root():
    return {"name": "wwork-api", "version": "0.1.0"}


@app.post("/emc")
def calculate_emc(
    body: Annotated[
        Climate,
        Body(
            openapi_examples={
                "fahrenheit": {
                    "summary": "Fahrenheit",
                    "value": {
                        "temperature": {"value": 70.0, "unit": "Fahrenheit"},
                        "relative_humidity": 0.35,
                    },
                },
                "celsius": {
                    "summary": "Celsius",
                    "value": {
                        "temperature": {"value": 21.1, "unit": "Celsius"},
                        "relative_humidity": 0.35,
                    },
                },
            }
        ),
    ]
):
    try:
        t = str(body.temperature.value)
        rh = str(body.relative_humidity)
        celsius = body.temperature.unit == TemperatureUnit.Celsius

        cmd = ["./wwork", "emc", t, rh]
        if celsius:
            cmd.append("--celsius")
        result = subprocess.run(
            cmd,
            capture_output=True,
            check=True,
        )
        emc = float(result.stdout.decode("utf-8"))
        return {"emc": emc}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="wwork failed")
