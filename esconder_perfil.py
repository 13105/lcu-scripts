from lol.Client import *

client = Client()


privacidade_antiga = client.API.GET("/lol-summoner/v1/current-summoner/profile-privacy")
print(privacidade_antiga)

# Muda a privacidade pra privado

private = {'enabledState': True, 'setting': 'PRIVATE'}
privacidade_nova = client.API.PUT("/lol-summoner/v1/current-summoner/profile-privacy",private)
print(privacidade_nova)

