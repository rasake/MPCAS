function [ newSpeed, newBrakeT ] = AccelerateTruck(speed, alpha, brakeT, brakePressure, gear)
global TRUCKMASS MAX_T AMBIENT_T TAU Ch Cb STEP_SIZE


g = 9.82;
Fg = TRUCKMASS*g*sin(alpha*pi/180);

if brakeT < MAX_T-100
    foundationBrakeForce = TRUCKMASS*g/20*brakePressure;
else
    foundationBrakeForce = TRUCKMASS*g/20*brakePressure*exp(-(brakeT-(MAX_T-100))/100);
end

switch gear
    case 1
        engineBrakeForce = 7*Cb;
    case 2
        engineBrakeForce = 5*Cb;
    case 3
        engineBrakeForce = 4*Cb;
    case 4
        engineBrakeForce = 3*Cb;
    case 5
        engineBrakeForce = 2.5*Cb;
    case 6
        engineBrakeForce = 2*Cb;
    case 7
        engineBrakeForce = 1.6*Cb;
    case 8
        engineBrakeForce = 1.4*Cb;
    case 9
        engineBrakeForce = 1.2*Cb;
    case 10
        engineBrakeForce = Cb;
end

truckAcceleration = (Fg - foundationBrakeForce - engineBrakeForce) / TRUCKMASS;

newSpeed = speed + truckAcceleration * STEP_SIZE;
newSpeed = max(newSpeed,0);

relBrakeT = brakeT-AMBIENT_T;
if brakePressure < 0.01
    newRelBrakeT = relBrakeT - brakeT/TAU * STEP_SIZE;
else
    newRelBrakeT = relBrakeT + Ch*brakePressure * STEP_SIZE;
end
newBrakeT = max(AMBIENT_T + newRelBrakeT, AMBIENT_T);

end

