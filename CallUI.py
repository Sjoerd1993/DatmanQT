# CallUI.py
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
import plotting_tools
from data import Data
import datman
from graph import Graph
import numpy as np

Ui_MainWindow, QtBaseClass = uic.loadUiType("form.ui")


class CallUI(QtBaseClass, Ui_MainWindow):
    def __init__(self):
        QtBaseClass.__init__(self)
        Ui_MainWindow.__init__(self)
        self.stopx = None
        self.hover = False
        self.figurecanvas = None
        self.datadict = {}
        self.setupUi(self)
        self.highlight = None
        self.clicked = False
        self.data = Data()
        self.graph = Graph()
        self.connect_actions()
        datman.load_empty(self)

    def connect_actions(self):
        # Connect File actions
        self.load_button.clicked.connect(lambda: datman.load_files(self))
        self.cut_data_button.clicked.connect(lambda: datman.cut_data(self))
        self.remove_button.clicked.connect(self.remove_sample)
        self.save_button.clicked.connect(self.save_data)
        self.normalize_button.clicked.connect(lambda: datman.normalize_data(self))
        self.shift_vertically_button.clicked.connect(lambda: datman.shift_vertically(self))
        self.center_button.clicked.connect(lambda: datman.center_data(self))
        self.selection_button.clicked.connect(lambda: datman.select_data_button(self))
        self.multiply_x_button.clicked.connect(lambda: datman.multiply_x(self))
        self.multiply_y_button.clicked.connect(lambda: datman.multiply_y(self))
        self.translate_x_button.clicked.connect(lambda: datman.translate_x(self))
        self.translate_y_button.clicked.connect(lambda: datman.translate_y(self))
        self.smooth_button.clicked.connect(lambda: datman.smoothen_data(self))
        self.smooth_log_button.clicked.connect(lambda: datman.smoothen_data_logscale(self))
        self.translate_x_button.clicked.connect(lambda: datman.translate_x(self))
        self.yscale_button.clicked.connect(lambda: plotting_tools.change_scale(self))
        self.xscale_button.clicked.connect(lambda: plotting_tools.change_scale(self, scale="xscale"))


    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def on_press(self, event):
        self.clicked = True
        self.hover = False
        self.startx = event.xdata
        self.stopx = event.xdata
        if self.clicked == True and self.selection_button.isChecked():
            plotting_tools.insert_vline(self)


    def on_hover(self, event):
        self.hover = False
        if self.clicked == True and self.selection_button.isChecked():
            plotting_tools.insert_vline(self)
            self.figurecanvas[1].draw()
            self.stopx = event.xdata
            self.hover = True

    def on_release(self, event):
        self.clicked = False
        if self.selection_button.isChecked() and self.hover:
            self.select_data()
            plotting_tools.insert_vline(self)
        self.hover = False
        self.figurecanvas[1].draw()

    def remove_sample(self):
        datman.delete_selected(self)
        if self.open_item_list.currentItem() is not None:
            key_to_remove = self.open_item_list.currentItem().text()
            del (self.datadict[key_to_remove])
            self.open_item_list.takeItem(self.open_item_list.currentRow())
            self.plot_figure()

    def sort_data(self, x, y):
        bar_list = {"x": x, "y": y}
        sorted = self.sort_bar(bar_list)
        return sorted["x"], sorted["y"]

    def sort_bar(self, bar_list):
        sorted_x = []
        sorted_x.extend(bar_list['x'])
        sorted_x.sort()
        sorted_y = []
        for x in sorted_x:
            sorted_y.append(bar_list['y'][bar_list['x'].index(x)])
        return {"x": sorted_x, "y": sorted_y}

    def save_data(self):
        datman.delete_selected(self)
        if len(self.datadict) == 1:
            for key, item in self.datadict.items():
                xdata = item.xdata
                ydata = item.ydata
            path = self.saveFileDialog()
            filename = path[0]
            if filename[-4:] != ".txt":
                filename = filename + ".txt"
            array = np.stack([xdata, ydata], axis=1)
            np.savetxt(filename, array, delimiter="\t")
        elif len(self.datadict) > 1:
            path = QFileDialog.getExistingDirectory(self, "Choose Directory")
            for key, item in self.datadict.items():
                xdata = item.xdata
                ydata = item.ydata
                filename = item.filename
                filename = filename.split(".")[0]
                if "/" in path:
                    filename = f"{path}/{filename}_edited.txt"
                else:
                    filename = f"{path}\{filename}_edited.txt"
                array = np.stack([xdata, ydata], axis=1)
                np.savetxt(filename, array, delimiter="\t")

    def saveFileDialog(self, documenttype="Text file (*.txt)"):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getSaveFileName(self, "Save your file", self.data.filename[:-4],
                                               documenttype, options=options)
        return fileName

    def plot_figure(self, layout=None, title=None):
        if title == None:
            title = self.get_title()
        if layout == None:
            layout = self.graphlayout
        self.clear_layout(layout)
        self.figurecanvas = plotting_tools.plotGraphOnCanvas(self, layout,
                                                             title=title, scale="log", marker=None)
        self.figurecanvas[1].canvas.mpl_connect('button_press_event', self.on_press)
        self.figurecanvas[1].canvas.mpl_connect('motion_notify_event', self.on_hover)
        self.figurecanvas[1].canvas.mpl_connect('button_release_event', self.on_release)
        datman.remove_highlight(self)


    def select_data(self):
        datman.delete_selected(self)
        selected_dict = {}
        startx = min(self.startx, self.stopx)
        stopx = max(self.startx, self.stopx)
        if self.edit_all_button.isChecked():
            for key, item in self.datadict.items():
                if item is not None and len(item.xdata) > 0:
                    if not ((startx < min(item.xdata) and stopx < min(item.xdata)) or (startx > max(item.xdata))):
                        selected_data = self.pick_data_selection(item, startx, stopx)
                        selected_dict[f"{key}_selected"] = selected_data
        else:
            key = self.open_item_list.currentItem().text()
            item = self.datadict[key]
            if not ((startx < min(item.xdata) and stopx < min(item.xdata)) or (startx > max(item.xdata))):
                selected_data = self.pick_data_selection(item, startx, stopx)
                selected_dict[f"{key}_selected"] = selected_data

        if (startx < min(item.xdata) and stopx < min(item.xdata)) or (startx > max(item.xdata)):
            datman.delete_selected(self)
            self.clear_layout(self.graphlayout)
            title = None
            self.plot_figure(title=title)

        if len(selected_dict) > 0:
            self.datadict.update(selected_dict)
            self.clear_layout(self.graphlayout)
            title = None
            if len(selected_dict) == 1:
                for key in self.datadict.keys():
                    title = self.datadict[key].filename
                    break
            self.plot_figure(title=title)

    def pick_data_selection(self, item, startx, stopx):
        xdata = item.xdata
        ydata = item.ydata
        xdata, ydata = self.sort_data(xdata, ydata)
        start_index = 0
        stop_index = len(xdata)
        found_start = False
        found_stop = False

        for index, value in enumerate(xdata):
            if value > startx and not found_start:
                start_index = index
                found_start = True
            if value > stopx and not found_stop:
                stop_index = index
                found_stop = True
        selected_data = Data()
        selected_data.xdata = xdata[start_index:stop_index]
        selected_data.ydata = ydata[start_index:stop_index]
        if len(selected_data.xdata) > 0 and (found_start or found_stop) == True:
            return selected_data

    def get_title(self):
        if len(self.datadict) > 1:
            return "Multiple datafiles"
        if len(self.datadict) == 1:
            for key in self.datadict.keys():
                return self.datadict[key].filename


def setUpWindow():
    app = QtWidgets.QApplication(sys.argv)
    nowWindow = CallUI()
    nowWindow.showMaximized()
    sys.exit(app.exec_())
