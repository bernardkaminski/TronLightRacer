#!/usr/bin/env python
from decimal import Decimal
import os
import sys
import csv
import gtk
import cairo
import glib


class Obstacle:
    """
    The Obstacle class represents an obstacle within the playing field
    """

    def __init__(self,amount_of_dots_on_screen, image_name):
        """
        This function initializes the Obstacle class, specifying the dimensions of the object

        @param amount_of_dots_on_screen: The dimensions, in pixels, of the object. The amount of space the object will take up
        @param image_name: The name of the image that will represent the object.
        @return: Nothing
        """
        self.x = [0]*amount_of_dots_on_screen
        self.y = [0]*amount_of_dots_on_screen
        self.amount_of_obstacles = 0
        self.image_name = image_name


class Player:
    """
    The Player class is what keeps track of the player in the grid during game play
    """

    def __init__(self, x_starting, y_starting, image_name, dot_size):
        """
        the initialising function for the Player class

        @param x_starting: The starting x position of the player om the grid in pixels(dependant on dot_size)
        @param y_starting: The starting x position of the player om the grid in pixels(dependant on dot_size)
        @param image_name: The name of the image file that will represent the player on the grid
        @param dot_size: The size of the the
        @return: nothing
        """
        self.x = x_starting
        self.y = y_starting
        self.dot_size = dot_size
        self.is_alive = True
        self.image_name = image_name
        self.left = False
        self.right = False
        self.up = True
        self.down = False

    def move(self):
        """
        changes the position of the player based on the variables up, right, down and left
        @return:nothing
        """
        if self.left:
            self.x -= self.dot_size
        if self.right:
            self.x += self.dot_size
        if self.up:
            self.y -= self.dot_size
        if self.down:
            self.y += self.dot_size

    def add_wall(self, obstacle):
        """
        adds coordinate the the obstacle object associated with the player. keeps adding the the tail of the player.
        @param obstacle: the obstacle object associated with the Player
        @return: nothing
        """
        obstacle.x[obstacle.amount_of_obstacles] = self.x
        obstacle.y[obstacle.amount_of_obstacles] = self.y
        obstacle.amount_of_obstacles += 1


class Grid(gtk.DrawingArea):

    """
    The class that does most of the work when it comes to displaying and running the game aspect of the program.
    This class contains the Obstacle and Player classes and keeps track and uses them in order to determine
    the winner of each game and eventually the match.
    """

    # All files needed for writing to the database
    # file that contains the user information
    FILE_NAME_VS = "../res/data/scoreVS.csv"
    # file that the user information will be copied to
    TEMP_NAME_VS = "../res/data/scoreVSTemp.csv"
    FILE_NAME = "../res/data/score.csv"
    TEMP_NAME = "../res/data/scoreTemp.csv"
    PLAYER_IMAGE = "../res/image/head.png"
    PLAYER1_OBSTACLE_IMAGE = "../res/image/square.png"
    PLAYER2_OBSTACLE_IMAGE = "../res/image/square2.png"
    MAP_OBSTACLE_IMAGE = "../res/image/blue.png"

    start_game_window = gtk.Window()
    start_game_window_fixed = gtk.Fixed()
    start_game_window_label = gtk.Label("")
    start_game_window_label.set_size_request(100, 100)
    start_game_message = ""

    MAX_GAME_COUNT = 3
    match_stats = [0]*3
    game_count = 0
    X_PLAYER1_START_POSITION = 0
    Y_PLAYER1_START_POSITION = 500
    X_PLAYER2_START_POSITION = 740
    Y_PLAYER2_START_POSITION = -10

    def __init__(self, grid_width, grid_length,grid_square_size, p1_user_name,p2_user_name, map_option, refresh_rate,
                 parent_frame):
        """
        the initialize function for the grid class sets all necessary variables

        @param grid_width: the width in the grid in pixels
        @param grid_length: the length of the grid in pixels
        @param grid_square_size: the amount length of pixels each square on a grid is
        @param p1_user_name: the user name that will be associated with player 1
        @param p2_user_name: the user name that will be associated with player 2
        @param map_option: the option that decides which map will be displayed(3 options)
        @param refresh_rate: the rate at which the grid redraws the images and move the players in milliseconds
        @param parent_frame: the frame that holds the grid drawing area
        @return:nothing
        """

        super(Grid, self).__init__()  # needed to inherit drawing area methods

        self.parent_frame = parent_frame
        self.refresh_rate = refresh_rate
        self.map_option = map_option
        self.p1_user_name = p1_user_name
        self.p2_user_name = p2_user_name
        self.grid_width = grid_width
        self.grid_length = grid_length
        self.grid_square_size = grid_square_size

        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(0, 0, 0))#set background color
        self.set_size_request(self.grid_width, self.grid_length)#set size
        self.connect("expose-event", self.expose)  # needed to show board

        self.begin = True  # not sure if we need this
        self.cont = True
        self.game_count = 0

        self.amount_of_dots_on_grid = grid_width * grid_length / (grid_square_size*grid_square_size)

        #initializing player objects
        self.player_one = Player(self.X_PLAYER1_START_POSITION, self.Y_PLAYER1_START_POSITION,
                                 self.PLAYER_IMAGE, grid_square_size)
        self.player_two = Player(self.X_PLAYER2_START_POSITION, self.Y_PLAYER2_START_POSITION,
                                 self.PLAYER_IMAGE, grid_square_size)

        #initializing the Obstacle objects 3 needed one for each player and one for the map
        self.p1_obstacle_list = Obstacle(self.amount_of_dots_on_grid, self.PLAYER1_OBSTACLE_IMAGE)
        self.p2_obstacle_list = Obstacle(self.amount_of_dots_on_grid, self.PLAYER2_OBSTACLE_IMAGE)
        self.map_obstacle_list = Obstacle(self.amount_of_dots_on_grid ,self.MAP_OBSTACLE_IMAGE)
        
        if map_option == 1:
            self.add_ob_to_map(15, 20, 25, 30)
            self.add_ob_to_map(50, 20, 60, 30)
        if map_option == 2:
            self.add_ob_to_map(50, 5, 70, 25)
            self.add_ob_to_map(30, 20, 45, 30)
            self.add_ob_to_map(5, 25, 25, 45)

        self.start_game_window.connect("destroy", self.restart)
        start_button = gtk.Button()
        close_button = gtk.Button()
        self.start_game_window.set_default_size(200,100)
        self.start_game_window.set_position(gtk.WIN_POS_CENTER)

        start_button.set_label("next Round!")
        start_button.set_size_request(80, 25)
        start_button.connect("clicked", self.restart)

        close_button.set_label("Quit")
        close_button.set_size_request(80, 25)
        close_button.connect("clicked", self.close)

        self.start_game_window_fixed.put(start_button, 10, 70)
        self.start_game_window_fixed.put(close_button, 110, 70)
        self.start_game_window_fixed.put(self.start_game_window_label, 40, 1)
        self.start_game_window.add(self.start_game_window_fixed)

        self.init_game()  # construct game

    def init_game(self):
        """
        initializes the starting conditions of the game
        @return:nothing
        """
        self.player_one.left = False
        self.player_one.right = False
        self.player_one.up = True
        self.player_one.down = False
        self.player_two.left = False
        self.player_two.right = False
        self.player_two.up = False
        self.player_two.down = True

        try:#load images
            self.head = cairo.ImageSurface.create_from_png(self.player_one.image_name)
            self.dot = cairo.ImageSurface.create_from_png(self.p1_obstacle_list.image_name)
            self.dot2 = cairo.ImageSurface.create_from_png(self.p2_obstacle_list.image_name)
            self.block = cairo.ImageSurface.create_from_png(self.map_obstacle_list.image_name)
        except Exception, e:
            print e.message
            sys.exit(1)

        glib.timeout_add(self.refresh_rate, self.on_timer) # start timer

    def on_timer(self):
        """
        This is the function that is called once per refresh rate.
        It updates the players positions, Obstacle lists and redraws the playing area
        It also checks if a player has one and in the case that a player has won  it stores the information
        in order to store to the database once three rounds have been played

        @return: boolean: true if the timer is to continue false if it is to stop
        """
        if self.game_count < self.MAX_GAME_COUNT and self.cont:
            if self.player_one.is_alive and self.player_two.is_alive:
                self.player_one.move()
                self.player_two.move()
                self.check_collision()
                self.player_one.add_wall(self.p1_obstacle_list)
                self.player_two.add_wall(self.p2_obstacle_list)
                self.queue_draw()
                return True
            else:
                if self.player_one.is_alive and not self.player_two.is_alive:
                    self.match_stats[self.game_count] = "playerOne"
                    self.start_game_message = self.p1_user_name + " won"
                if self.player_two.is_alive and not self.player_one.is_alive:
                    self.match_stats[self.game_count] = "playerTwo"
                    self.start_game_message = self.p2_user_name + " won"
                if not self.player_two.is_alive and not self.player_one.is_alive:
                    self.match_stats[self.game_count] = "tie"
                    self.start_game_message = "    tie"

                self.game_count += 1
                if self.game_count < self.MAX_GAME_COUNT:
                    self.show_start_game_window()
                else:
                    p1_wins = 0
                    p2_wins = 0
                    for stat in self.match_stats:
                        if stat == "playerTwo":
                            p2_wins += 1
                        if stat == "playerOne":
                            p1_wins += 1
                    if p1_wins > p2_wins:
                        self.start_game_message = self.p1_user_name+" won the match"
                         # call the function, in this case user1 won the match and user2 lost
                         # if there is a winner and a loser
                        self.add_score_to_database(self.p1_user_name, self.p2_user_name)
                        self.add_personal(self.p1_user_name, 0)
                        self.add_personal(self.p2_user_name, 1)
                        print "done"
                    if p2_wins > p1_wins:
                        self.start_game_message = self.p2_user_name+"won the match"
                        # call the function, in this case user2 won the match and user1 lost
                        # if there is a winner and a loser
                        self.add_score_to_database(self.p2_user_name, self.p1_user_name)
                        self.add_personal(self.p1_user_name, 1)
                        self.add_personal(self.p2_user_name, 0)
                    if p2_wins == p1_wins:
                        # if the match was a tie
                        self.add_tie_database(self.p1_user_name, self.p2_user_name)
                        self.add_personal(self.p1_user_name, 2)
                        self.add_personal(self.p2_user_name, 2)
                    self.show_end_match_window()
                print(self.game_count)
            print(self.match_stats)
            return False
        return False

    def expose(self, widget, event):
        """
        this is the function that actually draws the images using the gtk library
        @param widget: the widget that the drawing is being done on
        @param event:  the event that starts the drawing
        @return: nothing
        """
        cr = widget.window.cairo_create()
        if self.player_one.is_alive and self.player_two.is_alive:  # if in the game
            w = self.allocation.width
            h = self.allocation.height
            cr.set_source_rgb(0, 0, 0)
            cr.paint()
            for z in range(self.map_obstacle_list.amount_of_obstacles):
                    cr.set_source_surface(self.block,self.map_obstacle_list.x[z],self.map_obstacle_list.y[z])
                    cr.paint()
            for z in range(self.p1_obstacle_list.amount_of_obstacles):
                    cr.set_source_surface(self.dot, self.p1_obstacle_list.x[z], self.p1_obstacle_list.y[z])
                    cr.paint()
            for z in range(self.p2_obstacle_list.amount_of_obstacles):
                    cr.set_source_surface(self.dot2, self.p2_obstacle_list.x[z], self.p2_obstacle_list.y[z])
                    cr.paint()

            cr.set_source_surface(self.head,self.player_one.x,self.player_one.y)
            cr.paint()

            cr.set_source_surface(self.head,self.player_two.x,self.player_two.y)
            cr.paint()

    def check_collision(self):
        """
        this function checks if the players have collided with any obstacles
        @return: nothing
        """

        list_count = self.p1_obstacle_list.amount_of_obstacles
        # if player 1 runs into himself or player 2's tail
        while list_count > 0:
            if self.player_one.x == self.p1_obstacle_list.x[list_count] and self.player_one.y == self.p1_obstacle_list.y[list_count]:
                self.player_one.is_alive = False
            if self.player_two.x == self.p1_obstacle_list.x[list_count] and self.player_two.y == self.p1_obstacle_list.y[list_count]:
                self.player_two.is_alive = False
            list_count = list_count - 1

        list_count = self.p2_obstacle_list.amount_of_obstacles
        # if player one runs into himself
        while list_count > 0:
            if self.player_one.x == self.p2_obstacle_list.x[list_count] and self.player_one.y == self.p2_obstacle_list.y[list_count]:
                #self.inGame = False
                self.player_one.is_alive = False
            if self.player_two.x == self.p2_obstacle_list.x[list_count] and self.player_two.y == self.p2_obstacle_list.y[list_count]:
                #self.inGame = False
                self.player_two.is_alive = False
            list_count = list_count - 1

        list_count=self.map_obstacle_list.amount_of_obstacles
        while list_count> 0:
            if self.player_one.x == self.map_obstacle_list.x[list_count] and self.player_one.y == self.map_obstacle_list.y[list_count]:
                #self.inGame = False
                self.player_one.is_alive = False
            if self.player_two.x == self.map_obstacle_list.x[list_count] and self.player_two.y == self.map_obstacle_list.y[list_count]:
                #self.inGame = False
                self.player_two.is_alive = False
            list_count = list_count - 1

        if self.player_one.y > self.grid_length- self.grid_square_size:
            self.player_one.is_alive = False

        if self.player_one.y < 0:
            self.player_one.is_alive = False

        if self.player_one.x > self.grid_width- self.grid_square_size:
            self.player_one.is_alive = False

        if self.player_one.x < 0:
            self.player_one.is_alive = False

        if self.player_two.y > self.grid_length - self.grid_square_size:
            self.player_two.is_alive = False

        if self.player_two.y < 0:
            self.player_two.is_alive = False

        if self.player_two.x > self.grid_width-self.grid_square_size:
            self.player_two.is_alive = False

        if self.player_two.x < 0:
            self.player_two.is_alive = False

    def on_key_down(self, event):
        """
        this function is an even listener that records what button the users press on the keyboard and reacts
        accordingly by updating the players movements
        @param event: the event that the function is listening for
        @return: nothing
        """

        key = event.keyval

        if key == gtk.keysyms.Left and not self.player_two.right:
            self.player_two.left = True
            self.player_two.up = False
            self.player_two.down = False


        if key == gtk.keysyms.Right and not self.player_two.left:
            self.player_two.right = True
            self.player_two.up = False
            self.player_two.down = False


        if key == gtk.keysyms.Up and not self.player_two.down:
            self.player_two.up = True
            self.player_two.right = False
            self.player_two.left = False


        if key == gtk.keysyms.Down and not self.player_two.up:
            self.player_two.down = True
            self.player_two.right = False
            self.player_two.left = False


        if key == gtk.keysyms.a and not self.player_one.right:
            self.player_one.left = True
            self.player_one.up = False
            self.player_one.down = False


        if key == gtk.keysyms.d and not self.player_one.left:
            self.player_one.right = True
            self.player_one.up = False
            self.player_one.down = False


        if key == gtk.keysyms.w and not self.player_one.down:
            self.player_one.up = True
            self.player_one.right = False
            self.player_one.left = False


        if key == gtk.keysyms.s and not self.player_one.up:
            self.player_one.down = True
            self.player_one.right = False
            self.player_one.left = False

    def show_start_game_window(self):
        """
        sets up and shows the window that prompts the users to start the next round
        @return:nothing
        """
        self.start_game_window_label = gtk.Label(self.start_game_message)
        self.start_game_window_fixed.remove_mnemonic_label(self.start_game_window_label)
        self.start_game_window_fixed.put(self.start_game_window_label , 40, 15)
        self.start_game_window.show_all()

    def show_end_match_window(self):
        """
        shows and sets up the window that tell the users who the winner of the match is and to quit the game window
        @return:nothing
        """
        self.start_game_window_fixed.destroy()
        self.start_game_window_label = gtk.Label(self.start_game_message)
        self.start_game_window_fixed.put(self.start_game_window_label, 40, 15)
        okay_button = gtk.Button()
        okay_button.set_label("Okay")
        okay_button.set_size_request(80, 25)
        okay_button.connect("clicked", self.close)
        self.start_game_window_fixed.put(okay_button, 80, 40)
        self.start_game_window.add(self.start_game_window_fixed)
        self.start_game_window.show_all()

    def restart(self, widget):
        """
        resets all the necessary objects(re-initialize) in order to start a new game
        @param widget: the button that was pressed
        @return:nothing
        """
        self.start_game_window_label.destroy()
        #initializing player objects
        self.player_one = Player(self.X_PLAYER1_START_POSITION, self.Y_PLAYER1_START_POSITION,
                                 self.PLAYER_IMAGE, self.grid_square_size)
        self.player_two = Player(self.X_PLAYER2_START_POSITION, self.Y_PLAYER2_START_POSITION,
                                 self.PLAYER_IMAGE, self.grid_square_size)

        #initializing the Obstacle objects 3 needed one for each player and one for the map
        self.p1_obstacle_list = Obstacle(self.amount_of_dots_on_grid, self.PLAYER1_OBSTACLE_IMAGE)
        self.p2_obstacle_list = Obstacle(self.amount_of_dots_on_grid, self.PLAYER2_OBSTACLE_IMAGE)

        self.start_game_window.hide()
        self.init_game()

    def close(self, widget):
        """
        closes the grid and the parent window
        @param widget: the button that was pressed
        @return:nothing
        """
        self.cont= False
        self.start_game_window.destroy()
        self.parent_frame.destroy()

    def add_ob_to_map(self, x_bottom_left_cord, y_bottom_left_cord, x_top_right_cord, y_top_right_cord):
        """
        creates stores the approriate coordinates of the obstacles that are needed for different maps
        @param x_bottom_left_cord:  bottom left x coordinate of the obstacle
        @param y_bottom_left_cord: bottom left y coordinate of the obstacle
        @param x_top_right_cord: top right x coordinate of the obstacle
        @param y_top_right_cord: top right y coordinate of the obstacle
        @return: nothing
        """
        x_difference = x_top_right_cord-x_bottom_left_cord
        y_difference = y_top_right_cord-y_bottom_left_cord
        x = x_bottom_left_cord*self.grid_square_size
        y = y_bottom_left_cord*self.grid_square_size
        total_dots = (x_difference*y_difference)

        for i in range(0,total_dots):
                self.map_obstacle_list.x[self.map_obstacle_list.amount_of_obstacles] = x
                self.map_obstacle_list.y[self.map_obstacle_list.amount_of_obstacles] = y
                self.map_obstacle_list.amount_of_obstacles += 1
                y = y + self.grid_square_size
                if y == y_top_right_cord*self.grid_square_size:
                    y = y_bottom_left_cord*self.grid_square_size
                    x = x + self.grid_square_size

    def add_score_to_database(self, winning_user, losing_user):
        """
        stores the score between two users in a csv file called scoresVS.csv, if the match was not a tie.
        The csv format is the following:
        user1, user2, wins of user1, ties, total matches
        user2,user1, wins of user2, ties, total matches
        @param winning_user username of the winning user
        @param losing_user username of the losing user

        """
        g = open(self.TEMP_NAME_VS,'w')
        write_info = csv.writer(g,lineterminator='\n')
        added_users = False
        # update appropriate rows, copy the rest
        with open(self.FILE_NAME_VS, 'rU') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if winning_user == row[0] and losing_user == row[1]:
                    write_info.writerow([winning_user,losing_user,Decimal(row[2])+1,row[3],Decimal(row[4])+1])
                    added_users = True
                elif losing_user == row[0] and winning_user == row[1]:
                    write_info.writerow([losing_user,winning_user,row[2],row[3],Decimal(row[4])+1])
                elif row[0] != " ":
                    write_info.writerow([row[0], row[1], row[2], row[3], row[4]])
            if added_users == False:
                write_info.writerow([winning_user, losing_user , 1, 0, 1])
                write_info.writerow([losing_user, winning_user, 0, 0, 1])

            f.close()
            g.close()
            os.remove(self.FILE_NAME_VS)
            os.rename(self.TEMP_NAME_VS, self.FILE_NAME_VS)

    def add_tie_database(self, user1, user2):
        """
        Updated the scores between two users, if the match ended in a tie.
        @param user1: username of user1
        @param user2: username of user2
        """
        #open a temporary file to write to
        g = open(self.TEMP_NAME_VS,'w')
        write_info = csv.writer(g,lineterminator='\n')
        # user has not been added yet
        added_users = False

        # update appropriate rows, copy the rest
        with open(self.FILE_NAME_VS, 'rU') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                # update the ties for user 1 and user 2
                if user1 == row[0] and user2 == row[1]:
                    write_info.writerow([user1, user2,row[2], Decimal(row[3])+1,Decimal(row[4])+1])
                    added_users = True
                elif user2 == row[0] and user1 == row[1]:
                    write_info.writerow([user2, user1, row[2], Decimal(row[3])+1,Decimal(row[4])+1])
                # copy the rest
                else:
                    write_info.writerow([row[0], row[1], row[2], row[3]])
            # if the users have never played against each other, simply initialize to both 1 tie.
            if added_users == False:
                write_info.writerow([user1,user2,0,1,1])
                write_info.writerow([user2,user1,0,1,1])

            #close both files
            f.close()
            g.close()

            #remove the original file
            os.remove(self.FILE_NAME_VS)
            #rename the temporary file to the original file
            os.rename(self.TEMP_NAME_VS, self.FILE_NAME_VS)

    def add_personal(self, user, game):
        """
        Update the user's score in the users.csv database

        @param user: username of user whose score must be updated
        @param game: integer that tells the program if the user has won(0), lost(1), or tied(2) the match.
        """
        # user has not been updated yet
        added_user = False
        # open temporary file to write to
        g = open(self.TEMP_NAME, 'w')
        write_info = csv.writer(g, lineterminator='\n')

        # update appropriate rows, copy the rest
        with open(self.FILE_NAME, 'rU') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                # once the user has been updated, set added_user to true
                # if user won, add 1 to the wins column and 1 to the total matches
                if user == row[0] and game == 0:
                    write_info.writerow([user, Decimal(row[1])+1,row[2],row[3],Decimal(row[4])+1])
                    added_user = True
                # if user lost, add 1 to losses and 1 to total matches
                elif user == row[0] and game == 1:
                    write_info.writerow([user,row[1],Decimal(row[2])+1,row[3],Decimal(row[4])+1])
                    added_user = True
                # if match is a tie, add 1 to ties and 1 to total matches
                elif user == row[0] and game == 2:
                    write_info.writerow([user,row[1],row[2],Decimal(row[3])+1,Decimal(row[4])+1])
                    added_user = True
                # copy the other rows
                elif user != row[0]:
                    write_info.writerow([row[0],row[1],row[2],row[3],row[4]])
            # if the user hasn't played any matches before
            # add new row to the file, according to the game integer
            if added_user == False:
                if game == 0:
                    write_info.writerow([user,1,0,0,1])
                if game ==1 :
                    write_info.writerow([user,0,1,0,1])
                if game ==2:
                    write_info.writerow([user,0,0,1,1])

            # close both files
            f.close()
            g.close()

            # remove original file
            os.remove(self.FILE_NAME)

            # rename the temporary file to the original file
            os.rename(self.TEMP_NAME, self.FILE_NAME)


class GameFrame(gtk.Window):
    """
    this class is the window that holds the grid object that displays the game
    """

    dot_size = 10

    def __init__(self, width, height, user1, user2, option, refresh):
        """

        @param width: width of window
        @param height: height of the window
        @param user1: first user that will be playing
        @param user2: second user that will be playing
        @param option: the map option that will be passed to the grid class
        @param refresh: the refresh rate that will be sent to the grid class
        @return:nothing
        """
        super(GameFrame, self).__init__()
        self.set_title('Tron')
        self.set_size_request(width, height)
        self.set_resizable(True)
        self.set_position(gtk.WIN_POS_CENTER)
        player1 = user1
        player2 = user2
        self.grid = Grid(width, height, self.dot_size, player1, player2, option,refresh, self)

        self.connect("key-press-event", self.on_key_down)
        self.add(self.grid)

    def run(self):
        """
        shows the window
        @return: nothing
        """
        self.show_all()

    def on_key_down(self, widget, event):
        """
        starts the key down event for the grid class
        @param widget: the widget that called on the function
        @param event: the event of a key being pressed
        @return:nothing
        """
        key = event.keyval
        self.grid.on_key_down(event)
