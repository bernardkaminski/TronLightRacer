__author__ = 'Saki'

import unittest
import gtk
import sys
sys.path.insert(0,'../src/')
from gui import LoginManagement


class LoginUser(unittest.TestCase):

    #Setup LoginManagement(), all user and password entries and the login button (widget)
    def setUp(self):
        self.loginTest = LoginManagement()
        self.loginButton = gtk.Button()
        self.userEntry1 = gtk.Entry()
        self.passwordEntry1 = gtk.Entry()
        self.userEntry2 = gtk.Entry()
        self.passwordEntry2 = gtk.Entry()

    #If the user enters the wrong username (with right password) it wont let the user login
    def testNoUserNoLogin(self):
        self.userEntry1.set_text("Vanessa")
        self.userEntry2.set_text("Saki")
        self.passwordEntry1.set_text("Dem@Us3R01")
        self.passwordEntry2.set_text("Dem@Us3R02")
        self.loginTest.user_one_verified = False
        self.loginTest.user_two_verified = False

        self.loginTest.login_user(self.loginButton,self.userEntry1,self.passwordEntry1, self.userEntry2, 1)
        self.assertTrue(self.loginTest.user_one_verified==False, "We should not let User1 login!")
        self.assertTrue(self.loginTest.user_two_verified==False, "We should not let User2 login!")

        self.loginTest.login_user(self.loginButton,self.userEntry2,self.passwordEntry2, self.userEntry1, 2)
        self.assertTrue(self.loginTest.user_one_verified==False, "We should not let User1 login!")
        self.assertTrue(self.loginTest.user_two_verified==False, "We should not let User2 login!")

    #If the user enters the wrong password (with right username) it wont let the user login
    def testNoPasswordNoLogin(self):
        self.userEntry1.set_text("Demo01")
        self.userEntry2.set_text("Demo02")
        self.passwordEntry1.set_text("WeAreAwesome4Ever*")
        self.passwordEntry2.set_text("YeahTotally!")
        self.loginTest.user__one_verified = False
        self.loginTest.user2_two_verified = False

        self.loginTest.login_user(self.loginButton,self.userEntry1,self.passwordEntry1, self.userEntry2, 1)
        self.assertTrue(self.loginTest.user_one_verified==False, "We should not let User1 login!")
        self.assertTrue(self.loginTest.user_two_verified==False, "We should not let User2 login!")

        self.loginTest.login_user(self.loginButton,self.userEntry2,self.passwordEntry2, self.userEntry1, 2)
        self.assertTrue(self.loginTest.user_one_verified==False, "We should not let User1 login!")
        self.assertTrue(self.loginTest.user_two_verified==False, "We should not let User2 login!")

    #Only User 1 logs in, User 2 should not be logged in
    def testLoginOnlyUser1(self):
        self.userEntry1.set_text("Demo01")
        self.userEntry2.set_text("Demo02")
        self.passwordEntry1.set_text("Dem@Us3R01")
        self.passwordEntry2.set_text("Dem@Us3R02")
        self.loginTest.user_one_verified= False
        self.loginTest.user_two_verified = False

        self.loginTest.login_user(self.loginButton,self.userEntry1,self.passwordEntry1, self.userEntry2, 1)
        self.assertTrue(self.loginTest.user_one_verified==True, "Let User1 login!")
        self.assertTrue(self.loginTest.user_two_verified==False, "User2 should not be logged in!")

    #Only User 2 logs in, User 1 should not be logged in
    def testLoginOnlyUser2(self):
        self.userEntry1.set_text("Demo01")
        self.userEntry2.set_text("Demo02")
        self.passwordEntry1.set_text("Dem@Us3R01")
        self.passwordEntry2.set_text("Dem@Us3R02")
        self.loginTest.user_one_verified = False
        self.loginTest.user_two_verified = False

        self.loginTest.login_user(self.loginButton,self.userEntry2,self.passwordEntry2, self.userEntry1, 2)
        self.assertTrue(self.loginTest.user_one_verified==False, "User1 should not be logged in!")
        self.assertTrue(self.loginTest.user_two_verified==True, "Let User2 login!")

    #Loigin a user when after another user (one user is already logged in)
    def testLoginWithAnotherUserLoggedIn(self):
        self.userEntry1.set_text("Demo01")
        self.userEntry2.set_text("Demo02")
        self.passwordEntry1.set_text("Dem@Us3R01")
        self.passwordEntry2.set_text("Dem@Us3R02")
        self.loginTest.user_one_verified = False
        self.loginTest.user_two_verified = True

        self.loginTest.login_user(self.loginButton,self.userEntry1,self.passwordEntry1, self.userEntry2, 1)
        self.assertTrue(self.loginTest.user_one_verified==True, "Let User1 login!")
        self.assertTrue(self.loginTest.user_two_verified==True, "Let User2 login!")

        self.loginTest.user_one_verified = True
        self.loginTest.user_two_verified = False

        self.loginTest.login_user(self.loginButton,self.userEntry2,self.passwordEntry2, self.userEntry1, 2)
        self.assertTrue(self.loginTest.user_one_verified==True, "Let User1 login!")
        self.assertTrue(self.loginTest.user_two_verified==True, "Let User2 login!")

    #When an user tries to login but with the same username as the user already logged in
    def testLoginUser1AndUser2(self):
        self.userEntry1.set_text("Demo01")
        self.userEntry2.set_text("Demo02")
        self.passwordEntry1.set_text("Dem@Us3R01")
        self.passwordEntry2.set_text("Dem@Us3R02")
        self.loginTest.user_one_verified = True
        self.loginTest.user_two_verified = False

        self.loginTest.login_user(self.loginButton, self.userEntry1,self.passwordEntry1, self.userEntry1, 2)
        self.assertTrue(self.loginTest.user_one_verified==True, "User1 already logged in!")
        self.assertTrue(self.loginTest.user_two_verified==False, "User2 already logged in as User1!")

        self.loginTest.user_one_verified = False
        self.loginTest.user_two_verified = True

        self.loginTest.login_user(self.loginButton, self.userEntry2,self.passwordEntry2, self.userEntry2, 1)
        self.assertTrue(self.loginTest.user_one_verified==False, "User1 already logged in as User2!")
        self.assertTrue(self.loginTest.user_two_verified==True, "User2 already logged in!")

