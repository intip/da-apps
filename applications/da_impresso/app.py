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
from time import time, strftime, strptime
from publica.core.portal import Portal
from publica.admin.error import UserError
from publica.utils.json import encode
from publica.utils.decorators import serialize, dbconnectionapp,\
                                     Permission, logportal
from publica import settings
from public import Public
from adm import Adm

haslist = True
haslink = True
title = "DA - Impresso"
meta_type = "da_impresso"


class App(Adm, Public):
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
    def _install(self, title, dim_x, dim_y, 
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

        return {"rss":rss,
                "dim_x":dim_x,
                "dim_y":dim_y
                }


    @dbconnectionapp
    @serialize
    @Permission("ADM APP")
    def editApp(self, title, dim_x, dim_y, 
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

        dados = {"rss":rss,
                "dim_x":dim_x,
                "dim_y":dim_y}
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
        return ({"action":"viewd",
                 "img":"/imgs/preview.gif",
                 "titulo":"Din&acirc;mico",
                 "url":"",
                 "target":""},
                {"action":"viewe",
                 "img":"/imgs/previewe.gif",
                 "titulo":"Est&aacute;tico",
                 "url":"",
                 "target":""},
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

        for i in self.execSql("select_noticia_dados",
                              id_conteudo=int(id_conteudo)):

            tags = ""
            dados = {"tipo_noticia":i["tipo_noticia"],
                     "titulo_categoria":i["titulo_categoria"],
                     "titulo":i["titulo"],
                     "descricao":i["descricao"],
                     "editor":i["editor"],
                     "corpo":i["corpo"],
                     "has_video":i["video"],
                     "has_audio":i["audio"],
                     "has_galeria":i["galeria"],
                     "data_edicao":i["data_edicao"],
                     "autor":i["autor"],
                     "foto":[],
                     "video":[],
                     "destaque":[],
                     "fotos_ipad":[],
                     "videos_ipad":[],
                     "tags":tags,
                     "pdf":i["pdf"],
                     "is_capa":i["is_capa"],
                     "titulo_capa":i["titulo_capa"],
                     "ordem":i["ordem"],
                     "titulo_galeria":i["titulo_galeria"]}

            dados["destaque"].append({"titulo":i["titulo_destaque"],
                                      "descricao":i["descricao_destaque"],
                                      "img":i["imagem_destaque"]})

            for j in self.execSql("select_videos",
                                  id_conteudo=int(id_conteudo)):
                dados["video"].append(j)

            for j in self.execSql("select_noticia_autores",
                                  id_conteudo=int(id_conteudo)):
                dados["autor"].append(j)

            for j in self.execSql("select_noticia_fotos",
                                  id_conteudo=int(id_conteudo)):
                dados["foto"].append({"arquivo":j["arquivo"],
                                      "arquivo_grande":j["arquivo_grande"],
                                      "alinhamento":j["alinhamento"],
                                      "credito":j["credito"],
                                      "legenda":j["legenda"],
                                      "link":j["link"]})

            for j in self.execSql("select_fotos_ipad",
                                  id_conteudo=id_conteudo):
                dados["fotos_ipad"].append({"arquivo":j["foto"],
                                      "credito":j["credito"],
                                      "legenda":j["legenda"]})

            for j in self.execSql("select_videos_ipad",
                                  id_conteudo=id_conteudo):
                dados["videos_ipad"].append({"thumb":j["thumb"],
                                        "nome":j["nome"],
                                        "link":j["link"],
                                        "is_audio":j["is_audio"]})

            url = portal.getUrlByApp(env_site=self.id_site,
                                     schema=self.schema,
                                     id_conteudo=id_conteudo,
                                     exportar=1,
                                     admin=1,
                                     mkattr=1)

            creators = []
            if i["autor"]:
                creators.append(i["autor"])

            return {"titulo":i["titulo"],
                    "meta_type":self.meta_type,
                    "id_conteudo":id_conteudo,
                    "publicado_em":i["publicado_em"],
                    "expira_em":i["expira_em"],
                    "atualizado_em":i["atualizado_em"],
                    "url":url,
                    "creators":creators,
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
            if i["descricao"]:
                dados["description"] = i["descricao"][:80]
            else:
                dados["description"] = i["corpo"][:80]
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
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)

        fotos = self._getFotosSite(id_noticia=id_pk)
        destaque = self._getDestaqueSite(id_noticia=id_pk)

        for foto in fotos:
            if foto["arquivo"]:
                portal._copyFile2Temp(arq=foto["arquivo"],
                                      id_site=id_site)
            if foto["arquivo_grande"]:
                 portal._copyFile2Temp(arq=foto["arquivo_grande"],
                                       id_site=id_site)
        if destaque:
          if destaque["img"]:
             portal._copyFile2Temp(arq=destaque["img"],
                                   id_site=id_site)

        return "Arquivos copiados com sucesso!" 


    @dbconnectionapp
    @logportal
    @Permission("PERM APP")
    def delConteudo(self, id_conteudo):
        """
        """
        titulo = ""
        for i in self.execSql("select_noticia",
                              id_conteudo=int(id_conteudo)):
            titulo = i["titulo"]

        self.logmsg = "Not&iacute;cia '%s' deletada" % titulo
        self.execSqlu("delete_noticia",
                      id_conteudo=int(id_conteudo))

