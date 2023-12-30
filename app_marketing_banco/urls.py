from django.urls import path
from app_marketing_banco.View import views

urlpatterns = [
    path('nuevaprediccion/', views.nueva_prediccion, name='nueva_prediccion'),
]
