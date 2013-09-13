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
from urllib import unquote
from datetime import datetime
from time import time, strftime, strptime
from publica.core.portal import Portal
from publica.admin.error import UserError
from publica.utils.decorators import serialize, dbconnectionapp,\
                                     Permission, logportal
from publica import settings
from site import Site

haslist = True
haslink = False
meta_type = "da_menutree"
title = "DA - Menu"


class App(Site):
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
    def _install(self, title, 
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
    def _getListContent(self):
        """
        """
        for i in self.execSql("select_conteudo"):
            i["serialized"] = {}
            yield i


    @dbconnectionapp
    @serialize
    @Permission("ADM APP")
    def editApp(self, title, 
                       rss_titulo=None, rss_link=None, rss_descricao=None,
                       rss_idioma=None, rss_categoria=None, rss_copyright=None,
                       rss_imagem_titulo=None, rss_imagem_link=None,
                       rss_imagem=None):
        """Edita os atributos da instancia
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
            for u in settings.USER_PERMISSION:
                self.execSqlu("permissions_admin",
                              user=buffer(u))

        return "Aplicativo configurado com sucesso"


    @staticmethod 
    def retornarWidgets():
        """ Retorna os itens para a listagem
        """
        return ({"action":"qrcode",
                 "img":"/imgs/qrcode.png",
                 "titulo":"Qrcode",
                 "url":""}, )

    # hurdle

    @dbconnectionapp
    @serialize
    @logportal
    @Permission("PERM APP")
    def addMenu(self, id_treeapp, id_aplicativo, titulo, json,
                      exportar=None, exportar_xml=None, exportar_json=None):
        """
        """
        portal = Portal(id_site=self.id_site, request=self.request)
        id_conteudo = self.execSql("select_nextval_conteudo").next()["id"]

        self.execSqlu("insert_conteudo",
                      id_conteudo=id_conteudo,
                      titulo=titulo,
                      json=unicode(json)) 

        portal._addConteudo(env_site=self.id_site,
                            id_pk=id_conteudo,
                            schema=self.schema,
                            meta_type=self.meta_type,
                            id_aplicativo=id_aplicativo,
                            id_treeapp=id_treeapp,
                            titulo=titulo,
                            publicado=True,
                            publicado_em=strftime("%Y-%m-%d %H:%M"),
                            expira_em=None,
                            titulo_destaque=None,
                            descricao_destaque=None,
                            imagem_destaque=None,
                            tags=None,
                            permissao=None)

        if exportar_xml or exportar_json or exportar:

            portal._insertLog(self.id_site,
                              "Novo DA-Menu cadastrado e publicado: '%s'" % titulo)

            portal._exportarFormatosConteudo(id_aplicativo=id_aplicativo,
                                             id_conteudo=id_conteudo,
                                             schema=self.schema,
                                             id_treeapp=id_treeapp,
                                             html=exportar,
                                             xml=None,
                                             json=None,
                                             dados={},
                                             subitems=None,
                                             add=1)

            return "Novo DA-Menu cadastrado e publicada"


        self.logmsg = "Novo DA-Menu adicionado '%s'" % titulo
        return "Novo DA-Menu cadastrado e publicado"


    @dbconnectionapp
    @logportal
    @Permission("PERM APP")
    def delConteudo(self, id_conteudo):
        """ 
        """
        titulo = self.execSql("select_menu",
                              id_conteudo=int(id_conteudo)).next()["titulo"]
        self.execSqlu("delete_menu",
                      id_conteudo=int(id_conteudo))
        self.logmsg = "DA-Menu '%s' deletado" % titulo


    @dbconnectionapp
    def getMenu(self, id_conteudo):
        """
        """
        for i in self.execSql("select_menu",
                              id_conteudo=int(id_conteudo)):
            return i


    @dbconnectionapp
    @serialize
    @logportal
    @Permission("PERM APP")
    def editMenu(self, id_aplicativo, id_treeapp, id_conteudo, titulo, json,
                       exportar=None, exportar_json=None, exportar_xml=None):
        """
        """
        self.execSqlu("update_menu",
                      id_conteudo=int(id_conteudo),
                      titulo=titulo,
                      json=unquote(json)) 

        portal = Portal(id_site=self.id_site,
                        request=self.request)
        portal._editConteudo(env_site=self.id_site,
                             id_pk=id_conteudo,
                             id_aplicativo=int(id_aplicativo),
                             schema=self.schema,
                             id_treeapp=id_treeapp,
                             titulo=titulo,
                             publicado=True,
                             publicado_em=strftime("%Y-%m-%d %H:%M"),
                             expira_em=None,
                             titulo_destaque=None,
                             descricao_destaque=None,
                             imagem_destaque=None,
                             permissao=None,
                             tags=None)

        if exportar_xml or exportar_json or exportar:

            portal._insertLog(self.id_site,
                              "DA-Menu '%s' editado e publicado" % titulo)

            portal._exportarFormatosConteudo(id_aplicativo=id_aplicativo,
                                             id_conteudo=id_conteudo,
                                             schema=self.schema,
                                             id_treeapp=id_treeapp,
                                             html=exportar,
                                             xml=None,
                                             json=None,
                                             dados={},
                                             subitems=None,
                                             edit=1)

            return ("DA-Menu editado com sucesso! "
                    "Publica&ccedil;&atilde;o iniciada.")

        self.logmsg = "DA-Menu editado '%s'" % titulo
        return "Menu editado com sucesso!"
