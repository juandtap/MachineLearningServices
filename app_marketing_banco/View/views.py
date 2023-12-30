from django.shortcuts import render


def nueva_prediccion(request):
    return render(request, 'formulario_info_cliente.html')
