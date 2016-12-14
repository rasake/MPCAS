clc
clear all
clf

   
%% %%%%%% Parameters %%%%%%%
nbrTimeSteps = 10000;
p = 0.05; % tree prob
f = 0.5; % fire prob
N = 128;
initialTreeDensity = 0.1;
totNbrOfTrees = N^2;

%% %%%%%% Full simulation %%%%%%%%
% initalize forrest
forrestMatrix = rand(N) < initialTreeDensity ;
originalMatrix = forrestMatrix;
h1 = imagesc(originalMatrix);
h2 = imagesc(originalMatrix);
fireMetrics = [];
for k=1:nbrTimeSteps
    % grow trees
    forrestMatrix = ((rand(N,N) < p) + forrestMatrix) > 0;
    % potentially start a fire
    beforeFire  = forrestMatrix;
    if rand() < f
        i = randi(N);
        j = randi(N);
        forrestMatrix = Burn(forrestMatrix, i,j);
    end
    fireMatrix = beforeFire - forrestMatrix;

    nbrTreesBurnt = sum(sum(fireMatrix));
    if nbrTreesBurnt > 0
       relFireSize = nbrTreesBurnt/totNbrOfTrees;
       nbrTreesBeforeFire = sum(sum(beforeFire));
       densityBeforeFire = nbrTreesBeforeFire/totNbrOfTrees;
       fireMetrics = [fireMetrics;[densityBeforeFire, relFireSize]];       
    end
    % plottting
    delete(h1)
    delete(h2)
    hold on
    [greenX, greenY] = find(forrestMatrix == 1);
    h1 = scatter(greenX,greenY, 'g.');
    [orangeX, orangeY] = find(fireMatrix == 1);
    h2 = scatter(orangeX,orangeY, 'r.');
%     if sum(sum(fireMatrix)) > 0
%         pause(2)
%     end
    %pause(1.2)
end

%% Power law fit
xCut = x(find(x<0.01));
xLog = log(xCut);
cFreqLog = log(1-freq(1:length(xLog)));
plot(xLog, cFreqLog);
%%
% basic fitting yields slope
k = -0.163043294001174;
m = 1.604061672412913;

tau = 1-k;
C = exp(m);




%% Plotting
[freq,x] = ecdf(fireMetrics(:,2));

loglog(x,1-freq,'b')
hold on

xlabel('Rel. fire size')
ylabel('Rank Frequency')
%% Inverse sampling
nbrSamples = 10000;

samples = zeros(1, nbrSamples);
for k=1:nbrSamples
    r = rand();
    samples(k) = 1/128^2*(1-r)^(-1/(tau-1));
end
%%
nbrSamples = 10000;
randomNumbers = rand(1,nbrSamples);
samples = 1/128^2*(1-randomNumbers).^(-1/(tau-1));
%[freqSamp,xSamp] = ecdf(samples);
%% 
[freqSamp,xSamp] = ecdf(samples);
loglog(xSamp, 1-freqSamp,'r')
hold on
%loglog(freqSamp, xSamp,'r')

legend('Simulation Results', 'Inverse Transform Sampling')