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



def analisis_estatico(ioc):

	url = 'https://de.api.labs.sophos.com/analysis/file/static/v1'
	headers = {'Authorization': token_acceso}

	files = {'file': (ioc, open(ioc, 'rb'), 'application/octet-stream')}

	# Make the request
	response = requests.post(url, headers=headers, files=files)

	json_response = response.json()


	try:
		json_response['error']
	except KeyError:
		try:
			json_response['jobStatus']
		except KeyError:
			print('Error')
		else:
			jobID = json_response['jobId']
			print('%s' % jobID)






if __name__ == "__main__":
	autorizacion()
	ioc=str(sys.argv[1])
	analisis_estatico(ioc)
	sys.exit(0)
