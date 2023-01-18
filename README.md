# Portfolio optimization with D-Wave quantum annealer
Author: Martin Vesely\
Organization: The Czech National Bank\
Project number: P2/22\
Project name: Finding Optimal Currency Composition of Foreign Exchange Reserves with a Quantum Computer\

# Purpose
This Python code is intended for Markowitz-like portfolio optimization 
with quantum annealer provided by D-Wave. The code has been developed 
as part of research project on application of quantum computers in finance 
(see above).

# Files description
Main program is in file main.py. Procedures for actual optimization
are saved in ptfOptim.py. As the optimization has to be formulated as QUBO for the annealer,
continuous objective function has to be binarized. The binarization
procedures are saved in quadProgramBinarization.py. Input data (i.e. returns,
covariance matrices and transaction costs) are provided in file inputData.py.
In this file, the data are saved as arrays which can be loaded with function
also saved in this file. Files toArray.py and filesOperations.py are auxiliary
ones intended for postprocessing of results and saving them into TXT files.
File advancedSimAnneal.py implements a function for multiple runs of
simulated annealing (SA implementation is however part of D-Wave libraries). 

All functions and procedures in above mentioned files are commented for easy 
understanding of purpose of particular parts of the code.

# Requirements
For using the code, it is necessary to have an account at D-Wave.

To run the optimization, all files have to be saved in one directory.

# Development environment
All the codes were developed in the D-Wave Leap (TM) environment.
