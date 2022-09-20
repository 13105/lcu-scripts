from lol.Client import *
import datetime
import json

client = Client()

summonerId = client.API.GET("/lol-summoner/v1/current-summoner")["summonerId"]


lista_champs = client.API.GET(f"/lol-collections/v1/inventories/{summonerId}/champion-mastery")
lista_champs_possuidos = client.API.GET("/lol-champions/v1/owned-champions-minimal")

lista_id_nome = [ (x["id"],x["name"]) for x in lista_champs_possuidos ]



for champ in lista_champs:
    
    if not champ["chestGranted"]:
        for j in lista_id_nome:
            
            if champ["championId"] == j[0]:
                print(j[1])
                break
        

