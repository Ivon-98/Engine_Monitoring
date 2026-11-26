# Engine Monitoring

Personal project **under development**: an interface that simulates real-time engine monitoring, using the NASA C-MAPSS dataset.

## Description

The app reads a engine's data cycle by cycle and plots it as if it were live sensor readings. It lets you choose which sensors to visualize (up to 4 at a time) and displays the engine's operating settings along with its status/RUL (Remaining Useful Life).


## Data

The project uses the **NASA Turbofan Engine Degradation Simulation (C-MAPSS)** dataset, with subsets FD001–FD004. Processed files live in `data/processed/`. A detailed description of the dataset and its variables (sensors, settings, degradation) is included in the PDF:

- `data/processed/Damage Propagation Modeling.pdf`

## Goal

The purpose of the project is to connect this interface to Machine Learning models for:

- **Real-time status monitoring** of the engine.
- **Remaining Useful Life (RUL) prediction** / remaining life cycles.

Currently the interface only visualizes historical data; the predictive model integration is still pending.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
cd app
python app.py
```

The app runs at `http://localhost:8080`.

## Project status

🚧 Actively under development. Next steps:


