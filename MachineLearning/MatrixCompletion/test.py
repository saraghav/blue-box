#!/usr/bin/python -i
import numpy as np
from NuclearNormMinimization import NuclearNormMinimization
from sklearn.metrics import mean_squared_error

U = np.random.random((10,10))
S = np.zeros((10,10))
S[0,0] = 500
S[1,1] = 100
S[2,2] = 50
V = np.random.random((10,20))

matrix = np.matmul(U, np.matmul(S, V))
incomplete_matrix = matrix.copy()

blah = np.random.random(incomplete_matrix.shape)
hidden_entries = (blah >= 0.7)
sampled_entries = np.logical_not(hidden_entries)
incomplete_matrix[ hidden_entries ] = np.nan

solver = NuclearNormMinimization()
completed_matrix = solver.complete(incomplete_matrix)

mse = mean_squared_error(matrix, completed_matrix)
print('mean_squared_error = {0:.6f}'.format(mse))
