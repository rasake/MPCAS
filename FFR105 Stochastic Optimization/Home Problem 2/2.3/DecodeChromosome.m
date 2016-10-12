function [ weights, thresholds ] = DecodeChromosome( chromosome )

global NBR_HIDDEN_NEURONS

weights = cell(1,2);

% matrix 1
matrix1 = [];
for i = 1:3:NBR_HIDDEN_NEURONS*3
    iRow = chromosome(i:i+2);
    matrix1 = [matrix1; iRow];
end
weights{1} = matrix1;
%matrix2
matrix2 = [];
for i = NBR_HIDDEN_NEURONS*3+1:NBR_HIDDEN_NEURONS:NBR_HIDDEN_NEURONS*5
    iRow = chromosome(i:i+NBR_HIDDEN_NEURONS-1);
    matrix2 = [matrix2; iRow];
end
weights{2} = matrix2;


thresholds = cell(1,2);
thresholds{1} = chromosome(NBR_HIDDEN_NEURONS*5+1:NBR_HIDDEN_NEURONS*6)';
thresholds{2} = chromosome(NBR_HIDDEN_NEURONS*6+1:end)';


end

