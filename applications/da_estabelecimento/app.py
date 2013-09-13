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
"""
    Modulo principal do aplicativo.
"""

from time import time

from publica.core.portal import Portal
from publica.utils.decorators import serialize, dbconnectionapp, \
                                     Permission, logportal
from publica import settings
from site import Site
from publica.admin.interfaces import BaseApp
from adm import Adm


title = "DA - Estabelecimentos"
meta_type = "da_estabelecimento"
haslink = True
haslist = True

class App (BaseApp, Adm, Site):
    """
        Classe base do aplicativo de estabelecimento
    """

    title = title
    meta_type = meta_type
    haslink = haslink
    haslist = haslist

    def __init__(self, id_site, schema=None, request=None):
        """
            Construtor da instancia do aplicativo.
        """
        self.id_site = id_site
        self.schema = schema
        self.request = request

    @dbconnectionapp
    def _install(self, title, rss_titulo=None, rss_link=None,
                       rss_descricao=None, rss_idioma=None, rss_categoria=None,
                       rss_copyright=None, rss_imagem_titulo=None,
                       rss_imagem_link=None, rss_imagem=None):
        """
            Metodo chamado ao adicionar um aplicativo
        """
        nid = str(time()).replace(".", "")
        if not self.schema:
            self.schema = "%s_%s" % (meta_type, nid)
        self.execSqlu("structure")

        portal = Portal(id_site=self.id_site, request=self.request)

        user_dinamic = portal._getUserDinamic(id_site=self.id_site)
        if user_dinamic:
            self.execSqlu("permissions", user=buffer(user_dinamic))

        if settings.USER_PERMISSION:
            for i in settings.USER_PERMISSION:
                self.execSqlu("permissions_admin", user=buffer(i))

        rss = {"titulo":rss_titulo,
               "link":rss_link,
               "descricao":rss_descricao,
               "idioma":rss_idioma,
               "categoria":rss_categoria,
               "copyright":rss_copyright,
               "imagem_titulo":rss_imagem_titulo,
               "imagem_link":rss_imagem_link,
               "rss_imagem":rss_imagem}

        return {"rss":rss}


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
        for conteudo in self.execSql("select_conteudo_dados",
                                     id_conteudo=int(id_conteudo)):
            portal = Portal(id_site=self.id_site,
                            request=self.request)
            tags = ""
            url = portal.getUrlByApp(env_site=self.id_site,
                                     schema=self.schema,
                                     id_conteudo=id_conteudo,
                                     exportar=1,
                                     admin=1,
                                     mkattr=1)

            dados = {"titulo":conteudo["titulo"],
                     "expira_em":conteudo["expira_em"],
                     "publicado_em":conteudo["publicado_em"],
                     "publicado":conteudo["publicado"],
                     "imagem":conteudo["imagem"],
                     "filiado":conteudo["filiado"],
                     "descricao":conteudo["descricao"],
                     "imagem_destaque":conteudo["imagem_destaque"],
                     "titulo_destaque":conteudo["titulo_destaque"],
                     "descricao_destaque":conteudo["descricao_destaque"],
                     "tags":tags}
            return dados

    @dbconnectionapp
    @serialize 
    @Permission("ADM SITE")
    def copyFiles2Temp(self, id_pk, id_site=None):
        """
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)

        for destaque in self.execSql("select_destaque",
                                      id_conteudo=int(id_pk)):
            if destaque["imagem"]:
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

            if conteudo["imagem"]:
                portal._copyFile2Temp(arq=conteudo["imagem"],
                                       id_site=id_site)

        return "Arquivos copiados com sucesso!" 

    @dbconnectionapp
    def _getTitleDados(self, id_pk):
        """
        """
        for i in self.execSql("select_titulo",
                              id_conteudo=int(id_pk)):
            return {"title":i["titulo"]}

    @dbconnectionapp
    @serialize
    @Permission("ADM APP")
    def editApp(self, title, rss_titulo=None, rss_link=None, rss_descricao=None,
                rss_idioma=None, rss_categoria=None, rss_copyright=None,
                rss_imagem_titulo=None, rss_imagem_link=None, rss_imagem=None):
        """
            Edita os dados de aplicativo de uma instancia instalada.
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

        dados = {"rss":rss}

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
            for i in settings.USER_PERMISSION:
                self.execSqlu("permissions_admin",
                              user=buffer(i))

        return "Aplicativo configurado com sucesso"

    @dbconnectionapp
    def _getDublinCore(self, id_pk):
        """
            
        """
        dados = {"title":"",
                 "created":"",
                 "modified":"",
                 "description":"",
                 "keywords":""}

        for i in self.execSql("select_dublin_core",
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

    @staticmethod
    def retornarWidgets():
        """
            Retorna os itens para a listagem
        """
        return ({"action":"viewd",
                 "img":"/imgs/preview.gif",
                 "titulo":"Din&acirc;mico",
                 "url":""},
                {"action":"viewe",
                 "img":"/imgs/previewe.gif",
                 "titulo":"Est&aacute;tico",
                 "url":""},
                {"action":"view",
                 "img":"/imgs/env.edit.png",
                 "titulo":"Filiais",
                 "url":"listfiliais.env",
                 "target":"listagem"},
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
    @logportal
    @Permission("PERM APP")
    def delConteudo(self, id_conteudo):
        """
            Deleta  um estabelecimento
        """
        titulo = self.execSql("select_titulo",
                              id_conteudo=int(id_conteudo))
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        for title in titulo:
            portal._insertLog(self.id_site,
                              "Estabelecimento {0} deletado.".format(title['titulo']))
        self.execSqlu("delete_conteudo_", id_conteudo=int(id_conteudo))











