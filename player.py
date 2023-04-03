from board import Direction, Rotation, Action
from random import Random
from exceptions import NoBlockException
import time

class Player:
    def choose_action(self, board):
        raise NotImplementedError

class MyPlayer(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)
        self.prev_score = 0


    def get_column_height(self,cloned_board):
        column_heights = [0,0,0,0,0,0,0,0,0,0]
        for x in range(cloned_board.width):
            for y in range(cloned_board.height,0,-1):
                if (x,y) in cloned_board.cells:
                    column_heights[x] = cloned_board.height-y
        return column_heights


    def avg_height(self,cloned_board):
        column_heights = self.get_column_height(cloned_board)
        avg_height = sum(column_heights)/len(column_heights)
        return avg_height



    def get_bumpiness(self, cloned_board):
        bumpiness = 0
        column_heights = self.get_column_height(cloned_board)
        for x in range(cloned_board.width -1):
            if column_heights[x] > column_heights[x+1]:
                bumpiness += column_heights[x] - column_heights[x+1]
            else:
                bumpiness += column_heights[x+1] - column_heights[x]
        return bumpiness



    def get_blocks_above_holes(self, cloned_board): #blocks above holes
        blocks_above_holes = 0
        for x, y in cloned_board.cells:
            flag = True
            count_y = 1
            while flag==True:
                if ((x,y + count_y) not in cloned_board.cells) and (count_y+y!=24):
                    blocks_above_holes+=1
                    count_y+=1
                else:
                    flag = False
        return blocks_above_holes



    def get_holes(self, cloned_board):
        holes = 0
        board_cells = list(cloned_board.cells) + [(10, i) for i in range(24)] + [(i, 24) for i in range(20)] + [(i, -1) for i in range(10)] + [(-1, i) for i in range(24)]
        for x in range(10):
            for y in range(24):
                if (x, y) not in board_cells:
                    if (x+1, y) in board_cells and (x-1, y) in board_cells and (x, y+1) in board_cells and (x, y-1) in board_cells:
                        holes+=1
        return holes

    

    def score_board(self, board):
        score_change = board.score - self.prev_score
        blocks_above_holes = self.get_blocks_above_holes(board)
        bumpiness = self.get_bumpiness(board)
        avg_height = self.avg_height(board)
        # max_height = max(self.get_column_height(board))
        holes = self.get_holes(board)
        # if score_change > 1500:
        #     score = bumpiness* -0.8 + holes*-3.9+  blocks_above_holes*-3.6 + avg_height*-1.6 + score_change*2
        # elif score_change > 300:
        #     score = bumpiness* -1.1 + holes*-3.9+  blocks_above_holes*-4.6 + avg_height*-2.6 + score_change*0.4
        # elif score_change > 90:
        #     score = bumpiness* -1.16 + holes*-3.9+  blocks_above_holes*-4.9 + avg_height*-2.6 + score_change*-0.1
        # elif score_change > 24:
        #     score = bumpiness* -2.8 + holes*-4.9+  blocks_above_holes*-5.2 + avg_height*-3.6 + score_change*-0.3
        # else:
        #     score = bumpiness* -3.1+ holes*-8.9+  blocks_above_holes*-7.2 + avg_height*-4.6 + score_change*-0.5
        score = bumpiness* -220 + holes*-780+  blocks_above_holes*-720 + avg_height*120
        return score



    def move_to_target(self, board, cloned_board, t_pos, t_rot):
        for i in range(0, t_rot):
            try:
                cloned_board.rotate(Rotation.Anticlockwise)
            except NoBlockException:
                pass
        left_of_shape = board.falling.left
        while t_pos != left_of_shape:
            if t_pos < left_of_shape:
                try:
                    left_of_shape -= 1
                    cloned_board.move(Direction.Left)
                except NoBlockException:
                    pass
            elif t_pos > left_of_shape:
                left_of_shape += 1
                try:
                    cloned_board.move(Direction.Right)
                except NoBlockException:
                    pass
        try:
            cloned_board.move(Direction.Drop)
        except NoBlockException:
            pass


    def make_best_move(self, board, best_pos, best_rot):
        moves = []
        # Specific rotation
        for i in range(best_rot):
            moves.append(Rotation.Anticlockwise)

        curr_pos = board.falling.left
        while best_pos != curr_pos:

            if best_pos < curr_pos:
                curr_pos -= 1
                moves.append(Direction.Left)

            elif best_pos > curr_pos:
                curr_pos += 1
                moves.append(Direction.Right)

        moves.append(Direction.Drop)

        return moves


    def choose_action(self, board):
        best_score = -100000
        self.prev_score = board.score
        for t_pos in range(board.width):
            for t_rot in range(4):
                clone_board = board.clone()
                self.move_to_target(board, clone_board, t_pos, t_rot)
                score = self.score_board(clone_board)
                if score > best_score:
                    best_score = score
                    best_pos = t_pos
                    best_rot = t_rot
        return self.make_best_move(board, best_pos, best_rot)

SelectedPlayer = MyPlayer
            

