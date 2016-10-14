function [x, speed, brakeT, brakePressure, gear] = RunSlopeDetailed(chromosome, slope, set)

global STEP_SIZE START_SPEED START_T START_GEAR MAX_SPEED MAX_ALPHA MAX_T BETA


[weights, thresholds] = DecodeChromosome(chromosome);



t = 0;
x = 0;
totDistance = 0;
y = 2000;
speed = START_SPEED;
sumSpeed = speed;
brakeT = START_T;

condition = true;
i = 1;
secondsSinceGearChange = 0;
while condition
    iTime = t(i);
    iX = x(i);
    iY = y(i);
    iSpeed = speed(i);
    iAlpha = GetSlopeAngle(iX,slope,set);
    d = iSpeed * STEP_SIZE;
    totDistance = totDistance + d;
    deltaX = d*cos(iAlpha*pi/180);
    deltaY =  -d*sin(iAlpha*pi/180);
    
    nextX = iX+deltaX;
    nextY = iY+deltaY;
    
    iBrakeT = brakeT(i);
    networkInput = [iSpeed/MAX_SPEED; iAlpha/MAX_ALPHA; iBrakeT/MAX_T];
    networkOutput = FeedForward(networkInput, weights, thresholds, BETA);
    iBrakePressure = (networkOutput(1)+1)/2; %mapping output to [0,1]
    brakePressure(i) = iBrakePressure;
    tmp = networkOutput(1);
    desiredGearChange = sign(tmp).*heaviside(abs(tmp)-0.1); %mapping output to {-1,0,1}
    
    if i == 1
        oldGear = START_GEAR;
    else
        oldGear = gear(i-1);
    end
    if secondsSinceGearChange > 2
        iGear = oldGear + desiredGearChange;
        iGear = max(iGear,1); %restrict gears to [1,10]
        iGear = min(iGear,10);
        secondsSinceGearChange = 0;
    else
        iGear = oldGear;
        secondsSinceGearChange = secondsSinceGearChange + STEP_SIZE;
    end
    gear(i) = iGear;
    
    [nextSpeed,nextBrakeT] = AccelerateTruck(iSpeed, iAlpha, iBrakeT, iBrakePressure, iGear);
    
    
    x(i+1) = nextX;
    y(i+1) = nextY;
    t(i+1) = iTime + STEP_SIZE;
    speed(i+1) = nextSpeed;
    brakeT(i+1) = nextBrakeT;
    sumSpeed = sumSpeed + nextSpeed;
    
    condition = totDistance < 1000 & nextBrakeT < MAX_T & nextSpeed < MAX_SPEED;
    i = i+1;
end

end

