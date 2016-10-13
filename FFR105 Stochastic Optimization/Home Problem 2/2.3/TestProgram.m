clear all
clc
global TRUCKMASS MAX_T AMBIENT_T TAU Ch Cb STEP_SIZE MAX_SPEED MAX_ALPHA
global START_SPEED START_GEAR START_T
global NBR_HIDDEN_NEURONS BETA

TRUCKMASS = 20000; %kg
MAX_T = 750; %Kelvin
AMBIENT_T = 283; %Kelvin
TAU = 30; %seconds
Ch = 40; %K/s
Cb = 3000; %N
MAX_SPEED = 25; %m/s
MAX_ALPHA = 10; %degrees
START_SPEED = 20; %m/s
START_GEAR = 7;
START_T = 500; %K
STEP_SIZE = 0.01;
NBR_HIDDEN_NEURONS = 3;
BETA = 0.2;
slope = 1;
set = 2;

bestChromosome = [0.84063 0.71455 -0.88914 -0.019155 0.95563 0.51375 -0.41326 -0.066065 0.34416 0.79152 -0.1303 -0.68813 0.48622 -0.88955 0.43923 0.82755 0.045899 -0.24387 0.99432 -0.36209];


[x, speed, brakeT, brakePressure, gear] = RunSlopeDetailed(bestChromosome, slope, set);

if set == 2
    titleStr = ['Running the best network on slope ' num2str(slope) ' in the test set'];
else
    titleStr = ['Running the best network on slope ' num2str(slope) ' in the set' num2str(set)];
end

subplot(5,1,1)
plot(x,GetSlopeAngle(x, slope, set))
ylabel('Alpha')
title(titleStr)

subplot(5,1,2)
plot(x(1:end-1),brakePressure)
ylabel('Brake Pressure')

subplot(5,1,3)
plot(x(1:end-1),gear)
ylabel('gear')

subplot(5,1,4)
plot(x,speed)
ylabel('speed')

subplot(5,1,5)
plot(x,brakeT)
xlabel('x')
ylabel('Brake Temp.')

