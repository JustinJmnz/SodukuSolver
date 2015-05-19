'''
Created on Sep 26, 2014

@author: justin
'''
import sys
import numpy as np
from __builtin__ import False, str
from numpy.matrixlib.defmatrix import matrix

global finished
def next_coordinate(row, col):
    """
    Returns the next coordinate to explore in a sudoku puzzle, regardless of
    whether or not the cell is actually empty. The order is left to right,
    top to bottom.
    """
    if col == 8:
        return row + 1, 0
    else:
        return row, col + 1

def solve(M, row=0, col=0):
    """
    Recursively solves a Sudoku puzzle starting at the given row and column.
    Note that two assumptions are made:
    
    1. All positions to the left and above of the starting position are filled
    2. All filled in cells are valid (no duplicates as in the Sudoku rules)

    Note that the second assumption does NOT imply that the puzzle is solvable.

    M - A numpy matrix representing a Sudoku board. Initially, cells with
        value 0 are considered empty, and cells with other values are
        considered fixed.
    row - the current row
    col - the current column
    """
    # Find the first empty cell from [row, col]. Stop if we pass the end of the
    # puzzle.
    while row < 9 and M[row,col] != 0:
        row, col = next_coordinate(row, col)

    # If we passed the last row (row 8) then we've solved the puzzle, so just
    # return true.
    if row == 9:
        return True

    # Otherwise, we need to do the standard guessing logic below:
    # Find forbidden values.
    F = set()

    # Find all values in the same column
    for k in range(9):
        F.add(M[row,k])

    # Find all values in the same row
    for k in range(9):
        F.add(M[k,col])

    # Slightly trickier, we also need the numbers in the 3x3 grid containing
    # the number. box_row and box_col are the row and column of the top left
    # cell in the current box.
#     print row
    box_row = row - row%3
    box_col = col - col%3

    # Now check the 3x3 box starting at box_row, box_col
    for k in range(3):
        for l in range(3):
            F.add(M[box_row+k, box_col+l])
    
    possibleCombinations = set([1,2,3,4,5,6,7,8,9])
    possibleValues = possibleCombinations.difference(F)
    pList = list(possibleValues)
    if(row == 9 & col == 9):
        return True
    if(M[row,col] != 0):
        r,c = next_coordinate(row, col)
        solve(M, r,c)
    else:
        for i in pList:
            M[row,col] = i
            r,c = next_coordinate(row, col)
            if(solve(M,r, c)): 
                print M
                global finished
                finished = M.tolist()
                return True
        
#     
#     
#     if(row == 9 & col == 9):
#         return True
#     if(M[row,col] != 0):
#         r,c = next_coordinate(row, col)
#         solve(M, r,c)
#     else:
#         possibleValues = possibleValues.difference(F) # All values in possibleValues, but not in F
#         p = list(possibleValues)
#         print possibleValues
#         for location in possibleValues:
#             M[row][col] = location
#             r,c = next_coordinate(row, col)
#             solve(M,r,c)
#             print M
#         while k < 10:
#  
#             if(k not in possibleValues): # if k is not in possibleValues
#                 k = k + 1 # increment k
# #                 if(k == 9): # if k = 9, set value to 0
# #                     M[row,col] = 0
# #                     return False
#             else: # k is in possibleValues
#  
#                 M[row,col] = k
#                 print M
#                 row, col = next_coordinate(row, col)
#                 
#                 else:
#                     k = k + 1
#     
    M[row,col] = 0
    return False

def main():
    args = sys.argv[1:]
    if not args:
        print 'usage: argument_test.py [file path]'
        sys.exit(1)
    ''' If you will use one argument only'''
    filepath = args[0]
    print filepath
    fileopener = open(filepath)
    datalists=[]
    data = fileopener.readlines()
    for row in data:
        datarow = row.replace('\n','')
        datarow = datarow.replace(' ','')
        datarow = datarow.replace('.','0')
        datalists.append(list(datarow))
    print datalists
    dataarray = np.matrix(datalists, dtype=np.int)
    print dataarray
    if(solve(dataarray)):
        print 'SOLVED'
        global finished
        file = open("soduku_solved.txt","w+")
        for i in finished:
            file.write(str(i)+'\n')
        
    else:
        print "NOT SOLVED"
    fileopener.close()

if __name__ == '__main__':
    main()
    pass
