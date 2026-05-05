# UrbanFlow — Urban Traffic Flow Modelling System

A computational model simulating real-world urban traffic flow
built in Python. Designed for use by Metro Councils globally
for traffic planning and road network analysis.

---

## What It Does

- Loads real road networks from any city in the world
- Lets you select a specific road to simulate
- Simulates bidirectional traffic with real vehicle classes
- Displays live metrics, charts and road visualisation
- Exports results as CSV or PDF report

---

## Vehicle Classification (Zimbabwe VED / MoT)

| Code | Class | Description |
|------|-------|-------------|
| M | Motorcycle | Bikes and scooters |
| L | Light Motor Vehicle | Cars, sedans, hatchbacks |
| MB | Minibus | Combis, emergency taxis |
| B | Bus | Large passenger buses |
| HGV | Heavy Goods Vehicle | Trucks and lorries |

---

## How To Run

### 1. Clone the repository
git clone https://github.com/zidlabheki-ui/urbanflow-traffic-sim.git
cd urbanflow-traffic-sim

### 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

### 3. Install dependencies
pip install numpy pandas matplotlib scipy customtkinter osmnx networkx requests

### 4. Run the application
python main.py

---

## How To Use

1. Enter a city name e.g. Bulawayo, Zimbabwe
2. Click Search City Roads
3. Search and select a specific road
4. Click Load Selected Road
5. Adjust parameters if needed
6. Click Run Simulation

---

## Built With

- Python 3.12
- CustomTkinter — modern UI framework
- OSMnx — real road network data from OpenStreetMap
- Matplotlib — live charts and graphs
- Pandas — data import and export
- NumPy — mathematical modelling
- NetworkX — road network graph analysis

---

## Project Context

Built as a Computational Modelling project demonstrating
real-world traffic flow simulation using the Nagel-Schreckenberg
cellular automaton model adapted for urban road networks.

---

## Author

Developed by Zidla Bhekumuzi
Year: 2026