
from datetime import date, timedelta
from functools import lru_cache

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


@lru_cache(maxsize=12)
def get_monthly_analysis(year=2026, month=1):
    start_date = date(year, month, 1)

    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)

    total_days = (next_month - start_date).days
    daily_results = []

    for day_number in range(total_days):
        current_date = start_date + timedelta(days=day_number)
        date_string = current_date.isoformat()

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

        result = calculate_accuracy(
            hourly_actual,
            selected_forecasts
        )

        daily_results.append({
            "date": date_string,
            **result
        })

    monthly_metrics = calculate_monthly_accuracy(daily_results)

    return {
        "year": year,
        "month": month,
        "metrics": monthly_metrics,
        "daily_results": daily_results
    }
