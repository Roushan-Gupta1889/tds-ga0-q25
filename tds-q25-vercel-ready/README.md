# TDS GA0 Q25 — Vercel POST Analytics Endpoint

This project implements the assignment API using FastAPI and the supplied 36-record telemetry dataset.

## Files

- `app.py` — FastAPI app, POST endpoint, metrics, and CORS middleware.
- `telemetry_data.py` — supplied sample telemetry data bundled as a Python constant.
- `requirements.txt` — FastAPI dependency.

## Deploy with the GitHub web interface

1. Extract the ZIP locally.
2. Create a **new public GitHub repository**.
3. Upload `app.py`, `telemetry_data.py`, and `requirements.txt` to the repository root (do not upload the ZIP as a single file).
4. Open Vercel and sign in with GitHub.
5. Select **Add New → Project**, import the repository, and deploy. Vercel currently supports zero-configuration FastAPI apps; this project intentionally uses root-level `app.py` and does not need a `vercel.json` routing file.
6. Open the deployed site's base URL. A GET request should return a small health message.
7. In the GA0 Q25 answer field, enter the deployed base URL including `https://` (for example, `https://YOUR-PROJECT.vercel.app/`). Do not submit a made-up or example hostname; use the actual URL Vercel gives your deployment.

## Test request

Send a `POST` request to the deployed base URL with JSON:

```json
{"regions":["apac","emea"],"threshold_ms":178}
```

Expected response (floating-point values may display with slightly different last digits):

```json
{
  "apac": {
    "avg_latency": 157.90916666666666,
    "p95_latency": 204.2215,
    "avg_uptime": 98.456,
    "breaches": 3
  },
  "emea": {
    "avg_latency": 168.57,
    "p95_latency": 229.51999999999998,
    "avg_uptime": 98.32958333333333,
    "breaches": 4
  }
}
```

`p95_latency` uses linear interpolation between the adjacent sorted values. `breaches` counts rows where `latency_ms > threshold_ms` (strictly greater than the threshold).

## Learning goals

- Parse and validate a JSON POST body with Pydantic.
- Group records by region.
- Calculate mean, interpolated 95th percentile, and threshold breach count.
- Enable cross-origin POST/preflight requests using CORS middleware.
- Deploy a Python API using Vercel's FastAPI runtime.
