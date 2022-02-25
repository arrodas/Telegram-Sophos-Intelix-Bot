#!/usr/bin/python3

import subprocess
import base64
import requests

#import urllib.request
from requests_toolbelt import MultipartEncoder

from flask import Flask, request, json, send_file, send_from_directory

flask = Flask(__name__)

@flask.route("/", methods=['GET', 'POST'])
#app.config["FOTOS"] = "/home/pi/arrodasbot"

def mibot():
    if request.method == 'POST':
        if request.is_json and 'message' in request.json:
            message = request.json['message']
            #print(message)
            if 'text' in message:
                text = message['text']
                minusculas = text.lower()
                direccion = minusculas[0:3]
                resumen = minusculas[0:4]
                dinamico = minusculas[0:8]
                estatico = minusculas[0:8]
                ayuda = minusculas[0:5]
                check_estatico = minusculas[0:14]
                check_dinamico = minusculas[0:14]
                foto = minusculas[0:4]
                if dinamico == 'dinamico':
                    analisis = open("tipo_analisis", "w+" ) 
                    analisis.write('dinamico')
                    analisis.close()
                    return replyMessage('Ahora me tienes que enviar el fichero y te doy un JobID para consultar pasados minutos')
                elif estatico == 'estatico':
                    analisis = open("tipo_analisis", "w+" ) 
                    analisis.write('estatico')
                    analisis.close()
                    return replyMessage('Ahora me tienes que enviar el fichero y te doy un JobID para consultar pasados minutos')
                elif resumen == 'hash':
                    p = subprocess.check_output('./check_hash.py %s' % text[4:], shell=True)
                    return replyMessage(str(p,'utf-8'))
                elif direccion == 'url':
                    p = subprocess.check_output('./check_url.py %s' % text[3:], shell=True)
                    return replyMessage(str(p,'utf-8'))
                elif check_estatico == 'check_estatico':
                    p = subprocess.check_output('./check_job_estatico.py %s' % text[15:], shell=True)
                    return replyMessage(' ' + str(p,'utf-8'))
                elif check_dinamico == 'check_dinamico':
                    p = subprocess.check_output('./check_job_dinamico_html.py %s' % text[15:], shell=True)
                    return enviaFichero()
                elif ayuda == 'help':
                    return replyMessage('Los comandos son: url [URL sin http(s)], hash [SHA256], estatico [binario en siguiente mensaje], dinamico [binario en siguiente mensaje], check_estatico [job_ID], check_dinamico [job_ID] y foto [num_foto]')
                else:
                    return replyMessage('Lo k tu dise no entiendo. ¿me has dicho esto?: ' + message['text'])
            elif 'document' in message:
                file = open("botID.txt", 'r')
                botID = file.read().rstrip()
                file.close()
                p = subprocess.check_output('wget https://api.telegram.org/bot%s/getFile?file_id=%s -O salida_wget.txt' % (botID, message['document']['file_id']), shell=True)
                with open("salida_wget.txt") as json_file:
                    fichero = json.load(json_file)
                p = subprocess.check_output('wget https://api.telegram.org/file/bot%s/%s -O fichero' % (botID, fichero['result']['file_path']), shell=True)
                analisis = open("tipo_analisis", "w+" ) 
                if analisis == 'dinamico':
                    p = subprocess.check_output('./sube_dinamico.py fichero', shell=True)
                    analisis.write('')
                    analisis.close()
                    return replyMessage(str(p,'utf-8'))
                else:
                    p = subprocess.check_output('./sube_estatico.py fichero', shell=True)
                    analisis.write('')
                    analisis.close()
                    return replyMessage(str(p,'utf-8'))
    return ''

def replyJson(data):
    response = flask.make_response(json.dumps(data))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

def replyMessage(text):
    file = open("chatID.txt", 'r')
    chatID = file.read().rstrip()
    file.close()
    return replyJson({
        'method': 'sendMessage',
        'chat_id': chatID,
        'text': text
	})

def enviaFichero():
    file = open("chatID.txt", 'r')
    chatID = file.read().rstrip()
    file.close()
    file = open("botID.txt", 'r')
    botID = file.read().rstrip()
    file.close()
    p = subprocess.check_output('curl -F document=@"AnalisisDinamico.html" https://api.telegram.org/bot%s/sendDocument?chat_id=%s' % (botID, chatID), shell=True) 
    return replyJson({
        'method': 'sendMessage',
        'chat_id': chatID,
        'text': ''
        })


