#!/usr/bin/python3 -i
from Haar1D import Haar1D
import numpy as np

# signal = [56, 40, 8, 24, 48, 48, 40, 16]
signal = np.sin( 4*np.pi*np.arange(0,512)/512 )
noise = np.random.uniform(-0.1, 0.1, signal.shape)
noisy_signal = signal + noise

tf = Haar1D()
tf.add_signal(signal)
tf.transform(3)
tf.inverse_transform()
tf.calculate_multiresolution_representation()

tf.plot_coeffs_separated()
# tf.plot_signal_comparison()
# tf.plot_signal_comparison_multires()
