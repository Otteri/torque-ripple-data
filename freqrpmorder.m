% Load data by using csv-import

% times = rpmdata.times;
% speeds = rpmdata.speedrpm;
% coggings = rpmdata.Torquepu;
% fs = 1/0.001;

time = combineddata.y1;
speeds = combineddata.y2;
coggings = combineddata.y3;
fs = 1/0.000052;


%speeds = SpectrumAmplitudes.speedrpm;
%coggings = SpectrumAmplitudes.torqueNm;
%fs = 1/0.000008;

rpmfreqmap(coggings,fs,speeds);
%export_fig('-transparent', 'filename.pdf')
%exportgraphics(f,'map.png','Resolution',300)