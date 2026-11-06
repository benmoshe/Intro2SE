"""
=====================================================================
                    NumPy Basics - Intro to Python Libraries
=====================================================================

What is NumPy?
    NumPy ("Numerical Python") is THE library for working with numbers
    in Python. Its main object is the "array" (ndarray) - like a Python
    list, but:
        1. MUCH faster (written in C under the hood)
        2. Lets you do math on ALL elements at once (no loops needed!)
        3. Supports multi-dimensional data (tables / matrices)

Install:
    pip install numpy

Run this file:
    python 1_numpy_basics.py
"""

# The convention is to import numpy as "np" - everyone does this,
# so you'll see "np." everywhere online.
import numpy as np


# =====================================================================
# 1. CREATING ARRAYS
# =====================================================================
print("=" * 50)
print("1. CREATING ARRAYS")
print("=" * 50)

# From a regular Python list
grades = np.array([85, 92, 78, 95, 88])
print("From a list:      ", grades)

# np.zeros(n) -> array of n zeros (useful as a "starting point")
print("np.zeros(5):      ", np.zeros(5))

# np.ones(n) -> array of n ones
print("np.ones(3):       ", np.ones(3))

# np.arange(start, stop, step) -> like range(), but returns an array
# NOTE: 'stop' is NOT included (same as range)
print("np.arange(0,10,2):", np.arange(0, 10, 2))

# np.linspace(start, stop, num) -> 'num' evenly spaced numbers
# NOTE: here 'stop' IS included. Very useful for plotting!
print("np.linspace(0,1,5):", np.linspace(0, 1, 5))

# Random numbers - np.random.randint(low, high, size)
print("Random ints:      ", np.random.randint(1, 7, size=5))  # 5 dice rolls


# =====================================================================
# 2. ARRAY PROPERTIES
# =====================================================================
print("\n" + "=" * 50)
print("2. ARRAY PROPERTIES")
print("=" * 50)

# A 2D array = a list of lists (think: a table / matrix)
matrix = np.array([[1, 2, 3],
                   [4, 5, 6]])

print(matrix)
print("shape:", matrix.shape)   # (rows, columns) -> (2, 3)
print("size: ", matrix.size)    # total number of elements -> 6
print("ndim: ", matrix.ndim)    # number of dimensions -> 2
print("dtype:", matrix.dtype)   # type of the elements -> int64


# =====================================================================
# 3. MATH ON ARRAYS (the magic of NumPy!)
# =====================================================================
print("\n" + "=" * 50)
print("3. MATH ON ARRAYS")
print("=" * 50)

# With a regular list, to add 5 to each element you need a loop:
regular_list = [85, 92, 78, 95, 88]
with_loop = [g + 5 for g in regular_list]
print("Python list + loop:", with_loop)

# With NumPy - the operation is applied to EVERY element automatically.
# This is called "vectorization".
print("NumPy grades + 5:  ", grades + 5)
print("NumPy grades * 2:  ", grades * 2)
print("NumPy grades / 10: ", grades / 10)

# Two arrays of the same size -> element-by-element operation
a = np.array([1, 2, 3])
b = np.array([10, 20, 30])
print("a + b =", a + b)  # [11 22 33]
print("a * b =", a * b)  # [10 40 90]

# Common math functions work on whole arrays too
print("np.sqrt(a):", np.sqrt(a))


# =====================================================================
# 4. STATISTICS / AGGREGATION FUNCTIONS
# =====================================================================
print("\n" + "=" * 50)
print("4. STATISTICS")
print("=" * 50)

print("grades:", grades)
print("sum:    ", np.sum(grades))     # also: grades.sum()
print("mean:   ", np.mean(grades))    # average
print("median: ", np.median(grades))  # middle value
print("std:    ", np.std(grades))     # standard deviation (spread)
print("min/max:", np.min(grades), "/", np.max(grades))
print("argmax: ", np.argmax(grades))  # INDEX of the max value (not the value!)

# On 2D arrays you can choose the direction with 'axis':
#   axis=0 -> down the columns (one result per column)
#   axis=1 -> across the rows   (one result per row)
print("\nmatrix:\n", matrix)
print("sum of each column (axis=0):", matrix.sum(axis=0))  # [5 7 9]
print("sum of each row    (axis=1):", matrix.sum(axis=1))  # [6 15]


# =====================================================================
# 5. INDEXING, SLICING AND FILTERING
# =====================================================================
print("\n" + "=" * 50)
print("5. INDEXING, SLICING AND FILTERING")
print("=" * 50)

# Indexing & slicing work just like Python lists
print("grades[0]:  ", grades[0])     # first element
print("grades[-1]: ", grades[-1])    # last element
print("grades[1:4]:", grades[1:4])   # elements at index 1,2,3

# In 2D: matrix[row, column]
print("matrix[1, 2]:", matrix[1, 2])   # row 1, column 2 -> 6
print("matrix[:, 0]:", matrix[:, 0])   # ALL rows, column 0 -> [1 4]

# Boolean filtering - a VERY useful NumPy feature.
# Step 1: a condition gives back an array of True/False
print("grades > 90:          ", grades > 90)
# Step 2: use that True/False array to pick only the matching elements
print("grades[grades > 90]:  ", grades[grades > 90])


# =====================================================================
# 6. RESHAPING
# =====================================================================
print("\n" + "=" * 50)
print("6. RESHAPING")
print("=" * 50)

numbers = np.arange(1, 7)            # [1 2 3 4 5 6]
print("original:", numbers)

# reshape(rows, cols) - same data, new shape.
# rows * cols MUST equal the number of elements (here 2*3 = 6)
print("reshape(2, 3):\n", numbers.reshape(2, 3))
print("reshape(3, 2):\n", numbers.reshape(3, 2))

# .T -> transpose (swap rows and columns)
print("transpose of matrix:\n", matrix.T)


# =====================================================================
# QUICK SUMMARY
# =====================================================================
#   np.array(list)          -> create an array
#   np.zeros / ones / arange / linspace -> quick array creation
#   arr.shape / arr.size    -> array dimensions
#   arr + 5, arr * arr      -> math on every element (no loops!)
#   np.mean / sum / max ... -> statistics
#   arr[arr > x]            -> filtering
#   arr.reshape(r, c)       -> change shape
