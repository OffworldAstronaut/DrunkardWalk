# 🍺 DrunkardWalk

This is a study repository dedicated to the unidimensional random walk, commonly known as the "drunkard walk".

This repository, written in Python and structured based on the OOP principles, models both the *isotropic* variety of the stochastic process as first studied by Pearson (1905) and the **unidimensional random walk in a random environment** (RWRE) as mentioned by **Bogachev (2006)**. 

The RWRE modeled here is probably the simplest avaiable model of the genre: an unidimensional random walk over a lattice with **static disorder** -- each position of the 1D space has a different coin assigned to it randomly before the system's time evolution.

## Features

- OOP architecture, simple to develop and maintain; 
- Models both the simplest isotropic case and the static disorder variety with ease; 
- Static disorder regulated by a parameter $w \in [0.0, 1.0]$;
- Simulation and plotting included as class methods; 

---

## Structure

### Classes

- ``Drunkard``: models a walker, forms a composition relation with ``Sidewalk``; 
- ``Sidewalk``: environment for the walker's walk, has basic movement and plotting methods; 
- ``City``: environment for multiple sidewalks, executes ensemble simulations and statistics;

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
# examplesidewalk.py

import DrunkardWalk as DW

# Dummy variables -- we only need the size of the sidewalks and the coins 
quantity_sidewalks = 10_000
size_sidewalks = 1_500
disorder_intensity = 0.00

city = DW.City(quantity_sidewalks, size_sidewalks, disorder_intensity)

# generate the coins 
coins = city.generate_coins()

# create a sidewalk with the generated coins

sidewalk = DW.Sidewalk(size_sidewalks, coins)

sidewalk.wander(end_step=20_000)

sidewalk.plot_avgpos()
sidewalk.plot_stdpos(1000, loglog=True)
sidewalk.plot_endpos()

```

### 2. Run a Multi-Walker Simulation

```python

# examplecity.py 

import DrunkardWalk as DW

quantity_sidewalks = 10_000
size_sidewalks = 1_500
disorder_intensity = 1.00

city = DW.City(quantity_sidewalks, size_sidewalks, disorder_intensity)

city.roam()

#city.make_avg_graph(plot_only=True)
city.make_std_graph(tail=125, plot_only=True, loglog=True)
#city.make_endpos_graph()
```

## TODO

- Better integration between ``City`` and ``Sidewalk``: the latter should generate it's own coins;
- Plotting improvements (specially log-log dispersion and exponent calculation); 
- Integration of ``comparison_alpha_w.py`` as a City's special method;
- Code re-documentation for up-to-date explanations;