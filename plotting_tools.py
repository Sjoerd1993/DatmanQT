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
    fig = canvas.theplot
    fig.plot(X, Y, label=filename, linestyle=linestyle, marker=marker)
    if revert:
        fig.invert_xaxis()
    canvas.theplot.set_title(title)
    canvas.theplot.set_xlim(xlim)
    canvas.theplot.set_yscale(scale)
    fig.legend()

def change_scale(self, scale = "yscale"):
    canvas = self.figurecanvas[1]
    if scale == "yscale":
        if self.graph.yscale == "log":
            canvas.theplot.set_yscale("linear")
            self.graph.yscale = "linear"
        else:
            canvas.theplot.set_yscale("log")
            self.graph.yscale = "log"

    elif scale == "xscale":
        if self.graph.xscale == "log":
            canvas.theplot.set_xscale("linear")
            self.graph.xscale = "linear"
        else:
            canvas.theplot.set_xscale("log")
            self.graph.xscale = "log"
    xmin, xmax, ymin, ymax = find_limits(self)
    canvas.theplot.set_xlim(xmin, xmax)
    canvas.theplot.set_ylim(ymin, ymax)
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
    def __init__(self, parent=None, xlabel=None, ylabel='Intensity (arb. u)', title="", scale="linear"):
        super(PlotWidget, self).__init__(Figure())
        self.setParent(parent)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.theplot = self.figure.add_subplot(111)
        self.theplot.set_title(title)
        self.theplot.set_xlabel(xlabel)
        self.theplot.set_ylabel(ylabel)
        self.figure.set_tight_layout(True)
        self.theplot.set_yscale("log")