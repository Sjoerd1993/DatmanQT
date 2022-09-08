from dataclasses import dataclass, field

@dataclass
class Data:
    filename: str = ""
    xdata: list = field(default_factory=list)
    ydata: list = field(default_factory=list)
    xdata_selected: list = field(default_factory=list)
    ydata_selected: list = field(default_factory=list)
    
