# Make a TIC TAC TOE game
from random import randint
from IPython.display import clear_output

# Let user select what they want
usr_input = input("Enter your choice 'X' or 'O': ").upper()
if usr_input == 'X':
    computer_input = 'O'

elif usr_input == 'O':
    computer_input = 'X'

# Game will run until user does not enters no
while usr_input!='NO':
    computer_number=0
    if usr_input == 'X':
        computer_input = 'O'
        print('You are now X \nMake move')
    elif usr_input == 'O':
        computer_input = 'X'
        print('You are now O \nMake move')
        
    #Dictonary
    # Make every position in board as blank space
    d = {1:' ',2:' ',3:' ',4:' ',5:' ',6:' ',7:' ',8:' ',9:' ' }
    
    # Board
    line = ' {0} | {1} | {2} \n-----------\n {3} | {4} | {5}\n----------- \n {6} | {7} | {8}'
    
    # Condition becomes true if user type no
    condition = False
    print(line.format(1,2,3,4,5,6,7,8,9))
    while condition != True:
        # Take input from user to represent 'X' or 'O' on board
        usr_number = int(input('Enter number: '))
        
        # If user puts number at which there is already a 'X' or 'O' then user must enter number again
        while computer_number==usr_number or d[usr_number]=='O' or d[usr_number]=='X':
            print('Please enter other number')
            usr_number = int(input('Enter number: '))
        if d[usr_number] == ' ':
            d[usr_number] = usr_input
            
        #clear screen here
        clear_output()
        
        # Print the board
        print(line.format(d[1],d[2],d[3],d[4],d[5],d[6],d[7],d[8],d[9])+'\n')
        
        # Condition to check if user has won or not
        # Check win condition on rows
        if (d[1]==d[2]==d[3]==usr_input) or (d[4]==d[5]==d[6]==usr_input)or (d[7]==d[8]==d[9]==usr_input):
            print('You won!!')
            break
        
        # Check win condition on column
        elif (d[1]==d[4]==d[7]==usr_input) or (d[2]==d[5]==d[8]==usr_input) or (d[3]=='X' and d[6]=='X' and d[9]==usr_input):
            print('You won!!')
            break
        
        # Check win condition on diagonals
        elif (d[7]==d[5]==d[3]==usr_input) or (d[1]==d[5]==d[9]==usr_input):    
            print('You won!!')
            break
        
        # Now its computer's turn
        # Computer will choose any number between 0 to 9
        
        computer_number= randint(1,9)
        
        # To check if user number and computer number match or not
        ## If they match then computer must again choose a number 
        ## If number selected by computer has 'O' or 'X' at that position then computer must select number again
        while (computer_number==usr_number or d[computer_number]=='O' or d[computer_number]=='X' ):
            computer_number= randint(1,9)
        
        
        if d[computer_number] == ' ' :
            d[computer_number] = computer_input
            
        #clear screen here
        clear_output()
        
        # Print the board
        print(line.format(d[1],d[2],d[3],d[4],d[5],d[6],d[7],d[8],d[9])+'\n')
        
        # Condition to check if computer has won or not
        # Check win condition on rows
        if (d[1]==d[2]==d[3]==computer_input) or (d[4]==d[5]==d[6]==computer_input)or (d[7]==d[8]==d[9]==computer_input):
            print('Computer won!!')
            condition = True
        
        # Check win condition on column
        elif (d[1]==d[4]==d[7]==computer_input) or (d[2]==d[5]==d[8]==computer_input) or (d[3]==d[6]==d[9]==computer_input):
            print('Computer won!!')
            condition = True
        
        # Check win condition on diagonals
        elif  (d[7]==d[5]==d[3]==computer_input) or (d[1]==d[5]==d[9]==computer_input):
            print('Computer won!!')
            condition = True
       
        
    usr_input = input("Enter your choice 'X' or 'O' or 'NO' to exit game: ").upper()
