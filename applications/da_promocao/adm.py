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


from datetime import datetime
from time import time, strftime, strptime

from publica.admin.error import UserError
from publica.utils.decorators import serialize, dbconnectionapp,\
                                     Permission, logportal
from publica.core.portal import Portal
from publica.utils.json import encode

class Adm(object):
    """
    """
    
    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def addPromocao(self, id_treeapp, id_aplicativo, titulo, publicado_em,
                    descricao=None, regulamento=None, imagem=None,
                    titulo_destaque=None, img_destaque=None,
                    descricao_destaque=None, imagem_destaque=None, tags=None, 
                    expira_em=None, publicado=None,
                    relacionamento=[], exportar=None, permissao=None,
                    exportar_json=None, exportar_xml=None):
        """
        Metodo chamado ao adicionar uma Promocao.
        """
        portal = Portal(id_site=self.id_site, request=self.request)
        id_conteudo = self.execSql("select_nextval_promocao").next()["id"]
        publicado = True if publicado else False
        tags = tags if tags else None
        dt = publicado_em

        try:
            p = strptime(publicado_em, '%d/%m/%Y %H:%M')
            publicado_em = strftime('%Y-%m-%d %H:%M', p)
        except ValueError:
            raise UserError(("Ocorreu um erro: "
                             " Data de publica&ccedil;&aring;o "
                             " inv&aacute;lida (%s)" % publicado_em))

        try:
            p = strptime(expira_em, "%d/%m/%Y %H:%M")
            expira_em = strftime("%Y-%m-%d %H:%M", p)
        except ValueError:
            expira_em = None

        id_imagem = portal.addArquivo(arquivo=imagem,
                             id_conteudo=id_conteudo,
                             schema=self.schema,
                             dt=dt)

        self.execSqlBatch("insert_promocao",
                          id_conteudo=id_conteudo,
                          titulo=titulo,
                          descricao=descricao,
                          regulamento=regulamento,
                          img_destaque=img_destaque,
                          publicado=publicado, 
                          publicado_em=publicado_em,
                          expira_em=expira_em,
                          imagem=id_imagem)

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
                            relacionamento=relacionamento)

        if exportar or exportar_xml or exportar_json:
            portal._insertLog(self.id_site,
                              ("Promo&ccedil;&atilde;o "
                               "'%s' adicionada e publicada") % titulo)
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
            return ("Promo&ccedil;&atilde;o adicionada com sucesso! "
                    "Publica&ccedil;&atilde;o iniciada.")

        portal._insertLog(self.id_site,
                          "Promo&ccedil;&atilde;o '%s' adicionada" % titulo)
        return "Promo&ccedil;&atilde;o adicionada com sucesso!"


    @dbconnectionapp
    def _getPromocao(self, id_conteudo):
        """
        Retorna os dados de uma promocao.
        """
        promocao = {"promocao":None}
        for i in self.execSql("select_promocao", id_conteudo=int(id_conteudo)):
            promocao["promocao"] = i

        return promocao


    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def editPromocao(self, id_conteudo=None, id_treeapp=None, id_aplicativo=None,
                     publicado_em=None,
                     titulo_destaque=None, imagem_destaque=None, imagem=None,
                     titulo=None, descricao_destaque=None, regulamento=None,
                     id_destaque=None,
                     expira_em=None, publicado=None, relacionamento=[],
                     exportar=None, tags=None, permissao=None, descricao=None,
                     exportar_json=None, exportar_xml=None):
        """
        Edita os dados de uma promocao.
        """
        portal = Portal(id_site=self.id_site, request=self.request)
        publicado = True if publicado else False
        tags = tags if tags else None
        dt = publicado_em

        try:
            p = strptime(publicado_em, "%d/%m/%Y %H:%M")
            publicado_em = strftime("%Y-%m-%d %H:%M", p)
        except ValueError:
            raise UserError("Ocorreu um erro: "
                            "Data de publica&ccedil;&aring;o "
                            "inv&aacute;lida (%s)" % publicado_em)
        try:
            p = strptime(expira_em, "%d/%m/%Y %H:%M")
            expira_em = strftime("%Y-%m-%d %H:%M", p)
        except ValueError:
            expira_em = None


        id_imagem = portal.addArquivo(arquivo=imagem,
                             id_conteudo=id_conteudo,
                             schema=self.schema,
                             dt=dt)

        self.execSqlBatch("update_promocao",
                          id_conteudo=int(id_conteudo),
                          titulo=titulo,img_destaque=imagem_destaque,
                          publicado=publicado, publicado_em=publicado_em,
                          expira_em=expira_em, regulamento=regulamento,
                          descricao=descricao, imagem=imagem)

        if titulo_destaque or imagem_destaque or descricao_destaque:
            if not imagem_destaque:
                imagem_destaque = None
            else:
                imagem_destaque = portal.addArquivo(arquivo=imagem_destaque,
                                                    id_conteudo=id_conteudo,
                                                    schema=self.schema,
                                                    dt=dt)

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
                             relacionamento=relacionamento)


        if exportar or exportar_xml or exportar_json:
            portal._insertLog(self.id_site,
                              "Promo&ccedil;&atilde;o '%s' editada" % titulo)
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
            return ("Promo&ccedil;&atilde;o editada com sucesso! "
                    "Publica&ccedil;&atilde;o iniciada.")

        portal._insertLog(self.id_site,
                          "Promo&ccedil;&atilde;o '%s' editada" % titulo)
        return "Promo&ccedil;&atilde;o editada com sucesso!"
        
        
    @dbconnectionapp
    def _get_usuarios(self, id_conteudo):
        """
            Retorna os usuarios de uma promocao cadastrada
        """
        return self.execSql("select_usuarios_p", id_conteudo=int(id_conteudo))

    
    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def edit_sorteio(self, id_conteudo=None, tipo_sorteio=None,
                           data_sorteio=None, num_sorteados=None,
                           id_site=None, retirada=None):
        """
        edita os dados do sorteio.
        """
        portal = Portal(id_site=self.id_site, request=self.request)
        try:
            p = strptime(data_sorteio, "%d/%m/%Y %H:%M")
            data_sorteio = strftime("%Y-%m-%d %H:%M", p)
        except ValueError:
            raise UserError("Ocorreu um erro: "
                            "Data de sorteio "
                            "inv&aacute;lida (%s):" % data_sorteio)

        self.execSqlu("update_sorteio", id_conteudo=int(id_conteudo),
                      data_sorteio=data_sorteio, num_sorteados=num_sorteados,
                      tipo_sorteio=tipo_sorteio, retirada=retirada)
        # TODO log
        return "Sorteio editado com sucesso."
   
 
    @dbconnectionapp
    def _get_usuario(self, id_usuario):
        """
            Retorna os dados de um usuario
        """
        for i in self.execSql("select_usuario", id_usuario=int(id_usuario)):
            return i


    @dbconnectionapp
    def _get_sorteados(self, id_conteudo):
        """
            Retorna os sorteados de uma promocao
        """
        return self.execSql("select_sorteados", id_conteudo=int(id_conteudo))

        
    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def del_usuario_p(self, id_conteudo=None, id_usuario_promocao=None,
                      nome=None, titulo=None):
        """
            Deleta usuario de uma promocao
        """
        for i in id_usuario_promocao:
            self.execSqlBatch("delete_usuario_p",
                              id_usuario_promocao=int(i))
        
        portal = Portal(id_site = self.id_site, request = self.request)
        portal._insertLog(self.id_site,
                  "Usu&aacute;rio {0} exclu&iacute;do "
                  "da promo&ccedil;&atilde;o: {1}".format(nome, titulo))
        
        self.execSqlCommit()
        
        return "Usu&aacute;rio(s) deletado(s) com sucesso."

    
    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def do_sorteio(self, id_conteudo=None, num_sorteados=None, titulo=None):
        """
            Executa o sorteio da promocao.
        """
        usuarios = self.execSql("select_usuarios_p", id_conteudo=int(id_conteudo))
        try:
            sorteados = self.sortear(cadastrados=usuarios, num_sorteados=int(num_sorteados))
        except ValueError:
            raise UserError("Ocorreu um erro: "
                            "N&uacute;mero de sortados maior que o de concorrentes. ")
        for sorteado in sorteados:
            self.execSqlBatch("insert_sorteados", id_usuario=sorteado['id_usuario'],
                          id_conteudo=id_conteudo, nome=sorteado['nome'])

        self.execSqlu("update_sorteado", id_conteudo=int(id_conteudo))
        self.execSqlCommit()

        portal = Portal(id_site = self.id_site, request = self.request)
        portal._insertLog(self.id_site,
                  "Promo&ccedil;&atilde;o '%s' sorteada" % titulo)
        
        return "Sorteio realizado."


    @dbconnectionapp
    def inserir_usuario_promocao(self, id_conteudo=None, id_usuario=None,
                                 nome=None):
        """
            Insere um usuario cadastrado em uma promocao
        """
        
        self.execSqlBatch("insert_usuario_promocao", 
                          id_conteudo=int(id_conteudo),
                          id_usuario=int(id_usuario), 
                          nome=nome)
        self.execSqlCommit()
        return "Usuario cadastrado na promocao"

    @serialize
    @dbconnectionapp
    def inserir_usuario(self, nome=None, email=None, sexo=None, identidade=None,
                        telefone=None, cidade=None, estado=None):
        """
            Cadastra um usuario.
        """
        self.execSqlBatch("insert_usuario", nome=nome, email=email, sexo=sexo,
                          identidade=identidade, telefone=telefone,
                          cidade=cidade, estado=estado)
        self.execSqlCommit()
        return "Usuario cadastrado"


    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def get_primeiros(self, id_conteudo, num_sorteados, titulo=None):
        """
            Retorna os primeiros a se cadastrarem na promocao.
        """

        cadastrados = self.execSql("select_usuario_data", id_conteudo=id_conteudo)
        x=0
        for cadastrado in cadastrados:
            if x < int(num_sorteados):
                self.execSqlBatch("insert_sorteados", id_conteudo=int(id_conteudo),
                                  nome=cadastrado['nome'], id_usuario=cadastrado['id_usuario'])
                x=x+1
            else:
                break

        self.execSqlu("update_sorteado", id_conteudo=int(id_conteudo))
        self.execSqlCommit()

        portal = Portal(id_site = self.id_site, request = self.request)
        portal._insertLog(self.id_site,
                  "Promo&ccedil;&atilde;o '%s' sorteada" % titulo)
        return "Sorteio realizado."
