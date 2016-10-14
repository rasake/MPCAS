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
%     disp('----------')
    operator = chromosome(4*i+1);
    destinationIndex = chromosome(4*i+2);
    operand1 = num2str(masterRegisters{chromosome(4*i+3)});
    operand2 = num2str(masterRegisters{chromosome(4*i+4)});
%     disp( [num2str(operator) ' '  num2str(destinationIndex) ' ' num2str(operand1) ' ' num2str(operand2)])
    switch operator
        case 1
            if operand1 == '0' & isempty(strfind(operand2,'Inf'))
                result = operand2;
            elseif operand2 == '0' & isempty(strfind(operand1,'Inf'))
                result = operand1;
            else
                result = [operand1 '+' operand2];
            end
        case 2
            if length(operand1) == length(operand2) & operand1 == operand2
                result = '0';
            else
                result = [operand1 '-' operand2];
            end
        case 3
            if operand1 == '1'
                result = operand2;
            elseif operand2 == '1'
                result = operand1;
            elseif length(operand1)==2 & length(operand2)==2 & operand1=='-1' & operand2=='-1'
                result = '1';
            elseif length(operand1) == 2 & operand1 == '-1'
                result = ['(-' operand2 ')'];
            elseif length(operand2) == 2 & operand2 == '-1'
                result = ['-(' operand1 ')'];
            elseif length(operand1) == length(operand2) & operand1 == operand2
                if operand1(1) == '-'
                    result = ['(' operand1(2:end) ')^2'];
                else
                    result = ['(' operand1 ')^2'];  
                end          
            else
                result = ['(' operand1 ')*(' operand2 ')'];
            end            
        case 4
            if operand2 == '0'
                result = 'Inf';
            elseif length(operand1) == length(operand2) & operand1 == operand2
                result = '1';
            else
                result = ['(' operand1 ')/(' operand2 ')'];
            end
    end
    masterRegisters{destinationIndex} = result;
%     disp('----------')

y = masterRegisters{1};

end

