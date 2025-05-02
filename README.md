# 🍺 DrunkardWalk

This is a study repository for the classical, one-dimensional *random walk*, commonly known as the *drunkard's walk*. It's structured following OOP orientations and python module formatting. 

## Features

- Simulate a single random walker (drunkard) on a one-dimensional sidewalk;
- Run multiple simulations (walkers) in parallel to analyze ensemble behavior;
- Calculate and plot:
  - The path of a single walker;
  - The average position of a single walk;
  - The standard deviation (dispersion) of a single walk;
  - The average position across multiple walkers;
  - The standard deviation across multiple walkers.

---

## Structure

### Classes

- `Drunkard`: Represents a walker who moves left or right based on a coin flip.
- `Sidewalk`: Environment for a single walker. Contains logic for walking and plotting.
- `City`: Simulates many walkers on their own sidewalks. Serves as basis for calculating ensemble statistics.

---

## 📈 Example Outputs

The simulation generates `.png` graphs such as:
- `RandomWalkVolatility_...png`: Standard deviation of a single walk.
- `AvgPos_...png`: Average position of multiple walkers over time.
- `Disp_...png`: Dispersion (standard deviation) of positions among all walkers.

---

## Installation

The requirements will be automatically installed via ``pip``.

### Method 1

```bash
pip install git+https://github.com/OffworldAstronaut/DrunkardWalk.git
```

### Method 2

```bash
git clone https://github.com/OffworldAstronaut/DrunkardWalk
cd DrunkardWalk
pip install .
```

## Usage

### 1. Run a Single Walk Simulation

```python
sidewalk = Sidewalk(size=100, coin_p=0.5)
sidewalk.wander(end_step=1000)
sidewalk.make_wandering_plot()
sidewalk.make_volatilty_plot()
```

### 2. Run a Multi-Walker Simulation

```python
city = City(n_sidewalks=100, sidewalk_size=100, coin_p=0.5)
city.roam(end_step=500)
city.make_avg_graph()
city.make_std_graph()
```