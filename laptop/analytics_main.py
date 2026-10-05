
from common.Dashboard import Dashboard

import json
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from analytics.AnalyticsDashboard import AnalyticsDashboard


# connect to database
# read the temperature data from the last N seconds
# calculate mean, standard deviation, median, minimum, maximum, and mode
# round the mode to the nearest degree
# plot the data and shade the alarm region
# display the mean and standard deviation on the plot
# display the statistics and whether an alarm is triggered


def main():
    root = tk.Tk()
    AnalyticsDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()