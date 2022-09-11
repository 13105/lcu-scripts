from lol.LCUAPI import LeagueClientAPI
import os.path

class Client():
    def get_lockfileData(self, diretorio_raiz_do_lol):

        lockfile_dir = os.path.join(diretorio_raiz_do_lol, "lockfile")

        # lockfile não encontrado => client fechado
        if not os.path.isfile(lockfile_dir): return

        #lockfile encontrado
        arq = open(lockfile_dir, "r")

        # se o lockfile existe, ele nunca está vazio.
        lockfileData = arq.read().split(":")

        #Formato de retorno:
        # [<Nome do processo>, <PID>, <Porta, <Senha>, <Protocolo>] 

        #Exemplo:
        #LeagueClient:12345:54321:password:https
        
        return lockfileData

    def __init__(self, diretorio_raiz_do_lol="C:\Riot Games\League of Legends"):
        
        
        certificado = os.path.join(os.path.dirname(__file__),"riot.pem")
        
        self.pnome, self.pid, self.porta, self.senha, self.protocolo = self.get_lockfileData(diretorio_raiz_do_lol)
        
        self.API = LeagueClientAPI(self.porta,"riot",self.senha,certificado)
        
        # seta mais coisas [...]


