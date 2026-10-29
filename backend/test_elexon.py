
import httpx

url = "https://data.elexon.co.uk/bmrs/api/v1/datasets/FUELHH"

params = {
    "settlementDateFrom": "2026-01-01",
    "settlementDateTo": "2026-01-01",
    "fuelType": "WIND"
}

response = httpx.get(url, params=params, timeout=30)

print("Status Code:", response.status_code)
print("Request URL:", response.url)


if response.status_code == 200:
    data = response.json()
    records = data["data"]

    print("Total WIND records:", len(records))

    for record in records[:3]:
        print(
            "Time:", record["startTime"],
            "| Generation:", record["generation"], "MW"
        )
else:
    print("Error:", response.text[:1000])
