from tabulate import tabulate
import time
import math

def get_input_values():
    """
    Prompt the user to enter input values for the Needleman-Wunsch algorithm.

    Returns:
        tuple: A tuple containing the input values - S (str), T (str), Match (int), Mismatch (int), Gap (int).
    """
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
    """
    Print the matrix in a tabular format.

    Args:
        matrix (list): The matrix to be printed.
        S (str): The first sequence.
        T (str): The second sequence.
    """
    # add space to the string to print the matrix because of [0][0] = 0
    printS = " " + S
    printT = " " + T
    #convert the string to list to be able to print it
    printS = list(printS)
    printT = list(printT)
    print(tabulate(matrix, headers=printT, showindex=printS, tablefmt="grid"))

def create_and_initialize_matrix(S, T, Gap):
    """
    Create and initialize a matrix for the Needleman-Wunsch algorithm.

    Args:
        S (str): The first sequence.
        T (str): The second sequence.
        Gap (int): The gap penalty.

    Returns:
        tuple: A tuple containing two matrices - the score matrix and the direction matrix.
    """
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
    """
    Fill the score and direction matrices using the Needleman-Wunsch algorithm.

    Args:
        matrix (list): The score matrix.
        directionmatrix (list): The direction matrix.
        S (str): The first sequence.
        T (str): The second sequence.
        Match (int): The score for a match.
        Mismatch (int): The score for a mismatch.
        Gap (int): The gap penalty.

    Returns:
        tuple: A tuple containing the updated score matrix and direction matrix.
    """
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
            # Fill the matrix with the maximum score and its direction
            matrix[i][j], directionmatrix[i][j] = max((dscore, 'D'), (lscore, 'L'), (uscore, 'U'))
    
    return matrix, directionmatrix

def traceback(direction_matrix, S, T):
    """
    Perform traceback to obtain the optimal alignment.

    Args:
        direction_matrix (list): The direction matrix.
        S (str): The first sequence.
        T (str): The second sequence.

    Returns:
        tuple: A tuple containing the two aligned sequences.
    """
    # Initialize the alignment variables
    alignment1 = ""
    alignment2 = ""
    i, j = len(S), len(T)

    while i > 0 or j > 0:
        # case of match or mismatch
        if direction_matrix[i][j] == 'D':
            alignment1 = S[i-1] + alignment1
            alignment2 = T[j-1] + alignment2
            i -= 1
            j -= 1
        # case of gap up
        elif direction_matrix[i][j] == 'U':
            alignment1 = S[i-1] + alignment1
            alignment2 = "-" + alignment2
            i -= 1
        # case of gap left
        elif direction_matrix[i][j] == 'L':
            alignment1 = "-" + alignment1
            alignment2 = T[j-1] + alignment2
            j -= 1
        else:
            break  # Avoid infinite loop

    return alignment1, alignment2

# ask the user for the input values
S, T, Match, Mismatch, Gap = get_input_values()
start_time = time.process_time()

# create and initialize the matrix
matrix, directionmatrix = create_and_initialize_matrix(S, T, Gap)

# fill the matrices with the score and direction using the Needleman-Wunsch algorithm
matrix, directionmatrix = fill_matrix(matrix, directionmatrix, S, T, Match, Mismatch, Gap)

# perform traceback to obtain the optimal alignment
alignment1, alignment2 = traceback(directionmatrix, S, T)

# Calculate the execution time
end_time = time.process_time()
execution_time = end_time - start_time

if len(S)<=30 and len(T)<=30:
    print("\n Score Matrix:")
    printMatrix(matrix, S, T)
    print("\n Direction Matrix:")
    printMatrix(directionmatrix, S, T)

# Print the alignment
print("\nAlignment 1:", alignment1)
print("Alignment 2:", alignment2)
print(f"\nExecution Time : {execution_time} seconds.")
