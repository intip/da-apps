# -*- encoding: LATIN1 -*-
#
# Copyright 2009 Prima Tech.
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
    Public methods module.
"""

from publica.utils.decorators import serialize, dbconnectionapp, jsoncallback
from publica.core.portal import Portal

class Site:
    """
        Depois de ver tudo que precisa dinamicamente, defino os metodos aqui..
    """
    def getFiliaisRegiao(self, regiao=None):
        """
            
        """

    @dbconnectionapp
    def getPrimeiraFilial(self, id_conteudo=None):
        """
            Returns the first branch in the database
        """
        for i in self.execSql("select_primeira_filial", 
                                id_conteudo=id_conteudo):
            return i
            
    @dbconnectionapp
    def getConteudoTipoLista(self, tipo=None):
        """
            Returns the list of establishments of (tipo) kind.
        """
        return self.execSql("select_conteudo_tipo", 
                            tipo=tipo)
        
    @dbconnectionapp
    def getTiposSite(self):
        """
            Retuns JSON encoded establishment types.
        """
        return encode([i for i in self.execSql("select_tipos")])
        
    @jsoncallback
    @dbconnectionapp
    def getConteudoBusca(self, regiao=None, categoria=None):
        """
            Returns the results of an establishment search
        """
        lista = []
        portal = Portal(id_site=self.id_site, request=self.request)
        if regiao == "todas" and categoria == "todas":
            for i in self.execSql("select_busca"):
                i["url"] = portal.getUrlByApp(env_site=self.id_site,
                                              schema=self.schema,
                                              id_conteudo=i["id_conteudo"],
                                              exportar=1,
                                              admin=1,
                                              mkattr=1)
                lista.append(i)
            return lista
        elif regiao == "todas":
            for i in self.execSql("select_busca_categoria", 
                                    categoria=categoria):
                i["url"] = portal.getUrlByApp(env_site=self.id_site,
                                              schema=self.schema,
                                              id_conteudo=i["id_conteudo"],
                                              exportar=1,
                                              admin=1,
                                              mkattr=1)
                lista.append(i)
                return lista
        elif categoria == "todas":
            for i in self.execSql("select_busca_regiao", 
                                    regiao=regiao):
                i["url"] = portal.getUrlByApp(env_site=self.id_site,
                                              schema=self.schema,
                                              id_conteudo=i["id_conteudo"],
                                              exportar=1,
                                              admin=1,
                                              mkattr=1)
                lista.append(i)
                return lista
        else:
            for i in self.execSql("select_busca_completa",
                                    regiao=regiao, 
                                    categoria=categoria):
                i["url"] = portal.getUrlByApp(env_site=self.id_site,
                                              schema=self.schema,
                                              id_conteudo=i["id_conteudo"],
                                              exportar=1,
                                              admin=1,
                                              mkattr=1)
                lista.append(i)
                return lista
        
    @jsoncallback
    @dbconnectionapp
    def getFilial(self, id_filial):
        """
            Returns JSON encoded data of a branch.
        """
        for i in self.execSql("select_filial", id_filial=int(id_filial)):
            return i
        
    @jsoncallback
    @dbconnectionapp
    def getTitulo(self, id_conteudo):
        """
            Returns JSON encoded title of an establishment
        """
        print id_conteudo
        for i in self.execSql("select_titulo", id_conteudo=int(id_conteudo)):
            return i
        
        
        
        
        
