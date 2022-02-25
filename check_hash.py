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


# Make the Hash Lookup
def busca_hash(ioc):
	url = 'https://de.api.labs.sophos.com/lookup/files/v1/%s' % ioc
	headers = {'Authorization': token_acceso}

	# Make the request
	response = requests.get(url, headers=headers)

	# Get the JSON response in Python DICT
	json_response = response.json()

	try:
		json_response['error']

	except:
		# Test to see if detectionName key exists - if it doesn't it'll mark it unknown
		try:
			json_response['detectionName']
		except KeyError:
			dectectionname = "Unknown"
		else:
			dectectionname = json_response['detectionName']

		# Rep Score and Reputation Interpretation
		repscore = int(json_response['reputationScore'])
		if 0 <= repscore <= 19:
			repclasification = 'Malware'

		elif 20 <= repscore <= 29:
			repclasification = 'PUA (potentially unwanted application)'

		elif 30 <= repscore <= 69:
			repclasification = 'Unknown/Suspicious'

		elif 70<= repscore <= 100:
			repclasification = 'Known good'

	# If there's an error then return values
	else:
		repscore = 'Unknown'
		dectectionname = 'Unknown'
		repclasification = 'Unknown'

	print('IoC= %s' % ioc)
	print('Reputation Score= %s' % repscore)
	print('Detection Name= %s' % dectectionname)
	print('Clasification= %s' % repclasification)



if __name__ == "__main__":
	autorizacion()
	ioc=str(sys.argv[1])
	busca_hash(ioc)
	sys.exit(0)
