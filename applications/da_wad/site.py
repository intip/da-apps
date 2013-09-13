# -*- encoding: LATIN1 -*-
#
# Copyright 2009 Prima Tech.
#
# Licensed under the Environ License, Version 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.intip.com.br/licenses/ENVIRON-LICENSE-1.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import sys
sys.path.append("{0}/modules/soappy".format(os.path.dirname(__file__)))
sys.path.append("{0}/modules/fpconst".format(os.path.dirname(__file__)))
import re
import types
import datetime
import smtplib
import thread
import random
try:
    import cx_Oracle
except:
    pass
from SOAPpy import WSDL

import time as dtime, time
from random import Random, choice, random
from urllib import unquote, quote
from StringIO import StringIO
from RandImage import RandImage
from msgs import msg1, msg2, msg3, msg4, msg5, msg6,\
                 msg7, msg8, msg9, msg10, msg11, msg12,\
                 msg13, msg14, msg15
from email.Message import Message
from email.MIMEText import MIMEText
from publica.utils.packages.pil.PIL import Image, ImageDraw, ImageFont
from publica.utils.json import encode, decode
from publica.utils.postal import Email
from publica.utils.util import newpasswd, md5 as hashlib
from publica.utils.decorators import dbconnectionapp, serialize, jsoncallback
from publica.admin.exchange import getDadosSite
from publica import settings
from publica.db.resolver import _quote
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
os.environ["NLS_LANG"] = ".UTF8"

class Site(object):
    """
    """

    # private methods

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

    _wad_data = property(_getDados, None, None, "Dados do wad")


    def _getConnection(self):
        """
        """
        os.environ["NLS_LANG"] = ".UTF8"
        dados = self._wad_data
        conn = cx_Oracle.Connection("%s/%s@%s" % (dados["wad_user"],
                                                  dados["wad_password"],
                                                  dados["wad_sid"]))
        return conn


    def _getSessionId(self):
        """Retorna o id do cookie de sessao se o usuario tiver logado
        """
        ck = self.request.getCookie(COOKIE_NAME)
        if ck:
            return ck.split("|")
        return []


    @dbconnectionapp
    def _isSessionActive(self):
        """Retorna se existem um cookie de sessao ativo
        """
        ck = self._getSessionId()
        if len(ck) == 3:

            datahora = (datetime.datetime.now() -
                        datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
            id_session, nome, email = ck
            usuario = {"id_session":None}
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


    # public methods


    @dbconnectionapp
    @serialize
    def expiresUser(self):
        """
        """
        name_host = self._wad_data["site"]
        dados = self._getSessionId()
        if dados:
            id_session = dados[0]
            self.execSqlu("delete_session",
                          id_session=id_session)
        expires = datetime.datetime.now() - datetime.timedelta(hours=1)
        self.request.setCookie(name=COOKIE_NAME,
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
            res = {"type":"ok",
                   "description":"Usuario autenticado",
                   "id":"1",
                   "nome":dados["nome"],
                   "email":dados["email"]}
        else:
            res = {"type":"error",
                   "description":"Usuario nao autenticado",
                   "id":"1"}

        return encode(res)


    @dbconnectionapp
    @jsoncallback
    def autenticar(self, e, senha, cod=None, host=None):
        """
        erros:
          1 - sem conexao com banco
          2 - usuario ou senha incorreta
          3 - servico inexistente
          4 - erro desconhecido
          5 - usuario nao existe
          6 - usuario bloqueado
        sucesso:
          1 - usuario autenticado com sucesso
        """
        dados = self._wad_data
        ids = dados["id_servico"]
        origem = dados["origin_wsdl"]
        email = e[:64]
        senha = senha[:44]
        authc = None

        res = {"type":"error", "description":"", "id":"1"}
        try:
            conn = self._getConnection()
        except:
            return res
        if not conn:
            res = {"type":"error",
                   "description":"Sem conexao com banco de dados",
                   "id":"1"}

        else:

            cursor = conn.cursor()
            pResult = cursor.var(cx_Oracle.NUMBER)
            p1 = cursor.var(cx_Oracle.STRING)
            p1.setvalue(0, email)
            p2 = cursor.var(cx_Oracle.STRING)
            p2.setvalue(0, senha)
            p3 = cursor.var(cx_Oracle.NUMBER)
            p3.setvalue(0, ids)

            cursor.callproc("wad.SP_EMAIL_EXIST", (p1, pResult))
            res = pResult.getvalue()
            if pResult.getvalue() <= 0:
                res = {"type":"error",
                       "description":"usuario nao existe",
                       "id":"5"}
                conn.close()
                return res


            cursor.callproc("wad.SP_LOGINSERVICO_EXIST", (p1, p3, pResult))
            if pResult.getvalue() != 1:
                cursor.callproc("wad.SP_LOGINSERVICO_ENABLE",
                                (p1, p3, None, 4, pResult))

            cursor.callproc("wad.SP_EMAIL_AUTHENTIC", (p1, p2, pResult, ids))
            res = pResult.getvalue()
            if res <= 0:
                res = {"type":"error",
                       "description":"Usuario ou senha incorreta",
                       "id":"2"}

            else:

                # verifica se o login esta bloqueado
                """
                 Documentation: retorna 5 caracteres, cada caracter representa uma validacao (0 ou 1)
                 1 = informa se o login está bloqueado;
                 2 = reservado, não tem valor definido;
                 3 = informa se o login informado existe;
                 4 = informa se a foi autenticado;
                 5 = informa se o serviço informado existe para o usuário;
                """
                _proxy =  WSDL.Proxy(dados["url_wsdl"])
                userblock = _proxy.autenticaUsuarioBloqueio(email,
                                                            senha,
                                                            str(ids),
                                                            origem)
                if userblock["result"][0] == "1": # usuario bloqueado
                    res = {"type":"error",
                           "description":"Usuario bloqueado",
                           "id":"6"}
                else: 

                    pIdExterno = cursor.var(cx_Oracle.NUMBER)
                    pLogin = cursor.var(cx_Oracle.STRING)
                    pEmail = cursor.var(cx_Oracle.STRING)
                    pNome = cursor.var(cx_Oracle.STRING)
                    pApelido = cursor.var(cx_Oracle.STRING)
                    pSexo = cursor.var(cx_Oracle.STRING)
                    pCancelado = cursor.var(cx_Oracle.NUMBER)
                    pDt_Expiracao = cursor.var(cx_Oracle.DATETIME)
                    pDt_Nascimento = cursor.var(cx_Oracle.DATETIME)
                    pCPF_CNPJ = cursor.var(cx_Oracle.STRING)
                    pPessoa = cursor.var(cx_Oracle.STRING)
                    pContato = cursor.var(cx_Oracle.STRING)
                    pRg = cursor.var(cx_Oracle.STRING)
                    pCtrl_Origem = cursor.var(cx_Oracle.STRING)
                    pCtrl_BloqUpdate = cursor.var(cx_Oracle.NUMBER)
                    pCtrl_Dt_Insert = cursor.var(cx_Oracle.DATETIME)
                    pCtrl_Dt_UltimoAcesso = cursor.var(cx_Oracle.DATETIME)
                    pCtrl_Dt_Ultimoupdate = cursor.var(cx_Oracle.DATETIME)
                    pCtrl_CodigoSGVD = cursor.var(cx_Oracle.NUMBER)
                    pCtrl_AssinanteJornal = cursor.var(cx_Oracle.NUMBER)
                    pCtrl_AssinanteCodDistrib = cursor.var(cx_Oracle.NUMBER)
                    pCtrl_LoginMasterId = cursor.var(cx_Oracle.NUMBER)
                    pCtrl_LoginCortesia = cursor.var(cx_Oracle.NUMBER)
                    pCtrl_LoginClassificacao = cursor.var(cx_Oracle.NUMBER)
                    pResult = cursor.var(cx_Oracle.NUMBER)

                    p1 = cursor.var(cx_Oracle.STRING)
                    p1.setvalue(0, email)
                    p2 = cursor.var(cx_Oracle.NUMBER)
                    p2.setvalue(0, ids)

                    cursor.callproc("wad.SP_LOGIN_GETDATA",
                                    (p1,
                                     pIdExterno,
                                     pLogin,
                                     pEmail,
                                     pNome,
                                     pApelido,
                                     pSexo,
                                     pCancelado,
                                     pDt_Expiracao,
                                     pDt_Nascimento,
                                     pCPF_CNPJ,
                                     pPessoa,
                                     pContato,
                                     pRg,
                                     pCtrl_Origem,
                                     pCtrl_BloqUpdate,
                                     pCtrl_Dt_Insert,
                                     pCtrl_Dt_UltimoAcesso,
                                     pCtrl_Dt_Ultimoupdate,
                                     pCtrl_CodigoSGVD,
                                     pCtrl_AssinanteJornal,
                                     pCtrl_AssinanteCodDistrib,
                                     pCtrl_LoginMasterId,
                                     pCtrl_LoginCortesia,
                                     pCtrl_LoginClassificacao,
                                     pResult))

                    if pResult.getvalue() > 0:

                        p1 = cursor.var(cx_Oracle.STRING)
                        p1.setvalue(0, email)
                        p2 = cursor.var(cx_Oracle.NUMBER)
                        p2.setvalue(0, ids)

                        dnow, dtpas = self._gdt()
                        id = self._psid()
                        nome = pNome.getvalue()
                        sexo = pSexo.getvalue()
                        rg = pRg.getvalue()
                        extra = encode({"nome":nome, "sexo":sexo, "rg":rg})

                        expires = datetime.datetime.now() + datetime.timedelta(hours=1)
                        nome = unicode(nome, "utf-8").encode('latin1')

                        self._sessionAdd(id_session=id,
                                         nome=nome,
                                         email=email,
                                         datahorae=dtpas,
                                         extr=extra)

                        nome = quote(nome)
                        valor = "%s|%s|%s" % (id, nome, email)
                        name_host = dados["site"]

                        self.request.setCookie(COOKIE_NAME,
                                               valor,
                                               expires="",
                                               host=name_host)
                        res = {"type":"ok",
                               "description":"Usuario autenticado com sucesso",
                               "id":"1"}
                    else:
                        res = {"type":"error",
                               "description":"erro desconhecido",
                               "id":"4"}

            cursor.close()

        if conn:
            conn.close()

        return res


    @jsoncallback
    def vercad(self, e):
        """
        erros:
          1 - sem conexao com banco
          2 - email nao existe
        sucesso:
          1 - email verificado
          2 - ja existe nao e dono
        """
        dados = self._wad_data
        conn = self._getConnection()
        if not conn:
            res = {"type":"error",
                   "description":"Sem conexao com banco de dados",
                   "id":"1"}
        else:

            cursor = conn.cursor()
            pResult = cursor.var(cx_Oracle.NUMBER)

            pIdExterno = cursor.var(cx_Oracle.NUMBER)
            pLogin = cursor.var(cx_Oracle.STRING)
            pEmail = cursor.var(cx_Oracle.STRING)
            pNome = cursor.var(cx_Oracle.STRING)
            pApelido = cursor.var(cx_Oracle.STRING)
            pSexo = cursor.var(cx_Oracle.STRING)
            pCancelado = cursor.var(cx_Oracle.NUMBER)
            pDt_Expiracao = cursor.var(cx_Oracle.DATETIME)
            pDt_Nascimento = cursor.var(cx_Oracle.DATETIME)
            pCPF_CNPJ = cursor.var(cx_Oracle.STRING)
            pPessoa = cursor.var(cx_Oracle.STRING)
            pContato = cursor.var(cx_Oracle.STRING)
            pRg = cursor.var(cx_Oracle.STRING)
            pCtrl_Origem = cursor.var(cx_Oracle.STRING)
            pCtrl_BloqUpdate = cursor.var(cx_Oracle.NUMBER)
            pCtrl_Dt_Insert = cursor.var(cx_Oracle.DATETIME)
            pCtrl_Dt_UltimoAcesso = cursor.var(cx_Oracle.DATETIME)
            pCtrl_Dt_Ultimoupdate = cursor.var(cx_Oracle.DATETIME)
            pCtrl_CodigoSGVD = cursor.var(cx_Oracle.NUMBER)
            pCtrl_AssinanteJornal = cursor.var(cx_Oracle.NUMBER)
            pCtrl_AssinanteCodDistrib = cursor.var(cx_Oracle.NUMBER)
            pCtrl_LoginMasterId = cursor.var(cx_Oracle.NUMBER)
            pCtrl_LoginCortesia = cursor.var(cx_Oracle.NUMBER)
            pCtrl_LoginClassificacao = cursor.var(cx_Oracle.NUMBER)
            pResult = cursor.var(cx_Oracle.NUMBER)

            p1 = cursor.var(cx_Oracle.STRING)
            p1.setvalue(0, e)

            cursor.callproc("wad.SP_LOGIN_GETDATA",
                            (p1,
                             pIdExterno,
                             pLogin,
                             pEmail,
                             pNome,
                             pApelido,
                             pSexo,
                             pCancelado,
                             pDt_Expiracao,
                             pDt_Nascimento,
                             pCPF_CNPJ,
                             pPessoa,
                             pContato,
                             pRg,
                             pCtrl_Origem,
                             pCtrl_BloqUpdate,
                             pCtrl_Dt_Insert,
                             pCtrl_Dt_UltimoAcesso,
                             pCtrl_Dt_Ultimoupdate,
                             pCtrl_CodigoSGVD,
                             pCtrl_AssinanteJornal,
                             pCtrl_AssinanteCodDistrib,
                             pCtrl_LoginMasterId,
                             pCtrl_LoginCortesia,
                             pCtrl_LoginClassificacao,
                             pResult))

            if pResult.getvalue() > 0:
                if pCtrl_Origem.getvalue().upper() == dados["wad_user"].upper():
                    res = {"type":"ok",
                           "description":"email verificado",
                           "id":"1"}
                else:
                    res = {"type":"ok",
                           "description":"email verificado, mas nao e dono",
                           "id":"2"}
            else:
                res = {"type":"erro",
                       "description":"email nao ja existe",
                       "id":"2"}

            cursor.close()

        if conn:
           conn.close()

        return res


    @jsoncallback
    def recuperar(self, e):
        """
        erros:
            1 - sem conexao com banco
            2 - usuario nao existe
            3 - erro nao indentificado
            4 - servico inexistente
        sucesso
            1 - senha enviada
        """
        dados = self._wad_data
        ids = dados["id_servico"]
        e = e[:64]
        conn = self._getConnection()
        if not conn:
            res = {"type":"error",
                   "description":"Sem conexao com banco de dados",
                   "id":"1"}
        else:

            cursor = conn.cursor()
            pResult = cursor.var(cx_Oracle.NUMBER)
            p1 = cursor.var(cx_Oracle.STRING)
            p1.setvalue(0, e)

            cursor.callproc("wad.SP_EMAIL_EXIST", (p1, pResult))
            res = pResult.getvalue()
            if pResult.getvalue() <= 0:
                res = {"type":"error",
                       "description":"usuario nao existe",
                       "id":"5"}
            else:
                passn = newpasswd()

                pResult = cursor.var(cx_Oracle.NUMBER)
                p1 = cursor.var(cx_Oracle.STRING)
                p1.setvalue(0, e)
                p2 = cursor.var(cx_Oracle.STRING)
                p2.setvalue(0, passn)

                cursor.callproc("wad.SP_CHANGEPASSWORD", (p1, None, p2, pResult, 1))
                if pResult.getvalue() > 0:
                    res = {"type":"ok",
                           "description":"email enviado",
                           "id":"1"}
                    msg = unicode(msg1, "latin1")
                    msg = msg % {"senha":passn,
                                 "title": dados["titulo"]}

                    email = Email()
                    email.enviarEmail(subject=unicode(msg2, "latin1"),
                                      to=e,
                                      fro=dados["from_host"],
                                      text=msg.encode("latin1"),
                                      returnpath=dados["return_path"],
                                      host=settings.SMTP_HOST,
                                      port=settings.SMTP_PORT,
                                      type="text/plain")

                else:
                    res = {"type":"error",
                           "description":"erro nao identificado",
                           "id":"3"}
            conn.close()

        return res


    @dbconnectionapp
    @jsoncallback
    def cadastrar(self, e, nome, ultimo, apelido, sexo, nascimento, cpf_cnpj,
                        senha, confirma, rua, numero, complemento, bairro,
                        cidade, estado, cep, ddd, fone, codigo,
                        timefutebol=None, rg=""):
        """
        erros:
          1 - sem conexao com banco
          2 - ja existe o email
          3 - ja existe o login
          4 - dados incorretos
          5 - erro desconhecido
          6 - codigo de verificacao incorreto
          7 - servico inexistente
        sucesso:
          1 - cadastro efetuado
        """
        nome = unicode(nome, "Latin1").encode("utf-8")
        ultimo = unicode(ultimo, "Latin1").encode("utf-8")
        rua = unicode(rua, "Latin1").encode("utf-8")
        complemento = unicode(complemento, "Latin1").encode("utf-8")
        bairro = unicode(bairro, "Latin1").encode("utf-8")
        cidade = unicode(cidade, "Latin1").encode("utf-8")
        estado = unicode(estado, "Latin1").encode("utf-8")

        dadose = self._wad_data
        ids = dadose["id_servico"]
        codigo = codigo.lower()
        ck = self.request.getCookie(COOKIE_CAPTCHA)
        if ck:
             res = {"type":"error", "description":"codigo incorreto", "id":"6"}
             for i in self.execSql("select_sessao_captcha",
                                   hash=ck):
                 if i["solucao"] == codigo:
                     res = None
                     break
        else:
            res = {"type":"error",
                   "description":"codigo incorreto",
                   "id":"6"}

        if res is not None:
            return res

        conn = self._getConnection()
        if not conn:
            res = {"type":"error",
                   "description":"Sem conexao com banco de dados",
                   "id":"1"}

        else:
            email = e

            cursor = conn.cursor()
            pResult = cursor.var(cx_Oracle.NUMBER)
            p1 = cursor.var(cx_Oracle.STRING)
            p1.setvalue(0, email)

            cursor.callproc("wad.SP_EMAIL_EXIST", (p1, pResult))
            res = pResult.getvalue()
            if pResult.getvalue() > 0:
                res = {"type":"erro",
                       "description":"ja existe o email",
                       "id":"2"}
            else:
                p1 = cursor.var(cx_Oracle.STRING)
                p1.setvalue(0, email.replace("@", ""))

                cursor.callproc("wad.SP_LOGIN_EXIST", (p1, pResult))
                res = pResult.getvalue()
                if res > 0:
                    res = {"type":"erro",
                           "description":"ja existe o login",
                           "id":"3"}
                else:

                    errs = 0
                    def isdate(dt):
                        try:
                            dt = dtime.strptime(dt, "%d/%m/%Y")
                            dtime.strftime("%Y-%m-%d", dt)
                            return dtime.strftime("%Y-%m-%d", dt)
                        except:
                            return None

                    try:
                      numero = int(numero)
                    except:
                      numero = None

                    try:
                      fone = int(fone.replace("-", ""))
                    except:
                      fone = None

                    try:
                      ddd = int(ddd)
                    except:
                      ddd = None

                    try:
                      cep = int( cep.replace("-", "") )
                    except:
                      cep = None

                    from publica.utils.cpf import CPF
                    er = ""
                    nascimento = isdate(nascimento)
                    if email.find("@") < 0 or (len(email) > 64 or len(email) == 0):
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
                               "description":"dados incorretos"+er,
                               "id":"4"}
                    else:
                        nome = nome + " " + ultimo
                        dados = {"e":e,
                                 "nome":nome,
                                 "apelido":apelido,
                                 "sexo":sexo,
                                 "nascimento":nascimento,
                                 "cpf_cnpj":cpf_cnpj,
                                 "senha":senha,
                                 "confirma":confirma,
                                 "rua":rua,
                                 "numero":numero,
                                 "complemento":complemento,
                                 "bairro":bairro,
                                 "cidade":cidade,
                                 "estado":estado,
                                 "cep":cep,
                                 "ddd":ddd,
                                 "fone":fone,
                                 "codigo":codigo,
                                 "rg":rg,
                                 "timefutebol":timefutebol,
                                 "ids":ids}

                        dados = str(dados)
                        cod = (time.time() + random()).__str__()
                        hash = hashlib(cod).hexdigest()
                        self.execSqlu("insert_wad_temp",
                                      dados=dados,
                                      email=e,
                                      hash=hash)


                        site = getDadosSite(id_site=self.id_site,
                                            request=self.request)
                        link = ("%s/da_wad/%s,%s/validaCadastro?hash=%s"
                                            % (site["base_dinamico"],
                                               self.schema,
                                               self.id_site,
                                               hash))
                        msg = msg3 % {"link":link,
                                      "title":dadose["titulo"]}


                        email = Email()
                        email.enviarEmail(subject=msg12 % dadose["titulo"],
                                      to=e,
                                      fro=dadose["from_host"],
                                      text=msg,
                                      returnpath=dadose["return_path"],
                                      host=settings.SMTP_HOST,
                                      port=settings.SMTP_PORT,
                                      type="text/html")

                        res = {"type":"ok", "description":"sucesso", "id":"1"}

            conn.close()

        return res


    @dbconnectionapp
    def validaCadastro(self, hash):
        """
        """
        dadose = self._wad_data
        ok = False
        for i in self.execSql("select_cadastro_captcha",
                              hash=hash):

            conn = self._getConnection()
            if not conn:
                return "erro"

            # take care of this
            dados = eval(i["dados"])
            #dados["nome"] = u"Zé das Çoves".encode('utf-8')

            def isdate(dt):
                try:
                    dt = dtime.strptime(dt, "%d/%m/%Y")
                    dtime.strftime("%Y-%m-%d", dt)
                    ano = int(dtime.strftime("%Y", dt))
                    mes = int(dtime.strftime("%m", dt))
                    dia = int(dtime.strftime("%d", dt))
                    return cx_Oracle.Date(ano, mes, dia)
                except:
                    return None

            cursor = conn.cursor()

            pResult = cursor.var(cx_Oracle.NUMBER)
            p1 = cursor.var(cx_Oracle.STRING)
            p1.setvalue(0, dados["e"])
            cursor.callproc("wad.SP_EMAIL_EXIST", (p1, pResult))
            res = pResult.getvalue()
            if pResult.getvalue() > 0:
                return "Cadastro já efetuado"

            cursor.execute("SELECT wad.FN_LOGINSUGGEST(%s) FROM dual" % _quote(dados["e"]))
            login = cursor.fetchone()[0]

            pResult = cursor.var(cx_Oracle.STRING)
            p1 = cursor.var(cx_Oracle.STRING)
            p1.setvalue(0, login)
            p3 = cursor.var(cx_Oracle.STRING)
            p3.setvalue(0, dados["e"])
            p4 = cursor.var(cx_Oracle.STRING)
            p4.setvalue(0, dados["nome"])
            p5 = cursor.var(cx_Oracle.STRING)
            p5.setvalue(0, dados["apelido"])
            p6 = cursor.var(cx_Oracle.STRING)
            p6.setvalue(0, dados["sexo"])
            p9 = cursor.var(cx_Oracle.STRING)
            p9.setvalue(0, dados["cpf_cnpj"])
            p10 = cursor.var(cx_Oracle.STRING)
            p10.setvalue(0, "F")
            p12 = cursor.var(cx_Oracle.STRING)
            p12.setvalue(0, dados["rg"])
            p13 = cursor.var(cx_Oracle.STRING)
            p13.setvalue(0, dados["senha"])
            nascimento = isdate(dados["nascimento"])

            cursor.callproc("wad.SP_LOGIN_INSERT", (p1,
                                                    None,
                                                    p3,
                                                    p4,
                                                    p5,
                                                    p6,
                                                    None,
                                                    nascimento,
                                                    p9,
                                                    p10,
                                                    None,
                                                    p12,
                                                    p13,
                                                    0,
                                                    3,
                                                    pResult))

            if pResult.getvalue() > 0:

                if (dados and dados.has_key("timefutebol")
                                  and dados.get("timefutebol", None)):
                    p1 = cursor.var(cx_Oracle.STRING)
                    p1.setvalue(0, dados["e"])
                    p2 = cursor.var(cx_Oracle.STRING)
                    p2.setvalue(0, "attr_timefutebol")
                    p3 = cursor.var(cx_Oracle.STRING)
                    p3.setvalue(0, dados["timefutebol"])

                    cursor.callproc("wad.SP_LOGINATRIBUTO_INSERT",
                                    (p1, p2, p3, 4, pResult))

                p1 = cursor.var(cx_Oracle.STRING)
                p1.setvalue(0, dados["e"])
                p2 = cursor.var(cx_Oracle.NUMBER)
                p2.setvalue(0, dados["ddd"])
                p3 = cursor.var(cx_Oracle.NUMBER)
                p3.setvalue(0, dados["fone"])
                p6 = cursor.var(cx_Oracle.STRING)
                p6.setvalue(0, "55")

                cursor.callproc("wad.SP_TELEFONE_INSERT", (p1, p2, p3,
                                                           1, None, p6, None, 4, pResult))

                if pResult.getvalue() > 0:
                    p1 = cursor.var(cx_Oracle.STRING)
                    p1.setvalue(0, dados["e"])
                    p2 = cursor.var(cx_Oracle.STRING)
                    p2.setvalue(0, dados["rua"][:63])
                    p3 = cursor.var(cx_Oracle.NUMBER)
                    p3.setvalue(0, int( str(dados["numero"])[:10] ) )
                    p4 = cursor.var(cx_Oracle.STRING)
                    p4.setvalue(0, dados["complemento"][:31])
                    p5 = cursor.var(cx_Oracle.STRING)
                    p5.setvalue(0, dados["bairro"][:63])
                    p6 = cursor.var(cx_Oracle.STRING)
                    p6.setvalue(0, dados["cidade"][:63])
                    p7 = cursor.var(cx_Oracle.STRING)
                    p7.setvalue(0, dados["estado"][:31])
                    p8 = cursor.var(cx_Oracle.NUMBER)
                    p8.setvalue(0, int(str(dados["cep"])[:10])   )
                    p9 = cursor.var(cx_Oracle.STRING)
                    p9.setvalue(0, "Brasil")

                    cursor.callproc("wad.SP_ENDERECO_INSERT",
                                     (p1, p2, p3, p4, p5, p6, p7, p8, p9,
                                      1, None, 4, pResult))

                    if pResult.getvalue() > 0:
                        return msg13 % dadose["titulo"]

                    else:
                        return msg14

            conn.close()

        return "erro"


    @jsoncallback
    def votar(self, schema, i, voto):
        """
        sucess:
            1 - Voto calculado com sucesso
        error:
            1 - Usuario nao logado
            2 - Usuario ja votou
            3 - erro desconhecido
        """
        name_host = self._wad_data["site"]
        authc = None
        usuario = self._isSessionActive()
        voto = int(voto)
        if voto < 1 or voto > 5:
            voto = 1
        voto = voto/5.0
        if usuario:
            key = "voto%s%s" % (schema, i)
            ck = self.request.getCookie(key)
            if ck:
                res = {"type":"error",
                       "description":"Usuario ja votou",
                       "id":"2"}
            else:
                try:
                    portal = Portal(id_site=self.id_site,
                                    request=self.request)
                    portal._setVotacao(id_site=self.id_site,
                                       id_conteudo=i,
                                       schema=schema,
                                       voto=voto)
                    res = {"type":"ok",
                           "description":"Voto computado com sucesso",
                           "id":"1"}
                    expires = datetime.datetime.now() + datetime.timedelta(days=365)
                    self.request.setCookie(key,
                                           str(voto),
                                           host=name_host,
                                           expires=expires)
                except:
                    res = {"type":"error",
                           "description":"Erro desconhecido",
                           "id":"3"}

        else:
            res = {"type":"error",
                   "description":"Usuario nao autenticado",
                   "id":"1"}

        return res


    @dbconnectionapp
    @jsoncallback
    def comentar(self, schema, i, comentario, ip=None):
        """
        sucess:
            1 - Comentario adicionado com sucesso
            2 - comentario bloqueado
        error:
            1 - Usuario nao logado
            2 - Erro desconhecido
        """
        dados = self._wad_data
        ids = dados["id_servico"]

        authc = None
        usuario = self._isSessionActive()
        if usuario:

            try:
                email = usuario["email"]
                moderadoi = self.execSql("select_moderado",
                                        schemai=schema,
                                        schema=buffer(schema),
                                        id_conteudo=int(i)).next()
                moderado = decode(moderadoi["configuracao"])
                autorizado = False
                bloqueado = False

                autorizado = moderado.get("moderacao", False)
                autorizado = False if autorizado else True

                comentario = unquote(comentario)
                comentario = comentario[:301]

                id_comentario = self.execSql("select_id_comentario").next()["next"]
                self.execSqlu("insert_comentario",
                              id_comentario=int(id_comentario),
                              id_conteudo=int(i),
                              schema=schema,
                              autor=usuario["nome"],
                              email=usuario["email"],
                              comentario=comentario,
                              ip=self.request.getiphost(),
                              autorizado=autorizado)

                if not moderado.get("moderacao"):
                    self.execSqlu("update_conteudo_exportar",
                                  schema=schema,
                                  id_conteudo=int(i))

                else:
                    emails = moderado.get("email_moderacao", "")
                    if not emails:
                        emails = dados["return_path"]

                    self._enviarAprovacao(id_comentario=id_comentario,
                                          id_conteudo=i,
                                          id_aplicativo=moderadoi["id_aplicativo"],
                                          email=emails,
                                          comentario=comentario,
                                          autor=usuario["nome"],
                                          email_autor=usuario["email"])

                portal = Portal(id_site=self.id_site, request=self.request)
                portal._updateComentarioQtde(env_site=self.id_site,
                                             id_conteudo=i,
                                             schema=schema)

                if moderado.get("moderacao", None):
                    res = {"type":"ok",
                           "description":"Comentario bloqueado",
                           "id":"1"}
                else:
                    res = {"type":"ok",
                           "description":"Comentario adicionado com sucesso",
                           "id":"2"}
            except:
                res = {"type":"error",
                       "description":"Erro desconhecido",
                       "id":"2"}
        else:
            res = {"type":"error",
                   "description":"Usuario nao autenticado",
                   "id":"1"}

        return res


    def _enviarAprovacao(self, id_comentario, id_conteudo, id_aplicativo,
                               email, comentario, autor, email_autor):
        """
        """
        dados = self._wad_data
        ids = dados["id_servico"]
        subject = msg15 % dados["titulo"]

        site = getDadosSite(id_site=self.id_site,
                            request=self.request)

        link1 = (("%sportal/acaoComentario?"
                  "env_site=%s&acao=publicar&id_conteudo=%s&id_comentario=%s&id_aplicativo=%s")
                  % (site["url_adm"],
                     self.id_site,
                     id_conteudo,
                     id_comentario,
                     id_aplicativo))

        link2 = (("%sportal/acaoComentario?"
                  "env_site=%s&acao=bloquear&id_conteudo=%s&id_comentario=%s&id_aplicativo=%s")
                  % (site["url_adm"],
                     self.id_site,
                     id_conteudo,
                     id_comentario,
                     id_aplicativo))

        text = msg5 % (dados['titulo'],
                       autor,
                       email_autor,
                       comentario,
                       link1,
                       link2)

        for e in email.split(";"):

            if e:
                email = Email()
                email.enviarEmail(subject=subject,
                                  to=e,
                                  fro=settings.FROM_HOST,
                                  text=text,
                                  returnpath=settings.RETURN_PATH,
                                  host=settings.SMTP_HOST,
                                  port=settings.SMTP_PORT,
                                  type="text/plain")


    @jsoncallback
    def enviar(self, url, tipo, site, equipe, meu_nome, e, nome1, e1,
                     nome2=None, e2=None, nome3=None, e3=None,
                     nome4=None, e4=None):
        """
        error:
            1: servico nao encontrado
        """
        dados = self._wad_data
        email = Email()
        subject = msg7 % dados["titulo"]

        for nome, e in [(nome1, e1), (nome2, e2), (nome3, e3), (nome4, e4)]:
            if nome and e:
                mensagem = unicode(msg6, "latin1")
                mensagem = (mensagem % (unicode(nome, "latin1"),
                                    unicode(meu_nome, "latin1"),
                                    unicode(unquote(tipo), "latin1"),
                                    unicode(site, "latin1"),
                                    unicode(url, "latin1"),
                                    unicode(equipe, "latin1")))

                email.enviarEmail(subject=subject,
                                  to=e,
                                  fro=dados["from_host"],
                                  text=mensagem.encode("latin1"),
                                  returnpath=dados["return_path"],
                                  host=settings.SMTP_HOST,
                                  port=settings.SMTP_PORT,
                                  type="text/plain")


        return {'ok':'Mensagem enviada'}


    @dbconnectionapp
    @jsoncallback
    def corrigir(self, url, nome, e, correcao, schema):
        """
        """
        dados = self._wad_data
        if nome and e:
            mensagem = unicode(msg8, "latin1")
            mensagem = mensagem % (unicode(nome, "latin1"),
                                   unicode(e, "latin1"),
                                   unicode(url, "latin1"),
                                   unicode(correcao, "latin1"))

            subject = msg9
            email = Email()
            emails = [i for i in dados["return_path"].split(";") if i.strip()]
            
            for em in emails:
                email.enviarEmail(subject=subject,
                                  to=em,
                                  fro=settings.FROM_HOST,
                                  text=mensagem.encode("latin1"),
                                  returnpath=settings.RETURN_PATH,
                                  host=settings.SMTP_HOST,
                                  port=settings.SMTP_PORT,
                                  type="text/plain")

        return {'ok':'Mensagem enviada'}


    @dbconnectionapp
    @jsoncallback
    def denuncia(self, id_comentario, i, denuncia, url, schema):
        """
        error:
            2: nao logado
            3: login nao encontrado
        """
        dados = self._wad_data
        usuario = self._isSessionActive()
        if usuario:

            conn = self._getConnection()
            cursor = conn.cursor()

            email = usuario["email"]

            pIdExterno = cursor.var(cx_Oracle.NUMBER)
            pLogin = cursor.var(cx_Oracle.STRING)
            pEmail = cursor.var(cx_Oracle.STRING)
            pNome = cursor.var(cx_Oracle.STRING)
            pApelido = cursor.var(cx_Oracle.STRING)
            pSexo = cursor.var(cx_Oracle.STRING)
            pCancelado = cursor.var(cx_Oracle.NUMBER)
            pDt_Expiracao = cursor.var(cx_Oracle.DATETIME)
            pDt_Nascimento = cursor.var(cx_Oracle.DATETIME)
            pCPF_CNPJ = cursor.var(cx_Oracle.STRING)
            pPessoa = cursor.var(cx_Oracle.STRING)
            pContato = cursor.var(cx_Oracle.STRING)
            pRg = cursor.var(cx_Oracle.STRING)
            pCtrl_Origem = cursor.var(cx_Oracle.STRING)
            pCtrl_BloqUpdate = cursor.var(cx_Oracle.NUMBER)
            pCtrl_Dt_Insert = cursor.var(cx_Oracle.DATETIME)
            pCtrl_Dt_UltimoAcesso = cursor.var(cx_Oracle.DATETIME)
            pCtrl_Dt_Ultimoupdate = cursor.var(cx_Oracle.DATETIME)
            pCtrl_CodigoSGVD = cursor.var(cx_Oracle.NUMBER)
            pCtrl_AssinanteJornal = cursor.var(cx_Oracle.NUMBER)
            pCtrl_AssinanteCodDistrib = cursor.var(cx_Oracle.NUMBER)
            pCtrl_LoginMasterId = cursor.var(cx_Oracle.NUMBER)
            pCtrl_LoginCortesia = cursor.var(cx_Oracle.NUMBER)
            pCtrl_LoginClassificacao = cursor.var(cx_Oracle.NUMBER)
            pResult = cursor.var(cx_Oracle.NUMBER)

            p1 = cursor.var(cx_Oracle.STRING)
            p1.setvalue(0, email)


            cursor.callproc("wad.SP_LOGIN_GETDATA",
                            (p1,
                             pIdExterno,
                             pLogin,
                             pEmail,
                             pNome,
                             pApelido,
                             pSexo,
                             pCancelado,
                             pDt_Expiracao,
                             pDt_Nascimento,
                             pCPF_CNPJ,
                             pPessoa,
                             pContato,
                             pRg,
                             pCtrl_Origem,
                             pCtrl_BloqUpdate,
                             pCtrl_Dt_Insert,
                             pCtrl_Dt_UltimoAcesso,
                             pCtrl_Dt_Ultimoupdate,
                             pCtrl_CodigoSGVD,
                             pCtrl_AssinanteJornal,
                             pCtrl_AssinanteCodDistrib,
                             pCtrl_LoginMasterId,
                             pCtrl_LoginCortesia,
                             pCtrl_LoginClassificacao,
                             pResult))

            if pResult.getvalue() > 0:

                nome = pNome.getvalue()
                cpf = pCPF_CNPJ.getvalue() or ""
                rg = pRg.getvalue() or ""

                sql = ("SELECT * FROM table(wad.FN_TELEFONE_GETDATA(%s))" % _quote(email))
                cursor.execute(sql)
                telefone = ""
                for j in cursor.fetchall(): # DDD, Fone, Tipo, Ramal, DDI, Codigo_Externo, Ctrl_Origem, Ctrl_BloqUpdate
                    telefone += "(%s) %s " % (j[0], j[1])

                sql = ("SELECT * FROM table(wad.FN_ENDERECO_GETDATA(%s))" % _quote(email))
                cursor.execute(sql)
                endereco = ""

                def isnotNone(inp):
                    if not inp:
                        return ""
                    return str(inp)

                # Endereco_Id, Rua, Numero Complemento, Bairro, 
                # Cidade, Estado, CEP, Pais, Tipo, Codigo_Externo, 
                # Ctrl_Origem, Ctrl_BloqUpdate, Ctrl_UltimoUpdate
                for j in cursor.fetchall():
                    rua = isnotNone(j[1]) + ", " + isnotNone(j[2])
                    bairro = isnotNone(j[4])
                    cidade = isnotNone(j[5])
                    estado = isnotNone(j[6])
                    cep = isnotNone(j[7])
                    pais = isnotNone(j[8])
                    endereco += ("Rua: %s\nBairro: %s\n"
                                 "Cidade: %s\nEstado: %s\n"
                                 "Cep: %s\nPais: %s\n") % (rua, bairro, cidade,
                                                           estado, cep, pais)

            else:
                conn.close()
                return {"error":"login nao encontrado",
                               "id":3}

            portal = Portal(id_site=self.id_site,
                            request=self.request)

            portal._mkdbg(env_site=self.id_site) 
            comentario = self.execSql("select_comentario",
                                      app=buffer(schema),
                                      id_comentario=int(id_comentario)).next()


            mensagem = unicode(msg10, "latin1")
            mensagem = mensagem % (unicode(nome, "latin1"),
                                   unicode(cpf, "latin1"),
                                   unicode(rg, "latin1"),
                                   unicode(email, "latin1"),
                                   unicode(telefone, "latin1"),
                                   unicode(endereco, "latin1"),
                                   unicode(denuncia, "latin1"),
                                   unicode(url, "latin1"),
                                   unicode(comentario["autor"], "latin1"),
                                   unicode(comentario["email"], "latin1"),
                                   unicode(comentario["comentario"], "latin1"))

            subject = unicode(msg11, "latin1")
            moderadoi = self.execSql("select_moderado",
                                     schemai=schema,
                                     schema=buffer(schema),
                                     id_conteudo=int(i)).next()

            moderado = decode(moderadoi["configuracao"])
            email_moderado = [i for i in 
                              moderado.get("email_moderacao", "").split(";") 
                                if i.strip()]
            if not email_moderado:
                email_moderado = [i for i in dados["return_path"].split(";") 
                                            if i.strip()]

            for em in email_moderado:

                email = Email()
                email.enviarEmail(subject=subject,
                                  to=em,
                                  fro=settings.FROM_HOST,
                                  text=mensagem.encode("latin1"),
                                  returnpath=settings.RETURN_PATH,
                                  host=settings.SMTP_HOST,
                                  port=settings.SMTP_PORT,
                                  type="text/plain")

            return {"ok":"Mensagem enviada", "id":1}
        else:
            return {"error":"nao logado", "id":2}


    @dbconnectionapp
    def captcha(self):
        """
        """
        dados = self._wad_data
        name_host = dados["site"]
        dados = self._wad_data
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
                      solucao=solucao)
        self.request.setHeader("Content-type",
                               "image/jpeg")

        return source
    
    @jsoncallback
    def atualizar(self, matricula, senha_velha, email, senha_nova, apelido, 
                  primeiro_nome, ultimo_nome, sexo, data_nasc, cpf, rg, cep, 
                  estado, cidade, bairro, endereco, numero, complemento, 
                  telefone, ddd):
        """
            Atualiza um cadastro a partir de uma matricula e senha como login
        """
        senha_velha = senha_velha.decode("latin1").encode("utf-8")
        email = email.decode("latin1").encode("utf-8")
        senha_nova = senha_nova.decode("latin1").encode("utf-8")
        apelido = apelido.decode("latin1").encode("utf-8")
        primeiro_nome = primeiro_nome.decode("latin1").encode("utf-8")
        ultimo_nome = ultimo_nome.decode("latin1").encode("utf-8")
        estado = estado.decode("latin1").encode("utf-8")
        cidade = cidade.decode("latin1").encode("utf-8")
        bairro = bairro.decode("latin1").encode("utf-8")
        endereco = endereco.decode("latin1").encode("utf-8")
        dadose = self._wad_data
        ok = False
        conn = self._getConnection()
        if not conn:
            return "erro"
        #checar se está logado
        dados = {}
        dados["e"] = email #ou matricula???
        dados["apelido"] = apelido
        dados["nome"] = nome + ultimo_nome
        dados["sexo"] = sexo
        dados["cpf_cnpj"] = cpf
        dados["rg"] = rg
        dados["senha"] = senha_nova
        dados["nascimento"] = nascimento
        dados["estado"] = estado
        dados["cidade"] = cidade
        dados["bairro"] = bairro
        dados["endereco"] = endereco
        dados["numero"] = numero
        dados["complemento"] = complemento
        dados["telefone"] = telefone
        dados["ddd"] = ddd

        # take care of this
        #dados = eval(i["dados"])
        #dados["nome"] = u"Zé das Çoves".encode('utf-8')

        def isdate(dt):
            try:
                dt = dtime.strptime(dt, "%d/%m/%Y")
                dtime.strftime("%Y-%m-%d", dt)
                ano = int(dtime.strftime("%Y", dt))
                mes = int(dtime.strftime("%m", dt))
                dia = int(dtime.strftime("%d", dt))
                return cx_Oracle.Date(ano, mes, dia)
            except:
                return None

        cursor = conn.cursor()

        pResult = cursor.var(cx_Oracle.NUMBER)
        p1 = cursor.var(cx_Oracle.STRING)
        p1.setvalue(0, dados["e"])
        cursor.callproc("wad.SP_EMAIL_EXIST", (p1, pResult))
        res = pResult.getvalue()
        if pResult.getvalue() == 0:
            return "Cadastro inexistente"

        cursor.execute("SELECT wad.FN_LOGINSUGGEST(%s) FROM dual" % _quote(dados["e"]))
        login = cursor.fetchone()[0]

        pResult = cursor.var(cx_Oracle.STRING)
        p1 = cursor.var(cx_Oracle.STRING)
        p1.setvalue(0, login)
        p3 = cursor.var(cx_Oracle.STRING)
        p3.setvalue(0, dados["e"])
        p4 = cursor.var(cx_Oracle.STRING)
        p4.setvalue(0, dados["nome"])
        p5 = cursor.var(cx_Oracle.STRING)
        p5.setvalue(0, dados["apelido"])
        p6 = cursor.var(cx_Oracle.STRING)
        p6.setvalue(0, dados["sexo"])
        p9 = cursor.var(cx_Oracle.STRING)
        p9.setvalue(0, dados["cpf_cnpj"])
        p10 = cursor.var(cx_Oracle.STRING)
        p10.setvalue(0, "F")
        p12 = cursor.var(cx_Oracle.STRING)
        p12.setvalue(0, dados["rg"])
        p13 = cursor.var(cx_Oracle.STRING)
        p13.setvalue(0, dados["senha"])
        nascimento = isdate(dados["nascimento"])

        cursor.callproc("wad.SP_LOGIN_UPDATE", (p1,         #LoginEmail
                                                None,       #Email 64
                                                p4,         #Nome 64
                                                p5,         #Apelido 32
                                                p6,         #Sexo
                                                nascimento, #Nascimento
                                                p9,         #CPF
                                                None,       #CNPJ
                                                p10,        #Pessoa Jur(F ou J)
                                                p12,        #RG
                                                pResult))      #Result

        if pResult.getvalue() > 0:

            p1 = cursor.var(cx_Oracle.STRING)
            p1.setvalue(0, dados["e"])#???
            p2 = cursor.var(cx_Oracle.NUMBER)
            p2.setvalue(0, dados["ddd"])
            p3 = cursor.var(cx_Oracle.NUMBER)
            p3.setvalue(0, dados["telefone"])
            p6 = cursor.var(cx_Oracle.STRING)
            p6.setvalue(0, "55")
            #Executar um remove antes????
            cursor.callproc("wad.SP_TELEFONE_INSERT",  #Não tem update????? 
                            (p1,        #
                             p2,        #
                             p3,        #
                             1,         #
                             None,      #
                             p6,        #
                             None,      #
                             4,         #
                             pResult))  #

            if pResult.getvalue() > 0:
                p1 = cursor.var(cx_Oracle.STRING)
                p1.setvalue(0, dados["e"])
                p2 = cursor.var(cx_Oracle.STRING)
                p2.setvalue(0, dados["rua"][:63])
                p3 = cursor.var(cx_Oracle.NUMBER)
                p3.setvalue(0, int( str(dados["numero"])[:10] ) )
                p4 = cursor.var(cx_Oracle.STRING)
                p4.setvalue(0, dados["complemento"][:31])
                p5 = cursor.var(cx_Oracle.STRING)
                p5.setvalue(0, dados["bairro"][:63])
                p6 = cursor.var(cx_Oracle.STRING)
                p6.setvalue(0, dados["cidade"][:63])
                p7 = cursor.var(cx_Oracle.STRING)
                p7.setvalue(0, dados["estado"][:31])
                p8 = cursor.var(cx_Oracle.NUMBER)
                p8.setvalue(0, int(str(dados["cep"])[:10])   )
                p9 = cursor.var(cx_Oracle.STRING)
                p9.setvalue(0, "Brasil")
                pEnd = cursor.var(cx_Oracle.NUMBER)
                cursor.execute("SELECT * FROM table(wad.FN_ENDERECO_GETDATA(%s))" % _quote(dados["e"]))
                pEnd.setvalue(0, cursor.fetchall()[0][0])

                cursor.callproc("wad.SP_ENDERECO_UPDATE",
                                 (p1,   #LoginEmail
                                  pEnd,   #Endereco_Id -> FN_ENDERECO_GETDATA
                                  p2,   #Rua
                                  p3,   #Numero
                                  p4,   #Complemento
                                  p5,   #Bairro
                                  p6,   #Cidade
                                  p7,   #Estado
                                  p8,   #CEP
                                  p9,   #Pais
                                  1,    #Tipo
                                  4,    #Codigo_Externo
                                  pResult))#result

                if pResult.getvalue() > 0:
                    return msg13 % dadose["titulo"]

                else:
                    return msg14

        conn.close()

        return "erro"
        

    def conectarRADIUS(self, usuario="", senha=""):
        """
            Returns the login status in a RADIUS request
        """
        import pyrad.packet
        from pyrad.client import Client
        from pyrad.dictionary import Dictionary
        srv = Client(server="200.188.188.18", secret="centraluai",
                     dict=Dictionary("", "dictionary.acc"), authport=1665)

        req = srv.CreateAuthPacket(code=pyrad.packet.AccessRequest,
                                   User_Name=usuario, NAS_Identifier="localhost")
        req["Password"]=req.PwCrypt(senha)

        reply=srv.SendPacket(req)
        login = False

        if reply.code == pyrad.packet.AccessAccept:
            login = True
        else:
            login = False

        if login:
            dnow, dtpas = self._gdt()
            id = self._psid()

            expires = datetime.datetime.now() + datetime.timedelta(hours=1)
            nome = unicode(usuario, "utf-8").encode('latin1')

            self._sessionAdd(id_session=id,
                             nome=nome,
                             email=nome,
                             datahorae=dtpas,
                             extr="")

#            nome = quote(nome)
            valor = "%s|%s|%s" % (id, nome, nome)
            name_host = self._wad_data["site"]

            self.request.setCookie(COOKIE_NAME,
                                   valor,
                                   expires="",
                                   host=name_host)
            return {"type":"ok",
                    "description":"Usuario autenticado com sucesso",
                    "id":"1"}
        else:
            return {"type":"error", 
                    "description":"Usuario ou senha incorreta",
                    "id":"2"}
        
    @dbconnectionapp
    @jsoncallback
    def autenticarCentral(self, e, senha, cod=None, host=None):
        """
        erros:
          1 - sem conexao com banco
          2 - usuario ou senha incorreta
          3 - servico inexistente
          4 - erro desconhecido
          5 - usuario nao existe
        sucesso:
          1 - usuario autenticado com sucesso
        """
        dados = self._wad_data
        ids = dados["id_servico"]
        email = e[:64]
        senha = senha[:44]
        authc = None

        res = {"type":"error", "description":"", "id":"1"}
        try:
            conn = self._getConnection()
        except:
            return res
        if not conn:
            res = {"type":"error",
                   "description":"Sem conexao com banco de dados",
                   "id":"1"}

        else:

            cursor = conn.cursor()
            pResult = cursor.var(cx_Oracle.NUMBER)
            if email.count("@uai.com.br"):
                email = email.replace("@uai.com.br", "")
            p1 = cursor.var(cx_Oracle.STRING)
            p1.setvalue(0, email)
            p2 = cursor.var(cx_Oracle.STRING)
            p2.setvalue(0, senha)
            p3 = cursor.var(cx_Oracle.NUMBER)
            p3.setvalue(0, ids)
            p4 = cursor.var(cx_Oracle.NUMBER)
            p4.setvalue(0, 1)
            arq = ""
            if e.isdigit():
                p1.setvalue(0,  email)
                cursor.callproc("wad.SP_LOGIN_AUTHENTIC_ASSJORNAL", (p1, p2, p4, pResult, ids))
                res = pResult.getvalue()
                if res <= 0:
                    res = {"type":"error",
                           "description":"Matrícula ou senha incorreta",
                           "id":"2"}
                    cursor.close()
                    conn.close()
                    return res
                else:
                    arq = "Matricula: " + e
            else:
                cursor.callproc("wad.SP_LOGIN_AUTHENTIC", (p1, p2, pResult, ids))
                res = pResult.getvalue()
                if res <= 0:
                    res = {"type":"error",
                           "description":"Usuário ou senha incorreta!",
                           "id":"2"}
                    cursor.close()
                    conn.close()
                    return res
                else:
                    cursor.execute("SELECT * FROM email WHERE co_email = '{0}'".format(email))
                    try:
                        if cursor.fetchall()[0][1] == "S":
                            arq = "Login: " + email
                        else:
                            res = {"type":"error",
                                   "description":"Usuário ou senha incorreta.",
                                   "id":"7"}
                            cursor.close()
                            conn.close()
                            return res
                    except IndexError:
                        res = {"type":"error",
                               "description":"Usuário ou senha incorreta.",
                               "id":"7"}
                        cursor.close()
                        conn.close()
                        return res

            pIdExterno = cursor.var(cx_Oracle.NUMBER)
            pLogin = cursor.var(cx_Oracle.STRING)
            pEmail = cursor.var(cx_Oracle.STRING)
            pNome = cursor.var(cx_Oracle.STRING)
            pApelido = cursor.var(cx_Oracle.STRING)
            pSexo = cursor.var(cx_Oracle.STRING)
            pCancelado = cursor.var(cx_Oracle.NUMBER)
            pDt_Expiracao = cursor.var(cx_Oracle.DATETIME)
            pDt_Nascimento = cursor.var(cx_Oracle.DATETIME)
            pCPF_CNPJ = cursor.var(cx_Oracle.STRING)
            pPessoa = cursor.var(cx_Oracle.STRING)
            pContato = cursor.var(cx_Oracle.STRING)
            pRg = cursor.var(cx_Oracle.STRING)
            pCtrl_Origem = cursor.var(cx_Oracle.STRING)
            pCtrl_BloqUpdate = cursor.var(cx_Oracle.NUMBER)
            pCtrl_Dt_Insert = cursor.var(cx_Oracle.DATETIME)
            pCtrl_Dt_UltimoAcesso = cursor.var(cx_Oracle.DATETIME)
            pCtrl_Dt_Ultimoupdate = cursor.var(cx_Oracle.DATETIME)
            pCtrl_CodigoSGVD = cursor.var(cx_Oracle.NUMBER)
            pCtrl_AssinanteJornal = cursor.var(cx_Oracle.NUMBER)
            pCtrl_AssinanteCodDistrib = cursor.var(cx_Oracle.NUMBER)
            pCtrl_LoginMasterId = cursor.var(cx_Oracle.NUMBER)
            pCtrl_LoginCortesia = cursor.var(cx_Oracle.NUMBER)
            pCtrl_LoginClassificacao = cursor.var(cx_Oracle.NUMBER)
            pResult = cursor.var(cx_Oracle.NUMBER)

            p1 = cursor.var(cx_Oracle.STRING)
            if e.isdigit():
                p1.setvalue(0, "em" + email)
            else:
                p1.setvalue(0, email)

            cursor.callproc("wad.SP_LOGIN_GETDATA",
                            (p1,
                             pIdExterno,
                             pLogin,
                             pEmail,
                             pNome,
                             pApelido,
                             pSexo,
                             pCancelado,
                             pDt_Expiracao,
                             pDt_Nascimento,
                             pCPF_CNPJ,
                             pPessoa,
                             pContato,
                             pRg,
                             pCtrl_Origem,
                             pCtrl_BloqUpdate,
                             pCtrl_Dt_Insert,
                             pCtrl_Dt_UltimoAcesso,
                             pCtrl_Dt_Ultimoupdate,
                             pCtrl_CodigoSGVD,
                             pCtrl_AssinanteJornal,
                             pCtrl_AssinanteCodDistrib,
                             pCtrl_LoginMasterId,
                             pCtrl_LoginCortesia,
                             pCtrl_LoginClassificacao,
                             pResult))

            if pResult.getvalue() > 0:

                p1 = cursor.var(cx_Oracle.STRING)
                p1.setvalue(0, email)
                p2 = cursor.var(cx_Oracle.NUMBER)
                p2.setvalue(0, ids)

                dnow, dtpas = self._gdt()
                id = self._psid()
                nome = pNome.getvalue()
                sexo = pSexo.getvalue()
                rg = pRg.getvalue()
                extra = encode({"nome":nome, "sexo":sexo, "rg":rg})

                expires = datetime.datetime.now() + datetime.timedelta(hours=1)
                nome = unicode(nome, "utf-8").encode('latin1')

                self._sessionAdd(id_session=id,
                                 nome=nome,
                                 email=email,
                                 datahorae=dtpas,
                                 extr=extra)

                nome = quote(nome)
                valor = "%s|%s|%s|%s" % (id, nome, email, arq)
                name_host = dados["site"]

                self.request.setCookie(COOKIE_NAME,
                                       valor,
                                       expires="",
                                       host=name_host)
                res = {"type":"ok",
                       "description":"Usuario autenticado com sucesso",
                       "id":"1"}
            else:
                res = {"type":"error",
                       "description":"erro desconhecido",
                       "id":"4"}

            cursor.close()

        if conn:
            conn.close()

        return res


