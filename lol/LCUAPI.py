import urllib.request as ureq
import urllib.parse, json, ssl, base64



    
class LeagueClientAPI:
    
    #retorna dados em bytes (raw data)
    def GET_raw(self, endpoint):
        req = ureq.Request(

            (self.url + endpoint),    
            headers=self.raw_data_http_headers,
            method="GET"
            
        )
        
        
        try:
            resposta = ureq.urlopen(req, context=self.contexto_ssl)
             
        except urllib.error.HTTPError as http_err:
            if http_err.code == 400:
                print(http_err.read().decode())
                
                
        else:
            print(resposta.read())
        
    
    #efetua request e retorna um dicionario
    def efetuar_req(self, req):
        
        try:
        
            resposta = ureq.urlopen(req, context=self.contexto_ssl)
            body = resposta.read()
            if body:
                
                return json.loads(body)
                
            else: 
                return
                
        except urllib.error.HTTPError as http_err:
            #print("Erro",http_err.getcode(),"\n->",http_err.read().decode())
            return
        
            
    
    
        
    def PUT(self, endpoint, dict_corpo):
        
        
        req = ureq.Request(

            (self.url + endpoint),    
            headers=self.default_http_headers,
            method="PUT",
            
            data=json.dumps(dict_corpo).encode("utf-8")
            
        )
        
        
        return self.efetuar_req(req)
        
    def PUT_RAW(self, endpoint, arg):
        
        
        req = ureq.Request(

            (self.url + endpoint),    
            headers=self.default_http_headers,
            method="PUT",
            
            data=arg
            
        )
        
        
        return self.efetuar_req(req)    
        
    #requisição delete pode ou não ter corpo
    def DELETE(self, endpoint, dict_corpo=""):
        return
    
    def POST(self, endpoint, dict_corpo={}):
        
        
        
        req = ureq.Request(

            (self.url + endpoint),    
            headers=self.default_http_headers,
            method="POST",
            
            data=json.dumps(dict_corpo).encode("utf-8")
            
        )
        
        
        return self.efetuar_req(req)
    
    def GET(self, endpoint):
        req = ureq.Request(

            (self.url + endpoint),    
            headers=self.default_http_headers,
            method="GET"
            
        )
        
        return self.efetuar_req(req)
        
    def PATCH(self, endpoint, dict_corpo):
        req = ureq.Request(

            (self.url + endpoint),    
            headers=self.default_http_headers,
            method="PATCH",
            data=json.dumps(dict_corpo).encode("utf-8")
        )
        
        return self.efetuar_req(req)    
    
    def __init__(self, porta, usuario, senha, certificado_dir):
    
        self.url = "https://127.0.0.1:" + porta
        
        #carrega certificado da riot
        self.contexto_ssl = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.contexto_ssl.load_verify_locations(certificado_dir)
        
        
        #configurações do opener
        usuario_senha = (usuario +":"+ senha).encode('ascii')
        
        #string de autorização basica http (Authorization)
        auth_str = "Basic " + base64.b64encode(usuario_senha).decode('ascii')
        
        
        #http headers serão os mesmos em todo metodo de requisição
        
        self.default_http_headers = {
                "Authorization": auth_str,
                "User-Agent":"curl/7.79.1",
                "Accept":"application/json",
                "Content-Type":"application/json"
            }
            
        
        self.raw_data_http_headers = {
                "Authorization": auth_str,
                "User-Agent":"curl/7.79.1",
                "Accept":"*/*"

            }
        

        #TODO:: VERBOSE
        #Verbose 3: retorna código de saida http, código de status e código de debugging
        #Verbose 2: retorna código saida http e código de status
        #Verbose 1: retorna apenas a saida http, não retorna código de status
        #Verbose 0: cala a boca do programa, não retorna nem código de status e nem saida http
        #self.verbose = 1
            
            
        
        
        
        

#formato do corpo:
    # dicionário -> json_str -> bytes(utf-8 str)
    

#x = LeagueClientAPI("63454","riot","senhasenhasenhasenha");




#corpo = {
 #       "statusMessage": "teset"
 #   }
   


#ret = x.GET("/lol-perks/v1/perks")
#print(ret)
