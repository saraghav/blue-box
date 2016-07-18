#!/usr/bin/python3
import ilogger
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
from matplotlib.backends.backend_pdf import PdfPages
from data_browser import PointBrowser

logger = ilogger.setup_logger(__name__)

class Plotter(object):

    fig_num = 0

    def plot(self, xdata, ydata, showcursor=True, formatspec='', legend=None):
        logger.debug('entered plot(xdata, ydata)')
        fig = plt.figure(num=self.fig_num)
        ax = fig.add_subplot(1,1,1)
    
        lines = ax.plot(xdata, ydata, formatspec, linewidth='2')
        if legend is not None:
            for line_index, line in enumerate(lines):
                line.set_label(legend[line_index])
            ax.legend(legend)
    
        if showcursor is True:
            # useblit=True set for faster performance
            self.cursor = Cursor(ax, useblit=True, color='red', linewidth=2)
    
        plt.show()
        self.fig_num += 1
    
    fig = None
    ax = None
    
    def plot_hold(self, xdata, ydata, showcursor=True, formatspec='', legend=None):
        
        logger.debug('entered plot_hold(xdata, ydata)')
        if self.fig is None and self.ax is None:
            self.fig = plt.figure(num=self.fig_num)
            self.ax = self.fig.add_subplot(1,1,1)
    
        lines = self.ax.plot(xdata, ydata, formatspec, linewidth='2')
        if legend is not None:
            for line_index, line in enumerate(lines):
                line.set_label(legend[line_index])
            self.ax.legend()

        if showcursor is True:
            # useblit=True set for faster performance
            self.cursor = Cursor(self.ax, useblit=True, color='red', linewidth=2)

    def hist_hold(self, data, showcursor=True, formatspec='', legend=None, bins=20, normed=False, yscale='lin'):
        
        logger.debug('entered hist_hold(xdata, ydata)')
        if self.fig is None and self.ax is None:
            self.fig = plt.figure(num=self.fig_num)
            self.ax = self.fig.add_subplot(1,1,1)
   
        if legend is not None and len(legend) == 1:
            legend = legend[0]
        n, bins, patches = self.ax.hist(data, bins=bins, normed=normed, linewidth='2', label=legend)

        if yscale == 'log':
            self.ax.set_yscale("log", nonposy='clip')

        if showcursor is True:
            # useblit=True set for faster performance
            self.cursor = Cursor(self.ax, useblit=True, color='red', linewidth=2)
    
    def plot_show(self, point_browser=False):
        self.ax.grid(which='both', axis='both')
        
        if point_browser is True:
            self.browser = PointBrowser()
            self.fig.canvas.mpl_connect('button_release_event', self.browser.on_button_release)
        
        plt.show()
        self.clear()

    def plot_save(self, filename, filetype='pdf'):
        self.ax.grid(which='both', axis='both')
        if filetype == 'pdf':
            pdf_file = PdfPages(filename + '.pdf')
            pdf_file.savefig(self.fig)
            pdf_file.close()
            self.clear()

    def clear(self):
        self.fig_num += 1
        del self.cursor
        del self.ax
        del self.fig
        self.fig = None
        self.ax = None
        self.cursor = None
