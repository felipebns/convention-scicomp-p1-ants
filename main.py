from simulation import Simulation

if __name__ == "__main__":
    fidelity = 247
    pheromone_saturation = 50
    decay_rate = 0.4
    deposit_rate = 8
    n_ants = 500
    max_steps = 1500

    sim = Simulation(fidelity=fidelity, pheromone_saturation=pheromone_saturation, decay_rate=decay_rate, deposit_rate=deposit_rate, n_ants=n_ants, max_steps=max_steps)
    sim.run()

