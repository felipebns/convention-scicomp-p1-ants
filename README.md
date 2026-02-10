# Project 1 - Ants - SciComp

Ant trail formation simulation based on the Watmough95 paper.

## How to run the project

1. Create and activate the virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the simulation:
```bash
python main.py
```

## How to run tests

```bash
python test/run_tests.py
```

## Simulation results

At the end of execution, the program prints:

- **F/L ratio**: Ratio between ants following trails (Following) and exploring (Leading/random_walk)
- **Following ants**: Average number of ants following trails per step
- **Exploring ants**: Average number of ants exploring per step
- **r mean length of trails**: Average length of trails followed by ants

Additionally, a plot showing the pheromone trails is displayed.