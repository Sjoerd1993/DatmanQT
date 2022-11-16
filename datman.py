import plotting_tools
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QFileDialog
from pathlib import Path
import os
import numpy as np
from data import Data
import re
from matplotlib.widgets import SpanSelector


def select_data_button(self):
    if not self.selection_button.isChecked():
        delete_selected(self)
        self.plot_figure()
    else:
        try:
            define_highlight(self)
        except TypeError:
            print("Could not define a ROI, perhaps no files are loaded yet")
        self.startx = 0
        self.stopx = 0


def delete_selected(self):
    key_list = []
    for key in self.datadict:
        if key.endswith("_selected"):
            key_list.append(key)
    for key in key_list:
        del (self.datadict[key])


def define_highlight(self, span=None):
    self.span = SpanSelector(
        self.figurecanvas[0].axes[0],
        self.onselect,
        "horizontal",
        useblit=True,
        props=dict(alpha=0.3, facecolor="tab:red"),
        interactive=True,
        drag_from_anywhere=True)
    if span is not None:
        self.span.extents = span
    self.span.set_visible(False)
    self.span.set_active(False)


def load_files(self):
    files = get_path(self)
    open_selection(self, files)
    self.open_item_list.setCurrentRow(0)
    self.selected_measurement = self.open_item_list.currentItem().text()
    self.select_measurement()
    define_highlight(self)


def normalize_data(self):
    delete_selected(self)
    if self.edit_all_button.isChecked():
        for key, item in self.datadict.items():
            item.ydata = normalize(item.ydata)
    else:
        if skip_single_operation(self):
            return None
        key = self.open_item_list.currentItem().text()
        self.datadict[key].ydata = normalize(self.datadict[key].ydata)
    self.startx = 0
    self.stopx = 0
    self.plot_figure()


def shift_vertically(self):
    delete_selected(self)
    shifter = 1
    shift_value = 10000
    for key, item in self.datadict.items():
        item.ydata = [value * shifter for value in item.ydata]
        shifter *= shift_value
    self.startx = 0
    self.stopx = 0
    self.plot_figure()


def center_data(self):
    delete_selected(self)
    if self.edit_all_button.isChecked():
        for key, item in self.datadict.items():
            item.xdata = center_data_calculation(item.xdata, item.ydata)
    else:
        if skip_single_operation(self):
            return None
        key = self.open_item_list.currentItem().text()
        self.datadict[key].xdata = center_data_calculation(self.datadict[key].xdata, self.datadict[key].ydata)
    self.startx = 0
    self.stopx = 0
    self.plot_figure()


def center_data_calculation(xdata, ydata):
    max_value = max(ydata)
    middle_index = ydata.index(max_value)
    middle_value = xdata[middle_index]
    xdata = [coordinate - middle_value for coordinate in xdata]
    return xdata


def normalize(ydata):
    max_y = max(ydata)
    new_y = [value / max_y for value in ydata]
    return new_y


def translate_y(self):
    try:
        translate_value = float(self.translate_y_entry.text())
    except ValueError:
        print("Please enter a valid number")
        translate_value = 0
    if self.edit_all_button.isChecked():
        for key, item in self.datadict.items():
            item.ydata = [value + translate_value for value in item.ydata]
    else:
        if skip_single_operation(self):
            return None
        key = self.open_item_list.currentItem().text()
        self.datadict[key].ydata = [value + translate_value for value in self.datadict[key].ydata]
    self.plot_figure()


def skip_single_operation(self):
    if self.open_item_list.currentItem() is None or self.selected_measurement == "":
        return True
    else:
        return False


def find_xlimits(self):
    first_loop = True
    for key, item in self.datadict.items():
        xdata = item.xdata
        if first_loop == True:
            xmin = min(xdata)
            xmax = max(xdata)
        first_loop = False
        if min(xdata) < xmin:
            xmin = min(xdata)
        if max(xdata) > xmax:
            xmax = max(xdata)
    return xmin, xmax


def translate_x(self):
    try:
        translate_value = float(self.translate_x_entry.text())
    except ValueError:
        print("Please enter a valid number")
        translate_value = 0
    if self.edit_all_button.isChecked():
        for key, item in self.datadict.items():
            item.xdata = [value + translate_value for value in item.xdata]
    else:
        if skip_single_operation(self):
            return None
        key = self.open_item_list.currentItem().text()
        self.datadict[key].xdata = [value + translate_value for value in self.datadict[key].xdata]

    self.startx = 0
    self.stopx = 0
    self.plot_figure()


def multiply_y(self):
    try:
        multiply_value = float(self.multiply_y_entry.text())
    except ValueError:
        print("Please enter a valid number")
        multiply_value = 1
    if self.edit_all_button.isChecked():
        for key, item in self.datadict.items():
            item.ydata = [value * multiply_value for value in item.ydata]
    else:
        if skip_single_operation(self):
            return None
        key = self.open_item_list.currentItem().text()
        self.datadict[key].ydata = [value * multiply_value for value in self.datadict[key].ydata]
    self.startx = 0
    self.stopx = 0
    self.plot_figure()


def multiply_x(self):
    try:
        multiply_value = float(self.multiply_x_entry.text())
    except ValueError:
        print("Please enter a valid number")
        multiply_value = 1
    if self.edit_all_button.isChecked():
        for key, item in self.datadict.items():
            item.xdata = [value * multiply_value for value in item.xdata]
    else:
        if skip_single_operation(self):
            return None
        key = self.open_item_list.currentItem().text()
        self.datadict[key].xdata = [value * multiply_value for value in self.datadict[key].xdata]
    self.startx = 0
    self.stopx = 0
    self.plot_figure()


def smoothen_data(self):
    if self.edit_all_button.isChecked():
        for key, item in self.datadict.items():
            ydata = item.ydata
            item.ydata = smooth(ydata, 3)
    else:
        if skip_single_operation(self):
            return None
        key = self.open_item_list.currentItem().text()
        ydata = self.datadict[key].ydata
        self.datadict[key].ydata = smooth(ydata, 5)
    self.plot_figure()
    self.startx = 0
    self.stopx = 0


def smoothen_data_logscale(self):
    if self.edit_all_button.isChecked():
        for key, item in self.datadict.items():
            print(f"Creating log scale, max value first is {max(item.ydata)}")
            item.ydata = [np.log(value) for value in item.ydata]
            item.ydata = smooth(item.ydata, 5)
            item.ydata = np.exp(item.ydata)
    else:
        if skip_single_operation(self):
            return None
        key = self.open_item_list.currentItem().text()
        ydata = self.datadict[key].ydata
        ydata = [np.log(value) for value in ydata]
        ydata = smooth(ydata, 5)
        ydata = np.exp(ydata)
        self.datadict[key].ydata = ydata
    self.plot_figure()
    self.startx = 0
    self.stopx = 0


def smooth(y, box_points):
    box = np.ones(box_points) / box_points
    y_smooth = np.convolve(y, box, mode="same")
    return y_smooth


def cut_data(self):
    select_data = self.select_data()
    if select_data:
        for key, item in self.datadict.items():
            if item is None:
                continue
            xdata = item.xdata
            ydata = item.ydata
            new_x = []
            new_y = []
            if f"{key}_selected" in self.datadict:
                selected_item = self.datadict[f"{key}_selected"]
                if selected_item == None:
                    continue
                for index, (valuex, valuey) in enumerate(zip(xdata, ydata)):
                    if valuex < min(selected_item.xdata) or valuex > max(selected_item.xdata):
                        new_x.append(valuex)
                        new_y.append(valuey)
                item.xdata = new_x
                item.ydata = new_y
        delete_selected(self)
        self.plot_figure()
        self.startx = 0
        self.stopx = 0
        define_highlight(self)


def open_selection(self, files):
    for file in files:
        if file != "":
            delete_selected(self)
            path = os.path.dirname(file)
            filename = Path(file).name
            self.data.filename = filename
            os.chdir(path)
            data = get_data(file)
            if (len(data.xdata) != len(data.ydata)) or len(data.xdata) == 0:
                break
            else:
                data.filename = filename
                if filename not in self.datadict:
                    self.datadict[filename] = data
                    self.open_item_list.addItem(filename)
            self.plot_figure()


def define_canvas(self):
    layout = self.graphlayout
    self.clear_layout(self.graphlayout)
    self.figurecanvas = plotting_tools.plotGraphOnCanvas(self, layout, scale="log", marker=None)
    self.figurecanvas[1].canvas.mpl_connect('button_press_event', self.on_press)
    self.figurecanvas[1].canvas.mpl_connect('motion_notify_event', self.on_hover)
    self.figurecanvas[1].canvas.mpl_connect('button_release_event', self.on_release)


def get_data(path):
    data = Data()
    seperator = "\t "
    data_array = [[], []]
    with (open(path, 'r')) as file:
        for line in file:
            line = line.strip()
            line = re.split('\s+', line)
            try:
                data_array[0].append(float(line[0]))
                data_array[1].append(float(line[1]))
            except ValueError:
                pass
    data.xdata = data_array[0]
    data.ydata = data_array[1]
    return data


def load_empty(self):
    canvas = plotting_tools.PlotWidget(xlabel="X value", ylabel="Y Value",
                                       title="Plot")
    create_layout(self, canvas, self.graphlayout)


def create_layout(self, canvas, layout):
    toolbar = NavigationToolbar(canvas, self)
    layout.addWidget(canvas)
    layout.addWidget(toolbar)


def get_path(self, documenttype="Text file (*.txt *.xy *.dat);;All Files (*)"):
    dialog = QFileDialog
    options = dialog.Options()
    path = QFileDialog.getOpenFileNames(self, "Open files", "",
                                        documenttype, options=options)[0]
    return path
