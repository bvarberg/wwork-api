import subprocess
from fastapi import FastAPI

from models.temperature import RequestBodyEMC, TemperatureUnit

app = FastAPI()


@app.get("/")
def root():
    return {"name": "wwork-api", "version": "0.1.0"}


@app.post("/emc")
def calculate_emc(body: RequestBodyEMC):
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
        return {"error": "executing wwork failed"}
