import numpy as np
from math import sin, cos, pi
#import tensorflow as tf
####################################################################################
##################################### CONFIG #######################################
class Config(object):
    ###============ player params =========
    # Player parameters
    CAP_RANGE = 2.0      # Capture radius of the defender
    VD = 1.0             # Defender's velocity
    VI = 1.5             # Intruder's (invader's) velocity
    TAG_RANGE = 5.0      # Radius of the target area
    SECTOR_ANGLE = pi/3  # Sector angle (60 degrees)
    
    # Simulation parameters
    TIME_STEP = 0.1      # Time step for the simulation
    
    ##========= target =========

    # Initial positions of the players relative to the target
    x0 = [
        np.array([0., 2.*CAP_RANGE+TAG_RANGE]), 
        (1.99*CAP_RANGE+TAG_RANGE)*np.array([sin(pi/4), cos(pi/4)])
    ]

    # Parameters for learning (assuming some form of reinforcement learning or optimization)
    LEARNING_RATE = 0.01            # Learning rate for the optimizer
    LAYER_SIZES = [30, 6, 30]       # Sizes of neural network layers, if applicable
    # ACT_FUNCS = [activation functions]  # Activation functions for the NN layers (commented out)
    TAU = 0.01                      # Used for updating target networks, if applicable
    MAX_BUFFER_SIZE = 10000         # Maximum size of the replay buffer
    BATCH_SIZE = 1000               # Batch size for training
    TRAIN_STEPS = 100               # Number of training steps per episode
    TARGET_UPDATE_INTERVAL = 1      # Interval for updating target network

    # Saving and logging parameters
    DATA_FILE = 'valueData.csv'     # Path to save data
    MODEL_DIR = 'models/'           # Directory to save models
    MODEL_FILE = 'valueFn'          # Base name for saved model files

    SAVE_FREQUENCY = 100            # Frequency of saving model checkpoints
    PRINTING_FREQUENCY = 50         # Frequency of printing out information during training
