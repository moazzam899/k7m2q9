
from fastapi import FastAPI, HTTPException
from datetime import date

from elexon_service import get_actual_wind, get_wind_forecasts

from datetime import timedelta

from analysis import (
    convert_actual_to_hourly,
    select_day_ahead_forecasts,
    calculate_accuracy
)

app = FastAPI(
    title="WindSight API",
    description="UK Wind Power Forecast Intelligence",
    version="1.0.0"
)


@app.get("/")
def home():
    return {"message": "WindSight API is running!"}


@app.get("/api/health")
def health_check():
    return {
        "status": "success",
        "message": "Backend is healthy"
    }


@app.get("/api/wind/actual")
def actual_wind(date: date):
    try:
        records = get_actual_wind(date.isoformat())

        return {
            "date": date.isoformat(),
            "total_records": len(records),
            "data": records
        }

    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail="Unable to fetch actual wind generation data"
        ) from error



@app.get("/api/wind/forecast")
def wind_forecast():
    try:
        records = get_wind_forecasts(
            "2025-12-31T00:00:00Z",
            "2026-01-02T00:00:00Z"
        )

        return {
            "total_records": len(records),
            "data": records
        }

    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail="Unable to fetch wind forecast data"
        ) from error



@app.get("/api/wind/analysis")
def wind_analysis(date: date):
    try:
        delivery_date = date.isoformat()

        actual_records = get_actual_wind(delivery_date)
        hourly_actual = convert_actual_to_hourly(actual_records)

        forecast_start = (
            date - timedelta(days=2)
        ).isoformat() + "T00:00:00Z"

        forecast_end = (
            date + timedelta(days=1)
        ).isoformat() + "T00:00:00Z"

        forecast_records = get_wind_forecasts(
            forecast_start,
            forecast_end
        )

        selected_forecasts = select_day_ahead_forecasts(
            forecast_records,
            delivery_date
        )

        results = calculate_accuracy(
            hourly_actual,
            selected_forecasts
        )

        return {
            "date": delivery_date,
            "metrics": {
                "mae": results["mae"],
                "rmse": results["rmse"],
                "bias": results["bias"],
                "total_hours": results["total_hours"]
            },
            "comparisons": results["comparisons"]
        }

    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail="Unable to calculate wind forecast accuracy"
        ) from error
