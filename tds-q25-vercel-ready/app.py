"""TDS GA0 Q25: Vercel POST analytics endpoint."""
from statistics import mean
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from telemetry_data import RECORDS

app = FastAPI(title="eShopCo Regional Analytics API", version="1.0.0")

# Allow the assignment grader (and other browser clients) to POST from any origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)


class AnalyticsRequest(BaseModel):
    regions: list[str] = Field(min_length=1)
    threshold_ms: float


def percentile_linear(values: list[float], percentile: float) -> float:
    """Calculate a percentile using linear interpolation (NumPy default method)."""
    if not values:
        raise ValueError("Cannot calculate a percentile without values")
    ordered = sorted(float(value) for value in values)
    position = (len(ordered) - 1) * percentile / 100.0
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = position - lower
    return ordered[lower] + (ordered[upper] - ordered[lower]) * fraction


@app.get("/")
def health() -> dict[str, Any]:
    return {"message": "eShopCo analytics endpoint is ready", "method": "POST"}


@app.post("/")
def analytics(payload: AnalyticsRequest) -> dict[str, dict[str, float | int]]:
    """Return metrics for each requested region."""
    response: dict[str, dict[str, float | int]] = {}

    # Normalize region labels but retain predictable lowercase response keys.
    for raw_region in payload.regions:
        region = raw_region.strip().lower()
        if not region:
            raise HTTPException(status_code=422, detail="Region names cannot be empty")

        rows = [row for row in RECORDS if str(row["region"]).lower() == region]
        if not rows:
            raise HTTPException(
                status_code=422,
                detail=f"No telemetry records found for region '{raw_region}'",
            )

        latencies = [float(row["latency_ms"]) for row in rows]
        uptimes = [float(row["uptime_pct"]) for row in rows]
        response[region] = {
            "avg_latency": mean(latencies),
            "p95_latency": percentile_linear(latencies, 95),
            "avg_uptime": mean(uptimes),
            "breaches": sum(value > payload.threshold_ms for value in latencies),
        }

    return response
