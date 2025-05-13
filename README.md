
# 2D Boids Swarm Simulation (COMP4105 Project)

This project simulates swarm behavior in a 2D environment using the Boids algorithm, extended with predator avoidance, obstacle detection, manual leader control, and experiment automation.

---

## Setup Instructions (for New Machines)

### 1. Clone or Download the Repository
Ensure Python 3.8+ is installed.

```bash
git clone <your-repo-url>
cd 2D-Boids-Swarm-Simulation-COMP4105
```

### 2. Install Required Packages

```bash
pip install -r requirements.txt
```

requirements.txt:
```
pygame>=2.0
matplotlib
pandas
numpy
plotly
kaleido
```

---

## Project Structure

```
/boids
├── main.py                  # Run interactive simulation
├── boid.py                  # Defines individual boid behavior
├── environment.py           # Manages swarm, obstacles, predator logic
├── utils.py                 # Behavior calculations (separation, alignment, cohesion)
├── experiment_runner.py     # Automates experiments (30/60 boids, 3 behavior configs, predator on/off)
├── compare_experiments.py   # Aggregates & plots summary comparisons
├── plot_results.py          # Visualize specific runs with detailed plots
├── requirements.txt         # Dependencies
├── results/                 # Contains all CSV logs
```

---

## Running the Simulation

### 1. Interactive Boid Simulation

```bash
python main.py
```

Features:

- Press arrow keys to control the leader boid (highlighted in pink).
- Red predator moves autonomously and causes boids to flee.
- Boids avoid circular, square, and triangular obstacles.
- Screenshot auto-saved at key frames (see step logic inside main.py).

Modify simulation settings in environment.py:
```python
env = Environment(width, height, num_boids=30, with_predator=True)
```

---

### 2. Run Full Experiments (Automated)

```bash
python experiment_runner.py
```

- Runs 12 simulations: 2 densities × 3 behavior configs × 2 predator states.
- Output CSV logs saved in results/, e.g.,:
  30b_sep1.0_ali1.0_coh1.0_pred.csv

---

### 3. Compare All Experiments Visually

```bash
python compare_experiments.py
```

- Generates summary bar charts for:
  - Avg Distance to Center (group cohesion)
  - Collision Counts
- Automatically grouped by config.

---

### 4. Plot Any Individual Simulation

```bash
python plot_results.py
```

Choose a file like:
- simulation_log_30b_sep1.0_ali1.0_coh1.0_pred.csv
- Interactive time-series plots of average cohesion & collisions.

---

## Features Implemented

- Boid Rules: Separation, Alignment, Cohesion
- Obstacle Avoidance (circle, square, triangle)
- Manual Leader Control
- Predator Avoidance (100px range)
- Experiment automation across multiple configs
- Plotting tools for summary and focused analysis


