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
from time import time, strftime, strptime
from urllib import unquote
from publica.admin.error import UserError
from publica.utils.json import encode
from publica.core.portal import Portal
from publica.utils.decorators import serialize, dbconnectionapp,\
                                     Permission
import urllib
import json
import os

class Adm(object):
    """
    """
    def _getDadosApp(self):
        """
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        return portal._getApp(env_site=self.id_site,
                               schema=self.schema)["dados"]

    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def addcategoria(self, nome):
        """
            insert a new categoria

            >>> self.addCategoria(nome=\"name\")
        """
        self.execSqlu("insert_categoria",
                     nome=nome)

        return {"ok":"ok"}


    @dbconnectionapp
    def getCategorias(self):
        
        
        return list(self.execSql("select_categoria"))



    @dbconnectionapp
    def getCatjson(self):



         return encode([i for i in self.execSql("select_categoria")])




    @dbconnectionapp
    def getRegjson(self):



         return encode([i for i in self.execSql("select_regiao")])




    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def editcategoria(self, nome, id_categoria):

        self.execSqlBatch("update_categoria",
                          nome= nome,
                          id_categoria=int(id_categoria))
        self.execSqlCommit()

        return {"ok":"ok"}


    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def editRegiao(self, nome, id_regiao):

        self.execSqlBatch("update_regiao",
                          nome=nome,
                          id_regiao=int(id_regiao))
        self.execSqlCommit()

        return "regiao editada com sucesso!"




    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def delCategoria(self, id_categoria):

        self.execSqlBatch("delete_categoria",
                          id_categoria=int(id_categoria))
        self.execSqlCommit()

        return {"ok":"ok"}



    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def delRegiao(self, id_regiao):

        self.execSqlBatch("delete_regiao",
                          id_regiao=int(id_regiao))
        self.execSqlCommit()

        return "regiao deletado com sucesso!"




    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def addRegiao(self, nome):
        """
            insert a new regiao

            >>> self.addregiao(nome=\"name\")
        """
        self.execSqlu("insert_regiao",
                     nome=nome)

        return "Regiao adicionada com sucesso!"

    @dbconnectionapp
    def getRegiao(self):
        
        
        return list(self.execSql("select_regiao"))


    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def addConteudo(self, id_site, id_treeapp, id_aplicativo,
                          titulo, descricao, regiao,
                          telefone,telefonec, rua, num, bairro, cep, 
                          cidade,imagem, site, estado,
                          publicado_em, categoria=None, editor=False, credito=None, 
                          endereco=None, lat=None, lng=None, 
                          expira_em=None, publicado=None,
                          titulo_destaque=None, descricao_destaque=None,
                          imagem_destaque=None, peso_destaque=None,
                          relacionamento=[], tags="", permissao=None,
                          exportar_xml=None, exportar_json=None,
                          exportar=None, observacao=None, pagamento=None,
                          cadeirantes=None, capacidade=None):
        """
        """
        if site:
            site = site.replace("http://","")
        dadosapp = self._getDadosApp()
        publicado = True if publicado else False
        tags = tags if tags else None
        dt = publicado_em
        try:
            p = strptime(publicado_em, "%d/%m/%Y %H:%M")
            publicado_em = strftime("%Y-%m-%d %H:%M", p)
        except ValueError, e:
            raise UserError(("Ocorreu um erro: "
                             "Data de publica&ccedil;&aring;o "
                             "inv&aacute;lida (%s)") % publicado_em)

        try:
            p = strptime(expira_em, "%d/%m/%Y %H:%M")
            expira_em = strftime("%Y-%m-%d %H:%M", p)
        except ValueError, e:
           expira_em = None

        # inserir conteudo
        portal = Portal(id_site=self.id_site, request=self.request)
        id_conteudo = self.execSql("select_nextval_conteudo").next()["id"]
        id_imagem = portal.addArquivo(arquivo=imagem,
                                      id_conteudo=id_conteudo,
                                      schema=self.schema,
                                      dt=dt)

        if not endereco:       
            endereco = "{0}, n.{1}, {2}, {3}".format(rua, num, cidade, estado)
        if not (lat) or not (lng):
            try:
                lat, lng = self.gerarMapa(endereco)
            except Exception, exp:
                lat, lng = (0,0)
        
        self.execSqlBatch("insert_conteudo",
                          id_conteudo=id_conteudo,
                          titulo=titulo,
                          pagamento=pagamento,
                          descricao=descricao,
                          observacao=observacao,
                          publicado=publicado,
                          expira_em=expira_em,
                          publicado_em=publicado_em,
                          endereco=endereco,
                          imagem=id_imagem,
                          credito=credito,
                          editor=True if bool(editor) else False,
                          regiao=int(regiao) if regiao else None,
                          telefone=telefone,
                          telefonec=telefonec,
                          site=site,
                          estado=estado,
                          rua=rua,
                          num=num,
                          bairro=bairro,
                          cep=cep,
                          capacidade=capacidade,
                          cadeirantes=cadeirantes,
                          lat=float(lat),
                          lng=float(lng),
                          cidade=cidade)

        # inserindo os destaques
        dados_destaque = []
        if titulo_destaque or imagem_destaque or descricao_destaque:
            imagem_destaque = self._addFile(arquivo=imagem_destaque,
                                            id_conteudo=id_conteudo,
                                            schema=self.schema,
                                            dt=dt,
                                            transform={"metodo":dadosapp['redimensionamento'],
                                                       "dimenx":dadosapp['dimenx'],
                                                       "dimeny":dadosapp['dimeny']})
        if categoria: 
            if type(categoria) is not list:
                categoria =[categoria]
            for i in range(len(categoria)):
                self.execSqlBatch("insert_categoria_bar",
                                  id_categoria=int(categoria[i]),
                                  id_conteudo=int(id_conteudo))

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

        if (exportar_xml=='1') or (exportar_json=='1') or (exportar=='1'):

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
            raise UserError("Local n&atilde;o encontrado pelo google maps,"
                            "caso o erro persistir favor inserir a latitude e "
                            "longitude manualmente")
        return lat, lng


    @dbconnectionapp
    @Permission("PERM APP")
    def _getBar(self, id_conteudo):
        """
       Retorna os dados de um Bar
        """
        
        for i in self.execSql("select_conteudo",
                              id_conteudo=int(id_conteudo)):
            i["categorias"]=[]
            for j in self.execSql("select_categoria_bar", id_conteudo=int(i["id_conteudo"])):
                categoria = {"id_categoria":j["id_categoria"],
                             "nome":j["nome"]}
                i["categorias"].append(categoria)
            return i


    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def editConteudo(self, id_conteudo, id_treeapp, id_aplicativo,
                          titulo, descricao, regiao,
                          telefone,telefonec, rua, num, bairro, cep, 
                          cidade,imagem, site, estado,
                          publicado_em, editor=False, credito=None, endereco=None, 
                          expira_em=None, categoria=None, lat=None, lng=None, publicado=None,
                          titulo_destaque=None, descricao_destaque=None,
                          imagem_destaque=None, peso_destaque=None,
                          relacionamento=[], tags="", permissao=None,
                          exportar_xml=None, exportar_json=None,
                          exportar=None, pagamento=None, observacao=None,
                          cadeirantes=None, capacidade=None):
        """
        """
        portal = Portal(id_site=self.id_site, request=self.request)
        publicado = True if publicado else False
        tags = tags if tags else None
        dadosapp = self._getDadosApp()
        dt = publicado_em
        try:
            p = strptime(publicado_em, "%d/%m/%Y %H:%M")
            publicado_em = strftime("%Y-%m-%d %H:%M", p)
        except ValueError, e:
            raise UserError(("Ocorreu um erro: "
                             "Data de publica&ccedil;&aring;o "
                             "inv&aacute;lida (%s)") % publicado_em)

        try:
            p = strptime(expira_em, "%d/%m/%Y %H:%M")
            expira_em = strftime("%Y-%m-%d %H:%M", p)
        except ValueError, e:
           expira_em = None
        id_imagem = portal.addArquivo(arquivo=imagem,
                                      id_conteudo=id_conteudo,
                                      schema=self.schema,
                                      dt=dt)

        # deletar conteudo tabela destaques ou outras tabelas
        self.execSqlBatch("delete_destaque",
                          id_conteudo=int(id_conteudo))
        endereco = "{0}, n.{1}, {2}, {3}".format(rua, num, cidade, estado)
        if not (lat) or not (lng):
            lat, lng = self.gerarMapa(endereco)
        self.execSqlBatch("update_conteudo",
                          id_conteudo=int(id_conteudo),
                          titulo=titulo,
                          pagamento=pagamento,
                          descricao=descricao,
                          observacao=observacao,
                          publicado=publicado,
                          expira_em=expira_em,
                          publicado_em=publicado_em,
                          endereco=endereco,
                          imagem=id_imagem,
                          credito=credito,
                          editor=True if bool(editor) else False,
                          regiao=int(regiao) if regiao else None,
                          telefone=telefone,
                          telefonec=telefonec,
                          site=site,
                          estado=estado,
                          rua=rua,
                          num=num,
                          bairro=bairro,
                          cep=cep,
                          cadeirantes=cadeirantes,
                          capacidade=capacidade,
                          lat=float(lat),
                          lng=float (lng),
                          cidade=cidade)
      
        #deletando as categorias
        if categoria:
            self.execSqlBatch("delete_categoria_bar",
                               id_conteudo=int(id_conteudo))
            if type(categoria) is not list:
                categoria =[categoria]
            for i in range(len(categoria)):
                self.execSqlBatch("insert_categoria_bar",
                                  id_categoria=int(categoria[i]),
                                  id_conteudo=int(id_conteudo))
        # inserindo os destaques
        dados_destaque = []
        if titulo_destaque or imagem_destaque or descricao_destaque:
            imagem_destaque = self._addFile(arquivo=imagem_destaque,
                                             id_conteudo=id_conteudo,
                                             schema=self.schema,
                                             dt=dt,
                                             transform={"metodo":dadosapp['redimensionamento'],
                                                       "dimenx":dadosapp['dimenx'],
                                                       "dimeny":dadosapp['dimeny']})
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

        if (exportar_xml=='1') or (exportar_json=='1') or (exportar=='1'):

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



