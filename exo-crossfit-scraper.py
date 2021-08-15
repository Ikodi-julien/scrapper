#!/usr/bin/python3
#coding:utf-8
# On importe la fonction 'get' (téléchargement) de 'requests' 
# Et la classe 'Selector' (Parsing) de 'scrapy'
from requests import get
from scrapy import Selector
import json
# Lien de la page à scraper
url = "https://entrainement-sportif.fr/crossfit-lexique-entrainement.htm"
response = get(url)
source = None # Le code source de la page 
# print(response.status_code)
if response.status_code == 200 :
    # Si la requete s'est bien passee
    source = response.text
    
if source :
    # Si le code source existe
    selector = Selector(text=source)
    # On récup tous les titres, pas de piège ici
    titles = selector.css("body > article > dl > dt *::text").getall()
    # Les 4 premiers titres me sont inutils
    del titles[:3]
    # Les descriptions ont des balises à l'intérieur, ce qui créé des "bouts" de string avec getall(), du coup à chaque balise dd je reconstitue une string complète    
    descriptionList = []
    for node in selector.css("body > article > dl > dd") :
        descriptionList.append(' '.join(node.css("*::text").getall()))
    # Les 4 premières descriptions sont inutiles
    del descriptionList[:3]
    # La 11ème est coupée en deux, je la vire
    del descriptionList[11]
    # Fabrication d'un objet json avec les données
    dataList = []
    for index in range(len(titles)) :
        dataObject = {}
        dataObject["titre_" + str(index)] = titles[index]
        dataObject["description_" + str(index)] = descriptionList[index]
        dataList.append(dataObject)
    
    with open('exercices.json', 'w') as exercices :
        dataJson = json.dump(dataList, exercices,  ensure_ascii=0, indent=4, sort_keys=0)
    # print('dataJson: ', dataJson)