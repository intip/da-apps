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
import operator
import random
from time import strftime, strptime
from publica.admin.error import UserError
from datetime import datetime, timedelta
from publica.core.portal import Portal
from publica import settings
from publica.admin.exchange import getDadosSite
from publica.utils.decorators import serialize, dbconnectionapp,\
                                     Permission, jsoncallback
from publica.utils import util


class Adm(object):
    """
    """
    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def addConteudo(self, id_site, id_treeapp, id_aplicativo,
                    titulo, descricao, vigencia_de, vigencia_ate,
                    resultado, id_regulamento, publicado_em,
                    tipo, expira_em=None, publicado=None,
                    titulo_destaque=None, descricao_destaque=None,
                    imagem_destaque=None, peso_destaque=None,
                    relacionamento=[], tags="", permissao=None,
                    exportar_xml=None, exportar_json=None,
                    exportar=None, categoria=None, servico=None,
                    extra=None, num_sorteados=None):
        """
            add new content
        """
        publicado = True if publicado else False
        tags = tags if tags else None
        dt = publicado_em
        publicado_em = self.formataData(publicado_em)
        vigencia_de = self.formataData(vigencia_de)
        vigencia_ate = self.formataData(vigencia_ate)
        resultado = self.formataData(resultado)

        try:
            p = strptime(expira_em, "%d/%m/%Y %H:%M")
            expira_em = strftime("%Y-%m-%d %H:%M", p)
        except ValueError, e:
           expira_em = None

        # inserir conteudo
        id_conteudo = self.execSql("select_nextval_conteudo").next()["id"]

        self.execSqlBatch("insert_conteudo",
                          id_conteudo=id_conteudo,
                          titulo=titulo,
                          descricao=descricao,
                          vigencia_de=vigencia_de,
                          vigencia_ate=vigencia_ate,
                          resultado=resultado,
                          tipo=tipo,
                          id_regulamento=int(id_regulamento),
                          servico=servico,
                          num_sorteados=num_sorteados,
                          extra=extra,
                          categoria=categoria,
                          publicado_em=publicado_em,
                          expira_em=expira_em,
                          publicado=publicado)

        # inserindo os destaques
        dados_destaque = []
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

    def formataData(self, data):
        """
            formata a data para inserir no banco
        """
        try:
            p = strptime(data, "%d/%m/%Y %H:%M")
            newdata = strftime("%Y-%m-%d %H:%M", p)
            return newdata
        except ValueError, e:
            raise UserError(("Ocorreu um erro: "
                             "Data inv&aacute;lida (%s)") % data)

    @dbconnectionapp
    @Permission("PERM APP")
    def _getConteudo(self, id_conteudo=None):
        """
        """
        if id_conteudo:
            for i in self.execSql("select_conteudo",
                                  id_conteudo=int(id_conteudo)):
                return i
        else:
            return self.execSql("select_conteudos")


    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def editConteudo(self, id_conteudo, id_site, id_treeapp, id_aplicativo,
                           titulo, descricao, vigencia_de, vigencia_ate,
                           resultado, id_regulamento, publicado_em,
                           tipo, expira_em=None, publicado=None,
                           titulo_destaque=None, descricao_destaque=None,
                           imagem_destaque=None, peso_destaque=None,
                           relacionamento=[], tags="", permissao=None,
                           exportar_xml=None, exportar_json=None,
                           exportar=None, categoria=None, servico=None,
                           extra=None, num_sorteados=None):
        """
            edit content
        """
        dt = publicado_em
        publicado = True if publicado else False
        tags = tags if tags else None
        publicado_em = self.formataData(publicado_em)
        vigencia_de = self.formataData(vigencia_de)
        vigencia_ate = self.formataData(vigencia_ate)
        resultado = self.formataData(resultado)
        count = self._getCountUsersSorteados(id_conteudo=int(id_conteudo))
        try:
            p = strptime(expira_em, "%d/%m/%Y %H:%M")
            expira_em = strftime("%Y-%m-%d %H:%M", p)
        except ValueError, e:
           expira_em = None

        # deletar conteudo tabela destaques ou outras tabelas
        self.execSqlBatch("delete_destaque",
                          id_conteudo=int(id_conteudo))

        self.execSqlBatch("update_conteudo",
                          id_conteudo=int(id_conteudo),
                          titulo=titulo,
                          descricao=descricao,
                          vigencia_de=vigencia_de,
                          vigencia_ate=vigencia_ate,
                          resultado=resultado,
                          id_regulamento=int(id_regulamento),
                          tipo=tipo,
                          num_sorteados=num_sorteados,
                          categoria=categoria,
                          servico=servico,
                          extra=extra,
                          publicado_em=publicado_em,
                          expira_em=expira_em,
                          publicado=publicado)

        # inserindo os destaques
        dados_destaque = []
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
        if int(count) == 0:
            self.alterStatusPromocao(id_conteudo, 'false')
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
                                edit=1)
            if int(count) > 0:
                self.alterStatusPromocao(id_conteudo, 'true')
            return ("Conteudo editado com sucesso! "
                    "Publica&ccedil;&atilde;o iniciada.")

        self._addLog("Conteudo editado '%s'" % titulo)
        return "Conteudo editado com sucesso."

    @dbconnectionapp
    @jsoncallback
    @Permission("PERM APP")
    def addRegulamento(self, titulo, regulamento):
        """
            adiciona novo regulamento callback
        """
        self.execSqlu("insert_regulamento",
                      titulo=titulo,
                      regulamento=regulamento)
        return "Regulamento adicionado com sucesso"

    @jsoncallback
    @Permission("PERM APP")
    def getRegulamentos(self):
        """
           retorna regulamentos com callback
        """
        return self._getRegulamentos()

    @dbconnectionapp
    @jsoncallback
    @Permission("PERM APP")
    def delRegulamento(self, id_regulamento):
        """
            deleta um regulamento callback
        """
        self.execSqlu("delete_regulamento",
                       id_regulamento=int(id_regulamento))
        return "Regulamento deletado com sucesso"

    @dbconnectionapp
    @jsoncallback
    @Permission("PERM APP")
    def editRegulamento(self, id_regulamento, titulo, regulamento):
        """
            edita um regulamento callback
        """
        self.execSqlu("update_regulamento",
                       id_regulamento=int(id_regulamento),
                       titulo=titulo,
                       regulamento=regulamento)
        return "Regulamento editado com sucesso"

    @dbconnectionapp
    @jsoncallback
    def getUsuarioDado(self, dado, id_conteudo=None, blacklist=None):
        """
           retorna usuario pelo dado enviado
        """
        index = dado.find("@")
        cpf = False
        try:
            valid = dado.replace('.','').replace('-','')
            int(valid)
            if len(valid) == 11:
                cpf = True
        except:
            pass
        res = []
        if not id_conteudo and not blacklist:

            if index != -1:
                qtde = list(self.execSql("select_count_user_email",
                                          email=dado))[0]["count"]
                for i in self.execSql("select_usuario_email",
                                      email=dado):
                    i["nome"] = i["nome"].decode("utf8").encode("latin1")
                    res.append(i)
            elif cpf :
                qtde = list(self.execSql("select_count_user_cpf",
                                          cpf=dado))[0]["count"]
                for i in self.execSql("select_user_cpf",
                                       cpf=dado):
                    i["nome"] = i["nome"].decode("utf8").encode("latin1")
                    res.append(i)
            else:
                qtde = list(self.execSql("select_count_user_nome",
                                          nome=dado))[0]["count"]
                for i in self.execSql("select_usuario_nome",
                                      nome=dado):
                    i["nome"] = i["nome"].decode("utf8").encode("latin1")
                    res.append(i)
        elif id_conteudo and not blacklist:

            if index != -1:
                qtde = list(self.execSql("select_count_user_email_id_conteudo",
                                          email=dado,
                                          id_conteudo=int(id_conteudo)))[0]["count"]
                for i in self.execSql("select_user_email_id_conteudo",
                                       email=dado,
                                       id_conteudo=int(id_conteudo)):
                    i["nome"] = i["nome"].decode("utf8").encode("latin1")
                    res.append(i)
            elif cpf:
                qtde = list(self.execSql("select_count_user_cpf_id_conteudo",
                                          cpf=dado,
                                          id_conteudo=int(id_conteudo)))[0]["count"]
                for i in self.execSql("select_user_cpf_id_conteudo",
                                       cpf=dado,
                                       id_conteudo=int(id_conteudo)):
                    i["nome"] = i["nome"].decode("utf8").encode("latin1")
                    res.append(i)

            else:

                qtde = list(self.execSql("select_count_user_nome_id_conteudo",
                                          nome=dado,
                                          id_conteudo=int(id_conteudo)))[0]["count"]
                for i in self.execSql("select_user_nome_id_conteudo",
                                        nome=dado,
                                        id_conteudo=int(id_conteudo)):
                    i["nome"] = i["nome"].decode("utf8").encode("latin1")
                    res.append(i)

        return {"res":res, "qtde":qtde}


    @jsoncallback
    def getUsuariosParticipantes(self, limit, offset, id_conteudo=None, blacklist=None):
        """
            retorna usuarios callback
        """
        return self._getUsuariosParticipantes(limit=limit,
                                              offset=offset,
                                              id_conteudo=id_conteudo,
                                              blacklist=blacklist)

    @dbconnectionapp
    @Permission("PERM APP")
    def _getRegulamentos(self):
        """
            retorna todos regulamentos
        """
        regulamentos = []
        for i in self.execSql("select_regulamentos"):
            regulamentos.append(i)
        return regulamentos

    @dbconnectionapp
    @Permission("PERM APP")
    def _getUsuariosParticipantes(self, limit, offset, id_conteudo=None, blacklist=None):
        """
            Retorna usuarios Participantes
        """
        result = []
        if id_conteudo and not blacklist:
            for i in self.execSql("select_usuario_promocao_id_conteudo",
                                  limit=int(limit),
                                  offset=int(offset),
                                  id_conteudo=int(id_conteudo)):
                i["nome"] = i["nome"].decode("utf8").encode("latin1")
                result.append(i)
            qtde = self._getCountUsers(id_conteudo)

        elif id_conteudo and blacklist:
            for i in self.execSql("select_usuario_promocao_blackid",
                                   limit=int(limit),
                                   offset=int(offset),
                                   id_conteudo=int(id_conteudo)):
                i["nome"] = i["nome"].decode("utf8").encode("latin1")
                result.append(i)
            qtde = self._getCountUsers(id_conteudo, blacklist)

        elif blacklist and not id_conteudo:
            for i in self.execSql("select_usuario_blacklist",
                                   limit=int(limit),
                                   offset=int(offset)):
                i["nome"] = i["nome"].decode("utf8").encode("latin1")
                result.append(i)
            qtde = self._getCountUsers(bloqueio=blacklist)

        else:
            for i in self.execSql("select_usuarios_promocoes",
                                   limit=int(limit),
                                   offset=int(offset)):
                i["nome"] = i["nome"].decode("utf8").encode("latin1")
                result.append(i)
            qtde = self._getCountUsers()

        return {"res":result, "qtde":qtde}

    @dbconnectionapp
    @Permission("PERM APP")
    def _getUsuario(self, id_usuario):
        """
            Retorna apenas um usuario,
            os dados do usuario vinculado ao
            email e também as frases caso
            haja
        """
        for i in self.execSql("select_usuario",
                               id_usuario=int(id_usuario)):
            dados_pai = self._getDadosUsuario(i['email'])
            i['cpf_pai'] = dados_pai['cpf_cnpj']
            i['nome_pai'] = dados_pai['nome']
            i["nome"] = i["nome"].decode("utf8").encode("latin1")
            i["endereco"] = i["endereco"]
            if i["frase"]:
                i["frase"] = i["frase"].decode("utf8").encode("latin1")
            return i

    def _getCountUsers(self, id_conteudo=None, bloqueio=None):
        """
            Retorna total de usuario
        """
        if id_conteudo and not bloqueio:
            qtde = list(self.execSql("select_count_usuario_promocao",
                                     id_conteudo=int(id_conteudo)))[0]["count"]
        elif id_conteudo and bloqueio:
            qtde = list(self.execSql("select_usuario_promocao_blackid_count",
                                      id_conteudo=int(id_conteudo)))[0]["count"]

        elif bloqueio and not id_conteudo:
            qtde = list(self.execSql("select_usuario_blacklist_count"))[0]["count"]

        else:
            qtde = list(self.execSql("select_count_usuario_total"))[0]["count"]
        return qtde

    def _getCountParticipacoes(self, id_conteudo):
        """
            Retorna o n de participaçoes de uma promocao
        """
        qtde = list(self.execSql("select_count_participacoes_promocao",
                    id_conteudo=int(id_conteudo)))[0]["count"]

        return qtde

    @jsoncallback
    @Permission("PERM APP")
    def getFraseParticipantes(self, id_conteudo, offset=0, limit=None):
        """
            retorna as frases do Parcipantes callback
        """
        return self._getFraseParticipantes(id_conteudo, offset, limit)

    @dbconnectionapp
    def _getFraseParticipantes(self, id_conteudo, offset=0, limit=None):
        """
            retorna frase dos Participantes
        """
        result = []
        if not limit:
            for i in self.execSql("select_frases_participantes",
                               id_conteudo=int(id_conteudo)):
                i['frase'] = i["frase"].decode("utf8").encode("latin1") if i['frase'] else ''
                i['nome'] = i["nome"].decode("utf8").encode("latin1")
                result.append(i)
        else:
            for i in self.execSql("select_frases_participantes_limit",
                                  id_conteudo=int(id_conteudo),
                                  limit=int(limit),
                                  offset=int(offset)):
                i['frase'] = i["frase"].decode("utf8").encode("latin1") if i['frase'] else ''
                i['nome'] = i["nome"].decode("utf8").encode("latin1")
                result.append(i)
        return result


    @dbconnectionapp
    @Permission("PERM APP")
    def _getCountUsersSorteados(self, id_conteudo=None, desclassificados=None):
        """
            retorna o count dos users Sorteados
        """
        if id_conteudo and not desclassificados:
            qtde = list(self.execSql("select_count_sorteados_promocao",
                                     id_conteudo=int(id_conteudo)))[0]["count"]
        elif id_conteudo and desclassificados:
            qtde = list(self.execSql("select_sorteados_promocao_desclassificados_count",
                                      id_conteudo=int(id_conteudo)))[0]["count"]

        elif desclassificados and not id_conteudo:
            qtde = list(self.execSql("select_sorteados_desclassificados_count"))[0]["count"]

        else:
            qtde = list(self.execSql("select_count_sorteados_total"))[0]["count"]
        return qtde


    @dbconnectionapp
    @jsoncallback
    @Permission("PERM APP")
    def bloqUser(self, email):
        """
            bloqueia usuario
        """
        self.execSqlu("update_blacklist_user",
                      email=email)
        return "usu&aacute;rio bloqueado com sucesso"

    @dbconnectionapp
    @jsoncallback
    @Permission("PERM APP")
    def desbloqUser(self, email):
      """
        desbloqueia usuario
      """
      self.execSqlu("update_blacklist_user_desbloq",
                     email=email)
      return "usu&aacute;rio desbloqueado com sucesso"


    @dbconnectionapp
    @jsoncallback
    @Permission("PERM APP")
    def getUsuariosSorteados(self, limit, offset, id_conteudo=None,
                             desclassificados=None):
        """
          retorna usuario Sorteados ou
          desclassificados
        """
        return self._getusuariosSorteados(limit=limit,
                                         offset=offset,
                                         id_conteudo=id_conteudo,
                                         desclassificados=desclassificados)

    @jsoncallback
    @Permission("PERM APP")
    def addSorteadoConcurso(self, id_conteudo, ids=[]):
        """
            post de sorteio cultural
        """
        if type(ids) is list:
            for i in ids:
                self._addSorteado(id_conteudo, i)
        else:
            self._addSorteado(id_conteudo, ids)

        return "Sorteados adicionado com sucesso"

    @dbconnectionapp
    @Permission("PERM APP")
    def _addSorteado(self, id_conteudo, id_usuario):
        """
            add new sorteado
        """
        self.execSqlu("insert_sorteado",
                       id_conteudo=int(id_conteudo),
                       id_usuario=int(id_usuario),
                       dia_hora=datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.execSqlu("update_status_user_promocao",
                       id_conteudo=int(id_conteudo),
                       id_usuario=int(id_usuario),
                       status='sorteado')


    @dbconnectionapp
    @Permission("PERM APP")
    def alterStatusPromocao(self, id_conteudo, finalizada="false"):
        """
            altera o status da promocao
        """
        self.execSqlu("update_status_promocao",
                       id_conteudo=int(id_conteudo),
                       finalizada=finalizada)



    @dbconnectionapp
    @Permission("PERM APP")
    def _getusuariosSorteados(self, limit, offset, id_conteudo=None,
                             desclassificados=None):
        """
          retorna usuario Sorteados ou
          desclassificados
        """
        result = []
        if id_conteudo and not desclassificados:
            for i in self.execSql("select_sorteados_promocao",
                                  limit=int(limit),
                                  offset=int(offset),
                                  id_conteudo=int(id_conteudo)):
                i["nome"] = i["nome"].decode("utf8").encode("latin1")
                result.append(i)
            qtde = self._getCountUsersSorteados(id_conteudo)

        elif id_conteudo and desclassificados:
            for i in self.execSql("select_desclassificados_promocao",
                                   limit=int(limit),
                                   offset=int(offset),
                                   id_conteudo=int(id_conteudo)):
                i["nome"] = i["nome"].decode("utf8").encode("latin1")
                result.append(i)
            qtde = self._getCountUsersSorteados(id_conteudo, desclassificados)

        elif desclassificados and not id_conteudo:
            for i in self.execSql("select_desclassificados",
                                   limit=int(limit),
                                   offset=int(offset)):
                i["nome"] = i["nome"].decode("utf8").encode("latin1")
                result.append(i)
            qtde = self._getCountUsersSorteados(desclassificados=desclassificados)

        else:
            for i in self.execSql("select_sorteados",
                                   limit=int(limit),
                                   offset=int(offset)):
                i["nome"] = i["nome"].decode("utf8").encode("latin1")
                result.append(i)
            qtde = self._getCountUsersSorteados()

        return {"res":result, "qtde":qtde}


    @dbconnectionapp
    @jsoncallback
    @Permission("PERM APP")
    def desclassificaUser(self, id_usuario, id_conteudo):
        """
            desclassifica usuario atraves do id_usuario
            para a promoçao informada
        """
        dados = self._getConteudo(id_conteudo)
        if dados['tipo'] != 'cultural':
            id_new = self._sortUser(id_conteudo, 1)
            if id_new:
                for i in id_new:
                    self._addSorteado(id_conteudo, i['id_usuario'])
            else:
                return {"error":"usuario n&atilde;o pode ser desclassificado,"
                        " por nao ter outro que se encaixam nas regras"
                        " para substitui-lo"}

        self.execSqlu("update_status_user_promocao",
                          id_conteudo=int(id_conteudo),
                          id_usuario=int(id_usuario),
                          status='desclassificado')

        self.execSqlu("delete_user_sorteado",
                       id_usuario=int(id_usuario))

        return {"ok":"desclassificado com sucesso"}


    @dbconnectionapp
    @jsoncallback
    @Permission("PERM APP")
    def classificarUser(self, id_usuario, id_conteudo):
        """
            classifica usuario atraves do email
            para a promoçao informada
        """

        self.execSqlu("update_status_user_promocao",
                       id_conteudo=int(id_conteudo),
                       id_usuario=int(id_usuario),
                       status='livre')

        return "classificado com sucesso"

    @dbconnectionapp
    @Permission("PERM APP")
    def _sortUser(self, id_conteudo, limit=None):
        """
            retorna dados do
            User sorteado
        """
        dados = self._getConteudo(id_conteudo)
        if not limit:
            limit= int(dados['num_sorteados'])
        data = datetime.now() - timedelta(days=int(self.bloqueio_numero))
        data = data.strftime("%Y-%m-%d %H:%M")
        if dados['tipo'] == 'cadastro':
            if self.tipo_bloqueio == 'periodo':
                ids = list(self.execSql("select_sorteio_primeiro_cadastrar",
                                        id_conteudo=int(id_conteudo),
                                        limit=limit,
                                        data=data))
            else:
                ids = list(self.execSql("select_sorteio_primeiro_cadastrar_prom",
                                        id_conteudo=int(id_conteudo),
                                        limit=limit,
                                        bloqueio_numero=int(self.bloqueio_numero)))

            get_id = operator.itemgetter('id_usuario')
            ids.sort(key=get_id)

        else:
            if self.tipo_bloqueio == 'periodo':
                result = list(self.execSql("select_sorteio_aleatorio",
                                           id_conteudo=int(id_conteudo),
                                           data=data))
            else:
                result = list(self.execSql("select_sorteio_aleatorio_prom",
                                           id_conteudo=int(id_conteudo),
                                           bloqueio_numero=int(self.bloqueio_numero)))

            random.shuffle(result)
            ids = []
            for i in range(len(result)):
                if i >= limit:
                    break
                else:
                    ids.append(result[i])
        try:
            ids = ids if ids[0]['id_usuario'] != None else []
        except IndexError, e:
            ids = []
        if (len(ids) >= int(dados['num_sorteados'])):
            return ids
        else:
            ids = []
            return ids

    @jsoncallback
    @Permission("PERM APP")
    def sorteiaUser(self, id_conteudo, limit=None):
        """
            adiciona um novo sorteado
            promocoes random jsoncallback
        """

        ids = self._sortUser(id_conteudo, limit)
        if ids:
            for i in ids:
                self._addSorteado(id_conteudo, i['id_usuario'])

            return {"ok":"Usuários sorteados com sucesso"}
        else:
            return {"error":"N&atilde;o h&aacute usu&aacute;rios suficientes que se "
                            "encaixam nas regras da promo&ccedil;&atilde;o"}

    def _sorteiaUser(self, id_conteudo, limit=None):
        """
            adiciona um novo sorteado
            promocoes random
        """

        ids = self._sortUser(id_conteudo, limit)
        if ids:
            for i in ids:
                self._addSorteado(id_conteudo, i['id_usuario'])

            return "ok:Usuarios sorteados com sucesso"
        else:
            return "error:Nao ha usuarios suficientes"


    def _publicaContent(self, id_conteudo, id_aplicativo=None, id_treeapp=None):
        """
            publica o conteudo
        """

        portal = Portal(id_site=self.id_site, request=self.request)
        dados = self._setDados(id_conteudo=id_conteudo)
        try:
            self.execSqlu("update_publicacao_promocao",
                           id_conteudo=int(id_conteudo))
            portal._exportarFormatosConteudo(id_aplicativo=id_aplicativo,
                                             id_conteudo=id_conteudo,
                                             schema=self.schema,
                                             id_treeapp=id_treeapp,
                                             html=1,
                                             xml=None,
                                             json=None,
                                             dados=dados,
                                             subitems=None,
                                             add=1)
            return {"ok":"Publicado com sucesso"}
        except Exception as e:
            return {"error":e}

    @jsoncallback
    @Permission("PERM APP")
    def publicaConteudo(self, id_conteudo, id_aplicativo=None, id_treeapp=None):
        """
            publica o conteudo
        """
        self.alterStatusPromocao(id_conteudo, 'true')
        return self._publicaContent(id_conteudo,
                                    id_aplicativo,
                                    id_treeapp)

    @dbconnectionapp
    @Permission("PERM APP")
    def makeXLS(self, id_relatorio, id_promocao=None):
        """
        cria o arquivo xls
        a var index é utilizada para
        controlar em qual linha entrara o conteudo
        """
        timename = str(util.dtnow('%d/%m/%Y %H:%M%S')).replace("/", "")
        timename = timename.replace(":", "")
        timename = "_" + timename.replace(" ", "")
        site = getDadosSite(id_site=self.id_site,
                            request=self.request)
        base = site["base_app"]
        if not base.endswith("/"):
            base = base + "/"
        if int(id_relatorio) == 1:
            titulo = 'Relacao_usuario_participacao'
        elif int(id_relatorio) == 2:
            titulo = 'Relacao_participantes_contemplados'
        elif int(id_relatorio) == 4:
            titulo = 'Dados_usuarios_por_promocao'
        else:
            titulo = 'Relacao_participantes_promocao'
        saveplace = ("{0}/ns{1}/arquivos/tmp/"
                     "{2}{3}.xls").format(str(settings.PATH_FILES),
                                          str(self.id_site),
                                          titulo,
                                          timename)
        saveurl = "{0}tmp/{1}{2}.xls".format(
            base, titulo, timename)
        book = Workbook()
        font = Font()
        font.bold = True
        style = XFStyle()
        style.font = font
        style0 = XFStyle()
        style0.font = font

        alignment = Alignment()
        alignment.horz = Alignment.HORZ_CENTER
        style0.alignment = alignment

        pattern = Pattern()
        pattern.pattern = Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 22
        style0.pattern = pattern
        index = 0
        sheet = book.add_sheet('promocoes')
        # sheet
        if int(id_relatorio) == 1 or int(id_relatorio) == 3:
            promocoes = self._getConteudo()
            if int(id_relatorio) == 1:
                campos_s1 = [{"nome": "Nome"},
                             {"email": "email"},
                             {"cpf": "CPF"},
                             {"quantidade de participacoes": u"Quantidade de participações"},
                             {"status":"status"},
                             {"bloqueio":"bloqueado"}]
                sheet.write_merge(0, 0, 0, 5, u"Relação usuário participação por promoção", style0)
            else:
                campos_s1 = [{"nome":"Nome"},
                             {"email":"email"},
                             {"cpf":"CPF"},
                             {"telefone":"Telefone"},
                             {"endereco":u"Endereço"},
                             {"data_hora":u"Hora participação"}]
                sheet.write_merge(0, 0, 0, 5, u"Dados de usuários por promoção", style0)
            total_geral = 0
            count = 0
            for i in promocoes:
                count_participacoes = self._getCountParticipacoes(i['id_conteudo'])
                count += count_participacoes
                index += 1
                titulo = i['titulo']
                sheet.write_merge(index, index, 0, 5, titulo.decode("latin1"), style0)
                index += 1
                for j in range(len(campos_s1)):
                    sheet.write(index, j, campos_s1[j].values()[0], style)
                    sheet.col(j).width = 30 * 256

                cont = 0
                if int(id_relatorio) == 1:
                    for y in self.execSql("select_usuarios_promocoes_all",
                                           id_conteudo=int(i['id_conteudo'])):
                        sheet.write(index + 1,
                                    0,
                                    self.dec(y['nome']))
                        sheet.write(index + 1,
                                    1,
                                    self.dec(y['email']))
                        sheet.write(index + 1,
                                    2,
                                    self.dec(y['cpf']))
                        sheet.write(index + 1,
                                    3,
                                    self.dec(y['total']))
                        sheet.write(index + 1,
                                     4,
                                     self.dec(y['status']))
                        if y['bloqueio']:
                            bloqueio = 'Sim'
                        else:
                            bloqueio = 'Não'
                        sheet.write(index + 1,
                                    5,
                                    self.dec(bloqueio))
                        index += 1
                        cont += 1
                if int(id_relatorio) == 3:
                    for y in self.execSql("select_usuarios_promocoes_all2",
                                          id_conteudo=int(i['id_conteudo'])):
                        endereco = "{0}, {1}, {2}, {3}, {4}". format(y['endereco'],
                                                                     y['numero'],
                                                                     y['bairro'],
                                                                     y['estado'],
                                                                     y['cep'])
                        sheet.write(index + 1,
                                    0,
                                    self.dec(y['nome']))
                        sheet.write(index + 1,
                                    1,
                                    self.dec(y['email']))
                        sheet.write(index + 1,
                                    2,
                                    self.dec(y['cpf']))
                        sheet.write(index + 1,
                                    3,
                                    self.dec(y['telefone']))
                        sheet.write(index + 1,
                                     4,
                                     self.dec(endereco))
                        sheet.write(index + 1,
                                    5,
                                    y['dhora_participacao'])
                        index += 1
                        cont += 1

                if cont:
                    index += 2
                    sheet.write(index, 0, 'Total', style)
                    sheet.write(index,
                                1,
                                cont)
                    total_geral += cont
                    index += 1
                    sheet.write(index, 0, u'Total Participações', style)
                    sheet.write(index,
                                1,
                                count_participacoes)

                else:
                    index += 2
                    sheet.write(index, 0, 'Total', style)
                    sheet.write(index,
                                1,
                                cont)
                    index += 2



            index += 6
            sheet.write_merge(index, index, 0, 1, "Total Geral", style0)
            index += 1
            sheet.write(index, 0, "Total de Participantes", style)
            sheet.write(index, 1, self.dec(total_geral), style)
            index += 1
            sheet.write(index, 0, u"Total de Participações Geral", style)
            sheet.write(index, 1, self.dec(count), style)

        else:
            if int(id_relatorio) == 4:
                cont = 0
                titulo_promo = self._getConteudo(id_promocao)['titulo']
                sheet.write_merge(0, 0, 0, 5, u"Relação de partcipantes da promoção " + titulo_promo.decode('latin1'), style0)
                campos_s1 = [{"nome":"Nome"},
                             {"email":"email"},
                             {"cpf":"CPF"},
                             {"telefone":"Telefone"},
                             {"endereco":u"Endereço"},
                             {"status":"Status"}
                             ]
                saveplace = ("{0}/ns{1}/arquivos/tmp/{2}{3}.xls").format(str(settings.PATH_FILES),
                                                str(self.id_site),
                                                unicode(titulo + '_' + titulo_promo, errors='ignore'),
                                                timename)
                saveurl = "{0}tmp/{1}{2}.xls".format(base, unicode(titulo + '_' + titulo_promo, errors='ignore'), timename)
                index += 1
                for j in range(len(campos_s1)):
                        sheet.write(index, j, campos_s1[j].values()[0], style)
                        sheet.col(j).width = 30 * 256
                for i in self.execSql("select_usuarios_promocoes_all2",
                                      id_conteudo=int(id_promocao)):
                    endereco = "{0}, {1}, {2}, {3}, {4}". format(i['endereco'],
                                                                 i['numero'],
                                                                 i['bairro'],
                                                                 i['estado'],
                                                                 i['cep'])
                    sheet.write(index + 1,
                                        0,
                                        self.dec(i['nome']))
                    sheet.write(index + 1,
                                        1,
                                        self.dec(i['email']))
                    sheet.write(index + 1,
                                        2,
                                        self.dec(i['cpf']))
                    sheet.write(index + 1,
                                        3,
                                        self.dec(i['telefone']))
                    sheet.write(index + 1,
                                        4,
                                        self.dec(endereco))
                    sheet.write(index + 1,
                                        5,
                                        self.dec(i['status']))
                    index += 1
                    cont += 1
            else:
                cont = 0
                sheet.write_merge(0, 0, 0, 5, u"Relação de usuários contemplados", style0)
                campos_s1 = [{"nome":"Nome"},
                             {"email":"email"},
                             {"cpf":"CPF"},
                             {"telefone":"Telefone"},
                             {"endereco":u"Endereço"},
                             {"Contemplações":u"Contemplações"}]
                index += 1
                for j in range(len(campos_s1)):
                        sheet.write(index, j, campos_s1[j].values()[0], style)
                        sheet.col(j).width = 30 * 256
                for i in self.execSql("select_contemplados"):
                    endereco = "{0}, {1}, {2}, {3}, {4}". format(i['endereco'],
                                                                 i['numero'],
                                                                 i['bairro'],
                                                                 i['estado'],
                                                                 i['cep'])
                    sheet.write(index + 1,
                                        0,
                                        self.dec(i['nome']))
                    sheet.write(index + 1,
                                        1,
                                        self.dec(i['email']))
                    sheet.write(index + 1,
                                        2,
                                        self.dec(i['cpf']))
                    sheet.write(index + 1,
                                        3,
                                        self.dec(i['telefone']))
                    sheet.write(index + 1,
                                        4,
                                        self.dec(endereco))

                    sheet.write(index + 1,
                                        5,
                                        self.dec(i['total']))
                    index += 1
                    cont += 1

            index += 6
            sheet.write(index, 0, u"Total de usuários", style)
            sheet.write(index, 1, self.dec(cont), style)

        book.save(saveplace)
        return saveurl

    def dec(self, var):
        """
            pass latin1 to utf-8
        """
        try:
            return var.decode("latin1")
        except:
            return var

