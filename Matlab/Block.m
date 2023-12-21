% Initial condition: psi(heading angle), velocity(v), y position, x position
D1 = [pi/3, 1, 5, 2];
D2 = [-pi/3, 1, 7, 10];
I = [pi/6, 1.5, 12, 5];

simOut = sim("Block");
D1x = D1x1.Data(:)'; 
D1y = D1y1.Data(:)';
D2x = D2x1.Data(:)';
D2y = D2y1.Data(:)';
Ix = Ix1.Data(:)';
Iy = Iy1.Data(:)';
t = D1x1.Time(:)';  

% Plotting the trajectories of the defenders and intruder
figure;
hold on; 
h1 = plot(D1x, D1y, 'r', 'LineWidth', 2);
h2 = plot(D2x, D2y, 'b', 'LineWidth', 2);
h3 = plot(Ix, Iy, 'g', 'LineWidth', 2);
xlabel('X position');
ylabel('Y position');
title('Trajectories of Defenders and Intruder');
grid on;

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
    plot([D1x(idx), D2x(idx), Ix(idx)], [D1y(idx), D2y(idx), Iy(idx)], 'k--');
end

legend([h1, h2, h3], 'Defender 1', 'Defender 2', 'Intruder');

hold off;
