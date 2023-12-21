# Target Defense Game Simulation

This repository contains the Python and MATLAB simulation code for a Target Defense Game with two defenders and a faster intruder, as part of thesis research work.

## Repository Structure

```plaintext
Thesis-research
│   README.md
│   .DS_Store    
│
└───Figure
│   │   OptimalTrajectories.png
│   │   barrier.png
│   │   barrier_sector.png
│   │   opttraj.png
│   │   traj_D_win.png
│   │   traj_D_win_sector.png
│   │   traj_I_win.png
│   │   traj_I_win_sector.png
│   
└───Matlab
│   │   Block Diagram.png
│   │   Block.m
│   │   Block.slx
│   │   Capture_Settings.png
│   │   Defender_1_Subsystem.png
│   │   Intruder_Subsystem.png
│   │   Simulation_result.png
│   │   Theta_1_Calculation.png
│
└───Python
    │   animator.py
    │   Config.py
    │   envelope.py
    │   one_plot.py
    │   opttraj.py
    │   overall_plot.py
    │   RK4.py
    │   Sector_Draw.py
    │   traj_generator.py
    │   vecgram.py
    │
    └───res
        │   someData.csv
        │   switch.csv
```

## Python Simulation

The Python code simulates the target defense game in a two-dimensional space where the defenders' objective is to intercept the intruder before it reaches the target area. Optimal trajectories are computed and visualized.

### Dependencies

- Python 3.x
- Matplotlib
- Numpy
- Scipy

### Running the Simulation

Navigate to the Python directory and run the desired script. For example:

```bash
cd Python
python one_plot.py
```

This will execute the simulation and save trajectory plots in the Figures directory.

## MATLAB Simulation

MATLAB code provides a block diagram-based simulation environment where the dynamics of the defenders and the intruder are modeled and simulated over time.

### MATLAB Version

- MATLAB R2021a or later

### Running the Simulation

Open MATLAB, navigate to the Matlab directory, and run the simulation script:

```matlab
cd Matlab
Block.slx
```

This will execute the simulation, and the results can be visualized in MATLAB's Simulink environment.

## Figures

The Figures directory contains various plots of the optimal trajectories, barriers, and winning scenarios for both the defender and the intruder. These images are generated from the Python scripts and represent key outcomes of the simulation.

## Contributing

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## Documentation

[report](https://www.overleaf.com/project/652b96096ece88dceaee7601)