from django.shortcuts import render
from rest_framework.decorators import api_view
from app_marketing_banco.Logica.modelo_prediccion import ModeloPrediccion
from reportlab.pdfgen import canvas
from django.http import HttpResponse


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

    # no sirve eliminar
    if request.GET.get('format') == 'pdf':
     
        
        
        print("empieza a generar PDF")
        try:
        # Generar PDF
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'filename="resultados_prediccion.pdf"'
            pdf = canvas.Canvas(response)

            # Agregar contenido al PDF
            pdf.drawString(100, 800, 'Resultados Predicción')
            pdf.drawString(100, 780, f'El cliente {resultados[1]} el Servicio de Depósito a plazo fijo')

            # Dibujar la tabla en el PDF
            y_position = 750
            for resultado in resultados:
                pdf.drawString(100, y_position, str(resultado))
                y_position -= 20

            pdf.save()
            return response
            
        except Exception as ex:
            print("ERROR IMPRMIENDO PDF: ",ex)
    
    
    return render(request, "resultado_prediccion.html", {'datos': resultados})
