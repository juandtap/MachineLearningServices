from django.urls import path
from app_marketing_banco.View import views

urlpatterns = [
    path('nuevaprediccion/', views.nueva_prediccion, name='nueva_prediccion'),
    path('resultados/', views.predecir, name='resultados_prediccion')
]
