# Target Defense Game Simulation

This repository contains the Python and MATLAB simulation code for a Target Defense Game with two defenders and a faster intruder, as part of thesis research work.

## Repository Structure

```plaintext
Thesis-research
│   README.md                            - Main documentation file explaining the repository content.
│   .DS_Store                            - macOS folder settings file, usually hidden in the directory.

└───Figure
│   │   OptimalTrajectories.png          - Shows the all optimal trajectories computed for the game scenario.
│   │   barrier.png                      - Depicts the scenario when game start from the barrier.
│   │   barrier_sector.png               - The barrier scenario with sector-shaped capture range.
│   │   opttraj.png                      - A depiction of the optimal trajectories with two defender and one intruder.
│   │   traj_D_win.png                   - Illustrates a scenario where the defender win.
│   │   traj_D_win_sector.png            - Defense win scenario with sector-shaped capture range.
│   │   traj_I_win.png                   - Depicts a scenario where the intruder win.
│   │   traj_I_win_sector.png            - Intruder win scenario with sector-shaped capture range.

└───Matlab
│   │   Block Diagram.png                - Visual layout of the simulation's block diagram.
│   │   Block.m                          - MATLAB script for simulation.
│   │   Block.slx                        - MATLAB Simulink file for running the simulation.
│   │   Capture_Settings.png             - Settings for the capture mechanism in the simulation.
│   │   Defender_1_Subsystem.png         - Detailed subsystem diagram for defender 1.
│   │   Intruder_Subsystem.png           - Detailed subsystem diagram for the intruder.
│   │   Simulation_result.png            - The result output of the simulation.
│   │   Theta_1_Calculation.png          - Calculation process for the angle theta in the simulation.

└───Python
    │   animator.py                      - Generates animations.
    │   Config.py                        - Contains configuration settings for the simulation.
    │   envelope.py                      - Define functions for generating trajectory plot.
    │   one_plot.py                      - Generates a single plot of trajectory.
    │   opttraj.py                       - Visualizes optimal trajectories with two defender and one intruder.
    │   overall_plot.py                  - Produces a plot contains all optimal trajectories.
    │   RK4.py                           - Implements the fourth-order Runge-Kutta method for numerical integration.
    │   Sector_Draw.py                   - Adding sectors indicating defender range.
    │   traj_generator.py                - Creates trajectories based on different initial position.
    │   vecgram.py                       - Define functions for generating vectograms.
    │   someData.csv                     - Data output from simulation runs for analysis 
    │   switch.csv                       - Data defining switching strategies in the simulation
    │   res                              - Data output from envelope_barrier from enevlope.py

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

## Documentation

[report](https://www.overleaf.com/project/652b96096ece88dceaee7601)