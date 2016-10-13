function fitness = EvaluateChromosome(chromosome, set)

global STEP_SIZE START_SPEED START_T START_GEAR MAX_SPEED MAX_ALPHA MAX_T BETA


[weights, thresholds] = DecodeChromosome(chromosome);



if set == 1
    nbrSlopes =10;
else
    nbrSlopes = 5;
end

tmpFitnessArray = zeros(1,nbrSlopes);
for slope = 1:nbrSlopes;    
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
        alpha = GetSlopeAngle(x,slope,set);
        d = speed * STEP_SIZE;
        totDistance = totDistance + d;
        deltaX = d*cos(alpha*pi/180);
        deltaY =  -d*sin(alpha*pi/180);
        
        nextX = x+deltaX;
        nextY = y+deltaY;
        
        networkInput = [speed/MAX_SPEED; alpha/MAX_ALPHA; brakeT/MAX_T];
        networkOutput = FeedForward(networkInput, weights, thresholds, BETA);
        brakePressure = (networkOutput(1)+1)/2; %mapping output to [0,1]
        tmp = networkOutput(2);
        desiredGearChange = sign(tmp).*heaviside(abs(tmp)-0.5); %mapping output to {-1,0,1}
        
        if i == 1
            oldGear = START_GEAR;
        end
        if secondsSinceGearChange > 2
            iGear = oldGear + desiredGearChange;
            iGear = max(iGear,1); %restrict gears to [1,10]
            iGear = min(iGear,10);
            secondsSinceGearChange = 0;
            oldGear = iGear;
        else
            iGear = oldGear;
            secondsSinceGearChange = secondsSinceGearChange + STEP_SIZE;
        end
        
        [nextSpeed,nextBrakeT] = AccelerateTruck(speed, alpha, brakeT, brakePressure, iGear);
        
        
        x = nextX;
        y = nextY;
        t = t + STEP_SIZE;
        speed = nextSpeed;
        brakeT = nextBrakeT;
        sumSpeed = sumSpeed + nextSpeed;
        
        condition = totDistance < 1000 & nextBrakeT < MAX_T & nextSpeed < MAX_SPEED;
        i = i+1;
    end
    tmpFitnessArray(slope) = sumSpeed/i * totDistance;
end

%fitness = (mean(tmpFitnessArray) + min(tmpFitnessArray))/2;
fitness = mean(tmpFitnessArray);
end

