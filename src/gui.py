#!/usr/bin/env python
from decimal import Decimal

__author__ = 'vanessajones, bernie, tony'

import gtk
import csv
from engine import GameFrame
from collections import OrderedDict

class LoginManagement:
    """
    The LoginManagement class is responsible for handling the login system and all the GUI associated with the main menu of the game.
    This will include displaying all statistics, warning messages, and a main menu screen for logging in and out.
    """

    def __init__(self):
        """
        This is the initialization function for the LoginManagement class. It creates a main menu window for a user
        to login, view statistics, and play
        @return:Nothing
        """
        self.make_account = True
        self.username_taken = False
        self.wins = ""
        self.losses = ""
        self.ties = ""
        self.games = ""
        self.player_one_wins = ""
        self.player_two_wins = ""
        self.player_ties = ""

        # Option to pick which map to load
        self.option = 0 # default map selection will be 0: plain
        self.refresh = 80 # default speed will be slow: 80 (refresh rate)

        # file that contains the user information
        self.filename = "../res/data/users.csv"
        # file that contains the user information
        self.filename_versus = "../res/data/scoreVS.csv"
        # file that the user information will be copied to
        self.temp_name_versus = "../res/data/scoreVSTemp.csv"

        self.filename_score = "../res/data/score.csv"
        self.temp_name_score = "../res/data/scoreTemp.csv"
        self.message = ""

        # Set users as unverified yet
        self.user_one_verified = False
        self.user_two_verified = False

        # Building main window for the login and game
        self.window = gtk.Window()
        self.window.set_default_size(750,500)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_title("Tron")

        # Creating title "Tron" label
        title = gtk.Label("Tron")
        title.set_size_request(100,100)
        title.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#40E0D0'))

        # Username label user 1
        username_label_one = gtk.Label("Username:")
        title.set_size_request(100,100)

        # Password label user 1
        password_label_one = gtk.Label("Password:")
        title.set_size_request(100,100)

        # Username label user 2
        username_label_two = gtk.Label("Username:")
        title.set_size_request(100,100)

        # Password label user 2
        password_label_two = gtk.Label("Password:")
        title.set_size_request(100,100)

        # Creating login title labels
        user_one_login = gtk.Label("User 1 login")
        user_two_login = gtk.Label("User 2 login")

        # Creating text box for username
        self.user_one_entry = gtk.Entry()
        # Set visibility to true --> you can see what you write
        self.user_one_entry.set_visibility(True)

        # Creating text box for password
        self.user_one_password = gtk.Entry()
        # Set visibility to false --> people cannot see your password as you type
        self.user_one_password.set_visibility(False)

        # Repeat previous step for user 2
        self.user_two_entry = gtk.Entry()
        self.user_two_entry.set_visibility(True)

        self.user_two_password = gtk.Entry()
        self.user_two_password.set_visibility(False)

        # Creating button for create account option
        self.user_one_create = gtk.Button()
        self.user_one_create.set_label("Create Account")
        self.user_one_create.set_size_request(120,30)

        # Creating button for login option
        self.user_one_login = gtk.Button()
        self.user_one_login.set_label("Login")
        self.user_one_login.set_size_request(120,30)

        # Creating button for logout option
        self.user_one_logout = gtk.Button()
        self.user_one_logout.set_label("Logout")
        self.user_one_logout.set_size_request(120, 30)
        # Set sensitive to false --> people cannot press on it yet, indeed you cant logout before logging in
        self.user_one_logout.set_sensitive(False)

        # Creating button for view stats option
        self.user_one_stats = gtk.Button()
        self.user_one_stats.set_label("View Stats")
        self.user_one_stats.set_size_request(120, 30)
        # Set sensitive to false --> people cannot press on it yet, you can't view personal stats if nobody is logged in
        self.user_one_stats.set_sensitive(False)

        # Creating button for create an account
        self.user_two_create = gtk.Button()
        self.user_two_create.set_label("Create Account")
        self.user_two_create.set_size_request(120,30)

        # Creating button for login
        self.user_two_login = gtk.Button()
        self.user_two_login.set_label("Login")
        self.user_two_login.set_size_request(120,30)

        # Creating button for logout
        self.user_two_logout = gtk.Button()
        self.user_two_logout.set_label("Logout")
        self.user_two_logout.set_size_request(120,30)
        self.user_two_logout.set_sensitive(False)

        self.user_two_stats = gtk.Button()
        self.user_two_stats.set_label("View Stats")
        self.user_two_stats.set_size_request(120, 30)
        self.user_two_stats.set_sensitive(False)

        # Creating play button. Will be grayed out until both users are logged in
        self.play_button = gtk.Button()
        self.play_button.set_label("Play!")
        self.play_button.set_size_request(120,30)
        self.play_button.set_sensitive(False)

        # Creating top 10 button to view stats of top 10 players, any user can see it.
        top_ten = gtk.Button()
        top_ten.set_label("Top 10")
        top_ten.set_size_request(120, 30)
        top_ten.set_sensitive(True)
        self.wins = []
        self.user_names = []

        # Creating head to head stats button to view stats between two players, if both as logged in
        self.head_to_head = gtk.Button()
        self.head_to_head.set_label("Head-To-Head")
        self.head_to_head.set_size_request(120, 30)
        self.head_to_head.set_sensitive(False)

        # Creating settings button to access settings page
        self.settings = gtk.Button()
        self.settings.set_label("Settings")
        self.settings.set_size_request(120, 30)
        self.settings.set_sensitive(False)

        # Creating container to place all widgets inside
        self.fix = gtk.Fixed()

        # Placing widgets inside container at specific locations

        # Player 1 login
        self.fix.put(user_one_login, 125, 150)
        self.fix.put(username_label_one,130,200)
        self.fix.put(password_label_one,130,260)
        self.fix.put(self.user_one_entry,80,230)
        self.fix.put(self.user_one_password,80,290)
        self.fix.put(self.user_one_create,100,340)
        self.fix.put(self.user_one_login,100,370)
        self.fix.put(self.user_one_logout, 100, 400)
        self.fix.put(self.user_one_stats, 100, 430)

        # Middle of menu
        self.fix.put(top_ten, 315, 300)
        self.fix.put(self.head_to_head, 315, 330)
        self.fix.put(self.play_button,315,270)
        self.fix.put(self.settings, 315, 360)

        # Player 2 login
        self.fix.put(user_two_login, 550, 150)
        self.fix.put(username_label_two,560,200)
        self.fix.put(password_label_two,560,260)
        self.fix.put(self.user_two_entry,510,230)
        self.fix.put(self.user_two_password,510,290)
        self.fix.put(self.user_two_create,530, 340)
        self.fix.put(self.user_two_login,530,370)
        self.fix.put(self.user_two_logout, 530, 400)
        self.fix.put(self.user_two_stats, 530, 430)

        # Title
        self.fix.put(title,330,100)

        self.window.connect("destroy", self.close)

        # Signals for when buttons are clicked

        self.user_one_create.connect("clicked", self.add_user, self.user_one_entry, self.user_one_password)
        self.user_two_create.connect("clicked", self.add_user, self.user_two_entry, self.user_two_password)

        self.user_one_login.connect("clicked", self.login_user, self.user_one_entry,self.user_one_password, self.user_two_entry, 1)
        self.user_two_login.connect("clicked", self.login_user, self.user_two_entry, self.user_two_password, self.user_one_entry, 2)

        self.user_one_logout.connect("clicked", self.logout_user, self.user_one_verified, self.user_one_logout, self.user_one_stats, self.user_one_create, self.user_one_login, self.play_button, self.head_to_head, self.user_one_entry, self.user_one_password)
        self.user_two_logout.connect("clicked", self.logout_user, self.user_two_verified, self.user_two_logout, self.user_two_stats, self.user_two_create, self.user_two_login, self.play_button, self.head_to_head, self.user_two_entry, self.user_two_password)

        self.user_one_stats.connect("clicked", self.personal_stats, self.user_one_entry)
        self.user_two_stats.connect("clicked", self.personal_stats, self.user_two_entry)

        self.head_to_head.connect("clicked", self.view_head, self.user_one_entry, self.user_two_entry)
        top_ten.connect("clicked", self.view_top_ten)

        self.settings.connect("clicked", self.set_settings)
        self.play_button.connect("clicked", self.start_game)

        # Creating warning label for password
        self.warning = gtk.Label()

        self.fix.put(self.warning, 330,400)
        self.window.add(self.fix)
        self.window.show_all()

        # Creating warning window right before the game is about to start
        self.start_game_window = gtk.Window()
        self.start_game_window.set_default_size(300,100)
        self.start_game_window.set_title("Tron")
        self.start_game_window.set_position(gtk.WIN_POS_CENTER)

        # Creating settings window
        self.settings_window = gtk.Window()
        self.settings_window.set_default_size(300, 300)
        self.settings_window.set_title("Settings")
        self.settings_window.set_position(gtk.WIN_POS_CENTER)

        # Creating stats window
        self.stats_window = gtk.Window()
        self.stats_window.set_default_size(100, 100)
        self.stats_window.set_title("Statistics")
        self.stats_window.set_position(gtk.WIN_POS_CENTER)

        # Creating Head-to-Head window
        self.head_to_head_window = gtk.Window()
        self.head_to_head_window.set_default_size(200, 100)
        self.head_to_head_window.set_title("Head-To-Head")
        self.head_to_head_window.set_position(gtk.WIN_POS_CENTER)

        # Creating top 10 window
        self.top_ten_window = gtk.Window()
        self.top_ten_window.set_default_size(300, 300)
        self.top_ten_window.set_title("Top 10")
        self.top_ten_window.set_position(gtk.WIN_POS_CENTER)

    def login_user(self, widget, username_field, password_field, other_username, current_user):
        """
        This function logs a user in and allows for the user to view their own personal statistics
        @param widget: The login button that was clicked
        @param username_field: The username text field
        @param password_field: The password text field
        @param other_username: The second user
        @param current_user: The first user
        @return: Nothing
        """
        # reinitialize the warning text
        self.warning.set_text("")

        # get the user's input for username and password
        # also get the other user's input username as to not log in twice with same username
        username = username_field.get_text()
        other_user = other_username.get_text()
        password = password_field.get_text()

        # set user verified to false initially
        user_verified = False

        # search through the csv file self.filename
        # if the username and password match, the user has been verified!
        # set user verified to true
        with open(self.filename, 'r+') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if username == row[0] and password == row[1]:
                    user_verified = True

        # if the current user is trying to log in as user 1
        if current_user == 1:

            # if user 2 has already logged in and has logged in under the same username, return an error as
            # to not log in twice with the same username
            if self.user_two_verified == True and other_user == username:
                    self.warning.set_markup('<span color="red">User already logged in</span>')
                    self.user_one_verified = False
                    self.user_one_password.set_text("")

            else:
                # if the user has been verified, print success message and make logout & view personal stats visible and
                # create an account & login insensitive so users understand that they are logged in.
                if user_verified == True:
                    self.warning.set_markup('<span color="dark green">User is verified</span>')
                    self.user_one_verified=True
                    self.user_one_logout.set_sensitive(True)
                    self.user_one_stats.set_sensitive(True)
                    self.user_one_create.set_sensitive(False)
                    self.user_one_login.set_sensitive(False)

                # Otherwise, print an error message: the user has failed to log in.
                if user_verified == False:
                    self.warning.set_markup('<span color="red">Wrong username or password</span>')
                    self.user_one_verified = False
                    self.user_one_password.set_text("")

        # repeat the step above, but as user 2 instead.
        if current_user == 2:

            if self.user_one_verified == True and other_user == username:
                    self.warning.set_markup('<span color="red">User already logged in</span>')
                    self.user_two_verified = False
                    self.user_two_password.set_text("")

            else:
                 if user_verified == True:
                    self.warning.set_markup('<span color="dark green">User is verified</span>')
                    self.user_two_verified = True
                    self.user_two_logout.set_sensitive(True)
                    self.user_two_stats.set_sensitive(True)
                    self.user_two_create.set_sensitive(False)
                    self.user_two_login.set_sensitive(False)

                 if user_verified == False:
                    self.warning.set_markup('<span color="red">Wrong username or password</span>')
                    self.user_two_verified = False
                    self.user_two_password.set_text("")

        # Finally, if both users are successfully logged in, make play, head-to-head score and settings sensitive.
        if self.user_one_verified == True and self.user_two_verified == True:
            self.play_button.set_sensitive(True)
            self.head_to_head.set_sensitive(True)
            self.settings.set_sensitive(True)

    def logout_user(self, widget, verified_user, logout_button, stats_button, create_button, login_button, play_button, head_button, username_entry, password_entry):
        """
       This function logs out a user and grays out buttons to not allow certain actions when two users are logged in
       @param widget:The logout button that was pressed
       @param verified_user: The user that logs out after log out
       @param logout_button: The logout button that will be grayed out after log out
       @param stats_button: The personal stats button that will be grayed out
       @param create_button: The create button that will be clickable after log out
       @param login_button: The login button that will be clickable after log out
       @param play_button: The play button that will be grayed out after log out
       @param head_button: The head to head button that will be grayed out after log out
       @param username_entry: The username text field that will be blank after log out
       @param password_entry: The password text field that will be blank after log out
       @return: Nothing
       """
        # set variable to False, user is no longer verified
        verifiedUser = False

        # change the available buttons back to the login view
        logout_button.set_sensitive(False)
        stats_button.set_sensitive(False)
        create_button.set_sensitive(True)
        login_button.set_sensitive(True)
        play_button.set_sensitive(False)
        head_button.set_sensitive(False)
        self.settings.set_sensitive(False)

        # delete the user information from the input
        username_entry.set_text("")
        password_entry.set_text("")

        # Resetting settings. Map will be plain as default and speed will be slow: 80 for refresh rate
        self.option = 0
        self.refresh = 80

        # display a success message
        self.warning.set_markup('<span color="dark green">Successfully logged out</span>')

    # Create an account function.
    # Checks if the username and password is in the correct format.
    # Also checks if the username is not already taken
    # Returns True if an account is created
    def add_user(self,widget,username_field, password_field):
        """
        This function adds a user to the database
        @param widget: The create account button was clicked
        @param username_field: The username field
        @param password_field: The password field
        @return: Nothing
        """
        # clear warning
        self.warning.set_text("")

        # prepare pop-up window
        wrong_input_prompt = gtk.MessageDialog(type=gtk.MESSAGE_INFO,buttons=gtk.BUTTONS_NONE, flags=0)
        wrong_input_prompt.set_position(gtk.WIN_POS_CENTER)
        wrong_input_prompt.label.set_selectable(False)


        # assigns the Entry widgets to us and pw
        us = username_field
        pw = password_field

        # open a csv file in append mode: if it doesnt exist, create it. if it exists, write to the end of the file
        write_info = csv.writer(open(self.filename,'a+'))

        # get the user input from the Entry widgets (get the desired username and password)
        username = us.get_text()
        password = pw.get_text()

        # assume username is not taken and making an account is possible
        self.username_taken = False
        self.make_account = True

        # look through the csv file to check if the username already exists
        with open(self.filename, 'r+') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                for field in row:
                    if field == username:
                        # print error message
                        self.warning.set_markup('<span color="red">Username already exists</span>')
                        # set username as taken, cannot make an account
                        self.username_taken = True

        # if the username isn't taken, check the username and password for the correct format
        if self.username_taken == False:
            make_account = True
            ascii = [chr(c) for c in range(128)]
            for character in username:
                if not character in ascii:
                    wrong_input_prompt.set_markup("Username must contain only ASCII characters")
                    wrong_input_prompt.show()
                    self.make_account = False

            # password must be 8 characters long
            if (len(password)<8):
                wrong_input_prompt.set_markup("Password must be at least eight characters long and contain one digit, one lowercase character, one uppercase character and at least one non-alphanumeric character.")
                wrong_input_prompt.show()
                self.make_account=False

            # password must have at least one digit
            elif not any(char.isdigit() for char in password):
                wrong_input_prompt.set_markup("Password must be at least eight characters long and contain one digit, one lowercase character, one uppercase character and at least one non-alphanumeric character.")
                wrong_input_prompt.show()
                self.make_account = False
            #password must have at least one lowercase
            elif not any(char.islower() for char in password):
                wrong_input_prompt.set_markup("Password must be at least eight characters long and contain one digit, one lowercase character, one uppercase character and at least one non-alphanumeric character.")
                wrong_input_prompt.show()
                self.make_account = False
            #password must have at least one uppercase
            elif not any(char.isupper() for char in password):
                wrong_input_prompt.set_markup("Password must be at least eight characters long and contain one digit, one lowercase character, one uppercase character and at least one non-alphanumeric character.")
                wrong_input_prompt.show()
                self.make_account = False
            #password must contain at learn one non-alphanumeric character
            elif password.isalnum():
                wrong_input_prompt.set_markup("Password must be at least eight characters long and contain one digit, one lowercase character, one uppercase character and at least one non-alphanumeric character.")
                wrong_input_prompt.show()
                self.make_account = False

        # since the username isn't taken and the username and password follow the correct format, make the account!
        if self.username_taken == False and self.make_account == True:
                # write information to csv user file, in append mode
                write_info.writerow([username,password])
                # display success to user
                self.warning.set_markup('<span color="dark green">Account successfully created</span>')

                # If we want to delete the password entry to make the user type in his password again
                # Prof doesn't like this feature
                # pw.set_text("")
                return True

    def start_game(self, widget):
        """
        This function opens up a new window and prompts the users to start the game.
        @param widget: The play game button that was clicked
        @return: Nothing
        """

        play_message = gtk.Label(self.user_one_entry.get_text()+" is RED | "+self.user_two_entry.get_text()+" is PINK ")
        start_button = gtk.Button()
        start_button.set_label("Start Game!")
        start_button.set_size_request(120, 30)
        start_button.connect("clicked", self.play)

        fix_two = gtk.Fixed()
        fix_two.put(start_button, 90, 50)
        fix_two.put(play_message, 25, 20)
        self.start_game_window.add(fix_two)
        self.start_game_window.show_all()

    def play(self,widget):
        """
        This function opens the game frame and starts the Tron game.
        @param widget: The start game button was pressed
        @return: Nothing
        """
        self.start_game_window.destroy()
        game_frame = GameFrame(750, 500, self.user_one_entry.get_text(), self.user_two_entry.get_text(), self.option, self.refresh)
        game_frame.run()

    def view_top_ten(self, widget):  # Top 10
        """
        This function opens up a new window to display the top ten players who have the most wins
        @param widget: The top ten button was clicked
        @return: Nothing
        """
        database = {}  # Creating dictionary to store top ten users who have the most wins
        f = open(self.filename_score, 'r')
        reader = csv.reader(f)
        for row in reader:
            if int(row[1]) not in database:
                database[int(row[1])] = list()
            key = int(row[1]) # key of dictionary will be number of wins
            value = row[0] # value of dictionary will be a list of user names
            database[key].append(value)
        database = OrderedDict(sorted(database.items(), key = lambda t: t[0]))
        columns = ["Position", "User", "Wins"]
        self.wins = []
        self.user_names = []
        users = 0
        for key in database:
            self.wins.append(key)
            self.user_names.append(database[key])
            users = users +1
        list_model = gtk.ListStore(int, str, int)
        z = 0
        w = len(self.wins)
        counter = 0
        for listing in reversed(self.user_names): # Looping through wins and username arrays to match
            w -= 1
            for y in (listing):
                if counter == 10:
                    break
                counter += 1
                row = [z+1,"" + y, self.wins[w]]
                list_model.append(row)
                z += 1

        view = gtk.TreeView(model=list_model)
        # for each column
        for i in range(len(columns)):
            # cell renderer to render the text
            cell = gtk.CellRendererText()
            col = gtk.TreeViewColumn(columns[i], cell, text=i)
            view.append_column(col)
        grid = gtk.Table(rows=1, columns=1, homogeneous=True) # Creating table format to display top 10
        grid.attach(view, 0, 1, 0, 1)
        self.top_ten_window.add(grid)
        self.top_ten_window.show_all()

    def view_head(self, widget, user_one, user_two): # Head to head
        """
        This function opens up a new window to display head to head stats between the two users logged in
        @param widget: The head to head button that was clicked
        @param user_one: User one who is logged in
        @param user_two: User two who is logged in
        @return: Nothing
        """
        # Getting usernames
        username_one = user_one.get_text()
        username_two = user_two.get_text()
        f = open(self.filename_versus, 'r') # Opening file to get data
        self.player_one_wins = ""
        self.player_two_wins = ""
        self.player_ties = ""
        reader = csv.reader(f)
        for row in reader:
            if row[0] == username_one and row[1] == username_two:
                self.player_one_wins = row[2] # Within csv file, 1st column is the number of games won by player 1
                self.player_ties = row[3] # Within csv file, 2nd column is the number of ties
                self.player_two_wins = str(Decimal(row[4])-Decimal(row[3])-Decimal(row[2])) # Within csv file, 3rd column is the number of games won by player 2
        columns = [username_one, " Vs",username_two, "Ties"] # Column names
        row = [self.player_one_wins, "   -", self.player_two_wins, self.player_ties]
        list_model = gtk.ListStore(str, str, str, str)
        list_model.append(row)
        view = gtk.TreeView(model=list_model)
        for i in range(len(columns)):
            cell = gtk.CellRendererText()
            # the column is created
            col = gtk.TreeViewColumn(columns[i], cell, text=i)
            # and it is appended to the treeview
            view.append_column(col)
        grid = gtk.Table(rows=1, columns=1, homogeneous=True) # Creating table format to display stats
        grid.attach(view, 0, 1, 0, 1)
        self.head_to_head_window.add(grid)
        self.head_to_head_window.show_all()

    def personal_stats(self, widget, user): # Retrieving personal stats of the logged in user
        """
        This function opens up a new window and display the personal stats of the current user logged in
        @param widget: The view personal stats button that was clicked
        @param user: The logged in user who wants to view their own stats
        @return: Nothing
        """
        username = user.get_text() # Getting username to know what info to retrieve from database
        f = open(self.filename_score, 'r')
        self.wins = ""
        self.losses = ""
        self.ties = ""
        self.games = ""
        reader = csv.reader(f)
        for row in reader:
            if row[0] == username:
                self.wins = row[1] # Within the csv file, the 2nd column contains the number of wins
                self.losses = row[2] # Within the csv file, the 3rd column contains the number of losses
                self.ties = row[3] # Within the csv file, the 4th column contains the number of ties
                self.games = row[4] # Within the csv file, the 5th column contains the number of games played by the user
        columns = ["User", "Wins","Losses", "Ties", "Number of Matches"]
        row = [username, self.wins, self.losses, self.ties, self.games]
        list_model = gtk.ListStore(str, str, str, str, str)
        list_model.append(row)
        view = gtk.TreeView(model=list_model)
        for i in range(len(columns)):
            cell = gtk.CellRendererText()
            # the column is created
            col = gtk.TreeViewColumn(columns[i], cell, text=i)
            # and it is appended to the treeview
            view.append_column(col)
        grid = gtk.Table(rows=1, columns=1, homogeneous=True) # Creating table format to display stats
        grid.attach(view, 0, 1, 0, 1)
        self.stats_window.add(grid)
        self.stats_window.show_all()

    def set_settings(self, widget):
        """
        This function allows the user to change the settings of the game. Settings include game speed and map selection
        @param widget: The settings button that was clicked
        @return: Nothing
        """
        # Creating Settings title
        title = gtk.Label("Settings")
        title.set_size_request(100,50)

        # Creating label to display message: Pick your map
        pick_map = gtk.Label("Pick your map:")
        pick_map.set_size_request(100, 50)

        # Creating label to display message: Pick your speed
        pick_speed = gtk.Label("Pick your speed:")
        pick_speed.set_size_request(125, 50)

        # Creating selection box for the different maps
        self.map_selection = gtk.combo_box_new_text()
        self.map_selection.append_text('Plain')
        self.map_selection.append_text('2-Box')
        self.map_selection.append_text('3-Box')
        self.map_selection.connect("changed", self.changed_map) # Event signaller when selection is changed

        # Creating selection box for the different speeds
        self.speed_box = gtk.combo_box_new_text()
        self.speed_box.append_text('Slow')
        self.speed_box.append_text('Medium')
        self.speed_box.append_text('Fast')
        self.speed_box.connect("changed", self.changed_speed)

        # Creating apply button to apply settings set
        apply = gtk.Button()
        apply.set_label("Apply")
        apply.connect("clicked", self.apply_clicked)

        fix_settings = gtk.Fixed()

        fix_settings.put(title, 100, 10)
        fix_settings.put(pick_map, 20, 120)
        fix_settings.put(self.map_selection, 140, 130)
        fix_settings.put(pick_speed, 12, 160)
        fix_settings.put(self.speed_box, 140, 170)
        fix_settings.put(apply, 130, 240)

        self.settings_window.add(fix_settings)
        self.settings_window.show_all()

    def apply_clicked(self, widget):
        """
        This function closes the settings window after the apply button is clicked so the new settings are the applied
        @param widget: The apply button was clicked
        @return: Nothing
        """
#        # Closing the settings window and settings were saved when clicked
        self.settings_window.destroy()

    def changed_map(self, combobox):
        """
        This function changes the map of the game
        @param combobox: The drop down box that holds the three map selections
        @return: Nothing
        """
        if self.map_selection.get_active_text()=="Plain":
            self.option = 0
        if self.map_selection.get_active_text()=="2-Box":
            self.option = 1
        if self.map_selection.get_active_text()=="3-Box":
            self.option = 2

    def changed_speed(self, combobox):
        """
        This function changes the speed of the game
        @param combobox: The drop down box that will hold the three speeds
        @return: Nothing
        """
        if self.speed_box.get_active_text()=="Slow":
            self.refresh = 80
        if self.speed_box.get_active_text()=="Medium":
            self.refresh = 40
        if self.speed_box.get_active_text()=="Fast":
            self.refresh = 20

    def close(self, widget):
        """
        This closes the game window
        @param widget: The current game window that is open
        @return: Nothing
        """
        gtk.main_quit()
