'''
Variety of functions related to computing the edit distance between
strings and, importantly, which WILL be used by the DistleGame to
provide feedback to the DistlePlayer during a game of Distle.

[!] Feel free to use any of these methods as needed in your DistlePlayer.

[!] Feel free to ADD any methods you see fit for use by your DistlePlayer,
e.g., some form of entropy computation.
'''

def get_edit_dist_table(row_str: str, col_str: str) -> list[list[int]]:
    '''
    Returns the completed Edit Distance memoization structure: a 2D list
    of ints representing the number of string manupulations required to
    minimally turn each subproblem's string into the other.
    
    Parameters:
        row_str (str):
            The string located along the table's rows
        col_str (col):
            The string located along the table's columns
    
    Returns:
        list[list[int]]:
            Completed memoization table for the computation of the
            edit_distance(row_str, col_str)
    '''
    
    rows, cols = len(row_str), len(col_str)
    memo_table: list[list[int]] = []
    memo_table = [[0] * (cols + 1) for item in range(rows + 1)]
    
    for col_index in range(1, cols + 1):
        memo_table[0][col_index] = col_index

    for row_index in range(1, rows + 1):
        memo_table[row_index][0] = row_index

    for row_index in range(1, rows + 1):
        for col_index in range(1, cols + 1):
            delete_value = insert_value = replace_value = transpose_value = rows + cols + 1
            delete_value = memo_table[row_index - 1][col_index] + 1
            insert_value = memo_table[row_index][col_index - 1] + 1
            replace_value = memo_table[row_index - 1][col_index - 1] 
            
            if row_str[row_index - 1] != col_str[col_index - 1]:
                replace_value += 1

            transpose_value = rows + cols + 1
            if (
                row_index + col_index > 2 and
                row_str[row_index - 1] == col_str[col_index - 2] and 
                row_str[row_index - 2] == col_str[col_index - 1]
            ):
                transpose_value = memo_table[row_index - 2][col_index - 2] + 1
                
            memo_table[row_index][col_index] = min(delete_value, insert_value, replace_value, transpose_value)
    return memo_table



def edit_distance(s0: str, s1: str) -> int:
    '''
    Returns the edit distance between two given strings, defined as an
    int that counts the number of primitive string manipulations (i.e.,
    Insertions, Deletions, Replacements, and Transpositions) minimally
    required to turn one string into the other.
    
    [!] Given as part of the skeleton, no need to modify
    
    Parameters:
        s0, s1 (str):
            The strings to compute the edit distance between
    
    Returns:
        int:
            The minimal number of string manipulations
    '''
    if s0 == s1: return 0
    return get_edit_dist_table(s0, s1)[len(s0)][len(s1)]


def get_transformation_list(s0: str, s1: str) -> list[str]:
    '''
    Returns one possible sequence of transformations that turns String s0
    into s1. The list is in top-down order (i.e., starting from the largest
    subproblem in the memoization structure) and consists of Strings representing
    the String manipulations of:
        1. "R" = Replacement
        2. "T" = Transposition
        3. "I" = Insertion
        4. "D" = Deletion
    In case of multiple minimal edit distance sequences, returns a list with
    ties in manipulations broken by the order listed above (i.e., replacements
    preferred over transpositions, which in turn are preferred over insertions, etc.)
    
    [!] Given as part of the skeleton, no need to modify
    
    Example:
        s0 = "hack"
        s1 = "fkc"
        get_transformation_list(s0, s1) => ["T", "R", "D"]
        get_transformation_list(s1, s0) => ["T", "R", "I"]
    
    Parameters:
        s0, s1 (str):
            Start and destination strings for the transformation
    
    Returns:
        list[str]:
            The sequence of top-down manipulations required to turn s0 into s1
    '''
    
    return get_transformation_list_with_table(s0, s1, get_edit_dist_table(s0, s1))

def get_transformation_list_with_table(s0: str, s1: str, table: list[list[int]]) -> list[str]:
    '''
    See get_transformation_list documentation.
    
    This method does exactly the same thing as get_transformation_list, except that
    the memoization table is input as a parameter. This version of the method can be
    used to save computational efficiency if the memoization table was pre-computed
    and is being used by multiple methods.
    
    [!] MUST use the already-solved memoization table and must NOT recompute it.
    [!] MUST be implemented recursively (i.e., in top-down fashion)
    '''
    return transformation_list_with_table(s0, s1, [], get_edit_dist_table(s0, s1))
    
def transformation_list_with_table(s0: str, s1: str, complete_transform_list: list[str], table: list[list[int]]) -> list[str]:
    '''
    Generates a list of transformation operations (Insert, Delete, Replace, Transpose) to convert string s0 into string s1
    using the provided memoization table.

    This function traces the transformation path based on a memoization table, which contains 
    the minimum edit distances for substrings of s0 and s1.

    Args:
        s0 (str): The source string.
        s1 (str): The target string.
        complete_transform_list (list[str]): A list to store the sequence of transformation operations.
        table (list[list[int]]): The memoization table containing the minimum edit distances between substrings of s0 and s1.

    Returns:
        list[str]: A list of transformation operations ('I', 'D', 'R', 'T') necessary to change s0 into s1.
    '''
    row_index: int = len(s0)
    col_index: int = len(s1)
    memo_table = table
    
    def get_transformation(s0: str, s1: str, row_index: int, col_index: int, transform_list: list[str], memo_table: list[list[int]]) -> list[str]:
        """
        Recursively traces back through the memoization table to generate a sequence of transformation operations 
        (Insert, Delete, Replace, Transpose) that converts string s0 into string s1.

        This function uses the provided memoization table, which contains the minimum edit distances between substrings 
        of s0 and s1, to identify the optimal transformation path. It compares the values for each operation (insert, 
        delete, replace, and transpose) and appends the corresponding operation ('I', 'D', 'R', 'T') to the 
        transformation list. The recursive trace follows the minimal-cost path, with tiebreaker priorities: 
        Replace ('R') > Transpose ('T') > Insert ('I') > Delete ('D').

        Args:
            s0 (str): The original string.
            s1 (str): The target string.
            row_index (int): The current row index in the memoization table.
            col_index (int): The current column index in the memoization table.
            transform_list (list[str]): A list to accumulate the sequence of transformation operations.
            memo_table (list[list[int]]): The memoization table that stores the minimum edit distances for substrings of s0 and s1.

        Returns:
            list[str]: A list of transformation operations ('I', 'D', 'R', 'T') that transform s0 into s1.
        """
        # If goal position in tabel reached, return transformations
        if row_index == 0 and col_index == 0:
            return transform_list[::-1]
        
        #Get values from table
        current_value = memo_table[row_index][col_index]
        delete_value = insert_value = replace_value = transpose_value = len(s0) + len(s1) + 1 # >> [AM] What's the point of this line if you immediately replace the values below

        delete_value = memo_table[row_index - 1][col_index] 
        insert_value = memo_table[row_index][col_index - 1] 

        replace_value = memo_table[row_index - 1][col_index - 1]
        if s0[row_index - 1] != s1[col_index - 1]:
            replace_value += 1
            
        transpose_value = memo_table[row_index - 2][col_index - 2]


        # Tiebreaker implementation with recursion
        if replace_value <= current_value and (row_index > 0 and col_index > 0):
            if s0[row_index - 1] != s1[col_index - 1]:
                transform_list.append('R')
            return get_transformation(s0, s1, row_index - 1, col_index - 1, transform_list, memo_table)

        if transpose_value <= current_value and (row_index > 1 and col_index > 1 and 
                                                 s0[row_index - 1] == s1[col_index - 2] and 
                                                 s0[row_index - 2] == s1[col_index - 1]):
            transform_list.append('T')
            return get_transformation(s0, s1, row_index - 2, col_index - 2, transform_list, memo_table)

        if insert_value <= current_value and col_index > 0:
            transform_list.append('I')
            return get_transformation(s0, s1, row_index, col_index - 1, transform_list, memo_table)
        
        if delete_value <= current_value and row_index > 0:
            transform_list.append('D')
            return get_transformation(s0, s1, row_index - 1, col_index, transform_list, memo_table)
        
        else:
            return []

    # Handles empty strings
    if col_index <= 0: # >> [AM] probably best to put this code at the top of the function so you don't waste time with the other calculations if it's an empty string
        while row_index > 0:
            complete_transform_list.append('D')
            row_index -= 1
    elif row_index <= 0:
        while col_index > 0:
            complete_transform_list.append('I')
            col_index -= 1
    else:       
        get_transformation(s0, s1, row_index, col_index, complete_transform_list, memo_table) # Root call
        
    return complete_transform_list

# ===================================================
# >>> [AM] Summary
# Excellent submission that has a ton to like and was
# obviously well-tested. Generally clean style (apart
# from a few quibbles noted above), and shows
# strong command of programming foundations alongside
# data structure and algorithmic concepts. Keep up
# the great work!
# ---------------------------------------------------
# >>> [AM] Style Checklist
# [X] = Good, [~] = Mixed bag, [ ] = Needs improvement
#
# [X] Variables and helper methods named and used well
# [X] Proper and consistent indentation and spacing
# [X] Proper docstrings provided for ALL methods
# [X] Logic is adequately simplified
# [X] Code repetition is kept to a minimum
# ---------------------------------------------------
# Correctness:          100 / 100
# -> EditDistUtils:      20 / 20  (-2 / missed test)
# -> DistlePlayer:      283 / 265 (-1 / below threshold; max -30)
# Mypy Penalty:        -0 (-4 if mypy wasn't clean)
# Style Penalty:       -0
# Total:                100 / 100
# ===================================================