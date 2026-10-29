
from elexon_service import get_actual_wind, get_wind_forecasts
from analysis import (
    convert_actual_to_hourly,
    select_day_ahead_forecasts,
    calculate_accuracy
)

delivery_date = "2026-01-01"

# Actual wind generation
actual_records = get_actual_wind(delivery_date)
hourly_actual = convert_actual_to_hourly(actual_records)

# Historical forecasts published before the delivery day
forecast_records = get_wind_forecasts(
    "2025-12-30T00:00:00Z",
    "2026-01-01T00:00:00Z"
)

selected_forecasts = select_day_ahead_forecasts(
    forecast_records,
    delivery_date
)

print("Hourly actual records:", len(hourly_actual))
print("Historical forecast records:", len(forecast_records))
print("Selected day-ahead forecasts:", len(selected_forecasts))

print("\nFirst 5 selected forecasts:")

for hour, forecast in sorted(selected_forecasts.items())[:5]:
    print(
        "Delivery:", hour,
        "| Forecast:", forecast["forecast_mw"], "MW",
        "| Published:", forecast["publish_time"]
    )


results = calculate_accuracy(
    hourly_actual,
    selected_forecasts
)

print("\n--- Forecast Accuracy ---")
print("Compared hours:", results["total_hours"])
print("MAE:", results["mae"], "MW")
print("RMSE:", results["rmse"], "MW")
print("Bias:", results["bias"], "MW")