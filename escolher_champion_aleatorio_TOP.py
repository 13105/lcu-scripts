from lol.Client import *
from time import sleep
from random import randint


#FLAG PARA COLOCAR APENAS CAMPEÕES COM BAU DISPONIVEL
BAU_ONLY = True




def get_banimentos(arrs_actions):
    return (a["championId"] for a in arrs_actions[0] if a["type"] == "ban" and a["completed"])
    

def get_my_action(minha_celula, arrs_actions):
    #formato do conteudo da array 'actions' na soloq (jogadores não são organizados de acordo com o id da celula):
    #[
        #[ [<banimento_jogador_1>], [<banimento_jogador_2>] ...  [<banimento_jogador_10>] ],
        #[ <revelação do banimento de todos os 10 jogadores> ],
        
        # O servidor escolhe a ordem dos picks. Exemplo:
        #[ <PICK_DO_JOGADOR(TIME)>,         <PICK_DO_JOGADOR(ADVERSARIO) ]
        #[ <PICK_DO_JOGADOR(TIME)>,         <PICK_DO_JOGADOR(ADVERSARIO) ]
        #[ <PICK_DO_JOGADOR(TIME)>          <PICK_DO_JOGADOR(ADVERSARIO)                                ]
        #[ <PICK_DO_JOGADOR(ADVERSARIO),    <PICK_DO_JOGADOR(TIME)> ]
        ##[ <PICK_DO_JOGADOR(TIME)>,        <PICK_DO_JOGADOR(ADVERSARIO) ] ]
    #]


    for action_set in arrs_actions:
        

        if len(action_set) > 1:
            
            for action in action_set:
                
                
                if action["actorCellId"] != minha_celula or action["type"] != "pick":
                    continue
                
                #minha celula identificada !
                #escolherei ao mesmo tempo que outro jogador
                return action
        else:
            
            if action_set[0]["actorCellId"] != minha_celula or action_set[0]["type"] != "pick":
                continue
                
            #minha celula identificada !
            # escolherei solo
            return action_set[0]
                
                
client = Client()
sessao = client.API.GET("/lol-champ-select/v1/session")

if not sessao:
    exit("Erro: Você não está na tela de seleção.")
    
minha_celula = sessao["localPlayerCellId"]
my_action = get_my_action(minha_celula, sessao["actions"])

#TODO:: Estou na tela de banimentos ?
# na tela de banimentos pelo menos um estado de ban está em progresso.
# se na tela de banimentos, não fica passando por cima dos bonecos.




if not my_action:
    exit("Erro: Action de pick não encontrada. (O gamemode é Summoners Rift soloQ ?)")



#lista de champions
all_champions = client.API.GET("/lol-champ-select/v1/all-grid-champions")

all_champions_owned = [x["id"] for x in all_champions if x["owned"]]
all_champions_max_id = len(all_champions_owned)-1

if not my_action["isInProgress"]:
    #exit("Erro: Não é a sua vez de escolher o campeão.")
    
    #não é a minha vez de pegar,
    #então fica mostrando retrato de todos os campeoes que eu tenho mt rapido até ser a minha vez
    # esse é o bingo da derrota kkk
    
    i=10
    while True:

        my_action["championId"] = all_champions_owned [randint(0,all_champions_max_id)]
        
        client.API.PATCH(f"/lol-champ-select/v1/session/actions/{my_action['id']}", my_action)
        
        #blocking simples pra não dar pau na requisição
        sleep(0.2)
        if not i:
        
            #verifica se é a minha vez de escolher
            my_action = get_my_action(minha_celula, client.API.GET("/lol-champ-select/v1/session")["actions"])
            
            if not my_action["isInProgress"]:
                # ainda não é minha vez de escolher
                #renova loop
                i = 10
                
                
            else:
                # é a minha vez de escolher !
                # para de zoar com os retratos e procede com a escolha
                break
        else:    
            i-=1
        


#lista de champions filtrada por role ou tipo
champion_pool = []
champions_banidos = get_banimentos(sessao["actions"])

# Monta pool de champions elegiveis para pick
if (all_champions):
    
    
    for champion in all_champions:
        
        if (
            champion["disabled"] or
            not champion["owned"] or
            champion["id"] in champions_banidos or
            champion["selectionStatus"]["pickedByOtherOrBanned"]
        ):
            print(champion["name"])
            continue
        
        if BAU_ONLY:
            if (champion["masteryChestGranted"]):
                continue
                
                
        if ('fighter' in champion["roles"] or 'tank' in champion["roles"]):
            champion_pool.append((champion["name"],champion["id"]))


# picka um boneco aleatorio
champion_nome, champion_id = champion_pool[randint(0,len(champion_pool))]

print(f"\nProbabilidade de escolher cada campeão aleatoriamente na pool atual: {1/len(champion_pool):.2%}\nLockando {champion_nome} ...")
#{
#  "actorCellId": 0,
#  "championId": 0,
#  "completed": true,
#  "id": 0,
#  "isAllyAction": true,
#  "type": "pick"
#}

#edita minha action
my_action["championId"] = champion_id
my_action["completed"] = True

#confirma escolha

client.API.PATCH(f"/lol-champ-select/v1/session/actions/{my_action['id']}", my_action)
#testa se o boneco foi lockado
 
my_action_atualizada = get_my_action(minha_celula, client.API.GET("/lol-champ-select/v1/session")["actions"])
if my_action_atualizada["completed"]:
    exit(f"Campeão lockado com sucesso !")
    
else:
    exit("Erro: Não foi possivel lockar o campeão. (O campeão já foi lockado ?)")
