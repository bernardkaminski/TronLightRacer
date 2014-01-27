__author__ = 'Saki'

import unittest
import gtk
import sys
sys.path.insert(0, '../src/')
from gui import LoginManagement


class AddUser(unittest.TestCase):

    #Setup LoginManagement(), all user and password entries and the Login button (widget)
    def setUp(self):
        self.addUserTest = LoginManagement()
        self.userEntry = gtk.Entry()
        self.passwordEntry = gtk.Entry()
        self.loginButton = gtk.Button()
        self.addUserTest.username_taken = False
        self.addUserTest.make_account = True

    #Verify if we can add an user successfully
    #(this test will return false after the second try because the user will already exists in the user.csv)
    def testAddUserSuccessful(self):
        self.userEntry.set_text("BarackObama")
        self.passwordEntry.set_text("Password1*")

        self.addUserTest.add_user(self.loginButton, self.userEntry, self.passwordEntry)
        self.assertTrue(self.addUserTest.username_taken==False, "Username is not taken yet!")
        self.assertTrue(self.addUserTest.make_account==True, "User should be able to make an account")

    #If the username already exists in the user.csv file it will not let the user create an account
    def testUsernameAlreadyExists(self):
        self.userEntry.set_text("Demo01")
        self.passwordEntry.set_text("Dem@Us3R01")
        self.addUserTest.username_taken = False
        self.addUserTest.make_account = True

        self.addUserTest.add_user(self.loginButton, self.userEntry, self.passwordEntry)
        self.assertTrue(self.addUserTest.username_taken == True, "Username is already taken")
        self.assertTrue(self.addUserTest.make_account == True, "User should not be able to make an account")

    #If there is a non alphanumerical character in the username it will not let the user create an account
    def testUsernameRestriction(self):
        self.userEntry.set_text("WeAreAwesomeYeah***")
        self.passwordEntry.set_text("Totally!Yeah*")
        self.addUserTest.username_taken = False
        self.addUserTest.make_account = True

        self.addUserTest.add_user(self.loginButton, self.userEntry, self.passwordEntry)
        self.assertTrue(self.addUserTest.username_taken==False, "Username is not taken yet")
        self.assertTrue(self.addUserTest.make_account==False, "Username must contain only ASCII characters")

    #If the password is less than 8 characters, it will not let the user create an account
    def testPasswordContains8Char(self):
        self.userEntry.set_text("Vanessa")
        self.passwordEntry.set_text("Jones1!")
        self.addUserTest.username_taken = False
        self.addUserTest.make_account = True

        self.addUserTest.add_user(self.loginButton, self.userEntry, self.passwordEntry)
        self.assertTrue(self.addUserTest.username_taken==False, "Username is not taken yet")
        self.assertTrue(self.addUserTest.make_account==False, "Password must be at least eight characters long!")

    #If the password does not contain one Uppercase letter, it will not let the user create an account
    def testPasswordContainsOneUppercase(self):
        self.userEntry.set_text("Vanessa01")
        self.passwordEntry.set_text("vanessajones1!")
        self.addUserTest.username_taken = False
        self.addUserTest.make_account = True

        self.addUserTest.add_user(self.loginButton, self.userEntry, self.passwordEntry)
        self.assertTrue(self.addUserTest.username_taken==False, "Username is not taken yet")
        self.assertTrue(self.addUserTest.make_account==False, "Password must contain one uppercase character!")

    #If the password does not contain one non alphanumeric character, it will not let the user create an account
    def testPasswordContainsNonAlphanumeric(self):
        self.userEntry.set_text("Saki01")
        self.passwordEntry.set_text("Saki4Ever")
        self.addUserTest.username_taken = False
        self.addUserTest.make_account = True

        self.addUserTest.add_user(self.loginButton, self.userEntry, self.passwordEntry)
        self.assertTrue(self.addUserTest.username_taken == False, "Username is not taken yet")
        self.assertTrue(self.addUserTest.make_account == False, "Password must contain one non alphanumeric character!")

    #If the password does not contain one number, it will not let the user create an account
    def testPasswordContainsOneDigit(self):
        self.userEntry.set_text("Saki02")
        self.passwordEntry.set_text("SakiForever!!")
        self.addUserTest.username_taken = False
        self.addUserTest.make_account = True

        self.addUserTest.add_user(self.loginButton, self.userEntry, self.passwordEntry)
        self.assertTrue(self.addUserTest.username_taken == False, "Username is not taken yet")
        self.assertTrue(self.addUserTest.make_account == False, "Password must contain one number!")