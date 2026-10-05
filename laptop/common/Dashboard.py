import json
import tkinter as tk
from tkinter import ttk
from typing import Optional
def load_config() -> dict:
    config_path = __file__+"/../../config.json"
    with open(config_path, "r") as f:
        config = json.load(f) 
    return config

class Dashboard:
    COLORS = {
        "background": "#F1F5F3",
        "surface": "#FFFFFF",
        "ink": "#20332F",
        "muted": "#73817D",
        "line": "#E1E9E5",
        "accent": "#D66C4D",
        "accent_light": "#F9E9E3",
        "status": "#E5F2EB",
        "status_ink_success": "#347452",
        "status_ink_failure": "#E66C5D",
    }

    def __init__(self, root: tk.Tk ) -> None:
        #self.headerConfig = GuiBox
        #self.header = GuiBox
        self.root = root
        self.config = load_config()

        self.root.geometry("980x640")
        self.root.minsize(760, 520)
        self.root.configure(background=self.COLORS["background"])
 
        self._configureStyles()
        self._buildLayout()

    def setTitle(self, title: str):
        self.root.title(title)
        
    def getHeader(self):
        return self.headerFrame

    def getMainPanel(self):
        return self.mainPanelFrame

    def getSidePanel(self):
        return self.sidePanelFrame


    def _configureStyles(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("App.TFrame", background=self.COLORS["background"])
        style.configure("Card.TFrame", background=self.COLORS["surface"])
        style.configure("Eyebrow.TLabel", background=self.COLORS["background"], foreground=self.COLORS["muted"], font=("Segoe UI", 9, "bold"))
        style.configure("Title.TLabel", background=self.COLORS["background"], foreground=self.COLORS["ink"], font=("Segoe UI", 25, "bold"))
        style.configure("Subtitle.TLabel", background=self.COLORS["background"], foreground=self.COLORS["muted"], font=("Segoe UI", 10))
        style.configure("Section.TLabel", background=self.COLORS["surface"], foreground=self.COLORS["ink"], font=("Segoe UI", 12, "bold"))
        style.configure("Muted.TLabel", background=self.COLORS["surface"], foreground=self.COLORS["muted"], font=("Segoe UI", 9))
        style.configure("Reading.TLabel", background=self.COLORS["surface"], foreground=self.COLORS["accent"], font=("Segoe UI", 30, "bold"))
        style.configure("StatName.TLabel", background=self.COLORS["surface"], foreground=self.COLORS["muted"], font=("Segoe UI", 10))
        style.configure("StatValue.TLabel", background=self.COLORS["surface"], foreground=self.COLORS["ink"], font=("Segoe UI", 10, "bold"))

    def _buildLayout(self) -> None:
        self.rootFrame = ttk.Frame(self.root, style="App.TFrame", padding=(28, 24))
        self.rootFrame.pack(fill="both", expand=True)

        self.headerFrame = self._buildHeader(self.rootFrame) 
        
        bodyFrame = self._buildBody(self.rootFrame)
        self.mainPanelFrame = self._buildMainPanel(bodyFrame)
        self.sidePanelFrame = self._buildSidePanel(bodyFrame)

    def _buildBody(self, parent: ttk.Frame):
        bodyFrame = ttk.Frame(parent, style="App.TFrame")
        bodyFrame.pack(fill="both", expand=True, pady=(24, 0))
        bodyFrame.columnconfigure(0, weight=1)
        bodyFrame.columnconfigure(1, weight=0)
        bodyFrame.rowconfigure(0, weight=1)
        return bodyFrame

    def _buildSidePanel(self, parent: ttk.Frame) -> None:
        sidePanelFrame = ttk.Frame(parent, style="Card.TFrame", padding=20)
        sidePanelFrame.grid(row=0, column=1, sticky="ns")
        sidePanelFrame.columnconfigure(0, weight=1)
        return sidePanelFrame


    def _buildHeader(self, rootFrame: ttk.Frame) -> None:
        headerFrame = ttk.Frame(rootFrame, style="App.TFrame")
        headerFrame.pack(fill="x")

        # TODO remove default values and leave it to the subclass
        self.header_toptext = tk.StringVar(self.root,"--")
        self.header_middletext = tk.StringVar(self.root, "--")
        self.header_bottomtext =  tk.StringVar(self.root,"--" )

        titleAreaFrame = ttk.Frame(headerFrame, style="App.TFrame")
        titleAreaFrame.pack(side="left", fill="x", expand=True)
        ttk.Label(titleAreaFrame, textvariable=self.header_toptext, style="Eyebrow.TLabel").pack(anchor="w", pady=(0, 5))
        ttk.Label(titleAreaFrame, textvariable=self.header_middletext, style="Title.TLabel").pack(anchor="w")
        ttk.Label(titleAreaFrame, textvariable=self.header_bottomtext, style="Subtitle.TLabel").pack(anchor="w", pady=(3, 0))
        self.headerStatusLabel = tk.Label(
            headerFrame,
            text= "No alarm tiggered",
            bg=self.COLORS["status"],
            fg=self.COLORS["status_ink_failure"],
            font=("Segoe UI", 9, "bold"),
            padx=14,
            pady=10,
        )
        self.headerStatusLabel.pack(side="right", anchor="n", pady=(10, 0))

    def setHeaderText(self,
                         toptext: Optional[str] = None,
                         middletext: Optional[str] = None,
                         bottomtext: Optional[str] = None
                         ):
        if toptext is None: toptext = self.header_toptext.get()
        if middletext is None: middletext = self.header_middletext.get()
        if bottomtext is None: bottomtext = self.header_bottomtext.get()
        self.header_toptext.set(toptext)
        self.header_middletext.set(middletext)
        self.header_bottomtext.set(bottomtext)

    def setHeaderStatus(self,isStatusSuccess: bool, text: str):
        self.headerStatusLabel.config(
            text = text,
            fg = self.COLORS["status_ink_success"] if isStatusSuccess else self.COLORS["status_ink_failure"] ,
        )

    def _buildMainPanel(self, parent: ttk.Frame) -> None:
        mainPanelFrame = ttk.Frame(parent, style="Card.TFrame", padding=20)
        mainPanelFrame.grid(row=0, column=0, sticky="nsew", padx=(0, 18))
        mainPanelFrame.rowconfigure(1, weight=1)
        mainPanelFrame.columnconfigure(0, weight=1)
        return mainPanelFrame


