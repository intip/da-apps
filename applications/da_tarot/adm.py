# -*- encoding: LATIN-1 -*-
#
# Copyright 2010 Prima Tech.
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
    Control module of the application.
"""

from time import strftime, strptime
import urllib
import json
import os

from publica.utils.json import encode

from publica.admin.error import UserError
from publica.utils.decorators import serialize, dbconnectionapp, \
                                     Permission, logportal
from publica.core.portal import Portal

class Adm(object):
    """
        Classe que contem os metodos de administracao dos dados.
    """
    #Onde estah a abstracao?
    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def addConteudo(self, titulo, publicado_em, publicado, id_aplicativo, 
                    id_treeapp, permissao, relacionamento="", exportar="", 
                    expira_em="", imagem="", descricao="", titulo_destaque="", 
                    descricao_destaque="", imagem_destaque="", **kargs):
        """
        Metodo chamado ao adicionar
        """
        portal = Portal(id_site=self.id_site, request=self.request)
        id_conteudo = self.execSql("select_nextval_conteudo").next()["id"]
        publicado = True if publicado else False
        tags = kargs.get("tags")
        data_publicado = publicado_em

        try:
            nova_data = strptime(publicado_em, "%d/%m/%Y %H:%M")
            publicado_em = strftime("%Y-%m-%d %H:%M", nova_data)
        except ValueError:
            raise UserError("Ocorreu um erro: "
                            "Data de publica&ccedil;&aring;o "
                            "inv&aacute;lida (%s)" % publicado_em)
        try:
            novo_expira = strptime(expira_em, "%d/%m/%Y %H:%M")
            expira_em = strftime("%Y-%m-%d %H:%M", novo_expira)
        except ValueError:
            expira_em = None

        id_imagem = portal.addArquivo(arquivo=imagem,
                             id_conteudo=id_conteudo,
                             schema=self.schema,
                             dt=data_publicado)

        self.execSqlBatch("insert_conteudo_", titulo=titulo,
                                              descricao=descricao, 
                                              publicado=publicado,
                                              imagem=id_imagem, 
                                              publicado_em=publicado_em,
                                              expira_em=expira_em, 
                                              id_conteudo=int(id_conteudo))

        if titulo_destaque or imagem_destaque or descricao_destaque:
            if not imagem_destaque:
                imagem_destaque = None
            else:
                imagem_destaque = portal.addArquivo(arquivo=imagem_destaque,
                                                    id_conteudo=id_conteudo,
                                                    schema=self.schema,
                                                    dt=data_publicado)
            self.execSqlBatch("insert_destaque",
                              id_conteudo=int(id_conteudo),
                              titulo=titulo_destaque,
                              descricao=descricao_destaque,
                              img=imagem_destaque)
        self.execSqlCommit()

        dados = self._setDados(id_conteudo=id_conteudo)
        portal._addConteudo(env_site=self.id_site,
                            id_pk=id_conteudo,
                            id_aplicativo=id_aplicativo,
                            schema=self.schema,
                            meta_type=self.meta_type,
                            id_treeapp=id_treeapp,
                            titulo=titulo,
                            publicado=publicado,
                            publicado_em=publicado_em,
                            expira_em=expira_em,
                            titulo_destaque=titulo_destaque,
                            descricao_destaque=descricao_destaque,
                            imagem_destaque=imagem_destaque,
                            permissao=permissao,
                            tags=tags,
                            relacionamento=relacionamento,
                            dados=dados)

        exportar_xml = kargs.get("exportar_xml") != "null"
        exportar_json = kargs.get("exportar_xml") != "null"

        if exportar or exportar_xml or exportar_json:
            portal._insertLog(self.id_site,
                              "Conte&uacute;do '%s' editado" % titulo)
            portal._exportarFormatosConteudo(id_aplicativo=id_aplicativo,
                                             id_conteudo=id_conteudo,
                                             schema=self.schema,
                                             id_treeapp=id_treeapp,
                                             html=exportar,
                                             xml=exportar_xml,
                                             json=exportar_json,
                                             subitems=None,
                                             add=1)
            return ("Conte&uacute;do adicionado com sucesso! "
                    "Publica&ccedil;&atilde;o iniciada.")

        portal._insertLog(self.id_site,
                          "Conte&uacute;do '%s' adicionado" % titulo)
        return "Conte&uacute;do adicionado com sucesso!"


    @dbconnectionapp
    def _getConteudo(self, id_conteudo):
        """
            Retorna o conteudo
        """
        for i in self.execSql("select_conteudo", 
                              id_conteudo = int(id_conteudo)):
            i["titulo"] = i["titulo"].decode("latin-1").encode("utf-8")
            return i
    
    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def editConteudo(self, id_conteudo=None, id_treeapp=None, 
                     id_aplicativo=None,
                     titulo_destaque=None, imagem_destaque=None, publicado=None,
                     relacionamento=[], titulo=None, descricao=None,
                     filiado=None, informacoes=None, imagem=None, tags=None,
                     publicado_em=None, expira_em=None, exportar=None,
                     id_destaque=None, exportar_xml=None, exportar_json=None,
                     descricao_destaque=None, permissao=None, tipo=None):
        """
            Edita os dados
        """
        portal = Portal(id_site=self.id_site, request=self.request)
        publicado = True if publicado else False
        tags = tags if tags else None
        data_publicado = publicado_em

        try:
            nova_data = strptime(publicado_em, "%d/%m/%Y %H:%M")
            publicado_em = strftime("%Y-%m-%d %H:%M", nova_data)
        except ValueError:
            raise UserError("Ocorreu um erro: "
                            "Data de publica&ccedil;&aring;o "
                            "inv&aacute;lida (%s)" % publicado_em)
        try:
            novo_expira = strptime(expira_em, "%d/%m/%Y %H:%M")
            expira_em = strftime("%Y-%m-%d %H:%M", novo_expira)
        except ValueError:
            expira_em = None

        id_imagem = portal.addArquivo(arquivo=imagem,
                             id_conteudo=id_conteudo,
                             schema=self.schema,
                             dt=data_publicado)
        

        self.execSqlBatch("update_conteudo", titulo=titulo, filiado=filiado,
                      descricao=descricao, informacoes=informacoes,
                      imagem=id_imagem, publicado_em=publicado_em,
                      expira_em=expira_em, id_conteudo=int(id_conteudo))

        if titulo_destaque or imagem_destaque or descricao_destaque:
            if not imagem_destaque:
                imagem_destaque = None
            else:
                imagem_destaque = portal.addArquivo(arquivo=imagem_destaque,
                                                    id_conteudo=id_conteudo,
                                                    schema=self.schema,
                                                    dt=data_publicado)

            if id_destaque:
                self.execSqlBatch("update_destaque",
                                  id_destaque=int(id_destaque),
                                  titulo=titulo_destaque,
                                  descricao=descricao_destaque,
                                  img=imagem_destaque)
            else:
                self.execSqlBatch("insert_destaque",
                                  id_conteudo=int(id_conteudo),
                                  titulo=titulo_destaque,
                                  descricao=descricao_destaque,
                                  img=imagem_destaque)
        elif id_destaque:
            self.execSqlBatch("delete_destaque",
                              id_destaque=int(id_destaque))
            titulo_destaque = None
            descricao_destaque = None
            imagem_destaque = None

        self.execSqlCommit()

        dados = self._setDados(id_conteudo=id_conteudo)
        portal._editConteudo(env_site=self.id_site,
                             id_pk=id_conteudo,
                             id_aplicativo=int(id_aplicativo),
                             schema=self.schema,
                             id_treeapp=id_treeapp,
                             titulo=titulo,
                             publicado=publicado,
                             publicado_em=publicado_em,
                             expira_em=expira_em,
                             titulo_destaque=titulo_destaque,
                             descricao_destaque=descricao_destaque,
                             imagem_destaque=imagem_destaque,
                             permissao=permissao,
                             tags=tags,
                             relacionamento=relacionamento,
                             dados=dados)

        if exportar_xml == "null":
            exportar_xml = 0
        if exportar_json == "null":
            exportar_json = 0
            
        if exportar or exportar_xml or exportar_json:
            portal._insertLog(self.id_site,
                              "Conte&uacute;do '%s' editado" % titulo)
            portal._exportarFormatosConteudo(id_aplicativo=id_aplicativo,
                                             id_conteudo=id_conteudo,
                                             schema=self.schema,
                                             id_treeapp=id_treeapp,
                                             html=exportar,
                                             xml=exportar_xml,
                                             json=exportar_json,
                                             subitems=None,
                                             add=1)
            return ("Conte&uacute;do editado com sucesso! "
                    "Publica&ccedil;&atilde;o iniciada.")

        portal._insertLog(self.id_site,
                          "Conte&uacute;do '%s' editado" % titulo)
        return "Conte&uacute;do editado com sucesso!"
