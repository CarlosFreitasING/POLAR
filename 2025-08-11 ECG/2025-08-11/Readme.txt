
Worker journey in 2025-08-11:

1. From 08:00 to 10:00 preparing sandwich panel samples in Moreira de Cónegos.
Work description in Moreira de Cónegos: Ligth manipulation and transport of 20 kg sandwich panel by 2 workers. 
Cut of samples with circular saw, saber and angle grinder. Cleaning workspace of debris.

2. Commuting from Moreira de Cónegos to Porto at 10:00.
Approximate duration of 45 minutes.

3. Placement of 4 façade sandwich panels from 10:45 to 12:00.

4. Lunch from 12:00 to 13:00.

5. Placement of 12 façade sandwich panels from 13:00 to 17:50. 
Additional preparation of sandwich panel for rain steel gutters.
Additional operations include manipulation steel plates, cuting and assembling on the façade with ligth elements.

6. Commuting from Porto to Moreira de Cónegos at 17:50.
Approximate duration of 45 minutes.

End of acquisition.
_______

App used for data acquisition:
https://www.ecglogger.com/

Cellphones used for data acquisition:
CW00 = CW04
CW01 - Samsung Galaxy A25 5G
CW02 - Samsung Galaxy A26 5G
CW03 - Samsung Galaxy A26 5G
CW04 - Samsung Galaxy A26 5G

GG9903 / GG9906 worker acquisition in working conditions.
W00 - RG
W01 - GF
W02 - CB
W03 - GS
W04 - FM
_______

Time sync. Cellphone from Worker 02 had diferent fuse time.
The polar band H10 were placed in workers sequentially and aided by responsible.
Files are separated by hour.

CW00 - 10:05
CW01 - 10:05
CW02 - 16:05
CW03 - 10:05
CW04 - 10:05
________

Data structure:

Collumn 01 - UNIX time epoch in nanoseconds. To convert to excel date use formula "=((A1/86400)+25569)".

Collumn 02 - Has ECG signal in milivolt. 
Signal acquisition uses moving average filter to remove DC component of the signal. 
Values range from -3 milivolt to 3 milivolt.
Rough acquisition frequency of 130 Hz.
Despite not being a medical device it is possible to observe some features like from the PQRST complex.
Atrial contraction - P. Ventricular depolarization - R. Myocardial repolarization - T.
Signal is highly dependent on polar band placement and susceptible to movement artifacts.
Electrodes placement differs from ECG holter but show promising results for clinical practice.
https://www.researchgate.net/publication/363193345_Feasibility_of_evaluation_of_Polar_H10_chest-belt_ECG_in_patients_with_a_broad_range_of_heart_conditions

Collumn 03 - pulse in beats per minute [bpm] (= f [Hz] * 60)

Collumn 04 - R-R interval in miliseconds [ms].

Collumn 05 - User added marker. Not used in the sampling.