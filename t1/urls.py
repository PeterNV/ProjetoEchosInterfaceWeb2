from django.urls import path
from appt1 import views
urlpatterns = [
    # rota, view responsavel, nome de referencia
    path('',views.home,name='home'),
    path('dados/',views.retorna_dados,name='retorna_dados'),
    path('get_dados/',views.get_dados,name='get_dados'),

    path('dados_dois/',views.retorna_dados_dois,name='retorna_dados_dois'),
    path('get_dados_dois/',views.get_dados_dois,name='get_dados_dois'),

    path('dados_tres/',views.retorna_dados_tres,name='retorna_dados_tres'),
    path('get_dados_tres/',views.get_dados_tres,name='get_dados_tres'),

    path('dados_quatro/',views.retorna_dados_quatro,name='retorna_dados_quatro'),
    path('get_dados_quatro/',views.get_dados_quatro,name='get_dados_quatro'),

    path('dados_cinco/',views.retorna_dados_cinco,name='retorna_dados_cinco'),
    path('get_dados_cinco/',views.get_dados_cinco,name='get_dados_cinco'),
    
    path('dados_seis/',views.retorna_dados_seis,name='retorna_dados_seis'),
    path('get_dados_seis/',views.get_dados_seis,name='get_dados_seis'),

    path('dados_sete/',views.retorna_dados_sete,name='retorna_dados_sete'),
    path('get_dados_sete/',views.get_dados_sete,name='get_dados_sete'),
    #path('dados_armazenados/',views.retorna_dados_armazenados,name='retorna_dados_armazenados'),
    path('get_dados_armazenados/',views.get_dados_armazenados,name='get_dados_armazenados'),

    path('rg/',views.retornaGraficos,name='dados_estacao'),
    
]