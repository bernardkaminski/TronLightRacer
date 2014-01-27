__author__ = 'Saki'
import unittest
import sys
sys.path.insert(0,'../src/')
from engine import Player


class StatisticsTest(unittest.TestCase):

    #Setting up Player
    def setUp(self):
        self.player = Player(200, 200, "imagename", 5)

    #Check coordinates after the method move() (should decrease the y coordinate by dot_size (in this case 5))
    def testCoordinates(self):
        self.player.move()
        self.assertEquals(self.player.x, 200, "Incorrect default x position")
        self.assertEquals(self.player.y, 195, "Incorrect default y position")

    #Check coordinates after left button is pressed and move() method is called
    # (should decrease the y coordinate by dot_size (in this case 5) and x coordinates by dot_size)
    def testCoordinatesAfterLeft(self):
        self.player.left = True
        self.player.move()
        self.assertEquals(self.player.x, 195, "Incorrect x position")
        self.assertEquals(self.player.y, 195, "Incorrect y position")

if __name__ == "__main__":
    unittest.main()
