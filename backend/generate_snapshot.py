
import json
from pathlib import Path

from monthly_service import get_monthly_analysis

OUTPUT_FILE = Path(__file__).resolve().parent / "data" / "january_2026.json"

def main():
    print("Generating January 2026 analysis snapshot...")

    result = get_monthly_analysis(2026, 1)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(result, file, indent=2)

    print(f"Snapshot saved: {OUTPUT_FILE}")
    print(f"Hours analyzed: {result['metrics']['total_hours']}")
    print(f"MAE: {result['metrics']['mae']} MW")

if __name__ == "__main__":
    main()
