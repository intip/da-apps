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

from publica import settings
from publica.core.portal import Portal
from publica.utils.json import encode, decode
from publica.utils.decorators import dbconnectionapp, serialize, jsoncallback, \
                                     permissioncron
from datetime import datetime, timedelta, time
COOKIE_PROMO= "promo"
COOKIE_ASSINANTE="promoassi"

class Public(object):

    """
        public class of methods of this content
    """
    def _getAppAuth(self):
        """
            retorna os dados do app
        """
        portal = Portal(id_site=self.id_site,
                       request=self.request)
        return portal._getPlug(env_site=self.id_site,
                              id_plugin=self.auth)['app']

    def _getPlugCaptcha(self):
        """
            returns plugin captcha
        """
        portal = Portal(id_site=self.id_site,
                       request=self.request)
        return portal._getPlug(env_site=self.id_site,
                               id_plugin=self.captcha)['app']

    @dbconnectionapp
    def _getSorteadosPromocao(self, id_conteudo):
        """
            retorna os sorteados de uma promocao
        """
        sorteados = []
        for i in self.execSql("select_sorteados_promocao_not_limit",
                               id_conteudo=int(id_conteudo)):
            i["nome"] = i["nome"].decode("utf8").encode("latin1")
            sorteados.append(i)
        return sorteados
    
    @dbconnectionapp
    def _getPromocao(self, id_conteudo):
        """
            retorna uma promoção
        """
        for i in self.execSql("select_conteudo",
                              id_conteudo=int(id_conteudo)):
            i['sorteados'] = self._getSorteadosPromocao(i['id_conteudo'])
            if self.tipo == 'aberta':
                tipo = True
            else:
                tipo = False
            
            i['aberta'] = tipo
            return i

    @dbconnectionapp
    def _getPromocoesFinalizadas(self, limit=None):
        """
            retorna as promocoes que foram
            finalizadas
        """
        if limit:
            return self.execSql("select_promocoes_limit_finalizadas",
                                 limit=int(limit))
        else:
            return self.execSql("select_promocoes_finalizadas")


    @dbconnectionapp
    def _getPromocoes(self, limit=None):
        """
            retorna todas promocoes 
        """
        if limit:
            return self.execSql("select_promocoes_limit",
                                 limit=int(limit))
        else:
            return self.execSql("select_promocoes")

    @jsoncallback
    def autenticar(self, email, senha, challenge=None, 
                   response=None):
        """
            retorna o autenticar da central

        """
        #sessao = self._verificaSessao(email, id_conteudo)
        ip = self.request.getiphost()
        central = self._getAppAuth()
        captcha = self._getPlugCaptcha()
        #if sessao:
            #return {"type":"error",
                #    "description":sessao,
                 #   "id":"7"}
        if self.ips:
            if ip in self.ips:
                return {"type":"error",
                        "description":"ip bloqueado",
                        "id":"6"}
        if central:
            if captcha:
                if not captcha._submit(challenge=challenge,
                                       response=response,
                                       remoteip=ip):
                    return {"type":"error",
                            "description":"codigo incorreto",
                            "id":"2"}

            if self.tipo == "aberta":
                return central._autenticar(email, 
                                           senha,
                                           self.id_servico,
                                           COOKIE_PROMO)
            else:
                return central._autenticarAssinante(email, 
                                                    senha,
                                                    self.id_servico,
                                                    COOKIE_ASSINANTE)
        else:
            return {"type":"error",
                    "description":"nao vinculado a central",
                    "id":"1"} 

    @jsoncallback
    def logoff(self):
        """
            expira user do user
        """
        central = self._getAppAuth()
        if central:
            if self.tipo == "aberta":
                return central._expiresUser(COOKIE_PROMO)
            else:
                return central._expiresUser(COOKIE_ASSINANTE)
        else:
            return {"type":"error",
                    "description":"nao vinculado a central",
                    "id":"1"}  

    def _getDadosUsuario(self, email):
        """
            retorna dados do usuario
            
            1 = error central nao vinculada
        """
        central = self._getAppAuth()
        if central:
            return central._getUserData(email)
        else:
            return {"type":"error",
                    "description":"nao vinculado a central",
                    "id":"1"}
    
    @dbconnectionapp
    def _getPromocaoFinalizadaDias(self, dias, limit=None):
        """
            retorna as promocoes finalizadas 
            no periodo em dias passado
        """
        data = datetime.now() - timedelta(days=int(dias))
        if limit:
            return self.execSql("select_promocoes_finalizada_dias_limit",
                                 limit=int(limit),
                                 data=data)
        else:
            return self.execSql("select_promocoes_finalizada_dias",
                                 data=data)

    
    @jsoncallback
    def getDadosUsuario(self):   
        """
            retorna dados do usuario callback

            1 = usuario nao autenticado
            2 = error central nao vinculada
        """
        central = self._getAppAuth()
        if central:
            if self.tipo == 'aberta':
                sessao = central._isSessionActive(cookie=COOKIE_PROMO)
            else:
                sessao = central._isSessionActive(cookie=COOKIE_ASSINANTE)
            if sessao:
                return self._getDadosUsuario(sessao['email'])
            else:
                return {"type":"error",
                        "description":"usuario nao autenticado",
                         "id":"1"}
        else:
            return {"type":"error",
                    "description":"nao vinculado a central",
                    "id":"2"}  

    @jsoncallback
    def insereEndereco(self, email, rua, numero, complemento,
                        bairro, cidade, estado, cep, pais,
                        tipo="1", codigo_externo=''):
        """
            insere um novo endereço para o user
         
            1 = error central nao vinculada
        """
        central = self._getAppAuth()
        if central:
            if self.tipo == 'aberta':
                sessao = central._isSessionActive(cookie=COOKIE_PROMO)
            else:
                sessao = central._isSessionActive(cookie=COOKIE_ASSINANTE)
            if sessao:
                return central._insereEndereco(email=email, 
                                               rua=rua, 
                                               numero=numero, 
                                               complemento=complemento,
                                               bairro=bairro, 
                                               cidade=cidade, 
                                               estado=estado, 
                                               cep=cep.replace("-",""), 
                                               pais=pais,
                                               tipo=tipo, 
                                               codigo_externo=codigo_externo)
            else:
                return {"type":"error",
                        "description":"login expirado",
                         "id":"2"} 
        else:
            return {"type":"error",
                    "description":"nao vinculado a central",
                    "id":"1"} 

    @jsoncallback
    def insereTelefone(self, email, telefone):
        """

            insere um novo telefone para o usuário
            
            1 = error central nao vinculada

        """
        central = self._getAppAuth()
        if central:
            if self.tipo == 'aberta':
                sessao = central._isSessionActive(cookie=COOKIE_PROMO)
            else:
                sessao = central._isSessionActive(cookie=COOKIE_ASSINANTE)
            if sessao:
                return central._insereTelefone(email=email,
                                               telefone=telefone)
            else:
                return {"type":"error",
                        "description":"nao vinculado a central",
                         "id":"2"} 
        else:
            return{"type":"error",
                   "description":"nao vinculado a central",
                   "id":"1"}  

    @dbconnectionapp
    def _verificaSessao(self, email, id_conteudo=None):
        """
            verifica se o usuário participou
            de alguma promocão caso sim 
            retorna False senão retorna
            e horario que falta para logar
        """
        if not id_conteudo:
            res = list(self.execSql("select_dhora_participante",
                                    email=email))
        else:
            res = list(self.execSql("select_dhora_participante_idconteudo",
                                    email=email,
                                    id_conteudo=id_conteudo))
        if res:
            for i in res:
                data_user = datetime.strptime(i['dhora_participacao'],"%d/%m/%Y %H:%M") + timedelta(minutes=15)
                dt_now = datetime.now()
                if data_user > dt_now:
                    temp = data_user -dt_now
                    return str(temp)
                else:
                    return False
        else:
            return False

    @dbconnectionapp
    def _getStatusUsuario(self, email):
        """
            retorna o status do usuario
        """
        status = list(self.execSql("select_status_usuario",
                                   email=email))
        return status

    @dbconnectionapp
    def _getStatusUsuarioPromocao(self, cpf, id_conteudo):
      """
          retorna status do usuario na promocao
      """
      status = list(self.execSql("select_status_usuario_promocao",
                                  id_conteudo=int(id_conteudo),
                                  cpf=cpf))
      return status

    @dbconnectionapp
    def _getStatusDuplicado(self, nome, cpf, id_conteudo):
        """
           retorna se o user ta duplicado
        """
        duplicado = list(self.execSql("select_duplicado_user",
                                       nome=nome,
                                       cpf=cpf,
                                       id_conteudo=id_conteudo))
        return duplicado

    @dbconnectionapp
    @permissioncron
    def _autoSort(self):
        """
            sorteia uma promocao automaticamente
        """
        data_de = datetime.now().strftime("%Y-%m-%d 00:00")
        data_ate = datetime.now().strftime("%Y-%m-%d %H:%M")
        result = []
        for i in self.execSql("select_promocoes_sort_auto",
                               data_de=data_de,
                               data_ate=data_ate):
            count = self._getCountUsersSorteados(i['id_conteudo'])
            if not int(count):
                promocao = {}
                sorteio = self._sorteiaUser(i['id_conteudo'])
                promocao['titulo'] = i['titulo']
                promocao['result'] = sorteio
                result.append(promocao)
        return result



    @dbconnectionapp
    def _cadastraUser(self, id_conteudo, id_usuario_wad, nome, cpf, email, 
                      endereco, numero, complemento, cep, 
                      bairro, cidade, estado, pais, telefone):
        """
            cadastra um usuario
        """
        id_usuario = list(self.execSql("select_nextval_participante"))[0]['id'] 
        bloqueio = self._getStatusUsuario(email)
        duplicado = self._getStatusDuplicado(nome, cpf, id_conteudo)
        if not bloqueio:
            bloqueio = "false"
        else:
            bloqueio = bloqueio[0]['bloqueio']
        if not duplicado:
            duplicado = "false"
        else:
            duplicado = "true" 
        self.execSqlu("insert_participante",
                       id_usuario=int(id_usuario),
                       id_usuario_wad=id_usuario_wad,
                       nome=nome,
                       cpf=cpf,
                       email=email,
                       endereco=endereco,
                       numero=numero,
                       complemento=complemento,
                       cep=cep,
                       bairro=bairro,
                       cidade=cidade,
                       estado=estado,
                       pais=pais,
                       telefone=telefone,
                       dhora_participacao=datetime.now().strftime("%Y-%m-%d %H:%M"),
                       bloqueio=bloqueio,
                       duplicado=duplicado)

        return id_usuario       

    @jsoncallback
    def participaPromocao(self, id_conteudo, nome, cpf, email, endereco,
                          numero, complemento, cep, bairro, cidade, estado,
                          pais, telefone, frase=None): 
        """
            vincula o usuario a uma promocao
        """
        central = self._getAppAuth()
        if central:
            if self.tipo == 'aberta':
                sessao = central._isSessionActive(cookie=COOKIE_PROMO)
            else:
                sessao = central._isSessionActive(cookie=COOKIE_ASSINANTE) 
            if sessao: 
                temp = self._verificaSessao(email, id_conteudo)
                if temp:
                    return{"type":"error",
                           "description":temp,
                           "id":2}
                else:         
                    id_usuario_wad = self._getDadosUsuario(email)["id"]
                    id_usuario = self._cadastraUser(id_conteudo=int(id_conteudo),
                                                    id_usuario_wad=int(id_usuario_wad),
                                                    nome=nome,
                                                    cpf=cpf,
                                                    email=email,
                                                    endereco=endereco,
                                                    numero=numero,
                                                    complemento=complemento,
                                                    cep=cep,
                                                    bairro=bairro,
                                                    cidade=cidade,
                                                    estado=estado,
                                                    pais=pais,
                                                    telefone=telefone)
                    status = "livre" #self._getStatusUsuarioPromocao(cpf, id_conteudo)

                    #if not status:
                        #status = 'livre'
                    #else:
                        #status = status[0]['status']
                    self.execSqlu("insert_promocao_user",
                                    id_usuario=int(id_usuario),
                                    id_conteudo=int(id_conteudo),
                                    status=status,
                                    frase=frase)
                    #if self.tipo == 'aberta':
                        #central._expiresUser(cookie=COOKIE_PROMO)
                    #else:
                        #central._expiresUser(cookie=COOKIE_ASSINANTE)
                        
                    return {"type":"ok",
                            "description":"sucesso",
                            "id":1}
            else:
                return{"type":"error",
                       "description":"usuario nao autenticado",
                       "id":3}
