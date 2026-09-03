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
                    "Hora": data.get("Hora")
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
        BASE_URL = 'https://gpadsfirebase-default-rtdb.firebaseio.com/sensores/est0002/dados.json?auth=tUqIcUl6tQ9lOLId0HG9tRXlzrF5nMquklNWQD3l'
        response = requests.post(BASE_URL, data=json.dumps(ULTIMOS_DADOS_DOIS))
        print("POST response:", response.json())
        return JsonResponse({"status": "ok"})
def get_dados_dois(request):
    return JsonResponse(ULTIMOS_DADOS_DOIS)
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

    url = "https://gpadsfirebase-default-rtdb.firebaseio.com/sensores/est0001/dados.json?auth=tUqIcUl6tQ9lOLId0HG9tRXlzrF5nMquklNWQD3l"

    try:
        resposta = requests.get(url)
        dados = resposta.json()
    except:
        dados = None

    if not dados:
        return render(request, 'estacao/DataConfirmada.html', {
            'DataInvalida': True,
            'DataValida': False
        })

    ExibeGrafico = RGraficos()
    ExibeGrafico.datae = request.GET.get('datadados')

    datacompleta = ExibeGrafico.datae

    leitura = []

    t = []
    u = []
    p = []
    gas, q_ar, luz, rpm, v_vento = [], [], [], [], []
    i = 0

    encontrou_dados = False

    for chave, valor in dados.items():

        if not isinstance(valor, dict):
            continue

        if str(valor.get("Data", "")) == datacompleta:

            encontrou_dados = True

            i += 1
            leitura.append(i)

            try:
                temperatura = float(valor.get("Temperatura", 0))
                umidade = float(valor.get("Umidade", 0))
                pressao = float(valor.get("Pressao", 0))

                t.append(temperatura)
                u.append(umidade)
                p.append(pressao)
                v_vento.append(float(valor.get("Vento", 0)))
                luz.append(float(valor.get("Luz", 0)))
                rpm.append(float(valor.get("Rpm", 0)))
                gas.append(float(valor.get("Gas", 0)))
                q_ar.append(float(valor.get("Ar", 0)))
            except:
                pass

    if not encontrou_dados or len(t) == 0:

        return render(request, 'estacao/DataConfirmada.html', {
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

    return render(request, 'estacao/DataConfirmada.html', context)

def retornaGraficosDois(request):
    myclient = pymongo.MongoClient("mongodb+srv://pedrovilanova34:sacul0499@cluster0.ksgparj.mongodb.net/")
    mydb = myclient["Dados"]
    mycol = mydb["SensorRl"]
    ExibeGrafico = RGraficos()
    ExibeGrafico.datae = request.GET.get('datadadosDois')
    VerificaTempAlta = 0
    RespostaTempAlta = ""
    
    VerificaTempBaixa = 0
    RespostaTempBaixa = ""
    
    
    VerificaUmidAlta = 0
    RespostaUmidAlta = ""
        
    VerificaUmidBaixa = 0
    RespostaUmidBaixa = ""
    RespostaTempAlta = ""
    print(ExibeGrafico.datae)
 
    datacompleta = ''
    datacompleta = ExibeGrafico.datae
    print(ExibeGrafico.datae)
  
    i = 0
    leitura = []
    
    t, u,  p = [], [], []
    y = mycol.find_one({"Data": datacompleta})
    tmax = []
    tmin = []
    hmax = []
    hmin = []
    pmax = []
    pmin = []
    
    tm = 0.0
    hm = 0.0
    pm = 0.0    
    print(y)
    for x in mycol.find({"Data": datacompleta}):
       
        i+=1
        leitura.append(i)
        tm += float(x.get("Temperatura"))
        hm += float(x.get("Umidade"))
        pm += float(x.get("Ponto_de_orvalho"))
        print("Temp med: ",tm)

        tmax.append(x.get("Temperatura"))
        tmin.append(x.get("Temperatura"))
        hmax.append(x.get("Umidade"))
        hmin.append(x.get("Umidade"))
        pmax.append(x.get("Ponto_de_orvalho"))
        pmin.append(x.get("Ponto_de_orvalho"))
        

        t.append(float(x.get("Temperatura")))
        u.append(float(x.get("Umidade")))
        p.append(float(x.get("Ponto_de_orvalho")))
        if float(x.get("Temperatura")) > 27.00 and float(x.get("Temperatura")) < 32.99:
                      VerificaTempAlta += 1
        if float(x.get("Temperatura")) > 15.00 and float(x.get("Temperatura")) < 18.00:
                      VerificaTempBaixa += 1
        if float(x.get("Umidade")) > 55.00 and float(x.get("Umidade")) < 60.99:
                      VerificaUmidAlta += 1
        if float(x.get("Umidade")) > 20.00 and float(x.get("Umidade")) < 40.00:
                      VerificaUmidBaixa += 1
        print(x)
    print("{:.2f}".format(float(tm/i)))
    print("{:.2f}".format(float(hm/i)))
    print("{:.2f}".format(float(pm/i)))

    print(max(tmax))
    print(min(tmin))
    print(max(hmax))
    print(min(hmin))
    print(max(pmax))
    print(min(pmin))
   
    print(y)
    if VerificaTempAlta >= 10:
            RespostaTempAlta = "SIM"
    else:
            RespostaTempAlta = "NÃO"
    
    if VerificaTempBaixa >= 10:
            RespostaTempBaixa = "SIM"
    else:
            RespostaTempBaixa = "NÃO"
    
    if VerificaUmidAlta >= 10:
            RespostaUmidAlta = "SIM"
    else:
            RespostaUmidAlta = "NÃO"
    
    if VerificaUmidBaixa >= 10:
            RespostaUmidBaixa = "SIM"
    else:
            RespostaUmidBaixa = "NÃO"
    if y == None:
        AsDatas ={
        
         'DataInvalida': True,
         'DataValida': False
        }
        return render(request,'estacao/DataConfirmadaDois.html',AsDatas)
    else:    
           img_t = cria_grafico(leitura, t, 'red')
           img_u = cria_grafico(leitura, u, 'blue')

           img_p = cria_grafico(leitura, p, 'purple')

          

           context = {
               'temperatura': t[-1], 
               'umidade': u[-1], 
               
               'pressao': p[-1],
               'tempMed':"{:.2f}".format(sum(t) / len(t)),
               'umidMed':"{:.2f}".format(sum(u) / len(u)),
               'pdoMed':"{:.2f}".format(sum(p) / len(p)),
               
               'tempMax':"{:.2f}".format(max(t)),
               'tempMin':"{:.2f}".format(min(t)),
               'humMax':"{:.2f}".format(max(u)),
               'humMin':"{:.2f}".format(min(u)),
               'pdoMax':"{:.2f}".format(max(p)),
               'pdoMin':"{:.2f}".format(min(p)),
            
               'img_t': img_t,
               'img_u': img_u,
               'img_p': img_p,
               'DataInvalida': False,
               'DataValida': True,
               'datacompleta': datacompleta,
               'RespTempAlta': RespostaTempAlta,
               'RespTempBaixa': RespostaTempBaixa,
               'RespUmidAlta': RespostaUmidAlta,
               'RespUmidBaixa':RespostaUmidBaixa,
               'TotalTempAlta': VerificaTempAlta,
               'TotalTempBaixa': VerificaTempBaixa,
               'TotalUmidAlta': VerificaUmidAlta,
               'TotalUmidBaixa': VerificaUmidBaixa,
        }
    return render(request,'estacao/DataConfirmadaDois.html',context)