from django.shortcuts import render
from .models import   RGraficos
import pymongo
from django.shortcuts import render
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import paho.mqtt.client as mqtt
import json
import threading
from datetime import datetime
import pytz
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests

@csrf_exempt
def retorna_dados(request):
    global ULTIMOS_DADOS

    if request.method == "POST":
        data = json.loads(request.body)

        ULTIMOS_DADOS = {
            "t": data.get("Temperatura"),
            "p": data.get("Pressao"),
            "u": data.get("Umidade"),
            "g": data.get("Gas"),
            "r": data.get("Rpm"),
            "v": data.get("Vento"),
            "a": data.get("Ar"),
            "vl": data.get("Volt"),
            "lz" : data.get("Luz"),
            "c": data.get("Chuva_acumulada")
        }
        ULTIMOS_DADOS_ARMAZENA = {
                    "Temperatura": data.get("Temperatura"),
                    "Pressao": data.get("Pressao"),
                    "Umidade": data.get("Umidade"),
                    "Gas": data.get("Gas"),
                    "Rpm": data.get("Rpm"),
                    "Vento": data.get("Vento"),
                    "Ar": data.get("Ar"),
                    "Volt": data.get("Volt"),
                    "Luz": data.get("Luz"),
                    "Data": data.get("Data"),
                    "Hora": data.get("Hora"),
                    "Chuva_acumulada": data.get("Chuva_acumulada")
        }
        BASE_URL = 'https://gpadsfirebase-default-rtdb.firebaseio.com/sensores/est0001/dados.json?auth=tUqIcUl6tQ9lOLId0HG9tRXlzrF5nMquklNWQD3l'
        response = requests.post(BASE_URL, data=json.dumps(ULTIMOS_DADOS_ARMAZENA))
        print("POST response:", response.json())
        return JsonResponse({"status": "ok"})
def get_dados(request):
    return JsonResponse(ULTIMOS_DADOS)

@csrf_exempt
def retorna_dados_dois(request):
    global ULTIMOS_DADOS_DOIS

    if request.method == "POST":
        data = json.loads(request.body)

        ULTIMOS_DADOS_DOIS = {
            "t": data.get("Temperatura"),
            "p": data.get("Pressao"),
            "u": data.get("Umidade"),
            "g": data.get("Gas"),
            "r": data.get("Rpm"),
            "v": data.get("Vento"),
            "a": data.get("Ar"),
            "vl": data.get("Volt"),
            "lz" : data.get("Luz"),
            "c": data.get("Chuva_acumulada")
        }
        ULTIMOS_DADOS_DOIS_ARMAZENA = {
            "Temperatura": data.get("Temperatura"),
            "Pressao": data.get("Pressao"),
            "Umidade": data.get("Umidade"),
            "Gas": data.get("Gas"),
            "Rpm": data.get("Rpm"),
            "Vento": data.get("Vento"),
            "Ar": data.get("Ar"),
            "Volt": data.get("Volt"),
            "Luz": data.get("Luz"),
            "Data": data.get("Data"),
            "Hora": data.get("Hora"),
            "Chuva_acumulada": data.get("Chuva_acumulada")
        }
        BASE_URL = 'https://gpadsfirebase-default-rtdb.firebaseio.com/sensores/est0002/dados.json?auth=tUqIcUl6tQ9lOLId0HG9tRXlzrF5nMquklNWQD3l'
        response = requests.post(BASE_URL, data=json.dumps(ULTIMOS_DADOS_DOIS_ARMAZENA))
        print("POST response:", response.json())
        return JsonResponse({"status": "ok"})
def get_dados_dois(request):
    return JsonResponse(ULTIMOS_DADOS_DOIS)

@csrf_exempt
def retorna_dados_tres(request):
    global ULTIMOS_DADOS_TRES

    if request.method == "POST":
        data = json.loads(request.body)

        ULTIMOS_DADOS_TRES = {
            "t": data.get("Temperatura"),
            "p": data.get("Pressao"),
            "u": data.get("Umidade"),
            "g": data.get("Gas"),
            "r": data.get("Rpm"),
            "v": data.get("Vento"),
            "a": data.get("Ar"),
            "vl": data.get("Volt"),
            "lz" : data.get("Luz"),
            "c": data.get("Chuva_acumulada")
        }
        ULTIMOS_DADOS_TRES_ARMAZENA = {
            "Temperatura": data.get("Temperatura"),
            "Pressao": data.get("Pressao"),
            "Umidade": data.get("Umidade"),
            "Gas": data.get("Gas"),
            "Rpm": data.get("Rpm"),
            "Vento": data.get("Vento"),
            "Ar": data.get("Ar"),
            "Volt": data.get("Volt"),
            "Luz": data.get("Luz"),
            "Data": data.get("Data"),
            "Hora": data.get("Hora"),
            "Chuva_acumulada": data.get("Chuva_acumulada")
        }
        BASE_URL = 'https://gpadsfirebase-default-rtdb.firebaseio.com/sensores/est0003/dados.json?auth=tUqIcUl6tQ9lOLId0HG9tRXlzrF5nMquklNWQD3l'
        response = requests.post(BASE_URL, data=json.dumps(ULTIMOS_DADOS_TRES_ARMAZENA))
        print("POST response:", response.json())
        return JsonResponse({"status": "ok"})
def get_dados_tres(request):
    return JsonResponse(ULTIMOS_DADOS_TRES)

def get_dados_armazenados(request):
    DADOS_ARMAZENADOS = {
                                "datas": "Dados não encontrados"
                        }
    allData = []
    saveIndex = []
    allIndex = 0
    data = request.GET.get('estname')
    print("Data recebida: ", data)     
    if str(data).startswith("est") == True:
        BASE_URL = f"https://gpadsfirebase-default-rtdb.firebaseio.com/sensores/{data}/dados.json?auth=tUqIcUl6tQ9lOLId0HG9tRXlzrF5nMquklNWQD3l"
    elif str(data).startswith("boia") == True:
        BASE_URL = f"https://gpadsfirebase-default-rtdb.firebaseio.com/boias/{data}/dados.json?auth=tUqIcUl6tQ9lOLId0HG9tRXlzrF5nMquklNWQD3l"       
    #BASE_URL = f'https://gpadsfirebase-default-rtdb.firebaseio.com/sensores/{data}/dados.json?auth=tUqIcUl6tQ9lOLId0HG9tRXlzrF5nMquklNWQD3l'
    resposta = requests.get(BASE_URL)
    try:
                          resposta = requests.get(BASE_URL)
                          dados = resposta.json()
    except:
                          dados = None
                          print("Dados recebidos: ", dados)
    if not dados:
                        DADOS_ARMAZENADOS = {
                                "datas": "Dados não encontrados"
                        }
                        print("Dados não encontrados")
    else: 
                    datas_unicas = set()
                    
                    for chave, valor in dados.items():
                    
                        if isinstance(valor, dict) and "Data" in valor:
                                datas_unicas.add(str(valor["Data"]))
                    for data in sorted(datas_unicas):
                    
                            allIndex += 1
                            allData.append(data)
                            saveIndex.append(allIndex)
                    DADOS_ARMAZENADOS = {
                        "datas": allData
                    }
    
    return JsonResponse(DADOS_ARMAZENADOS)
def cria_grafico(x, y, cor):
    plt.figure(figsize=(5,3))
    plt.plot(x, y, color=cor)
    plt.ylim((min(y)-2, max(y)+2))
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    return img


import requests
from django.shortcuts import render


def home(request):

    url = "https://gpadsfirebase-default-rtdb.firebaseio.com/sensores/est0001/dados.json?auth=tUqIcUl6tQ9lOLId0HG9tRXlzrF5nMquklNWQD3l"

    try:
        resposta = requests.get(url)
        dados = resposta.json()
    except:
        dados = None

    allData = []
    saveIndex = []
    allIndex = 0

    if not dados:

        AsDatas = {
            'Data': "Dados não encontrados",
            'DataDois': "Dados não encontrados",
            'Index': "",
            'IndexDois': ""
        }

        return render(request, 'estacao/home.html', AsDatas)

    # Equivalente ao distinct("Data")
    datas_unicas = set()

    for chave, valor in dados.items():

        if isinstance(valor, dict) and "Data" in valor:
            datas_unicas.add(str(valor["Data"]))

    # Ordena as datas (opcional)
    for data in sorted(datas_unicas):

        allIndex += 1
        allData.append(data)
        saveIndex.append(allIndex)

    AsDatas = {
        'Data': allData,
        'DataDois': "Dados não encontrados",
        'Index': saveIndex,
        'IndexDois': ""
    }

    return render(request, 'estacao/home.html', AsDatas)
# Create your views here.

def retornaGraficos(request):

    
    retornaBoia = False
    retornaEstacao = False
    ExibeGrafico = RGraficos()
    ExibeGrafico.datae = request.GET.get('datadados')
    ExibeGrafico.estname = str(request.GET.get('estdados')).replace("-", "").lower()
    datacompleta = ExibeGrafico.datae
    print("Data recebida: ", datacompleta)
    print("Estação recebida: ", ExibeGrafico.estname) 
    if str(ExibeGrafico.estname).startswith("est") == True:
        retornaEstacao = True
        retornaBoia = False
        url = f"https://gpadsfirebase-default-rtdb.firebaseio.com/sensores/{ExibeGrafico.estname}/dados.json?auth=tUqIcUl6tQ9lOLId0HG9tRXlzrF5nMquklNWQD3l"
    elif str(ExibeGrafico.estname).startswith("boia") == True:
        retornaBoia = True
        retornaEstacao = False
        url = f"https://gpadsfirebase-default-rtdb.firebaseio.com/boias/{ExibeGrafico.estname}/dados.json?auth=tUqIcUl6tQ9lOLId0HG9tRXlzrF5nMquklNWQD3l"
    
    try:
            resposta = requests.get(url)
            dados = resposta.json()
    except:
            dados = None
    
    if not dados and retornaEstacao == True and retornaBoia == False:
            return render(request, 'estacao/DataConfirmadaEst.html', {
                'DataInvalida': True,
                'DataValida': False
            })
    elif not dados and retornaEstacao == False and retornaBoia == True:
            return render(request, 'estacao/DataConfirmadaBoia.html', {
                'DataInvalida': True,
                'DataValida': False
            })
    
    leitura = []

    t = []
    u = []
    p = []
    t, u ,p, gas, q_ar, luz, rpm, v_vento = [], [], [], [], [], [], [], []
    i = 0
    adc , ph, uv, tens, turb = [], [], [], [], []
    encontrou_dados = False
    if retornaEstacao == True and retornaBoia == False:
        for chave, valor in dados.items():

            if not isinstance(valor, dict):
                continue

            if str(valor.get("Data", "")) == datacompleta:

                encontrou_dados = True

                i += 1
                leitura.append(i)

                try:
                

                    t.append(float(valor.get("Temperatura", 0)))
                    u.append(float(valor.get("Umidade", 0)))
                    p.append(float(valor.get("Pressao", 0)))
                    v_vento.append(float(valor.get("Vento", 0)))
                    luz.append(float(valor.get("Luz", 0)))
                    rpm.append(float(valor.get("Rpm", 0)))
                    gas.append(float(valor.get("Gas", 0)))
                    q_ar.append(float(valor.get("Ar", 0)))
                except:
                    pass

        if not encontrou_dados or not t:
            
            return render(request, 'estacao/DataConfirmadaEst.html', {
                            'DataInvalida': True,
                            'DataValida': False
            })
            
        img_t = cria_grafico(leitura, t, 'red')
        img_u = cria_grafico(leitura, u, 'blue')
        img_p = cria_grafico(leitura, p, 'purple')
        img_gas = cria_grafico(leitura, gas, 'grey')
        img_ar = cria_grafico(leitura, q_ar, 'orange')
        img_luz = cria_grafico(leitura, luz, 'yellow')
        img_rpm = cria_grafico(leitura, rpm, 'black')
        img_vv = cria_grafico(leitura, v_vento, 'black')
        context = {

            # Última leitura
            'temperatura': t[-1],
            'umidade': u[-1],
            'pressao': p[-1],
            'qualidade_do_ar': q_ar[-1], 
            'valor_luz': luz[-1], 
            'rpm': rpm[-1],
            'velocidade_do_vento': v_vento[-1],
            # Médias
            'tempMed': "{:.2f}".format(sum(t) / len(t)),
            'umidMed': "{:.2f}".format(sum(u) / len(u)),
            'presMed': "{:.2f}".format(sum(p) / len(p)),
            'velMed':"{:.2f}".format(sum(v_vento) / len(v_vento)),
            'luzMed':"{:.2f}".format(sum(luz) / len(luz)),
            'rpmMed':"{:.2f}".format(sum(rpm) / len(rpm)),
            'gasMed':"{:.2f}".format(sum(gas) / len(gas)),
            'arMed':"{:.2f}".format(sum(q_ar) / len(q_ar)),
            # Máximos
            'tempMax': "{:.2f}".format(max(t)),
            'humMax': "{:.2f}".format(max(u)),
            'presMax': "{:.2f}".format(max(p)),
            'venMax':"{:.2f}".format(max(v_vento)),
            'venMin':"{:.2f}".format(min(v_vento)),
            'luzMax':"{:.2f}".format(max(luz)),
            'luzMin':"{:.2f}".format(min(luz)),
            'rpmMax':"{:.2f}".format(max(rpm)),
            'rpmMin':"{:.2f}".format(min(rpm)),
            'gasMax':"{:.2f}".format(max(gas)),
            'gasMin':"{:.2f}".format(min(gas)),
            'qarMax':"{:.2f}".format(max(q_ar)),
            'qarMin':"{:.2f}".format(min(q_ar)),
            # Mínimos
            'tempMin': "{:.2f}".format(min(t)),
            'humMin': "{:.2f}".format(min(u)),
            'presMin': "{:.2f}".format(min(p)),

            # Gráficos
            'img_t': img_t,
            'img_u': img_u,
            'img_p': img_p,
            'img_gas': img_gas,
            'img_ar': img_ar,
            'img_luz': img_luz,
            'img_rpm': img_rpm,
            'img_vv': img_vv,
            'DataInvalida': False,
            'DataValida': True,
            'datacompleta': datacompleta
        }

        return render(request, 'estacao/DataConfirmadaEst.html', context)
    if retornaEstacao == False and retornaBoia == True:
          for chave, valor in dados.items():
          
                      if not isinstance(valor, dict):
                          continue
          
                      if str(valor.get("Data", "")) == datacompleta:
          
                          encontrou_dados = True
          
                          i += 1
                          leitura.append(i)
          
                          try:
                          
          
                              adc.append(float(valor.get("ADC", 0)))
                              ph.append(float(valor.get("Ph", 0)))
                              uv.append(float(valor.get("Sensor UV(V)", 0)))
                              tens.append(float(valor.get("Tensão(V)", 0)))
                              turb.append(float(valor.get("Turbidez", 0)))
                              
                          except:
                              pass
          
          if not encontrou_dados or not adc:
                       
                        return render(request, 'estacao/DataConfirmadaBoia.html', {
                                        'DataInvalida': True,
                                        'DataValida': False
                        })
                       
          img_adc = cria_grafico(leitura, adc, 'red')
          img_ph = cria_grafico(leitura, ph, 'blue')
          img_uv = cria_grafico(leitura, uv, 'purple')
          img_tensao = cria_grafico(leitura, tens, 'grey')
          img_turbidez = cria_grafico(leitura, turb, 'orange')
                   
          context = {
            
                        # Última leitura
                        'adc': adc[-1],
                        'ph': ph[-1],
                        'uv': uv[-1],
                        'tensao': tens[-1], 
                        'turbidez': turb[-1], 
                        
                        # Médias
                        'adcMed': "{:.2f}".format(sum(adc) / len(adc)),
                        'phMed': "{:.2f}".format(sum(ph) / len(ph)),
                        'uvMed': "{:.2f}".format(sum(uv) / len(uv)),
                        'tensaoMed':"{:.2f}".format(sum(tens) / len(tens)),
                        'turbidezMed':"{:.2f}".format(sum(turb) / len(turb)),
                     
                        # Máximos
                        'adcMax': "{:.2f}".format(max(adc)),
                        'adcMin': "{:.2f}".format(min(adc)),
                        'phMax': "{:.2f}".format(max(ph)),
                        'phMin': "{:.2f}".format(min(ph)),
                        'uvMax': "{:.2f}".format(max(uv)),
                        'uvMin': "{:.2f}".format(min(uv)),
                        'tensaoMax':"{:.2f}".format(max(tens)),
                        'tensaoMin':"{:.2f}".format(min(tens)),
                        'turbidezMax':"{:.2f}".format(max(turb)),
                        'turbidezMin':"{:.2f}".format(min(turb)),
                       
            
                        # Gráficos
                        'img_adc': img_adc,
                        'img_ph': img_ph,
                        'img_uv': img_uv,
                        'img_tensao': img_tensao,
                        'img_turbidez': img_turbidez,
                       
                        'DataInvalida': False,
                        'DataValida': True,
                        'datacompleta': datacompleta
                    }
            
          return render(request, 'estacao/DataConfirmadaBoia.html', context)