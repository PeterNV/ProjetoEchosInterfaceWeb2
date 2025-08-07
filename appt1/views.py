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
import datetime
from datetime import datetime
import pytz

def mqtt_receive():
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("EstacaoMetIFPE")

    def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        data = json.loads(msg.payload)
        temperature = data['Temperatura']
        humidity = data['Umidade']
        pressao = data['Pressao']
        vento = data['Vento']
        volt = data['Volt']
        luz = data['Luz']
        rpm = data['Rpm']
        gas = data['Gas']
        ar = data['Ar']
        thedate1 = data['Data']
        hora1 = data['Hora']
        print("Temperature:", temperature)
        print("Humidity:", humidity)
        print("Pressão:", pressao)
        print("Vento:", vento)
        print("Volt:", volt)
        print("Luz:", luz)
        print("Rpm:", rpm)
        print("Gas:", gas)
        print("Ar:", ar)
        print("Data:", thedate1)
        print("Hora:", hora1)
        myclient = pymongo.MongoClient("mongodb+srv://phpvn:sacul0499@cluster0.u9irlhy.mongodb.net/")
        mydb = myclient["Dados"]
        mycol = mydb["DadosEstacao"]
        #UTC = pytz.utc
        
        IST = pytz.timezone('America/Recife')

        datetime_ist = datetime.now(IST)
             
        thedate = datetime_ist.strftime('%d/%m/%Y')
        thetime = datetime_ist.strftime('%H:%M:%S')
        print(thedate)
        print(thetime)
            
        thedate = str(datetime.date.today().day)+'/'+str(datetime.date.today().month)+'/'+str(datetime.date.today().year)
        thetime = str(datetime.datetime.now().hour)+':'+str(datetime.datetime.now().minute)+':'+str(datetime.datetime.now().second)
        mydict = { "Temperatura": temperature,"Umidade": humidity, "Pressão": pressao, "Vento": vento,
                   "Volt":volt,"Luz":luz,"Rpm":rpm,"Gás":gas,"Ar":ar,"Data":thedate,"Hora": hora}

        x = mycol.insert_one(mydict)
        client = mqtt.Client()
        client.connect("test.mosquitto.org", 1883)

    # Suponha que você tenha dados a serem enviados em um formato similar
        dados = {
            'Temperatura': temperature,
            'Umidade': humidity,
            'Pressao': pressao,
            'Luz': luz,
            'Gas': gas,
            'Rpm': rpm,
            'Vento': vento,
            'Ar': ar,
        }

        client.publish("EstacaoMetIFPED", json.dumps(dados))
        client.disconnect()
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    client.connect("test.mosquitto.org", 1883)
    client.loop_forever()


mqtt_thread = threading.Thread(target=mqtt_receive)
mqtt_thread.daemon = True  # A thread será encerrada quando o programa principal terminar
mqtt_thread.start()

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

def cria_gauge(data, min, max, cor_inicio, cor_meio, cor_fim, unidade):
    go_temp = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = data[-1],
        number = {'suffix': unidade, 'font': {'size': 64, 'color': '#444', 'family': 'sans-serif'}},
        gauge = {
            'axis':{'range': [min, max], 'tickwidth': 1, 'tickcolor': '#000'},
            'bar': {'color': '#444'},
            'borderwidth' : 2,
            'bordercolor': 'black',
            'steps': [
                {'range': [min,min + (max-min)/3], 'color': cor_inicio},
                {'range': [min + (max-min)/3,min + 2*(max-min)/3], 'color': cor_meio},
                {'range': [min + 2*(max-min)/3,max], 'color': cor_fim}
            ]

        }
    ))

    go_temp.update_layout(font=dict(size=36))

    img = go_temp.to_image(format='png')
    img_b64 = "data:image/png;base64," + base64.b64encode(img).decode()
    return img_b64

def home(request):
    myclientt = pymongo.MongoClient("mongodb+srv://phpvn:sacul0499@cluster0.u9irlhy.mongodb.net/")
    mydbt = myclientt["Dados"]
    mycolt = mydbt["DadosEstacao"]
    allData = []
    allIndex = 0
    saveIndex = []
    for y in mycolt.distinct("Data"):
            print(str(y))
            allIndex += 1
            print(allIndex)
            allData.append(str(y))
            saveIndex.append(allIndex)
            AsDatas ={
                
                'Data' : allData,  
                'Index': saveIndex
                
            }
    return render(request,'estacao/home.html',AsDatas)
# Create your views here.

def retornaGraficos(request):
    myclient = pymongo.MongoClient("mongodb+srv://phpvn:sacul0499@cluster0.u9irlhy.mongodb.net/")
    mydb = myclient["Dados"]
    mycol = mydb["DadosEstacao"]
    ExibeGrafico = RGraficos()
    ExibeGrafico.datae = request.GET.get('datadados')
   
    print(ExibeGrafico.datae)
 
    datacompleta = ''
    datacompleta = ExibeGrafico.datae
    print(ExibeGrafico.datae)
  
    i = 0
    leitura = []
    
    t, u, gas, q_ar, luz, rpm, v_vento, p = [], [], [], [], [], [], [], []
    y = mycol.find_one({"Data": datacompleta})
    tmax = []
    tmin = []
    hmax = []
    hmin = []
    pmax = []
    pmin = []
    vmax = []
    vmin = []
    lmax = []
    lmin = []
    rmax = []
    rmin = []
    gmax = []
    gmin = []
    qmax = []
    qmin = []
    tm = 0.0
    hm = 0.0
    pm = 0.0
    vm = 0.0
    lm = 0.0
    rm = 0.0
    gm = 0.0
    qm = 0.0
    for x in mycol.find({"Data": datacompleta}):
        
        i+=1
        leitura.append(i)
        tm += float(x.get("Temperatura"))
        hm += float(x.get("Umidade"))
        pm += float(x.get("Pressão"))
        vm += float(x.get("Vento"))
        lm += float(x.get("Luz"))
        rm += float(x.get("Rpm"))
        gm += float(x.get("Gás"))
        qm += float(x.get("Ar"))

        tmax.append(x.get("Temperatura"))
        tmin.append(x.get("Temperatura"))
        hmax.append(x.get("Umidade"))
        hmin.append(x.get("Umidade"))
        pmax.append(x.get("Pressão"))
        pmin.append(x.get("Pressão"))
        vmax.append(x.get("Vento"))
        vmin.append(x.get("Vento"))
        lmax.append(x.get("Luz"))
        lmin.append(x.get("Luz"))
        rmax.append(x.get("Rpm"))
        rmin.append(x.get("Rpm"))
        gmax.append(x.get("Gás"))
        gmin.append(x.get("Gás"))
        qmax.append(x.get("Ar"))
        qmin.append(x.get("Ar"))

        t.append(float(x.get("Temperatura")))
        u.append(float(x.get("Umidade")))
        p.append(float(x.get("Pressão")))
        v_vento.append(float(x.get("Vento")))
        luz.append(float(x.get("Luz")))
        rpm.append(float(x.get("Rpm")))
        gas.append(float(x.get("Gás")))
        q_ar.append(float(x.get("Ar")))
        print(x)
    print("{:.2f}".format(float(tm/i)))
    print("{:.2f}".format(float(hm/i)))
    print("{:.2f}".format(float(pm/i)))
    print("{:.2f}".format(float(vm/i)))
    print("{:.2f}".format(float(lm/i)))
    print("{:.2f}".format(float(rm/i)))
    print("{:.2f}".format(float(gm/i)))
    print("{:.2f}".format(float(qm/i)))
    print(max(tmax))
    print(min(tmin))
    print(max(hmax))
    print(min(hmin))
    print(max(pmax))
    print(min(pmin))
    print(max(vmax))
    print(min(vmin))
    print(max(lmax))
    print(min(lmin))
    print(max(rmax))
    print(min(rmin))
    print(max(gmax))
    print(min(gmin))
    print(max(qmax))
    print(min(qmin))
    print(y)
    if y == None:
        AsDatas ={
        
         'DataInvalida': True,
         'DataValida': False
        }
        return render(request,'estacao/DataConfirmada.html',AsDatas)
    else:    
           img_t = cria_grafico(leitura, t, 'red')
           img_u = cria_grafico(leitura, u, 'blue')
           img_gas = cria_grafico(leitura, gas, 'grey')
           img_ar = cria_grafico(leitura, q_ar, 'orange')
           img_luz = cria_grafico(leitura, luz, 'yellow')
           img_rpm = cria_grafico(leitura, rpm, 'black')
           img_vv = cria_grafico(leitura, v_vento, 'black')
           img_p = cria_grafico(leitura, p, 'purple')

          

           context = {
              'temperatura': t[-1], 
               'umidade': u[-1], 
               'gas': gas[-1], 
               'qualidade_do_ar': q_ar[-1], 
               'valor_luz': luz[-1], 
               'rpm': rpm[-1],
               'velocidade_do_vento': v_vento[-1],
               'pressao': p[-1],
               'tempMed':"{:.2f}".format(float(tm/i)),
               'umidMed':"{:.2f}".format(float(hm/i)),
               'presMed':"{:.2f}".format(float(pm/i)),
               'velMed':"{:.2f}".format(float(vm/i)),
               'luzMed':"{:.2f}".format(float(lm/i)),
               'rpmMed':"{:.2f}".format(float(rm/i)),
               'gasMed':"{:.2f}".format(float(gm/i)),
               'arMed':"{:.2f}".format(float(qm/i)),
               'tempMax':"{:.2f}".format(float(max(tmax))),
               'tempMin':"{:.2f}".format(float(min(tmin))),
               'humMax':"{:.2f}".format(float(max(hmax))),
               'humMin':"{:.2f}".format(float(min(hmin))),
               'presMax':"{:.2f}".format(float(max(pmax))),
               'presMin':"{:.2f}".format(float(min(pmin))),
               'venMax':"{:.2f}".format(float(max(vmax))),
               'venMin':"{:.2f}".format(float(min(vmin))),
               'luzMax':"{:.2f}".format(float(max(lmax))),
               'luzMin':"{:.2f}".format(float(min(lmin))),
               'rpmMax':"{:.2f}".format(float(max(rmax))),
               'rpmMin':"{:.2f}".format(float(min(rmin))),
               'gasMax':"{:.2f}".format(float(max(gmax))),
               'gasMin':"{:.2f}".format(float(min(gmin))),
               'qarMax':"{:.2f}".format(float(max(qmax))),
               'qarMin':"{:.2f}".format(float(min(qmin))),
               'img_t': img_t,
               'img_u': img_u,
               'img_gas': img_gas,
               'img_ar': img_ar,
               'img_luz': img_luz,
               'img_rpm': img_rpm,
               'img_vv': img_vv,
               'img_p': img_p,
               'DataInvalida': False,
               'DataValida': True,
               'datacompleta': datacompleta,
               
        }
    return render(request,'estacao/DataConfirmada.html',context)

