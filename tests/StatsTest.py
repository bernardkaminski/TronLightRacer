__author__ = 'saki'

import unittest
import gtk
import sys
sys.path.insert(0,'../src/')
from gui import LoginManagement

class StatisticsTests(unittest.TestCase):

    #Setup LoginManagement(), all user and password entries and the viewStats button (widget)
    def setUp(self):
        self.statsTest = LoginManagement()
        self.viewStats = gtk.Button()
        self.user1 = gtk.Entry()
        self.user1.set_text("Demo01")
        self.user2 = gtk.Entry()
        self.user2.set_text("Demo02")
        self.user3 = gtk.Entry()
        self.user3.set_text("Demo11")

    #Verify if returns right personal statistics for user whom has already played
    def testVerifyPersonalUserExist(self):
        self.statsTest.personal_stats(self.viewStats,self.user1)
        self.assertTrue(self.statsTest.wins=="8", "wrong message")
        self.assertTrue(self.statsTest.ties=="0", "wrong message")
        self.assertTrue(self.statsTest.losses=="14", "wrong message")
        self.assertTrue(self.statsTest.games=="22", "wrong message")

    #Verify if returns right personal statistics for user whom never played before
    def testVerifyPersonalUserDoesNotExist(self):
        self.statsTest.personal_stats(self.viewStats,self.user3)
        self.assertTrue(self.statsTest.wins=="", "wrong message")
        self.assertTrue(self.statsTest.ties=="", "wrong message")
        self.assertTrue(self.statsTest.losses=="", "wrong message")
        self.assertTrue(self.statsTest.games=="", "wrong message")

    #Verify if returns right head to head stats for users who already player against each other
    def testVerifyHeadUsersAlreadyPlayed(self):
        self.statsTest.view_head(self.viewStats,self.user1,self.user2)
        self.assertTrue(self.statsTest.player_one_wins=="2","wrong")
        self.assertTrue(self.statsTest.player_ties=="0","wrong")
        self.assertTrue(self.statsTest.player_two_wins=="2","wrong")

    #Verify if returns right head-to head stats for users who never played
    def testVerifyHeadUsersNeverPlayed(self):
        self.statsTest.view_head(self.viewStats,self.user1,self.user3)
        self.assertTrue(self.statsTest.player_one_wins=="","wrong")
        self.assertTrue(self.statsTest.player_ties=="","wrong")
        self.assertTrue(self.statsTest.player_two_wins=="","wrong")

    #Verify if the Default TopTen is right
    def testDefaultTopTen(self):
        self.assertTrue(self.statsTest.wins == [], "wrong" )
        self.assertTrue(self.statsTest.user_names == [], "wrong")

    #Verify if the First player on the list is correct
    def testTopTenFirst(self):
        self.statsTest.view_top_ten(self.viewStats)
        self.assertTrue(self.statsTest.wins[5] == 8, "wrong" )
        self.assertTrue(self.statsTest.user_names[5] == ["Demo01", "Demo06"], "wrong")

    #Verify if the player in the random order is correct
    def testTopTenRandom(self):
        self.statsTest.view_top_ten(self.viewStats)
        self.assertTrue(self.statsTest.wins[3] == 5, "wrong" )
        self.assertTrue(self.statsTest.user_names[3] == ["Demo05", "Demo10"], "wrong")

    #Verify if the Last player on the list is correct
    def testTopTenLast(self):
        self.statsTest.view_top_ten(self.viewStats)
        self.assertTrue(self.statsTest.wins[0] == 2, "wrong" )
        self.assertTrue(self.statsTest.user_names[0] == ["Demo07"], "wrong")


if __name__ == "__main__":
    unittest.main()

