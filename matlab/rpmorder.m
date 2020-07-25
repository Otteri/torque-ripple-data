% fs = 1000;
% t1 = 30;
% t = 0:1/fs:t1;
% 
% f0 = 10;
% f1 = 40;
% rpm = 60*linspace(30,3000,length(t));
% 
% o1 = 1;
% o2 = 2.5;
% o6 = 6;
% 
% x = 2*chirp(t,o1*f0,t1,o1*f1)+chirp(t,o2*f0,t1,o2*f1) + ...
%     0.8*chirp(t,o6*f0,t1,o6*f1,'quadratic');
% times = rpmdata.times;
% speeds = rpmdata.speedrpm;
% coggings = rpmdata.Torquepu;
% fs = 1/0.001;

time = combineddata.y1;
speeds = combineddata.y2;
torques = combineddata.y3;
fs = 1/0.000052;

% [map,or,rp] = rpmordermap(coggings,fs,speeds,0.25, ...
%     'Amplitude','peak','Window',{'chebwin',80});

[map,or,rp] = rpmordermap(torques,fs,speeds);

[OR,RP] = meshgrid(or,rp);
waterfall(OR,RP,map')

%s = surf(OR,RP,map');
%s.EdgeColor = 'interp';

view(-15,45)
xlabel('Order')
ylabel('RPM')
zlabel('Amplitude')