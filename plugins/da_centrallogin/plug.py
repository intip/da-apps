# coding: utf-8
#
# Copyright 2009 Prima Tech Informatica Ltda.
#
# Licensed under the Environ License, Version 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.cmspublica.com.br/licenses/ENVIRON-LICENSE-1.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import urllib
import os
import sys
import re
import types
import datetime
import smtplib
import operator
sys.path.append("{0}/modules/soappy".format(os.path.dirname(__file__)))
sys.path.append("{0}/modules".format(os.path.dirname(__file__)))
sys.path.append("{0}/modules/fpconst".format(os.path.dirname(__file__)))
from suds.client import Client
from SOAPpy import WSDL
from urllib import urlopen
import time as dtime, time
from time import time, strftime, strptime
from xml.etree import ElementTree as ET
from publica.admin.exchange import getDadosSite
from msgs import msg1, msg2, msg3, msg4, msg5, msg6,\
                 msg7, msg8, msg9, msg10, msg11, msg12,\
                 msg13, msg14, msg15
from email.Message import Message
from publica.utils.postal import Email
from email.MIMEText import MIMEText
from publica.core.portal import Portal
from publica.admin.error import UserError
from publica.utils.json import encode
from publica.utils.decorators import serialize, jsoncallback, dbconnectionapp,\
                                     Permission, logportal
from publica.utils.json import encode, decode
from publica import settings
from datetime import datetime as DateTime, \
        timedelta as TimeDelta, datetime as DateTimeType

hasapp = False
haspage = False
haslist = False
hasportlet = False
hascomment = True
title = "DA - Central Login"
meta_type = "da_centrallogin"

COOKIE_NAME = "wdah"
COOKIE_CAPTCHA = "envcat"


class Plug:
    """
    """
    title = title
    meta_type = meta_type
    hasapp = hasapp
    haspage = haspage
    haslist = haslist
    hascomment = hascomment
    central = 1
    __comment_action__ = [
              ["open", "Informa&ccedil;&otilde;es do usu&aacute;rio",
               ["userinfo.env", 500, 300, "true"]],
    ]

    def __init__(self, id_site, id_plugin=None, request=None, dados={}):
        """
        """
        self.id_plugin = id_plugin
        self.id_site = id_site
        self.request = request
        self.dados = dados
        self._proxy = None

        if id_plugin and not dados:
            portal = Portal(id_site=self.id_site,
                            request=self.request)
            self.dados = portal._getDadosPlug(env_site=self.id_site,
                                              id_plugin=self.id_plugin)

    def _install(self, title, wsdl_url, wsdl_origin, id_servico, 
                 session_type, session_schema, func_type, func_schema,
                 from_host, return_path, titulo_mail, smtp_host, smtp_port,
                 provedor):
        """
            Adiciona uma instancia do plugin
        """
        return {"titulo": title,
                "wsdl_url": wsdl_url,
                "wsdl_origin": wsdl_origin,
                "id_servico": id_servico,
                "session_type": session_type,
                "session_schema": session_schema,
                "func_type": func_type,
                "func_schema": func_schema,
                "from_host": from_host,
                "return_path": return_path,
                "titulo_mail":titulo_mail,
                "smtp_host":smtp_host,
                "smtp_port":smtp_port,
                "provedor":provedor}

    @serialize
    @Permission("ADM PLUG")
    def editPlug(self, title, wsdl_url, wsdl_origin, id_servico, session_type, 
                 session_schema, func_type, func_schema, from_host, return_path, titulo_mail,
                 smtp_host, smtp_port, provedor):
        """
            Edita os atributos do plugin
        """
        dados = {"titulo": title,
                "wsdl_url": wsdl_url,
                "wsdl_origin": wsdl_origin,
                "id_servico": id_servico,
                "session_type": session_type,
                "session_schema": session_schema,
                "func_type": func_type,
                "func_schema": func_schema,
                "from_host": from_host,
                "return_path": return_path,
                "titulo_mail":titulo_mail,
                "smtp_host":smtp_host,
                "smtp_port":smtp_port,
                "provedor":provedor}

        portal = Portal(id_site=self.id_site,
                        request=self.request)
        portal._editPlug(env_site=self.id_site,
                         id_plugin=self.id_plugin, 
                         title=title, 
                         dados=dados)
        return "Plugin configurado com sucesso"

    def _getProxy(self, suds=False):
        """
        """
        if suds:
            self._proxy = Client(self.dados["wsdl_url"]).service
        else:
            self._proxy = WSDL.Proxy(self.dados["wsdl_url"])
        return self._proxy

    def _getUserData(self, email):
        """
        <?xml version="1.0" encoding="ISO-8859-1"?>
        <LOGIN>
            <ID></ID>
            <LOGIN></LOGIN>
            <EMAIL></EMAIL>
            <NOME></NOME>
            <APELIDO></APELIDO>
            <SEXO></SEXO>
            <CANCELADO></CANCELADO>
            <DT_EXPIRACAO></DT_EXPIRACAO>
            <DT_NASCIMENTO></DT_NASCIMENTO>
            <CPF_CNPJ></CPF_CNPJ>
            <PESSOA></PESSOA>
            <CONTATO></CONTATO>
            <RG></RG>
            <CTRL_ORIGEM></CTRL_ORIGEM>
            <CTRL_BLOQUPDATE></CTRL_BLOQUPDATE>
            <CTLR_DT_INSERT></CTLR_DT_INSERT>
            <CTRL_DT_ULTIMO_ACESSO></CTRL_DT_ULTIMO_ACESSO>
            <CTRL_DT_ULTIMO_UPDATE></CTRL_DT_ULTIMO_UPDATE>
            <CTLR_CODIGOSGVD></CTLR_CODIGOSGVD>
            <CTRL_ASSINANTEJORNAL></CTRL_ASSINANTEJORNAL>
            <CTRL_ASSINANTECODDISTRIB></CTRL_ASSINANTECODDISTRIB>
            <CTRL_LOGINMASTERID></CTRL_LOGINMASTERID>
            <CTRL_LOGINCORTESIA></CTRL_LOGINCORTESIA>
            <CTRL_LOGINCLASSIFICACAO></CTRL_LOGINCLASSIFICACAO>
            <RESULT>0</RESULT>
        </LOGIN> 
        """
        xml_src = self._getProxy(suds=True).buscaDadosLogin(login=email,
                                                             origem=self.dados["wsdl_origin"])
        tel_src = self._getProxy(suds=True).buscaDadosTelefone(login=email,
                                                               origem=self.dados["wsdl_origin"])
        end_src = self._getProxy(suds=True).buscaDadosEndereco(login=email,
                                                                origem=self.dados["wsdl_origin"])
        tree = ET.fromstring(unicode(xml_src).encode("latin1"))
        if tel_src == "0":
            telefone = ""
        else:
            tree_tel = ET.fromstring(unicode(tel_src).encode("latin1"))
            telefone =[] 
            for tel in tree_tel.findall("ID"):
                tel = {"id":tel.get("num"),
                       "fone":'('+tel.find("DDD").text+') '+tel.find("FONE").text}
                telefone.append(tel)
            telefone.sort(key=operator.itemgetter('id'), reverse=True)
        if end_src == "0":
            endereco = ""
        else:
            tree_end = ET.fromstring(unicode(end_src).encode("latin1"))
            endereco =[]
            for end in tree_end.findall("ID"):
                ende = {"id":end.get("num"),
                        "tipo":end.find("TIPO").text,
                        "rua":self._verifyEncode(end.find("RUA").text),
                        "numero":end.find("NUMERO").text,
                        "complemento":self._verifyEncode(end.find("COMPLEMENTO").text),
                        "bairro":self._verifyEncode(end.find("BAIRRO").text),
                        "cidade":self._verifyEncode(end.find("CIDADE").text),
                        "estado":self._verifyEncode(end.find("ESTADO").text),
                        "cep":end.find("CEP").text,
                        "pais":end.find("PAIS").text}
                endereco.append(ende)
            endereco.sort(key=operator.itemgetter('id'), reverse=True)    
        return {"id":tree.findall("ID")[0].text,
                "nome": tree.findall("NOME")[0].text,
                "email": tree.findall("EMAIL")[0].text,
                "cpf_cnpj": tree.findall("CPF_CNPJ")[0].text,
                "login": tree.findall("LOGIN")[0].text,
                "rg": tree.findall("RG")[0].text,
                "telefone":telefone,
                "endereco":endereco}

    def _action(self, id_treeapp, schema, id_conteudo, link,
                      add=None, edit=None, delete=None, dados={}):
        """
        """
        pass

    def _verifyEncode(self, dado):
        """
           ver encode da var
        """
        if type(dado) is unicode:
            return dado.encode('latin1')
        else:
            return dado

    def _getAppSession(self):
        """
        busca o aplicativo de sessão
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        dados = portal._getDadosPlug(env_site=self.id_site,
                                     id_plugin=self.id_plugin)
        if dados.get("session_schema", None):

            return portal._getAplication(id_site=self.id_site,
                                         meta_type=dados["session_type"],
                                         schema=dados["session_schema"])

    def _getAppFunc(self):
        """
        busca o aplicativo das funções: comentario, votação, etc..
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        dados = portal._getDadosPlug(env_site=self.id_site,
                                     id_plugin=self.id_plugin)
        if dados.get("func_schema", None):

            return portal._getAplication(id_site=self.id_site,
                                         meta_type=dados["func_type"],
                                         schema=dados["func_schema"])


    def _isSessionActive(self, cookie=None):
        """
        verifica se há uma sessão ativa do user no app session
        """
        cookie = cookie if cookie else COOKIE_NAME
        session = self._getAppSession()
        usuario = session._isSessionActive(cookie)
        if usuario:
            return usuario
        else:
            self._expiresUser(cookie)
            return False

    def _expiresUser(self, cookie=None):
        """
        expira a sessao com o user
        """
        cookie = cookie if cookie else COOKIE_NAME
        session = self._getAppSession()
        expire = session.expiresUser(cookie)
        return expire

    @jsoncallback
    def logoff(self):
        """
        """

        return self._logoff()

    def _logoff(self):
    
        session = self._getAppSession()

        return session.expiresUser()

    @serialize
    @Permission("ADM PLUG")
    def bloqueaDesbloqueaUser(self, email, block=None):
        """
        """
        proxy = self._getProxy(suds=True)
        if block:
            res = proxy.bloqueiaUsuario(login=email,
                                        servico_id=self.dados["id_servico"],
                                        origem=self.dados["wsdl_origin"])
            if res.result == "1":
                return "Usu&aacute;rio bloqueado com sucesso!"
            return "Usu&aacuterio n&atilde;o pode ser bloqueado."
        else:
            res = proxy.desbloqueiaUsuario(login=email,
                                           servico_id=self.dados["id_servico"],
                                           origem=self.dados["wsdl_origin"])
            if res.result == "1":
                return "Usu&aacute;rio desbloqueado com sucesso!"
            return "Usu&aacuterio n&atilde;o pode ser desbloqueado."

    @jsoncallback
    def autenticar(self, email, senha, id_servico=None):
        """
            encapsulamento do metodo autenticar
            em json
        """
        return self._autenticar(email=email,
                                senha=senha,
                                id_servico=id_servico)

    
    def _autenticar(self, email, senha, id_servico=None, cookie=None):
        """
          erros:
             3 - Login existe mais senha incorreta
             4 - Usuario Bloqueado
             5 - Usuario nao existe
              
          Sucesso:
             1 - Autenticado com sessão
             2 - Autenticado sem sessão
        """
        session = self._getAppSession()
        proxy = self._getProxy(suds=True)
        res = proxy.autenticaUsuarioBloqueio(login=email,
                                             senha=senha,
                                             servico=id_servico if id_servico else self.dados["id_servico"],
                                             origem=self.dados["wsdl_origin"])
        if int(res.result[3]) and not int(res.result[0]):           
            self.validaCadastro(email)
            if session:             
                dnow, dtpas = session._gdt()
                sessiondate = session._getDados()
                id = session._psid()
                dados = self._getUserData(email)
                expires = datetime.datetime.now() + datetime.timedelta(hours=1)
                extra = encode({"nome": dados['nome'], "cpf_cnpj": dados['cpf_cnpj'], "email": dados['email']})
                nome = urllib.quote(dados['nome'].encode("latin1"))
                session._sessionAdd(id_session=id,
                                         nome=dados['nome'].encode("latin1"),
                                         email=email,
                                         datahorae=dtpas,
                                         extr=extra)
                valor = "%s|%s|%s" % (id, nome, email)
                name_host = sessiondate["site"]
                cookie = cookie if cookie else COOKIE_NAME
                self.request.setCookie(cookie,
                                          valor,
                                          expires="",
                                          host=name_host)

                return {"type":"ok",
                        "description": "autenticado com sessao",
                        "id": "1"}
            else:        
                return {"type": "ok",
                        "description": "autenticado sem sessao",
                         "id": "2"}
        elif not int(res.result[3]) and int(res.result[2]) and not int(res.result[0]):
            return  {"type": "error",
                      "description": "Login existe mais senha esta incorreta",
                       "id": "3"}
        elif int(res.result[0]):
            return  {"type": "error",
                      "description": "Usuario bloqueado",
                       "id": "4"}
        else:
            return  {"type": "error",
                      "description": "Usuario nao existe",
                       "id": "5"}
    @jsoncallback
    def autenticarAssinante(self, email, senha, id_servico=None):
        """
            encapsulamento do metodo autenticarAssinante
            em json
        """
        return self._autenticarAssinante(email=email,
                                         senha=senha,
                                         id_servico=id_servico)
    
    def _autenticarAssinante(self, email, senha, id_servico=None, cookie=None):
        """
           erros:
               3 - error ao autenticar
           Sucesso:
               1 - usuário autenticado com sessao
               2 - usuário autenticado sem sessao               
        """
        session = self._getAppSession()
        proxy = self._getProxy(suds=True)
        res = proxy.autenticaAssinanteProvedor(email=email,
                                               senha=senha,
                                               provedor=self.dados.get("provedor", None),
                                               servico=id_servico if id_servico else self.dados["id_servico"],
                                               origem=self.dados["wsdl_origin"])
        if int(res.result):
            if session:             
                dnow, dtpas = session._gdt()
                sessiondate = session._getDados()
                id = session._psid()
                dados = self._getUserData(email)
                expires = datetime.datetime.now() + datetime.timedelta(hours=1)
                extra = encode({"nome": dados['nome'], "cpf_cnpj": dados['cpf_cnpj'], "email": dados['email']})
                nome = urllib.quote(dados['nome'].encode("latin1"))
                session._sessionAdd(id_session=id,
                                         nome=dados['nome'].encode("latin1"),
                                         email=email,
                                         datahorae=dtpas,
                                         extr=extra)
                valor = "%s|%s|%s" % (id, nome, email)
                name_host = sessiondate["site"]
                cookie = cookie if cookie else COOKIE_NAME
                self.request.setCookie(cookie,
                                          valor,
                                          expires="",
                                          host=name_host)

                return {"type":"ok",
                        "description": "autenticado com sessao",
                        "id": "2"}
            else:        
                return {"type": "ok",
                        "description": "autenticado sem sessao",
                         "id": "1"}
        else:
            return {"type":"error",
                    "description":"error ao autenticar",
                    "id":"3"}

    def _insereEndereco(self, email, rua, numero, complemento,
                        bairro, cidade, estado, cep, pais,
                        tipo="1", codigo_externo=''):
        """
            insere novo endereço para user
            
            sucesso:
                1 - inserido com sucesso
            error:
                2 - error ao inserir endereco
        """
        login = self._getUserData(email)['login']
        proxy = self._getProxy(suds=True)
        end = proxy.insereEndereco(login=login,
                                   rua=rua.decode("latin1"),
                                   numero=numero,
                                   complemento=complemento,
                                   bairro=bairro.decode("latin1"),
                                   cidade=cidade.decode("latin1"),
                                   estado=estado.decode("latin1"),
                                   cep=cep,
                                   pais=pais.decode("latin1"),
                                   tipo=tipo,
                                   codigo_externo=codigo_externo,
                                   origem=self.dados["wsdl_origin"])
        if int(end.result):

            return {"type":"ok",
                    "description": "inserido com sucesso",
                    "id": "1"}
        else:
        
            return {"type":"error",
                    "description": "error ao inserir endereco",
                    "id": "2"}
    
    def _insereTelefone(self, email, telefone):
        """
            insere novos telefones

            sucesso:
                1 - sucesso ao inserir telefone
            error:
                2 - erro ao inserir telefone
        
        """
        telefone = telefone.replace("(",'').replace(")",'').split(' ')
        login = self._getUserData(email)['login']
        proxy = self._getProxy(suds=True)
        tel = proxy.insereTelefone(login=login, 
                                   ddi='', 
                                   ddd=telefone[0], 
                                   telefone=telefone[1].replace('-',''), 
                                   tipo='1', 
                                   ramal='', 
                                   codigo_externo='',            
                                   origem=self.dados["wsdl_origin"])
        if int(tel.result):
   
            return {"type":"ok",
                    "description":"sucesso ao inserir telefone",
                    "id":"1"}
        else:
     
            return {"type":"error",
                    "description":"error ao inserir telefone",
                    "id":"2"}
    
    def vercad(self, email):
        """
           Valida se existe login
        """
        proxy = self._getProxy(suds=True)
        res = proxy.emailExiste(email=email,
                                origem=self.dados["wsdl_origin"]) 
        if int(res.result):
            return True
        else:
            return False

    @jsoncallback
    def verEmail(self, email):
        """
        """
        confirmado = self.vercad(email)
        if confirmado:
            return {"type": "ok",
                    "description": "email existe",
                    "id":"1"}
        else:
            return {"type": "ok",
                    "description": "email nao existe",
                    "id":"2"}

    @serialize
    @Permission("ADM PLUG")
    def recuperar(self, email):
        """
        """
        proxy = self._getProxy(suds=True)
        res = proxy.esqueciSenha(email=email,
                                 tl=self.dados["titulo"],
                                 origem=self.dados["wsdl_origin"])
        if int(res.result):
            return True
        return False
   
    @serialize
    def validaCadastro(self, email, data_expiracao=""):
        """
        """
        proxy = self._getProxy(suds=True)
        res = proxy.habilitaServico(email=email,
                                      servico=self.dados["id_servico"],
                                      data_expiracao=data_expiracao,
                                      origem=self.dados["wsdl_origin"])
        if res.result =='1':
            return True
        return False

    @serialize
    @Permission("ADM PLUG")
    def atualizarCad(self, matricula, senha_velha, email, senha_nova, apelido,
                     primeiro_nome, ultimo_nome, sexo, data_nasc, cpf, rg, cep,
                     estado, cidade, bairro, endereco, numero, complemento,
                     telefone, ddd, tipo_end="residencial", pessoa="", cod="",
                     pais="Brasil", codigo=""):
 
        """
        """
        proxy = self._getProxy(suds=True)
        end_id = proxy.buscaDadosEndereco(login=email, origem=self.dados["wsdl_origin"])
        tel_id = proxy.buscaDadosTelefone(login=email, origem=self.dados["wsdl_origin"])
        cad = proxy.alteraLogin(login=email,
                                email=email,
                                nome=primeiro_nome+" "+ultimo_nome,
                                apelido=apelido,
                                sexo=sexo,
                                dt_nascimento=data_nasc,
                                cpfcnpj=cpf,
                                pessoa=pessoa,
                                contato=ddd+telefone,
                                rg=rg,
                                origem=self.dados["wsdl_origin"])

        end = proxy.alteraEndereco(login=email,
                                   endereco_id=end_id,
                                   rua=endereco,
                                   numero=numero,
                                   complemento=complemento,
                                   bairro=bairro,
                                   cidade=cidade,
                                   estado=estado,
                                   cep=cep,
                                   pais=pais,
                                   tipo=tipo_end,
                                   codigo_externo=codigo,
                                   origem=self.dados["wsdl_origin"])


        tel = proxy.alteraTelefone(login=email,
                                   telefone_id=tel_id,
                                   ddd=ddd,
                                   fone=telefone,
                                   ramal=ramal,
                                   ddi=ddi,
                                   tipo=tipo_tel,
                                   codigo_externo=codigo,
                                   origem=self.dados["wsdl_origin"])

        if int(cad.result) != 0 and int(end.result) != 0 and int(tel.result) !=0:
            return "Altera&ccedil;&otilde;es feitas com sucesso!"
        return "Houve um erro ao atualizar seus dados, por favor tente novamente mais tarde"
   
    @dbconnectionapp
    def captcha(self):
        """
        """
        session = self._getAppSession()
        captcha = session.captcha()
        return captcha

    @jsoncallback
    def cadastrar(self, e, nome, ultimo, apelido, sexo, nascimento, 
                cpf_cnpj, senha, confirma, rua, numero, complemento, 
                bairro, cidade, estado, cep, ddd, fone, captcha,
                timefutebol=None, ddi="", ramal="", codigo="", tipo_tel="1",
                tipo_end="1", rg="", pais="Brasil", 
                master="", expiracao="", pessoa="F", id_servico=None):
        """
         erros:
          1 - ja existe o email
          2 - dados incorretos
          3 - erro nao definido
          4 - codigo incorreto
          5 - ja existe login
        sucesso:
          1 - cadastro efetuado

        """
        session = self._getAppSession()
        capt = captcha.lower()
        captcha = session.getCaptchaSession(captcha.upper())
        validacao = self.vercad(e)
        if validacao:
            res = {"type":"error",
                   "description":"email ja existente",
                   "id":"1"}
        else:
            if captcha:
                errs = 0
                try:
                    numero = numero
                except:
                    numero = None
                try:
                   fone = fone.replace("-", "")
                except:
                   fone = None
                try:
                   ddd = ddd
                except:
                   ddd = None
                try:
                   cep = cep.replace("-", "")
                except:
                   cep = None
                from publica.utils.cpf import CPF
                er = ""
                if e.find("@") < 0 or (len(e) > 64 or len(e) == 0):
                    errs = 1
                    er+="email "
                elif len(nome) > 64 or len(nome) == 0:
                    errs = 1
                    er+="nome "
                elif len(ultimo) > 64 or len(ultimo) == 0:
                    errs = 1
                    er+="sobrenome "
                elif len(apelido) > 32 or len(apelido) == 0:
                    errs = 1
                    er+="apelido "
                elif sexo not in ("F", "M"):
                    errs = 1
                    er+=" sexo "
                elif nascimento == None:
                    errs = 1
                    er+="nascimento "
                elif not CPF(cpf_cnpj).isValid():
                    errs = 1
                    er+="cpf "
                elif not (len(senha) >= 6 and len(senha) < 32) or (senha != confirma):
                    errs = 1
                    er+="senha "
                elif len(rua) > 64 or len(rua) == 0:
                    errs = 1
                    er+"rua "
                elif numero == None:
                    errs = 1
                    er+="numero "
                elif len(complemento) > 32:
                    errs = 1
                    er+="complemento "
                elif len(bairro) > 64 or len(bairro) == 0:
                    errs = 1
                    er+="bairro "
                elif len(cidade) > 64 or len(cidade) == 0:
                    errs = 1
                    er+="cidade "
                elif len(estado) > 32 or len(estado) == 0:
                    errs = 1
                    er+="estado "
                elif cep == None:
                    errs = 1
                    er+="cep "
                elif ddd == None:
                    errs = 1
                    er+="ddd "
                elif fone == None:
                    errs = 1
                    er+="fone "
                if errs:
                    res = {"type":"error",
                           "description":"dados incorretos "+er,
                           "id":"2"}
                
                else:                   
                    nome = nome + " " + ultimo
                    nlogin = e.find('@')
                    login = e[ :nlogin]
                    verlogin = self.verLogin(login)
                    if verlogin:
                        res = {"type": "error",
                                "description": "Login existe",
                                "id":"5"}
                    elif not verlogin:
                        tempHash = session.cadastrarUser(login=login,
                                                        master=master,
                                                        email=e,
                                                        nome=nome,
                                                        apelido=apelido,
                                                        sexo=sexo,
                                                        dt_expiracao=expiracao,
                                                        dt_nascimento=nascimento,
                                                        cpfcnpj=cpf_cnpj,
                                                        pessoa= pessoa,
                                                        contato=fone,
                                                        rg=rg,
                                                        senha=senha,
                                                        rua=rua,
                                                        numero=numero,
                                                        complemento=complemento,
                                                        bairro=bairro,
                                                        cidade=cidade,
                                                        estado=estado,
                                                        cep=cep,
                                                        pais=pais,
                                                        tipo_end=tipo_end,
                                                        ddi=ddi,
                                                        ddd=ddd,
                                                        telefone=fone.replace('-',''),
                                                        tipo_tel=tipo_tel,
                                                        ramal=ramal,
                                                        codigo_externo=codigo)
                        site = getDadosSite(id_site=self.id_site,
                                             request=self.request)
                        if not id_servico:
                            link = ("%splug/da_centrallogin/%s,%s/validaCad?codigo=%s"
                                                % (site["base_dinamico"],
                                                   self.id_plugin,
                                                   self.id_site,
                                                   tempHash))
                        else:
                            link = ("%splug/da_centrallogin/%s,%s/validaCad?codigo=%s&serv=%s"
                                                % (site["base_dinamico"],
                                                   self.id_plugin,
                                                   self.id_site,
                                                   tempHash,
                                                   id_servico))    
                        msg = msg3 % {"link":link,
                                      "title":self.dados["titulo"]}
                        email = Email()
                        email.enviarEmail(subject=msg12 % self.dados["titulo"],
                                              to=e,
                                              fro=self.dados["from_host"],
                                              text=msg,
                                              returnpath=self.dados["return_path"],
                                              host=self.dados["smtp_host"],
                                              port=self.dados["smtp_port"],
                                              type="text/html")
                        res = {"type": "ok",
                                "description": "cadastro efetuado com sucesso",
                                "id":"1"}
                    else:
                        res = {"type":"error",
                               "description":"erro nao definido",
                               "id":"3"}
            else:
                res = {"type": "error",
                       "description": "codigo incorreto",
                       "id": "4"}  
        return res

    def verLogin(self, login):
        """
        """
        proxy = proxy = self._getProxy(suds=True)
        verlog = proxy.loginExiste(login=login,
                                   origem=self.dados["wsdl_origin"])
        if int(verlog.result):
            return True
        else:
            return False
                                   
        
    
    def validaCad(self, codigo, serv=None):
        """
        erros
          2 - 
       
        sucesso
          1 - 
        """
        proxy = self._getProxy(suds=True)
        session = self._getAppSession()
        valida = session.getHash(codigo)
        if valida:
            cad = proxy.insereLogin(login=valida['login'].decode('Latin1'),
                                     master=valida['master'],
                                     email=valida['email'],
                                     nome=valida['nome'].decode('Latin1'),
                                     apelido=valida['apelido'].decode('Latin1'),
                                     sexo=valida['sexo'],
                                     dt_expiracao=valida['dt_expiracao'],
                                     dt_nascimento=valida['dt_nascimento'],
                                     cpfcnpj=valida['cpfcnpj'],
                                     pessoa=valida['pessoa'],
                                     contato=valida['contato'],
                                     rg=valida['rg'],
                                     senha=valida['senha'],
                                     servico=serv if serv else self.dados["id_servico"],
                                     origem=self.dados["wsdl_origin"])
            end = proxy.insereEndereco(login=valida['login'],
                                       rua=valida['rua'].decode('Latin1'),
                                       numero=valida['numero'],
                                       complemento=valida['complemento'],
                                       bairro=valida['bairro'].decode('Latin1'),
                                       cidade=valida['cidade'].decode('Latin1'),
                                       estado=valida['estado'],
                                       cep=valida['cep'],
                                       pais=valida['pais'],
                                       tipo=valida['tipo_end'],
                                       codigo_externo=valida['codigo_externo'],
                                       origem=self.dados["wsdl_origin"])
            tel = proxy.insereTelefone(login=valida['login'],
                                       ddi=valida['ddi'],
                                       ddd=valida['ddd'],
                                       telefone=valida['telefone'],
                                       tipo=valida['tipo_tel'],
                                       ramal=valida['ramal'],
                                       codigo_externo=valida['codigo_externo'],
                                       origem=self.dados["wsdl_origin"])
            if int(cad.result) != 0 and int(end.result) != 0 and int(tel.result) != 0:
                session.delHash(codigo)
                self.validaCadastro(valida['email'])
                return "valida&ccedil;&atilde;o foi um sucesso"
            
        else:
            return "valida&ccedil;&atilde;o ja efetuada"
        
    @jsoncallback
    def comentar(self, schema, comentario, i):
        """
        erros
        3 - usuario nao autenticado
        
        sucesso
        1 - comentario adicionado com sucesso
        2 - comentario bloqueado
         
        """
        session = self._getAppSession() 
        func = self._getAppFunc()
        usuario = session._isSessionActive()      
        if usuario:
            nome = usuario['nome']
            email = usuario['email']
            resposta = func._comentar(schema, i, email, nome, comentario)
            if resposta['id']=='1':
                res = {"type": "ok",
                       "description": "Comentario adicionado com sucesso",
                       "id": "1"}
            elif resposta['id'] == '2':
                res = {"type": "ok",
                       "description": "Comentario bloqueado",
                       "id": "2"}
        else:
            res = {"type": "error",
                   "description": "usuario nao autenticado",
                   "id": "3"}
        return res

    @jsoncallback      
    def votar(self, schema, i, voto):
        """
        sucesso
        1 - Voto computado com sucesso
        
        error
        1 - usuario ja votou
        2 - usuario nao autenticado
    
        """
        session = self._getAppSession()
        func = self._getAppFunc()
        usuario = session._isSessionActive()
        if usuario:
            return func._votar(schema, i, voto) 
            if resposta['id'] == '1' and resposta['type'] == 'error':
                res = {"type":"error",
                       "description":"Usuario ja votou",
                       "id":"1"}

            elif resposta['id'] == '1' and resposta['type'] == 'ok':
                res = {"type":"ok",
                       "description":"Voto computado com sucesso",
                       "id":"1"}
        else:
            res = {"type":"error",
                   "description":"Usuario nao autenticado",
                   "id":"2"}
        return res

    @jsoncallback
    def denuncia(self, id_comentario, i, 
                 denuncia, url, schema):
        """
        """
        session = self._getAppSession()
        func = self._getAppFunc()
        usuario = session._isSessionActive()
        if usuario:
            return func._denuncia(id_comentario, 
                                  i, 
                                  usuario['email'], 
                                  usuario['nome'], 
                                  denuncia, 
                                  url, 
                                  schema)
        else:
            return {"type":"error",
                   "description":"Usuario nao autenticado",
                   "id":"2"}
