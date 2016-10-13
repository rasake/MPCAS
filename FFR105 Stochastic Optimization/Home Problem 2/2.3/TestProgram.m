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

bestChromosome = [0.67613 0.79888 0.80765 0.087744 -0.47502 0.4147 -0.77812 0.53967 -0.68642 -0.97956 -0.22278 -0.17582 0.89331 0.93655 0.75374 -0.043294 -0.46897 -0.037936 1.0783 -0.41749];


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

