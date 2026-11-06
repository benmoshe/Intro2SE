"""
=====================================================================
                    Pandas Basics - Intro to Python Libraries
=====================================================================

What is Pandas?
    Pandas is the library for working with TABLES of data (think: Excel
    in Python). It is built on top of NumPy.

    Two main objects:
        1. Series    -> a single column (1D, with labels)
        2. DataFrame -> a full table (rows + named columns)

Install:
    pip install pandas

Run this file:
    python 2_pandas_basics.py
"""

# The convention is to import pandas as "pd"
import pandas as pd


# =====================================================================
# 1. CREATING A DATAFRAME
# =====================================================================
print("=" * 50)
print("1. CREATING A DATAFRAME")
print("=" * 50)

# The easiest way: a dictionary where
#   key   = column name
#   value = list of values in that column
data = {
    "name":   ["Dana", "Yossi", "Noa", "Avi", "Maya", "Tom"],
    "age":    [21, 23, 22, 25, 21, 24],
    "course": ["SE", "OOP", "SE", "OOP", "SE", "OOP"],
    "grade":  [88, 75, 95, 62, 91, 80],
}

df = pd.DataFrame(data)   # "df" is the common name for a DataFrame
print(df)

# In real life you usually LOAD data from a file instead:
#   df = pd.read_csv("students.csv")
#   df = pd.read_excel("students.xlsx")


# =====================================================================
# 2. EXPLORING THE DATA (first thing you do with a new dataset!)
# =====================================================================
print("\n" + "=" * 50)
print("2. EXPLORING THE DATA")
print("=" * 50)

print("head(3) - first 3 rows:")
print(df.head(3))         # df.tail(3) gives the LAST 3 rows

print("\nshape:", df.shape)            # (rows, columns)
print("columns:", list(df.columns))    # column names

print("\ninfo() - column types & missing values:")
df.info()

print("\ndescribe() - quick statistics on numeric columns:")
print(df.describe())


# =====================================================================
# 3. SELECTING COLUMNS AND ROWS
# =====================================================================
print("\n" + "=" * 50)
print("3. SELECTING DATA")
print("=" * 50)

# One column -> returns a Series
print("df['name']:")
print(df["name"])

# Several columns -> pass a LIST of names -> returns a DataFrame
print("\ndf[['name', 'grade']]:")
print(df[["name", "grade"]])

# Rows by position -> .iloc[] ("integer location")
print("\ndf.iloc[0] - the first row:")
print(df.iloc[0])

# Rows/cells by label -> .loc[row, column]
print("\ndf.loc[2, 'name']:", df.loc[2, "name"])


# =====================================================================
# 4. FILTERING ROWS (like NumPy boolean filtering!)
# =====================================================================
print("\n" + "=" * 50)
print("4. FILTERING")
print("=" * 50)

# Students with grade above 85
print("grade > 85:")
print(df[df["grade"] > 85])

# Combine conditions with & (and) / | (or)
# IMPORTANT: each condition must be inside parentheses!
print("\nSE students with grade > 90:")
print(df[(df["course"] == "SE") & (df["grade"] > 90)])


# =====================================================================
# 5. ADDING & MODIFYING COLUMNS
# =====================================================================
print("\n" + "=" * 50)
print("5. ADDING COLUMNS")
print("=" * 50)

# New column computed from an existing one (applied to every row)
df["bonus_grade"] = df["grade"] + 5

# New True/False column based on a condition
df["passed"] = df["grade"] >= 70

print(df)


# =====================================================================
# 6. SORTING
# =====================================================================
print("\n" + "=" * 50)
print("6. SORTING")
print("=" * 50)

# ascending=False -> highest first
print(df.sort_values("grade", ascending=False))


# =====================================================================
# 7. GROUPING (the most powerful basic feature)
# =====================================================================
print("\n" + "=" * 50)
print("7. GROUPING")
print("=" * 50)

# groupby = "split the table into groups, then calculate per group"
# Here: the average grade for each course
print("Average grade per course:")
print(df.groupby("course")["grade"].mean())

# How many students in each course?
print("\nStudents per course:")
print(df["course"].value_counts())


# =====================================================================
# 8. SAVING TO A FILE
# =====================================================================
print("\n" + "=" * 50)
print("8. SAVING")
print("=" * 50)

# index=False -> don't write the row numbers (0,1,2...) into the file
df.to_csv("students_output.csv", index=False)
print("Saved to students_output.csv")


# =====================================================================
# QUICK SUMMARY
# =====================================================================
#   pd.DataFrame(dict) / pd.read_csv(file) -> create / load a table
#   df.head() / df.info() / df.describe()  -> explore the data
#   df["col"] / df[["a", "b"]]             -> select columns
#   df.iloc[i] / df.loc[row, col]          -> select rows / cells
#   df[df["col"] > x]                      -> filter rows
#   df["new"] = ...                        -> add a column
#   df.sort_values("col")                  -> sort
#   df.groupby("col")["other"].mean()      -> statistics per group
#   df.to_csv(file)                        -> save
