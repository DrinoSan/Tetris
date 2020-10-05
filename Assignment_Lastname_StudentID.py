# Tetris - DYOA Advanced at TU Graz WS 2020
# Name:       Sandrino Becirbegovic
# Student ID: 01414464

import pygame
import sys
import time
import random
from pygame.locals import *
from framework import BaseGame

# Recommended Start: init function of Block Class


class Block:
    blocknames = [
        "clevelandZ",
        "rhodeIslandZ",
        "blueRicky",
        "smashBoy",
        "orangeRicky",
        "teewee",
        "hero",
    ]

    def __init__(self, game, block_name):
        self.name = block_name  # TODO set name / Can be 'hero', 'teewee', ...
        # TODO randomize rotation (e.g. 0, 1, 2, 3; Hint: different number of rotations per block)
        self.rotation = random.randint(0, len(game.block_list[self.name]) - 1)
        self.set_shape(game.block_list[self.name][self.rotation])
        self.x = int(game.board_width / 2) - int(self.width / 2)
        self.y = 0
        # "purple"  # TODO Set Color correctly / Can be 'red', 'green', ... (see self.blockColors)
        self.color = game.block_colors[self.name]
        self.maxBlockRot = len(game.block_list[self.name]) - 1

    def set_shape(self, shape):
        self.shape = shape
        # max(ele.count("x") for ele in shape)
        self.width = self.getWidth(self.shape)
        self.height = len(shape)  # TODO Calculate the correct height

    def getWidth(self, shape):
        startVal = 0
        endVal = 0
        for e in shape:
            for idx, val in enumerate(e):
                print(idx, " ", val)
                if val != "x" and idx < startVal:
                    startVal = idx
                if val == "." and idx > endVal:
                    endVal = idx
                else:
                    endVal = len(e) - 1
        endVal += 1
        width = endVal - startVal
        return width

    def right_rotation(self, rotation_options):
        try:
            self.rotation += 1
            self.set_shape(rotation_options[self.rotation])
        except IndexError:
            self.rotation = 0
            self.set_shape(rotation_options[self.rotation])

    def left_rotation(self, rotation_options):
        try:
            self.rotation -= 1
            self.set_shape(rotation_options[self.rotation])
        except IndexError:
            self.rotation = self.maxBlockRot
            self.set_shape(rotation_options[self.rotation])
            print(self.rotation)


class Game(BaseGame):
    pygame.init()
#############################

    def pauseGame(self):
        while True:
            key = pygame.key.get_pressed()
            if key[K_p]:
                return

    def run_game(self):
        self.board = self.get_empty_board()
        fall_time = time.time()

        current_block = self.get_new_block()
        next_block = self.get_new_block()

        # TODO Fill in the score dictionary
        #  Maps "lines removed" to "raw points gained"
        #  0 lines: 0 points; 1 line: 40 points; 2 lines: 100 points; 3 lines: 300 points; 4 lines: 1200 points
        self.score_dictionary = {0: 0, 1: 40, 2: 100, 3: 300, 4: 1200}

        # GameLoop
        while True:
            self.test_quit_game()
            # TODO Game Logic: implement key events & move blocks (Hint: check if move is valid/block is on the Board)

            # Main event loop
#            for event in pygame.event.get():
#                if event.type == pygame.QUIT:
#                    pygame.quit()
#                    exit()

            # print(event)

            keys = pygame.key.get_pressed()
            if keys[K_q]:
                current_block.left_rotation(
                    self.block_list[current_block.name])
                print(current_block.width)
            if keys[K_e]:
                current_block.right_rotation(
                    self.block_list[current_block.name])
            if keys[K_LEFT]:
                self.is_block_on_valid_position(
                    current_block, -1, current_block.y)
                current_block.x -= 1
            if keys[K_RIGHT]:
                self.is_block_on_valid_position(
                    current_block, 1, current_block.y)
                current_block.x += 1
            if keys[K_DOWN]:
                current_block.y += 3
            if keys[K_p]:
                print(current_block.width)
                self.pauseGame()

            # speed

            # Draw after game logic
            self.display.fill(self.background)
            self.draw_game_board()
            self.draw_score()
            self.draw_next_block(next_block)
            if current_block != None:
                self.draw_block(current_block)
            pygame.display.update()
            self.set_game_speed(self.speed)
            self.clock.tick(self.speed)

    # Check if Coordinate given is on board (returns True/False)
    def is_coordinate_on_board(self, x, y):
        # TODO check if coordinate is on playingboard (in boundary of self.boardWidth and self.boardHeight)
        return (True if x >= 0 and y >= 0 and x <= self.board_width and y <= self.board_height else False)

    # Parameters block, x_change (any movement done in X direction), yChange (movement in Y direction)
    # Returns True if no part of the block is outside the Board or collides with another Block
    def is_block_on_valid_position(self, block, x_change=0, y_change=0):
        try:
            for i in range(len(self.gameboard[block.y])-1):
                print("BlockX = ", block.x)
                print("el: ", i)
                if self.gameboard[block.y][i] == block.x and self.gameboard[block.y][i] != self.blank_color:
                    while j < block.width:
                        if self.gameboard[current_block.height + 1][block.x + j] != self.blank_color:
                            print("CRASHHHHHHHHHHHHHHHH with Block")
                if block.x + x_change < 0:
                    block.x -= x_change
                    print("LINKS")
                if block.x + block.width + x_change > self.board_width:
                    block.x -= x_change
                    print("Rechts")

        except IndexError:
            block.y = 0
        # TODO check if block is on valid position after change in x or y direction
        # Check if the line on y Coordinate is complete
        # Returns True if the line is complete

    def check_line_complete(self, y_coord):
        # TODO check if line on yCoord is complete and can be removed
        return True if all(e != self.blank_color for e in self.gameboard[y_coord]) else False

    # Go over all lines and remove those, which are complete
    # Returns Number of complete lines removed
    def remove_complete_line(self):
        removedLine = 0
        # TODO go over all lines and check if one can be removed
        for i in range(self.board_height):
            if self.check_line_complete(i):
                removedLine += 1
        self.calculate_new_score(removedLine, self.level)
        return removedLine

    # Create a new random block
    # Returns the newly created Block Class

    def get_new_block(self):
        # TODO make block choice random! (Use random.choice out of the list of blocks) see blocknames array
        blockname = random.choice(Block.blocknames)
        block = Block(self, blockname)
        return block

    def add_block_to_board(self, block):
        # TODO once block is not falling, place it on the gameboard
        #  add Block to the designated Location on the board once it stopped moving
        i = 0
        while i < block.width:
            self.gameboard[block.y][block.x+i] = block.color
            i += 1

    def calculate_new_score(self, lines_removed, level):  # TODO calculate new score
        # Points gained: Points per line removed at once times the level modifier!
        # Points per lines removed corresponds to the score_directory
        # The level modifier is 1 higher than the current level.
        levelModifier = level+1
        pointsPerLine = self.score_dictionary[lines_removed]
        pointsGained = pointsPerLine * levelModifier
        self.score += pointsGained

    # TODO calculate new level
    def calculate_new_level(self, score):
        if score % 300 == 0:
            self.level = int(score / 300)
        return self.level
    # set the current game speed

    def set_game_speed(self, speed):
        # TODO set the correct game speed!
        # It starts as defined in base.py and should increase by 1 after a level up.
        if self.calculate_new_level(self.score) < self.calculate_new_level(self.score):
            self.speed += 1
        else:
            self.speed = speed

# -------------------------------------------------------------------------------------
# Do not modify the code below, your implementation should be done above
# -------------------------------------------------------------------------------------


def main():
    pygame.init()
    game = Game()

    game.display = pygame.display.set_mode(
        (game.window_width, game.window_height))
    game.clock = pygame.time.Clock()
    pygame.display.set_caption("Tetris")

    game.show_text("Tetris")

    game.run_game()
    game.show_text("Game Over")


if __name__ == "__main__":
    main()
