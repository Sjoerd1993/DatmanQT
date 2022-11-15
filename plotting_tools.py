from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import datman


def plotGraphOnCanvas(self, layout, title = "", scale="log", marker = None, revert = False):
    canvas = PlotWidget(xlabel="X value", ylabel="Y value",
                        title = "Horizontal Scan")
    figure = canvas.figure
    for key, item in self.datadict.items():
        if item is not None:
            X = item.xdata
            Y = item.ydata
            if item.filename != "":
                plotgGraphFigure(self, X, Y, canvas, filename=key, revert=revert, title=title, scale=scale)
    layout.addWidget(canvas)
    figurecanvas = [figure, canvas]
    self.toolbar = NavigationToolbar(canvas, self)
    layout.addWidget(self.toolbar)
    return figurecanvas




def plotgGraphFigure(self, X, Y, canvas, filename="", xlim=None, title="", scale="log",marker=None, linestyle="solid",
                     revert = False):
    fig = canvas.ax
    if self.selected_measurement == filename:
        linewidth = 3
    else:
        linewidth = 1.5
    fig.plot(X, Y, linewidth = linewidth ,label=filename, linestyle=linestyle, marker=marker)
    canvas.ax.set_title(title)
    set_canvas_limits(self, canvas)
    canvas.ax.set_yscale(scale)
    fig.legend()

def set_canvas_limits(self, canvas):
    xmin, xmax, ymin, ymax = find_limits(self)
    span = (xmax - xmin)
    canvas.ax.set_xlim(xmin - 0.01*span, xmax+0.01*span)
    #canvas.ax.set_ylim(ymin*0.8, ymax*1.2)


def change_scale(self, scale = "yscale"):
    canvas = self.figurecanvas[1]
    if scale == "yscale":
        if self.graph.yscale == "log":
            canvas.ax.set_yscale("linear")
            self.graph.yscale = "linear"
        else:
            canvas.ax.set_yscale("log")
            self.graph.yscale = "log"

    elif scale == "xscale":
        if self.graph.xscale == "log":
            canvas.ax.set_xscale("linear")
            self.graph.xscale = "linear"
        else:
            canvas.ax.set_xscale("log")
            self.graph.xscale = "log"
    set_canvas_limits(self, canvas)
    self.figurecanvas[1].draw()

def find_limits(self):
    xmin_all = None
    xmax_all = None
    ymin_all = None
    ymax_all = None
    for key, item in self.datadict.items():
        if item is not None and len(item.xdata) > 0:
            xmin_item = min(item.xdata)
            xmax_item = max(item.xdata)
            ymin_item = min(item.ydata)
            ymax_item = max(item.ydata)

            if xmin_all == None:
                xmin_all = xmin_item
            if xmax_all == None:
                xmax_all = xmax_item
            if ymin_all == None:
                ymin_all = ymin_item
            if ymax_all == None:
                ymax_all = ymax_item

            if xmin_item < xmin_all:
                xmin_all = xmin_item
            if xmax_item > xmax_all:
                xmax_all = xmax_item
            if ymin_item < ymin_all:
                ymin_all = ymin_item
            if ymax_item > ymax_all:
                ymax_all = ymax_item

    return xmin_all, xmax_all, ymin_all, ymax_all


class PlotWidget(FigureCanvas):
    def __init__(self, parent=None, xlabel="", ylabel="", title="", scale="linear"):
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title(title)
        self.figure.set_tight_layout(True)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        super(PlotWidget, self).__init__(self.figure)

