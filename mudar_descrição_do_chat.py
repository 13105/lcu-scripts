from lol.Client import *
from random import randint

"""
Muda a descrição do chat.
Permite ultrapassar o limite de caracteres do limite do client.
se não tiver espaço na string ou não tiver caracteres ascii, o texto é escondido.
    
"""


str_msg = ""

for linhas in range(0,40):
    for i in range(0,49):
        str_msg += chr(randint(65,126))

    str_msg +=" "

client = Client()

msg = {
    "statusMessage": str_msg
}
 
 
ret = client.API.PUT("/lol-chat/v1/me",msg)

print(ret)