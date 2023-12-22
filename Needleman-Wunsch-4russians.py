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

def determine_best_t(n):
    """
    Determines the best value of t that is a divisor of n and closest to the square root of n.

    Args:
        n (int): The number for which the best value of t needs to be determined.

    Returns:
        int: The best value of t.

    """
    # calculate the square root of n that as mignitude simalar to log(n)
    sqrt_n = math.sqrt(n)

    # initialize the minimum difference to a very high number
    min_diff = float('inf')
    best_t = None

    # loop to find the divisor of n that is closest to the square root of n
    for i in range(1, n + 1):
        if n % i == 0:
            t = i + 1  # t is the divisor + 1
            diff = abs(sqrt_n - (t - 1))  # find the difference from the square root of n
            if diff < min_diff:
                min_diff = diff
                best_t = t

    return best_t

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

def calculate_n_blocs(t, s):
    """
    Calculate the number of blocks on a line or column.

    Parameters:
    t (int): The total number of elements in line or column in the matrix.
    s (int): The number of elements in each block.

    Returns:
    int: The number of blocks.
    """
    matrix_s = t+1
 
    for i in range (1, matrix_s):
        sum = (s-1)*i+1
        if matrix_s - sum == 0:
            break
    return i

def fill_matrixlookuptable(matrix, directionmatrix, S, T, tS, tT, n_blockS, n_blockT, Match, Mismatch, Gap):
    """
    Fills the lookup table with block matrices and direction matrices.

    Args:
        matrix (list): The main matrix.
        directionmatrix (list): The main direction matrix.
        S (str): The sequence S.
        T (str): The sequence T.
        tS (int): The size of each block in S.
        tT (int): The size of each block in T.
        n_blockS (int): The number of blocks in S.
        n_blockT (int): The number of blocks in T.
        Match (int): The score for a match.
        Mismatch (int): The score for a mismatch.
        Gap (int): The score for a gap.

    Returns:
        tuple: A tuple containing the lookup table, the updated main matrix, and the updated main direction matrix.
    """
    lookuptable = []
    for i in range(1, n_blockS + 1):
        for j in range(1, n_blockT + 1):
            #initialize the block matrix of size tS*tT
            tempmatrixblock = [[None] * (tT) for _ in range(tS)]
            #fill the block matrix with its first column and line from the main matrix
            tempmatrixblock = [row[((j-1)*tT)-(j-1):(j*tT)-(j-1)]for row in matrix [((i-1)*tS)-(i-1):(i*tS)-(i-1)]]
            # create the block to save directions for trace back
            directionmatrixblock = [[None] * (tT) for _ in range(tS)]
            #took subsequence of S and T to fill the block matrix
            blockS = S[((i-1)*tS)-(i-1):(i*tS)-(i-1)-1]
            blockT = T[((j-1)*tT)-(j-1):(j*tT)-(j-1)-1]
            #fill the block matrix with the score and direction
            tempmatrixblock, directionmatrixblock = fill_matrix(tempmatrixblock, directionmatrixblock, blockS, blockT, Match, Mismatch, Gap)
            #save the block matrix and direction matrix in the lookup table
            block = [tempmatrixblock, directionmatrixblock]
            lookuptable.append(block)

            # save the direction block matrix content in the main direction matrix
            for l, row in enumerate(directionmatrixblock):
                for m, value in enumerate(row):
                    #check if value already present to avoid overwriting
                    if  directionmatrix[((i-1)*tS)-(i-1)+ l][((j-1)*tT)-(j-1) + m] == None:
                        directionmatrix[((i-1)*tS)-(i-1)+ l][((j-1)*tT)-(j-1) + m] = value
            
            # save the block matrix content in the main matrix
            # save the last row of the block matrix in the main matrix
            matrix[(i*tS)-i][((j-1)*tT)-(j-1):(j*tT)-(j-1)]= tempmatrixblock[-1]
            # save the last column of the block matrix in the main matrix
            for k in range(len(tempmatrixblock)):
                matrix[((i-1)*tS)-(i-1)+k][(j*tT)-j] = tempmatrixblock[k][-1]
            
    return lookuptable, matrix, directionmatrix


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

# determine the best value of t block tS*tT size
tS = determine_best_t(len(S))
tT = determine_best_t(len(T))
print("height of the block:", tS)
print("width of the block:", tT)

# calculate the number of blocks of size tS and the last block length
n_blockS = calculate_n_blocs(len(S), tS)

# calculate the number of blocks of size tT and the last block length
n_blockT = calculate_n_blocs(len(T), tT)
print ("number of blokcs in one column:", n_blockS)
print ("number of blokcs in one line:", n_blockT)

# create and initialize the matrix
matrix, directionmatrix = create_and_initialize_matrix(S, T, Gap)

# fill the matrixs with the score and direction with lookup table
lookuptable, matrix, directionmatrix = fill_matrixlookuptable(matrix, directionmatrix, S, T, tS, tT, n_blockS, n_blockT, Match, Mismatch, Gap)

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