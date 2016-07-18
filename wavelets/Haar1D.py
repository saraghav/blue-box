#!/usr/bin/python3
from DiscreteWaveletTransform import DiscreteWaveletTransform
import numpy as np
import plotting
import ilogger

logger = ilogger.setup_logger(__name__)

class Haar1D(DiscreteWaveletTransform):
    
    def __init__(self, **kwds):
        super().__init__(**kwds)
        self.transform_type = 'Haar1D'
        self.normalize = True

    def transform(self, scale):
        self.scale = int(scale)
        self.wavelet_coeffs = np.copy(self.signal)
        
        if self.zero_padding is True:
            if self.scale > int(np.round(np.log2(len(self.signal)))):
                raise Exception('bad scale setting')
            for scale_i in range(0,self.scale):
                window = [ True if temp_i%(2**scale_i)==0 else False for temp_i in range(0,len(self.signal)) ]
                window = np.array(window)
                self.wavelet_coeffs[window] = self.lift(self.wavelet_coeffs[window])
        else:
            raise NotImplementedError

        self.separate_wavelet_coeffs()

    def inverse_transform(self, wavelet_coeffs=None, update_self=False):
        if wavelet_coeffs is None:
            wavelet_coeffs = self.wavelet_coeffs
            update_self = True
        signal_recovered = np.copy(wavelet_coeffs)
        
        if self.zero_padding is True:
            for scale_i in range(self.scale-1,-1,-1):
                window = [ True if temp_i%(2**scale_i)==0 else False for temp_i in range(0,len(self.signal)) ]
                window = np.array(window)
                signal_recovered[window] = self.drop(signal_recovered[window])
        else:
            raise NotImplementedError

        if update_self is True:
            self.signal_recovered = signal_recovered

        return signal_recovered

    def lift(self, signal):
        for i in range(0, len(signal), 2):
            # predict and update operations for a single lifting step
            #   of the Haar 1D transform
            signal[i+1] = signal[i+1] - self._predict(signal[i])
            signal[i]   = signal[i] + self._update(signal[i+1])

            # normalization step for the Haar 1D transform
            if self.normalize is True:
                signal[i]   *= np.sqrt(2)
                signal[i+1] /= np.sqrt(2)
        return signal

    def drop(self, signal):
        for i in range(0, len(signal), 2):
            # invert the normalization step for the Haar 1D transform
            if self.normalize is True:
                signal[i]   /= np.sqrt(2)
                signal[i+1] *= np.sqrt(2)

            # invert the predict and update operations for a single lifting step
            #   of the Haar 1D transform
            signal[i]   = signal[i] - self._update(signal[i+1])
            signal[i+1] = signal[i+1] + self._predict(signal[i])
        return signal

    def calculate_multiresolution_representation(self):
        signal_multires = np.empty((0,0))
        signal_length = len(self.signal)
        
        if self.zero_padding is True:
            for scale_i in range(0, self.scale):
                coeff_indices = np.arange(2**scale_i, signal_length, 2**(scale_i+1))
                wavelet_coeffs_single = np.zeros_like(self.wavelet_coeffs)
                wavelet_coeffs_single[coeff_indices] = self.wavelet_coeffs[coeff_indices]
                signal_at_res = self.inverse_transform(wavelet_coeffs_single)
                signal_at_res.shape = len(signal_at_res),1

                try:
                    signal_multires = np.concatenate([signal_multires, signal_at_res], axis=1)
                except ValueError:
                    signal_multires = signal_at_res

            coeff_indices = np.arange(0, signal_length, 2**(scale_i+1))
            wavelet_coeffs_single = np.zeros_like(self.wavelet_coeffs)
            wavelet_coeffs_single[coeff_indices] = self.wavelet_coeffs[coeff_indices]
            signal_at_res = self.inverse_transform(wavelet_coeffs_single)
            signal_at_res.shape = len(signal_at_res), 1
            signal_multires = np.concatenate([signal_multires, signal_at_res], axis=1)
        else:
            raise NotImplementedError

        self.signal_multires = signal_multires

    def separate_wavelet_coeffs(self):
        signal_length = len(self.signal)
        coeff_label_subscript = int(np.round(np.log2(signal_length)))
        coeff_separated = np.empty((0,))
        for scale_i in range(0, self.scale):
            coeff_label_subscript -= 1
            coeff_label = 'd' + str(coeff_label_subscript)
            coeff_indices = np.arange(2**scale_i, signal_length, 2**(scale_i+1))
            coeff = self.wavelet_coeffs[coeff_indices]
            setattr(self, coeff_label, coeff)
            coeff_separated = np.concatenate([coeff, coeff_separated])

        coeff_label = 's' + str(coeff_label_subscript)
        coeff_indices = np.arange(0, signal_length, 2**(scale_i+1))
        coeff = self.wavelet_coeffs[coeff_indices]
        setattr(self, coeff_label, coeff)
        coeff_separated = np.concatenate([coeff, coeff_separated])

        self.wavelet_coeffs_separated = coeff_separated

    def _predict(self, s):
        return s

    def _update(self, d):
        return 0.5*d

