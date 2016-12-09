clc
clear all
clf

   
%% %%%%%% Parameters %%%%%%%
nbrTimeSteps = 10000;
p = 0.01; % tree prob
f = 0.1; % fire prob
N = 8;
initialTreeDensity = 0.1;
totNbrOfTrees = N^2;


%% %%%%%% Full simulation %%%%%%%%
% initalize forrest
forrestMatrix = rand(N) < initialTreeDensity ;
originalMatrix = forrestMatrix;
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
end

%% Power law fit
[freq,x] = ecdf(fireMetrics(:,2));
xCut = x(find(x<0.1));
xLog = log(xCut);
cFreqLog = log(1-freq(1:length(xLog)));
plot(xLog, cFreqLog);


% 
% %% Rejection sampling
% nbrSamples = 5000;
% 
% samples = zeros(1, nbrSamples);
% for k=1:nbrSamples
%     r = rand()
%     samples(k) = theoreticCDF(r)
% end
% 


%% Plotting
[freq,x] = ecdf(fireMetrics(:,2));
loglog(x,1-freq,'b')
hold on

xlabel('Rel. fire size')
ylabel('Rank Frequency')
title(['Rank Frequency Plot for f=', num2str(f), ', p=', num2str(p)])


%% 
matrixSizes = [8,16,32,64,128,256,512]';
slopes = [-0.288446497214688, -0.278389820367614, -0.222173356498579,...
-0.213861687461618, -0.168011629382435, -0.154937512962719, -0.154945137834750]';
taus = 1-slopes;
X = 1./matrixSizes;
plot(X,taus, 'b.')
title('Task 4')
legend('Simulation results')
xlabel('1/N')
ylabel('Power law exponent')
% g = fit(X,slopes,'a*exp(b*x)+c')
% plot(g,X,slopes)