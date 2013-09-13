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
import os
import sys
import re
import datetime
import random
import time as dtime, time
from random import Random, choice, random
from publica.utils.packages.pil.PIL import Image, ImageDraw, ImageFont
from RandImage import RandImage
from publica import settings
from publica.utils.util import newpasswd, md5 as hashlib
from publica.utils.json import encode, decode
from publica.utils.decorators import dbconnectionapp, serialize, jsoncallback
from publica.core.portal import Portal
try:
    from mx.DateTime import DateTime, \
        TimeDelta, DateTimeType
except ImportError:
    from datetime import datetime as DateTime, \
        timedelta as TimeDelta, datetime as DateTimeType

COOKIE_NAME = "wdah"
COOKIE_CAPTCHA = "envcat"
PATH_FONT = os.path.dirname(__file__) + "/fonts"


class Public(object):

    """
        public class of methods of this content
    """
    def _gdt(self):
        """
        """
        return (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
               (datetime.datetime.now() -
                    datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))

    def _psid(self):
        """
        """
        return (time.time() + random()).__str__()

    def _getDados(self):
        """
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        dados = portal._getApp(env_site=self.id_site,
                               schema=self.schema)
        return dados["dados"]

    _session_data = property(_getDados, None, None, "Dados da session")

    def _getSessionId(self, cookie):
        """Retorna o id do cookie de sessao se o usuario tiver logado
        """
        ck = self.request.getCookie(cookie)
        if ck:
            return ck.split("|")
        return []

    @dbconnectionapp
    def _isSessionActive(self, cookie=None):
        """Retorna se existem um cookie de sessao ativo
        """
        cookie = cookie if cookie else COOKIE_NAME
        ck = self._getSessionId(cookie)
        if len(ck) == 3:

            datahora = (datetime.datetime.now() -
                        datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
            id_session, nome, email = ck
            usuario = {"id_session": None}
            for i in self.execSql("select_session_dados",
                                  id_session=id_session,
                                  datahora=datahora):
                self.execSqlu("update_session_user",
                              id_session=id_session)
                usuario = i

            if (usuario["id_session"]):
                usuario["extra"] = decode(usuario["extra"])

                return usuario

        return False

    @dbconnectionapp
    def _sessionAdd(self, id_session, nome, email, datahorae, extr):
        """
        """
        self.execSqlu("insert_session",
                      id_session=id_session,
                      nome=nome,
                      email=email,
                      extra=extr,
                      datahorae=datahorae)

    @dbconnectionapp
    def expiresUser(self, cookie=None):
        """
        """
        cookie = cookie if cookie else COOKIE_NAME
        name_host = self._session_data["site"]
        dados = self._getSessionId(cookie)
        if dados:
            id_session = dados[0]
            self.execSqlu("delete_session",
                          id_session=id_session)
        expires = datetime.datetime.now() - datetime.timedelta(hours=1)
        self.request.setCookie(name=cookie,
                               value="",
                               host=name_host,
                               expires=expires)
        return "Login expirado com sucesso"

    @jsoncallback
    def logoff(self):
        """
        """
        return self.expiresUser()

    def isAuthenticated(self):
        """
        sucesso:
            1 - usuario autenticado
        erro:
            1 - usuario nao autenticado
        """
        dados = self.isSessionActive()
        if dados:
            res = {"type": "ok",
                   "description": "Usuario autenticado",
                   "id": "1",
                   "nome": dados["nome"],
                   "email": dados["email"]}
        else:
            res = {"type": "error",
                   "description": "Usuario nao autenticado",
                   "id": "1"}

        return encode(res)

    @dbconnectionapp
    def captcha(self):
        """
        retorna o codigo da imagem
        """
        dados = self._session_data
        name_host = dados["site"]
        hash = (time.time() + random()).__str__()

        randimage = RandImage(PATH_FONT)
        imagem = randimage.get_new_image()
        solucao = imagem[1].lower()
        source = imagem[0]     
        dpas = (datetime.datetime.now() -
                  datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
        expires = datetime.datetime.now() + datetime.timedelta(days=1)
        self.request.setCookie(COOKIE_CAPTCHA,
                               str(hash),
                               expires=expires,
                               host=name_host)

        self.execSqlu("insert_captcha",
                      datah=dpas,
                      hash=hash,
                      solucao=solucao.upper())
        self.request.setHeader("Content-type",
                               "image/jpeg")

        return source

    @dbconnectionapp
    def getCaptchaSession(self, captcha):
        """
        """
        ck = self.request.getCookie(COOKIE_CAPTCHA)
        if ck:
            for i in self.execSql("select_sessao_captcha",
                                   hash=ck):
                if i["solucao"] == captcha:
                    res = True
                    break
            else:
                res = False

        return res

    @dbconnectionapp
    def cadastrarUser(self, login,  email, nome, apelido, 
                      sexo, dt_nascimento, cpfcnpj, pessoa, 
                      contato, rg, senha, rua, numero, complemento, 
                      bairro, cidade, estado, cep, pais, tipo_tel, 
                      ddd, telefone, tipo_end, dt_expiracao="", master="", 
                      ddi="", ramal="", codigo_externo=""):
        """
        """
        cod = (time.time() + random()).__str__()
        codigo = hashlib(cod).hexdigest()
        self.execSqlu("insert_session_temp",
                             codigo=codigo,
                             login=login,
                             master=master,
                             email=email,
                             nome=nome,
                             apelido=apelido,
                             sexo=sexo,
                             dt_expiracao=dt_expiracao,
                             dt_nascimento=dt_nascimento,
                             cpfcnpj=cpfcnpj,
                             pessoa= pessoa,
                             contato=telefone,
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
                             telefone=telefone,
                             tipo_tel=tipo_tel,
                             ramal=ramal,
                             codigo_externo=codigo_externo)
        return codigo

    @dbconnectionapp
    def getHash(self, codigo):
        """
        """
        chave = codigo
        if chave:
            for i in self.execSql("select_session_temp",
                                      codigo=chave):
                return i
        return False

    @dbconnectionapp
    def delHash(self, codigo):
        """
        """
        delete = self.execSqlu("delete_temp_session",
                                    codigo=codigo)
        return True
       
