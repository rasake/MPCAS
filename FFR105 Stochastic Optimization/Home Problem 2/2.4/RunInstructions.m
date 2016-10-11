function [ y ] = RunInstructions( x, chromosome, nbrVariableRegisters, constants )
%RUNINSTRUCTIONS Runs the instructions in chromosome with x as input

nGenes = length(chromosome);
nbrOfInstructions = nGenes/4;
% Store variable and consants in same register for ease of access
masterRegisters = [zeros(1, nbrVariableRegisters) constants];
masterRegisters(1) = x;

for i = 0:nbrOfInstructions-1
%     instruction = chromosome(4*i+1:4*(i+1));
%     operator = instruction(1);
%     destinationIndex = instruction(2);
%     operand1 = masterRegisters(instruction(3));
%     operand2 = masterRegisters(instruction(4));
    operator = chromosome(4*i+1);
    destinationIndex = chromosome(4*i+2);
    operand1 = masterRegisters(chromosome(4*i+3));
    operand2 = masterRegisters(chromosome(4*i+4));
    switch operator
        case 1
            result = operand1 + operand2;
        case 2
            result = operand1 - operand2;
        case 3
            result = operand1 * operand2;
        case 4
            if operand2 == 0
                result = 1e9;
            else
                result = operand1 / operand2;
            end
    end
    masterRegisters(destinationIndex) = result;

% Ensure constants have not been tampered with
%assert(masterRegisters(nbrVariableRegisters+1:end) == constanRegisters);
y = masterRegisters(1);

end

