
fitness = [1 3 54 2 55 7];
[topDog, topIndex] = max(fitness);
tmp = 0;
for i = 1:300
    iSelected = TournamentSelect(fitness, 0, 6);
    tmp_i = iSelected == topIndex;
    tmp = tmp + tmp_i;
end
disp('Cases of best ind. sel.: ' )
disp(tmp)
