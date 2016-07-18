#!/usr/bin/python3
import numpy as np
import math
import plotting

class DiscreteWaveletTransform(object):
    
    def __init__(self, **kwds):
        super().__init__(**kwds)
        self.zero_padding = True
        self.plotter = plotting.Plotter()

    def transform(self, scale):
        pass

    def inverse(self):
        pass

    def ceil_power_of_two(self, num):
        if num > 0:
            return 1<<(num-1).bit_length()
        elif num == 0:
            return 0
        else:
            raise NotImplementedError

    def add_signal(self, signal):
        self.signal = np.array(signal)

        if self.zero_padding is True:
            current_length = len(self.signal)
            desired_length = self.ceil_power_of_two(current_length)
            self.signal = np.append(self.signal, np.zeros(desired_length-current_length))
        else:
            raise NotImplementedError

    def add_wavelet_coeffs(self, wavelet_coeffs, scale):
        self.wavelet_coeffs = wavelet_coeffs
        self.scale = scale

    def plot_coeffs(self):
        self.plotter.plot_hold(np.arange(len(self.wavelet_coeffs)), self.wavelet_coeffs, legend=['wavelet coefficients'])
        self.plotter.plot_show()

    def plot_coeffs_separated(self):
        self.plotter.plot_hold(np.arange(len(self.wavelet_coeffs_separated)), self.wavelet_coeffs_separated, legend=['wavelet coeffs separated'])
        self.plotter.plot_show()

    def plot_signal_comparison(self):
        self.plotter.plot_hold(np.arange(len(self.signal)), self.signal, legend=['signal'])
        self.plotter.plot_hold(np.arange(len(self.signal_recovered)), self.signal_recovered, legend=['signal recovered'])
        self.plotter.plot_show()

        self.plotter.plot_hold(np.arange(len(self.signal)), self.signal_recovered-self.signal, legend=['recovered - original'])
        self.plotter.plot_show()

    def plot_signal_comparison_multires(self):
        self.plotter.plot_hold(np.arange(len(self.signal)), self.signal, legend=['signal'])
        self.plotter.plot_hold(np.arange(len(self.signal_multires)), self.signal_multires)
        self.plotter.plot_show()
