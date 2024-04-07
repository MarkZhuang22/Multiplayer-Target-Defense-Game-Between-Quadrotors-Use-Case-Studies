%% Prediction Interception
% Initial condition: velocity(v), y position, x position
D1 = [1, 26, 23];
D2 = [1, 23, 26];
I = [1.5, 30, 30];

% Define target area
targetX = 0;
targetY = 0;
targetRadius = 2;

simOut = sim("ModelPrediction");
D1x = simOut.get('D1x').Data(:)';
D1y = simOut.get('D1y').Data(:)';
D2x = simOut.get('D2x').Data(:)';
D2y = simOut.get('D2y').Data(:)';
Ix = simOut.get('Ix').Data(:)';
Iy = simOut.get('Iy').Data(:)';
t = simOut.get('tout');

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

% Labeling start positions
plot(D1x(1), D1y(1), 'rs', 'MarkerSize', 10, 'MarkerFaceColor', 'r');
plot(D2x(1), D2y(1), 'bs', 'MarkerSize', 10, 'MarkerFaceColor', 'b');
plot(Ix(1), Iy(1), 'gs', 'MarkerSize', 10, 'MarkerFaceColor', 'g');
 
% Labeling positions at specific time intervals
timeIntervals = 0:5:max(t);  % From 0 to max time, every 5 seconds
for t_i = timeIntervals
    [~, idx] = min(abs(t - t_i));  % Find the index of the closest time

    % Plot circles at the positions of the drones at the current interval
    plot(D1x(idx), D1y(idx), 'ro', 'MarkerSize', 10);
    plot(D2x(idx), D2y(idx), 'bo', 'MarkerSize', 10);
    plot(Ix(idx), Iy(idx), 'go', 'MarkerSize', 10);

    % Connect the circles with a black dotted line
    % Plot line from Defender 1 to Intruder
    plot([D1x(idx), Ix(idx)], [D1y(idx), Iy(idx)], 'k--');
    % Plot line from Defender 2 to Intruder
    plot([D2x(idx), Ix(idx)], [D2y(idx), Iy(idx)], 'k--');

end

legend([h1, h2, h3], 'Defender 1', 'Defender 2', 'Intruder','Location', 'southeast');

hold off;

%% Save to mat files to create gif
% Add 'frame' to the structured data, without 'reference'
frame = 'NED'; % Assuming North-East-Down frame of reference

% Now create the 'pathsim' structure without the 'reference' field
pathsim_D1 = struct('Xe', [D1x', D1y', zeros(length(D1x), 1)], 'frame', frame, ...
                    'attitude', zeros(length(t), 3), 'time', t', ...
                    'Rbe', repmat(eye(3), 1, 1, length(t)), 'TAS', zeros(length(t), 1));
pathsim_D2 = struct('Xe', [D2x', D2y', zeros(length(D2x), 1)], 'frame', frame, ...
                    'attitude', zeros(length(t), 3), 'time', t', ...
                    'Rbe', repmat(eye(3), 1, 1, length(t)), 'TAS', zeros(length(t), 1));
pathsim_I = struct('Xe', [Ix', Iy', zeros(length(Ix), 1)], 'frame', frame, ...
                   'attitude', zeros(length(t), 3), 'time', t', ...
                   'Rbe', repmat(eye(3), 1, 1, length(t)), 'TAS', zeros(length(t), 1));

% Save the .mat files
save('D1_pathsim.mat', 'pathsim_D1');
save('D2_pathsim.mat', 'pathsim_D2');
save('I_pathsim.mat', 'pathsim_I');