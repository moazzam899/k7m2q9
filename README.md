# WindSight — Wind Power Forecast Intelligence

**An interactive analytics dashboard for evaluating day-ahead wind power forecasts against actual wind generation in Great Britain.**

WindSight analyzes historical wind generation and forecast data from the Elexon API to measure forecast accuracy, identify prediction errors, and present actionable insights for energy trading and operational planning.

## Live Demo

- **Dashboard:** https://windsight-dashboard.vercel.app/
- **Backend API:** https://windsight-api-l5nx.onrender.com/
- **API Documentation:** https://windsight-api-l5nx.onrender.com/docs

## Project Overview

Wind power generation is variable and weather-dependent. Accurate forecasting helps energy market participants plan electricity purchases, manage imbalance exposure, and make better operational decisions.

WindSight provides an interactive dashboard that compares actual wind generation with day-ahead forecasts and summarizes forecast performance using standard statistical metrics.

The current analysis covers January 2026, containing 31 days and 744 hourly comparisons.

## Key Features

- **Forecast vs Actual:** Compare hourly actual wind generation against day-ahead forecasts.
- **Performance Metrics:** Calculate Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and forecast Bias.
- **Daily Error Analysis:** Visualize daily forecast errors.
- **Business Insights:** Highlight systematic forecast bias and potential implications for purchasing and risk management.
- **Risk Indicators:** Categorize daily forecast errors into illustrative Low, Moderate, and High risk levels.
- **Interactive Dashboard:** Explore forecast performance through charts and KPI cards.
- **REST API:** Retrieve processed wind generation and forecast analysis through FastAPI.
- **Docker Support:** Containerized backend for consistent deployment.

## Technology Stack

### Frontend
- React.js
- Vite
- Recharts
- Lucide React
- CSS

### Backend
- Python 3.12
- FastAPI
- HTTPX
- Elexon API

### Deployment & Tools
- Docker
- Render
- Vercel
- Git and GitHub

## Data Sources

WindSight uses publicly available data from the Elexon API.

| Dataset | Description |
|---|---|
| FUELHH | Half-hourly actual electricity generation by fuel type |
| WINDFOR | Wind generation forecast data, including publication timestamps |

**API Base URL:** https://data.elexon.co.uk/bmrs/api/v1

## Forecast Analysis Methodology

The January 2026 analysis follows these steps:

1. Retrieve actual wind generation data from the Elexon FUELHH dataset.
2. Retrieve wind forecast data from the WINDFOR dataset.
3. Convert half-hourly actual generation readings into hourly averages.
4. Apply a day-ahead forecast selection methodology.
5. For each delivery hour, select the latest forecast published before the previous day's 12:00 UTC decision cutoff.
6. Match hourly forecasts with corresponding actual generation values.
7. Calculate forecast accuracy metrics across all valid hourly comparisons.

**Decision Cutoff Assumption:** The previous-day 12:00 UTC cutoff is an analytical assumption used to simulate a day-ahead decision process. It is documented to avoid using forecasts published after the assumed decision time.

### Performance Metrics

**Mean Absolute Error (MAE)**

Measures the average absolute difference between forecast and actual generation.

MAE = Mean(|Forecast − Actual|)

**Root Mean Squared Error (RMSE)**

Measures the square root of the average squared forecast error, giving larger errors greater weight.

RMSE = √Mean((Forecast − Actual)²)

**Forecast Bias**

Measures the average signed forecast error.

Bias = Mean(Forecast − Actual)

A positive bias indicates overforecasting, while a negative bias indicates underforecasting.

## January 2026 Results

The analysis produced the following results:

| Metric | Result |
|---|---:|
| Analysis Period | January 2026 |
| Days Analyzed | 31 |
| Hourly Comparisons | 744 |
| MAE | 2,017.92 MW |
| RMSE | 2,477.04 MW |
| Bias | +1,806.23 MW |

### Key Observations

- The positive forecast bias indicates systematic overforecasting during the analyzed period.
- MAE summarizes the typical absolute forecast error.
- RMSE highlights the impact of larger forecast deviations.
- These results can help identify periods that may require additional attention in energy purchasing and imbalance risk management.

## Business Insights

WindSight translates statistical results into business-oriented observations:

- **Forecast Bias:** Identifies systematic overforecasting or underforecasting.
- **Purchasing Decisions:** Helps highlight forecast deviations that may affect electricity purchasing decisions.
- **Risk Management:** Highlights days with larger forecast errors for closer operational attention.

The dashboard's Low, Moderate, and High risk categories use illustrative MAE thresholds. They are not financial loss estimates or official market risk classifications.

## Project Structure

```text
wind-power-analytics/
│
├── backend/
│   ├── data/
│   │   └── january_2026.json
│   ├── main.py
│   ├── elexon_service.py
│   ├── analysis.py
│   ├── monthly_service.py
│   ├── generate_snapshot.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── index.css
│   ├── package.json
│   └── index.html
│
└── README.md
```

## Running Locally

### Prerequisites

- Node.js and npm
- Python 3.12+
- Git

### 1. Clone the repository

```bash
git clone https://github.com/moazzam899/k7m2q9.git
cd k7m2q9
```

### 2. Start the Backend

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment.

**Windows:**

```powershell
.venv\Scripts\activate
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start FastAPI:

```bash
uvicorn main:app --reload --port 8000
```

Backend runs at:

http://localhost:8000

API documentation:

http://localhost:8000/docs

### 3. Start the Frontend

Open another terminal:

```bash
cd frontend
npm install
```

Create a `.env` file inside the frontend directory:

```env
VITE_API_URL=http://localhost:8000
```

Start the development server:

```bash
npm run dev
```

Frontend runs at:

http://localhost:5173

## Docker Deployment

The backend includes a Dockerfile.

From the repository root, build the Docker image:

```bash
docker build --load -t windsight-backend ./backend
```

Run the container:

```bash
docker run -d --name windSight-api -p 8001:8000 windsight-backend
```

Verify the backend:

http://localhost:8001/

## Deployment Architecture

| Component | Platform |
|---|---|
| Frontend | Vercel |
| Backend | Render |
| Data Source | Elexon API |
| Containerization | Docker |
| Repository | GitHub |

The frontend communicates with the deployed FastAPI backend through the `VITE_API_URL` environment variable.

## Limitations and Future Improvements

- The current dashboard focuses on January 2026.
- The analysis uses a documented assumed day-ahead decision cutoff.
- Risk categories are illustrative and can be refined using market-specific thresholds.
- Future improvements could include additional months, longer-term forecast accuracy trends, weather data integration, and more detailed imbalance cost analysis.

## AI Assistance Disclosure

AI tools were used as development assistance during parts of this project, including guidance on implementation, debugging, and documentation. The project architecture, data processing workflow, integration, testing, and deployment were developed and validated as part of the implementation process.

## Author

**Moazzam Abbasi**

- GitHub: https://github.com/moazzam899

---

*WindSight — Turning wind forecast data into actionable intelligence.*