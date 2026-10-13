import tkinter as tk
from tkinter import ttk
from pathlib import Path
import json
from requests.structures import CaseInsensitiveDict
from pymongo import MongoClient
import pymongo
import time
import numpy as np

from analytics.Dashboard import Dashboard

class AnalyticsDashboard(Dashboard):
    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root)
        configPath = Path(__file__).parents[1] / "secrets" / "config.json"
        with open(configPath, "r") as f:
            self.config = CaseInsensitiveDict(json.load(f))["mongodb"]

        self.summaryTitleVar = tk.StringVar(self.root, "Summary") # const
        self.latestReadingTitleVar = tk.StringVar(self.root, "LATEST READING") # const
        self.latestReadingVar = tk.StringVar(self.root, "--")
        self.unitsVar = tk.StringVar(self.root, "degrees C") # const

        self.meanVar = tk.StringVar(self.root, "--")
        self.stdVar = tk.StringVar(self.root, "--")
        self.medianVar = tk.StringVar(self.root, "--")
        self.minVar = tk.StringVar(self.root, "--")
        self.maxVar = tk.StringVar(self.root, "--")
        self.modeVar = tk.StringVar(self.root, "--")

        self._initializeHeader()
        self.buildMainPanel(self.getMainPanel())
        self.buildSidePanel(self.getSidePanel())
        self.alarmState = False

        connectionString = self.config["connectionsstring"]
        self.mongoClient = MongoClient(connectionString)
        self.mongoCollection = self.mongoClient[self.config["database"]][self.config["collection"]]

        self.data = self.hitDatabase()
        self.root.after(100, self.update)

    def update(self):
    
        self.data = self.hitDatabase()
        self.updateplot()
        self.updateSidePanel()
        
        self.root.after(1000, self.update)
        pass

    def hitDatabase(self):
        timeWindow = 60 # seconds
        targetTime = time.asctime(
            time.localtime(
                time.time()-timeWindow
            )
        )
        self.data = self.mongoCollection.find(
            {
                "timestamp":
                {
                    "$gte": targetTime
                }
            }
        ).sort("timestamp",pymongo.DESCENDING).to_list()
        return self.data

    @staticmethod
    def _formatFloat(f):
        return str(f)[:4]
                                              
    def updateSidePanel(self):
        data = self.data
        temperatures = [float(d.get("Temperature")) for d in data]
        latest = temperatures[0]

        self.latestReadingVar.set(self._formatFloat(latest))
        self.meanVar.set(self._formatFloat(np.mean(temperatures)))
        self.stdVar.set(self._formatFloat(np.std(temperatures)))
        self.medianVar.set(self._formatFloat(np.median(temperatures)))
        self.minVar.set(self._formatFloat(np.min(temperatures)))
        self.maxVar.set(self._formatFloat(np.max(temperatures)))

        u,c = np.unique(temperatures,return_counts=True)
        m = u[np.argmax(c)]
        self.modeVar.set(self._formatFloat(m))


    def updateplot(self):
        canvas = self.chart_canvas
        canvas.delete("all")

        width = max(canvas.winfo_width(), 1)
        height = max(canvas.winfo_height(), 1)

        left, right = 50, width - 20
        top, bottom = 20, height - 40


        readings = [
            float(row["Temperature"])
            for row in reversed(self.data)
            if "Temperature" in row
        ]

        if len(readings) < 2:
            self._draw_chart_placeholder()
            return

        YMIN = 15
        YMAX = 35

        def temp_to_y(temp):
            return bottom - (temp - YMIN) / (YMAX - YMIN) * (bottom - top)

        # Grid and Y-axis labels
        for step in range(5):
            y = top + (bottom - top) * step / 4

            canvas.create_line(
                left,
                y,
                right,
                y,
                fill=self.COLORS["line"]
            )

            temp = YMAX - (YMAX - YMIN) * step / 4

            canvas.create_text(
                left - 8,
                y,
                text=f"{temp:.0f}",
                anchor="e",
                fill=self.COLORS["muted"],
                font=("Segoe UI", 8),
            )

        # Vertical grid lines
        for step in range(6):
            x = left + (right - left) * step / 5

            canvas.create_line(
                x,
                top,
                x,
                bottom,
                fill=self.COLORS["line"]
            )

        # Alarm lines
        y_low = temp_to_y(18)
        y_high = temp_to_y(28)

        canvas.create_line(
            left,
            y_low,
            right,
            y_low,
            fill="#D9534F",
            width=2,
            dash=(6, 4),
        )

        canvas.create_text(
            right - 5,
            y_low - 8,
            text="Low alarm limit (18°C)",
            anchor="e",
            fill="#D9534F",
            font=("Segoe UI", 8, "bold"),
        )

        canvas.create_line(
            left,
            y_high,
            right,
            y_high,
            fill="#D9534F",
            width=2,
            dash=(6, 4),
        )

        canvas.create_text(
            right - 5,
            y_high - 8,
            text="High alarm limit (28°C)",
            anchor="e",
            fill="#D9534F",
            font=("Segoe UI", 8, "bold"),
        )
        canvas.create_text(
            left,
            top - 8,
            text=f"Min: {min(readings):.1f}°C",
            anchor="w",
            fill=self.COLORS["muted"],
            font=("Segoe UI", 8),
        )

        canvas.create_text(
            right,
            top - 8,
            text=f"Max: {max(readings):.1f}°C",
            anchor="e",
            fill=self.COLORS["muted"],
            font=("Segoe UI", 8),
        )

        # Data points
        points = []

        for i, temp in enumerate(readings):
            x = left + i * (right - left) / (len(readings) - 1)
            y = temp_to_y(temp)

            points.append((x, y))

        # Area fill under curve
        polygon = [
            left,
            bottom,
            *[coord for pt in points for coord in pt],
            right,
            bottom,
        ]

        canvas.create_polygon(
            polygon,
            fill="#4F8EF7",
            stipple="gray25",
            outline="",
        )

        # Trend line
        for p1, p2 in zip(points[:-1], points[1:]):
            canvas.create_line(
                *p1,
                *p2,
                fill="#4F8EF7",
                width=3,
                smooth=True,
            )

        # Markers
        for x, y in points:
            canvas.create_oval(
                x - 3,
                y - 3,
                x + 3,
                y + 3,
                fill="#4F8EF7",
                outline="",
            )

        # Latest reading highlight
        latest = readings[-1]
        lx, ly = points[-1]
        self.alarmState = True if latest > 28 or latest < 18 else False
        if self.alarmState:
            self.setHeaderStatus(False, "Alarm triggered!")
        else:
            self.setHeaderStatus(True, "No alarm")
        latest_color = ("#D9534F" if self.alarmState else "#428A10")
        self.summaryTitleLabel.config(foreground=latest_color) # this line is wrong
        canvas.create_oval(
            lx - 5,
            ly - 5,
            lx + 5,
            ly + 5,
            fill= latest_color,
            outline="",
        )

        canvas.create_text(
            lx,
            ly - 16,
            text=f"{latest:.1f}°C",
            fill=self.COLORS["ink"],
            font=("Segoe UI", 9, "bold"),
        )

        canvas.create_text(
            left,
            height - 12,
            text="Last 60 seconds",
            anchor="w",
            fill=self.COLORS["muted"],
            font=("Segoe UI", 8),
        )


    def _initializeHeader(self):
        self.setHeaderText(
        toptext="SENSOR MONITOR",
        middletext="Temperature",
        bottomtext="Recent readings and statistical summary"
        )
        self.setHeaderStatus(True, "No alarm")


    def buildMainPanel(self, mainPanelFrame):
        self.chart_canvas = tk.Canvas(
            mainPanelFrame,
            background=self.COLORS["surface"],
            highlightthickness=0,
            height=360,
        )
        self.chart_canvas.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(16, 0))

    def buildSidePanel(self, sidePanelFrame):

        ttk.Label(
            sidePanelFrame,
            textvariable=self.summaryTitleVar,
            style="Section.TLabel"
        ).grid(row=0, column=0, sticky="w")

        ttk.Label(
            sidePanelFrame,
            textvariable=self.latestReadingTitleVar,
            style="Muted.TLabel"
        ).grid(row=1, column=0, sticky="w", pady=(24, 2))

        self.summaryTitleLabel =ttk.Label(
            sidePanelFrame,
            textvariable=self.latestReadingVar,
            style="Reading.TLabel"
        )
        self.summaryTitleLabel.grid(row=2, column=0, sticky="w")
        ttk.Label(
            sidePanelFrame,
            textvariable=self.unitsVar,
            style="Muted.TLabel"
        ).grid(row=3, column=0, sticky="w", pady=(0, 18))

        separator = tk.Frame(
            sidePanelFrame,
            height=1,
            background=self.COLORS["line"]
        )
        separator.grid(row=4, column=0, sticky="ew", pady=(0, 12))

        stats = (
            ("Mean", self.meanVar),
            ("Std. deviation", self.stdVar),
            ("Median", self.medianVar),
            ("Minimum", self.minVar),
            ("Maximum", self.maxVar),
            ("Mode", self.modeVar),
        )

        for row_index, (label, valueVar) in enumerate(stats, start=5):
            ttk.Label(
                sidePanelFrame,
                text=label,
                style="StatName.TLabel"
            ).grid(row=row_index, column=0, sticky="w", pady=8)

            ttk.Label(
                sidePanelFrame,
                textvariable=valueVar,
                style="StatValue.TLabel"
            ).grid(row=row_index, column=1, sticky="e", padx=(20, 0))