time = combineddata.y1;
speeds = combineddata.y2;
torques = combineddata.y3;
fs = 1/0.000052;

[map,or,rp] = rpmordermap(torques,fs,speeds);
[OR,RP] = meshgrid(or,rp);
waterfall(OR,RP,map')

view(-15,45)
xlabel('Order')
ylabel('RPM')
zlabel('Amplitude')