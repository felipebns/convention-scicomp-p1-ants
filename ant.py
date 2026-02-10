import random
import math

ROUND_PRECISION = 4

class Ant:    
    def __init__(self, fidelity: int, pheromone_sat: int) -> None:
        self.speed = 1
        self.x = 128
        self.y = 128 
        self.found_left = False
        self.found_front = False
        self.found_right = False
        self.left_conc = 0
        self.front_conc = 0
        self.right_conc = 0
        self.angle = random.choice([45, 135, 225, 315]) # Spawn in diagonal
        self.state = "random_walk"
        self.fidelity = fidelity 
        self.pheromone_sat = pheromone_sat 
        self.follow_counter = 0
        self.follow_distances = []
        self.turning_kernel = [0.581, 0.36, 0.047, 0.008, 0.004] # n0, n1, n2, n3, n4 

    def random_walk(self) -> None:
        n_multiplier = random.choice([-1, 1])
        n_value = random.choices([0, 1, 2, 3, 4], weights=self.turning_kernel)[0] #returns list

        self.walk_control()
        self.set_new_angle(n_multiplier, n_value)

    def set_new_angle(self, n_multiplier: int, n_value: int) -> None: #n_multiplier is -1 or 1. n_value is the value of the turning kernel, from 0 to 4
        self.angle = ((n_multiplier * n_value * 45) + self.angle) % 360
    
    def walk_control(self) -> None:
        if self.angle == 0:
            self.y += self.speed
        elif self.angle == 45: 
            self.y += self.speed / math.sqrt(2)
            self.x += self.speed / math.sqrt(2)
        elif self.angle == 90:
            self.x += self.speed
        elif self.angle == 135:
            self.x += self.speed / math.sqrt(2)
            self.y -= self.speed / math.sqrt(2)
        elif self.angle == 180:
            self.y -= self.speed
        elif self.angle == 225:
            self.y -= self.speed / math.sqrt(2)
            self.x -= self.speed / math.sqrt(2)
        elif self.angle == 270:
            self.x -= self.speed
        elif self.angle == 315:
            self.y += self.speed / math.sqrt(2)
            self.x -= self.speed / math.sqrt(2)

        self.x = round(self.x, ROUND_PRECISION)
        self.y = round(self.y, ROUND_PRECISION)

    def update_awareness(self, found_left: bool, found_front: bool, found_right: bool, left_conc: int, front_conc: int, right_conc: int) -> None:
        self.found_left = found_left
        self.found_front = found_front
        self.found_right = found_right
        self.left_conc = left_conc
        self.front_conc = front_conc
        self.right_conc = right_conc

    def chose_state(self) -> None:
        if not(self.x > 256 or self.y > 256 or self.x < 0 or self.y < 0):
            fidelity_result = self.fidelity_test()

            if fidelity_result == 1: # the decision tree is the same for every state of the ant, so there is no need for an if for every state
                if (self.found_front + self.found_left + self.found_right) == 1: #case in wich only one of them is true
                    self.state = "follow"
                elif (self.found_front + self.found_left + self.found_right) > 1: #more than one is true
                    self.state = "fork"
                else:
                    self.state = "random_walk" #no trails
                    self.update_follow_distances()
            else:
                self.state = "random_walk"
                self.update_follow_distances()
        else:
            self.state = "out_of_bounds"

    def update_follow_distances(self):
        if self.follow_counter != 0: #only contabilizes when ant finished following trail, avoids random -> follow
            self.follow_distances.append(self.follow_counter)
            self.follow_counter = 0

    def fidelity_test(self) -> bool:
        return random.randint(0, 255) < self.fidelity

    def follow(self) -> None:
        self.follow_counter += 1
        n_value = 1
        n_multiplier = 0 # if self.found_front is true, n_value stays 0, and the ant keeps moving forward
        if self.found_left:
            n_multiplier = -1
        elif self.found_right:
            n_multiplier = 1

        self.set_new_angle(n_multiplier=n_multiplier, n_value=n_value)
        self.walk_control()

    def fork(self) -> None: #need value of concentration here
        self.follow_counter += 1
        n_value = 1 # first algorithm, prioritaze moving forward, even if it has less concentration!
        n_multiplier = 0 # move forward, same angle 
        if not self.found_front: 
            if self.left_conc > self.pheromone_sat:
                self.left_conc = self.pheromone_sat
            if self.right_conc > self.pheromone_sat:
                self.right_conc = self.pheromone_sat

            if self.left_conc > self.right_conc:
                n_multiplier = -1
            elif self.left_conc < self.right_conc:
                n_multiplier = 1
            elif self.left_conc == self.right_conc:
                n_multiplier = random.choice([-1, 1])
                n_value = random.choices([0, 1, 2, 3, 4], weights=self.turning_kernel)[0] #returns list
                
        self.set_new_angle(n_multiplier, n_value=n_value)
        self.walk_control()

    def control(self) -> None:
        self.chose_state()
        if self.state != "out_of_bounds":
            if self.state == "random_walk":
                self.random_walk()
            elif self.state == "follow":
                self.follow()
            elif self.state == "fork": #need to walk once during fork
                self.fork()