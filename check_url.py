#!/usr/bin/python3

# requests for web call to REST API
import requests
# System for CLI Args
import sys
# OS for File Validation
import os
# CSV for exporting to CSV
import csv
# Import Time
import time
# Import URLParse library to validate URLS in IOCS
from string import Template

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth

import json
import urllib.parse
from urllib.parse import urlparse


# client_id.txt y client_secret.txt deben estar en el mismo directorio que el fichero python a ejecutar
# client_id.txt y client_secret.txt permiten realizar la autenticacion OAUTH2
# obteniendose el Token temporal de Autenticacion que se inyecta en la cabecera


def autorizacion():

	file_client_id = open("client_id.txt", "r")
	client_id = file_client_id.read().rstrip()

	file_client_secret = open("client_secret.txt", "r")
	client_secret = file_client_secret.read().rstrip()

	token_url = 'https://api.labs.sophos.com/oauth2/token'

	auth = HTTPBasicAuth(client_id, client_secret)
	client = BackendApplicationClient(client_id=client_id)
	oauth = OAuth2Session(client=client)
	auth_code = oauth.fetch_token(token_url=token_url, auth=auth)

	respuesta_json = json.loads(json.dumps(auth_code))
	global token_acceso
	token_acceso=respuesta_json["access_token"]

def busca_url(ioc):

    url_codificada = urllib.parse.quote_plus(ioc)
    url = 'https://de.api.labs.sophos.com/lookup/urls/v1/%s' % url_codificada
    headers = {'Authorization': token_acceso}

    # Make the request
    response = requests.get(url, headers=headers)

    json_response = response.json()

    try:
        json_response['error']
    except KeyError:
        try:
            json_response['productivityCategory']
        except KeyError:
            prodcategory = 'Unknown'
        else:
            prodcategory = json_response['productivityCategory']
            #Check to see if Security Category Exists
         
        try:
            #print('tercer try')
            json_response['securityCategory']
        
        except KeyError:
             securitycategory = 'Unknown'
        else:
             securitycategory = json_response['securityCategory']

        try:
            json_response['riskLevel']
        except KeyError:
            risklevel = 'Unknown'
        else:
            risklevel = json_response['riskLevel']
    else:
        prodcategory = 'Unknown'
        securitycategory = 'Unknown'
        risklevel = 'Unknown'

    print('URL= %s' % ioc)
    print('Prod Category= %s' % prodcategory)
    print('Security Category= %s' % securitycategory)
    print('Risk Level= %s' % risklevel)



if __name__ == "__main__":
	autorizacion()
	ioc=str(sys.argv[1])
	busca_url(ioc)
	sys.exit(0)
