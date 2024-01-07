from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string

from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration


def export_pdf(request):
    print("entra a la funcion para exportar pdf")
    resultados = request.session.get('resultados_prediccion', [])

    context = {'datos': resultados}

    html = render_to_string("reporte-pdf.html", context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; "report.pdf"'

    font_config = FontConfiguration()
    HTML(string=html).write_pdf(response, font_config=font_config)

    return response
