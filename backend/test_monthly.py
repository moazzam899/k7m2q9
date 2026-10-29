
from datetime import date, timedelta

from elexon_service import (
    get_actual_wind,
    get_wind_forecasts
)

from analysis import (
    convert_actual_to_hourly,
    select_day_ahead_forecasts,
    calculate_accuracy,
    calculate_monthly_accuracy
)

daily_results = []

start_date = date(2026, 1, 1)

# Analyze all 31 days of January 2026
for day_number in range(31):
    current_date = start_date + timedelta(days=day_number)
    date_string = current_date.isoformat()

    print(f"\nAnalyzing {date_string}...")

    actual_records = get_actual_wind(date_string)
    hourly_actual = convert_actual_to_hourly(actual_records)

    forecast_start = (
        current_date - timedelta(days=2)
    ).isoformat() + "T00:00:00Z"

    forecast_end = (
        current_date + timedelta(days=1)
    ).isoformat() + "T00:00:00Z"

    forecast_records = get_wind_forecasts(
        forecast_start,
        forecast_end
    )

    selected_forecasts = select_day_ahead_forecasts(
        forecast_records,
        date_string
    )

    results = calculate_accuracy(
        hourly_actual,
        selected_forecasts
    )

    daily_results.append(results)

    print("Compared hours:", results["total_hours"])
    print("Daily MAE:", results["mae"], "MW")

monthly = calculate_monthly_accuracy(daily_results)

print("\n--- Combined Results ---")
print("Total compared hours:", monthly["total_hours"])
print("MAE:", monthly["mae"], "MW")
print("RMSE:", monthly["rmse"], "MW")
print("Bias:", monthly["bias"], "MW")
