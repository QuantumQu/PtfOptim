# Portfolio optimization with D-Wave quantum annealer
Author: Martin Vesely\
Organization: The Czech National Bank\
Project number: P2/22\
Project name: Finding Optimal Currency Composition of Foreign Exchange Reserves with a Quantum Computer\

--------------------------------------------------------------------------------------------------------\
This Python code is intended for Markowitz-like portfolio optimization 
with quantum annealer provided by D-Wave. The code has been developed 
as part of research project on application of quantum computers in finance 
(see header).

Main program is in file main.py. Procedures for actual optimization
are saved in ptfOptim.py. As the optimization is formulated as QUBO,
continuous objective function has to be binarized. The binarization
procedures are saved in quadProgramBinarization.py. Input data (i.e. returns,
covariance matrices and transaction costs) are provided in file inputData.py.
In this file, the data are saved as arrays which can be loaded with function
also saved in this file. Files toArray.py and filesOperations.py are auxiliary
once inteded for postprocessing of results and saving them into TXT files.
Last file advancedSimAnneal.py implements a function for multiple runs of
simulated annealing (SA implementation is however part of D-Wave libraries). 

All functions and procedures in above mentioned files are commented.

For using the code, it is necessary to have an account at D-Wave.

All the codes were developed in the D-Wave Leap (TM) environment.

