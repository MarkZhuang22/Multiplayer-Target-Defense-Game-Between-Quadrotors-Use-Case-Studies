%% PNG Law
% Initial condition: heading angles, velocity(v), y position, x position
D1 = [0, 1,28, 20];
D2 = [pi, 1,27, 35];
I = [5*pi/4,1.5, 30, 30];

% Define target area
targetX = 0;
targetY = 0;
targetRadius = 2;

% Run Simulink model
simOut = sim("ModelPNG");
% Extract the data using dot notation
D1x = simOut.D1x.Data(:)';
D1y = simOut.D1y.Data(:)';
D2x = simOut.D2x.Data(:)';
D2y = simOut.D2y.Data(:)';
Ix = simOut.Ix.Data(:)';
Iy = simOut.Iy.Data(:)';
t = simOut.tout;
n1_D1_values = simOut.n1_D1.signals.values;
n1_D2_values = simOut.n1_D2.signals.values;

% Set up the figure and axes
fig = figure;
ax = axes('Parent', fig, 'NextPlot', 'replacechildren');
axis equal;
hold on;
grid on;
xlim([min([D1x, D2x, Ix]) - 5, max([D1x, D2x, Ix]) + 5]);
ylim([min([D1y, D2y, Iy]) - 5, max([D1y, D2y, Iy]) + 5]);

% Plotting the trajectories of the defenders and intruder
h1 = plot(D1x, D1y, 'r', 'LineWidth', 2);
h2 = plot(D2x, D2y, 'b', 'LineWidth', 2);
h3 = plot(Ix, Iy, 'g', 'LineWidth', 2);
xlabel('X position');
ylabel('Y position');
title('Trajectories of Defenders and Intruder');
grid on;

% Plot the target area as a circle
viscircles([targetX, targetY], targetRadius, 'Color', 'm', 'LineWidth', 2);

% Prepare for quiver plot by extracting LOS vector components for each time step
U_D1 = zeros(1, length(t));
V_D1 = zeros(1, length(t));
U_D2 = zeros(1, length(t));
V_D2 = zeros(1, length(t));

for i = 1:length(t)
    U_D1(i) = n1_D1_values(1,1,i);
    V_D1(i) = n1_D1_values(1,2,i);
    U_D2(i) = n1_D2_values(1,1,i);
    V_D2(i) = n1_D2_values(1,2,i);
end

% Plotting the LOS vector as an arrow from the current position of each defender
for i = 1:length(t)
    scale_factor = 4; 
    quiver(D1x(i), D1y(i), U_D1(i) * scale_factor, V_D1(i) * scale_factor, 'MaxHeadSize', 0.5, 'Color', 'r', 'AutoScale', 'off');
    quiver(D2x(i), D2y(i), U_D2(i) * scale_factor, V_D2(i) * scale_factor, 'MaxHeadSize', 0.5, 'Color', 'b', 'AutoScale', 'off');
end

% Labeling start positions
plot(D1x(1), D1y(1), 'rs', 'MarkerSize', 10, 'MarkerFaceColor', 'r');
plot(D2x(1), D2y(1), 'bs', 'MarkerSize', 10, 'MarkerFaceColor', 'b');
plot(Ix(1), Iy(1), 'gs', 'MarkerSize', 10, 'MarkerFaceColor', 'g');

% Labeling positions at specific time intervals
timeIntervals = 0:5:max(t); % From 0 to max time, every 5 seconds
for t_i = timeIntervals
    [~, idx] = min(abs(t - t_i)); % Find the index of the closest time

    % Plot circles at the positions of the drones at the current interval
    plot(D1x(idx), D1y(idx), 'ro', 'MarkerSize', 10);
    plot(D2x(idx), D2y(idx), 'bo', 'MarkerSize', 10);
    plot(Ix(idx), Iy(idx), 'go', 'MarkerSize', 10);

    % Connect the circles with a black dotted line
    plot([D1x(idx), Ix(idx)], [D1y(idx), Iy(idx)], 'k--');
    plot([D2x(idx), Ix(idx)], [D2y(idx), Iy(idx)], 'k--');
end

% Add legend
legend([h1, h2, h3], 'Defender 1', 'Defender 2', 'Intruder', 'Location', 'bestoutside');

% Release the hold on the current figure
hold off;