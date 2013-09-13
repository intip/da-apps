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
import urllib2
import xml.etree.ElementTree as ET
from time import time, strftime, strptime
from publica.core.portal import Portal
from publica.admin.error import UserError
from publica.utils.decorators import serialize, dbconnectionapp, \
                                     Permission, permissioncron, logportal
from publica.admin.appportal import PortalUtils
from publica.admin.interfaces import BaseApp
from publica import settings
from site import Site
from adm import Adm

haslist = True
haslink = True
meta_type = "da_dzai"
title = "DA - Dzai"


class App(Adm, Site, PortalUtils, BaseApp):
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
    def _install(self, title, url, id_usuario, hash, id_pagina=None,
                       fast_path=None, fast_origem=None, fast_portal=None,
                       rss_titulo=None, rss_link=None, rss_descricao=None,
                       rss_idioma=None, rss_categoria=None, rss_copyright=None,
                       rss_imagem_titulo=None, rss_imagem_link=None,
                       rss_imagem=None):
        """Adiciona uma instancia do produto
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)

        if not portal._getTreeAppByHash(env_site=self.id_site,
                                        hash=hash):
            raise UserError("O hash especificado n&atilde;o foi encontrado.")

        nid = str(time()).replace(".", "")
        if not self.schema:
            self.schema = "%s_%s" % (meta_type, nid)
        self.execSqlu("structure")

        user_dinamic = portal._getUserDinamic(id_site=self.id_site)
        if user_dinamic:
            self.execSqlu("permissions",
                          user=buffer(user_dinamic))

        if settings.USER_PERMISSION:
            for u in settings.USER_PERMISSION:
                self.execSqlu("permissions_admin",
                              user=buffer(u))

        if fast_path:
            if not fast_path.endswith("/"):
                fast_path += "/"

        try:
            id_pagina = int(id_pagina)
        except:
            id_pagina = None

        rss = {"titulo":rss_titulo,
               "link":rss_link,
               "descricao":rss_descricao,
               "idioma":rss_idioma,
               "categoria":rss_categoria,
               "copyright":rss_copyright,
               "imagem_titulo":rss_imagem_titulo,
               "imagem_link":rss_imagem_link,
               "rss_imagem":rss_imagem}

        return {"rss":rss,
                "url":url,
                "id_usuario":id_usuario,
                "hash":hash,
                "id_pagina":id_pagina,
                "fast_path":fast_path,
                "fast_origem":fast_origem,
                "fast_portal":fast_portal}


    @dbconnectionapp
    @serialize
    @Permission("ADM APP")
    def editApp(self, title, url, id_usuario, h, id_pagina=None,
                      fast_path=None, fast_origem=None, fast_portal=None,
                      rss_titulo=None, rss_link=None, rss_descricao=None,
                      rss_idioma=None, rss_categoria=None, rss_copyright=None,
                      rss_imagem_titulo=None, rss_imagem_link=None,
                      rss_imagem=None, delvideo=None):
        """Edita os atributos da instancia
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)
 
        if not portal._getTreeAppByHash(env_site=self.id_site,
                                        hash=h):
            raise UserError("O hash especificado n&atilde;o foi encontrado.")

        user_dinamic = portal._getUserDinamic(id_site=self.id_site)
        if user_dinamic:
            self.execSqlu("permissions",
                          user=buffer(user_dinamic))

        if settings.USER_PERMISSION:
            for u in settings.USER_PERMISSION:
                self.execSqlu("permissions_admin",
                              user=buffer(u))

        if fast_path:
            if not fast_path.endswith("/"):
                fast_path += "/"

        try:
            id_pagina = int(id_pagina)
        except:
            id_pagina = None


        rss = {"titulo":rss_titulo,
               "link":rss_link,
               "descricao":rss_descricao,
               "idioma":rss_idioma,
               "categoria":rss_categoria,
               "copyright":rss_copyright,
               "imagem_titulo":rss_imagem_titulo,
               "imagem_link":rss_imagem_link,
               "rss_imagem":rss_imagem}

        dados = {"rss":rss,
                 "url":url,
                 "id_usuario":id_usuario,
                 "hash":h,
                 "id_pagina":id_pagina,
                 "fast_path":fast_path,
                 "fast_origem":fast_origem,
                 "fast_portal":fast_portal}

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
        try:
            self.execSqlu("create_rule")
        except:
            pass

        if delvideo:
            self.execSqlu("delete_videos")
            return ("Aplicativo configurado com sucesso! "
                    "V&iacute;deos deletados!")

        return "Aplicativo configurado com sucesso"


    @staticmethod
    def retornarWidgets():
        """ Retorna os itens para a listagem
        """
        return ({"action":"viewd",
                 "img":"/imgs/preview.gif",
                 "titulo":"Preview",
                 "url":"",
                 "target":""},
                {"action":"viewe",
                 "img":"/imgs/previewe.gif",
                 "titulo":"Publicado",
                 "url":"",
                 "target":""},)


    @dbconnectionapp
    def _verifyStatusContent(self, id_conteudo):
        """
        """
        for i in self.execSql("select_status_content",
                              id_conteudo=int(id_conteudo)):
            return i["publicado"] 


    @dbconnectionapp
    def _setDados(self, id_conteudo):
        """
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)

        for i in self.execSql("select_conteudo",
                              id_conteudo=int(id_conteudo)):

            tags = [j["tag"] for j in portal._getTags(
                                     id_site=self.id_site,
                                     id_conteudo=id_conteudo,
                                     schema=self.schema,
                                     text=None)]
            dados = {
                     "titulo":i["titulo"],
                     "descricao":i["descricao"],
                     "sea_id":i["sea_id"],
                     "embed":i["embed"],
                     "thumb":i["thumb"],
                     "destaque":[],
                     "tags":tags}

            dados["destaque"].append({"titulo":i["titulo_destaque"],
                                      "descricao":i["descricao_destaque"],
                                      "img":i["imagem_destaque"]})

            url = portal.getUrlByApp(env_site=self.id_site,
                                     schema=self.schema,
                                     id_conteudo=id_conteudo,
                                     exportar=1,
                                     admin=1,
                                     mkattr=1)
            return {"titulo":i["titulo"],
                    "meta_type":self.meta_type,
                    "id_conteudo":id_conteudo,
                    "publicado_em":i["publicado_em"],
                    "expira_em":i["expira_em"],
                    "atualizado_em":None,
                    "url":url,
                    "creators":"",
                    "dados":dados
                    }

        return {}


    @dbconnectionapp
    def _getTitleDados(self, id_pk):
        """
        """
        for i in self.execSql("select_titulo",
                              id_conteudo=int(id_pk)):
            return {"title":i["titulo"]}


    @dbconnectionapp
    def _getDublinCore(self, id_pk):
        """
        """
        dados = {"title":"",
                 "created":"",
                 "modified":"",
                 "description":"",
                 "keywords":""}

        for i in self.execSql("select_conteudo",
                              id_conteudo=int(id_pk)):

            portal = Portal(id_site=self.id_site,
                            request=self.request)

            tags = i["tags"]
            dados["title"] = i["titulo"]
            dados["created"] = i["publicado_em"] 
            dados["modified"] = i["atualizado_em"]
            if i["descricao"]:
                dados["description"] = i["descricao"][:80]
            else:
                dados["description"] = ""
            dados["keywords"] = tags 

        return dados 


    @dbconnectionapp
    def _getListContent(self):
        """
        """
        for i in self.execSql("select_conteudo"):
            serialized = self._setDados(i["id_conteudo"])
            i["serialized"] = serialized
            yield i


    @dbconnectionapp
    @serialize 
    @Permission("ADM SITE")
    def copyFiles2Temp(self, id_pk, id_site=None):
        """
            this app doesn't have files to copy
        """
        return "Arquivos copiados com sucesso!" 


    @dbconnectionapp
    @logportal
    @Permission("PERM APP")
    def delConteudo(self, id_conteudo):
        """
        """
        titulo = ""
        for i in self.execSql("select_titulo",
                              id_conteudo=int(id_conteudo)):
            titulo = i["titulo"]

        self.logmsg = "V&iacute;deos dzai '%s' deletado" % titulo
        self.execSqlu("delete_video",
                      id_conteudo=int(id_conteudo))

