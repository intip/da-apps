# -*- encoding: iso8859-1 -*-
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
from publica.utils.decorators import serialize, dbconnectionapp,\
                                     Permission, logportal
from publica.core.portal import Portal
from publica.admin.error import UserError
from publica.utils.json import encode


class Adm(object):
    """
    """

    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def addContent(self, id_treeapp, id_aplicativo, publicado_em,
                         titulo, imagem, destaque1=[], imagem_grande="", 
                         titulo_destaque=None, descricao_destaque=None,
                         imagem_destaque=None, tags="",
                         relacionamento=[], expira_em=None,
                         publicado=None, permissao=None,
                         exportar=None, exportar_json=None, exportar_xml=None):
        """
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        id_conteudo = self.execSql("select_nextval_conteudo").next()["id"]

        publicado = True if publicado else False
        tags = tags if tags else None

        dt = publicado_em
        try:
            p = strptime(publicado_em, '%d/%m/%Y %H:%M')
            publicado_em = strftime('%Y-%m-%d %H:%M', p)
        except ValueError, e:
            raise UserError(("Ocorreu um erro: "
                             "Data de publica&ccedil;&aring;o "
                             "inv&aacute;lida (%s)" % publicado_em))

        try:
            p = strptime(expira_em, "%d/%m/%Y %H:%M")
            expira_em = strftime("%Y-%m-%d %H:%M", p)
        except ValueError, e:
           expira_em = None

        if not imagem: 
            imagem = None
        else:
            imagem = portal.addArquivo(arquivo=imagem,
                                       id_conteudo=id_conteudo,
                                       schema=self.schema,
                                       dt=dt)
        if not imagem_grande: 
            imagem_grande = None
        else:
            imagem_grande = portal.addArquivo(arquivo=imagem_grande,
                                       id_conteudo=id_conteudo,
                                       schema=self.schema,
                                       dt=dt)

        self.execSqlBatch("insert_conteudo",
                          id_conteudo=id_conteudo,
                          titulo=titulo,
                          imagem=imagem,
                          imagem_grande=imagem_grande,
                          publicado=publicado,
                          publicado_em=publicado_em,
                          expira_em=expira_em)

        if titulo_destaque or imagem_destaque or descricao_destaque:
            if not imagem_destaque: 
                imagem_destaque = None
            else:
                imagem_destaque = portal.addArquivo(arquivo=imagem_destaque,
                                                    id_conteudo=id_conteudo,
                                                    schema=self.schema,
                                                    dt=dt)
            self.execSqlBatch("insert_destaque",
                              id_conteudo=id_conteudo,
                              titulo=titulo_destaque,
                              descricao=descricao_destaque,
                              imagem=imagem_destaque)


        ordem = 0
        for i in destaque1:

            if i["imagem"]:
                imagem = portal.addArquivo(arquivo=i["imagem"],
                                           id_conteudo=id_conteudo,
                                           schema=self.schema,
                                           dt=dt)
            else:
                imagem = None

            self.execSqlBatch("insert_destaque1",
                              id_conteudo=id_conteudo,
                              titulo=i["titulo"],
                              descricao=i["descricao"],
                              link=i["link"],
                              imagem=imagem,
                              ordem=ordem,
                              chapeu=i["chapeu"],
                              tipo=i["tipo"])
            ordem += 1

        ordem = 0

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

        if exportar or exportar_json or exportar_xml:
            portal._insertLog(self.id_site,
                       "Programa&ccedil;&atilde;o '%s' adicionada e publicada" % titulo)

            portal._exportarFormatosConteudo(id_aplicativo=id_aplicativo,
                                             id_conteudo=id_conteudo,
                                             schema=self.schema,
                                             id_treeapp=id_treeapp,
                                             html=exportar,
                                             xml=exportar_xml,
                                             json=exportar_json,
                                             dados=dados,
                                             subitems=None,
                                             add=1)

            return ("Programa&ccedil;&atilde;o adicionada com sucesso! "
                    "Publica&ccedil;&atilde;o iniciada.")

        portal._insertLog(self.id_site,
                          "Programa&ccedil;&atilde;o '%s' publicada" % titulo)
        return "Programa&ccedil;&atilde;o adicionada com sucesso!"


    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def editContent(self, id_conteudo, id_treeapp, id_aplicativo, publicado_em,
                          titulo, imagem, destaque1=[], imagem_grande="", 
                          titulo_destaque=None, descricao_destaque=None,
                          imagem_destaque=None, tags="",
                          relacionamento=[], expira_em=None,
                          publicado=None, permissao=None,
                          exportar=None, exportar_json=None, exportar_xml=None):
        """
        """
        id_conteudo = int(id_conteudo)
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        publicado = True if publicado else False
        tags = tags if tags else None

        dt = publicado_em
        try:
            p = strptime(publicado_em, '%d/%m/%Y %H:%M')
            publicado_em = strftime('%Y-%m-%d %H:%M', p)
        except ValueError, e:
            raise UserError(("Ocorreu um erro: "
                             "Data de publica&ccedil;&aring;o "
                             "inv&aacute;lida (%s)" % publicado_em))

        try:
            p = strptime(expira_em, "%d/%m/%Y %H:%M")
            expira_em = strftime("%Y-%m-%d %H:%M", p)
        except ValueError, e:
           expira_em = None


        if not imagem: 
            imagem = None
        else:
            imagem = portal.addArquivo(arquivo=imagem,
                                       id_conteudo=id_conteudo,
                                       schema=self.schema,
                                       dt=dt)
        if not imagem_grande: 
            imagem_grande = None
        else:
            imagem_grande = portal.addArquivo(arquivo=imagem_grande,
                                       id_conteudo=id_conteudo,
                                       schema=self.schema,
                                       dt=dt)
         
        self.execSqlBatch("delete_destaque1",
                          id_conteudo=id_conteudo)
        self.execSqlBatch("delete_destaque",
                          id_conteudo=id_conteudo)

        self.execSqlBatch("update_conteudo",
                          id_conteudo=id_conteudo,
                          titulo=titulo,
                          imagem=imagem,
                          imagem_grande=imagem_grande,
                          publicado=publicado,
                          publicado_em=publicado_em,
                          expira_em=expira_em)

        if titulo_destaque or imagem_destaque or descricao_destaque:
            if not imagem_destaque: 
                imagem_destaque = None
            else:
                imagem_destaque = portal.addArquivo(arquivo=imagem_destaque,
                                                    id_conteudo=id_conteudo,
                                                    schema=self.schema,
                                                    dt=dt)
            self.execSqlBatch("insert_destaque",
                              id_conteudo=id_conteudo,
                              titulo=titulo_destaque,
                              descricao=descricao_destaque,
                              imagem=imagem_destaque)


        ordem = 0
        for i in destaque1:

            if i["imagem"]:
                imagem = portal.addArquivo(arquivo=i["imagem"],
                                           id_conteudo=id_conteudo,
                                           schema=self.schema,
                                           dt=dt)
            else:
                imagem = None

            self.execSqlBatch("insert_destaque1",
                              id_conteudo=id_conteudo,
                              titulo=i["titulo"],
                              descricao=i["descricao"],
                              link=i["link"],
                              imagem=imagem,
                              ordem=ordem,
                              chapeu=i["chapeu"],
                              tipo=i["tipo"])
            ordem += 1

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

        if exportar or exportar_xml or exportar_json:
            portal._insertLog(self.id_site,
                  "Programa&ccedil;&atilde;o '%s' editada e publicada" % titulo)

            portal._exportarFormatosConteudo(id_aplicativo=id_aplicativo,
                                             id_conteudo=id_conteudo,
                                             schema=self.schema,
                                             id_treeapp=id_treeapp,
                                             html=exportar,
                                             xml=exportar_xml,
                                             json=exportar_json,
                                             dados=dados,
                                             subitems=None,
                                             add=1)

            return ("Programa&ccedil;&atilde;o editada com sucesso!"
                    " Publica&ccedil;&atilde;o iniciada.")

        portal._insertLog(self.id_site,
                          "Programa&ccedil;&atilde;o '%s' editada" % titulo)
        return "Programa&ccedil;&atilde;o editada com sucesso!"


    @dbconnectionapp
    @Permission("PERM APP")
    def _getContent(self, id_conteudo):
        """
        """
        for i in self.execSql("select_conteudo",
                            id_conteudo=int(id_conteudo)):
            i["destaque1"] = self.execSql("select_destaque1",
                                          id_conteudo=int(id_conteudo))
            return i

    @dbconnectionapp
    @Permission("PERM APP")
    def _getTipos(self):
        """
            
        """
        return self.execSql("select_tipos")






