from ant import Ant
from grid import Grid
import numpy as np

class Simulation:
    def __init__(self, fidelity: int, pheromone_saturation: int, decay_rate: float, deposit_rate: float, n_ants: int, max_steps: int) -> None:
        self.fidelety = fidelity
        self.pheromone_saturation = pheromone_saturation
        self.decay_rate = decay_rate
        self.deposit_rate = deposit_rate
        self.n_ants = n_ants
        self.max_steps = max_steps
        self.ants = []
        self.grid = None
        self.setup()

    def setup(self) -> None:
        for i in range(self.n_ants):
            ant = Ant(fidelity=self.fidelety, pheromone_sat=self.pheromone_saturation)
            self.ants.append(ant)

        self.grid = Grid(ants=self.ants, deposit_rate=self.deposit_rate, decay_rate=self.decay_rate)

    def print_results(self, mean_length: float) -> None:
        print(f"F/L ratio: {np.mean([v[0] for v in self.grid.ant_ratio_counter.values()])}")
        print(f"Following ants: {np.mean([v[1] for v in self.grid.ant_ratio_counter.values()])}")
        print(f"Exploring ants: {np.mean([v[2] for v in self.grid.ant_ratio_counter.values()])}")
        print(f"r mean lenght of trails: {mean_length}")

    def calculate_mean_length(self) -> float:
        mean_length = 0
        for ant in self.ants:
            if len(ant.follow_distances) > 0:
                mean_length += np.mean(ant.follow_distances)
        mean_length = mean_length / len(self.ants)
        return mean_length

    def simulate_ant_movement(self) -> None:
        step = 0
        release_control = self.n_ants - 1
        removed_indexes = []
        while step < self.max_steps:
            for ant_index in range(len(self.ants) - release_control):
                if ant_index not in removed_indexes:
                    ant = self.ants[ant_index]
                    self.grid.scan_environment(ant=ant) # first thing
                    self.grid.deposit_pheromones(ant=ant) # first deposit, then move
                    ant.control() 
                    self.grid.update_ant_status_counter(ant=ant)
                    if ant.state == "out_of_bounds":
                        removed_indexes.append(ant_index)

            self.grid.update_ant_ratio_counter(step=step)
            self.grid.clean_ant_status_counter()
            self.grid.decay_pheromones()
            if release_control > 0:
                release_control -= 1
            step += 1

    def run(self) -> None:
        self.simulate_ant_movement()

        mean_length = self.calculate_mean_length()

        self.print_results(mean_length)

        self.grid.plot_movement()