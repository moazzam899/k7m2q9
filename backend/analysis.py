
from collections import defaultdict


def convert_actual_to_hourly(records):
    hourly_data = defaultdict(list)

    for record in records:
        hour = record["startTime"][:13] + ":00:00Z"
        hourly_data[hour].append(record["generation"])

    result = {}

    for hour, values in hourly_data.items():
        if len(values) == 2:
            result[hour] = sum(values) / 2

    return result


from datetime import datetime, timedelta, timezone


def select_day_ahead_forecasts(records, delivery_date):
    delivery_day = datetime.strptime(
        delivery_date, "%Y-%m-%d"
    ).replace(tzinfo=timezone.utc)

    # Assumed purchasing decision: previous day at 12:00 UTC
    decision_time = delivery_day - timedelta(hours=12)

    selected = {}

    for record in records:
        publish_time = datetime.fromisoformat(
            record["publishTime"].replace("Z", "+00:00")
        )

        delivery_time = datetime.fromisoformat(
            record["startTime"].replace("Z", "+00:00")
        )

        # Only forecasts for the requested delivery day
        if delivery_time.date() != delivery_day.date():
            continue

        # Ignore forecasts published after the purchasing decision
        if publish_time > decision_time:
            continue

        hour = record["startTime"]

        # Keep the latest forecast available before decision time
        if (
            hour not in selected
            or publish_time > selected[hour]["publish_datetime"]
        ):
            selected[hour] = {
                "forecast_mw": record["generation"],
                "publish_time": record["publishTime"],
                "publish_datetime": publish_time
            }

    return selected



import math


def calculate_accuracy(hourly_actual, selected_forecasts):
    comparisons = []

    for hour, actual_mw in sorted(hourly_actual.items()):
        if hour not in selected_forecasts:
            continue

        forecast_mw = selected_forecasts[hour]["forecast_mw"]
        error_mw = forecast_mw - actual_mw

        comparisons.append({
            "hour": hour,
            "actual_mw": actual_mw,
            "forecast_mw": forecast_mw,
            "error_mw": error_mw
        })

    if not comparisons:
        return {
            "mae": None,
            "rmse": None,
            "bias": None,
            "total_hours": 0,
            "comparisons": []
        }

    errors = [item["error_mw"] for item in comparisons]
    n = len(errors)

    mae = sum(abs(error) for error in errors) / n
    rmse = math.sqrt(sum(error ** 2 for error in errors) / n)
    bias = sum(errors) / n

    return {
        "mae": round(mae, 2),
        "rmse": round(rmse, 2),
        "bias": round(bias, 2),
        "total_hours": n,
        "comparisons": comparisons
    }



def calculate_monthly_accuracy(daily_results):
    all_comparisons = []

    for day in daily_results:
        all_comparisons.extend(day["comparisons"])

    if not all_comparisons:
        return {
            "mae": None,
            "rmse": None,
            "bias": None,
            "total_hours": 0
        }

    errors = [
        item["error_mw"]
        for item in all_comparisons
    ]

    n = len(errors)

    mae = sum(abs(error) for error in errors) / n
    rmse = math.sqrt(
        sum(error ** 2 for error in errors) / n
    )
    bias = sum(errors) / n

    return {
        "mae": round(mae, 2),
        "rmse": round(rmse, 2),
        "bias": round(bias, 2),
        "total_hours": n
    }
