from django.shortcuts import render
from rest_framework.decorators import api_view
from app_marketing_banco.Logica.modelo_prediccion import ModeloPrediccion


def nueva_prediccion(request):
    return render(request, 'formulario_info_cliente.html')


@api_view(['GET', 'POST'])
def predecir(request):
    try:
        print("Empieza la predccion")
        # lee los datos del formulario
        age = int(request.POST.get('edad'))

        job = request.POST.get('trabajo')

        marital = request.POST.get('estadocivil')

        education = request.POST.get('educacion')

        balance = float(request.POST.get('saldo'))

        housing = int(request.POST.get('hipoteca'))

        loan = int(request.POST.get('prestamo'))

        contact = request.POST.get('contacto')

        duration = int(request.POST.get('duracion'))

        campaign = request.POST.get('campaign')

        modelo = request.POST.get('modelo')

        print("MODELO SELECCIONADO: ", modelo)

        resultados = ModeloPrediccion.predecir_cliente(modelo=modelo, age=age, job=job, marital=marital,
                                                       education=education, balance=balance, housing=housing,
                                                       loan=loan, contact=contact, duration=duration, campaign=campaign)

    except Exception as e:
        print("Ocurrio un error: ", e)
        resultados = ['ERROR', 'ERROR', 'ERROR']

    return render(request, "resultado_prediccion.html", {'datos': resultados})
