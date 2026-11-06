"""
=====================================================================
                Matplotlib Basics - Intro to Python Libraries
=====================================================================

What is Matplotlib?
    Matplotlib is the most popular Python library for drawing graphs
    and charts. We use its "pyplot" module, which gives simple
    functions like plot(), bar(), scatter(), etc.

    The basic recipe for EVERY graph:
        1. Prepare the data (x values, y values)
        2. Draw it            -> plt.plot(...) / plt.bar(...) / ...
        3. Decorate it        -> title, axis labels, legend, grid
        4. Show it            -> plt.show()

Install:
    pip install matplotlib numpy

Run this file:
    python 3_matplotlib_basics.py
    (each graph opens in a window - CLOSE IT to see the next one)
"""

# The convention is to import pyplot as "plt"
import matplotlib.pyplot as plt
import numpy as np   # we use numpy to easily create data


# =====================================================================
# 1. LINE PLOT - the most basic graph
#    Good for: showing how something changes over time
# =====================================================================

# Step 1: data
days = [1, 2, 3, 4, 5, 6, 7]
temperature = [22, 24, 23, 26, 28, 27, 25]

# Step 2: draw
plt.plot(days, temperature)

# Step 3: decorate - ALWAYS label your graphs!
plt.title("Temperature During the Week")
plt.xlabel("Day")
plt.ylabel("Temperature (°C)")

# Step 4: show
plt.show()


# =====================================================================
# 2. CUSTOMIZING A LINE PLOT + MULTIPLE LINES
# =====================================================================

# np.linspace gives us 100 evenly spaced points between 0 and 2*pi
# -> a smooth curve
x = np.linspace(0, 2 * np.pi, 100)

# Useful style options:
#   color     -> "red", "blue", "green", ...
#   linestyle -> "-" solid, "--" dashed, ":" dotted
#   linewidth -> thickness of the line
#   label     -> the name that appears in the legend
plt.plot(x, np.sin(x), color="blue", linestyle="-", linewidth=2, label="sin(x)")
plt.plot(x, np.cos(x), color="red", linestyle="--", label="cos(x)")

plt.title("Sine vs Cosine")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()   # shows the 'label' of each line
plt.grid(True) # adds a background grid - easier to read values
plt.show()


# =====================================================================
# 3. BAR CHART
#    Good for: comparing values between categories
# =====================================================================

languages = ["Python", "Java", "C++", "JavaScript"]
students = [45, 30, 15, 25]

plt.bar(languages, students, color="skyblue")
# Tip: plt.barh(...) draws HORIZONTAL bars - better for long names

plt.title("Favorite Programming Language")
plt.xlabel("Language")
plt.ylabel("Number of Students")
plt.show()


# =====================================================================
# 4. SCATTER PLOT
#    Good for: checking if there's a relationship between two values
# =====================================================================

study_hours = [1, 2, 2, 3, 4, 5, 5, 6, 7, 8]
exam_grade = [55, 60, 58, 65, 70, 75, 78, 82, 88, 95]

# Each (x, y) pair becomes a single dot
plt.scatter(study_hours, exam_grade, color="green", marker="o")

plt.title("Study Hours vs Exam Grade")
plt.xlabel("Hours Studied")
plt.ylabel("Grade")
plt.show()
# -> We can SEE that more hours = higher grade (positive correlation)


# =====================================================================
# 5. HISTOGRAM
#    Good for: seeing how values are DISTRIBUTED
#    (how many values fall in each range)
# =====================================================================

# 1000 random grades around 75 (mean=75, standard deviation=10)
grades = np.random.normal(loc=75, scale=10, size=1000)

# bins = how many "buckets" to split the range into
# edgecolor makes the borders of the bars visible
plt.hist(grades, bins=20, color="orange", edgecolor="black")

plt.title("Distribution of Grades")
plt.xlabel("Grade")
plt.ylabel("Number of Students")
plt.show()


# =====================================================================
# 6. SUBPLOTS - several graphs in ONE window
# =====================================================================

# plt.subplots(rows, cols) creates a grid of graphs.
#   fig  -> the whole window
#   axes -> a list of the individual graphs (one per cell)
fig, axes = plt.subplots(1, 2, figsize=(10, 4))  # figsize = (width, height) in inches

# NOTE: with axes we use set_title / set_xlabel instead of title / xlabel
axes[0].plot(days, temperature, marker="o")
axes[0].set_title("Line Plot")
axes[0].set_xlabel("Day")

axes[1].bar(languages, students)
axes[1].set_title("Bar Chart")

plt.tight_layout()   # prevents the graphs from overlapping

# Save the figure to a file (do this BEFORE plt.show()!)
plt.savefig("my_subplots.png")
plt.show()


# =====================================================================
# QUICK SUMMARY
# =====================================================================
#   plt.plot(x, y)        -> line plot       (change over time)
#   plt.bar(x, h)         -> bar chart       (compare categories)
#   plt.scatter(x, y)     -> scatter plot    (relationship between 2 values)
#   plt.hist(data, bins)  -> histogram       (distribution)
#   plt.title / xlabel / ylabel / legend / grid -> decorations
#   plt.subplots(r, c)    -> several graphs in one window
#   plt.savefig("f.png")  -> save to file
#   plt.show()            -> display
