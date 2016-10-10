#!/usr/bin/python3
import numpy as np
from sklearn.metrics import mean_squared_error

class NuclearNormMinimization(object):

    def __init__(self, method='ProximalGradient', max_iterations=100000):
        '''
        initialize the nuclear norm minimization operator with the preferred algorithm
        '''
        self.solver_function = {
            'ProximalGradient': self.ProximalGradientAlgorithm,
        }

        self.max_iterations = max_iterations

        try:
            self.complete = self.solver_function[method]
        except KeyError:
            print('ERROR: The requested method "{0}" has not been implemented'.format(method))

    def ProximalGradientAlgorithm(self, incomplete_matrix, T=0.5, L=0.1):
        '''
        implements the Proximal Gradient Algorithm for matrix completion
        '''
        completed_matrix = np.random.random(incomplete_matrix.shape)

        for iteration in range(0, self.max_iterations):
            completed_matrix = self.ProximalPointOperator(incomplete_matrix, completed_matrix, T, L)
        return completed_matrix

    @staticmethod
    def ProximalPointOperator(M, X_km1, T, L):
        '''
        implements the proximal point operator for one iteration

        Arguments:
        M - given incomplete matrix
        X_km1 - current iterate (guess) of completed matrix
        T - step size
        L - constant for tuning the soft-thresholding operator

        Description:
        the implementation is based on using the soft-thresholding operator for 1-norm regularization of the singular values
        '''
        
        known_value_locations = np.logical_not(np.isnan(M))
        X_k_interim = X_km1.copy()
        X_k_interim[ known_value_locations ] -= T * (X_km1-M)[known_value_locations]

        U, S_interim, V = np.linalg.svd(X_k_interim, full_matrices=False)
        
        threshold = T*L
        S = [ NuclearNormMinimization.SoftThreshold(singular_value, threshold) for singular_value in S_interim ]

        X_k = np.dot(U, np.dot(np.diag(S), V))
        return X_k

    @staticmethod
    def SoftThreshold(value, threshold):
        '''
        implements the soft-thresholding operator
        '''
        if value > threshold:
            return value-threshold*np.sign(value)
        else:
            return 0
