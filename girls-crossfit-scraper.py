#!/usr/bin/python3
#coding:utf-8
# On importe la fonction 'get' (téléchargement) de 'requests' 
# Et la classe 'Selector' (Parsing) de 'scrapy'
from requests import get
from scrapy import Selector
import json
# Lien de la page à scraper
url = "https://www.exerse.fr/wod-girl-crossfit.php"
response = get(url)
source = None # Le code source de la page 
# print(response.status_code)
if response.status_code == 200 :
    # Si la requete s'est bien passee
    source = response.text
    
if source :
    # Si le code source existe
    selector = Selector(text=source)
    # On récup tous les titres des WOD Girls, pas de piège ici
    titles = selector.css("#maincontent > div > div > div > h3 *::text").getall()

    # Ici la liste des reps et le type d'entrainement, suivi des exos:
    girlDetails = selector.css("#maincontent > div > div > div > h3 + ul").getall()
    
    typeList = []
    exoList = []
    for girl in girlDetails :
        selectorDetails = Selector(text=girl)
        
        # reps, rounds et type
        repsDetails = selectorDetails.css("ul > li:nth-child(1) *::text").get()
        typeList.append(repsDetails)
        
        # exercices
        exos = selectorDetails.css("ul > li *::text").getall()
        exos.pop(0)
        exoList.append(exos)
        
    # Description du WOD
    girlDescs = selector.css("#maincontent > div > div > div > ul + p *::text").getall()
    
    # Objectifs
    girlTargets = selector.css("#maincontent > div > div > div > p + ul").getall()
    
    # On tente de récup les objectifs s'il y en a
    # Liste des index avec des objectifs
    indexList = [0, 2, 4, 5, 6, 9, 13, 16, 17, 20, 22, 25, 27, 28, 30, 31, 32, 33, 34, 35, 39]
    targetList = []
    
    for index in range(0, 43):
        if index in indexList:
            
            targetSelector = Selector(text=girlTargets.pop(0))
            targets = targetSelector.css("ul > li *::text").getall()
            targetList.append(targets)
            
        else:
            targetList.append("")
    
    # On fait un json
    girlsList = []
    
    for index in range(len(titles)) :
        dataObject = {}
        dataObject["id"] = index
        dataObject["title"] = titles[index]
        dataObject["type"] = typeList[index]
        dataObject["exercices"] = exoList[index]
        dataObject["desc"] = girlDescs[index]
        dataObject["target"] = targetList[index]
        girlsList.append(dataObject)
    
    with open('girls.json', 'w') as girls :
        dataJson = json.dump(girlsList, girls, ensure_ascii=0, indent=4, sort_keys=0)