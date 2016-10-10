#!/usr/bin/python3
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

class Random2DRobot(object):
    '''
    A random 2-dimensional robot for demonstrating particle filters
    '''
    
    def __init__(self, world_x_size, world_y_size, n_particles):
        '''
        define the simulation settings and setup the visualization
        '''
        # simulation settings
        self.world_x_size = world_x_size
        self.world_y_size = world_y_size
        self.n_particles = n_particles

        # initial robot state
        self.x_loc = world_x_size * np.random.random((1,))
        self.y_loc = world_y_size * np.random.random((1,))
        self.generate_measurement()

        # intial particles state
        self.particles_x_loc = world_x_size * np.random.random((self.n_particles,))
        self.particles_y_loc = world_y_size * np.random.random((self.n_particles,))
        self.pfilter_estimate().send(None)

        # setup graphics
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim([0, world_x_size])
        self.ax.set_ylim([0, world_y_size])
        
        self.robot_loc_plot, = self.ax.plot(self.x_loc, self.y_loc, 'o', markersize=30)
        self.particles_plot, = self.ax.plot(self.particles_x_loc, self.particles_y_loc, '*')
        self.particles_estimate_plot, = self.ax.plot(self.x_loc_estimate, self.y_loc_estimate, 'x', markersize=30)

        self.robot_animator = animation.FuncAnimation(self.fig, self.animate_robot, self.move_robot, interval=1000, blit=False)
        self.pfilter_animator = animation.FuncAnimation(self.fig, self.animate_pfilter, self.pfilter_update, interval=100, blit=False)
        self.pfilter_estimate_animator = animation.FuncAnimation(self.fig, self.animate_pfilter_estimate, self.pfilter_estimate, interval=100, blit=False)
        plt.show()
        
    def animate_robot(self, _):
        '''
        FuncAnimation function to update the robot location in the plot
        '''
        self.robot_loc_plot.set_data(self.x_loc, self.y_loc)
        return self.robot_loc_plot,

    def animate_pfilter(self, _):
        '''
        FuncAnimation function to update the particle locations in the plot
        '''
        self.particles_plot.set_data(self.particles_x_loc, self.particles_y_loc)
        return self.particles_plot,

    def animate_pfilter_estimate(self, _):
        '''
        FuncAnimation function to update the particle filter estimate in the plot
        '''
        self.particles_estimate_plot.set_data(self.x_loc_estimate, self.y_loc_estimate)
        return self.particles_estimate_plot,

    def move_robot(self):
        '''
        Actual robot movement model - this function is a proxy for real life
        '''
        self.x_loc += (2*np.random.random()-1) * self.world_x_size * 0.2
        self.y_loc += (2*np.random.random()-1) * self.world_y_size * 0.2
        self.snap_location()
        yield

    def generate_measurement(self):
        '''
        Actual robot measurement model - this function is a proxy for real life
        '''
        # actual location plus uniform random noise
        self.x_loc_measurement = self.x_loc + (2*np.random.random()-1) * self.world_x_size * 0.05
        self.y_loc_measurement = self.y_loc + (2*np.random.random()-1) * self.world_y_size * 0.05

    def pfilter_update(self, prune_motion_update=True):
        '''
        Execute one particle filter prediction step
        '''
        self.generate_measurement()

        # motion update
        particles_x_loc, particles_y_loc = map(np.array, zip(*map(self.motion_update, self.particles_x_loc, self.particles_y_loc)))
        if prune_motion_update:
            # remove motion update predictions that are outside the world
            valid_x_indices = np.logical_and(particles_x_loc>=0, particles_x_loc<=self.world_x_size)
            valid_y_indices = np.logical_and(particles_y_loc>=0, particles_y_loc<=self.world_y_size)
            valid_indices = np.logical_and(valid_x_indices, valid_y_indices)
            particles_x_loc = particles_x_loc[valid_indices]
            particles_y_loc = particles_y_loc[valid_indices]

        # get weights based on observation model
        get_weight = lambda x,y : self.sensor_update(x, y, self.x_loc_measurement, self.y_loc_measurement)
        weights = np.array(list(map(get_weight, particles_x_loc, particles_y_loc)))
        weights_normalized = weights / weights.sum()
        weights_normalized = weights_normalized.ravel()

        # resample the particles
        resampled_indices = np.random.choice(range(particles_x_loc.size), self.n_particles, p=weights_normalized)
        self.particles_x_loc = np.array([ particles_x_loc[i] for i in resampled_indices ])
        self.particles_y_loc = np.array([ particles_y_loc[i] for i in resampled_indices ])
        yield

    def pfilter_estimate(self):
        '''
        Calculate the posterior estimate of the robot location from the particles
        '''
        # estimate of position
        self.x_loc_estimate = self.particles_x_loc.mean()
        self.y_loc_estimate = self.particles_y_loc.mean()
        yield

    def motion_update(self, x, y):
        '''
        Robot motion model - how we think the robot would move
        '''
        x_next = x + (2*np.random.random()-1)*10
        y_next = y + (2*np.random.random()-1)*10
        return (x_next, y_next)

    def sensor_update(self, x, y, x_meas, y_meas):
        '''
        Robot sensor model - calculate the probability of the measurement, given a location hypothesis
        '''
        x_stddev = 0.5
        y_stddev = 0.5
        x_prob = stats.norm.pdf(x_meas, x, x_stddev)
        y_prob = stats.norm.pdf(y_meas, y, y_stddev)
        return x_prob*y_prob

    def snap_location(self):
        '''
        Helper function to ensure that the actual robot motion model does not push the robot outside of the world boundaries
        '''
        self.x_loc = np.minimum(np.maximum(0, self.x_loc), self.world_x_size)
        self.y_loc = np.minimum(np.maximum(0, self.y_loc), self.world_y_size)

