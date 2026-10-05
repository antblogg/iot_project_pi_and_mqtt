import tkinter as tk
from tkinter import ttk

from common.Dashboard import Dashboard

class AnalyticsDashboard(Dashboard):
    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root)
        self._initializeHeader()
        self.buildMainPanel(self.getMainPanel())
        self.buildSidePanel(self.getSidePanel())

    def _initializeHeader(self):
        self.setHeaderText(
        toptext="SENSOR MONITOR  /  LAPTOP",
        middletext="Temperature",
        bottomtext="Recent readings and statistical summary"
        )
        self.setHeaderStatus(True, "No alarm")


    def buildSidePanel(self, sidePanelFrame):
        ttk.Label(sidePanelFrame, text="Summary", style="Section.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(sidePanelFrame, text="LATEST READING", style="Muted.TLabel").grid(row=1, column=0, sticky="w", pady=(24, 2))
        ttk.Label(sidePanelFrame, text="--", style="Reading.TLabel").grid(row=2, column=0, sticky="w")
        ttk.Label(sidePanelFrame, text="degrees C", style="Muted.TLabel").grid(row=3, column=0, sticky="w", pady=(0, 18))

        separator = tk.Frame(sidePanelFrame, height=1, background=self.COLORS["line"])
        separator.grid(row=4, column=0, sticky="ew", pady=(0, 12))

        for row_index, label in enumerate(("Mean", "Std. deviation", "Median", "Minimum", "Maximum", "Mode"), start=5):
            ttk.Label(sidePanelFrame, text=label, style="StatName.TLabel").grid(row=row_index, column=0, sticky="w", pady=8)
            ttk.Label(sidePanelFrame, text="--", style="StatValue.TLabel").grid(row=row_index, column=1, sticky="e", padx=(20, 0))

    def buildMainPanel(self, mainPanelFrame):
        self.chart_canvas = tk.Canvas(
            mainPanelFrame,
            background=self.COLORS["surface"],
            highlightthickness=0,
            height=360,
        )
        self.chart_canvas.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(16, 0))
        self.chart_canvas.bind("<Configure>", self._draw_chart_placeholder)

    # todo kill
    def _draw_chart_placeholder(self, event=None) -> None:
        canvas = self.chart_canvas
        canvas.delete("all")
        width = max(canvas.winfo_width(), 1)
        height = max(canvas.winfo_height(), 1)
        left, right, top, bottom = 44, width - 16, 20, height - 34

        for step in range(5):
            y = top + (bottom - top) * step / 4
            canvas.create_line(left, y, right, y, fill=self.COLORS["line"])
        for step in range(5):
            x = left + (right - left) * step / 4
            canvas.create_line(x, top, x, bottom, fill=self.COLORS["line"])

        canvas.create_text(12, top, text="C", anchor="w", fill=self.COLORS["muted"], font=("Segoe UI", 9))
        canvas.create_text(
            (left + right) / 2,
            (top + bottom) / 2,
            text="Waiting for temperature data",
            fill=self.COLORS["ink"],
            font=("Segoe UI", 12, "bold"),
        )
        canvas.create_text(
            (left + right) / 2,
            (top + bottom) / 2 + 24,
            text="The chart will appear when readings are available",
            fill=self.COLORS["muted"],
            font=("Segoe UI", 9),
        )