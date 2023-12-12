import requests
import json
import time

urljson = 'https://myserver1-in01.onrender.com/download/data.json'
urltxt = 'https://myserver1-in01.onrender.com/download/data.txt'

def getDataJSON(url):
        try:
            response = requests.get(url)
            dataJSON = response.json()
            print(dataJSON['object']['name'])
            return dataJSON['object']['name']
        except json.JSONDecodeError:
            print("Error al decodificar JSON. Reintentando...")

def getDataTXT(url):
        try:
            response = requests.get(url)
            dataTXT = response.text
            print(dataTXT)
            return dataTXT
        except FileNotFoundError:
            print("Archivo no encontrado. Reintentando...")
