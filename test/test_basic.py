import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ant import Ant
from grid import Grid


class TestBasic(unittest.TestCase):
    
    def setUp(self):
        self.ant = Ant(fidelity=255, pheromone_sat=24)
        self.grid = Grid([self.ant], deposit_rate=8, decay_rate=1)
    
    def test_ant_initialization(self):
        self.assertEqual(self.ant.x, 128)
        self.assertEqual(self.ant.y, 128)
        self.assertEqual(self.ant.state, "random_walk")
    
    def test_ant_movement(self):
        self.ant.angle = 0
        initial_y = self.ant.y
        self.ant.walk_control()
        self.assertEqual(self.ant.y, initial_y + 1)
    
    def test_grid_initialization(self):
        self.assertEqual(self.grid.x_max, 256)
        self.assertEqual(self.grid.y_max, 256)
        self.assertEqual(len(self.grid.ants), 1)
    
    def test_pheromone_deposit(self):
        self.ant.x = 100
        self.ant.y = 100
        self.grid.deposit_pheromones(self.ant)
        self.assertIn((100, 100), self.grid.pheromone_trails)
        self.assertEqual(self.grid.pheromone_trails[(100, 100)], 8)
    
    def test_pheromone_decay(self):
        self.grid.pheromone_trails[(100, 100)] = 10
        self.grid.decay_pheromones()
        self.assertEqual(self.grid.pheromone_trails[(100, 100)], 9)
    
    def test_scan_no_pheromones(self):
        self.grid.scan_environment(self.ant)
        self.assertFalse(self.ant.found_front)
        self.assertFalse(self.ant.found_left)
        self.assertFalse(self.ant.found_right)
    
    def test_scan_with_pheromones(self):
        self.ant.angle = 0
        self.grid.pheromone_trails[(128, 129)] = 10
        self.grid.scan_environment(self.ant)
        self.assertTrue(self.ant.found_front)
    
    def test_state_follow(self):
        self.ant.found_front = True
        self.ant.fidelity = 255
        self.ant.chose_state()
        self.assertEqual(self.ant.state, "follow")
    
    def test_state_random_walk(self):
        self.ant.found_front = False
        self.ant.found_left = False
        self.ant.found_right = False
        self.ant.fidelity = 255
        self.ant.chose_state()
        self.assertEqual(self.ant.state, "random_walk")
    
    def test_out_of_bounds(self):
        self.ant.x = 300
        self.ant.chose_state()
        self.assertEqual(self.ant.state, "out_of_bounds")


if __name__ == '__main__':
    unittest.main()
