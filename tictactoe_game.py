from typing import List, Tuple
# this function returns a 3x3 board initialized with blank spaces in each row and col
def Create_Board() -> List[List[str]]:
    return [[" " for _ in range(3)] for _ in range(3)]
#this function prints the board like a real Tic-Tac-Toe grid.
def Print_Board(board: List[List[str]]) -> None:
    for row in board:
        print(" | ".join(row))
        print("---------")
#this function assures that every move made is valid by checking if the cell is empty at given row and col
def Is_Move_Valid(board: List[List[str]], row: int, col: int) -> bool:
    return board[row][col] == " "
#this function makes the move
def Make_Move(board: List[List[str]], row: int, col: int, player) -> None:
    board[row][col] = player
#this function checks wheter the given player has won the match
def Is_Winner(board: List[List[str]], player: str) -> bool:
  #this loop checks horizontally and vertically
    for i in range(3):
        if all(cell == player for cell in board[i]) or all(board[j][i] == player for j in range(3)):
            return True
   #this loop checks diagonally
    if board[0][0] == board[1][1] == board[2][2] == player or board[0][2] == board[1][1] == board[2][0] == player:
        return True
    #if none of above conditions are satisfied this means no player has won the match
    return False
#this function checks wheter the game is over (i-e any of player won or is their a tie situation)
def Is_Game_Over(board: List[List[str]]) -> bool:
    return Is_Winner(board, "X") or Is_Winner(board, "O") or all(" " not in row for row in board)

#this function implements simple minimax
def Minimax(board: List[List[str]], depth: int, maximizing_player: bool) -> int:
 #base cases to stop recursion
  #this indicates AI is losing
    if Is_Winner(board, "X"):
        return -1
   #this indicates AI is winning
    if Is_Winner(board, "O"):
        return 1
  #this indicates tie situation
    if Is_Game_Over(board):
        return 0
    if maximizing_player:
      #starting with worst possible score inorder to find maximum
        best_score = float("-inf")
        #trying to achieve best score(i-e 1) by placing O in every possible place then choose any one place that gives the best score
        for row in range(3):
            for col in range(3):
                if Is_Move_Valid(board, row, col):
                    board[row][col] = 'O'
                    score = Minimax(board, depth + 1, False)
                    board[row][col] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
      #if its opponent's turn so assigning the best possible score
        best_score = float("inf")
        #trying every possible move which could benefit AI in future
        for row in range(3):
            for col in range(3):
                if Is_Move_Valid(board, row, col):
                    board[row][col] = 'X'
                    score = Minimax(board, depth + 1, True)
                    board[row][col] = ' '
                    best_score = min(score, best_score)
        return best_score
#this implements the optimize version of Minimax by alpha beta pruning

def Minimax_Optimize(board: List[List[str]], depth: int, maximizing_player: bool, alpha: int, beta: int) -> int:
   #base conditions for recursion
    if Is_Winner(board, "X"):
        return -1
    if Is_Winner(board, "O"):
        return 1
    if Is_Game_Over(board):
        return 0

    if maximizing_player:
      #Starting with the worst possible score
        best_score = float("-inf")
        #trying all moves
        for row in range(3):
            for col in range(3):
                if Is_Move_Valid(board, row, col):
                    board[row][col] = 'O'
                    score = Minimax_Optimize(board, depth + 1, False, alpha, beta)
                    board[row][col] = ' '
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
        return best_score
    else:
         #Starting with the best possible score
        best_score = float("inf")
        #Try to minimize the best score (because opponent tries to defeat the AI).
        for row in range(3):
            for col in range(3):
                if Is_Move_Valid(board, row, col):
                    board[row][col] = 'X'
                    score = Minimax_Optimize(board, depth + 1, True, alpha, beta)
                    board[row][col] = ' '
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
        return best_score

#finding best move among all possible moves for Minimax
def Find_Best_Move(board: List[List[str]]) -> Tuple[int, int]:
    best_score = float("-inf")
    best_move = None
    for row in range(3):
        for col in range(3):
            if Is_Move_Valid(board, row, col):
                board[row][col] = 'O'
                score = Minimax(board, 0, False)
                board[row][col] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    return best_move

#finding best move among all possible moves for Optimized Minimax
def Find_Best_Move_Optimize(board: List[List[str]]) -> Tuple[int, int]:
    best_score = float("-inf")
    best_move = None
    for row in range(3):
        for col in range(3):
            if Is_Move_Valid(board, row, col):
                board[row][col] = 'O'
                score = Minimax_Optimize(board, 0, False, float("-inf"), float("inf"))
                board[row][col] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    return best_move
#this function has the actual implementation of all above functions
def Play_Game() -> None:
  while True:
    print("Choose Opponent(AI) Version:")
    print("1. Simple Minimax\n2. Optimized Minimax (Alpha-Beta Pruning)\n3.Exit")
    choice = input("Enter your choice: ")
    #Exit condition
    if choice == "3":
        break
     #Invalid condition
    if choice not in ["1", "2","3"]:
        print("Invalid choice. Please select 1, 2, or 3.")
        continue
    #Creating Board to improve Visuals
    board = Create_Board()
    Current_Player = "X"
    Print_Board(board)

    while not Is_Game_Over(board):
      #Taking user's input until game is over
        if Current_Player == "X":
            try:
                row, col = map(int, input("Enter Your Move (row col): ").split())
            except ValueError:
                print("Invalid input!")
                continue
        else:
            if choice == "1":
                row, col = Find_Best_Move(board)
            elif choice == "2":
                row, col = Find_Best_Move_Optimize(board)
            else:
                print("Invalid choice. Defaulting to simple Minimax.")
                row, col = Find_Best_Move(board)
            #Printing AI's Move where
            print(f"AI's Move {row},{col}")

        if 0 <= row < 3 and 0 <= col < 3 and Is_Move_Valid(board, row, col):
            Make_Move(board, row, col, Current_Player)
            Print_Board(board)
            if Is_Winner(board, Current_Player):
                print(f"Player {Current_Player} Wins!")
                break
            Current_Player = "O" if Current_Player == "X" else "X"
        else:
            print("Invalid move! Try again.")

    else:
        print("It's a tie!")
#Main function
if __name__ == '__main__':
    Play_Game()