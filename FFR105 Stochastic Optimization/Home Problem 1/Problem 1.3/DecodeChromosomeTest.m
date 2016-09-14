% test DecodeChromosome

%% Test 1: One variable chromosome
chromosome = [0 1 0 1 1 0 1 0 1 1];
variableRange = 3;
xExpected = -0.8710;
xCalculated = DecodeChromosome(chromosome, 1, variableRange);
error = xExpected - xCalculated;
assert(norm(error) < 0.0001)

%% Test 2: Two variable chromosome
chromosome = [0 1 0 1 1 0 1 0 1 1 0 1 0 1 1 0 1 0 1 1];
variableRange = 3;
xExpected = [-0.8710, -0.8710];
xCalculated = DecodeChromosome(chromosome, 2, variableRange);
error = xExpected - xCalculated;
assert(norm(error) < 0.0001)

%% Test 3: Three variable chromosome
chromosome = [0 1 0 1 1 0 1 0 1 1 0 1 0 1 1 0 1 0 1 1 0 1 0 1 1 0 1 0 1 1];
variableRange = 3;
xExpected = [-0.8710, -0.8710, -0.8710];
xCalculated = DecodeChromosome(chromosome, 3, variableRange);
error = xExpected - xCalculated;
assert(norm(error) < 0.0001)
