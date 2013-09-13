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

class Adm(object):
    """
    """

    def _getAppAuth(self):
        """
            Pega o app de cinemas para acesso aos métodos
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        dados = portal._getApp(env_site=self.id_site,
                               schema=self.schema)["dados"]

        if dados.get("auth_schema", None):

            return portal._getAplication(id_site=self.id_site,
                                         meta_type=dados["auth_type"],
                                         schema=dados["auth_schema"])

    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def addConteudo(self, id_site, id_treeapp, id_aplicativo,
                          titulo, titulo_original, pais, ano, 
                          genero, direcao, duracao, censura, elenco, 
                          sinopse, descricao, trailer, 
                          publicado_em, expira_em=None, publicado=None,
                          titulo_destaque=None, descricao_destaque=None,
                          imagem_destaque=None, peso_destaque=None,
                          relacionamento=[], tags="", permissao=None,
                          exportar_xml=None, exportar_json=None,
                          exportar=None):
        """
        """
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
        num_genero = len(genero)
        genero = list(genero)
        gener =''
        for i in range(num_genero):
            gener+=genero[i]
            if i != (num_genero-1):
                gener+=', '
        id_conteudo = self.execSql("select_nextval_conteudo").next()["id"]
        if type(pais) is not list:
            pais = [pais]
        for i in range(len(pais)):
            self.execSqlBatch("insert_pais_filme",
                               id_conteudo=int(id_conteudo),
                               id_pais=int(pais[i]))       
        self.execSqlu("insert_conteudo",
                          id_conteudo=id_conteudo,
                          titulo=titulo,
                          titulo_original=titulo_original,
                          pais=pais,
                          ano=ano,
                          genero=gener,
                          direcao=direcao,
                          duracao=duracao,
                          censura=censura,
                          elenco=elenco,
                          sinopse=sinopse,
                          trailer=trailer,
                          descricao=descricao,
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
            try:
                self._addLog("Novo conteudo cadastrado e publicado '%s'" % titulo)
            except:
                "what the fuck"
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

    @serialize
    @dbconnectionapp
    def getJson_generos(self):
        return list(self.execSql("select_genero"))

    @serialize
    @dbconnectionapp
    def getJson_paiss(self):
        return list(self.execSql("select_pais"))

    @dbconnectionapp
    @Permission("PERM APP")
    def _getConteudo(self, id_conteudo):
        """
        """
        for i in self.execSql("select_conteudo",
                              id_conteudo=int(id_conteudo)):
            i["paises"]=[]
            for j in self.execSql("select_pais_filme",
                                   id_conteudo=int(i['id_conteudo'])):
                pais={"id_pais":j["id_pais"],
                      "pais":j["nome"]}
                i['paises'].append(pais)   
        return i
    
    def getSessoes(self, id_filme, publica=False):
        """
        Pega a sessão de um filme
        """
        sessao = self._getAppAuth()
        if sessao:        
            id_conteudo = sessao.getSessaoByIdFilm(id_filme)
            if id_conteudo:
                if publica:
                    self.getPublicaCinema(id_conteudo[0]['id_conteudo'])
                else:
                    return id_conteudo[0]['id_conteudo']                
            else:
                return False 
        else:
            return False

    def getPublicaCinema(self, id_cinema):
        """
        publicação do cinema cujo há um filme vinculado após o filme
        for excluido, se for feita edição no filme.
        """
        portal = Portal(id_site=self.id_site, request=self.request)
        dados = portal._getApp(env_site=self.id_site,
                                   schema=self.schema)["dados"]
        portal._exportarFormatosConteudo(id_aplicativo=None,
                                         id_conteudo=int(id_cinema),
                                         schema=dados["auth_schema"],
                                         id_treeapp=None,
                                         html=1,
                                         xml=None,
                                         json=None,
                                         dados=dados,
                                         subitems=None,
                                         add=1)              
    @dbconnectionapp
    def get_generos(self):
        """
        """
        generos = [i for i in self.execSql("select_genero")]
        return generos

    @dbconnectionapp
    def get_genero_id(self, genero):
        """
        """
        genero = [i for i in self.execSql("select_genero_id",
                                           nome=genero,
                                           )][0]['id_genero']       
        return genero

    @dbconnectionapp
    @serialize
    def del_genero(self, id_):
        """
        """
        exists_genero = self.execSql("exists_genero",id_genero=int(id_))
        if len(list(exists_genero))>0:
            return {'error':'Não foi possível excluir o regitro, o genero esta vinculado a um filme'}
        self.execSqlBatch("delete_genero",id_genero=int(id_))
        self.execSqlCommit()
        return {'ok':'ok'}


    @dbconnectionapp
    @serialize
    def edit_genero(self, id_, nome):
        """
        """
        self.execSqlBatch("update_genero",id_genero=int(id_),
                                          nome=nome)
        self.execSqlCommit()
        return "ok"



    @serialize
    @dbconnectionapp
    def add_genero(self, nome):
        """
        """
        id_genero = self.execSql("select_nextval_genero").next()["id"]

        self.execSqlBatch("insert_genero",
                          nome=nome,
                          id_genero=id_genero)
        
        self.execSqlCommit()
        retorno = {'ok':True,'id_genero':id_genero}
        return retorno


    @dbconnectionapp
    def get_pais_id(self, pais):
        """
        """
        pais = [i for i in self.execSql("select_pais_id",
                                        nome=pais,
                                        )][0]['id_pais']  
        return pais

    @dbconnectionapp
    def get_paises(self):
        """
        """
        pais = [i for i in self.execSql("select_pais")]
        return pais

    @dbconnectionapp
    @serialize
    def del_pais(self, id_):
        """
        """
        self.execSqlBatch("delete_pais",id_pais=int(id_))
        self.execSqlCommit()
        return {'ok':'ok'}


    @dbconnectionapp
    @serialize
    def edit_pais(self, id_, nome):
        """
        """
        self.execSqlBatch("update_pais",id_pais=int(id_),
                                        nome=nome)
        self.execSqlCommit()
        return "ok"



    @serialize
    @dbconnectionapp
    def add_pais(self, nome):
        """
        """
        id_pais = self.execSql("select_nextval_pais").next()["id"]

        self.execSqlBatch("insert_pais",
                          nome=nome,
                          id_pais=id_pais)
        
        self.execSqlCommit()
        retorno = {'ok':True,'id_pais':id_pais}
        return retorno



    @dbconnectionapp
    def _getFilmes(self, limit=None):
        """
        """
        if limit:
            return self.execSql("select_filmes_limit",
                                 limit=limit)
        else:
            return self.execSql("select_filmes")



    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def editConteudo(self, id_conteudo, id_site, id_treeapp, id_aplicativo,
                          titulo, titulo_original, pais, ano, 
                          genero, direcao, duracao, censura, elenco, 
                          sinopse, descricao, trailer, 
                          publicado_em, expira_em=None, publicado=None,
                          titulo_destaque=None, descricao_destaque=None,
                          imagem_destaque=None, peso_destaque=None,
                          relacionamento=[], tags="", permissao=None,
                          exportar_xml=None, exportar_json=None,
                          exportar=None):
        """
        """
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
        num_genero = len(genero)
        genero = list(genero)
        gener =''
        for i in range(num_genero):
            gener+=genero[i]
            if i != (num_genero-1):
                gener+=', '
        # deletar conteudo tabela destaques ou outras tabelas
        self.execSqlBatch("delete_destaque",
                          id_conteudo=int(id_conteudo))
        self.execSqlBatch("delete_pais_filme",
                          id_conteudo=int(id_conteudo))
        if type(pais) is not list:
            pais = [pais]
        for i in range(len(pais)):
            self.execSqlBatch("insert_pais_filme",
                               id_conteudo=int(id_conteudo),
                               id_pais=int(pais[i])) 
        self.execSqlu("update_conteudo",
                          id_conteudo=int(id_conteudo),
                          titulo=titulo,
                          titulo_original=titulo_original,
                          pais=pais,
                          ano=ano,
                          genero=gener,
                          direcao=direcao,
                          duracao=duracao,
                          censura=censura,
                          elenco=elenco,
                          sinopse=sinopse,
                          trailer=trailer,
                          descricao=descricao,
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

        if exportar_xml or exportar_json or exportar:
            self.getSessoes(id_conteudo, publica=True)
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



