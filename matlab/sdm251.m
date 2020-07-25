clear;
% Script reads CSV-files and then creates plots automatically.
% The csv-data columns are assumed to be standard between the files.
% This assumption should be fine, because software generates the data.
%
% Vector graphic can be exported by using this command:
% export_fig(’-transparent’, ’filename.pdf’)


% These values are from motor nameplate
P = 720;    % watt
rpm = 3000; % rad/min
T_nom = getNominalTorque(P, rpm); % Calculate nominal torque

% Get all data files from selected directory
d = uigetdir(pwd, 'Select a folder');
if d == 0; return; end % Do nothing if user presses cancel
files = dir(fullfile(d, '*.csv'));

% Loop through the files
for i=1:numel(files)
    % Resolve the file location
    filename = files(i).name;
    filepath = join([files(i).folder, '\', filename]);
    
    % Read the data
    temp = csvread(filepath);
    time = temp(:, 1);   % Time (s)
    speed = temp(:, 2);  % Speed (rpm)
    torque = temp(:, 3); % Torque (%)    [3 ctrl, 4 sim]

    % Convert torque percents to Nm
    torque_Nm = percent2base(torque, T_nom);

    % Finally, create the plots
    plotdata('linechart', {filename, time, torque});
    plotdata('amplitude_spectrum', {filename, time, torque});     
    plotdata('linechart2', {filename, time, torque_Nm, speed});
end

% Calculate motor nominal torque
function T_nom = getNominalTorque(P, rpm)
    T_nom = (60*P) / (2*pi*rpm);
end

% Convert percents to base units
function base_values = percent2base(percent_values, nominals)
    decimals = 0.01 * percent_values;
    base_values = decimals .* nominals;
end
