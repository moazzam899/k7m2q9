import { useEffect, useState } from "react";

import {
  Wind,
  LayoutDashboard,
  Activity,
  CalendarDays,
  TrendingUp,
  TrendingDown,
  Clock3,
} from "lucide-react";

import "./App.css";

import {
  ResponsiveContainer,
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";




function App() {


const [monthlyData, setMonthlyData] = useState(null);
const [loading, setLoading] = useState(true);
const [error, setError] = useState("");

const [selectedDate, setSelectedDate] = useState("2026-01-01");

useEffect(() => {
  async function fetchMonthlyData() {
    try {
      const response = await fetch(
        "http://localhost:8000/api/wind/monthly"
      );

      if (!response.ok) {
        throw new Error("Failed to fetch monthly analysis");
      }

      const data = await response.json();

      setMonthlyData(data);
      console.log("WindSight Monthly API:", data);
    } catch (err) {
      setError(err.message);
      console.error("API Error:", err);
    } finally {
      setLoading(false);
    }
  }

  fetchMonthlyData();
}, []);



const metrics = [
  {
    title: "Mean Absolute Error",
    value: monthlyData?.metrics?.mae?.toLocaleString() ?? "—",
    unit: "MW",
    icon: Activity,
    description: "Average absolute forecast deviation",
  },
  {
    title: "Root Mean Square Error",
    value: monthlyData?.metrics?.rmse?.toLocaleString() ?? "—",
    unit: "MW",
    icon: TrendingUp,
    description: "Higher penalty for large errors",
  },
  {
    title: "Forecast Bias",
    value:
      monthlyData?.metrics?.bias != null
        ? `${monthlyData.metrics.bias > 0 ? "+" : ""}${monthlyData.metrics.bias.toLocaleString()}`
        : "—",
    unit: "MW",
    icon: TrendingDown,
    description: "Positive indicates over-forecasting",
  },
  {
    title: "Hours Analyzed",
    value: monthlyData?.metrics?.total_hours?.toLocaleString() ?? "—",
    unit: "hours",
    icon: Clock3,
    description: "January 1–31, 2026",
  },
];


const dailyErrorData = (monthlyData?.daily_results ?? []).map((day) => ({
  day: day.date.slice(8, 10),
  mae: day.mae,
}));



const selectedDay = monthlyData?.daily_results?.find(
  (day) => day.date === selectedDate
);

const hourlyChartData = (selectedDay?.comparisons ?? []).map((item) => ({
  hour: item.hour.slice(11, 16),
  actual: item.actual_mw,
  forecast: item.forecast_mw,
}));



  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">
            <Wind size={25} />
          </div>
          <div>
            <h2>WindSight</h2>
            <span>ENERGY INTELLIGENCE</span>
          </div>
        </div>

        <div className="sidebar-label">WORKSPACE</div>

        <nav className="navigation">
          <a href="#overview" className="nav-item active">
            <LayoutDashboard size={19} />
            Overview
          </a>

          <a href="#performance" className="nav-item">
            <Activity size={19} />
            Forecast Performance
          </a>
        </nav>

        <div className="sidebar-bottom">
          <span className="status-dot" />
          Elexon BMRS Data
        </div>
      </aside>

      <main className="main-content" id="overview">
        <header className="topbar">
          <div className="breadcrumb">
            Workspace <span>/</span> Overview
          </div>
          <div className="topbar-right">
            <span className="data-source">UK Wind Generation</span>
          </div>
        </header>

        <div className="dashboard-content">
          <div className="page-heading">
            <div>
              <div className="eyebrow">
                <span className="status-dot" />
                HISTORICAL MARKET ANALYSIS
              </div>
              <h1>Wind Forecast Overview</h1>
              <p>
                Day-ahead forecast accuracy and generation
                performance for UK wind energy.
              </p>
            </div>

            <div className="date-filter">
              <CalendarDays size={18} />
              January 2026
            </div>
          </div>

          
          {loading && <p>Loading January 2026 analysis...</p>}

{error && (
  <p style={{ color: "#dc3545" }}>
    Unable to load analysis: {error}
  </p>
)}

          <div className="metrics-grid">
            {metrics.map((metric) => {
              const Icon = metric.icon;

              return (
                <div className="metric-card" key={metric.title}>
                  <div className="metric-top">
                    <span>{metric.title}</span>
                    <div className="metric-icon">
                      <Icon size={19} />
                    </div>
                  </div>

                  <div className="metric-value">
                    {metric.value}
                    <span>{metric.unit}</span>
                  </div>

                  <p>{metric.description}</p>
                </div>
              );
            })}
          </div>

          <section className="chart-card" id="performance">
            <div className="section-heading">
              <div>
                <h3>Actual vs Forecast Generation</h3>
                <p>Hourly wind generation comparison</p>
              </div>
              
<div className="chart-controls">
  <select
    className="day-selector"
    value={selectedDate}
    onChange={(e) => setSelectedDate(e.target.value)}
  >
    {(monthlyData?.daily_results ?? []).map((day) => (
      <option key={day.date} value={day.date}>
        {new Date(`${day.date}T12:00:00Z`).toLocaleDateString("en-GB", {
          day: "numeric",
          month: "short",
          year: "numeric",
          timeZone: "UTC",
        })}
      </option>
    ))}
  </select>

  <span className="section-tag">MW</span>
</div>

            </div>

            
<div className="generation-chart">
  <ResponsiveContainer width="100%" height={320}>
    <LineChart
      data={hourlyChartData}
      margin={{ top: 15, right: 20, left: 0, bottom: 5 }}
    >
      <CartesianGrid stroke="#edf1f5" strokeDasharray="4 4" />

      <XAxis
        dataKey="hour"
        tick={{ fontSize: 11, fill: "#8291a3" }}
        tickLine={false}
        axisLine={false}
      />

      <YAxis
        tick={{ fontSize: 11, fill: "#8291a3" }}
        tickLine={false}
        axisLine={false}
        tickFormatter={(value) => `${(value / 1000).toFixed(0)}k`}
      />

      <Tooltip
        formatter={(value, name) => [
          `${Number(value).toLocaleString()} MW`,
          name,
        ]}
      />

      <Legend verticalAlign="top" height={36} />

      <Line
        type="monotone"
        dataKey="actual"
        name="Actual Generation"
        stroke="#159e84"
        strokeWidth={3}
        dot={false}
        activeDot={{ r: 5 }}
      />

      <Line
        type="monotone"
        dataKey="forecast"
        name="Forecast Generation"
        stroke="#5176e8"
        strokeWidth={3}
        dot={false}
        activeDot={{ r: 5 }}
      />
    </LineChart>
  </ResponsiveContainer>
</div>

          </section>

          <section className="chart-card">
            <div className="section-heading">
              <div>
                <h3>Daily Forecast Error</h3>
                <p>Daily mean absolute error throughout January</p>
              </div>
              <span className="section-tag">MAE</span>
            </div>

            
<div className="generation-chart">
  <ResponsiveContainer width="100%" height={280}>
    <BarChart
      data={dailyErrorData}
      margin={{ top: 15, right: 15, left: 0, bottom: 5 }}
    >
      <CartesianGrid
        stroke="#edf1f5"
        strokeDasharray="4 4"
        vertical={false}
      />

      <XAxis
        dataKey="day"
        tick={{ fontSize: 10, fill: "#8291a3" }}
        tickLine={false}
        axisLine={false}
        interval={2}
      />

      <YAxis
        tick={{ fontSize: 11, fill: "#8291a3" }}
        tickLine={false}
        axisLine={false}
        tickFormatter={(value) => `${(value / 1000).toFixed(0)}k`}
      />

      <Tooltip
        formatter={(value) => [
          `${Number(value).toLocaleString()} MW`,
          "Daily MAE",
        ]}
        labelFormatter={(day) => `January ${day}, 2026`}
      />

      <Bar
        dataKey="mae"
        name="Daily MAE"
        fill="#20aa91"
        radius={[4, 4, 0, 0]}
        maxBarSize={28}
      />
    </BarChart>
  </ResponsiveContainer>
</div>

          </section>

          <footer className="footer">
            WindSight · Powered by Elexon BMRS · January 2026
          </footer>
        </div>
      </main>
    </div>
  );
}

export default App;
