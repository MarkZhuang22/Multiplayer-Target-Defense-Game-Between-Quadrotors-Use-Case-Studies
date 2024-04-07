% Monte Carlo Simulation 
% Define the number of simulations to run for each heading angle
numSimulations = 100;

% Define the fixed initial conditions for the intruder and Defender 2
I = [5*pi/4, 1.5, 5, 5]; % [heading angle, velocity, y position, x position]
D2 = [-pi/2, 1.0, 0, 0]; % [heading angle, velocity, y position, x position]

% Define regions and corresponding heading angle ranges
regions = {
    {1, [0, 5], [0, 5], [0, pi]},
    {2, [0, 5], [5, 10], [-pi/2, pi/2]},
    {3, [5, 10], [0, 5], [pi, 2*pi]},
    {4, [5, 10], [5, 10], []}
};

% Define typical angles for testing
typical_angles = {
    {1, [0, pi/6, pi/4, pi/3, pi/2, 2*pi/3, 3*pi/4, 5*pi/6, pi]},
    {2, [-pi/2, -pi/3, -pi/4, -pi/6, 0, pi/6, pi/4, pi/3, pi/2]},
    {3, [pi, 7*pi/6, 5*pi/4, 4*pi/3, 3*pi/2, 5*pi/3, 7*pi/4, 11*pi/6, 2*pi]}
};

modelName = 'Block1';

% Iterate over each region
for region_idx = 1:length(regions)
    region = regions{region_idx};
    region_num = region{1};
    y_range = region{2};
    x_range = region{3};
    angle_range = region{4};

    % Skip Region 4 as no heading angles are considered
    if isempty(angle_range)
        continue;
    end

    % Find the index in typical_angles that matches the current region number
    ta_index = find(cellfun(@(x) x{1} == region_num, typical_angles));

    % Proceed if typical angles for the current region are defined
    if ~isempty(ta_index)
        % Iterate over each typical angle for the region
        for angle_idx = 1:length(typical_angles{ta_index}{2})
            heading_angle = typical_angles{ta_index}{2}(angle_idx);
            successful_conditions = []; % Initialize for successful conditions

            % Monte Carlo simulation for each heading angle
            for sim_num = 1:numSimulations
                % Select a random position within the region
                D1_y = y_range(1) + (y_range(2) - y_range(1)) * rand();
                D1_x = x_range(1) + (x_range(2) - x_range(1)) * rand();

                % Define D1 with the selected heading angle and position
                D1 = [heading_angle, 1.0, D1_y, D1_x]; % Velocity of D1 is assumed to be 1.0

                % Run the simulation with the new initial conditions
                set_param(modelName, 'StopTime', '30'); % Set simulation stop time
                simOut = sim(modelName, 'SrcWorkspace', 'current');

                % Access the 'Stop' signal from the simOut structure
                stopSignal = simOut.Stop;  % This extracts the timeseries object

                % Now, check if the simulation stop condition was met
                % The Data property of the timeseries object holds the actual signal data
                if ~isempty(stopSignal) && stopSignal.Data(end) == 1
                    successful_conditions = [successful_conditions; D1];
                end
            end

            % Save the successful initial conditions
            filename = sprintf('successful_conditions_region%d_angle%.2frad.mat', region_num, heading_angle);
            save(filename, 'successful_conditions');
        end
    end
end