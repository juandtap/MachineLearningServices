import os



# Luego, utiliza `ruta_archivo` en lugar de './Recursos/pipePreprocesadores1.2.pickle'

from django.urls import reverse
import pandas as pd
from sklearn.pipeline import Pipeline
from tensorflow.python.keras.models import load_model, model_from_json
from keras import backend as K

import pickle
import keras


class ModeloSNN:
    """Clase modelo Preprocesamiento y SNN"""

    # Función para cargar preprocesador
    def cargarPipeline(self, nombreArchivo):

        with open(nombreArchivo, 'rb') as handle:
            pipeline = pickle.load(handle)
        return pipeline

    # Función para cargar red neuronal
    def cargarNN(self, nombreArchivo):
        model = keras.models.load_model(nombreArchivo)
        print("Red Neuronal Cargada desde Archivo")
        return model

    # Función para integrar el preprocesador y la red neuronal en un Pipeline
    def cargarModelo(self):
        # Se carga el Pipeline de Preprocesamiento
        try:
            # Obtener la ruta absoluta del directorio actual
            directorio_actual = os.path.abspath(os.path.dirname(__file__))
            # Construir la ruta completa al archivo
            nombreArchivoPreprocesador = os.path.join(directorio_actual, 'Recursos', 'pipePreprocesadores1.2.pickle')
            # nombreArchivoPreprocesador = './Recursos/pipePreprocesadores1.2'
            pipe = self.cargarPipeline(nombreArchivoPreprocesador)
            print('Pipeline de Preprocesamiento Cargado')
            cantidadPasos = len(pipe.steps)
            print("Cantidad de pasos: ", cantidadPasos)
            print(pipe.steps)
            # Se carga la Red Neuronal
            modeloOptimizado = self.cargarNN(os.path.join(directorio_actual, 'Recursos', 'modeloRedNeuronalOptimizada.h5'))
            # Se integra la Red Neuronal al final del Pipeline
            pipe.steps.append(['modelNN', modeloOptimizado])
            cantidadPasos = len(pipe.steps)
            print("Cantidad de pasos: ", cantidadPasos)
            print(pipe.steps)
            print('Red Neuronal integrada al Pipeline')
            return pipe
        except FileNotFoundError as e:
            print(f"Error archivo no encontrado: {e.filename}")
        except Exception as e:
            print(f"Error inesperado: {e}")
        return None

    # La siguiente función permite predecir si se aprueba o no un crédito a un nuevo cliente.
    # En la función se define el valor por defecto de las variables, se crea el dataframe con los nuevos valores y
    # los nombres de las variables.
    # El método "predict" ejecuta el Pipeline: los pasos de transformación y la clasificación (mediante la red neuronal).
    # Así se predice si el cliente es bueno (1) o malo (0).
    def predecirNuevoCliente(self, ESTADOCUENTACORRIENTE='A12', PLAZOMESESCREDITO=6, HISTORIALCREDITO='A34',
                             PROPOSITOCREDITO='A43',
                             MONTOCREDITO=1169, SALDOCUENTAAHORROS='A65', TIEMPOACTUALEMPLEO='A75', TASAPAGO=4,
                             ESTADOCIVILYSEXO='A93', GARANTE='A101', TIEMPORESIDENCIAACTUAL=4, ACTIVOS='A121', EDAD=67,
                             VIVIENDA='A152', CANTIDADCREDITOSEXISTENTES=2, EMPLEO='A173', CANTIDADPERSONASAMANTENER=2,
                             TRABAJADOREXTRANJERO='A201'):
        print("EMPIEZA A PREDECIR EL MODELO")
        pipe = self.cargarModelo()
        cnames = ['ESTADOCUENTACORRIENTE', 'PLAZOMESESCREDITO', 'HISTORIALCREDITO', 'PROPOSITOCREDITO', 'MONTOCREDITO',
                  'SALDOCUENTAAHORROS', 'TIEMPOACTUALEMPLEO', 'TASAPAGO', 'ESTADOCIVILYSEXO', 'GARANTE',
                  'TIEMPORESIDENCIAACTUAL',
                  'ACTIVOS', 'EDAD', 'VIVIENDA', 'CANTIDADCREDITOSEXISTENTES', 'EMPLEO', 'CANTIDADPERSONASAMANTENER',
                  'TRABAJADOREXTRANJERO']
        Xnew = [ESTADOCUENTACORRIENTE, PLAZOMESESCREDITO, HISTORIALCREDITO, PROPOSITOCREDITO, MONTOCREDITO,
                SALDOCUENTAAHORROS,
                TIEMPOACTUALEMPLEO, TASAPAGO, ESTADOCIVILYSEXO, GARANTE, TIEMPORESIDENCIAACTUAL, ACTIVOS, EDAD,
                VIVIENDA,
                CANTIDADCREDITOSEXISTENTES, EMPLEO, CANTIDADPERSONASAMANTENER, TRABAJADOREXTRANJERO]
        Xnew_Dataframe = pd.DataFrame(data=[Xnew], columns=cnames)
        print(Xnew_Dataframe)
        pred = (pipe.predict(Xnew_Dataframe) > 0.5).astype("int32")
        print(pred)
        pred = pred.flatten()[0]  # de 2D a 1D
        if pred == 1:
            pred = 'Aprobado. Felicidades =)'
        else:
            pred = 'Negado. Lo sentimos, intenta en otra ocasión'
        return pred
