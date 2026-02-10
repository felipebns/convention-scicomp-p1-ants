import matplotlib.pyplot as plt
import math

class Grid:
    def __init__(self, ants: list, deposit_rate: int, decay_rate: int) -> None:
        self.ants = ants
        self.deposit_rate = deposit_rate
        self.decay_rate = decay_rate
        self.x_min = 0
        self.x_max = 256
        self.y_min = 0
        self.y_max = 256
        self.following_ants = 0
        self.exploring_ants = 0
        self.ant_ratio_counter = {}
        self.pheromone_trails = {}

    def decay_pheromones(self) -> None:
        pos_invalidas = []
        for pos, concentration in self.pheromone_trails.items():
            if concentration <= 1:
                pos_invalidas.append(pos)
            else:
                self.pheromone_trails[pos] -= self.decay_rate

        for pos in pos_invalidas:
            self.pheromone_trails.pop(pos)

    def deposit_pheromones(self, ant: object) -> None:
        if (ant.x, ant.y) not in self.pheromone_trails.keys():
            self.pheromone_trails[(ant.x, ant.y)] = self.deposit_rate 
        else:
            self.pheromone_trails[(ant.x, ant.y)] += self.deposit_rate

    def update_ant_status_counter(self, ant: object) -> None:
        if ant.state != "out_of_bounds":
            if ant.state == "random_walk":
                self.exploring_ants += 1
            if ant.state == "follow" or ant.state == "fork":
                self.following_ants += 1

    def update_ant_ratio_counter(self, step: int) -> None:
        if self.exploring_ants != 0:
            self.ant_ratio_counter[step] = (self.following_ants / self.exploring_ants, self.following_ants, self.exploring_ants)
        else: 
            self.ant_ratio_counter[step] = (self.following_ants / 1, self.following_ants, 1) # minimize the error with setting exploring ants as 1
    
    def clean_ant_status_counter(self) -> None:
        self.following_ants = 0
        self.exploring_ants = 0

    def scan_environment(self, ant: object) -> None: #assume the ant only looks forward
        found_left = False
        found_front = False
        found_right = False

        left_conc = 0
        front_conc = 0
        right_conc = 0

        if ant.angle == 0:
            pos_left = (ant.x - (ant.speed / math.sqrt(2)), ant.y + (ant.speed / math.sqrt(2)))
            pos_front = (ant.x, ant.y + ant.speed)
            pos_right = (ant.x + (ant.speed / math.sqrt(2)), ant.y + (ant.speed / math.sqrt(2)))
        elif ant.angle == 45:
            pos_left = (ant.x, ant.y + ant.speed)
            pos_front = (ant.x + (ant.speed / math.sqrt(2)), ant.y + (ant.speed / math.sqrt(2)))
            pos_right = (ant.x + ant.speed, ant.y)
        elif ant.angle == 90:
            pos_left = (ant.x + (ant.speed / math.sqrt(2)), ant.y + (ant.speed / math.sqrt(2)))
            pos_front = (ant.x + ant.speed, ant.y)
            pos_right = (ant.x + (ant.speed / math.sqrt(2)), ant.y - (ant.speed / math.sqrt(2)))
        elif ant.angle == 135:
            pos_left = (ant.x + ant.speed, ant.y)
            pos_front = (ant.x + (ant.speed / math.sqrt(2)), ant.y - (ant.speed / math.sqrt(2)))
            pos_right = (ant.x, ant.y - ant.speed)
        elif ant.angle == 180:
            pos_left = (ant.x + (ant.speed / math.sqrt(2)), ant.y - (ant.speed / math.sqrt(2)))
            pos_front = (ant.x, ant.y - ant.speed)
            pos_right = (ant.x - (ant.speed / math.sqrt(2)), ant.y - (ant.speed / math.sqrt(2)))  
        elif ant.angle == 225:
            pos_left = (ant.x, ant.y - ant.speed)
            pos_front = (ant.x - (ant.speed / math.sqrt(2)), ant.y - (ant.speed / math.sqrt(2)))
            pos_right = (ant.x - ant.speed, ant.y) 
        elif ant.angle == 270:
            pos_left = (ant.x - (ant.speed / math.sqrt(2)), ant.y - (ant.speed / math.sqrt(2)))
            pos_front = (ant.x - ant.speed, ant.y)
            pos_right = (ant.x - (ant.speed / math.sqrt(2)), ant.y + (ant.speed / math.sqrt(2)))
        elif ant.angle == 315:
            pos_left = (ant.x - ant.speed, ant.y)
            pos_front = (ant.x - (ant.speed / math.sqrt(2)), ant.y + (ant.speed / math.sqrt(2)))
            pos_right = (ant.x, ant.y + ant.speed)

        if pos_left in self.pheromone_trails.keys():
            found_left = True
            left_conc = self.pheromone_trails[pos_left]
        if pos_front in self.pheromone_trails.keys():
            found_front = True
            front_conc = self.pheromone_trails[pos_front]
        if pos_right in self.pheromone_trails.keys():
            found_right = True
            right_conc = self.pheromone_trails[pos_right]
        
        ant.update_awareness(found_left, found_front, found_right, left_conc, front_conc, right_conc)
        
    def plot_movement(self) -> None:
        plt.figure(figsize=(10, 10))
        
        x_coords = [pos[0] for pos in self.pheromone_trails.keys()]
        y_coords = [pos[1] for pos in self.pheromone_trails.keys()]
        plt.scatter(x_coords, y_coords, c='black', s=20, alpha=0.6)
        
        plt.xlim(self.x_min, self.x_max)
        plt.ylim(self.y_min, self.y_max)
        plt.xlabel('X Position')
        plt.ylabel('Y Position')
        plt.title('Trail Formation by Foraging Ants')
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()