import sys

sys.path.append(".")
from django.shortcuts import render
from app_credito_banco.Logica.ModeloSNN import ModeloSNN  # para utilizar el método inteligente
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import json
from django.http import JsonResponse


class Clasificacion():
    def determinarAprobacion(request):
        return render(request, "aprobacioncreditos.html")

    @api_view(['GET', 'POST'])
    def predecir(request):
        try:
            # Formato de datos de entrada
            print("Entro al request")
            PLAZOMESESCREDITO = int(request.POST.get('PLAZOMESESCREDITO'))
            MONTOCREDITO = float(request.POST.get('MONTOCREDITO'))
            TASAPAGO = float(request.POST.get('TASAPAGO'))
            EDAD = int('' + request.POST.get('EDAD'))
            CANTIDADPERSONASAMANTENER = int('' + request.POST.get('CANTIDADPERSONASAMANTENER'))
            EMPLEO = request.POST.get('EMPLEO')
            # Consumo de la lógica para predecir si se aprueba o no el crédito
            modelo = ModeloSNN()
            print("creo la clase modeloSNN")
            resul = modelo.predecirNuevoCliente(PLAZOMESESCREDITO=PLAZOMESESCREDITO,
                                                MONTOCREDITO=MONTOCREDITO, TASAPAGO=TASAPAGO, EDAD=EDAD,
                                                CANTIDADPERSONASAMANTENER=CANTIDADPERSONASAMANTENER, EMPLEO=EMPLEO)
        except:
            resul = 'Datos inválidos'
        return render(request, "informe.html", {"e": resul})

    @csrf_exempt
    @api_view(['GET', 'POST'])
    def predecirIOJson(request):
        print(request)
        print('***********************************************')
        print(request.body)
        print('***********************************************')
        body = json.loads(request.body.decode('utf-8'))
        # Formato de datos de entrada
        PLAZOS = int(body.get("PLAZOMESESCREDITO"))
        MONTOCREDITO = float(body.get("MONTOCREDITO"))
        TASAPAGO = float(body.get("TASAPAGO"))
        EDAD = int(body.get("EDAD"))
        CANTIDADPERSONASAMANTENER = int(body.get("CANTIDADPERSONASAMANTENER"))
        EMPLEO = str(body.get("EMPLEO"))
        print(PLAZOS)
        print(MONTOCREDITO)
        print(TASAPAGO)
        print(EDAD)
        print(CANTIDADPERSONASAMANTENER)
        print(EMPLEO)
        modelo = ModeloSNN()
        resul = modelo.predecirNuevoCliente(ModeloSNN, PLAZOMESESCREDITO=PLAZOS, MONTOCREDITO=MONTOCREDITO,
                                            TASAPAGO=TASAPAGO, EDAD=EDAD,
                                            CANTIDADPERSONASAMANTENER=CANTIDADPERSONASAMANTENER, EMPLEO=EMPLEO)
        data = {'result': resul}
        resp = JsonResponse(data)
        resp['Access-Control-Allow-Origin'] = '*'
        return resp
