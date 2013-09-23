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
from publica.core.portal import Portal
from publica.utils.decorators import serialize, dbconnectionapp, Permission,\
    logportal
from publica.admin.appportal import PortalUtils
from publica.admin.interfaces import BaseApp
from publica import settings
from public import Public
from adm import Adm
from time import time

haslist = True
haslink = True
title = "DA - Concursos"
meta_type = "da_concursos"


class App(BaseApp, PortalUtils, Adm, Public):
    """
        Classe base para o funcionamento do aplicativo no Publica
    """
    title = title
    meta_type = meta_type
    haslist = haslist
    haslink = haslink

    def __init__(self, id_site, schema=None, request=None):
        """
            Método padrão de inicialização da classe
        """
        self.id_site = id_site
        self.schema = schema
        self.request = request

    @dbconnectionapp
    def _install(self, title, auth_id,
                 rss_titulo=None, rss_link=None, rss_descricao=None,
                 rss_idioma=None, rss_categoria=None, rss_copyright=None,
                 rss_imagem_titulo=None, rss_imagem_link=None,
                 rss_imagem=None):
        """
            Método padrão de instalação da aplicação no Publica
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

        return {"rss": rss,
                "auth_id": auth_id}

    @dbconnectionapp
    @serialize
    @Permission("ADM APP")
    def editApp(self, title, auth_id,
                rss_titulo=None, rss_link=None, rss_descricao=None,
                rss_idioma=None, rss_categoria=None, rss_copyright=None,
                rss_imagem_titulo=None, rss_imagem_link=None,
                rss_imagem=None):
        """
            Método padrão de edição dos dados da aplicação
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

        dados = {"rss": rss,
                 "auth_id": auth_id}
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
            Método padrão que retorna a informação dos widgets que a aplicação
            utiliza
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
                 "target": ""},)

    @dbconnectionapp
    def _verifyStatusContent(self, id_conteudo):
        """
            Método padrão interno de verificação do status de um conteúdo da
            aplicação
        """
        for i in self.execSql("select_status_content",
                              id_conteudo=int(id_conteudo)):
            return i["publicado"]

    @dbconnectionapp
    def _setDados(self, id_conteudo):
        """
            Método padrão que encapsula os dados de um conteúdo
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)

        for i in self.execSql("select_dados",
                              id_conteudo=int(id_conteudo)):

            tags = [j["tag"] for j in portal._getTags(id_site=self.id_site,
                                                      id_conteudo=id_conteudo,
                                                      schema=self.schema,
                                                      text=None)]
            dados = {"titulo": i["titulo"],
                     "descricao": i["descricao"],
                     "remuneracao_de": i["remuneracao_de"],
                     "remuneracao_ate": i["remuneracao_ate"],
                     "total_vagas": i["total_vagas"],
                     "descricao_vagas": i["descricao_vagas"],
                     "vagas_especiais": i["vagas_especiais"],
                     "descricao_remuneracao": i["descricao_remuneracao"],
                     "inscricoes": i["inscricoes"],
                     "banca_organizadora": i["banca_organizadora"],
                     "cadastro_reserva": i["cadastro_reserva"],
                     "validade_concurso": i["validade_concurso"],
                     "previsto": i["previsto"],
                     "nivel_escolaridade": i["nivel_escolaridade"],
                     "data_edital": i["data_edital"],
                     "data_inscricao": i["data_inscricao"],
                     "data_fim_inscricao": i["data_fim_inscricao"],
                     "data_prova": i["data_prova"],
                     "data_resultado": i["data_resultado"],
                     "destaque": [],
                     "tags": tags}

            dados["destaque"].append({"titulo": i["titulo_destaque"],
                                      "descricao": i["descricao_destaque"],
                                      "img": i["imagem_destaque"]})

            url = portal.getUrlByApp(env_site=self.id_site,
                                     schema=self.schema,
                                     id_conteudo=id_conteudo,
                                     exportar=1,
                                     admin=1,
                                     mkattr=1)

            return {"titulo": i["titulo"],
                    "meta_type": self.meta_type,
                    "id_conteudo": id_conteudo,
                    "publicado_em": i["publicado_em"],
                    "expira_em": i["expira_em"],
                    "atualizado_em": i["atualizado_em"],
                    "url": url,
                    "creators": [],
                    "dados": dados
                    }

        return {}

    @dbconnectionapp
    def _getTitleDados(self, id_pk):
        """
            Método padrão para retornar o título de um conteúdo para o portal,
            necessária em algumas ações internas do Publica
        """
        for i in self.execSql("select_titulo",
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
                dados["description"] = i["description"]

        return dados

    @dbconnectionapp
    def _getListContentRef(self):
        """
            Método padrão para retornar as referências de um conteúdo a ser
            copiado em folders
        """
        for i in self.execSql("select_dados"):
            serialized = self._setDados(i["id_conteudo"])
            i["serialized"] = serialized
            yield i

    @dbconnectionapp
    @serialize
    @Permission("ADM SITE")
    def copyFiles2Temp(self, id_pk, id_site=None):
        """
            Método padrão de cópia de arquivos do conteúdo do aplicativo para
            outras folders
        """
        return "Arquivos copiados com sucesso!"

    @dbconnectionapp
    @logportal
    @Permission("PERM APP")
    def delConteudo(self, id_conteudo):
        """
            Método padrão para o portal chamar a ação de deletar um conteúdo
        """
        titulo = ""
        for i in self.execSql("select_titulo",
                              id_conteudo=int(id_conteudo)):
            titulo = i["titulo"]

        self.logmsg = "Conteudo '%s' deletado" % titulo
        self.execSqlu("delete_conteudo",
                      id_conteudo=int(id_conteudo))
