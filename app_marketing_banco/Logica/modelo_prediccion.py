import os

import pandas as pd
import numpy as np
import pickle
import keras


# Clase para cargar el modelo de prediccion de Red Neuronal y de Naive Bayes
# Se carga el pipeline que contiene los tranformadores y el modelo
# Esta clase tiene un metodo que devuelve el resultado de la preddicion  como una lista


class ModeloPrediccion:
    _modelo_red_neuronal = None
    _modelo_naive_bayes = None

    @staticmethod
    def cargar_pipeline(nombre_archivo):
        with open(nombre_archivo, 'rb') as handle:
            pipeline = pickle.load(handle)
        return pipeline

    @staticmethod
    def cargar_red_neuronal(nombre_archivo):
        model = keras.models.load_model(nombre_archivo)
        return model

    @staticmethod
    def cargar_naive_bayes(nombre_archivo):
        with open(nombre_archivo, 'rb') as file:
            modelo_cargado = pickle.load(file)
        return modelo_cargado

    # carga el pipeline y la red neuronal y agrega la red al pipeline para luego hacer la prediccion

    @staticmethod
    def cargar_modelo_prediccion(modelo):

        archivo_modelo = None

        if modelo == "red_neuronal":
            # verifica si el modelo ya esta cargado en la variable _modelo_red_neuronal
            if ModeloPrediccion._modelo_red_neuronal is not None:
                print("Modelo ya esta cargado")
                return ModeloPrediccion._modelo_red_neuronal

            archivo_modelo = 'model_NN_bank_data.h5'

        if modelo == "naive_bayes":
            # verifica si el modelo ya esta cargado en la variable _modelo_naive_bayes
            if ModeloPrediccion._modelo_naive_bayes is not None:
                print("Modelo ya esta cargado")
                return ModeloPrediccion._modelo_naive_bayes

            archivo_modelo = 'model_NB_bank_data.pickle'

        print(f"Cargando modelo: {modelo},  archivo : {archivo_modelo}")

        try:
            # obtener la ruta absoluta del proyecto
            directorio_actual = os.path.abspath(os.path.dirname(__file__))

            # Carga del pipeline
            # construir el path del archivo
            archivo_pipeline = os.path.join(directorio_actual, 'Recursos', 'pipeline_bank_data.pickle')
            pipe = ModeloPrediccion.cargar_pipeline(archivo_pipeline)
            print("pipeline cargado desde archivo")
            cantidad_pasos = len(pipe.steps)
            print(f"Cantidad de pasos: {cantidad_pasos}")
            print(pipe.steps)

            # Carga de modelo

            if modelo == 'red_neuronal':

                modelo_red_neuronal = ModeloPrediccion.cargar_red_neuronal(
                    os.path.join(directorio_actual, 'Recursos', archivo_modelo))
                print("Red neuronal cargada desde archivo")
                # Se agrega la Red Neuronal al pipeline
                pipe.steps.append(["modelNN", modelo_red_neuronal])
                cantidad_pasos = len(pipe.steps)
                print(f"Cantidad de pasos: {cantidad_pasos}")
                print(pipe.steps)
                print("Red Neuronal integrada al pipeline")

                # se guarda el modelo en una variable para cargar una sola vez los archivos pipeline y red neuronal
                ModeloPrediccion._modelo_red_neuronal = pipe

                return ModeloPrediccion._modelo_red_neuronal

            else:
                modelo_naive_bayes = ModeloPrediccion.cargar_naive_bayes(
                    os.path.join(directorio_actual, 'Recursos', archivo_modelo))
                print("Red naive bayes cargada desde archivo")
                # Se agrega naive bayes al pipeline
                pipe.steps.append(["modelNB", modelo_naive_bayes])
                cantidad_pasos = len(pipe.steps)
                print(f"Cantidad de pasos: {cantidad_pasos}")
                print(pipe.steps)
                print("Naive Bayes integrado al pipeline")

                # se guarda el modelo en una variable para cargar una sola vez los archivos pipeline y naive bayes
                ModeloPrediccion._modelo_naive_bayes = pipe

                return ModeloPrediccion._modelo_naive_bayes

        except FileNotFoundError as e:
            print(f"Error archivo no encontrado: {e.filename}")
        except Exception as e:
            print(f"Error inesperado: {e}")
        return None

    @staticmethod
    def obtener_resultados_certezas(prediccion):
        marca = None
        certeza = None
        nuevomax = 1
        nuevomin = 0

        if prediccion < 0.5:
            marca = 'No Acepta'
            maxa = 0.5
            mina = 0
            certeza = 1 - ((prediccion - mina) / (maxa - mina) * (nuevomax - nuevomin) + nuevomin)
            certeza = str(int(certeza * 100)) + '%'

        elif prediccion >= 0.5:
            marca = 'Acepta'
            maxa = 1
            mina = 0.5
            certeza = (prediccion - mina) / (maxa - mina) * (nuevomax - nuevomin) + nuevomin
            certeza = str(int(certeza * 100)) + '%'

        return prediccion, marca, certeza

    # Funcion para realizar la prediccion

    @staticmethod
    def predecir_cliente(modelo='red_neuronal', age=40, job='management', marital='married',
                         education='tertiary',
                         balance=5000, housing=0, loan=0, contact='cellular', duration='60', campaign=1):
        column_names = ['age', 'job', 'marital', 'education',
                        'balance', 'housing', 'loan', 'contact', 'duration', 'campaign']
        x_new = [age, job, marital, education, balance, housing, loan, contact, duration, campaign]
        x_new_dataframe = pd.DataFrame(data=[x_new], columns=column_names)
        print("Datos de entrada:")
        print(x_new_dataframe)
        pipe = ModeloPrediccion.cargar_modelo_prediccion(modelo)
        print(f"Modelo de prediccion {modelo} cargado")
        y_pred = pipe.predict(x_new_dataframe)
        print(f"Prediccion realizada {modelo}")
        prediccion, marca, certeza = ModeloPrediccion.obtener_resultados_certezas(y_pred)
        dataframe_final = pd.DataFrame({'Predicción': [prediccion], 'Resultado': [marca], 'Certeza': [certeza]})
        np.set_printoptions(formatter={'float': lambda x: "{0:0.0f}".format(x)})
        print(dataframe_final.head())
        # retorna una lista con: Prediccion ( 0 ~ 1), Resultado( Acepta, No acepta) , Certeza (%)
        lista_resultados = dataframe_final.iloc[0].tolist()
        return lista_resultados
