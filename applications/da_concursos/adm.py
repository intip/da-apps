# coding: utf-8
#
# Copyright 2009 Prima Tech Informatica LTDA.
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
from time import strftime, strptime
from publica.utils.decorators import serialize, dbconnectionapp,\
    Permission
import publica.utils.json as json
from urllib import unquote
from publica.core.portal import Portal


class Adm(object):
    """
    """

    def _getDados(self):
        """
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        dados = portal._getApp(env_site=self.id_site,
                               schema=self.schema)
        return dados["dados"]

    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def addConteudo(self, id_site, id_treeapp, id_aplicativo,
                    titulo, descricao, publicado_em, id_estado,
                    cargo=None, expira_em=None, publicado=None,
                    titulo_destaque=None, descricao_destaque=None,
                    imagem_destaque=None, peso_destaque=None,
                    relacionamento=[], tags="", permissao=None,
                    exportar_xml=None, exportar_json=None,
                    exportar=None, descricao_vagas=None,
                    vagas_especiais=None, descricao_remuneracao=None,
                    banca_organizadora=None, cadastro_reserva=None,
                    validade_concurso=None, nivel_escolaridade=None,
                    data_edital=None, data_inscricao=None,
                    data_fim_inscricao=None, data_prova=None,
                    data_resultado=None, media=None, previsto=None,
                    remuneracao_de=None, remuneracao_ate=None,
                    total_vagas=None, inscricoes=None):
        """
            add conteudo
        """
        xml = "xmlcharrefreplace"
        arquivos = unquote(media).decode("utf8").encode("latin1",
                                                        xml)
        arquivos = json.decode(arquivos.replace("\n", "\\n"),
                               encoding="latin1")
        id_estado = unquote(id_estado).decode("utf8").encode("latin1",
                                                             xml)
        estados = json.decode(id_estado.replace("\n", "\\n"),
                              encoding="latin1")
        dt = publicado_em
        publicado = True if publicado else False
        previsto = True if previsto else False
        tags = tags if tags else None
        publicado_em = self.formatDate(publicado_em, True)
        expira_em = self.formatDate(expira_em, True)
        data_edital = self.formatDate(data_edital)
        data_inscricao = self.formatDate(data_inscricao)
        data_fim_inscricao = self.formatDate(data_fim_inscricao)
        data_prova = self.formatDate(data_prova)
        data_resultado = self.formatDate(data_resultado)
        # inserir conteudo
        id_conteudo = self.execSql("select_nextval_conteudo").next()["id"]
        total_vagas = int(total_vagas) if total_vagas else None
        remuneracao_de = int(remuneracao_de) if remuneracao_de else None
        remuneracao_ate = int(remuneracao_ate) if remuneracao_ate else None
        self.execSqlBatch("insert_conteudo",
                          id_conteudo=id_conteudo,
                          titulo=titulo,
                          descricao=descricao,
                          publicado_em=publicado_em,
                          cargo=cargo,
                          total_vagas=total_vagas,
                          descricao_vagas=descricao_vagas,
                          vagas_especiais=vagas_especiais,
                          previsto=previsto,
                          remuneracao_de=remuneracao_de,
                          remuneracao_ate=remuneracao_ate,
                          descricao_remuneracao=descricao_remuneracao,
                          inscricoes=inscricoes,
                          banca_organizadora=banca_organizadora,
                          cadastro_reserva=cadastro_reserva,
                          validade_concurso=validade_concurso,
                          nivel_escolaridade=nivel_escolaridade,
                          data_edital=data_edital,
                          data_inscricao=data_inscricao,
                          data_fim_inscricao=data_fim_inscricao,
                          data_prova=data_prova,
                          data_resultado=data_resultado,
                          expira_em=expira_em,
                          publicado=publicado)

        # inserindo os destaques
        if titulo_destaque or imagem_destaque or descricao_destaque:
            imagem_destaque = self._addFile(arquivo=imagem_destaque,
                                            id_conteudo=id_conteudo,
                                            schema=self.schema,
                                            dt=dt)
            if not imagem_destaque:
                imagem_destaque = None

            try:
                peso_destaque = int(peso_destaque)
            except:
                peso_destaque = 0

            self.execSqlBatch("insert_destaque",
                              id_conteudo=id_conteudo,
                              titulo=titulo_destaque,
                              descricao=descricao_destaque,
                              img=imagem_destaque,
                              peso=peso_destaque)

        self.execSqlCommit()
        # inserindo os arquivos
        if estados:
            for id_estado in estados:
                self.execSqlu("insert_estados_concurso",
                              id_conteudo=int(id_conteudo),
                              id_estado=int(id_estado))
        # inserindo os arquivos
        if arquivos:
            for arquivo in arquivos:
                arquivocam = self._addFile(arquivo=arquivo['valor'],
                                           id_conteudo=id_conteudo,
                                           schema=self.schema,
                                           dt=dt)
                self.execSqlu("insert_arquivo",
                              id_conteudo=int(id_conteudo),
                              titulo=arquivo['nome'],
                              arquivo=arquivocam,
                              tipo=arquivo['tipo'],
                              permissao=arquivo['permissao'])

        # acoes para o portal
        dados = self._setDados(id_conteudo=id_conteudo)
        self._addContentPortal(env_site=self.id_site,
                               id_pk=id_conteudo,
                               schema=self.schema,
                               meta_type=self.meta_type,
                               id_aplicativo=id_aplicativo,
                               id_treeapp=id_treeapp,
                               peso=peso_destaque,
                               titulo=titulo,
                               publicado=publicado,
                               publicado_em=publicado_em,
                               expira_em=expira_em,
                               titulo_destaque=titulo_destaque,
                               descricao_destaque=descricao_destaque,
                               imagem_destaque=imagem_destaque,
                               tags=tags,
                               permissao=permissao,
                               relacionamento=relacionamento,
                               dados=dados)

        if exportar_xml or exportar_json or exportar:

            self._addLog("Novo conteudo cadastrado e publicado '%s'" % titulo)
            self._exportContent(id_aplicativo=id_aplicativo,
                                id_conteudo=id_conteudo,
                                schema=self.schema,
                                id_treeapp=id_treeapp,
                                html=exportar,
                                xml=exportar_xml,
                                json=exportar_json,
                                dados=dados,
                                subitems=None,
                                add=1)

            return ("Conteudo cadastrado com sucesso! "
                    "Publica&ccedil;&atilde;o iniciada.")

        self._addLog("Novo conteudo cadastrada '%s'" % titulo)
        return "Conteudo cadastrado com sucesso."

    def formatDate(self, date, hour=False):
        """
            formata data
        """
        try:
            if hour:
                p = strptime(date, "%d/%m/%Y %H:%M")
                date = strftime("%Y-%m-%d %H:%M", p)
            else:
                p = strptime(date, "%d/%m/%Y")
                date = strftime("%Y-%m-%d", p)
            return date
        except ValueError:
            date = None

    @dbconnectionapp
    @Permission("PERM APP")
    def _getFileContent(self, id_conteudo):
        """
          return file content
        """
        files = []
        for i in self.execSql("select_file",
                              id_conteudo=int(id_conteudo)):
            files.append(i)
        return files

    @dbconnectionapp
    @Permission("PERM APP")
    def _getEstadosConc(self, id_conteudo):
        """
            retorna lista de estados
        """
        estados = []
        for i in self.execSql("select_estados_concurso",
                              id_conteudo=int(id_conteudo)):
            estados.append(i)
        return estados

    @dbconnectionapp
    @Permission("PERM APP")
    def _getConteudo(self, id_conteudo):
        """
        """
        for i in self.execSql("select_conteudo",
                              id_conteudo=int(id_conteudo)):
            i['arquivos'] = self._getFileContent(id_conteudo)
            i['estados'] = self._getEstadosConc(id_conteudo)
            return i

    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def editConteudo(self, id_conteudo, id_site, id_treeapp, id_aplicativo,
                     titulo, descricao, publicado_em, id_estado,
                     cargo=None, expira_em=None, publicado=None,
                     titulo_destaque=None, descricao_destaque=None,
                     imagem_destaque=None, peso_destaque=None,
                     relacionamento=[], tags="", permissao=None,
                     exportar_xml=None, exportar_json=None,
                     exportar=None, descricao_vagas=None,
                     vagas_especiais=None, remuneracao_de=None,
                     descricao_remuneracao=None, inscricoes=None,
                     banca_organizadora=None, cadastro_reserva=None,
                     validade_concurso=None, nivel_escolaridade=None,
                     data_edital=None, data_inscricao=None,
                     data_fim_inscricao=None, data_prova=None,
                     data_resultado=None, previsto=None, media=None,
                     remuneracao_ate=None, total_vagas=None):
        """
        """
        xml = "xmlcharrefreplace"
        arquivos = unquote(media).decode("utf8").encode("latin1",
                                                        "xmlcharrefreplace")
        arquivos = json.decode(arquivos.replace("\n", "\\n"),
                               encoding="latin1")
        id_estado = unquote(id_estado).decode("utf8").encode("latin1",
                                                             xml)
        estados = json.decode(id_estado.replace("\n", "\\n"),
                              encoding="latin1")
        publicado = True if publicado else False
        previsto = True if previsto else False
        tags = tags if tags else None
        dt = publicado_em
        publicado_em = self.formatDate(publicado_em, True)
        expira_em = self.formatDate(expira_em, True)
        data_edital = self.formatDate(data_edital)
        data_inscricao = self.formatDate(data_inscricao)
        data_fim_inscricao = self.formatDate(data_fim_inscricao)
        data_prova = self.formatDate(data_prova)
        data_resultado = self.formatDate(data_resultado)
        total_vagas = int(total_vagas) if total_vagas else None
        remuneracao_de = int(remuneracao_de) if remuneracao_de else None
        remuneracao_ate = int(remuneracao_ate) if remuneracao_ate else None
        # deletar conteudo tabela destaques ou outras tabelas
        self.execSqlBatch("delete_destaque",
                          id_conteudo=int(id_conteudo))
        self.execSqlBatch("delete_arquivos",
                          id_conteudo=int(id_conteudo))
        self.execSqlBatch("delete_estados_conteudo",
                          id_conteudo=int(id_conteudo))
        self.execSqlBatch("update_conteudo",
                          id_conteudo=int(id_conteudo),
                          titulo=titulo,
                          descricao=descricao,
                          publicado_em=publicado_em,
                          cargo=cargo,
                          descricao_vagas=descricao_vagas,
                          remuneracao_de=remuneracao_de,
                          remuneracao_ate=remuneracao_ate,
                          total_vagas=total_vagas,
                          vagas_especiais=vagas_especiais,
                          previsto=previsto,
                          descricao_remuneracao=descricao_remuneracao,
                          inscricoes=inscricoes,
                          banca_organizadora=banca_organizadora,
                          cadastro_reserva=cadastro_reserva,
                          validade_concurso=validade_concurso,
                          nivel_escolaridade=nivel_escolaridade,
                          data_edital=data_edital,
                          data_inscricao=data_inscricao,
                          data_fim_inscricao=data_fim_inscricao,
                          data_prova=data_prova,
                          data_resultado=data_resultado,
                          expira_em=expira_em,
                          publicado=publicado)
        # inserindo os destaques
        if titulo_destaque or imagem_destaque or descricao_destaque:
            imagem_destaque = self._addFile(arquivo=imagem_destaque,
                                            id_conteudo=id_conteudo,
                                            schema=self.schema,
                                            dt=dt)
            if not imagem_destaque:
                imagem_destaque = None

            try:
                peso_destaque = int(peso_destaque)
            except:
                peso_destaque = 0

            self.execSqlBatch("insert_destaque",
                              id_conteudo=int(id_conteudo),
                              titulo=titulo_destaque,
                              descricao=descricao_destaque,
                              img=imagem_destaque,
                              peso=peso_destaque)

        self.execSqlCommit()
        # inserindo os arquivos
        if estados:
            for id_estado in estados:
                self.execSqlu("insert_estados_concurso",
                              id_conteudo=int(id_conteudo),
                              id_estado=int(id_estado))
        #inserindo os arquivos
        if arquivos:
            for arquivo in arquivos:
                arquivocam = self._addFile(arquivo=arquivo['valor'],
                                           id_conteudo=id_conteudo,
                                           schema=self.schema,
                                           dt=dt)
                self.execSqlu("insert_arquivo",
                              id_conteudo=int(id_conteudo),
                              titulo=arquivo['nome'],
                              arquivo=arquivocam,
                              tipo=arquivo['tipo'],
                              permissao=arquivo['permissao'])
        # acoes para o portal
        dados = self._setDados(id_conteudo=id_conteudo)
        self._editContentPortal(env_site=self.id_site,
                                id_pk=id_conteudo,
                                id_aplicativo=int(id_aplicativo),
                                schema=self.schema,
                                id_treeapp=id_treeapp,
                                peso=peso_destaque,
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

        if exportar_xml or exportar_json or exportar:

            self._addLog("Conteudo '%s' editado e publicado" % titulo)
            self._exportContent(id_aplicativo=id_aplicativo,
                                id_conteudo=id_conteudo,
                                schema=self.schema,
                                id_treeapp=id_treeapp,
                                html=exportar,
                                xml=exportar_xml,
                                json=exportar_json,
                                dados=dados,
                                subitems=None,
                                add=1)

            return ("Conteudo editado com sucesso! "
                    "Publica&ccedil;&atilde;o iniciada.")

        self._addLog("Conteudo editado '%s'" % titulo)
        return "Conteudo editado com sucesso."

    @dbconnectionapp
    def _getEstados(self):
        """
        retorna os estados
        """
        return self.execSql("select_estados")
