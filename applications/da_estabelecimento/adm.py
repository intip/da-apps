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

    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def addConteudo(self, id_conteudo=None, id_treeapp=None, id_aplicativo=None,
                    titulo_destaque=None, imagem_destaque=None, publicado=None,
                    relacionamento=[], titulo=None, descricao=None,
                    filiado=None, informacoes=None, imagem=None, tags=None,
                    publicado_em=None, expira_em=None, exportar=None,
                    id_destaque=None, exportar_xml=None, exportar_json=None,
                    descricao_destaque=None, permissao=None, tipo=None):
        """
        Metodo chamado ao adicionar um estabelecimento.
        """
        portal = Portal(id_site=self.id_site, request=self.request)
        id_conteudo = self.execSql("select_nextval_conteudo").next()["id"]
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

        

        self.execSqlBatch("insert_conteudo_", titulo=titulo, filiado=filiado,
                      descricao=descricao, informacoes=informacoes,
                      publicado=publicado,
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
            self.execSqlBatch("insert_destaque",
                              id_conteudo=int(id_conteudo),
                              titulo=titulo_destaque,
                              descricao=descricao_destaque,
                              img=imagem_destaque)
        self.execSqlCommit()
        
        try:
            for tipo_selecionado in tipo:
                tipo_selecionado = tipo_selecionado.strip('d')
                self.execSqlu("insert_tipo_conteudo", 
                              id_tipo=int(tipo_selecionado), 
                              id_conteudo=int(id_conteudo),
                              nome=self.getNomeTipo(int(tipo_selecionado)))
        except TypeError:
            raise UserError("Selecione ao menos um tipo de estabelecimento.")
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

        if exportar or exportar_xml or exportar_json:
            portal._insertLog(self.id_site,
                              "Estabelecimento '%s' editado" % titulo)
            portal._exportarFormatosConteudo(id_aplicativo=id_aplicativo,
                                             id_conteudo=id_conteudo,
                                             schema=self.schema,
                                             id_treeapp=id_treeapp,
                                             html=exportar,
                                             xml=exportar_xml,
                                             json=exportar_json,
                                             subitems=None,
                                             add=1)
            return ("Estabelecimento adicionado com sucesso! "
                    "Publica&ccedil;&atilde;o iniciada.")

        portal._insertLog(self.id_site,
                          "Estabelecimento '%s' adicionado" % titulo)
        return "Estabelecimento adicionado com sucesso!"


    @dbconnectionapp
    def _getConteudo(self, id_conteudo):
        """
            Retorna o conteudo de um estabelecimento
        """
        for i in self.execSql("select_conteudo", 
                              id_conteudo = int(id_conteudo)):
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
            Edita os dados de um estabelecimento
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
        
        self.execSqlu("delete_tipo_conteudo", id_conteudo=int(id_conteudo))

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
        try:
            for tipo_selecionado in tipo:
                tipo_selecionado = tipo_selecionado.strip('d')
                self.execSqlu("insert_tipo_conteudo", 
                                  id_tipo=int(tipo_selecionado), 
                                  id_conteudo=int(id_conteudo),
                                  nome=self.getNomeTipo(int(tipo_selecionado)))
        except TypeError:
            raise UserError("Selecione ao menos um tipo de estabelecimento.")
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
                              "Estabelecimento '%s' editado" % titulo)
            portal._exportarFormatosConteudo(id_aplicativo=id_aplicativo,
                                             id_conteudo=id_conteudo,
                                             schema=self.schema,
                                             id_treeapp=id_treeapp,
                                             html=exportar,
                                             xml=exportar_xml,
                                             json=exportar_json,
                                             subitems=None,
                                             add=1)
            return ("Estabelecimento editado com sucesso! "
                    "Publica&ccedil;&atilde;o iniciada.")

        portal._insertLog(self.id_site,
                          "Estabelecimento'%s' editado" % titulo)
        return "Estabelecimento editado com sucesso!"

    @dbconnectionapp
    def _getTitulo(self, id_conteudo):
        """
            Retorna o titulo de um estabelecimento
        """
        titulo = self.execSql("select_titulo", id_conteudo=int(id_conteudo))

        for i in titulo:
            return i['titulo']
    
    @dbconnectionapp
    def _getTipos(self):
        """
            Retorna os tipos de estabelecimento que constam no banco.
        """
        return self.execSql("select_tipos")
    
    @dbconnectionapp
    def getTipos(self):
        """
            Retuns JSON encoded establishment types.
        """
        return encode([i for i in self.execSql("select_tipos")])
    
    @serialize
    @dbconnectionapp
    @Permission("PERM APP")
    def addTipo(self, tipo=None):
        """
            Adiciona um tipo de estabelecimento.
        """
        self.execSqlu("insert_tipo", tipo=tipo)
        return "Categoria adicionada."
        
    @serialize
    @dbconnectionapp
    @Permission("PERM APP")
    def delTipo(self, tipo=None):
        """
            Deleta uma categoria de produto.
        """
        self.execSqlu("delete_tipo", tipo=tipo)
        return "Categoria deletada."
    
    @dbconnectionapp
    def _getTiposConteudo(self, id_conteudo=None):
        """
            Retorna os tipos de um conteudo
        """
        return self.execSql("select_tipo_conteudo", id_conteudo=int(id_conteudo))
        
    @dbconnectionapp
    def _getFiliais(self, id_conteudo=None):
        """
            Retorna as filiais de um estabelecimento
        """
        return self.execSql("select_filiais", id_conteudo=int(id_conteudo))
    
    @dbconnectionapp
    def _getTiposLista(self, id_conteudo):
        """
            Returns a list with all types in the DB.
        """
        lista = []
        for i in self.execSql("select_tipos_lista", 
                            id_conteudo=int(id_conteudo)):
            lista.append(str(i["id_tipo"]))
        return lista
    
    @dbconnectionapp
    def getRegioes(self):
        """
            Returns the regions in the DB
        """
        return self.execSql("select_regioes")
    
    @dbconnectionapp
    def _getFilial(self, id_filial=None):
        """
            Returns the data of a branch
        """
        for i in self.execSql("select_filial", id_filial=int(id_filial)):
            return i
    
    @serialize
    @dbconnectionapp
    @Permission("PERM APP")
    def editFilial(self, endereco=None,
                   site=None, 
                   telefone=None, 
                   capacidade=None, 
                   regiao=None, 
                   forma_pagamento=None, 
                   acesso_cadeirante = None, 
                   observacoes = None, 
                   lat = None, 
                   lng = None, 
                   htmlbalao = None, 
                   rua = None, 
                   numero = None, 
                   complemento = None, 
                   bairro = None, 
                   cep = None, 
                   cidade = None, 
                   estado = None, 
                   id_filial = None, 
                   icone = None, 
                   ):
        """
            Edit the data of a branch.
        """
        endereco = "{0}, n.{1}, {2}, {3}".format(rua, numero, cidade, estado)
        lat, lng = self.gerarMapa(endereco)
        self.execSqlu("update_filial", 
                      endereco=endereco, 
                      site=site, 
                      telefone=telefone, 
                      capacidade=int(capacidade), 
                      regiao=regiao, 
                      forma_pagamento=forma_pagamento, 
                      acesso_cadeirante=acesso_cadeirante, 
                      observacoes=observacoes, 
                      lat=float(lat), 
                      lng=float(lng), 
                      htmlbalao=htmlbalao, 
                      rua=rua, 
                      numero=numero, 
                      complemento=complemento, 
                      bairro=bairro, 
                      cep=cep, 
                      cidade=cidade, 
                      estado=estado, 
                      icone=icone, 
                      id_filial=int(id_filial))
        return "Filial editada com sucesso."
    
    @serialize
    @dbconnectionapp
    @Permission("PERM APP")
    def addFilial(self, endereco=None,
                   site=None, 
                   telefone=None, 
                   capacidade=None, 
                   regiao=None, 
                   forma_pagamento=None, 
                   acesso_cadeirante = None, 
                   observacoes = None, 
                   lat = None, 
                   lng = None, 
                   htmlbalao = None, 
                   rua = None, 
                   numero = None, 
                   complemento = None, 
                   bairro = None, 
                   cep = None, 
                   cidade = None, 
                   estado = None, 
                   id_conteudo = None 
                   ):
        """
            Add a branch.
        """
        endereco = "{0}, n.{1}, {2}, {3}".format(rua, numero, cidade, estado)
        lat, lng = self.gerarMapa(endereco)
        self.execSqlu("insert_filial", 
                      endereco=endereco, 
                      site=site, 
                      telefone=telefone, 
                      capacidade=int(capacidade), 
                      regiao=regiao, 
                      forma_pagamento=forma_pagamento, 
                      acesso_cadeirante=acesso_cadeirante, 
                      observacoes=observacoes, 
                      lat=float(lat), 
                      lng=float(lng), 
                      rua=rua, 
                      numero=numero, 
                      complemento=complemento, 
                      bairro=bairro, 
                      cep=cep, 
                      cidade=cidade, 
                      estado=estado, 
                      id_conteudo = int(id_conteudo)
                      )
        return "Filial adicionada com sucesso."
    
    @staticmethod
    def gerarMapa(endereco):
        url = "http://maps.google.com/maps/api/geocode/json?address={0}&sensor=false".format(endereco)
        url = url.decode('latin1').encode('UTF-8')
        f = urllib.urlopen(url)
        resultado = json.loads(f.read())
        try:
            lat = resultado['results'][0]['geometry']['location']['lat']
            lng = resultado['results'][0]['geometry']['location']['lng']
        except IndexError:
            raise UserError("Local n&atilde;o encontrado.")
        return lat, lng
    
    @serialize
    @dbconnectionapp
    @Permission("PERM APP")
    def editFilialSemMapa(self, endereco=None,
                           site=None, 
                           telefone=None, 
                           capacidade=None, 
                           regiao=None, 
                           forma_pagamento=None, 
                           acesso_cadeirante = None, 
                           observacoes = None, 
                           lat = None, 
                           lng = None, 
                           htmlbalao = None, 
                           rua = None, 
                           numero = None, 
                           complemento = None, 
                           bairro = None, 
                           cep = None, 
                           cidade = None, 
                           estado = None, 
                           id_filial = None, 
                           icone = None, 
                           ):
        """
            Edit the data of a branch.
        """
        endereco = "{0}, n.{1}, {2}, {3}".format(rua, numero, cidade, estado)
        self.execSqlu("update_filial", 
                      endereco=endereco, 
                      site=site, 
                      telefone=telefone, 
                      capacidade=int(capacidade), 
                      regiao=regiao, 
                      forma_pagamento=forma_pagamento, 
                      acesso_cadeirante=acesso_cadeirante, 
                      observacoes=observacoes, 
                      lat=float(lat), 
                      lng=float(lng), 
                      htmlbalao=htmlbalao, 
                      rua=rua, 
                      numero=numero, 
                      complemento=complemento, 
                      bairro=bairro, 
                      cep=cep, 
                      cidade=cidade, 
                      estado=estado, 
                      icone=icone, 
                      id_filial=int(id_filial))
        return "Filial editada com sucesso."
    
    @serialize
    @dbconnectionapp
    @Permission("PERM APP")
    def addRegiao(self, regiao=None):
        """
            Adds a region to the DB
        """
        self.execSqlu("insert_regiao", regiao=regiao)
        return "Regi&atilde;o adicionada com sucesso."
        
    @serialize
    @dbconnectionapp
    @Permission("PERM APP")
    def delRegiao(self, regiao=None):
        """
            Deletes a region from the DB
        """
        self.execSqlu("delete_regiao", regiao=regiao)
        return "Regi&atilde;o deletada com sucesso."
        
    @dbconnectionapp
    def getRegioesJSON(self):
        """
            Returns a JSON encoded list of regions.
        """
        return encode([i for i in self.execSql("select_regioes")])
    
    @dbconnectionapp
    def getNomeTipo(self, id_tipo):
        """
            Returns the name of a type.
        """
        for i in self.execSql("select_nome_tipo", id_tipo=id_tipo):
            return i['tipo']
        
    @serialize
    @dbconnectionapp
    @Permission("PERM APP")
    def delFiliais(self, id_filial=None):
        """
            Deletes a list of branches
        """
        for i in id_filial:
            self.execSqlBatch("delete_filial", id_filial=int(i))
        self.execSqlCommit()
        return "Filiais deletadas com sucesso."
        
        
        
        
    
    
    
    
    
