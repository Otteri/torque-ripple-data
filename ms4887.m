clear;
% Script reads CSV-files and then creates plots automatically.
% The csv-data columns are assumed to be standard between the files.
% This assumption should be fine, because software generates the data.
%
% Vector graphic can be exported by using this command:
% export_fig(’-transparent’, ’filename.pdf’)


% These values are from motor nameplate
P = 6000;   % watt
rpm = 2000; % rad/min

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

    % Finally, create the plots
    plotdata('line_chart', {filename, time, speed});
    plotdata('amplitude_spectrum', {filename, time, speed});     
end
