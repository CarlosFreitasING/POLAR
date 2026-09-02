
Recorrido del trabajador el 11/08/2025:

LÍNEA DE TIEMPO DE LA JORNADA

08:00 ───── 10:00  Preparación de muestras de panel sándwich en Moreira de Cónegos.
				  Manipulación y transporte de paneles de 20 kg, corte de muestras
				  y limpieza del área de trabajo.

10:00 ───── 10:45  Desplazamiento desde Moreira de Cónegos hasta Oporto.

10:45 ───── 12:00  Colocación de 4 paneles sándwich de fachada.

12:00 ───── 13:00  Almuerzo.

13:00 ───── 17:50  Colocación de 12 paneles sándwich de fachada.
				  Preparación de paneles para canalones de acero, manipulación,
				  corte y montaje de placas de acero en la fachada.

17:50 ───── 18:35  Desplazamiento desde Oporto hasta Moreira de Cónegos.

18:35                Fin aproximado de la jornada y de la adquisición de datos.

-------------------------------------------------------------------------------------------
1. De 08:00 a 10:00: preparación de muestras de panel sándwich en Moreira de Cónegos.
Descripción del trabajo en Moreira de Cónegos: manipulación ligera y transporte de paneles sándwich de 20 kg por dos trabajadores.
Corte de muestras con sierra circular, sierra sable y amoladora angular. Limpieza del área de trabajo y retirada de residuos.

2. Desplazamiento desde Moreira de Cónegos hasta Oporto a las 10:00.
Duración aproximada: 45 minutos.

3. Colocación de 4 paneles sándwich de fachada entre las 10:45 y las 12:00.

4. Almuerzo de 12:00 a 13:00.

5. Colocación de 12 paneles sándwich de fachada entre las 13:00 y las 17:50.
Preparación adicional de paneles sándwich para canalones de acero.
Las operaciones adicionales incluyen la manipulación de placas de acero, así como su corte y montaje en la fachada utilizando herramientas ligeras.

6. Desplazamiento desde Oporto hasta Moreira de Cónegos a las 17:50.
Duración aproximada: 45 minutos.

Fin de la adquisición.
_______

Aplicación utilizada para la adquisición de datos:
https://www.ecglogger.com/

Teléfonos móviles utilizados para la adquisición de datos:
CW00 = CW04
CW01 - Samsung Galaxy A25 5G
CW02 - Samsung Galaxy A26 5G
CW03 - Samsung Galaxy A26 5G
CW04 - Samsung Galaxy A26 5G

GG9903 / GG9906: adquisición de datos de los trabajadores en condiciones de trabajo.
W00 - RG
W01 - GF
W02 - CB
W03 - GS
W04 - FM
_______

Sincronización horaria. El teléfono móvil del trabajador 02 tenía una diferencia horaria de una hora.
Las bandas Polar H10 se colocaron secuencialmente en los trabajadores con la ayuda del responsable.
Los archivos están separados por hora.

CW00 - 10:05
CW01 - 10:05
CW02 - 16:05
CW03 - 10:05
CW04 - 10:05
________

Estructura de los datos:

Columna 01 - tiempo UNIX en nanosegundos. Para convertirlo a fecha de Excel se puede utilizar la fórmula "=((A1/86400)+25569)".

Columna 02 - contiene la señal ECG en milivoltios.
La adquisición de la señal utiliza un filtro de media móvil para eliminar el componente de corriente continua de la señal.
Los valores oscilan entre -3 y 3 milivoltios.
La frecuencia de adquisición aproximada es de 130 Hz.
Aunque no se trata de un dispositivo médico, es posible observar algunas características del complejo PQRST.
Contracción auricular - onda P. Despolarización ventricular - onda R. Repolarización del miocardio - onda T.
La señal depende en gran medida de la colocación de la banda Polar y es susceptible a los artefactos producidos por el movimiento.
La colocación de los electrodos es diferente de la utilizada en un Holter ECG, pero presenta resultados prometedores para la práctica clínica.
https://www.researchgate.net/publication/363193345_Feasibility_of_evaluation_of_Polar_H10_chest-belt_ECG_in_patients_with_a_broad_range_of_heart_conditions

Columna 03 - pulso en latidos por minuto [bpm] (= f [Hz] * 60).

Columna 04 - intervalo R-R en milisegundos [ms].

Columna 05 - marcador añadido por el usuario. No se utilizó durante el muestreo.