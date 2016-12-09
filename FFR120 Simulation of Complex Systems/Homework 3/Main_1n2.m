clc
clear all
clf

   
%% %%%%%% Parameters %%%%%%%
nbrTimeSteps = 10000;
p = 0.1; % tree prob
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
    if sum(sum(fireMatrix)) > 0
        pause(0.01)
    end
    pause(0.3)
end


%% %%%%%%%% Single fire simulations %%%%%%%%%
nbrDensities = length(fireMetrics(:,1));
nbrDataPoints = 1;

fireSizes = [];
for k=1:nbrDensities
    density = fireMetrics(k,1);
    for l=1:nbrDataPoints
        beforeFire = rand(N) < density;
        [i,j] = RandomlyChooseTree(beforeFire);
        afterFire = Burn(beforeFire, i,j);
        nbrTreesBurnt = sum(sum(abs(beforeFire-afterFire)));
        relFireSize = nbrTreesBurnt/totNbrOfTrees;
        fireSizes = [fireSizes relFireSize];
    end
end

%% graphs for exercise 2

% % % plot full sim
[freq,x] = ecdf(fireMetrics(:,2));
loglog(x,1-freq,'b')
hold on
% % % plot single step sim
[freq,x] = ecdf(fireSizes);
loglog(x,1-freq, 'r')

xlabel('Rel. fire size')
ylabel('Rank Frequency')
title(['Rank Frequency Plot for f=', num2str(f), ', p=', num2str(p)])
legend('Long term dynamics', 'Uniformly distributed forrests')
