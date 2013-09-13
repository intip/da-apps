# coding: utf-8
#
# Copyright 2010 Prima Tech.
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
from datetime import datetime
from time import time, strftime, strptime
from publica.core.portal import Portal
from publica.admin.error import UserError
from publica.utils.decorators import serialize, dbconnectionapp,\
                                     Permission, logportal
from publica import settings
from adm import Adm
from site import Site

haslist = True
haslink = True
title = "DA - Vrum Opiniao"
meta_type = "da_vrumopiniao"


class App(Adm, Site):
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
    def _install(self, title, app_wad,
                       rss_titulo=None, rss_link=None, rss_descricao=None,
                       rss_idioma=None, rss_categoria=None, rss_copyright=None,
                       rss_imagem_titulo=None, rss_imagem_link=None,
                       rss_imagem=None):
        """
            Add new applications instance
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

        rss = {"titulo":rss_titulo,
               "link":rss_link,
               "descricao":rss_descricao,
               "idioma":rss_idioma,
               "categoria":rss_categoria,
               "copyright":rss_copyright,
               "imagem_titulo":rss_imagem_titulo,
               "imagem_link":rss_imagem_link,
               "rss_imagem":rss_imagem}

        return {"app_wad":app_wad,
                "rss":rss}


    @dbconnectionapp
    @serialize
    @Permission("ADM APP")
    def editApp(self, title, app_wad,
                       rss_titulo=None, rss_link=None, rss_descricao=None,
                       rss_idioma=None, rss_categoria=None, rss_copyright=None,
                       rss_imagem_titulo=None, rss_imagem_link=None,
                       rss_imagem=None):
        """
            Edit instance attributes
        """
        rss = {"titulo":rss_titulo,
               "link":rss_link,
               "descricao":rss_descricao,
               "idioma":rss_idioma,
               "categoria":rss_categoria,
               "copyright":rss_copyright,
               "imagem_titulo":rss_imagem_titulo,
               "imagem_link":rss_imagem_link,
               "rss_imagem":rss_imagem}

        dados = {"app_wad":app_wad,
                 "rss":rss}

        portal = Portal(id_site=self.id_site,
                        request=self.request)
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
        """ Retorna os itens para a listagem
        """
        return ({"action":"viewd",
                 "img":"/imgs/preview.gif",
                 "titulo":"Din&acirc;mico",
                 "url":""},
                {"action":"viewe",
                 "img":"/imgs/previewe.gif",
                 "titulo":"Est&aacute;tico",
                 "url":""},
                {"action":"viewp",
                 "img":"/imgs/env.comment.png",
                 "titulo":"Coment&aacute;rios",
                 "url":"/app/listcomentapp.env",
                 "target":"edicao"},
                {"action":"viewp",
                 "img":"/imgs/env.comment.mod.png",
                 "titulo":"Modera&ccedil;&atilde;o",
                 "url":"/app/addcomentmod.env",
                 "target":"edicao"},
                {"action":"qrcode",
                 "img":"/imgs/qrcode.png",
                 "titulo":"Qrcode",
                 "url":""})


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
                         
        for i in self.execSql("select_dublic_core",
                              id_conteudo=int(id_pk)):
                         
            portal = Portal(id_site=self.id_site,
                            request=self.request)

            tags = [j["tag"] for j in portal._getTags(id_site=self.id_site,
                                                      id_conteudo=int(id_pk),
                                                      schema=self.schema,
                                                      text=None)]
            tags = " ".join(tags)

            dados["title"] = i["titulo"]
            dados["created"] = i["publicado_em"]
            dados["modified"] = i["atualizado_em"]
            dados["description"] = i["descricao"][:80]
            dados["keywords"] = tags

        return dados


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
        for conteudo in self.execSql("select_conteudo",
                                     id_conteudo=int(id_conteudo)):

            portal = Portal(id_site=self.id_site,
                            request=self.request)
            tags = []
            url = portal.getUrlByApp(env_site=self.id_site,
                                     schema=self.schema,
                                     id_conteudo=id_conteudo,
                                     exportar=1,
                                     admin=1,
                                     mkattr=1)

            dados = {"titulo":conteudo["titulo"],
                     #"id_categoria":conteudo["id_categoria"],
                     #"imagem":conteudo["imagem"],
                     "codigo_fipe":conteudo["codigo_fipe"],
                     "ordem":conteudo["ordem"],
                     "aval_design":conteudo["aval_design"],
                     "aval_performance":conteudo["aval_performance"],
                     "aval_conforto_acabamento":conteudo["aval_conforto_acabamento"],
                     "aval_dirigibilidade":conteudo["aval_dirigibilidade"],
                     "aval_consumo":conteudo["aval_consumo"],
                     "aval_manutencao":conteudo["aval_manutencao"],
                     "aval_custo_beneficio":conteudo["aval_custo_beneficio"],
                     "destaque":[{"titulo":conteudo["destaque_titulo"],
                                  "descricao":conteudo["destaque_descricao"],
                                  "img":conteudo["destaque_imagem"]}],
                     "tags":tags}


            return {"titulo":conteudo["titulo"],
                    "meta_type":self.meta_type,
                    "id_conteudo":id_conteudo,
                    "publicado_em":conteudo["publicado_em"],
                    "expira_em":conteudo["expira_em"],
                    "atualizado_em":conteudo["atualizado_em"],
                    "url":url,
                    "creators":[],
                    "dados":dados}


    @dbconnectionapp
    @serialize 
    @Permission("ADM SITE")
    def copyFiles2Temp(self, id_pk, id_site=None):
        """
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)

        for destaque1 in self.execSql("select_destaque1",
                                      id_conteudo=int(id_pk)):
            if destaque1["imagem"]:
                portal._copyFile2Temp(arq=destaque["imagem"],
                                      id_site=id_site)

        for destaque2 in self.execSql("select_destaque2",
                                      id_conteudo=int(id_pk)):
            if destaque1["imagem"]:
                portal._copyFile2Temp(arq=destaque["imagem"],
                                      id_site=id_site)

        for conteudo in self.execSql("select_conteudo_",
                                     id_conteudo=int(id_pk)):
            if conteudo["imagem_destaque"]:
                 portal._copyFile2Temp(arq=conteudo["imagem_destaque"],
                                       id_site=id_site)

            if conteudo["destaque_imagem"]:
                 portal._copyFile2Temp(arq=conteudo["destaque_imagem"],
                                       id_site=id_site)

        return "Arquivos copiados com sucesso!" 


    @dbconnectionapp
    @logportal
    @Permission("PERM APP")
    def delConteudo(self, id_conteudo):
        """
        """
        dados = self.execSql("select_conteudo_",
                             id_conteudo=int(id_conteudo)).next()
        self.execSqlu("delete_conteudo",
                      id_conteudo=int(id_conteudo))
        self.logmsg = ("Conte&uacute;do Vrum Opini&atilde;o '%s:%s' "
                       "deletado") % (dados["titulo"],
                                      dados["publicado_em"])
        self._setRanking()

