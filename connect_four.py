# Connect 4! 4 pieces in a row to win. You can opt to drop pieces in, or pop pieces from the bottom.
# Extra stuff to add:
# 1. Make menu() less draggy -> create check_valid_input() function and game_end() function
# 2. Make the medium robot harder to beat -> It will avoid all moves such that the next player's move can be a winning move

import numpy as np 
import random

class Game:
    #mat = None
    rows = 6
    cols = 7
    #turn = 0
    #wins = 0

game = Game()
game_board = np.zeros((game.rows, game.cols))

#returns 1 if player wins, 2 if robot wins, 3 if draw, 0 if neither win nor draw
def check_victory(player, board):
    remaining_space = False
    if player == 'human':
        piece = 1
    else:
        piece = 2
    
    for x in range(game.rows):
        for y in range(game.cols):
            if y < game.cols-3: #horizontal victory check
                if board[x][y] == piece and board[x][y+1] == piece and board[x][y+2] == piece and board[x][y+3] == piece:
                    return piece
            elif x < game.rows-3: #vertical victory check
                if board[x][y] == piece and board[x+1][y] == piece and board[x+2][y] == piece and board[x+3][y] == piece:
                    return piece
            elif x >= game.rows-3 and y < game.cols-3: #diagonal victory check /
                if board[x][y] == piece and board[x-1][y+1] == piece and board[x-2][y+2] == piece and board[x-3][y+3] == piece:
                    return piece
            elif x < game.rows-3 and y < game.cols-3: #diagonal victory check \
                if board[x][y] == piece and board[x+1][y+1] == piece and board[x+2][y+2] == piece and board[x+3][y+3] == piece:
                    return piece
            if board[x][y] == 0 and remaining_space == False:
                remaining_space = True

    if remaining_space == True: #continue game
        return 0
    else: #draw (no more space to drop pieces)
        return 3

def check_move(col, pop, player):
    if player == 'human':
        piece = 1
    else:
        piece = 2
    
    #for valid pop, piece at bottom of column must be player's own
    if pop == True:
        if game_board[game.rows-1, col-1] == piece:
            return True
    
    #for valid drop, column must not already be filled up with pieces
    else:
        for i in range(game.rows):
            if game_board[game.rows-1-i, col-1] == 0:
                return True

def apply_move(col, pop, player, board, print_move):
    if player == 'human':
        piece = 1
    else:
        piece = 2
    
    #pop: pops/removes player's own piece from the bottom of column, then all other pieces on top of it move down by 1 spot
    if pop == True:
        if print_move == True:
            print("> POPPED AT COLUMN", col)
        for i in range(game.rows-1):
            board[game.rows-1-i, col-1] = board[game.rows-2-i, col-1]
        return board
    
    #drop: drops player's own piece into that column from the top
    else:
        if print_move == True:
            print("> DROPPED AT COLUMN", col)
        for i in range(game.rows):
            if board[game.rows-1-i, col-1] == 0:
                board[game.rows-1-i, col-1] = piece
                return board

def computer_move(level):
    #easy mode: moves are randomized
    if level == 'easy':
        ai_move_input = random.choice(['pop', 'drop'])
        ai_col_input = random.randint(1, game.cols)
        if check_move(ai_col_input, ai_move_input, 'ai') == True:
            apply_move(ai_col_input, ai_move_input, 'ai', game_board, True)
        else:
            computer_move('easy')
    
    #medium mode: 
    #1. if there is a winning move, the robot will execute it
    #2. if the player's next move is going to be a winning move, the robot will block it
    #3. otherwise, moves are randomized
    if level == 'medium':
        if next_round_victory('ai') == True:
            print("> THE ROBOT OUTSMARTS YOU!")
            apply_move(col_input, move_input, 'ai', game_board, True)
            return game_board
        elif next_round_victory('human') == True:
            print("> THE ROBOT BLOCKS THE WAY!")
            apply_move(col_input, move_input, 'ai', game_board, True)
        else:
            print("> A NORMAL ROBOT JUST DOING ITS JOB.")
            computer_move('easy')

def next_round_victory(player):
    global move_input, col_input
    if player == 'human':
        piece = 1
    else:
        piece = 2
        
    for move_input in ['drop', 'pop']:
        for col_input in range(1, game.cols+1):
            temp_board = np.copy(game_board)
            if check_move(col_input, move_input, player) == True:               #if the move is valid
                apply_move(col_input, move_input, player, temp_board, False)    #execute it on the temporary board
                if check_victory(player, temp_board) == piece:                  #if it results in victory
                    return True                                                 #execute it on the real board
        
def menu():
    while True:
        #checks for valid difficulty input (easy/medium)
        difficulty_input = input("LEVEL - EASY OR MEDIUM?: ").lower()
        if difficulty_input == 'easy' or difficulty_input == 'medium':
            break
        else:
            print("> TYPE IN 'EASY' OR 'MEDIUM'.")

    while True:
        print(game_board)
        
        #checks for valid move input (pop/drop)
        move_input = input("POP OR DROP? [TYPE 'EXIT' TO STOP THE GAME]: ").lower()
        if move_input == "pop":
            pop_input = True
        elif move_input == "drop":
            pop_input = False
        elif move_input == 'exit':
            break
        else:
            print("> TYPE IN 'POP' OR 'DROP'.")
            continue
            
        #checks for valid column input (integer 1-7)
        try:
            col_input = int(input("WHICH COLUMN [1-7]?: "))
        except:
            print("> INPUT AN APPROPRIATE COLUMN NUMBER.")
            continue
        if col_input < 1 or col_input > game.cols:
            print("> INPUT A COLUMN NUMBER BETWEEN 1 TO 7 (INCLUSIVE).")
            continue
        
        if check_move(col_input, pop_input, 'human') == True:
            print("\nPLAYER 1'S TURN")
            print(str(apply_move(col_input, pop_input, 'human', game_board, True)) + "\n")
        else:
            print("> YOU CAN'T DO THAT.")
            continue
        #executes player's move if valid
        
        #checks for player's victory or overall draw
        if check_victory('human', game_board) == 1:
            print("PLAYER 1 WINS!")
            break
        elif check_victory('human', game_board) == 3:
            print("THE GAME HAS ENDED IN A DRAW.")
            break
        
        #executes robot's move
        print("PLAYER 2'S TURN")
        computer_move(difficulty_input)
        
        #checks for robot's victory or overall draw, otherwise game proceeds to next turn
        if check_victory('ai', game_board) == 2:
            print(game_board)
            print("\nPLAYER 2 WINS!")
            break
        elif check_victory('ai', game_board) == 3:
            print(game_board)
            print("\nTHE GAME HAS ENDED IN A DRAW.")
            break

menu()