__author__ = 'Saki'

import unittest
import gtk
import sys
sys.path.insert(0,'../src/')
from engine import Grid
from engine import GameFrame

class GridTesting(unittest.TestCase):

    #Setting up GameFrame and Grid
    def setUp(self):
        self.game_frame = GameFrame
        self.grid = Grid(750, 500, 5, "Vanessa", "Saki", 0, 80, self.game_frame)

    #Player 1 or 2 collides with Player 1's tail
    def testCollisionTail1(self):
        self.grid.p1_obstacle_list.amount_of_obstacles = 12
        self.grid.player_one.x = 120
        self.grid.player_one.y = 140
        self.grid.player_two.x = 120
        self.grid.player_two.y = 140
        self.grid.p1_obstacle_list.x[4] = 120
        self.grid.p1_obstacle_list.y[4] = 140
        self.grid.check_collision()
        self.assertTrue(self.grid.player_one.is_alive == False, "player_one should be dead!")
        self.assertTrue(self.grid.player_two.is_alive == False, "player_two should be dead!")

    #Player 1 or 2 collides with Player 2's tail
    def testCollisionTail2(self):
        self.grid.p2_obstacle_list.amount_of_obstacles = 12
        self.grid.player_one.x = 120
        self.grid.player_one.y = 140
        self.grid.player_two.x = 120
        self.grid.player_two.y = 140
        self.grid.p2_obstacle_list.x[4] = 120
        self.grid.p2_obstacle_list.y[4] = 140
        self.grid.check_collision()
        self.assertTrue(self.grid.player_one.is_alive == False, "player_one should be dead!")
        self.assertTrue(self.grid.player_two.is_alive == False, "player_two should be dead!")

    #Player 1 or 2 collides with the obstacle on the map
    def testCollisionObstacleMap(self):
        self.grid.map_obstacle_list.amount_of_obstacles = 12
        self.grid.player_one.x = 120
        self.grid.player_one.y = 140
        self.grid.player_two.x = 120
        self.grid.player_two.y = 140
        self.grid.map_obstacle_list.x[4] = 120
        self.grid.map_obstacle_list.y[4] = 140
        self.grid.check_collision()
        self.assertTrue(self.grid.player_one.is_alive == False, "player_one should be dead!")
        self.assertTrue(self.grid.player_two.is_alive == False, "player_two should be dead!")

    #Player 1 or 2 collides with the wall (Right and Bottom walls)
    def testCollisionWall1(self):
        self.grid.map_obstacle_list.amount_of_obstacles = 12
        self.grid.player_one.x = 750
        self.grid.player_one.y = 500
        self.grid.check_collision()
        self.assertTrue(self.grid.player_one.is_alive == False, "player_one should be dead!")

    #Player 1 or 2 collides with the wall (Left and Top walls)
    def testCollisionWall2(self):
        self.grid.map_obstacle_list.amount_of_obstacles = 12
        self.grid.player_one.x = 0
        self.grid.player_one.y = 0
        self.grid.check_collision()
        self.assertTrue(self.grid.player_one.is_alive == False, "player_one should be dead!")

    #Check the status after first game play
    def testCheckGameCount1(self):
        self.grid.game_count = 0
        self.grid.player_one.is_alive = True
        self.grid.player_two.is_alive = True
        self.assertTrue(self.grid.on_timer()== True, "game_count is less than 3, it should return True!")

    #Check the status after second game play
    def testCheckGameCount2(self):
        self.grid.game_count = 1
        self.grid.player_one.is_alive = True
        self.grid.player_two.is_alive = True
        self.assertTrue(self.grid.on_timer()== True, "game_count is less than 3, it should return True!")

   #Check the status after third game play
    def testsCheckGameCount3(self):
        self.grid.game_count = 2
        self.grid.player_one.is_alive = True
        self.grid.player_two.is_alive = True
        self.assertTrue(self.grid.on_timer()== True, "game_count is less than 3, it should return True!")

   #Check the status after third game play
    def testsCheckGameCountOver(self):
        self.grid.game_count = 3
        self.grid.player_one.is_alive = True
        self.grid.player_two.is_alive = True
        self.assertTrue(self.grid.on_timer()== False, "game_count is equal to 3, it should return False!")