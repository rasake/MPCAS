
loopStop = 100;
tmpMinArray = zeros(1,loopStop);
parfor ix = 1:loopStop
    tmpMinArray(ix) = 1/FunctionOptimizationPar();
end

average = mean(tmpMinArray);
stDev = std(tmpMinArray);

disp('Average min: ')
disp(mean(tmpMinArray));
disp('Median min: ')
disp(median(tmpMinArray));
disp('Standard dev. min: ')
disp(std(tmpMinArray));