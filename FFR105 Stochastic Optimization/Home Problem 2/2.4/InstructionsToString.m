function [ y ] = InstructionsToString( chromosome, nbrVariableRegisters, constants)
%RUNINSTRUCTIONS Runs the instructions in chromosome with x as input

nGenes = length(chromosome);
nbrOfInstructions = nGenes/4;
nbrConstants = length(constants);
% Store variable and consants in same register for ease of access
masterRegisters =  cell(1, nbrVariableRegisters+nbrConstants);

for i = 1: nbrVariableRegisters
   masterRegisters{i} = num2str(0); 
end
masterRegisters{1} = 'x';
for i = 1: nbrConstants
   masterRegisters{nbrVariableRegisters+i} = num2str(constants(i));
end


for i = 0:nbrOfInstructions-1
    operator = chromosome(4*i+1);
    destinationIndex = chromosome(4*i+2);
    operand1 = num2str(masterRegisters{chromosome(4*i+3)});
    operand2 = num2str(masterRegisters{chromosome(4*i+4)});
    switch operator
        case 1
            result = [operand1 '+' operand2];
        case 2
            if operand1 == operand2
                result = '0';
            else
                result = [operand1 '-' operand2];
            end
        case 3
            result = [operand1 '*' operand2];
        case 4
            if operand2 == '0'
                result = 'Inf';
            elseif operand1 == operand2
                result = '1';
            else
                result = ['(' operand1 ')/(' operand2 ')'];
            end
    end
    masterRegisters{destinationIndex} = result;

y = masterRegisters{1};

end

