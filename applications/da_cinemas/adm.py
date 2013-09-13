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
from datetime import datetime
from urllib import unquote, quote
from publica.core.portal import Portal
from publica.admin.error import UserError
from publica.utils.json import encode
from publica.utils.decorators import serialize, dbconnectionapp,\
                                     Permission

import urllib
import json
import os

class Adm(object):
    """
    """

    def _getAppAuth(self):
        """
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
    def _getTipo(self):
        return self.execSql("select_tipo_sala")

    @dbconnectionapp
    def _getFilmes(self, limit):
        app_filmes = self._getAppAuth()
        return app_filmes._getFilmes(limit)

    @dbconnectionapp
    def _getSessoes(self):
        return self.execSql("select_filmes")

    @dbconnectionapp
    def _getSalasByCinema(self, id_conteudo):
        return [i for i in self.execSql("select_salas",id_conteudo=int(id_conteudo))]

    @serialize
    @dbconnectionapp
    def getSalasCinema(self, id_conteudo):
        return [i for i in self.execSql("select_salas",id_conteudo=int(id_conteudo))]


    @dbconnectionapp
    def _getSessoesByCinema(self, id_conteudo):
        """
        """

        portal = Portal(id_site=self.id_site,
                        request=self.request)
        dados = portal._getApp(env_site=self.id_site,
                               schema=self.schema)["dados"]


        data_atual = datetime.now()
        data_atual = str(data_atual.date())

        for i in self.execSql("select_sessoes_cinema", id_conteudo=int(id_conteudo),
                                                       SCHEMA = buffer(dados["auth_schema"])):
            i['nome_sessao'] =i['cinema_nome'] + " (" + i['sala_nome'] + ") - " +i['filme_nome'] 
            i['horario'] = list(i['horario'])
            if((i['data_inicio']<= data_atual) and (data_atual <= i['data_fim']) and (data_atual>= i['data_inicio'])):
                i['status'] = 'Ativo'
            else:
                i['status'] = 'Inativo'
            yield i

    @dbconnectionapp
    def _getSessoesByIdSessao(self, id_sessao):
        """
        """
        for i in self.execSql("select_sessoes_id_sessao", id_sessao=int(id_sessao)): 
            i['horario'] =  eval(i['horarios']);
            i['dia_inicio'] = str(i['data_inicio'])[8:10]
            i['mes_inicio'] = str(i['data_inicio'])[5:7]
            i['ano_inicio'] = str(i['data_inicio'])[0:4]
            i['dia_fim'] = str(i['data_fim'])[8:10]
            i['mes_fim'] = str(i['data_fim'])[5:7]
            i['ano_fim'] = str(i['data_fim'])[0:4]
            yield i

    def getDateNow(self):
        """
        """
        data = datetime.now()
        i = {}
        i['dia'] = data.day
        i['mes'] = data.month
        i['ano'] = data.year
        return i
        
    @dbconnectionapp
    def getSessaoByCinemaAndFilm(self):
        """
        retorna todos ids dos cinemas e 
        filmes para que a cron publique
        """
        cinema = self.execSql("select_sessao_by_cinema")
        filme = self.execSql("select_sessao_by_film")
        return {"cinema":cinema,
                "filme":filme}

    @dbconnectionapp
    def _getFilme(self, id_filme):
        """
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        dadosapp = portal._getApp(env_site=self.id_site,
                                  schema=self.schema)["dados"] 
        filme = self.execSql("select_filme",
                               SCHEMA = buffer(dadosapp['auth_schema']),
                               id_filme=int(id_filme)).next()
        fotos = [i for i in self.execSql("select_fotos_filme",
                                         id_filme=int(id_filme))]
        return {"filme": filme,
                "fotos": fotos}


        return list(self.execSql("select_filme", SCHEMA = buffer(dadosapp['auth_schema']), id_filme=int(id_filme)))

    @dbconnectionapp
    def getSessao(self):
        """
        """
        sessao = [i for i in self.execSql("select_sessao")]
        return sessao

    @dbconnectionapp
    def getSessaoByIdFilm(self, id_filme):
        """
            retorna a sessão de um filme
        """
        return list(self.execSql("select_sessao_byfilm", id_filme=int(id_filme)))

    @dbconnectionapp
    def getGeneros(self):
        """
        """
        generos = [i for i in self.execSql("select_genero")]
        return generos

    @dbconnectionapp
    def _getCinemas(self):
        """
        """
        cinemas = [i for i in self.execSql("select_cinemas")]
        return cinemas

    @serialize
    @dbconnectionapp
    def getJsonGeneros(self):
        return list(self.execSql("select_genero"))

    @serialize
    @dbconnectionapp
    def getJsonFilmes(self):
        app_filmes = self._getAppAuth()
        filmes = app_filmes._getFilmes()
        return list(filmes)

    @serialize
    @dbconnectionapp
    def getJsonCidades(self):
        return list(self.execSql("select_cidades"))

    @serialize
    @dbconnectionapp
    def addGenero(self, nome):
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
    @serialize
    @Permission("PERM APP")
    def editFilme(self, id_filme, titulo, titulo_original, pais, ano, genero, direcao,
                 duracao, censura, elenco, sinopse, status,
                 descricao, trailer, foto=[]):
        """
        """
        portal = Portal(id_site=self.id_site, request=self.request)
        data = datetime.now()
        data_atual = str(data.day) + "/" + str(data.month) + "/" + str(data.year) + " 00:00"

        self.execSqlBatch("delete_fotos",
                          id_filme=int(id_filme))

        dados = portal._getApp(env_site=self.id_site,
                               schema=self.schema)["dados"]

        if(dados["id_treeapp_filmes"] == ""):
            return " não é possível cadastrar filmes, é preciso configurar o aplicativo de cinemas com o id_treeapp da pasta filmes e o id do aplicativo"
        if(dados["id_aplicativo"] == ""):
            return " não é possível cadastrar filmes, é preciso configurar o aplicativo de cinemas com o id_treeapp da pasta filmes e o id do aplicativo"

        self.execSqlBatch("update_filme",
                          id_filme=id_filme,
                          titulo=titulo,
                          titulo_original=titulo_original,
                          pais=pais,
                          ano=ano,
                          genero=genero,
                          direcao=direcao,
                          duracao=duracao,
                          censura=censura,
                          elenco=elenco,
                          sinopse=sinopse,
                          status=status,
                          descricao=descricao,
                          trailer=trailer)
        # fotos
        dados_fotos = []
        for i in foto:
            if not i["img"]:
                imagem = None
            else:
                id_foto = self.execSql("select_nextval_foto_filme").next()["id"]
                arquivo = i["img"]
                imagem = self._addFile(arquivo=arquivo,
                                      id_conteudo=id_filme,
                                      schema=self.schema,
                                      dt=data_atual,
                                      transform={"metodo":dados["redimensionamento"],
                                           "marca":None,
                                           "alinhamento":None,
                                           "dimenx":int(dados["dimenx"]),  
                                           "dimeny":int(dados["dimeny"])})
                self.execSqlBatch("insert_fotos_filme",
                                  id_foto=id_foto,
                                  id_filme=id_filme,
                                  arquivo=imagem)

            if not imagem:
                continue
        
        self.execSqlCommit()
        dados2 = self._setDados(id_conteudo=id_filme)
        return "editado com sucesso"

    @dbconnectionapp
    @serialize
    @Permission("PERM APP")    
    def editSessao(self, minutos, id_conteudo, horas, 
                         tipo, id_filme, id_sala, data_inicio,
                         data_fim, id_sessao, status, exportar=None):
        """
        """
        portal = Portal(id_site=self.id_site, request=self.request)
        dados = portal._getApp(env_site=self.id_site,
                               schema=self.schema)["dados"]
        dados_filme = portal._getApp(env_site=self.id_site,
                                     schema=dados['auth_schema'])["dados"]
        horarios = []
        horas = horas.split(',')
        minutos = minutos.split(',')
        tipo = tipo.split(',')
        horas.remove('')
        minutos.remove('')
        tipo.remove('')
        for i in range(len(horas)):
            horario_init = {}
            horario_init["hora"] = horas[i]
            horario_init["minuto"] = minutos[i]
            horario_init["tipo"] = tipo[i]
            horarios.append(horario_init)

        self.execSqlBatch("update_sessao",
                          id_sessao=int(id_sessao),
                          data_inicio=data_inicio,
                          data_fim=data_fim,
                          id_tipo = 1,
                          id_conteudo = int(id_conteudo),
                          horarios=str(horarios),
                          status=status,
                          id_filme=int(id_filme),
                          id_sala=int(id_sala))
        self.execSqlCommit()
        if exportar:           
            portal._exportarFormatosConteudo(id_aplicativo=None,
                                             id_conteudo=id_conteudo,
                                             schema=self.schema,
                                             id_treeapp=None,
                                             html=1,
                                             xml=None,
                                             json=None,
                                             dados=dados,
                                             subitems=None,
                                             add=1)
            portal._exportarFormatosConteudo(id_aplicativo=None,
                                             id_conteudo=id_filme,
                                             schema=dados['auth_schema'],
                                             id_treeapp=None,
                                             html=1,
                                             xml=None,
                                             json=None,
                                             dados=dados_filme,
                                             subitems=None,
                                             add=1)
            return "Sessão editada e publicada juntamente com o cinema e o filme"
        return "Sessão editada com sucesso!"


    @dbconnectionapp
    @serialize    
    def addSessao(self, id_filme, data_inicio, data_fim, 
                        status, cines=[], exportar=None):
        """
        """
        cines = json.loads(cines)
        portal = Portal(id_site=self.id_site, request=self.request)
        dados = portal._getApp(env_site=self.id_site,
                               schema=self.schema)["dados"]
        dados_filme = portal._getApp(env_site=self.id_site,
                                    schema=dados['auth_schema'])["dados"]
        exportar_flag = False
        for i in cines:   
            id_sessao = self.execSql("select_nextval_sessao").next()["id"]
            self.execSqlBatch("insert_sessao",
                              id_sessao=id_sessao,
                              data_inicio=data_inicio,
                              data_fim=data_fim,
                              id_tipo = "1",
                              id_conteudo = int(i['cinema']),
                              horarios=str(i['session']),
                              status=status,
                              id_filme=id_filme,
                              id_sala=int(i['sala']))
        self.execSqlCommit()
        if exportar:            
            for i in cines:
                exportar_flag = True        
                portal._exportarFormatosConteudo(id_aplicativo=None,
                                                 id_conteudo=i['cinema'],
                                                 schema=self.schema,
                                                 id_treeapp=None,
                                                 html=1,
                                                 xml=None,
                                                 json=None,
                                                 dados=dados,
                                                 subitems=None,
                                                 add=1)
                portal._exportarFormatosConteudo(id_aplicativo=None,
                                                 id_conteudo=id_filme,
                                                 schema=dados['auth_schema'],
                                                 id_treeapp=None,
                                                 html=1,
                                                 xml=None,
                                                 json=None,
                                                 dados=dados_filme,
                                                 subitems=None,
                                                 add=1)

        
        if exportar_flag:  
            return "Sessão editada e publicada juntamente com o cinema correspondente e o filme"
        return "Sessão cadastrada com sucesso para o cinema correspondente!"

    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def addFilme(self, titulo, titulo_original, pais, ano, genero, direcao,
                 duracao, censura, elenco, sinopse, status,
                 descricao, trailer, foto=[]):
        """
        """
        portal = Portal(id_site=self.id_site, request=self.request)
        data = datetime.now()
        data_atual = str(data.day) + "/" + str(data.month) + "/" + str(data.year) + " 00:00"

        dados = portal._getApp(env_site=self.id_site,
                               schema=self.schema)["dados"]


        id_filme = self.execSql("select_nextval_filme").next()["id"]
        id_filme = 2000000000 - int(id_filme)
        self.execSqlBatch("insert_filme",
                          id_filme=id_filme,
                          titulo=titulo,
                          titulo_original=titulo_original,
                          pais=pais,
                          ano=ano,
                          genero=genero,
                          data=str(data.date()),
                          direcao=direcao,
                          duracao=duracao,
                          censura=censura,
                          elenco=elenco,
                          sinopse=sinopse,
                          status=status,
                          descricao=descricao,
                          trailer=trailer)
        # fotos
        dados_fotos = []
        for i in foto:
            if not i["img"]:
                imagem = None
            else:
                id_foto = self.execSql("select_nextval_foto_filme").next()["id"]
                arquivo = i["img"]
                imagem = self._addFile(arquivo=arquivo,
                                      id_conteudo=id_filme,
                                      schema=self.schema,
                                      dt=data_atual,
                                      transform={"metodo":dados["redimensionamento"],
                                           "marca":None,
                                           "alinhamento":None,
                                           "dimenx":int(dados["dimenx"]),  
                                           "dimeny":int(dados["dimeny"])})
                self.execSqlBatch("insert_fotos_filme",
                                  id_foto=id_foto,
                                  id_filme=id_filme,
                                  arquivo=imagem)
            self.execSqlCommit()

            if not imagem:
                continue

        if(dados["id_treeapp_filmes"] == ""):
            return " não é possível cadastrar filmes, é preciso configurar o aplicativo de cinemas com o id_treeapp da pasta filmes e o id do aplicativo"
        if(dados["id_aplicativo"] == ""):
            return " não é possível cadastrar filmes, é preciso configurar o aplicativo de cinemas com o id_treeapp da pasta filmes e o id do aplicativo"

        dados2 = self._setDados(id_conteudo=id_filme)
        self._addContentPortal(env_site=self.id_site,
                               id_pk=id_filme,
                               id_aplicativo=int(dados["id_aplicativo"]),
                               schema="app_default_135091332362",
                               meta_type=self.meta_type,
                               id_treeapp=int(dados["id_treeapp_filmes"]),
                               titulo=titulo,
                               publicado=True,
                               publicado_em="2012-09-20 09:52:00",
                               expira_em=None,
                               permissao=None,
                               titulo_destaque=None,
                               descricao_destaque=None,
                               imagem_destaque=None,
                               tags=None,
                               relacionamento=[],
                               dados=dados2)
        exportar=True,
        exportar_xml=None
        exportar_json=None

        self._exportContent(id_aplicativo=int(dados["id_aplicativo"]),
                            id_conteudo=id_filme,
                            schema=self.schema,
                            id_treeapp=int(dados["id_treeapp_filmes"]),
                            html=exportar,
                            xml=exportar_xml,
                            json=exportar_json,
                            dados=dados2,
                            subitems=None,
                            add=1)        
        return "cadastrado com sucesso"
    

    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def addCinema(self, id_site, id_treeapp, id_aplicativo, nome_cinema,
                        precos_cinema, site_cinema, estado_cinema,
                        id_cidade, publicado_em,telefone,
                        rua, num, bairro, cep,
                        foto=[], sala=[], expira_em=None,
                        publicado=None,lat=None,telefonec=None, lng=None,
                        exportar=None, exportar_xml=None,
                        exportar_json=None, relacionamento=[], permissao=None):
        id_conteudo = self.execSql("select_nextval_cinema").next()["id"]
        portal = Portal(id_site=self.id_site, request=self.request)
        publicado = True if publicado else False

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

        cidade_nome = self.execSql("select_nome_cidade",id_cidade=int(id_cidade)).next()["nome"]

        endereco = "{0}, n.{1}, {2}, {3}".format(rua, num, cidade_nome, estado_cinema)
        if not (lat) or not (lng):
            lat, lng = self.gerarMapa(endereco)

        self.execSqlBatch("insert_cinema",
                          id_conteudo=id_conteudo,
                          nome=nome_cinema,
                          rua=rua,
                          num=num,
                          lat=lat,
                          lng=lng,
                          endereco=endereco,
                          cep=cep,
                          bairro=bairro,
                          precos=precos_cinema,
                          id_cidade=id_cidade,
                          site=site_cinema,
                          estado=estado_cinema,
                          telefone=telefone,
                          telefonec=telefonec,
                          publicado=publicado,
                          expira_em=expira_em,
                          publicado_em=publicado_em)

        dados = portal._getApp(env_site=self.id_site,
                               schema=self.schema)["dados"]


        # fotos
        dados_fotos = []
        for i in foto:
            if not i["img"]:
                imagem = None
            else:
                id_foto = self.execSql("select_nextval_foto_conteudo").next()["id"]
                arquivo = i["img"]
                imagem = self._addFile(arquivo=arquivo,
                                      id_conteudo=id_conteudo,
                                      schema=self.schema,
                                      dt=dt,
                                      transform={"metodo":dados["redimensionamento"],
                                                 "marca":None,
                                                 "alinhamento":0,
                                                 "dimenx":int(dados["dimenx"]),  
                                                 "dimeny":int(dados["dimeny"])})

                self.execSqlBatch("insert_fotos_conteudo",
                                  id_foto=id_foto,
                                  id_conteudo=id_conteudo,
                                  credito=i['credito'],
                                  arquivo=imagem)

            if not imagem:
                continue

            dados_fotos.append({"arquivo": imagem})
        #salas
        dados_salas = []
        for i in sala:

            id_sala = self.execSql("select_nextval_sala").next()["id"]
            idSa = i["idSa"]
            nomeSala = i["nomeSala"]
            is3D = i["is3D"]

            self.execSqlBatch("insert_sala",
                              id_sala=id_sala,
                              id_conteudo=id_conteudo,
                              nome=nomeSala,
                              is3D=is3D)

            dados_salas.append({"nome": nomeSala,
                                "id_sala": id_sala})


            self.execSqlCommit()

        dados = self._setDados(id_conteudo=id_conteudo)
        self._addContentPortal(env_site=self.id_site,
                               id_pk=id_conteudo,
                               id_aplicativo=int(id_aplicativo),
                               schema=self.schema,
                               meta_type=self.meta_type,
                               id_treeapp=id_treeapp,
                               titulo=nome_cinema,
                               publicado=publicado,
                               publicado_em=publicado_em,
                               expira_em=expira_em,
                               permissao=permissao,
                               titulo_destaque=None,
                               descricao_destaque=None,
                               imagem_destaque=None,
                               tags=None,
                               relacionamento=relacionamento,
                               dados=dados)

        if exportar_xml or exportar_json or exportar:

            self._addLog("Novo cinema cadastrado e publicado '%s'" % nome_cinema)
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

            return ("Cinema adicionado com sucesso! "
                    "Publica&ccedil;&atilde;o iniciada.")

        self._addLog("Cinema adicionado '%s'" % nome_cinema)
        return "Cinema adicionado com sucesso."

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
    @serialize
    @Permission("PERM APP")
    def editCinema(self, id_site, id_treeapp, id_aplicativo, id_conteudo, nome_cinema,
                        precos_cinema, site_cinema, estado_cinema,
                        id_cidade, publicado_em,telefone,
                        rua, num, bairro, cep,
                        foto=[], sala=[], expira_em=None,
                        publicado=None,lat=None,telefonec=None, lng=None,
                        exportar=None, exportar_xml=None,
                        exportar_json=None, relacionamento=[], permissao=None):

        publicado = True if publicado else False
        portal = Portal(id_site=self.id_site, request=self.request)
        dt = publicado_em
        try:
            publicado_em_t = strptime(publicado_em, "%d/%m/%Y %H:%M")
            publicado_em = strftime("%Y-%m-%d %H:%M", publicado_em_t)
        except ValueError, e:
            raise UserError(("Ocorreu um erro: "
                             "Data de publica&ccedil;&aring;o "
                             "inv&aacute;lida (%s)") % publicado_em)
        try:
            p = strptime(expira_em, "%d/%m/%Y %H:%M")
            expira_em = strftime("%Y-%m-%d %H:%M", p)
        except ValueError, e:
            expira_em = None


        self.execSqlBatch("delete_dados_cinema",
                          id_conteudo=int(id_conteudo))

        endereco = "{0}, n.{1}, {2}, {3}".format(rua, num, id_cidade, estado_cinema)
        if not (lat) or not (lng):
            lat, lng = self.gerarMapa(endereco)

        dados = portal._getApp(env_site=self.id_site,
                               schema=self.schema)["dados"]

        #atualizar cinema
        self.execSqlBatch("update_cinema",
                          id_conteudo=id_conteudo,
                          nome=nome_cinema,
                          rua=rua,
                          num=num,
                          lat=lat,
                          lng=lng,
                          endereco=endereco,
                          cep=cep,
                          bairro=bairro,
                          precos=precos_cinema,
                          id_cidade=id_cidade,
                          site=site_cinema,
                          estado=estado_cinema,
                          telefone=telefone,
                          telefonec=telefonec,
                          publicado=publicado,
                          expira_em=expira_em,
                          publicado_em=publicado_em)

        # fotos
        dados_fotos = []
        for i in foto:
            if not i["img"]:
                imagem = None
            else:
                id_foto = self.execSql("select_nextval_foto_conteudo").next()["id"]
                arquivo = i["img"]
                imagem = self._addFile(arquivo=arquivo,
                                      id_conteudo=id_conteudo,
                                      schema=self.schema,
                                      dt=dt,                       
                                      transform={"metodo":dados["redimensionamento"],
                                                 "dimenx":int(dados["dimenx"]),  
                                                 "dimeny":int(dados["dimeny"])})
                self.execSqlBatch("insert_fotos_conteudo",
                                  id_foto=id_foto,
                                  id_conteudo=id_conteudo,
                                  arquivo=imagem,
                                  credito=i['credito'])

            if not imagem:
                continue

            dados_fotos.append({"arquivo": imagem})
        #salas
        dados_salas = []
        lista_id_sala = []
        for i in self.execSql("select_ids_sala",id_conteudo=int(id_conteudo)):
            lista_id_sala.append(i["id_sala"])    
        for i in sala:

            idSa = i["idSa"]
            nomeSala = i["nomeSala"]
            is3D = i["is3D"]
            if idSa:
                exists_sala = list(self.execSql("exists_id_sala",id_sala=int(idSa)))
            else:
                exists_sala = []

            if(len(exists_sala)>0):
                lista_id_sala.remove(int(idSa))
                self.execSqlBatch("update_sala",
                                   id_sala=int(idSa),
                                   nome=nomeSala,
                                   is3D=is3D)
            else:
                id_sala = self.execSql("select_nextval_sala").next()["id"]
                self.execSqlBatch("insert_sala",
                                  id_sala=id_sala,
                                  id_conteudo=id_conteudo,
                                  nome=nomeSala,
                                  is3D=is3D)
        for i in lista_id_sala:
            self.execSqlBatch("delete_sala",
                                   id_sala=int(i))
        self.execSqlCommit()

        dados = self._setDados(id_conteudo=id_conteudo)
        self._editContentPortal(env_site=self.id_site,
                               id_pk=id_conteudo,
                               id_aplicativo=int(id_aplicativo),
                               schema=self.schema,
                               meta_type=self.meta_type,
                               id_treeapp=id_treeapp,
                               titulo=nome_cinema,
                               publicado=publicado,
                               publicado_em=publicado_em,
                               expira_em=expira_em,
                               permissao=permissao,
                               titulo_destaque=None,
                               descricao_destaque=None,
                               imagem_destaque=None,
                               tags=None,
                               relacionamento=relacionamento,
                               dados=dados)

        if exportar_xml or exportar_json or exportar:

            self._addLog("Cinema editado e publicado '%s'" % nome_cinema)
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

            return ("Cinema editado com sucesso! "
                    "Publica&ccedil;&atilde;o iniciada.")

        self._addLog("Cinema editado '%s'" % nome_cinema)
        return "Cinema editado com sucesso."

    @dbconnectionapp
    @serialize
    def addCidade(self, nome):
        """
        """
        id_cidade = self.execSql("select_nextval_cidade").next()["id"]
        self.execSqlBatch("insert_cidade",
                           id_cidade=int(id_cidade),
                           nome=nome)
        self.execSqlCommit()
        retorno={'ok':True,'id_cidade':id_cidade}
        return retorno

    @dbconnectionapp
    @serialize
    def delCidade(self, id_cidade):
        """
        """
        exists_cidade = self.execSql("exists_cidade",id_cidade=int(id_cidade))
        if len(list(exists_cidade))>0:
            return {'error':'Não foi possível excluir o regitro, a cidade esta vinculada a um cinema'}
        self.execSqlBatch("delete_cidade",id_cidade=int(id_cidade))
        self.execSqlCommit()
        retorno = {'ok':'ok'}
        return retorno

    @dbconnectionapp
    @serialize
    def delGenero(self, id_genero):
        """
        """
        exists_genero = self.execSql("exists_genero",id_genero=int(id_genero))
        if len(list(exists_genero))>0:
            return {'error':'Não foi possível excluir o regitro, o genero esta vinculado a um filme'}
        self.execSqlBatch("delete_genero",id_genero=int(id_genero))
        self.execSqlCommit()
        return {'ok':'ok'}

    @dbconnectionapp
    @serialize
    def delFilme(self, id_filme):
        """
        """
        portal = Portal(id_site=self.id_site, request=self.request)

        self.execSqlBatch("delete_fotos", id_filme=int(id_filme))
        self.execSqlBatch("delete_filme",id_filme=int(id_filme))
        dados = portal._getApp(env_site=self.id_site,
                               schema=self.schema)["dados"]
        dict_itens = {"id_treeapp":dados["id_treeapp_filmes"], 
                      "id_aplicativo":dados["id_aplicativo"],
                      "id_conteudo":id_filme,
                      "schema":self.schema}
        list_dict = [dict_itens]
        portal.deleteConteudo(env_site=self.id_site, id_treeapp=dados["id_treeapp_filmes"], items=list_dict)
        self.execSqlCommit()



    @dbconnectionapp
    @serialize
    def delSessao(self, id_sessao):
        """
        """
        portal = Portal(id_site=self.id_site, request=self.request)
        dados = portal._getApp(env_site=self.id_site,
                               schema=self.schema)["dados"]
        dados_filme = portal._getApp(env_site=self.id_site,
                                     schema=dados['auth_schema'])["dados"]
        id_filme = [i["id_filme"] for i in self.execSql("select_sessao_byid",
                                            id_sessao=int(id_sessao))][0]
        id_conteudo = [i["id_conteudo"] for i in self.execSql("select_sessao_byid",
                                               id_sessao=int(id_sessao))][0]
        self.execSqlBatch("delete_sessao",
                           id_sessao=int(id_sessao))
        self.execSqlCommit()
        portal._exportarFormatosConteudo(id_aplicativo=None,
                                         id_conteudo=id_conteudo,
                                         schema=self.schema,
                                         id_treeapp=None,
                                         html=1,
                                         xml=None,
                                         json=None,
                                         dados=dados,
                                         subitems=None,
                                         add=1)
        portal._exportarFormatosConteudo(id_aplicativo=None,
                                         id_conteudo=id_filme,
                                         schema=dados['auth_schema'],
                                         id_treeapp=None,
                                         html=1,
                                         xml=None,
                                         json=None,
                                         dados=dados_filme,
                                         subitems=None,
                                         add=1)

        return "item deletado com sucesso o cinema e o filme ligado a essa sessão foram publicados"


    @dbconnectionapp
    @serialize
    def editCidade(self, id_cidade, nome):
        """
        """
        self.execSqlBatch("update_cidade",id_cidade=int(id_cidade),
                                          nome=nome)
        self.execSqlCommit()
        retorno = True
        return retorno

    @dbconnectionapp
    @serialize
    def editGenero(self, id_genero, nome):
        """
        """
        self.execSqlBatch("update_genero",id_genero=int(id_genero),
                                          nome=nome)
        self.execSqlCommit()
        return "ok"


    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def updateTop(self, titulo, texto, top1, top2, top3, top4, top5, top6, top7, top8, top9, top10):
        """
        """

        self.execSqlBatch("delete_top10")
        self.execSqlBatch("insert_top",
                      titulo=titulo,
                      texto=texto,
                      top1=top1,
                      top2=top2,
                      top3=top3,
                      top4=top4,
                      top5=top5,
                      top6=top6,
                      top7=top7,
                      top8=top8,
                      top9=top9,
                      top10=top10)
        self.execSqlCommit()
          
        return "Top 10 editado com sucesso."

    @dbconnectionapp
    def getCinema(self, id_conteudo):
        """
        """
        dic = {}
        cinema = self.execSql("select_cinema",
                               id_conteudo=int(id_conteudo)).next()
        fotos = [i for i in self.execSql("select_fotos_conteudo",
                                         id_conteudo=int(id_conteudo))]
        salas = [i for i in self.execSql("select_salas",id_conteudo=int(id_conteudo))]

        return {"cinema": cinema,
                "fotos": fotos,
                "salas": salas}

    @dbconnectionapp
    def _getSessoesByFilme(self, id_filme):
        """
        """
        return [i for i in self.execSql("select_sessoes_by_filme", id_filme=int(id_filme))]

    @dbconnectionapp
    def _getCinemasByFilme(self, id_filme):
        """
        """
        return [i for i in self.execSql("select_cinemas_filme", id_filme=int(id_filme))]

    @dbconnectionapp
    def getCidades(self):
        """
        """
        cidades = [i for i in self.execSql("select_cidades")]

        return cidades

    @dbconnectionapp
    def _getCinemasByCidade(self, id_cidade):
        """
        """

        sql = self.execSql("select_cinemas_by_cidade", id_cidade=id_cidade)
        cinemas = ""
        for i in sql:
            cinemas += i["titulo"] + ":" + str(i["id_conteudo"]) + ", "
        cinemas = cinemas[:-2]

        return cinemas

    @dbconnectionapp
    def getFilmesByCinema(self, id_cinema):
        """
        """

        sql = self.execSql("select_filmes_by_cinema", id_cinema=id_cinema)
        filmes = ""
        for i in sql:
            filmes += str(i["id_filme"]) + ":" + i["nome"] + ", "
        filmes = filmes[:-2]

        return filmes

    @dbconnectionapp
    def getTop10(self):
        """
        """

        return [i for i in self.execSql("select_top10")]
