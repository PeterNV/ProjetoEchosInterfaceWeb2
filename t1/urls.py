from django.urls import path
from appt1 import views
urlpatterns = [
    # rota, view responsavel, nome de referencia
    path('',views.home,name='home'),
    path('rg/',views.retornaGraficos,name='dados_estacao'),
   
]
