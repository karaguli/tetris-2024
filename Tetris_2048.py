import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.picture import Picture  # used for displaying images
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid # the class for modeling the game grid
from tetromino import Tetromino # the class for modeling the tetrominoes
import random # used for creating tetrominoes with random types/shapes
import numpy as np


class Game:
    # MAIN FUNCTION OF THE PROGRAM
    # -------------------------------------------------------------------------------
    # Main function where this program starts execution
    def start(self):
        # set the dimensions of the game grid
        grid_h, grid_w = 20, 20
        game_w = 12
        # set the size of the drawing canvas
        canvas_h, canvas_w = 40 * grid_h, 40 * grid_w
        stddraw.setCanvasSize(canvas_w, canvas_h)
        # set the scale of the coordinate system
        stddraw.setXscale(-0.5, grid_w - 0.5)
        stddraw.setYscale(-0.5, grid_h - 0.5)

        # creates a blank list to keep following 10 tetrominos
        self.tetrominos = list()
        # keeps the round count of the game
        self.round_count = 0
        # creates 10 tetrominos and assigns them inside the self.tetrominos array
        self.create_tetromino(grid_h, game_w)

        # keeps the next tetromino information
        self.next_type = self.tetrominos[self.round_count + 1]
        # moves the next tetromino rightside area to show the player
        self.next_type.get_cell_position(15, 15)

        # create the game grid
        grid = GameGrid(grid_h, grid_w)
        # create the first tetromino to enter the game grid
        # by using the create_tetromino function defined below
        current_tetromino = self.tetrominos[self.round_count]
        grid.current_tetromino = current_tetromino

        # keeps information if the game restarted
        self.restart = False
        # keeps information if the game paused
        self.is_paused = False
        # keeps information if the game finished
        self.is_finished = False
        self.game_over = False

        # display a simple menu before opening the game
        # by using the display_game_menu function defined below
        self.display_game_menu(grid_h, grid_w, grid)

        # the main game loop (keyboard interaction for moving the tetromino)
        while True:
            # gives following tetromino to GameGrid class to draw it on the screen
            grid.set_next(self.tetrominos[self.round_count + 1])
            # checks if the user paused the game using the button
            if stddraw.mousePressed():
                if stddraw.mouseX() <= 10.5 + 0.6 and stddraw.mouseX() >= 10.5 - 0.6:
                    if stddraw.mouseY() <= 18.5 + 0.6 and stddraw.mouseY() >= 10.8 - 0.6:
                        self.is_paused = True
                        print("Stopped")
                        self.display_game_menu(grid_h, grid_w, grid)

            # check user interactions via the keyboard
            if stddraw.hasNextKeyTyped(): # check if the user has pressed a key
                key_typed = stddraw.nextKeyTyped() # the most recently pressed key
                # if the left arrow key has been pressed
                if key_typed == "left":
                    # move the active tetromino left by one
                    current_tetromino.move(key_typed, grid)
                # if the right arrow key has been pressed
                elif key_typed == "right":
                    # move the active tetromino right by one
                    current_tetromino.move(key_typed, grid)
                # if the down arrow key has been pressed
                elif key_typed == "down":
                    # move the active tetromino down by one
                    # (soft drop: causes the tetromino to fall down faster)
                    current_tetromino.move(key_typed, grid)
                # if the up arrow key has been pressed
                elif key_typed == "up":
                    # rotate the tetromino
                    current_tetromino.rotation(grid, current_tetromino)
                # if the space key has been pressed
                elif key_typed == "space":
                    # hard drop tetromino
                    current_tetromino.hard_drop(grid, current_tetromino)
                # if the 'p' key has been pressed
                elif key_typed == "p":
                    print("Paused")
                    # pauses the game
                    self.is_paused = not self.is_paused
                    self.display_game_menu(grid_h, grid_w, grid)

                # clear the queue of the pressed keys for a smoother interaction
                stddraw.clearKeysTyped()

            # if game is not paused move down the tetromino
            if not self.is_paused:
                # move the active tetromino down by one at each iteration (auto fall)
                success = current_tetromino.move("down", grid)

            # place the active tetromino on the grid when it cannot go down anymore
            if not success:
                # get the tile matrix of the tetromino
                tiles_to_lock = current_tetromino.tile_matrix
                # update the game grid by locking the tiles of the landed tetromino
                self.game_over = grid.update_grid(tiles_to_lock)

                # merges available tiles until there is no tile to merge
                merge = self.check_merging(grid)
                while merge:
                    merge = self.check_merging(grid)

                # keeps row information if they are filled or not
                row_count = self.is_full(grid_h, grid_w, grid)
                index = 0
                # slides down the rows
                while index < grid_h:
                    while row_count[index]:
                        self.slide_down(row_count, grid)
                        row_count = self.is_full(grid_h, grid_w, grid)
                    index += 1

                # assigns labels to each tile using 4-component labeling
                labels, num_labels = self.linked_component_labeling(grid.tile_matrix, grid_w, grid_h)
                free_tiles = [[False for v in range(grid_w)] for b in range(grid_h)]
                free_tiles, num_free = self.find_free_tiles(grid_h, grid_w, labels, free_tiles)
                # dropdowns each tile that is not connected to the other ones
                grid.move_free_tiles(free_tiles)

                # drops down tiles that don't connect to any other tiles until there is no tile to drop down
                while num_free != 0:
                    labels, num_labels = self.linked_component_labeling(grid.tile_matrix, grid_w, grid_h)
                    free_tiles = [[False for v in range(grid_w)] for b in range(grid_h)]
                    free_tiles, num_free = self.find_free_tiles(grid_h, grid_w, labels, free_tiles)
                    grid.move_free_tiles(free_tiles)

                labels, num_labels = self.linked_component_labeling(grid.tile_matrix, grid_w, grid_h)
                merge = self.check_merging(grid)
                while merge:
                    merge = self.check_merging(grid)

                row_count = self.is_full(grid_h, grid_w, grid)
                index = 0

                while index < grid_h:
                    while row_count[index]:
                        self.slide_down(row_count, grid)
                        row_count = self.is_full(grid_h, grid_w, grid)
                    index += 1

                # assigns labels to each tile using 4-component labeling
                labels, num_labels = self.linked_component_labeling(grid.tile_matrix, grid_w, grid_h)
                free_tiles = [[False for v in range(grid_w)] for b in range(grid_h)]
                free_tiles, num_free = self.find_free_tiles(grid_h, grid_w, labels, free_tiles)
                grid.move_free_tiles(free_tiles)

                # drops down tiles that don't connect any other tiles until there is no tile to drop down
                while num_free != 0:
                    labels, num_labels = self.linked_component_labeling(grid.tile_matrix, grid_w, grid_h)
                    free_tiles = [[False for v in range(grid_w)] for b in range(grid_h)]
                    free_tiles, num_free = self.find_free_tiles(grid_h, grid_w, labels, free_tiles)
                    # Drop downs the each tile which is not connected the other ones
                    grid.move_free_tiles(free_tiles)

                labels, num_labels = self.linked_component_labeling(grid.tile_matrix, grid_w, grid_h)

                # end the main game loop if the game is over
                if self.game_over:
                    # print a message on the console when the game is over
                    print("Game Over")
                    self.is_finished = True
                    # Displays a menu to restart
                    self.display_game_menu(grid_h, grid_w, grid)

                # create the next tetromino to enter the game grid
                # by using the create_tetromino function defined below
                self.round_count += 1

                # determines the current tetromino and gives it to GameGrid
                current_tetromino = self.tetrominos[self.round_count]
                grid.current_tetromino = current_tetromino
                # calculates a random position for following current tetromino
                new_x, new_y = random.randint(2, 9), 21
                current_tetromino.get_cell_position(new_x, new_y)

                # resets the list and fill it with new tetrominos
                if self.round_count == 8:
                    self.tetrominos = list()
                    self.round_count = 0
                    self.create_tetromino(grid_h, game_w)
                # determines the next tetromino and moves it to rightside
                self.next_type = self.tetrominos[self.round_count+1]
                self.next_type.get_cell_position(15, 15)

            # if player restarted the game, each place is filled with NoneType object
            if self.restart:
                for a in range(0, 20):
                    for b in range(12):
                        grid.tile_matrix[a][b] = None
                self.restart = False
                grid.game_over = False
                current_tetromino = self.tetrominos[self.round_count]
                grid.current_tetromino = current_tetromino
                new_x, new_y = random.randint(2, 9), 22
                current_tetromino.get_cell_position(new_x, new_y)

            # display the game grid and as well the current tetromino
            grid.display()

    # Method checks if there is any available tile to merge
    # Merges available tiles and increases the score
    def check_merging(self, grid):
        # keeps if the merge operation performed
        merged = False
        for a in range(0, 19):
            for b in range(12):
                # checks if there is a tile above the tile in the a,b
                if grid.tile_matrix[a][b] is not None and grid.tile_matrix[a + 1][b] is not None:
                    # checks if two tiles numbers are equal
                    if grid.tile_matrix[a][b].number == grid.tile_matrix[a + 1][b].number:
                        # deletes the above tile from tile matrix
                        grid.tile_matrix[a + 1][b].set_position(None)
                        grid.tile_matrix[a + 1][b] = None
                        # updates the number of below tile
                        grid.tile_matrix[a][b].number += grid.tile_matrix[a][b].number
                        # updates the total score by new number of the tile
                        grid.score += grid.tile_matrix[a][b].number
                        # used for changing game speed by score
                        grid.last_updated += grid.tile_matrix[a][b].number
                        # calls necessary function to change tile color by it's number
                        grid.tile_matrix[a][b].update_color(grid.tile_matrix[a][b].number)
                        merged = True
        return merged

    # Method checks each row if they are completely filled with tiles and returns each row in an array
    # If row is completely filled it takes True value, else False
    def is_full(self, grid_h, grid_w, grid):
        # creates an array with full of False, array size is equal to number of rows in the game grid
        row_count = [False for i in range(grid_h)]
        # if a row is full, this score variable keeps total score which will come from this full row
        score = 0
        for h in range(grid_h):
            # keeps total number of tiles inside the same row, if counter == 12, row is full
            counter = 0
            for w in range(grid_w):
                if grid.is_occupied(h, w):
                    counter += 1
                # if row is full, calculates total score in this row
                if counter == 12:
                    score = 0
                    for a in range(12):
                        score += grid.tile_matrix[h][a].number
                    row_count[h] = True
        # updating total score
        grid.score += score
        # used for changing game speed by score
        grid.last_updated += score
        return row_count

    # Method downs each tile by one unit if it is available
    def slide_down(self, row_count, grid):
        for index, i in enumerate(row_count):
            if i:
                for a in range(index, 19):
                    row = np.copy(grid.tile_matrix[a + 1])
                    grid.tile_matrix[a] = row
                    for b in range(12):
                        if grid.tile_matrix[a][b] is not None:
                            grid.tile_matrix[a][b].move(0, -1)
                break

    # Function for creating random shaped tetrominoes to enter the game grid
    def create_tetromino(self, grid_height, grid_width):
        self.rotated = False
        # type (shape) of the tetromino is determined randomly
        tetromino_types = ['I', 'O', 'Z', 'J', 'L', 'T', 'S']
        for i in range(10):
            random_index = random.randint(0, len(tetromino_types) - 1)
            self.random_type = tetromino_types[random_index]
            # create and return the tetromino
            tetromino = Tetromino(self.random_type, grid_height, grid_width)
            self.tetrominos.append(tetromino)
        return self.tetrominos

    # Function for displaying a simple menu before starting the game
    def display_game_menu(self, grid_height, grid_width, grid):
        # colors used for the menu
        background_color = Color(0, 10, 26)
        button_color = Color(10, 222, 150)
        text_color = Color(0, 10, 26)
        # clear the background canvas to background_color
        stddraw.clear(background_color)
        # get the directory in which this python code file is placed
        current_dir = os.path.dirname(os.path.realpath(__file__))
        # path of the image file
        img_file = current_dir + "/images/menu_image.png"
        # center coordinates to display the image
        img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
        # image is represented using the Picture class
        image_to_display = Picture(img_file)
        # display the image
        stddraw.picture(image_to_display, img_center_x, img_center_y)
        # dimensions of the start game button
        button_w, button_h = grid_width - 1.5, 2
        # coordinates of the bottom left corner of the start game button
        button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
        # display the start game button as a filled rectangle
        stddraw.setPenColor(button_color)
        stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
        # display the text on the start game button
        stddraw.setFontFamily("Arial")
        stddraw.setFontSize(25)
        stddraw.setPenColor(text_color)

        # checks if game is paused with user
        if not self.is_finished and self.is_paused:
            stddraw.setPenColor(button_color)
            button2_blc_x, button2_blc_y = img_center_x - button_w / 2, 1
            stddraw.filledRectangle(button_blc_x, button_blc_y - 3, button_w, button_h)
            stddraw.setFontFamily("Arial")
            stddraw.setFontSize(25)
            stddraw.setPenColor(text_color)

            text_to_display = "Continue"
            stddraw.text(img_center_x, 5, text_to_display)

            text1_to_display = "Restart"
            stddraw.text(img_center_x, 2, text1_to_display)
            # displays restart-continue buttons
            while True:
                # display the menu and wait for a short time (50 ms)
                stddraw.show(50)
                # check if the mouse has been left-clicked on the button
                if stddraw.mousePressed():
                    # get the x and y coordinates of the location at which the mouse has
                    # most recently been left-clicked
                    mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
                    # check if these coordinates are inside the button
                    if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
                        if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
                            self.is_paused = False
                            break # break the loop to end the method and start the game
                        # restarts the game
                        elif mouse_y >= button2_blc_y and mouse_y <= button2_blc_y + button_h:
                            self.is_paused = False
                            grid.score = 0
                            self.restart = True
                            grid.speed_increased_counter = 0
                            # allows user to choice game speed
                            self.speed_screen(grid, background_color, grid_width, grid_height, img_file, button_color)
                            break
        # if game is finished, allows user to restart game
        elif self.is_finished:
            stddraw.setPenColor(Color(255, 23, 30))
            stddraw.text(img_center_x, 8, "Game Over")
            stddraw.setPenColor(text_color)
            text1_to_display = "Restart"
            stddraw.text(img_center_x, 5, text1_to_display)
            while True:
                # display the menu and wait for a short time (50 ms)
                stddraw.show(50)
                # check if the mouse has been left-clicked on the button
                if stddraw.mousePressed():
                    # get the x and y coordinates of the location at which the mouse has
                    # most recently been left-clicked
                    mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
                    if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
                        if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
                            self.restart = True
                            grid.speed_increased_counter = 0
                            self.is_paused = False
                            self.is_finished = False
                            self.game_over = False
                            # resets the score
                            grid.score = 0

                            # allows user to choice game speed
                            self.speed_screen(grid, background_color, grid_width, grid_height, img_file, button_color)
                            break
        else:
            text1_to_display = "Start the Game"
            stddraw.text(img_center_x, 5, text1_to_display)
            # menu interaction loop
            while True:
                # display the menu and wait for a short time (50 ms)
                stddraw.show(50)
                # check if the mouse has been left-clicked
                if stddraw.mousePressed():
                    # get the x and y coordinates of the location at which the mouse has
                    # most recently been left-clicked
                    mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
                    if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
                        if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
                            text1_to_display = "Start Game"
                            stddraw.text(img_center_x, 5, text1_to_display)
                            break
            # colors used for the menu
            self.speed_screen(grid, background_color, grid_width, grid_height, img_file, button_color)


    # Method shows new screen to choice game speed
    def speed_screen(self, grid, background_color, grid_width, grid_height, img_file, button_color):
        stddraw.clear(background_color)
        # center coordinates to display the image
        img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
        # image is represented using the Picture class
        image_to_display = Picture(img_file)
        # display the image
        stddraw.picture(image_to_display, img_center_x, img_center_y)
        # dimensions of the start game button
        button_w, button_h = grid_width - 17, 2
        stddraw.setPenColor(button_color)
        # coordinates of the bottom left corner of the start game button
        button1_blc_x, button1_blc_y = img_center_x - button_w / 2, 4
        button2_blc_x, button2_blc_y = button1_blc_x - 5, 4
        button3_blc_x, button3_blc_y = button1_blc_x + 5, 4
        # display the start game button as a filled rectangle
        stddraw.filledRectangle(button1_blc_x, button1_blc_y, button_w, button_h)
        stddraw.filledRectangle(button2_blc_x, button2_blc_y, button_w, button_h)
        stddraw.filledRectangle(button3_blc_x, button3_blc_y, button_w, button_h)
        stddraw.setPenColor(Color(0, 10, 26))

        fast_speed_text = "Slow"
        stddraw.text(img_center_x - 5, 5, fast_speed_text)

        normal_speed_text = "Normal"
        stddraw.text(img_center_x, 5, normal_speed_text)

        text_to_display = "Fast"
        stddraw.text(img_center_x + 5, 5, text_to_display)

        while True:
            # display the menu and wait for a short time (50 ms)
            stddraw.show(50)
            # check if the mouse has been left-clicked
            if stddraw.mousePressed():
                # get the x and y coordinates of the location at which the mouse has
                # most recently been left-clicked
                mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()

                # Draws a frame per 200ms
                if mouse_x >= button2_blc_x and mouse_x <= button2_blc_x + button_w:
                    if mouse_y >= button2_blc_y and mouse_y <= button2_blc_y + button_h:
                        print("Slow speed")
                        grid.game_speed = 250
                        break

                # Draws a frame per 175ms
                if mouse_x >= button1_blc_x and mouse_x <= button1_blc_x + button_w:
                    if mouse_y >= button1_blc_y and mouse_y <= button1_blc_y + button_h:
                        print("Normal speed")
                        grid.game_speed = 175
                        break

                # Draws a frame per 150ms
                if mouse_x >= button3_blc_x and mouse_x <= button3_blc_x + button_w:
                    if mouse_y >= button3_blc_y and mouse_y <= button3_blc_y + button_h:
                        print("Fast speed")
                        grid.game_speed = 120
                        break

    def linked_component_labeling(self, grid, grid_w, grid_h):
        # initially all the pixels in the image are labeled as 0 (background)
        labels = np.zeros([grid_h, grid_w], dtype=int)
        # min_equivalent_labels list is used to store min equivalent label for each label
        min_eq_labels = []
        # labeling starts with 1 (as 0 is considered as the background of the image)
        current_label = 1
        # first pass to assign initial labels and determine minimum equivalent labels
        # from conflicts for each pixel in the given binary image
        for y in range(grid_h):
            for x in range(grid_w):
                if grid[y, x] is None:
                    continue
                # get the set of neighboring labels for this pixel
                # using get_neighbor_labels function defined below
                neighbor_labels = self.get_neighbor_labels(labels, (x, y))
                # if all the neighbor pixels are background pixels
                if len(neighbor_labels) == 0:
                    # assign current_label as the label of this pixel
                    # and increase current_label by 1
                    labels[y, x] = current_label
                    current_label += 1
                    # initially the minimum equivalent label is the label itself
                    min_eq_labels.append(labels[y, x])
                # if there is at least one non-background neighbor
                else:
                    # assign minimum neighbor label as the label of this pixel
                    labels[y, x] = min(neighbor_labels)
                    # a conflict occurs if there are multiple (different) neighbor labels
                    if len(neighbor_labels) > 1:
                        labels_to_merge = set()
                        # add min equivalent label for each neighbor to labels_to_merge set
                        for l in neighbor_labels:
                            labels_to_merge.add(min_eq_labels[l - 1])
                        # update minimum equivalent labels related to this conflict
                        # using update_equivalent_labels function defined below
                        self.update_min_eq_labels(min_eq_labels, labels_to_merge)
        # second pass to rearrange equivalent labels so they all have consecutive values
        # starting from 1 and assign min equivalent label of each pixel as its own label
        # rearrange min equivalent labels using rearrange_min_equivalent_labels function
        self.rearrange_min_eq_labels(min_eq_labels)
        # for each pixel in the given binary image
        for y in range(grid_h):
            for x in range(grid_w):
                # get the value of the pixel
                if grid[y, x] is None:
                    continue
                # assign minimum equivalent label of each pixel as its own label
                labels[y, x] = min_eq_labels[labels[y, x] - 1]
        # return the labels matrix and the number of different labels
        return labels, len(set(min_eq_labels))

    # Function for getting labels of the neighbors of a given pixel
    def get_neighbor_labels(self, label_values, pixel_indices):
        x, y = pixel_indices
        # using a set to store different neighbor labels without any duplicates
        neighbor_labels = set()
        # add upper pixel to the set if the current pixel is not in the first row of the
        # image and its value is not zero (not a background pixel)
        if y != 0:
            u = label_values[y - 1, x]
            if u != 0:
                neighbor_labels.add(u)
        # add left pixel to the set if the current pixel is not in the first column of
        # the image and its value is not zero (not a background pixel)
        if x != 0:
            l = label_values[y, x - 1]
            if l != 0:
                neighbor_labels.add(l)
        # return the set of neighbor labels
        return neighbor_labels

    # Function for updating min equivalent labels by merging conflicting neighbor labels
    # as the smallest value among their min equivalent labels
    def update_min_eq_labels(self, all_min_eq_labels, min_eq_labels_to_merge):
        # find the min value among conflicting neighbor labels
        min_value = min(min_eq_labels_to_merge)
        # for each minimum equivalent label
        for index in range(len(all_min_eq_labels)):
            # if its value is in min_eq_labels_to_merge
            if all_min_eq_labels[index] in min_eq_labels_to_merge:
                # update its value as the min_value
                all_min_eq_labels[index] = min_value

    # Function for rearranging min equivalent labels so they all have consecutive values
    # starting from 1
    def rearrange_min_eq_labels(self, min_eq_labels):
        # find different values of min equivalent labels and sort them in increasing order
        different_labels = set(min_eq_labels)
        different_labels_sorted = sorted(different_labels)
        # create an array for storing new (consecutive) values for min equivalent labels
        new_labels = np.zeros(max(min_eq_labels) + 1, dtype=int)
        count = 1  # first label value to assign
        # for each different label value (sorted in increasing order)
        for l in different_labels_sorted:
            # determine the new label
            new_labels[l] = count
            count += 1  # increase count by 1 so that new label values are consecutive
        # assign new values of each minimum equivalent label
        for ind in range(len(min_eq_labels)):
            old_label = min_eq_labels[ind]
            new_label = new_labels[old_label]
            min_eq_labels[ind] = new_label

    # Method finds each tiles which does not connect any others
    def find_free_tiles(self, grid_h, grid_w, labels, free_tiles):
        counter = 0
        okay_labels = []
        for x in range(grid_h):
            for y in range(grid_w):
                if labels[x, y] != 1 and labels[x, y] != 0:
                    if x == 0:
                        okay_labels.append(labels[x, y])
                    if not okay_labels.count(labels[x, y]):
                        free_tiles[x][y] = True
                        counter += 1
        return free_tiles, counter

# start() function is specified as the entry point (main function) from which
# the program starts execution
game = Game()
game.start()