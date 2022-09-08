from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar



def plotGraphOnCanvas(self, layout, title = "", scale="log", marker = None, revert = False):
    canvas = PlotWidget(xlabel="X value", ylabel="Y value",
                        title = "Horizontal Scan")
    figure = canvas.figure
    for key, item in self.datadict.items():
        X = item.xdata
        Y = item.ydata
        plotgGraphFigure(X, Y, canvas, filename=key, revert=revert, title=title, scale=scale)
    layout.addWidget(canvas)
    figurecanvas = [figure, canvas]
    self.toolbar = NavigationToolbar(canvas, self)
    layout.addWidget(self.toolbar)
    return figurecanvas

def plotgGraphFigure(X, Y, canvas, filename="", xlim=None, title="", scale="log",marker=None, linestyle="solid",
                     revert = False):
    fig = canvas.ax
    fig.plot(X, Y, label=filename, linestyle=linestyle, marker=marker)
    if revert:
        fig.invert_xaxis()
    canvas.ax.set_title(title)
    canvas.ax.set_xlim(xlim)
    canvas.ax.set_yscale(scale)
    fig.legend()

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
    xmin, xmax, ymin, ymax = find_limits(self)
    canvas.ax.set_xlim(xmin, xmax)
    canvas.ax.set_ylim(ymin, ymax)
    self.figurecanvas[1].draw()

def find_limits(self):
    xmin_all = None
    xmax_all = None
    ymin_all = None
    ymax_all = None
    for key, item in self.datadict.items():
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
