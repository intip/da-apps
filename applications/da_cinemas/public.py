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
from publica import settings
from datetime import datetime
from publica.core.portal import Portal
from publica.utils.json import encode, decode
from publica.utils.decorators import dbconnectionapp, serialize, jsoncallback


class Public(object):

    """
        public class of methods of this content
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
    def getFilmesLast(self, limit=30):
        data = datetime.now()
        data = str(data.date())
        return [i for i in self.execSql("select_filmes_last",
                                         limit=int(limit),
                                         data=data)]

    @dbconnectionapp
    def getCinemasByFilme(self, id_filme):
        """
        """
        data = datetime.now()
        data = str(data.date())
        retorno = []
        for cinema in self.execSql("select_Cinemas_id_filme",
                                           id_filme=int(id_filme),
                                           data_atual=data):
            cinema['sessoes'] = []
            for i in self.execSql("select_sessoes_filme",
                               id_filme=int(id_filme),
                               id_conteudo=int(cinema['id_conteudo']),
                               data_atual=data):
                horarios = eval(i['horarios'])
                for x in horarios:
                    x['hora'] = x['hora']+':'+x['minuto']
                    del x['minuto']
                i['horarios'] = horarios
                cinema['sessoes'].append(i)
            retorno.append(cinema)
        return retorno

    @dbconnectionapp
    def getSalasByFilme(self, id_cinema):
        """
        """
        pass

    @jsoncallback
    @dbconnectionapp
    def getCidadesJson(self):
        """
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        dadosapp = portal._getApp(env_site=self.id_site,
                                  schema=self.schema)["dados"]
        cidades = []
        for i in self.execSql("select_cidades"):
            cidades.append(i)

        return cidades

    @dbconnectionapp
    def listaFilmes(self, limit=3):
        """
        """
        data = datetime.now()
        data = str(data.date())
        filmes = [] 
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        dadosapp = portal._getApp(env_site=self.id_site,
                                  schema=self.schema)["dados"]       
        for i in self.execSql("select_filmes_cartaz",SCHEMA=buffer(dadosapp['auth_schema']),
                                                     data_atual=data,
                                                     limit=int(limit)):
            if type (i['img'] == 'str'):
                i['img'] = i['img']
            else:
                i['img'] = i['img'][0]
            filmes.append(i)
        return filmes

    @dbconnectionapp
    def getFilme(self, id_filme):
         """
         """
         filme = self.execSql("select_filme",id_filme=int(id_filme)).next()
         return filme 

    @dbconnectionapp
    def getSessoesByFilme(self, id_conteudo, id_filme):
        """
        """
        for i in self.execSql("select_sessoes_filme",
                               id_filme=int(id_filme),
                               id_conteudo=int(id_conteudo)):
            horarios = eval(i['horarios'])
            for x in horarios:
                x['hora'] = x['hora']+':'+x['minuto']
                del x['minuto']
            i['horarios'] = horarios
            yield i
    
    @dbconnectionapp
    @jsoncallback
    def getFilmesBySessaoJson(self):
        """
        """
        data = datetime.now()
        data = str(data.date())
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        dadosapp = portal._getApp(env_site=self.id_site,
                                  schema=self.schema)["dados"]
        filmes =[]
        for i in self.execSql("select_filmes_sessoes",
                              SCHEMA=buffer(dadosapp['auth_schema']),
                              data_atual=data):
            i['url'] = portal.getUrlByApp(env_site=self.id_site, schema=dadosapp['auth_schema'], id_conteudo=i['id_conteudo'], exportar=1,admin=1)
            filmes.append(i)
        return filmes

                                   
    @dbconnectionapp
    def getFilmesMaisVotados(self, hash, limit=20, offset=0,
                                         d1=None, d2=None, qw=None,
                                         exportar=1, render=None,
                                         sametree=None, samesite=None):
        """
            calls _getListContent portal method
            to retrieve the content's tree form the parameter hash with the most votes

            @hash: list of string of tree hash identification
            @limit: size of items to retrieve

            >>> self.getFilmesMaisvotados(hash=['94169735419684109'])
            {"res":[...], "qtde":10}
            
            "res" is a list of tuples, the first value is id_conteudo and the second the votes.
        """
        id_site_origin = getSiteByHost(self.id_site, self.request)
        if id_site_origin:
            id_site_origin = id_site_origin["id_site"]
            if id_site_origin == int(self.id_site):
                id_site_origin = None

        if type(hash) is not list:
            hash = [hash]

        site = getDadosSite(id_site=self.id_site,
                            request=self.request)
        base = site["base_html"]

        items = self._getListContent(id_site=self.id_site,
                                      hash=hash,
                                      comentario=False,
                                      acesso=None,
                                      acesso24h=None,
                                      voto=False,
                                      keywords=qw,
                                      de=d1,
                                      ate=d2,
                                      limit=limit,
                                      offset=offset,
                                      render=render,
                                      sametree=sametree,
                                      samesite=samesite,
                                      id_site_origin=id_site_origin)
        
        itens = {}
        items_ = items['itens']                   
        for i in items_:
        
            itens[i['id_conteudo']] = i['voto']

        itens = [(v, k) for v, k in itens.iteritems()]

        itens = sorted(itens, key=lambda x: x[1])
        itens.reverse()

        return {"res":itens, "qtde":items["qtde"]}

    @serialize
    @dbconnectionapp
    def getCinemasByCidade(self, id_cidade, id_treeapp=None):
        """
        """
        cinemas = []
        for i in self.execSql("select_cinema_cidade",
                               id_cidade=int(id_cidade)):
            portal = Portal(id_site=self.id_site,
                            request=self.request)
            i['url'] = portal.getUrlByApp(env_site=self.id_site, schema=self.schema, id_conteudo=i['id_conteudo'], exportar=1,admin=1)
            cinemas.append(i)
        return cinemas

    
    @dbconnectionapp
    def getCidadeCinemaDict(self):
        """
        """
        cidades_cinema = {}        
        for i in self.execSql("select_cidades"):
            dados_cine = []
            for j in self.execSql("select_cinema_cidade",
                                   id_cidade=int(i['id_cidade'])):
                portal = Portal(id_site=self.id_site,
                                request=self.request)
                j['url'] = portal.getUrlByApp(env_site=self.id_site, schema=self.schema, id_conteudo=j['id_conteudo'], exportar=1,admin=1)
                dados = {"id_conteudo":j["id_conteudo"],
                         "titulo":j["titulo"],
                         "url":j["url"]}
                dados_cine.append(dados)
            cidades_cinema[i["nome"]] = dados_cine 
        return cidades_cinema                                        
               
    
    @dbconnectionapp
    def getCinemasByIdCidade(self, id_cidade, id_treeapp=None):
        """
        """
        cinemas = []
        for i in self.execSql("select_cinema_cidade",
                               id_cidade=int(id_cidade)):
            portal = Portal(id_site=self.id_site,
                            request=self.request)
            i['url'] = portal.getUrlByApp(env_site=self.id_site, schema=self.schema, id_conteudo=i['id_conteudo'], exportar=1,admin=1)
            cinemas.append(i)
        return cinemas

    @dbconnectionapp
    def getCinemasCidade(self, nome_cidade):
        """
        """
        cinemas = []
        for i in self.execSql("select_cinema_nome_cidade",
                               nome_cidade=nome_cidade):
            portal = Portal(id_site=self.id_site,
                            request=self.request)
            i['url'] = portal.getUrlByApp(env_site=self.id_site, schema=self.schema, id_conteudo=i['id_conteudo'], exportar=1, admin=1)
            cinemas.append(i)
        return cinemas

    @dbconnectionapp
    def getCinemaByIdCinema(self, id_cinema):
        """
        """
        data = datetime.now()
        data = str(data.date())
        dic = {}
        horario = []
        salas = []
        sessao_list = []
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        dadosapp = portal._getApp(env_site=self.id_site,
                                  schema=self.schema)["dados"]
        cinema = self.execSql("select_cinema",
                               id_conteudo=int(id_cinema)).next()
        fotos = [i for i in self.execSql("select_fotos_conteudo",
                                         id_conteudo=int(id_cinema))]
        filmes = [i for i in self.execSql("select_filmes_conteudo",
                                          SCHEMA=buffer(dadosapp['auth_schema']),
                                          id_conteudo=int(id_cinema),
                                          data_atual=data)]
        for i in filmes:
            sessao = {}
            sessao["id_sessao"] = i["id_sessao"]
            horarios = eval(i["horarios"])
            horario_str = ""
            for x in horarios:
                horario_str += x["hora"]+":"+x["minuto"] + "  "
            horario.append(horario_str)
            sessao["horario"] = horario_str
            sessao["filme"] = i
            sessao["sala_nome"] = i["sala_nome"]
            salas.append(i["sala_nome"])
            sessao_list.append(sessao)
            
        return {"cinema": cinema,
                "fotos": fotos,
                "salas": salas,
                "sessao": sessao_list,
                "horarios": horario,
                "filmes": filmes}     
