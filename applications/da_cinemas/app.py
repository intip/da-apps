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
from publica.utils.BeautifulSoup import BeautifulSoup
from time import time, strftime, strptime
from publica.core.portal import Portal
from publica.admin.error import UserError
from publica.utils.json import encode
from publica.utils.decorators import serialize, dbconnectionapp,\
                                     Permission, logportal
from publica.admin.appportal import PortalUtils
from publica.admin.interfaces import BaseApp


from publica import settings
from public import Public
from adm import Adm

haslist = True
haslink = True
title = "DA - Cinemas"
meta_type = "da_cinemas"


class App(BaseApp, PortalUtils, Adm, Public):
    """
    """
    title = title
    meta_type = meta_type
    haslist = haslist
    haslink = haslink

    def __init__(self, id_site, schema=None, request=None):
        """
        """
        self.id_site = id_site
        self.schema = schema
        self.request = request

    @dbconnectionapp
    def _install(self, title, redimensionamento,
                       dimenx=0, dimeny=0, auth_schema=None, auth_type=None,
                       rss_titulo=None, rss_link=None, rss_descricao=None,
                       rss_idioma=None, rss_categoria=None, rss_copyright=None,
                       rss_imagem_titulo=None, rss_imagem_link=None,
                       rss_imagem=None):
        """Adiciona uma instancia do produto
        """
        nid = str(time()).replace(".", "")
        if not self.schema:
            self.schema = "%s_%s" % (meta_type, nid)
        self.execSqlu("structure")
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        user_dinamic = portal._getUserDinamic(id_site=self.id_site)
        if user_dinamic:
            self.execSqlu("permissions",
                          user=buffer(user_dinamic))

        if settings.USER_PERMISSION:
            for u in settings.USER_PERMISSION:
                self.execSqlu("permissions_admin",
                              user=buffer(u))

        rss = {"titulo": rss_titulo,
               "link": rss_link,
               "descricao": rss_descricao,
               "idioma": rss_idioma,
               "categoria": rss_categoria,
               "copyright": rss_copyright,
               "imagem_titulo": rss_imagem_titulo,
               "imagem_link": rss_imagem_link,
               "rss_imagem": rss_imagem}

        try:
            thumbx = int(thumbx)
            thumby = int(thumby)
        except Exception:
            thumbx = 100
            thumby = 100

        if redimensionamento != "original":
            try:
                dimenx = int(dimenx)
                dimeny = int(dimeny)
            except Exception:
                dimenx = ""
                dimeny = ""

        return {"rss": rss,
                "redimensionamento":redimensionamento,
                "thumbx":thumbx,
                "auth_schema":auth_schema,
                "auth_type":auth_type,
                "thumby":thumby,
                "dimeny":dimeny,
                "dimenx":dimenx}

    @dbconnectionapp
    @serialize
    @Permission("ADM APP")
    def editApp(self, title,
                       redimensionamento, auth_schema=None, auth_type=None, 
                       dimenx=0, dimeny=0,rss_titulo=None, rss_link=None, rss_descricao=None,
                       rss_idioma=None, rss_categoria=None, rss_copyright=None,
                       rss_imagem_titulo=None, rss_imagem_link=None,
                       rss_imagem=None):
        """Edita os atributos da instancia
        """
        rss = {"titulo": rss_titulo,
               "link": rss_link,
               "descricao": rss_descricao,
               "idioma": rss_idioma,
               "categoria": rss_categoria,
               "copyright": rss_copyright,
               "imagem_titulo": rss_imagem_titulo,
               "imagem_link": rss_imagem_link,
               "rss_imagem": rss_imagem}

        try:
            thumbx = int(thumbx)
            thumby = int(thumby)
        except Exception:
            thumbx = 100
            thumby = 100

        if redimensionamento != "original":
            try:
                dimenx = int(dimenx)
                dimeny = int(dimeny)
            except Exception:
                dimenx = ""
                dimeny = ""

        dados = {"rss": rss,
                "redimensionamento":redimensionamento,
                "thumbx":thumbx,
                "thumby":thumby,
                "dimeny":dimeny,
                "auth_schema":auth_schema,
                "auth_type":auth_type,
                "dimenx":dimenx}

        portal = Portal(id_site=self.id_site, request=self.request)
        portal._editApp(env_site=self.id_site,
                        schema=self.schema,
                        titulo=title,
                        dados=dados)
        user_dinamic = portal._getUserDinamic(id_site=self.id_site)
        if user_dinamic:
            self.execSqlu("permissions",
                          user=buffer(user_dinamic))

        if settings.USER_PERMISSION:
            for u in settings.USER_PERMISSION:
                self.execSqlu("permissions_admin",
                              user=buffer(u))

        return "Aplicativo configurado com sucesso"

    @staticmethod
    def retornarWidgets():
        """
            Método padrão que retorna a informação dos widgets que a aplicação utiliza
        """
        return ({"action": "viewd",
                 "img": "/imgs/preview.gif",
                 "titulo": "Preview",
                 "url": "",
                 "target": ""},
                {"action": "viewe",
                 "img": "/imgs/previewe.gif",
                 "titulo": "Publicado",
                 "url": "",
                 "target": ""},
                {"action": "view",
                 "img": "/imgs/previewe.gif",
                 "titulo": "Sessão",
                 "url": "sessao.env",
                 "target": "listagem"},)

    @dbconnectionapp
    def _verifyStatusContent(self, id_conteudo):
        """
            Método padrão interno de verificação do status de um conteúdo da aplicação
        """
        for i in self.execSql("select_status_cinema",
                              id_conteudo=int(id_conteudo)):
            return i["publicado"]

    @dbconnectionapp
    def _setDados(self, id_conteudo):
        """
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)

        for i in self.execSql("select_cinema_dados", id_conteudo=int(id_conteudo)):

            dados = {"id_conteudo": i["id_conteudo"],
                     "nome": i["titulo"],
                     "precos": i["precos"],
                     "fotos": [],
                     "salas": []}

            for j in self.execSql("select_fotos_conteudo", id_conteudo=int(id_conteudo)):
                dados["fotos"].append({"arquivo": j["arquivo"]})

            for j in self.execSql("select_salas",
                                  id_conteudo=int(id_conteudo)):
                dados["salas"].append(j)

            url = portal.getUrlByApp(env_site=self.id_site,
                                     schema=self.schema,
                                     id_conteudo=id_conteudo,
                                     exportar=1,
                                     admin=1,
                                     mkattr=1)

            return {"nome": i["titulo"],
                    "meta_type": self.meta_type,
                    "id_conteudo": id_conteudo,
                    "publicado_em": i["publicado_em"],
                    "expira_em": i["expira_em"],
                    "atualizado_em": i["atualizado_em"],
                    "publicado": True if i["publicado"] else False,
                    "url": url,
                    "dados": dados}

        return {}

    @dbconnectionapp
    def _getTitleDados(self, id_pk):
        """
            Método padrão para retornar o título de um conteúdo para o portal,
            necessária em algumas ações internas do Publica
        """
        for i in self.execSql("select_nome_cinema",
                              id_conteudo=int(id_pk)):
            return {"title": i["titulo"]}

    @dbconnectionapp
    def _getDublinCore(self, id_pk):
        """
            Método padrão para a configuração das meta-tags de uma página
            interna de um determinado conteúdo
        """
        dados = {"title": "",
                 "created": "",
                 "modified": "",
                 "description": "",
                 "keywords": ""}

        for i in self.execSql("select_cinema",
                              id_conteudo=int(id_pk)):

            portal = Portal(id_site=self.id_site,
                            request=self.request)

            dados["title"] = i["titulo"]
            dados["created"] = i["publicado_em"]
            dados["modified"] = i["atualizado_em"]

        return dados

    @dbconnectionapp
    def _getListContentRef(self):
        """
            Método padrão para retornar as referências de um conteúdo a ser copiado em folders
        """
        for i in self.execSql("select_dados"):
            serialized = self._setDados(i["id_conteudo"])
            i["serialized"] = serialized
            yield i

    @dbconnectionapp
    def _getListContentRef(self):
        """
        """
        for i in self.execSql("select_cinema"):
            serialized = self._setDados(i["id_conteudo"])
            i["serialized"] = serialized
            yield i

    @dbconnectionapp
    @serialize
    @Permission("ADM SITE")
    def copyFiles2Temp(self, id_pk, id_site=None):
        """
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)

        fotos = self._getFotosSite(id_conteudo=id_pk)

        for foto in fotos:
            if foto["arquivo"]:
                portal._copyFile2Temp(arq=foto["arquivo"],
                                      id_site=id_site)

        return "Arquivos copiados com sucesso!"

    @dbconnectionapp
    @logportal
    @Permission("PERM APP")
    def delConteudo(self, id_conteudo):
        """
        """
        nome = ""
        for i in self.execSql("select_cinema",
                              id_conteudo=int(id_conteudo)):
            nome = i["titulo"]

        self.logmsg = "Cinema '%s' deletado" % nome
        self.execSqlu("delete_cinema",
                      id_conteudo=int(id_conteudo))
