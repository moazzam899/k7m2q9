
import httpx

BASE_URL = "https://data.elexon.co.uk/bmrs/api/v1/datasets"


def get_actual_wind(date):
    url = f"{BASE_URL}/FUELHH"

    params = {
        "settlementDateFrom": date,
        "settlementDateTo": date,
        "fuelType": "WIND"
    }

    response = httpx.get(url, params=params, timeout=30)
    response.raise_for_status()

    return response.json()["data"]


def get_wind_forecasts(start_date, end_date):
    url = f"{BASE_URL}/WINDFOR"

    params = {
        "publishDateTimeFrom": start_date,
        "publishDateTimeTo": end_date
    }

    response = httpx.get(url, params=params, timeout=30)
    response.raise_for_status()

    return response.json()["data"]
