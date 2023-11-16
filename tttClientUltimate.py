# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 07:59:26 2022

@author: trand27
"""

import threading # Imported to Handle the connection between the Host and Client and repeated inputs
import socket # Imported establish a connection to play the game on different devices
import sys # Imported to exit the the program when the game ends
#C:\Users\nguyenp25\Anaconda3\python.exe
class TicTacToe:
    def __init__(self): # board index starts at 0
        #[matrixIndex][rowIndex][colIndex] 
        # This part of the code was written by us
        self.boards = [
                       [[" ", " ", " "], 
                        [" ", " ", " "], #First Matrix, starts at index 0
                        [" ", " ", " "]],
                       
                       [[" ", " ", " "], 
                        [" ", " ", " "], #Second Matrix, index 1 etc.
                        [" ", " ", " "]],
                       
                       [[" ", " ", " "], 
                        [" ", " ", " "],
                        [" ", " ", " "]],
                       
                       [[" ", " ", " "], 
                        [" ", " ", " "], 
                        [" ", " ", " "]],
                       
                       [[" ", " ", " "], 
                        [" ", " ", " "], 
                        [" ", " ", " "]],
                       
                       [[" ", " ", " "], 
                        [" ", " ", " "],
                        [" ", " ", " "]],
                       
                       [[" ", " ", " "], 
                        [" ", " ", " "], 
                        [" ", " ", " "]],
                       
                       [[" ", " ", " "], 
                        [" ", " ", " "], 
                        [" ", " ", " "]],
                       
                       [[" ", " ", " "],
                        [" ", " ", " "], 
                        [" ", " ", " "]]
                       ]
        
        # This board checks for the overall winner, when a regular 3x3 board is won, it marks on this board who won what board with X or O. 
        # If its a tie between both players, marks the board with T (T for tie)
        self.boardFinal = [
            [" "],[" "],[" "],
            [" "],[" "],[" "],
            [" "],[" "],[" "]
            ]
   
        self.turn = "X" # sets player X as the first player
        self.you = "X" #You are the player X with mark X
        self.opponent = "O" # opponent is player O with mark O
        self.winner = None # Variable is set to the symbol of the person who won depending on the conditions of boardFinal
        self.game_over = False # This is used to check for when 1 out of the 9 boards has been won
        self.final_game_over = False # Used to check if the overall game is over
        self.finalboardCounter = 0 #When this reaches 9 and no one has won the overall board, the overall winner is a tie for both players
        self.counter = 0 #When this counter reaches 9, it means all 9 spots in a singular matrix has been filled, this is used to check for the appropriate win/lose/tie conditions

    # This infrastrucutre code was used from another source(can check References in the research paper) or https://www.youtube.com/watch?v=s6HOPw_5XuY
    def host_game(self, host, port): #starts game by creating TCP connection
         #Create a new socket, binds it, listens and accepts connection
         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
         s.bind((host, port)) 
         s.listen(1) 
         client, addr = s.accept()
         #Symbols , you are X, opponent is O if you are hosting
         self.you = "X"
         self.opponent = "O"
         threading.Thread(target=self.handle_connection, args=(client,)).start()
         s.close()
    # This infrastrucutre code was used from another source(can check References in the research paper) or https://www.youtube.com/watch?v=s6HOPw_5XuY
    def connect_to_game(self, host, port): #client connects to host's game
        # Client creates a socket and connects
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        self.you = 'O'
        self.opponent = 'X'
        threading.Thread(target=self.handle_connection, args=(client,)).start() #Running multiple things
        
   
        
    # check_if_won when called cycles through each matrix and scans each row, column, and diagonal for 3 consecutive player marks. 
    # If one of the following conditions is met, it appends whatever symbol was that has won( X or O ) that board with the corresponding index on the overall board
    # If none of the conditions stated above are met, append that corresponding index on the overall board with T(T for tie)
    # This part of the code was written by us
    
    def check_if_won(self):   
       index = 0
       
       
       for index in range(9):
           #When a condition is met, add 1 to the counter and set the mark on the overall board
           #set game_over to true so you dont need to check for a tie
           for row in range(3):# Checks for rows
               if self.boards[index][row][0] == self.boards[index][row][1] == self.boards[index][row][2] != " ":
                   self.winner = self.boards[index][row][2]
                   self.boardFinal[index] = self.winner
                   self.finalboardCounter += 1
                   self.game_over = True
                
                  
           for col in range(3):# Checks for columns
               if self.boards[index][0][col] == self.boards[index][1][col] == self.boards[index][2][col] != " ":
                   self.winner = self.boards[index][2][col]
                   self.boardFinal[index] = self.winner
                   self.finalboardCounter += 1
                   self.game_over = True
                
           #Checks for Diagonal from top left to bottom right of a 3x3 board/matrix
           if self.boards[index][0][0] == self.boards[index][1][1] == self.boards[index][2][2] != " ":
                   self.winner = self.boards[index][0][0]
                   self.boardFinal[index] = self.winner
                   self.finalboardCounter += 1
                   self.game_over = True
                   
           #Checks for Diagonal from top right to bottom left of a 3x3 board/matrix    
           if self.boards[index][2][0] == self.boards[index][1][1] == self.boards[index][0][2] != " ":
                   self.winner = self.boards[index][0][2]
                   self.boardFinal[index] = self.winner
                   self.finalboardCounter += 1
                   self.game_over = True
                   
           # If a board was won by one of the players, great! Set the variable game_over back to false
           if self.game_over == True:
               self.game_over = False
           else:
           #However if there was no winner and every index of the board was filled, Checks if there was a tie, mark that matrix to the corresponding overall board index with a T (T for tie)
               self.game_over = False
               if self.boards[index][0][0] != " " and self.boards[index][0][1] != " " and self.boards[index][0][2]!= " " and self.boards[index][1][0] != " " and self.boards[index][1][1] != " " and self.boards[index][1][2] != " " and self.boards[index][2][0] != " " and self.boards[index][2][1] != " " and self.boards[index][2][2] != " ":
                   self.winner = "T"
                   self.boardFinal[index] = self.winner
                   self.finalboardCounter += 1
           self.winner = None         

    # This is very similar to the method above that checks if a person has won a singular board on the overall board
    # This method checks for the winner/loser of the overall game by checking if there was 3 consecutive rows/columns/diagonals on the overall board
    # This code was written by us
    def check_if_won_final(self):
        addThree = 0
        for row in range(3): #Checks for rows
            if self.boardFinal[0+addThree] == self.boardFinal[1+addThree] == self.boardFinal[2+addThree] != " ":
                self.winner = self.boardFinal[0+addThree]
                self.final_game_over = True
                return True
            addThree+=3
            
        addOne = 0
        for col in range(3): #Checks for columns
            if self.boardFinal[0+addOne] == self.boardFinal[3+addOne] == self.boardFinal[6+addOne] != " ":
                self.winner = self.boardFinal[0+addOne]
                self.final_game_over = True
                return True
            addOne+=1
        #Checks for diagonals from top left to bottom right
        if self.boardFinal[0] == self.boardFinal[4] == self.boardFinal[8] != " ":
            self.winner = self.boardFinal[0]
            self.final_game_over = True
            return True
        #Checks for Diagonals from top right to bottom left
        if self.boardFinal[2] == self.boardFinal[4] == self.boardFinal[6] != " ":
            self.winner = self.boardFinal[2]
            self.final_game_over = True
            return True
        if self.finalboardCounter == 9:
            self.final_game_over = True
            return True
        return False
        

    # Prints out the 9x9 board in a fancy way 
    # First Prints the first matrix, then the second and third on the first row
    # After it goes to the next row and prints the 4th,5th, and 6th and repeats this process for 7th,8th, and 9th adding some other print statements just to make the board look more neater
    # This part of the code was written by us
    def print_board(self): 
        boardDim = len(self.boards)
        rows = 0
        addthree = 0
        print("===================================", )
        for i in range(0,boardDim,1):
            
            for cols in range(3):
                print(" | ".join(self.boards[cols+addthree][rows]), end= " | ")
                
            rows += 1
            #Prints these as dimensions to seperate matrixes to appear more visible
            if rows == 3:
                rows =0
                print("\n=================================== ", )
            else:
                print("")
                print("----------|-----------|-----------|")
            if i == 2 or i == 5:
                addthree += 3
                
    # Prints out the overall board(3x3), will display which boards are won from whom during real game time, if a player has won the first board(Top left), then the top left of this 3x3 will display the players mark who won that board on the top left of this 3x3 board
    # This part of the code was written by us
    def print_final_board(self):
        addThree = 0
        print("\nOverall Boards Won:")
        print("-----------")
        for index in range(3):
            for row in range(3): # Prints three items in the boardFinal array on seperate rows to make it look like a 3x3 matrix
                
                print(" | ".join(self.boardFinal[row+addThree]),end = " | ")
            print("\n-----------")
            addThree += 3
            
    #Method checks if inputed move is valid
    #The board is 9x9 however we decided to use inputs 0-8(could have been 1-9 but we were used to the first index being 0) for both row and column 
    # This part of the code was written by us, though we did use a little bit of the ideas in the reference video and expanded upon it
    def check_valid_move(self, move):
       if self.game_over: # if the game is over return this(this being depending on the condition that is met)
           return
       
       #Matrix index is used below, explained
       matrixIndex = 0
       rowInput=int(move[0]) # Takes the "row" Input
       colInput=int(move[1]) # Takes the "column" input
       
       #If player input is out of the scope of 0-8, return false
       if rowInput < 0 or rowInput > 8:
           return False
       if colInput < 0 or colInput > 8:
           return False
       
       #This was probably THE most complicated and most difficult part of the project, and the issue could have been easily avoided with a different implementation however we coded the win/lose conditions first so we decided to stick with it and implemented this algorithm
       #This code converts the players inputs to obtain the appropriate matrix. 
       #This was needed because it would take the players inputs of (rowIndex,columnIndex) as (matrixIndex,rowIndex), this basically fixes that issue by converting the two values into (row,columns)
       # Adds onto the matrix index if >= 6 or 3 by 6 or 3 respectively. If 3> columnInput add nothing to matrixIndex
       if colInput >= 6:
           matrixIndex+=6
       elif colInput >= 3:
           matrixIndex+=3
       
        # Adds onto the matrix index if rowInput >= 6 or 3 by 2 or 1 respectively. If 3> rowInput add nothing to matrixIndex
       if rowInput >= 6:
           matrixIndex+=2
       elif rowInput >= 3:
           matrixIndex+=1
           
       rowInput = rowInput%3
       colInput = colInput%3
       
       #Condition checks and makes it so boards that have already won cannot have new markers placed in them 
       if self.boardFinal[matrixIndex][0]  != " ":
           return False
       
       
       return self.boards[matrixIndex][colInput][rowInput] == " "
   
    # This part of the code was written by us, though we did use some of the ideas in the reference video and expanded upon it
    def apply_move(self, move, player):
        if self.game_over: # if the game is over return this(this being depending on the condition that is met)
            return
        # Algorithm explained above in the check_valid_move(self,move) method
        matrixIndex = 0
        rowInput=int(move[0])
        colInput=int(move[1]) 
        
        if colInput >= 6:
            matrixIndex+=6
        elif colInput >= 3:
            matrixIndex+=3
        
        if rowInput >= 6:
            matrixIndex+=2
        elif rowInput >= 3:
            matrixIndex+=1
            
        rowInput = rowInput%3
        colInput = colInput%3
        
        #Set the players mark to what ever they inputed for row,column
        #This prints out the players input on the actually board
        self.boards[matrixIndex][colInput][rowInput] = player
        self.print_board()
        #This if/else statement updates the overall board whenever a player has or hasnt won a board on the overall 9 boards
        if self.check_if_won():
            self.print_final_board()
        else:
            self.print_final_board()
        #If the method returns true, it means the game is over and prints the mark of the player of whoever won with a msg
        if self.check_if_won_final():
            if self.winner == self.you:
                print(self.winner,"is the winner!")
                sys.exit()
                
            elif self.winner == self.opponent:
                print(self.winner,"is the winner!")
                sys.exit()
        else:
            #if all 9 spots on the board overall have been filled and if no player has won the overall board, it means the game has ended in a tie
            counter = 0
            for index in range(9):
                if self.boardFinal[index][0] != " ": 
                    counter += 1
                    
                if counter == 9:
                    print("Its a draw")
                    sys.exit()
    
        
    
    # This infrastrucutre code was used from another source(can check References in the research paper)   
    def handle_connection(self, client):
        while not self.game_over:#Do this while game is not over and if its your turn
            if self.turn == self.you: #Checks if valid, if yes applies your symbol
                move = input("Enter your move (row, column): ")
                
                #if statement to check in the boardFinal if that index is not empty, you cant place a spot in that board if false
                if self.check_valid_move(move.split(',')):
                    client.send(move.encode('utf-8')) # Client sends the move and encodes it to host
                    self.apply_move(move.split(','), self.you) # Moves are split by commas(ex rows , cols)
                    self.turn = self.opponent
                else:
                    print("Move is invalid. Try again.")
            else:
                data = client.recv(1024) # Client waits to receive if not their turn
                if not data: 
                    break
                else:
                    self.apply_move(data.decode('utf-8').split(','), self.opponent)
                    self.turn = self.you
        client.close()

game = TicTacToe()
game.connect_to_game('localHost', 5555)