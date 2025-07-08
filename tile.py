import lib.stddraw as stddraw # the stddraw module is used as a basic graphics library
from lib.color import Color # used for coloring the tile and the number on it
from point import Point # used for representing the position of the tile
import copy as cp # the copy module is used for copying tile positions
import math # math module that provides mathematical functions
import numpy as np

# Class used for representing numbered tiles as in 2048
class Tile:
   # Class attributes shared among all Tile objects

   boundary_thickness = 0.004
   font_family, font_size = "Arial", 14

   # Constructor that creates a tile at a given position with 2 as its number
   def __init__(self, position = Point(0, 0)): # (0, 0) is the default position
      # Assigns the random number of the tile 2 or 4 for initial
      numbers = [2, 4]
      # Sets a background color for each possible number
      self.colors = [Color(255, 223, 11), Color(255, 190, 11), Color(251,110,7), Color(251,86,7), Color(255,23,30),
                Color(255,43,172), Color(154,56,236), Color(79,68,227), Color(58,134,255), Color(10,222,150), Color(86,250,0), Color(4,250,0)]
      self.num = int(np.random.choice(numbers, 1))
      self.number = self.num
      # set the colors of the tile
      self.background_color = self.colors[int(math.log2(self.num))-1] # background (tile) color
      self.foreground_color = Color(0, 0, 0) # foreground (number) color
      self.box_color = Color(0, 0, 0) # boundary (box) color
      # set the position of the tile as the given position
      self.position = Point(position.x, position.y)

   # Method for drawing the tile
   def draw(self, position = None, length = 1):
      if position is None:
          position = self.position
      # draw the tile as a filled square
      stddraw.setPenColor(self.background_color)
      stddraw.filledSquare(self.position.x, self.position.y, length / 2)
      # draw the bounding box around the tile as a square
      stddraw.setPenColor(self.box_color)
      stddraw.setPenRadius(Tile.boundary_thickness)
      stddraw.square(self.position.x, self.position.y, length / 2)
      stddraw.setPenRadius() # reset the pen radius to its default value
      # draw the number on the tile
      stddraw.setPenColor(self.foreground_color)
      stddraw.setFontFamily(Tile.font_family)
      stddraw.setFontSize(Tile.font_size)
      stddraw.boldText(self.position.x, self.position.y, str(self.number))

   # Method updates the background of the tile according to tile's number
   def update_color(self, num):
      self.background_color = self.colors[int(math.log2(num)) - 1]

   # Setter method for the position of the tile
   def set_position(self, position):
      # set the position of the tile as the given position
      self.position = cp.copy(position)

   # Getter method for the position of the tile
   def get_position(self):
      # return the position of the tile
      return cp.copy(self.position)

   # Method for moving the tile by dx along the x axis and by dy along the y axis
   def move(self, dx, dy):
      self.position.translate(dx, dy)