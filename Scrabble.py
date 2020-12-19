from sys import stdin
import math
import sys
import random
import time


TILES_USED = 0 # records how many tiles have been returned to user
CELL_WIDTH = 3 # cell width of the scrabble board
SHUFFLE = False # records whether to shuffle the tiles or not

# inserts tiles into myTiles
def getTiles(myTiles):
    global TILES_USED
    while len(myTiles) < 7 and TILES_USED < len(Tiles):
        myTiles.append(Tiles[TILES_USED])
        TILES_USED += 1


# prints tiles and their scores
def printTiles(myTiles):
    tiles = ""
    scores = ""
    for letter in myTiles:
        tiles += letter + "  "
        thisScore = getScore(letter)
        if thisScore > 9:
            scores += str(thisScore) + " "
        else:
            scores += str(thisScore) + "  "

    print("\nTiles : " + tiles)
    print("Scores: " + scores)


# gets the score of a letter
def getScore(letter):
    for item in Scores:
        if item[0] == letter:
            return item[1]

# initialize n x n Board with empty strings
def initializeBoard(n):
    Board = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append("")
        Board.append(row)

    return Board

# put character t before and after the string s such that the total length
# of the string s is CELL_WIDTH.
def getString(s,t):
    global CELL_WIDTH
    s = str(s)
    rem = CELL_WIDTH - len(s)
    rem = rem//2
    s = t*rem + s
    rem = CELL_WIDTH - len(s)
    s = s + t*rem
    return s

# print the Board on screen
def printBoard(Board):
    global CELL_WIDTH
    print("\nBoard:")
    spaces = CELL_WIDTH*" "
    board_str =  "  |" + "|".join(getString(item," ") for item in range(len(Board)))  +"|"
    line1 = "--|" + "|".join(getString("","-") for item in range(len(Board)))  +"|"


    print(board_str)
    print(line1)

    for i in range(len(Board)):
        row = str(i) + " "*(2-len(str(i))) +"|"
        for j in range(len(Board)):
            row += getString(Board[i][j]," ") + "|"
        print(row)
        print(line1)

    print()

scoresFile = open('scores.txt')
tilesFile = open('tiles.txt')

# read scores from scores.txt and insert in the list Scores
Scores = []
for line in scoresFile:
    line = line.split()
    letter = line[0]
    score = int(line[1])
    Scores.append([letter,score])
scoresFile.close()

# read tiles from tiles.txt and insert in the list Tiles
Tiles = []
for line in tilesFile:
    line= line.strip()
    Tiles.append(line)
tilesFile.close()

# decide whether to return random tiles
rand = input("Do you want to use random tiles (enter Y or N): ")
if rand == "Y":
    SHUFFLE = True
else:
    if rand != "N":
        print("You did not enter Y or N. Therefore, I am taking it as a Yes :P.")
        SHUFFLE = True
if SHUFFLE:
    random.shuffle(Tiles)


validBoardSize = False
while not validBoardSize:
    BOARD_SIZE = input("Enter board size (a number between 5 to 15): ")
    if BOARD_SIZE.isdigit():
        BOARD_SIZE = int(BOARD_SIZE)
        if BOARD_SIZE >= 5 and BOARD_SIZE <= 15:
            validBoardSize = True
        else:
            print("Your number is not within the range.\n")
    else:
        print("Are you a little tipsy? I asked you to enter a number.\n")

Board = initializeBoard(BOARD_SIZE)
printBoard(Board)

if BOARD_SIZE == 12:
    print(" FYI:In the 12X12 Board after putting in around 6th valid words,\n it will take around '3 mins' for the max possible score to come out.\n and it increases after that too.")
myTiles = []
getTiles(myTiles)
printTiles(myTiles)
##########################################################################################################################################################################################
#                                                                           Write your code below this                                                                                   #
##########################################################################################################################################################################################
# reads the dictionary.txt and inserts all its information into a list.
dictionaryfile=open("dictionary.txt","r")
dictionary=[]
for line in dictionaryfile:
    line=line.strip()
    dictionary.append(line)
dictionaryfile.close()

#                                                                   Task 1:Placing a word on Scrabble board
#                                                            ~Ensure location entered by user is a valid location~

#                                                                       situation 1:follow r:c:d format

# checks if r:c are integers in the possible range of the board.
def validRowAndColumn(loc):
    numbers=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]                 # if r and c is in this range, and is an integer.
    for i in range(len(numbers)):                                   # then it's in the correct format
        if loc[0] == numbers[i]:
            return True
        elif loc[1] ==  numbers[i]:
            return True

# checks if d is only H or V.
def validDirection(loc):
    if loc[2] == 'H' or loc[2] == 'V':                              # if d is only one of this value.
        return True                                                 # then it's in the correct format

#                                                       Situation 2:r and c must be valid.(r/c > 0 & r/c < board size)

# checks if r and c entered by user is valid on board.
def validOnBoard(loc):
    if loc[0] < BOARD_SIZE and loc[0] >= 0 and loc[1] < BOARD_SIZE and loc[1] >= 0:
        return True                                                 # have to be in the range of 0 to BOARD_SIZE to be valid.

# checks if the word is still valid on the board.
def validOnBoard2(word,loc):
    column = loc[1]
    row = loc[0]
    if loc[2] == "H":                                               # for Horizontal
        for i in range(len(word)):                                  # if the letter can be placed outside the Board, return False
            if column+i >= BOARD_SIZE:
                return False
    elif loc[2] == "V" :                                            # for vertical
        for i in range(len(word)):                                  # if letter can be placed outside the Board, return False
            if row+i >= BOARD_SIZE:
                return False


#                                                               Situation 3: first move must start at centre

#checks if r and c is on the centre of the board.
def firstMoveLocation(loc):
    if loc[0] == len(Board) // 2 and loc[1] == len(Board) // 2:
        return True

#                                                                Situation 4: if userInput cannot fit in board.

# Only for first move.
def firstMoveInsertOnBoard(word,loc):
    column = loc[1]
    row = loc[0]
    if loc[2] == "H":                                               # for Horizontal
        for i in range(len(word)):                                  # loop the word in range, and increment the column according to range in word.
            Board[row][column+i] = word[i]                          # replace empty space with the letter
    elif loc[2] == "V" :                                            # for Vertical
        for i in range(len(word)):                                  # loop the word in range, and increment the row according to range in word.
            Board[row+i][column] = word[i]                          # replace empty space with the letter

# After first move.
def insertOnBoard(word,loc,b):
    column = loc[1]
    row = loc[0]
    if loc[2] == "H":                                       # for Horizontal
        count=0                                             # used to count the number of letters colliding with tiles on board.
        for i in range(len(word)):                          # loop according to range of the word, to increment the column of location according to word.
            if b[row][column+i] == word[i]:                 # if the location of space according to the range of word contains a letter that is equal to the letter of word there.
                count+=1                                    # increase the count,
        for j in range(len(word)):                          # which means
            if count >= 1:                                  # atleast one tile on board is used.
                b[row][column+j] = word[j]                  # then only place the tiles.
            else:
                return False
    elif loc[2] == "V" :
        count=0
        for i in range(len(word)):                          # same thing for Vertical
            if b[row+i][column] == word[i]:                 # difference is its incrementing the row according to range of word.
                count+=1
        for j in range(len(word)):
            if count >= 1:
                b[row+j][column] = word[j]
            else:
                return False

#########################################################################################################################################################################################
#                                                               ~Ensure userInput and location follows the rule.

#                                                                       Rule 1: valid English Word

# checks if userInput only contains letters.
def containsNumbersOrWhiteSpace(word):
    toCheck=['0','1','2','3','4','5','6','7','8','9',' ',',','.','/',';','[',']','{','}','"',':',"'",'<','>','?','!','~','`','@','#','$','%','^','&','*','(',')','-','_','+','=']
    for letter in word:
        for i in range(len(toCheck)):                           # if userInput has any of these values, return False
            if letter == toCheck[i]:
                return False

# checks if userInput exists in the dictionary.
def validInDictionary(word):
    n=len(dictionary)
    for i in range(n):
        if word == dictionary[i]:                               # if word is in dictionary, return True
            return True
#                                                                   Rule 2: valid in myTiles and Board
#                                                                   Rule 4: must not change or relocate any existing tile

# checks if userInput contains letters from myTiles.(only applies for first move)
def firstMoveValidTiles(word,toCheck):
    validLettersInWord = []
    TileCheck = toCheck[:]
    n = len(word)

    for letter in word:
        added = 0                                               # added is to make sure only one letter is appended into the List.
        if letter in toCheck:
            if added != 1:                                      # if the letters is in the myTiles,append into list.
                validLettersInWord.append(letter)
                added = 1
                try:
                     TileCheck.remove(letter)                   # if valueError the letter in word is not in myTiles.
                except ValueError:
                    return False

    if len(validLettersInWord)== n:                             # if the appended letters are equal to the length of the word,it means that it is valid
        return True
    else:
        return False

# checks if userInput contains letters in myTiles and the Board.
def validTiles(word,loc):
    validLettersInWord = []
    TileCheck = myTiles[:]
    column = loc[1]
    row = loc[0]
    n = len(word)

    for i in range(len(word)):
        added = 0                                                   # added is to make sure that only one letter is appended.
        n1 = validLettersInWord.count(word[i])
        n2 = myTiles.count(word[i])
        if loc[2] == "H" and Board[row][column+i] == "" :           # for horizontail
            if word[i] in myTiles:                                  # if the position in the Board is empty,
                if added != 1 and n1 <= n2:                         # n1 and n2 is to check if the duplicate letters exists.
                    validLettersInWord.append(word[i])              # append into validLetters list
                    added = 1
        elif loc[2] == "V" and Board[row+i][column] == "":
            if word[i] in myTiles:
                if added != 1 and n1 <= n2:
                    validLettersInWord.append(word[i])
                    added = 1
    for k in range(len(word)):
        if loc[2] == "H":
            if Board[row][column+k] == word[k]:                     # if the tile on board collides with a letter from userInput,
                validLettersInWord.append(word[k])                  # if the letter is the same,append into the list
        elif loc[2] == "V":
            if Board[row+k][column] == word[k]:
                validLettersInWord.append(word[k])
    if len(validLettersInWord)== n:                                 # if the appended letters are equal to the length of the word,it means that it is valid
        return True
    else:
        return False

#                                                                   Rule 3: use atleast one tile from the Board

# checks if atleast one tile is used.
def useTileOnBoard(word,loc):
    column = loc[1]
    row = loc[0]
    if loc[2] == "H":
        emptyCount = 0                                          # used to count the number of letters not colliding with tiles on board.
        for i in range(len(word)):
            if Board[row][column+i] == "":
                emptyCount+=1
                if emptyCount == len(word):                     # if they are equal it means that not atleast one tile on board is used.
                    return False
    elif loc[2] == "V" :
        emptyCount=0
        for i in range(len(word)):
            if Board[row+i][column] == "":
                emptyCount+=1
                if emptyCount == len(word):
                    return False

########################################################################################################################################################################################
#                                                                               ~Background task~

# only removes tiles being used.
def removeTiles(word,loc):
    column = loc[1]
    row = loc[0]
    if loc[2] == "H":
        for i in range(len(word)):
            if Board[row][column+i] == "":                      # if space in Board is empty,remove letter from myTiles.
                myTiles.remove(word[i])
            else:
                pass
    elif loc[2] == "V":
        for i in range(len(word)):
            if Board[row+i][column] == "":
                myTiles.remove(word[i])
            else:
                pass

# counts the Score of word valid in myTiles only,not on Board.
def countScoresNoCond(word):
    counter=0                                                   # counter for getting sum of scores of each letter of user input if it is valid
    for i in range(len(word)):
        for j in range(len(myTiles)):
            if word[i] == myTiles[j]:
                for List in Scores:
                    if word[i] == List[0]:
                        counter += List[1]                      # accumulates the scores of the letter.
    return counter

# counts the scores of the valid word.
def countScores(word,loc):
    column = loc[1]
    row = loc[0]
    count = 0
    for i in range(len(word)):
        added = 0                                              # makes sure it doesn't add twice the scores of a letter
        for j in range(len(myTiles)):
            if loc[2] == "H" and Board[row][column+i] == "" :  # This is the condition for Horizontal direction
                if word[i] == myTiles[j] and added != 1:       # only adding the scores of the letter only if it is not already on the board.
                    for List in Scores:
                        if word[i] == List[0]:
                            count += List[1]
                            added = 1
            elif loc[2] == "V" and Board[row+i][column] == "": # This is the condition for Vertical direction
                if word[i] == myTiles[j] and added != 1:
                    for List in Scores:
                        if word[i] == List[0]:
                            count += List[1]
                            added = 1
    return count
########################################################################################################################################################################################
#                                                                                   ~Rules~

# only applies for first move.
def firstMoveValidUserInput(word):
    if containsNumbersOrWhiteSpace(word) == False:              # Reference Rule 1
        print("Invalid Move!")
    elif validInDictionary(word) != True:                       # Reference Rule 1
        print("This word doesn't exist in the dictionary!")
    elif firstMoveValidTiles(word,myTiles) == False:            # Reference Rule 2 & 4
        print("Invalid Move!")
    else:
        return True

# after first move.
def validUserInput(word,loc):
    if containsNumbersOrWhiteSpace(word) == False:              # Reference Rule 1
        print("Invalid Move!")
    elif validInDictionary(word) != True:                       # Reference Rule 1
        print("This word doesn't exist in the dictionary!")
    elif validTiles(word,loc) == False:                         # Reference Rule 2 & 4
        print("Invalid Move!")
    elif useTileOnBoard(word,loc) == False:                     # Reference Rule 3
        print("Invalid Move!")
    else:
        return True

#########################################################################################################################################################################################
#                                                                               ~Situation(valid location)~

def validFirstMove(word,loc):
    if len(loc) != 3:                                           # if the length of location input by user is less than 3.
        print("Invalid Move!")
    elif validRowAndColumn(loc) != True:                        # Reference Situation 1
        print("Invalid Move!")
    elif validOnBoard(loc) != True:                             # Referece Situation 2
        print("Invalid Move!")
    elif validOnBoard2(word,loc) == False:                      # Referece Situation 2
        print("Invalid Move!")
    elif validDirection(loc) != True:                           # Reference Situation 1
        print("Invalid Move!")
    elif firstMoveLocation(loc) != True:                        # Reference Situation 3
        n = str(len(Board) // 2)
        print("The location in the first move must be " + n + ":" + n + ":" + "H or " + n + ":" + n + ":V")
        print("Invalid Move!!!")
    else:
        return True

def validMove(word,loc):
    if len(loc) != 3:                                           # if the length of location input by user is less than 3.
        print("Invalid Move!")
    elif validRowAndColumn(loc) != True:                        # Reference Situation 1
        print("Invalid Move!")
    elif validDirection(loc) != True:                           # Reference Situation 1
        print("Invalid Move!")
    elif validOnBoard(loc) != True:                             # Reference Situation 2
        print("Invalid Move!")
    elif validOnBoard2(word,loc) == False:                      # Reference Situation 2
        print("Invalid Move!")
    else:
        return True
#########################################################################################################################################################################################
#                                                                   ~Task 2(finding maximum possible score)~
# the tiles that could be use is in myTiles and the tiles on Board.
def availableLetters():
    possibleLetters=myTiles[:]                                  # The tiles in myTiles.
    for j in Board:
        for k in range(len(j)):
            if j[k] != "":
                possibleLetters.append(j[k])                    # The tiles on the Board.
    return possibleLetters

# shortening the dictionary,to reduce time.
def shortenDic():
    dic=[]
    possible =[]
    possibleLetters = availableLetters()

    for word in dictionary:
        if len(word)<=BOARD_SIZE:                               # length of words more than 15 are ignored,because the Board only has max of 15*15 size
            dic.append(word)

    for words in dic:
        if words[0] in possibleLetters:                         # words starting with tiles(in myTiles & Board) are appended into list.
            possible.append(words)
    return possible

# finding words which could be made with tiles in myTiles and Board.
def validWordPossible():
    possibleLetters = availableLetters()                        # contains possible letter from myTiles and tiles on Board.
    validWords = []
    possible = shortenDic()                                     # contains words with letters starting with letters from possibleLetters
    for word in possible:
        validLetterWord=[]                                      # contains letters from possible word which is available in myTiles
        tile=possibleLetters[:]
        n=len(word)
        for letter in word:
            num=possibleLetters.count(letter)
            added = 0
            if letter in possibleLetters :
                if word.count(letter) <= num and added != 1:
                    validLetterWord.append(letter)
                    added = 1
                    try:
                        tile.remove(letter)
                    except ValueError:
                        tile = possibleLetters[:]

            if len(validLetterWord) == n :
                validWords.append(word)
    return validWords

#########################################################################################################################################################################################

# only applies for first move.finds all possible words which can be made in the middle.
def validWordfirstMove():
    validWord = validWordPossible()                             # contains all words which could be made using tiles in myTiles and on Board.
    validFirstMove = []                                         # all correct possible words which can fit the board is appended here.
    n = len(Board)
    location = [n//2,n//2,"H"]                                  # as a point because horizontal or vertical will be the same.
    for word in validWord:
        if validOnBoard2(word,location) != False:               # Reference Situation 2 (check if possible word can be placed on the board with its BOARD_SIZE)
            validFirstMove.append(word)
    return validFirstMove

# checks each possible word if it obeys the rules.
def validity(word,toCheck,loc):
    if validOnBoard2(word,loc) == False:                        # Reference Situation 2 (check if possible word can be placed on the board with its BOARD_SIZE)
        return False
    elif validTiles(word,loc) == False:                         # Reference Rule 2 & 4  (checks if the tiles can make this possible word)
        return False
    elif useTileOnBoard(word,loc) == False:                     # Reference Rule 3      (checks if it uses atleast one tile on board)
        return False
    elif firstMoveValidTiles(word,toCheck) == False:            # Reference Rule 2 & 4  (checks if the possible word uses double letters in the tiles.)
        return False
    else:
        return True

# finds all possible words that could be made horizontally and vertically that obeys the rules above.
def validWord():
    validWords = validWordPossible()                            # contains all words which could be made using tiles in myTiles and on Board.
    validMove = []                                              # all correct possible words that obeys the rules is appended here.

    # FINDS ALL POSSIBLE WORDS HORIZONTALLY
    for i in range(len(Board)):
        temp = myTiles[:]
        for j in range(len(Board[i])):
            if Board[i][j] != "":
                temp.append(Board[i][j])                        # contains letters in myTiles and tiles on each row of the Board, and appends one by one the tiles of each row and testing.
                for k in range(len(Board)):
                    location = [i,k,"H"]
                    if temp != myTiles:                         # ignores if temp only contains letters of myTiles,(because there will be no possible words there at that row)
                        for word in validWords:
                            if validity(word,temp,location) == True: # the RULES.
                                p = [word,location]
                                if validMove == []:
                                    validMove.append(p)
                                elif validMove[-1] == p:
                                    pass
                                else:
                                    validMove.append(p)
    # FINDS ALL POSSIBLE WORDS VERTICALLY.
    for i in range(len(Board)):
        temp = myTiles[:]
        for j in range(len(Board[i])):
            if Board[j][i] != "":
                temp.append(Board[j][i])                        # contains letters in myTiles and tiles on each column of the Board, and appends one by one the tiles of each column and testing.
                for k in range(len(Board)):
                    location = [k,i,"V"]
                    if temp != myTiles:                         # ignores if temp only contains letters of myTiles,(because there will be no possible words there at that column)
                        for word in validWords:
                            if validity(word,temp,location) == True:
                                p = [word,location]
                                if validMove == []:
                                    validMove.append(p)
                                elif validMove[-1] == p:
                                    pass
                                else:
                                    validMove.append(p)

    return validMove

############################################################################################################################################################################################
# finds max possible words in a list and prints them out(first move only)
def maxPossibleWordFM(uInput,loc):
    validFirstMove = validWordfirstMove()
    validWordScores=[]
    num = len(Board)
    location = [num//2,num//2,"H"]                                  # location of first move.

    for word in validFirstMove:
        validWordScores.append(countScoresNoCond(word))             # Reference Background tasks.

    m = 0
    n = len(validWordScores)                                        # to get the possible word with maximum score,
    for i in range(1,n):
        first=validWordScores[i-1]                                  # find the maximum score in the validWordScores first.
        second=validWordScores[i]                                   # and then get the index of where it is located,
        if first > second and first > m:                            # and use that index to get the word and location in the validMove list.
            m=first
        elif second > first and second > m:
            m=second
        else:
            m=m

    index=validWordScores.index(m)
    if uInput == validFirstMove[index] and loc == location:         # if userinput and location is the same as the max possible word.
        print("Your move was the best move. Well done!")
    elif countScoresNoCond(uInput) == m:                            # if score of userinput is the same as the max possible score.
        print("Your move is one of the best moves.Well done!")
    print("Maximum possible score in this move was " + str(m) + " with word " + validFirstMove[index] + " at " + str(location[0]) + ":" + str(location[1]) + ":" + location[2])

# finds in possible words list, the word with the maximum score and prints them out.
def maxPossibleWord(uInput,loc):
    validMove = validWord()                                         # contains all the possible words with their locations.
    validWordScores = []                                            # used to append all the scores of each word.

    for i in range(len(validMove)):
        validWordScores.append(countScores(validMove[i][0],validMove[i][1])) # Reference Background Tasks.

    m = 0
    n = len(validWordScores)                                        # to get the possible word with maximum score,
    for i in range(1,n):
        first=validWordScores[i-1]                                  # find the maximum score in the validWordScores first.
        second=validWordScores[i]                                   # and then get the index of where it is located,
        if first > second and first > m:                            # and use that index to get the word and location in the validMove list.
            m=first
        elif second > first and second > m:
            m=second
        else:
            m=m

    index=validWordScores.index(m)
    location = validMove[index][1]
    if uInput == validMove[index][0] and loc == location:           # if userinput and location is the same as the max possible word.
        print("Your move was the best move. Well done!")
    elif countScores(uInput,loc) == m:                              # if scores of userinput is the same as maximum possible score.
        print("Your move is one of the best moves.Well done!")
    print("Maximum possible score in this move was " + str(m) + " with word " + validMove[index][0] + " at " + str(location[0]) + ":" + str(location[1]) + ":" + location[2])

#########################################################################################################################################################################################
#                                                                               ~Main Execution~
counter = 0                                                         # used to break the loop by incrementing it.
totalScore = 0                                                      # used to accumulate score valid userinput each round.
while counter < 1:
    userInput = input("\nEnter your word:")
    userInput = userInput.upper()
    if userInput == "***":
        counter += 2
    else:
        location = input("Enter the location in row:col:direction format:")
        location = location.split(":")
        for i in range(len(location)):
            try:
                location[i] = int(location[i])                      # converts r and c from string into integer.
            except ValueError:
                pass                                                # pass d because, its always "H" or "V".
#     EXECUTION FOR FIRST MOVE ONLY.
        if Board == initializeBoard(BOARD_SIZE):
            if validFirstMove(userInput,location) == True and firstMoveValidUserInput(userInput) == True:
                maxPossibleWordFM(userInput,location)               # reference Task 2 codes.
                score = countScores(userInput,location)
                totalScore += score                                 # accumulate score.
                print("Your score in this move:" + str(score))
                print("Your total score is:" + str(totalScore))
                removeTiles(userInput,location)                     # remove tiles that have been used.
                firstMoveInsertOnBoard(userInput,location)          # Reference Situation 4
                printBoard(Board)
                getTiles(myTiles)
                printTiles(myTiles)
#     EXECUTION AFTER FIRST MOVE.
        else:
            if validMove(userInput,location) == True and validUserInput(userInput,location) == True:
                maxPossibleWord(userInput,location)                   # reference Task 2 codes
                score = countScores(userInput,location)
                totalScore += score                                   # accumulate scores.
                print("Your score in this move:" + str(score))
                print("Your total score is:" + str(totalScore))
                removeTiles(userInput,location)
                if insertOnBoard(userInput,location,Board) == False:  # Reference Situation 4
                    print("Invalid Move!")
                else:
                    printBoard(Board)
                    getTiles(myTiles)
                    printTiles(myTiles)
#########################################################################################################################################################################################
