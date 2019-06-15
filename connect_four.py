"""
Rules:
- Make 4 pieces in a row to win!
- You can drop pieces in or pop pieces from the bottom!
"""

import numpy as np 
import random

class Game:
    rows = 6
    cols = 7
    mat = np.zeros((rows, cols))
    piece = 1   #1: player, 2: computer
    difficulty = "easy"

game = Game()

# 1: player wins, 2: computer wins, 3: draw, 0: neither win nor draw (continue game)
def check_victory():
    continue_game = False
    
    # go through the rows and columns of the board
    for x in range(game.rows):
        for y in range(game.cols):
            # horizontal check
            if y < game.cols-3:
                if game.mat[x][y] == game.piece and game.mat[x][y+1] == game.piece and game.mat[x][y+2] == game.piece and game.mat[x][y+3] == game.piece:
                    return game.piece
            # vertical check
            if x < game.rows-3:
                if game.mat[x][y] == game.piece and game.mat[x+1][y] == game.piece and game.mat[x+2][y] == game.piece and game.mat[x+3][y] == game.piece:
                    return game.piece
            # / check
            if x >= game.rows-3 and y < game.cols-3:  
                if game.mat[x][y] == game.piece and game.mat[x-1][y+1] == game.piece and game.mat[x-2][y+2] == game.piece and game.mat[x-3][y+3] == game.piece:
                    return game.piece
            # \ check
            if x < game.rows-3 and y < game.cols-3:   
                if game.mat[x][y] == game.piece and game.mat[x+1][y+1] == game.piece and game.mat[x+2][y+2] == game.piece and game.mat[x+3][y+3] == game.piece:
                    return game.piece
            # if any spot in the board is empty, the game can still continue
            if game.mat[x][y] == 0:
                continue_game = True

    if continue_game == True:
        return 0    # continue game
    else: 
        return 3    # draw - the board is filled

def check_move(col, is_pop):
    # pop - piece at bottom of column must be player's own
    if is_pop:
        if game.mat[game.rows-1, col-1] == game.piece:
            return True
    
    # drop - column must not already be filled up with pieces
    else:
        for i in range(game.rows):
            if game.mat[game.rows-1-i, col-1] == 0:
                return True

    return False

def apply_move(col, is_pop, print_move):
    # pop - pops/removes player's own piece from the bottom of column, then all other pieces on top of it move down by 1 spot
    if is_pop:
        if print_move == True:
            print("> POPPED AT COLUMN", col)
        for i in range(game.rows-1):
            game.mat[game.rows-1-i, col-1] = game.mat[game.rows-2-i, col-1]
    
    # drop - drops player's own piece into that column from the top
    else:
        if print_move == True:
            print("> DROPPED AT COLUMN", col)
        for i in range(game.rows):
            if game.mat[game.rows-1-i, col-1] == 0:
                game.mat[game.rows-1-i, col-1] = game.piece
                break

def computer_move():
    # easy mode - moves are randomized
    if game.difficulty == 'easy':
        comp_move_input = random.choice(['pop', 'drop'])
        if comp_move_input == 'pop':
            comp_is_pop = True
        else:
            comp_is_pop = False
        comp_col_input = random.randint(1, game.cols)
        if check_move(comp_col_input, comp_is_pop) == True:
            apply_move(comp_col_input, comp_is_pop, True)
        else:
            computer_move()
    
    # # medium mode -
    # # 1. if there is a winning move, the computer will execute it
    # # 2. if the player's next move is going to be a winning move, the computer will block it
    # # 3. otherwise, moves are randomized
    # if game.difficulty == 'medium':
    #     if next_round_victory('computer') == True:
    #         print("> THE ROBOT OUTSMARTS YOU!")
    #         game.piece = 2
    #         apply_move(next_col_input, next_move_input, True)
    #         return
    #     elif next_round_victory('human') == True:
    #         print("> THE ROBOT BLOCKS THE WAY!")
    #         return
    #     else:
    #         print("> A NORMAL ROBOT JUST DOING ITS JOB.")
    #         game.difficulty = 'easy'
    #         game.piece = 2
    #         computer_move()

# def next_round_victory(player):
#     global next_col_input, next_move_input

#     if player == 'human':
#         game.piece = 1
#     if player == 'computer':
#         game.piece = 2
        
#     for next_move_input in ['drop', 'pop']:
#         for next_col_input in range(1, game.cols+1):
#             mat_original = np.copy(game.mat)
#             if check_move(next_col_input, next_move_input) == True:               #if the move is valid
#                 apply_move(next_col_input, next_move_input, False)    #execute it on the temporary board
#                 if check_victory() == game.piece:                  #if it results in victory
#                     game.mat = mat_original
#                     return True                                                 #execute it on the real board
#                 else:
#                     game.mat = mat_original
    
#     game.mat = mat_original
#     return False
        
def main():
    # input difficulty level
    while True:
        game.difficulty = input("LEVEL - EASY OR MEDIUM?: ").lower()
        if game.difficulty == "easy" or game.difficulty == "medium":
            break
        else:
            print("> TYPE IN 'EASY' OR 'MEDIUM'.")

    while True:
        print(game.mat)
        game.piece = 1
        
        # input player move (pop/drop)
        player_move = input("POP OR DROP? [TYPE 'EXIT' TO STOP THE GAME]: ").lower()
        if player_move == "pop":
            is_pop = True
        elif player_move == "drop":
            is_pop = False
        elif player_move == "exit":
            break
        else:
            print("> TYPE IN 'POP' OR 'DROP'.")
            continue
        
        # input column (1-7)
        try:
            col_input = int(input("WHICH COLUMN [1-7]?: "))
        except:
            print("> INPUT AN APPROPRIATE COLUMN NUMBER.")
            continue
        if col_input < 1 or col_input > game.cols:
            print("> INPUT A COLUMN NUMBER BETWEEN 1 TO 7 (INCLUSIVE).")
            continue
        
        # execute player's move if valid
        if check_move(col_input, is_pop) == True:
            print("\nPLAYER 1'S TURN")
            apply_move(col_input, is_pop, True)
            print(game.mat)
        else:
            print("> YOU CAN'T DO THAT.")
            continue
        
        # check for player's win or draw
        if check_victory() == 1:
            print("PLAYER 1 WINS!")
            break
        elif check_victory() == 3:
            print("THE GAME HAS ENDED IN A DRAW.")
            break
        
        # execute robot's move
        print("\nPLAYER 2'S TURN")
        game.piece = 2
        game.difficulty = 'medium'
        computer_move()

        # Check for robot's win or draw
        if check_victory() == 2:
            print(game.mat)
            print("\nPLAYER 2 WINS!")
            break
        elif check_victory() == 3:
            print(game.mat)
            print("\nTHE GAME HAS ENDED IN A DRAW.")
            break

main()