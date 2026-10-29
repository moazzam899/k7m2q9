
import httpx
from collections import Counter

url = "https://data.elexon.co.uk/bmrs/api/v1/datasets/WINDFOR"

params = {
    "publishDateTimeFrom": "2025-12-31T00:00:00Z",
    "publishDateTimeTo": "2026-01-02T00:00:00Z"
}

response = httpx.get(url, params=params, timeout=30)

print("Status Code:", response.status_code)
print("Request URL:", response.url)

if response.status_code == 200:
    result = response.json()

    records = result["data"]

    print("Total records:", len(records))

    print("\nFirst 3 forecast records:")

    for record in records[:3]:
        print(
            "Published:", record["publishTime"],
            "| Delivery:", record["startTime"],
            "| Forecast:", record["generation"], "MW"
        )

    publication_counts = Counter(
        record["publishTime"] for record in records
    )

    print("\nUnique publication times:", len(publication_counts))
    print("First 5 publication batches:")

    for publish_time, count in sorted(publication_counts.items())[:5]:
        print(publish_time, "->", count, "records")

else:
    print("Error:", response.text[:1500])
