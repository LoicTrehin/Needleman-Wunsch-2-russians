from tabulate import tabulate
import time
import math

def get_input_values():
    # Create two string variables S and T
    S = input("Enter the value for S: ")
    T = input("Enter the value for T: ")

    # Return the length of S and T
    print("Length of S:", len(S))
    print("Length of T:", len(T))

    # Create three numeric variables Match, Mismatch, and gap
    Match = int(input("Enter the value for Match: "))
    Mismatch = int(input("Enter the value for Mismatch: "))
    Gap = int(input("Enter the value for gap: "))

    return S, T, Match, Mismatch, Gap

def printMatrix(matrix, S, T):
    # add space to the string to print the matrix because of [0][0] = 0
    printS = " " + S
    printT = " " + T
    #convert the string to list to be able to print it
    printS = list(printS)
    printT = list(printT)
    print(tabulate(matrix, headers=printT, showindex=printS, tablefmt="grid"))

def create_and_initialize_matrix(S, T, Gap):
    # Create a 2D array of size (len(S)+1) * (len(T)+1) to store the score
    matrix = [[None] * (len(T) + 1) for _ in range(len(S) + 1)]
    # Create a 2D array of size (len(S)+1) * (len(T)+1) to store the direction
    directionmatrix = [[None] * (len(T) + 1) for _ in range(len(S) + 1)]
    # Initialize the first element of the matrix
    matrix[0][0] = 0

    # Initialize the first row and column of the matrix
    for i in range(1, len(S) + 1):
        matrix[i][0] = matrix[i-1][0] + Gap

    for j in range(1, len(T) + 1):
        matrix[0][j] = matrix[0][j-1] + Gap
    
    # Initialize the first row and column of the direction matrix
    for i in range(1, len(S) + 1):
        directionmatrix[i][0] = 'U'
    for j in range(1, len(T) + 1):
        directionmatrix[0][j] = 'L'

    return matrix, directionmatrix

def fill_matrix(matrix, directionmatrix, S, T, Match, Mismatch, Gap):
    for i in range(1, len(S) + 1):
        for j in range(1, len(T) + 1):
            # case of match or mismatch
            if S[i-1] == T[j-1]:
                dscore = matrix[i-1][j-1] + Match
            else:
                dscore = matrix[i-1][j-1] + Mismatch
            # case of gap
            lscore = matrix[i][j-1] + Gap
            uscore = matrix[i-1][j] + Gap
            # Fill the matrix with the maximum score and it's direction
            matrix[i][j], directionmatrix[i][j] = max((dscore, 'D'), (lscore, 'L'), (uscore, 'U'))
    
    return matrix, directionmatrix

def traceback(direction_matrix, S, T):
    # Initialize the alignement variables
    alignement1 = ""
    alignement2 = ""
    i, j = len(S), len(T)

    while i > 0 or j > 0:
        # case of match or mismatch
        if direction_matrix[i][j] == 'D':
            alignement1 = S[i-1] + alignement1
            alignement2 = T[j-1] + alignement2
            i -= 1
            j -= 1
        # case of gap up
        elif direction_matrix[i][j] == 'U':
            alignement1 = S[i-1] + alignement1
            alignement2 = "-" + alignement2
            i -= 1
        # case of gap left
        elif direction_matrix[i][j] == 'L':
            alignement1 = "-" + alignement1
            alignement2 = T[j-1] + alignement2
            j -= 1
        else:
            break  # Avoid infinite loop

    return alignement1, alignement2

# ask the user for the input values
S, T, Match, Mismatch, Gap = get_input_values()
start_time = time.process_time()

# create and initialize the matrix
matrix, directionmatrix = create_and_initialize_matrix(S, T, Gap)

# fill the matrixs with the score and direction with classic method
matrix, directionmatrix = fill_matrix(matrix, directionmatrix, S, T, Match, Mismatch, Gap)

# traceback to get the alignement
alignement1, alignement2 = traceback(directionmatrix, S, T)

# Calculate the execution time
end_time = time.process_time()
execution_time = end_time - start_time

if len(S)<=30 and len(T)<=30:
    print("\n Score Matrix:")
    printMatrix(matrix, S, T)
    print("\n Direction Matrix:")
    printMatrix(directionmatrix, S, T)


## Print the alignement
print("\nAlignement 1:", alignement1)
print("Alignement 2:", alignement2)
print(f"\nExecution Time : {execution_time} secondes.")
