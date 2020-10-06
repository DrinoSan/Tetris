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
        self.width = self.getWidth(self.shape)[0]
        self.shapeStartX = self.getWidth(self.shape)[1]
        self.shapeEndX = self.getWidth(self.shape)[2]
        self.height = len(shape)  # TODO Calculate the correct height

    def getWidth(self, shape):
        startVal = 1000
        endVal = 0
        for e in shape:
            for idx, val in enumerate(e):
                if val == "x" and idx < startVal:
                    startVal = idx
            for idx, val in enumerate(e):
                if val == "." and idx > endVal:
                    endVal = idx
                if val == "x" and idx == e.index(val):
                    endVal = len(shape[0])
                    break

        idx = idx+1
        width = endVal - startVal
        return [width, startVal, endVal]

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
                self.rotationCheck(
                    current_block, self.board_width, self.board_height)
                if self.is_rotation_valid(current_block) == True:
                    pass
                # TODO noch eine weiter abfrage um zu sehen ob die rotation erlaubt ist ansonsten wird die rotation zur�ckgesetzt
            if keys[K_e]:
                current_block.right_rotation(
                    self.block_list[current_block.name])
                self.rotationCheck(
                    current_block, self.board_width, self.board_height)
            if keys[K_LEFT]:
                if self.is_block_on_valid_position(current_block, -1, 0):
                    current_block.x -= 1
            if keys[K_RIGHT]:
                if self.is_block_on_valid_position(current_block, 1, 0):
                    current_block.x += 1
            if keys[K_DOWN]:
                current_block.y += 1
            if keys[K_p]:
                self.pauseGame()

            self.is_block_on_valid_position(current_block, 1, 1)
            if self.is_block_on_bottom(current_block) == True:
                self.draw_block_bottom(current_block)
                current_block = next_block
                next_block = self.get_new_block()

            if self.check_collision(current_block) == True:
                self.add_block_to_board(current_block)
                current_block = next_block
                next_block = self.get_new_block()
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

    def rotationCheck(self, block, width, height):
        while block.x < 0 or block.x + block.width > width or block.y < 0:
            if block.x < 0:
                block.x += 1
            if block.x + block.width > width:
                block.x -= 1

            if block.y < 0:
                block.y += 1

    def is_rotation_valid(self, block):
        pass
        # Check if Coordinate given is on board (returns True/False)

    def is_block_on_bottom(self, block):
        return (True if block.y + block.height == self.board_height else False)

    def is_coordinate_on_board(self, block, x_change, y_change):
        return (True if block.x + x_change >= 0 and block.y + y_change + block.height >= 0 and block.x + x_change + block.width <= self.board_width and block.y + y_change + block.height <= self.board_height else False)

        # Parameters block, x_change (any movement done in X direction), yChange (movement in Y direction)
        # Returns True if no part of the block is outside the Board or collides with another Block

    def is_block_on_valid_position(self, block, x_change=0, y_change=0):
        if self.is_coordinate_on_board(block, x_change, y_change) == True:
            return True
        else:
            False

    # TODO check if block is on valid position after change in x or y direction
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

    def draw_block_bottom(self, block):
        block_idx_range = [*range(block.x, (block.x + block.width), 1)]

        j = 0
        while j < block.height:
            for idx, _ in enumerate(self.gameboard[block.height]):
                if idx in block_idx_range:
                    i = 0
                    while i < block.width:
                        if block.shape[j][i] == "x":
                            self.gameboard[block.y+j][block.x+i] = block.color
                        i += 1
            j += 1

    def check_collision(self, block):
        block_idx_range = [*range(block.x, (block.x + block.width), 1)]
        block_idx_y_range = [*range(block.y, block.y + block.height, 1)]
        print("WERTE VON Y AM BOARD: ", block_idx_y_range)
        print("Werte von X am BOARD; ", block_idx_range)
        for idx_of_Block_in_Y, val_in_y in enumerate(block_idx_y_range):
            print(idx_of_Block_in_Y, "   ", val_in_y)
            for idx_of_Block_in_X, val_in_x in enumerate(block_idx_range):
                print(idx_of_Block_in_X, "    ", val_in_x)
                print()
                if (block.shape[block_idx_y_range.index(val_in_y)][block_idx_range.index(val_in_x)] == "x" and
                        self.gameboard[val_in_y+1][val_in_x] != "."):
                    return True

    def add_block_to_board(self, block):
        # TODO once block is not falling, place it on the gameboard
        #  add Block to the designated Location on the board once it stopped moving
        block_idx_range = [*range(block.x, (block.x + block.width), 1)]
        j = 0
        while j < block.height:
            for idx, _ in enumerate(self.gameboard[block.y + j]):
                if idx in block_idx_range:
                    i = 0
                    while i < block.width:
                        if block.shape[j][i] == "x":
                            self.gameboard[block.y+j][block.x+i] = block.color
                        i += 1
            j += 1

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
