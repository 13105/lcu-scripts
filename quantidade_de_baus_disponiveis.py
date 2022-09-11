from lol.Client import *
import datetime

client = Client()

 
baus = client.API.GET("/lol-collections/v1/inventories/chest-eligibility")
print("Baús disponiveis: ",baus["earnableChests"])

tempo = datetime.datetime.fromtimestamp(int(baus["nextChestRechargeTime"])/1000).strftime("%d/%m/%Y às %H:%M:%S")

print("Reseta em: ", tempo)