% ------------------------------------------------------------------------------
% MIT License
% 
% Copyright (c) 2023 Dr. Longhao Qian
% 
% Permission is hereby granted, free of charge, to any person obtaining a copy
% of this software and associated documentation files (the "Software"), to deal
% in the Software without restriction, including without limitation the rights
% to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
% copies of the Software, and to permit persons to whom the Software is
% furnished to do so, subject to the following conditions:
% 
% The above copyright notice and this permission notice shall be included in all
% copies or substantial portions of the Software.
% 
% THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
% IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
% FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
% AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
% LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
% OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
% SOFTWARE.
% ------------------------------------------------------------------------------
close all
clear;
%% load flight path results
load('D1_pathsim.mat')
load('D2_pathsim.mat')
load('I_pathsim.mat')
addpath('../../src/models')
addpath('../../src/utils')
addpath('../../src/camera')
addpath('../../src/hud')
%% define the figure
anim_fig = figure('Units', 'normalized', 'OuterPosition', [0.2 0.2 0.6 0.6]);
ax = axes('Position',[0.1 0.1 0.8 0.8],  'XLim',[-100 100],'YLim',[-100 100],'ZLim',[-50 50], 'DataAspectRatio', [1 1 1]);
% Add a target area to the main map
theta = linspace(0, 2*pi, 100); % Generate 100 points for a smooth circle
x = 2 * cos(theta); % x coordinates for the perimeter of the circle
y = 2 * sin(theta); % y coordinates for the perimeter of the circle
patch(ax, x, y, 'magenta', 'EdgeColor', 'none'); % Add the solid color circle to the main axis
%% define the actual trajectory
% NED frame is used. (-100 is the height of the circule)
trajectory_line_D1 = line(pathsim_D1.Xe(:, 1), pathsim_D1.Xe(:, 2), pathsim_D1.Xe(:, 3), 'LineWidth', 1, 'Color', 'red');
trajectory_line_D2 = line(pathsim_D2.Xe(:, 1), pathsim_D2.Xe(:, 2), pathsim_D2.Xe(:, 3), 'LineWidth', 1, 'Color', 'blue');
trajectory_line_I = line(pathsim_I.Xe(:, 1), pathsim_I.Xe(:, 2), pathsim_I.Xe(:, 3), 'LineWidth', 1, 'Color', 'green');
%% define the quadrator
% Define colors for the drones
color_D1 = 'red';
color_D2 = 'blue';
color_I = 'green';

Q_D1 = CreateQuadRotor(0.7, 0.3, ax, color_D1, 'NED');
Q_D2 = CreateQuadRotor(0.7, 0.3, ax, color_D2, 'NED');
Q_I = CreateQuadRotor(0.7, 0.3, ax, color_I, 'NED');
%% invert the Y and Z axis to properly display NED frame
set(ax, 'YDir', 'reverse')
set(ax, 'ZDir', 'reverse')
xlabel(ax, 'x axis, m');
ylabel(ax, 'y axis, m');
zlabel(ax, 'z axis, m');
grid on
%% define camera mode
pc = [-3; 0; -2];
pt = [20; 0; -2];
InitCamera(ax, 85, 'perspective');
%% define a mini map
ax2 = axes('Units', 'Normalized', 'Position',[0.75 0.1 0.2 0.55],...
'Box', 'on', ...
'LineWidth', 2, ...
'Color', [1, 1, 1], 'DataAspectRatio', [1 1 1]);
% Add a solid color target area to the mini-map
patch(ax2, x, y, 'magenta', 'EdgeColor', 'none'); % Add the solid color circle to the mini-map axis
t1 = title(ax2, ['t = 0s']);
trajectory_line_D1_2 = line(pathsim_D1.Xe(:, 1), pathsim_D1.Xe(:, 2), pathsim_D1.Xe(:, 3),'LineWidth', 1, 'Color', 'red', 'Parent', ax2);
trajectory_line_D2_2 = line(pathsim_D2.Xe(:, 1), pathsim_D2.Xe(:, 2), pathsim_D2.Xe(:, 3), 'LineWidth', 1, 'Color', 'blue','Parent', ax2);
trajectory_line_I_2 = line(pathsim_I.Xe(:, 1), pathsim_I.Xe(:, 2), pathsim_I.Xe(:, 3), 'LineWidth', 1, 'Color', 'green','Parent', ax2);

set(ax2, 'XLim',[-12, 12]);
set(ax2, 'YLim',[-12, 12]);
set(ax2, 'ZDir', 'reverse')
Q_D1_2 = CreateQuadRotor(0.7, 0.2, ax2, color_D1, 'NED');
Q_D2_2 = CreateQuadRotor(0.7, 0.2, ax2, color_D2, 'NED');
Q_I_2 = CreateQuadRotor(0.7, 0.2, ax2, color_I, 'NED');
xlabel(ax2, 'x(m)')
ylabel(ax2, 'y(m)')
grid(ax2, 'on')
% Get the number of time steps in your simulation
n = length(pathsim_D1.time);

% GIF creation setup
saveToGif = true;  
filename_gif = "trajectory.gif";

% Define GIF parameters
frameRate = 14; % Desired frame rate for the GIF
actualTimeStep = mean(diff(pathsim_D1.time));
desiredTimeStep = 1 / frameRate;
skipFrames = round(desiredTimeStep / actualTimeStep);


% Set a threshold for the minimum time difference required to update the frame
minTimeDiff = 0.4;  % Adjust this value as needed, based on your dataset's time resolution

% Initialize a variable to keep track of the last updated time
lastUpdatedTime = -Inf;


% Set up amplitude for roll, pitch, and yaw changes
roll_amplitude = pi; 
pitch_amplitude = pi;
yaw_amplitude = pi;   

% Animation loop
for k = 1 : n
    % Check if the time difference is too small to update the frame
    if k < n && (pathsim_D1.time(k+1) - lastUpdatedTime) < minTimeDiff
        continue;  % Skip this iteration and do not update the frame
    end
    
    % Update the last updated time
    lastUpdatedTime = pathsim_D1.time(k);

    % Calculate roll, pitch, and yaw for this frame
    roll = roll_amplitude * sin(2 * pi * k / n);
    pitch = pitch_amplitude * cos(2 * pi * k / n);
    yaw = yaw_amplitude * sin(2 * pi * k / n);

    % Update the drone1 model with attitude changes
    R_D1 = GenerateHgRotation([roll, pitch, yaw], 'euler', "NED");
    T_D1 = makehgtform('translate', [pathsim_D1.Xe(k, 1), pathsim_D1.Xe(k, 2), pathsim_D1.Xe(k, 3)]);
    set(Q_D1.frame, 'Matrix', T_D1 * R_D1);
    set(Q_D1_2.frame, 'Matrix', T_D1 * R_D1);

    % Update the drone 2 model with attitude changes
    R_D2 = GenerateHgRotation([-roll, -pitch, -yaw], 'euler', "NED");
    T_D2 = makehgtform('translate', [pathsim_D2.Xe(k, 1), pathsim_D2.Xe(k, 2), pathsim_D2.Xe(k, 3)]);
    set(Q_D2.frame, 'Matrix', T_D2 * R_D2);
    set(Q_D2_2.frame, 'Matrix', T_D2 * R_D2);

    % Update the drone 3 model with attitude changes
    R_I = GenerateHgRotation([roll, -pitch, yaw], 'euler', "NED");
    T_I = makehgtform('translate', [pathsim_I.Xe(k, 1), pathsim_I.Xe(k, 2), pathsim_I.Xe(k, 3)]);
    set(Q_I.frame, 'Matrix', T_I * R_I);
    set(Q_I_2.frame, 'Matrix', T_I * R_I);
        
    % Update the camera
    C21 = reshape(pathsim_I.Rbe(:, :, k), 3, 3)';
    UpdateCameraModelFixed(ax, pathsim_I.Xe(k, :), pc, pt, C21, 'NED');

    % Update the animation render range
    set(ax, 'XLim', [-20 + pathsim_I.Xe(k, 1), 20 + pathsim_I.Xe(k, 1)]);
    set(ax, 'YLim', [-20 + pathsim_I.Xe(k, 2), 20 + pathsim_I.Xe(k, 2)]);
    set(ax, 'ZLim', [-20 + pathsim_I.Xe(k, 3), 20 + pathsim_I.Xe(k, 3)]);
    set(t1, 'String', ['t=', num2str(pathsim_I.time(k), '%.2f')]);

    if saveToGif
        frame = getframe(anim_fig);
        im = frame2im(frame);
        [imind, cm] = rgb2ind(im, 256);
        if k == 1
            imwrite(imind, cm, filename_gif, 'gif', 'Loopcount', inf, 'DelayTime', 1/frameRate);
        else
            imwrite(imind, cm, filename_gif, 'gif', 'WriteMode', 'append', 'DelayTime', 1/frameRate);
        end
    end

    % Update the window with the latest changes
    drawnow limitrate;
end