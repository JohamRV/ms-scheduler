import connect_mongo
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
import statsmodels.api as sm
import datetime

diccionario_inst = connect_mongo.conexion_mongo()

#print(type(diccionario_inst))
#print('----------------------')
#print(diccionario_inst)
lista_instancias = []
#print(type(diccionario_inst.keys()))

diccionario_prediccion = {}
for nombre_instancia in diccionario_inst.keys():


    diccionario_pc1 = diccionario_inst[nombre_instancia]

    df = pd.DataFrame([[key, diccionario_pc1[key]] for key in diccionario_pc1.keys()], columns=['timestamp', 'cpu'])

    print(df)

    #Tomas los ultimos 75 valores, se consideran 3 periodos de muestras
    df_last75 = df.tail(30) 
    # Realizar la descomposición de la serie temporal, se considera un periodo de 25 muestras
    decomposition = sm.tsa.seasonal_decompose(df_last75['cpu'], model='additive',period = 10)


    # Obtener la componente estacional, la tendencia y el residuo
    seasonal = decomposition.seasonal
    trend = decomposition.trend
    residual = decomposition.resid

    # Valores mayores a 0
    seasonal = seasonal.clip(lower=0)

    repeated_signal = np.tile(seasonal[0:20], 2)
    #plt.figure(figsize=(18, 8))
    #plt.plot(repeated_signal)
    #plt.xlabel('Tiempo')
    #plt.ylabel('Amplitud')
    #plt.title('Señal periódica')
    #plt.grid(True)
    #plt.show()

    # Aplicar la condición y asignar los valores correspondientes
    valores = np.where(repeated_signal < 30, 0, 1)

    # Graficar los valores
    #plt.figure(figsize=(20, 4))
    #plt.plot(valores, '-o')
    #plt.xlim(0,100)
    #plt.xlabel('Datos')
    #plt.ylabel('Valores')
    #plt.title('Gráfico de valores (0 o 1) en función de los datos')
    #plt.show()

    # Suavizado de la gráfica
    alpha2 = 0.15  # Valor de factor de suavizado (0 < alpha < 1)
    data_pandas = pd.DataFrame(valores)
    valores_continuos = data_pandas.ewm(alpha=alpha2, adjust=False).mean()
    valores_continuos2 = np.where(valores_continuos < 0.1, 0, 1)

    # Graficar los valores
    #plt.figure(figsize=(20, 4))
    #plt.plot(valores_continuos2, '-')
    #plt.xlim(0,100)
    #plt.xlabel('Datos')
    #plt.ylabel('Valores')
    #plt.title('Tiempos de alto uso de CPU')
    #plt.show()

    valores_1 = np.where(valores_continuos2 == 1)[0].tolist()

    resultado1 = [num - 20 for num in valores_1 if num - 20 > 0]
    diccionario_prediccion[nombre_instancia] = resultado1


print(diccionario_prediccion)
