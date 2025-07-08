# Tetris-2024

ABSTRACT

This report will detail the design and implementation of the second project. Which is creating a challenging hybrid of two classic games one being Tetris and the other being 2048. The game is titled “Tetris 2048”. Players must manipulate falling tetrominoes in order to align them in ways that they will merge inspired by the tile combination mechanics of the game 2048 while being true to the rules of Tetris at the same time. Python was used in the development of the project. The development process consisted of creating and implementing responsive controls for manipulating tetromino shapes just like in Tetris, the conditions were also put in order to end the game when it was needed the most important thing being the merging of tiles that truly combines two games into one. The game does enhance strategic and fast thinking as in a player must always plan their tile placements and plan them under time constraints. In this report, the reader will see an overview of the given project and our solution to it.

ABOUT THE PROJECT

The project also named “Tetris 2048” is truly an innovative project that merges the core of both games Tetris and 2048. Tetris is a true classic and an all-time favorite. Merging this game with 2048 creates a beautiful hybrid game. In this fusion, a complex and engaging puzzle game is created. The goal of the game is to manipulate the sequence of falling geometric shapes called tetrominoes. The game comprises seven tetromino shapes, which are represented by the letters "O", "I", "S", "Z", "L", "J", and "T". All of the tetromino shapes are made with 4 number of tiles. They form a complete line on the game grid and merge with each other taking moves from both games yet again. Because of this, each tetromino carries tiles that are marked with numbers, numbers that are similar to the ones in the 2048 game. The score of this game is determined by two actions of the game physics. The counter counts the number on the full lines and counts the merged tiles’ numbers. The game ends when the grid fills up and there’s no room to place more tetrominoes. After which they will be returned to the opening screen. At this point, the user may choose to restart the game at a preferred speed. The choice of Python language in development is due to its simplicity and effectiveness in rapid game development. Moving on to the key features of this project, the first thing that comes to mind is its hybrid nature, we are creating a game that has never been created before we are required to ensure that our game will follow the rules of both games and provide the functionality that the two games has in a combined one game package. But we’re also tasked with implementing additional features that will create a better experience like a scoring system or adaptive difficulty. All in all, it can be said that the project aims to challenge the student to create something that has never been created before, using the creativity and technical skills of the student it makes the student create a unique game and improve upon that game with additional features.

ABOUT OUR SOLUTION

To start creating this type of project firstly we had to start by researching both games and understanding how they are played, their rules, and their strategies. Since we understand both basics, we wanted to combine them and create this new game out of it. We have established the functionalities that we are gonna implement in this project of ours whilst taking our base code as a reference and building up on it. We also had a rubric that had given us what we needed to implement and what was expected of us which worked as a checklist for us. We have carefully worked on different parts of our code implementing these functionalities one by one at a time and eventually, they all stacked up to become a complete project with all the functionalities we’ve wanted to implement. Now let’s talk about these functionalities and the classes that we have added to our code with some screenshots for better understanding.


class Game: def start(): We made some additions to the base code in this function, which is the main function of the program. The main addition we made is keyboard and mouse interaction to move the tetromino. Here, we assigned tasks to the right, left, and down keys, as well as the up, 'p', and space keys. Rotation is done by pressing the up key, hard drop is done by the space key, and pause is done by using 'p' and mouse interaction. We also added auxiliary functions to ensure that our additions work properly.

o def check_merging(): Method checks if there is any available tile to merge. Merges available tiles and increases the score.

o def is_full(): The method checks each row if they are completely filled with tiles and returns each row in an array. If the row is completely filled it takes a True value, else False.

o def slide_down(): Method downs each tile by one unit if it is available.

o def display_game_menu(): In this method, we added the menu of the pause screen and the menu at the end of the game, in addition to the menu given in the base code.

o def speed_screen(): The method shows a new screen to select the game speed. There are three options on this screen: slow, normal, and fast.

o def linked_component_labeling(): The method labels connected components in a grid, ensuring each component has a unique identifier, useful for managing block interactions in grid-based games.

o def get_neighbor_labels(): Function for getting labels of the neighbors of a given pixel.

o def update_min_eq_labels(): Function for updating min equivalent labels by merging conflicting neighbor labels as the smallest value among their min equivalent labels.

o def rearrange_min_eq_labels(): Function for rearranging min equivalent labels so they all have consecutive values starting from 1.

o def find_free_tiles(): The method finds each tile that does not connect any others.

class GameGrid: o def draw_grid(): In this method, we generally used the base code, but the change we made in the start_x, end_x = -0.5, 12 - 0.5 section enabled us to split the game screen and wrote information about the game on the right side. We also created the stop button in this method.

o def move_free_tiles(): The method takes a list of free tiles and sends them one unit down.

o def display_info(): The method displays the given information text on the screen.

o def Score(): The method draws the main score on the top right of the main game screen.

o def set_next(): The method takes the following tetromino from the Game object's right side.

o def change_speed(): Method that increases the game speed according to the total score for each 500 score. If the game speed is < 50, the speed does not change.

class Tile: o def init(): In this method, we made additions to the base code given to us. We set and applied a separate background color for each number and set the boundary colors.

o def update_color(): This method updates the background of the tile according to the tile's number.

o def set_position(): The setter method for the position of the tile.

o def get_position(): The getter method for the position of the tile.

o def move(): This method is for moving the tile by dx along the x-axis and by dy along the y-axis

class Tetromino: o def init(): In addition to the shapes in the base code, we added other shapes requested from us and found in the Tetris game to this method.

o def rotation(): Method rotates tetrominos clockwise. Copies tile matrix array to avoid losing data and move each tile on the original array using (x,y) = (y, n - 1 -x).

o def hard_drop(): Method to make hard drop. This method basically places the active tetromino immediately on the lowest available tile.
