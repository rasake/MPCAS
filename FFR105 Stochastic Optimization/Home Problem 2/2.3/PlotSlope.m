%close all
slope = 1;
set = 1;
deltaX = 0.1;
x = linspace(0,1000,1000/deltaX);

y = [2000];
for i = 2:1000/deltaX
   alpha = GetSlopeAngle(x(i),slope,set);
   deltaY = deltaX * tan(-alpha*pi/180);
   nextY = y(i-1)+deltaY;
   y = [y nextY];
end

plot(x,y)
%plot(x,GetSlopeAngle(x,slope,set))