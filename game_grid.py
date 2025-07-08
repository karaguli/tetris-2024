import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.color import Color # used for coloring the game grid
from point import Point  # used for tile positions
import numpy as np  # fundamental Python module for scientific computing
import copy as cp

# Class used for modelling the game grid
# Draws the game screen
class GameGrid:
    # Constructor for creating the game grid based on the given arguments
    def __init__(self, grid_h, grid_w):
        # set the dimensions of the game grid as the given arguments
        self.grid_height = grid_h
        self.grid_width = grid_w
        # create a tile matrix to store the tiles landed onto the game grid
        self.tile_matrix = np.full((grid_h, grid_w), None)
        # create the tetromino that is currently being moved on the game grid
        self.current_tetromino = None
        # the game_over flag shows whether the game is over or not
        self.game_over = False
        # set the color used for the empty grid cells
        self.empty_cell_color = Color(0, 10, 26)
        # set the colors used for the grid lines and the grid boundaries
        self.line_color = Color(31, 28, 105)
        self.boundary_color = Color(28, 15, 69)
        # thickness values used for the grid lines and the grid boundaries
        self.line_thickness = 0.002
        self.box_thickness = 4 * self.line_thickness
        # keeps total score
        self.score = 0

        self.pos = Point()
        # keeps the default value of game speed
        self.game_speed = 250
        # it maintains another score information to update the speed based on the total score.
        self.last_updated = 0
        # keeps number of time speed incread
        self.speed_increased_counter = 0

    # Method used for displaying the game grid
    def display(self):
        # checks if value of last_updated > 500, if yes, increases the game speed
        self.change_speed()
        # clear the background to empty_cell_color
        stddraw.clear(self.empty_cell_color)
        # draw the game grid
        self.draw_grid()
        # draw the current/active tetromino if it is not None (the case when the
        # game grid is updated)
        if self.current_tetromino is not None and self.next_tetromino is not None:
            self.current_tetromino.draw()
            self.next_tetromino.draw()
        # draw a box around the game grid
        self.draw_boundaries()
        # show the resulting drawing with a pause duration = game_speed ms
        stddraw.show(self.game_speed)

    # Method for drawing the cells and the lines of the grid
    def draw_grid(self):
        # for each cell of the game grid
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                # draw the tile if the grid cell is occupied by a tile
                if self.tile_matrix[row][col] is not None:
                    self.tile_matrix[row][col].draw()
        # draw the inner lines of the grid
        stddraw.setPenColor(self.line_color)
        stddraw.setPenRadius(self.line_thickness)
        # x and y ranges for the game grid
        start_x, end_x = -0.5, 12 - 0.5
        start_y, end_y = -0.5, self.grid_height - 0.5
        for x in np.arange(start_x + 1, end_x, 1):  # vertical inner lines
            stddraw.line(x, start_y, x, end_y)
        for y in np.arange(start_y + 1, end_y, 1):  # horizontal inner lines
            stddraw.line(start_x, y, end_x, y)
        stddraw.setPenRadius()  # reset the pen radius to its default value

        # draw the pause button
        stddraw.setPenColor(Color(230, 79, 79))
        stddraw.filledRectangle(18.6, 18.6, 1.5, 1.5)
        stddraw.setPenRadius(100)
        stddraw.setPenColor(Color(255, 255, 255))
        text_to_display = "| |"
        stddraw.text(19.0, 19.0, text_to_display)

        # draw the main score on the top right of the game screen
        self.Score(self.score)
        # displays total number of count how many times the speed increased
        self.display_info("Speed Increased", self.speed_increased_counter)

    # Method for drawing the boundaries around the game grid
    def draw_boundaries(self):
        # draw a bounding box around the game grid as a rectangle
        stddraw.setPenColor(self.boundary_color)  # using boundary_color
        # set the pen radius as box_thickness (half of this thickness is visible
        # for the bounding box as its lines lie on the boundaries of the canvas)
        stddraw.setPenRadius(self.box_thickness)
        # the coordinates of the bottom left corner of the game grid
        pos_x, pos_y = -0.5, -0.5
        stddraw.rectangle(pos_x, pos_y, self.grid_width, self.grid_height)
        stddraw.setPenRadius()  # reset the pen radius to its default value

    # Method used for checking whether the grid cell with given row and column
    # indexes is occupied by a tile or empty
    def is_occupied(self, row, col):
        # considering newly entered tetrominoes to the game grid that may have
        # tiles with position.y >= grid_height
        if not self.is_inside(row, col):
            return False
        # the cell is occupied by a tile if it is not None
        return self.tile_matrix[row][col] is not None

    # Method used for checking whether the cell with given row and column indexes
    # is inside the game grid or not
    def is_inside(self, row, col):
        if row < 0 or row >= self.grid_height:
            return False
        if col < 0 or col >= self.grid_width:
            return False
        return True

    # Method that locks the tiles of the landed tetromino on the game grid while
    # checking if the game is over due to having tiles above the topmost grid row.
    # The method returns True when the game is over and False otherwise.
    def update_grid(self, tiles_to_lock):
        # place all the tiles of the stopped tetromino onto the game grid
        n_rows, n_cols = len(tiles_to_lock), len(tiles_to_lock[0])
        for col in range(n_cols):
            for row in range(n_rows):
                # place each occupied tile onto the game grid
                if tiles_to_lock[row][col] is not None:
                    # compute the position of the tile on the game grid
                    pos = tiles_to_lock[row][col].get_position()
                    if self.is_inside(pos.y, pos.x):
                        self.tile_matrix[pos.y][pos.x] = tiles_to_lock[row][col]
                    # the game is over if any placed tile is out of the game grid
                    else:
                        self.game_over = True
        # return the game_over flag
        return self.game_over

    # Method takes list of free tile, send them one unit down
    def move_free_tiles(self, free_tiles):
        for row in range(self.grid_height):  # excluding the bottommost row
            for col in range(self.grid_width):
                if free_tiles[row][col]:
                    free_tile_copy = cp.deepcopy(self.tile_matrix[row][col])
                    self.tile_matrix[row - 1][col] = free_tile_copy
                    dx, dy = 0, -1  # change of the position in x and y directions
                    self.tile_matrix[row - 1][col].move(dx, dy)
                    self.tile_matrix[row][col] = None

    # Method displays given information text on the screen
    def display_info(self, txt, count):
        stddraw.setPenRadius(150)
        stddraw.setPenColor(Color(255, 255, 255))
        text_to_display = str(txt) + " x " + str(count)
        stddraw.text(15.5, 17.7, text_to_display)
        text_to_display = "NEXT TETROMINO"
        stddraw.text(15.5, 16.5, text_to_display)

    # Method draws the main score on the top right of the main game screen
    def Score(self, score=0):
        stddraw.setPenRadius(150)
        stddraw.setPenColor(Color(255, 255, 255))
        text_to_display = "Score: "+str(score)
        stddraw.text(15.5, 18.8, text_to_display)

    # Method takes following tetromino from Game object rightside
    def set_next(self, next_tetromino):
        self.next_tetromino = next_tetromino

    # Method that increases the game speed according to the total score for each 500 score
    # If game speed < 50, speed does not change
    def change_speed(self):
        if self.last_updated > 500 and self.game_speed >= 50:
            change_rate = int(self.game_speed * 0.05)
            print("Previous Speed", self.game_speed)
            self.game_speed -= change_rate
            print("New Speed", self.game_speed)
            self.speed_increased_counter += 1
            self.last_updated = self.score % 500
