# Target Defense Game Simulation

This repository contains the Python and MATLAB simulation code for a Target Defense Game with two defenders and a faster intruder, as part of thesis research work.

## Repository Structure

```plaintext
Thesis-research
│   README.md                            - Main documentation file explaining the repository content.
│   Thesis_Final_Report.pdf              - The final report document for the thesis.
│   Thesis_Presentation.pdf              - Presentation slides for the thesis.

└───Matlab
    │   Animation                        - Contains animation scripts for visualizing the simulation.
    │   Block_Diagram                    - Diagrams showing the block-based structure of the MATLAB simulation.
    │   Illustration                     - Illustrative figures representing simulation concepts.
    │   Monte_Carlo_Data                 - Data from Monte Carlo simulations.
    │   Simulink                         - Simulink models for the MATLAB-based simulation.
    │   Trajectory                       - Plots related to the trajectory.
    │   BaseModel.m                      - MATLAB script for the base model of the simulation.
    │   Model_APF.m                      - MATLAB script implementing the Artifical Potential Field model.
    │   Model_PNG.m                      - MATLAB script for Proportional Navigation Guidance (PNG) model.
    │   Monte_Carlo.m                    - Script for running Monte Carlo simulations.
    │   Prediction_Interception.m        - Script for predicting interception method.

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

The MATLAB simulation utilizes a block diagram approach to model the dynamics of the game, simulating the movements of the defenders and the intruder over time.

### MATLAB Version

- MATLAB R2021a or later

### Running the Simulation

In MATLAB, navigate to the Matlab directory and open the desired model or script:

```matlab
cd Matlab
open('BaseModel.m')
```

This will execute the simulation, and the results can be visualized in MATLAB's Simulink environment.

## Documentation
The 'Thesis_Final_Report.pdf' provides a comprehensive report on the entire project, detailing the research, methodology, and findings.
The 'Thesis_Presentation.pdf' contains the slides used during the thesis defense, offering a succinct overview of the project.
[report](https://www.overleaf.com/project/652b96096ece88dceaee7601)