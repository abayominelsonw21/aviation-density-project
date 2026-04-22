# ✈️ Global Aviation Data Pipeline
**Real-Time Medallion Architecture with PySpark & Delta Lake**

An end-to-end, real-time ETL pipeline designed to ingest, process, and analyze global flight telemetry data. This project implements a strict **Medallion Architecture** (Bronze, Silver, Gold) using **PySpark** and **Delta Lake**, optimized for execution on Apple Silicon (M1).

### 🛠 Tech Stack
- **Data Engine:** Apache Spark (PySpark)
- **Storage Format:** Delta Lake (ACID transactions, Schema Enforcement)
- **Ingestion:** OpenSky Network REST API (OAuth2 Authenticated)
- **Interface:** Streamlit (Stealth Monochrome Dashboard)

### 🏗 Architecture Overview

This pipeline processes thousands of real-time flight vectors through three distinct data layers:

1. **🥉 Bronze Layer (Raw Ingestion):**
   - Ingests raw JSON payloads from the OpenSky API.
   - Casts all elements to generic String types to prevent upstream API changes from breaking the ingestion pipeline.
   - **Mode:** `Append`

2. **🥈 Silver Layer (Validated & Enforced):**
   - Applies strict Delta Lake schema enforcement.
   - Casts strings to optimal data types (Floats, Booleans).
   - Filters out grounded flights, missing coordinates, and erroneous velocities.
   - **Mode:** `Overwrite` (with Schema Evolution)

3. **🥇 Gold Layer (Business Aggregates):**
   - Calculates global flight density and performance metrics.
   - Aggregates average cruising altitude and velocity grouped by `origin_country`.
   - Surfaces data for the executive dashboard.
   - **Mode:** `Overwrite`

### 🚀 Key Engineering Features
- **Schema Evolution Protection:** Utilizes `.option("overwriteSchema", "true")` to safely manage downstream schema alterations without destroying historical data partitioning.
- **Hardware Optimized:** Custom Spark Session configurations designed to leverage Apple's Unified Memory, preventing JVM heartbeat timeouts during heavy local processing.
- **Stealth UI:** A dark-mode, high-contrast Streamlit dashboard that visualizes the Gold layer aggregates seamlessly.

### ⚙️ Quick Start

**1. Setup Environment Variables**
Create a `.env` file in the root directory with your OpenSky API credentials:
```env
OPENSKY_CLIENT_ID=your_client_id_here
OPENSKY_CLIENT_SECRET=your_client_secret_here
