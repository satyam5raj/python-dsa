"""
================================================================
MATH PROBLEMS 81-90: PATTERN LOGIC
================================================================
Print visual patterns using nested loops
"""

# ================================================================
# PROBLEM 81: Solid rectangle
# ================================================================
def solid_rectangle(rows: int, cols: int):
    """
    * * * *
    * * * *
    * * * *

    INTERVIEW SCRIPT:
    "Outer loop: rows. Inner loop: columns.
     Print star for each (row, col) combination."
    """
    for i in range(rows):
        print('* ' * cols)

# ================================================================
# PROBLEM 82: Hollow rectangle
# ================================================================
def hollow_rectangle(rows: int, cols: int):
    """
    * * * *
    *     *
    *     *
    * * * *

    INTERVIEW SCRIPT:
    "Print star if: first/last row OR first/last column.
     Otherwise: print space."
    """
    for i in range(rows):
        for j in range(cols):
            if i == 0 or i == rows-1 or j == 0 or j == cols-1:
                print('*', end=' ')
            else:
                print(' ', end=' ')
        print()

# ================================================================
# PROBLEM 83: Half pyramid (left-aligned)
# ================================================================
def half_pyramid(n: int):
    """
    *
    * *
    * * *
    * * * *

    INTERVIEW SCRIPT:
    "Row i has i stars. Nested loop: outer for rows, inner for stars."
    """
    for i in range(1, n+1):
        print('* ' * i)

# ================================================================
# PROBLEM 84: Inverted pyramid
# ================================================================
def inverted_pyramid(n: int):
    """
    * * * * *
    * * * *
    * * *
    * *
    *

    INTERVIEW SCRIPT:
    "Row i (1-indexed) has n-i+1 stars."
    """
    for i in range(n, 0, -1):
        print('* ' * i)

# ================================================================
# PROBLEM 85: Full pyramid (center-aligned)
# ================================================================
def full_pyramid(n: int):
    """
        *
       * *
      * * *
     * * * *
    * * * * *

    INTERVIEW SCRIPT:
    "Row i: (n-i) leading spaces, then i stars (each separated by space).
     Alternatively: 2*i-1 stars with single spaces."
    """
    for i in range(1, n+1):
        spaces = ' ' * (n - i)
        stars = '* ' * i
        print(spaces + stars)

# ================================================================
# PROBLEM 86: Diamond pattern
# ================================================================
def diamond(n: int):
    """
       *
      * *
     * * *
    * * * *
    * * * *
     * * *
      * *
       *

    INTERVIEW SCRIPT:
    "Upper half: rows 1..n (like full pyramid).
     Lower half: rows n-1..1 (inverted)."
    """
    # Upper half
    for i in range(1, n+1):
        print(' ' * (n-i) + '* ' * i)
    # Lower half
    for i in range(n-1, 0, -1):
        print(' ' * (n-i) + '* ' * i)

# ================================================================
# PROBLEM 87: Butterfly pattern
# ================================================================
def butterfly(n: int):
    """
    *       *
    * *   * *
    * * * * *
    * * * * *
    * *   * *
    *       *

    INTERVIEW SCRIPT:
    "Upper half row i: i stars, 2*(n-i) spaces, i stars.
     Lower half is mirror of upper."
    """
    # Upper half
    for i in range(1, n+1):
        stars = '* ' * i
        spaces = '  ' * (2*(n-i))
        print(stars + spaces + stars)
    # Lower half
    for i in range(n, 0, -1):
        stars = '* ' * i
        spaces = '  ' * (2*(n-i))
        print(stars + spaces + stars)

# ================================================================
# PROBLEM 88: Pascal's triangle
# ================================================================
def pascals_triangle(n: int) -> list:
    """
       1
      1 1
     1 2 1
    1 3 3 1
    1 4 6 4 1

    INTERVIEW SCRIPT:
    "Each row starts and ends with 1.
     Middle elements: row[i][j] = row[i-1][j-1] + row[i-1][j].
     Build row by row."
    """
    triangle = []
    for i in range(n):
        row = [1] * (i+1)
        for j in range(1, i):
            row[j] = triangle[i-1][j-1] + triangle[i-1][j]
        triangle.append(row)
        padding = ' ' * (n - i - 1)
        print(padding + ' '.join(map(str, row)))
    return triangle

def pascals_triangle_row(row_num: int) -> list:
    """
    Get specific row using C(n,k) formula — O(n) time

    INTERVIEW SCRIPT:
    "Row n: C(n,0), C(n,1), ..., C(n,n).
     C(n,k) = C(n,k-1) * (n-k+1) / k.
     Each element computed from previous in O(1)."
    """
    row = [1]
    for k in range(1, row_num+1):
        row.append(row[-1] * (row_num - k + 1) // k)
    return row

# ================================================================
# PROBLEM 89: Number pyramid
# ================================================================
def number_pyramid(n: int):
    """
         1
        2 2
       3 3 3
      4 4 4 4
     5 5 5 5 5

    INTERVIEW SCRIPT:
    "Row i: (n-i) leading spaces, then digit i printed i times."
    """
    for i in range(1, n+1):
        print(' ' * (n-i) + f'{i} ' * i)

def number_triangle(n: int):
    """
    1
    1 2
    1 2 3
    1 2 3 4
    """
    for i in range(1, n+1):
        print(' '.join(str(j) for j in range(1, i+1)))

# ================================================================
# PROBLEM 90: Binary pattern
# ================================================================
def binary_pattern(n: int):
    """
    1
    0 1
    1 0 1
    0 1 0 1
    1 0 1 0 1

    INTERVIEW SCRIPT:
    "Row i starts with i%2 (0 for even row, 1 for odd).
     Alternate 0 and 1 across each row."
    """
    for i in range(1, n+1):
        row = []
        val = i % 2  # starting value alternates by row
        for j in range(i):
            row.append(str(val))
            val = 1 - val  # toggle
        print(' '.join(row))

def checkerboard(n: int):
    """
    Checkerboard pattern of 0s and 1s
    1 0 1 0
    0 1 0 1
    1 0 1 0
    0 1 0 1
    """
    for i in range(n):
        for j in range(n):
            print((i+j)%2, end=' ')
        print()

# ================================================================
# BONUS: NUMBER PATTERNS
# ================================================================
def floyd_triangle(n: int):
    """
    1
    2 3
    4 5 6
    7 8 9 10
    """
    num = 1
    for i in range(1, n+1):
        for j in range(i):
            print(num, end=' ')
            num += 1
        print()

def mirror_number_triangle(n: int):
    """
    1 2 3 4 5
    1 2 3 4
    1 2 3
    1 2
    1
    """
    for i in range(n, 0, -1):
        print(' '.join(str(j) for j in range(1, i+1)))

# ================================================================
# TEST ALL
# ================================================================
if __name__ == "__main__":
    N = 5
    print("=== PATTERN LOGIC ===")
    print("81. Solid rectangle 3x4:")
    solid_rectangle(3, 4)
    print("\n82. Hollow rectangle 4x5:")
    hollow_rectangle(4, 5)
    print("\n83. Half pyramid n=5:")
    half_pyramid(5)
    print("\n84. Inverted pyramid n=5:")
    inverted_pyramid(5)
    print("\n85. Full pyramid n=5:")
    full_pyramid(5)
    print("\n86. Diamond n=4:")
    diamond(4)
    print("\n87. Butterfly n=4:")
    butterfly(4)
    print("\n88. Pascal's triangle n=5:")
    pascals_triangle(5)
    print("\n89. Number pyramid n=5:")
    number_pyramid(5)
    print("\n90. Binary pattern n=5:")
    binary_pattern(5)
