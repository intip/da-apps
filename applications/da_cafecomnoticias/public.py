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
from urllib import quote
from publica import settings
from publica.admin.exchange import getDadosSite, getSiteByHost
from publica.utils.decorators import serialize, dbconnectionapp, jsoncallback
from urllib import unquote
from publica.core.portal import Portal
from publica.utils.json import encode, decode
from publica.utils.BeautifulSoup import BeautifulSoup
import urllib
import json
import os

class Public(object):

    @dbconnectionapp
    def _getEstabelecimento(self, id_conteudo):
        """
       Retorna os dados de um estabelecimento
        """
        
        for estabelecimento in self.execSql("select_conteudo",
                                            id_conteudo=int(id_conteudo)):
            soup = BeautifulSoup(estabelecimento["descricao"],
                                 fromEncoding=settings.GLOBAL_ENCODING)
            for a in soup.findAll("a"):
                href = unquote(a.get("href", "")).strip()
                if href.find("#h2href:") >= 0:
                    dados = href.split("#h2href:", 1)[-1]
                    href = self._renderLink(dados=dados)

                    if href.find("javascript") >= 0:
                        href = href.replace("[target=blank]", "")
                    elif href.find("target=blank") >= 0:
                        href = href.replace("[target=blank]", "")
                        a["target"] = "blank"

                    a["href"] = href

            estabelecimento["descricao"] = unquote( unicode(soup) )
            return estabelecimento



    def _getAttrEstabelecimento(self, id_estabelecimento):
        """
            return portal data of content

            >>> self._getAttrNoticia(1)
            {'id_treeapp':, 'id_aplicativo':, 'url':,
             'voto':, 'nvoto':, 'acesso':, 'comentario':, 'tags':}
        """
        return self._getAttrContent(schema=self.schema,
                                     id_conteudo=id_estabelecimento)




    @jsoncallback
    @dbconnectionapp   
    def getEstabelecimentosPublicados(self, limit=None, offset=None,
                                      exportar=1, admin=1):

        portal = Portal(id_site=self.id_site,
                        request=self.request)

        
        res = []
        for i in self.execSql("select_estabelecimento_publicado",
                               limit=int(limit),
                               offset=int(offset)):
            i['url'] = self._getUrlByApp(env_site=self.id_site,
                                          schema=self.schema,
                                          id_conteudo=i["id_conteudo"],
                                          exportar=exportar,
                                          admin=admin)
            i['imagem_destaque'] = portal.getUrlByFile(i['imagem_destaque'], id_site=self.id_site)
            i["categorias"]=[]
            for j in self.execSql("select_categoria_estabelecimento", id_conteudo=int(i["id_conteudo"])):
                categoria = {"id_categoria":j["id_categoria"],
                             "nome":j["nome"]}
                i["categorias"].append(categoria)
            res.append(i)
            
        qtde = self.execSql("select_estabelecimento_publicado_count").next()["qtde"]

        return {"itens":res, "qtde": qtde}



    
    @jsoncallback
    @dbconnectionapp   
    def getEstabelecimentosCategoria(self, limit=None, offset=None,
                                     regiao=None, categoria=None, nome=None,
                                     exportar=1, admin=1):

        portal = Portal(id_site=self.id_site,
                        request=self.request)

        if nome=='todos':
            nome=None
        res = []
        if categoria=='todas' and regiao !='todas' and nome == None :
            qtde = self.execSql("select_count_estabelecimento_regiao",
                                 regiao=int(regiao)).next()["qtde"]

            for i in self.execSql("select_estabelecimento_regiao",
                                   regiao=int(regiao),
                                   limit=int(limit),
                                   offset=int(offset)):
                i['url'] = self._getUrlByApp(env_site=self.id_site,
                                              schema=self.schema,
                                              id_conteudo=i["id_conteudo"],
                                              exportar=exportar,
                                              admin=admin)
                i['imagem_destaque'] = portal.getUrlByFile(i['imagem_destaque'], id_site=self.id_site)
                i["categorias"]=[]
                for j in self.execSql("select_categoria_estabelecimento", id_conteudo=int(i["id_conteudo"])):
                    categoria = {"id_categoria":j["id_categoria"],
                                 "nome":j["nome"]}
                    i["categorias"].append(categoria)

                res.append(i)

            return {"itens":res, "qtde":qtde}
      
        elif regiao =='todas' and categoria !='todas' and nome == None :
            qtde = self.execSql("select_count_estabelecimento_categoria",
                                 categoria=int(categoria)).next()["qtde"]

            for i in self.execSql("select_estabelecimento_categoria",
                                   categoria=int(categoria),
                                   limit=int(limit),
                                   offset=int(offset)):
                i['url'] = self._getUrlByApp(env_site=self.id_site,
                                              schema=self.schema,
                                              id_conteudo=i["id_conteudo"],
                                              exportar=exportar,
                                              admin=admin)
                i['imagem_destaque'] = portal.getUrlByFile(i['imagem_destaque'], id_site=self.id_site)
                i["categorias"]=[]
                for j in self.execSql("select_categoria_estabelecimento", id_conteudo=int(i["id_conteudo"])):
                    categoria = {"id_categoria":j["id_categoria"],
                                 "nome":j["nome"]}
                    i["categorias"].append(categoria)
                res.append(i)

            return {"itens":res, "qtde":qtde}

        
        elif regiao =='todas' and categoria =='todas' and nome !=None :

            qtde = self.execSql("select_estabelecimento_nome_count",
                                 nome=nome).next()["qtde"]

            for i in self.execSql("select_estabelecimento_nome",
                                   nome=nome,
                                   limit=int(limit),
                                   offset=int(offset)):
                i['url'] = self._getUrlByApp(env_site=self.id_site,
                                              schema=self.schema,
                                              id_conteudo=i["id_conteudo"],
                                              exportar=exportar,
                                              admin=admin)
                i['imagem_destaque'] = portal.getUrlByFile(i['imagem_destaque'], id_site=self.id_site)
                i["categorias"]=[]
                for j in self.execSql("select_categoria_estabelecimento", id_conteudo=int(i["id_conteudo"])):
                    categoria = {"id_categoria":j["id_categoria"],
                                 "nome":j["nome"]}
                    i["categorias"].append(categoria)

                res.append(i)

            return {"itens":res, "qtde":qtde}
    
        elif categoria =='todas' and regiao !='todas' and nome != None :
    
            qtde = self.execSql("select_estabelecimento_nome_regiao_count",
                                 regiao=int(regiao),
                                 nome=nome).next()["qtde"]

            for i in self.execSql("select_estabelecimento_nome_regiao",
                                   nome=nome,
                                   regiao=int(regiao),
                                   limit=int(limit),
                                   offset=int(offset)):
                i['url'] = self._getUrlByApp(env_site=self.id_site,
                                              schema=self.schema,
                                              id_conteudo=i["id_conteudo"],
                                              exportar=exportar,
                                              admin=admin)
                i['imagem_destaque'] = portal.getUrlByFile(i['imagem_destaque'], id_site=self.id_site)
                i["categorias"]=[]
                for j in self.execSql("select_categoria_estabelecimento", id_conteudo=int(i["id_conteudo"])):
                    categoria = {"id_categoria":j["id_categoria"],
                                 "nome":j["nome"]}
                    i["categorias"].append(categoria)

                res.append(i)

            return {"itens":res, "qtde":qtde}


        elif regiao =='todas' and  categoria !='todas' and nome != None : 

            qtde = self.execSql("select_estabelecimento_nome_categoria_count",
                                 categoria=int(categoria),
                                 nome=nome).next()["qtde"]

            for i in self.execSql("select_estabelecimento_nome_categoria",
                                   nome=nome,
                                   categoria=int(categoria),
                                   limit=int(limit),
                                   offset=int(offset)):
                i['url'] = self._getUrlByApp(env_site=self.id_site,
                                              schema=self.schema,
                                              id_conteudo=i["id_conteudo"],
                                              exportar=exportar,
                                              admin=admin)
                i['imagem_destaque'] = portal.getUrlByFile(i['imagem_destaque'], id_site=self.id_site)
                i["categorias"]=[]
                for j in self.execSql("select_categoria_estabelecimento", id_conteudo=int(i["id_conteudo"])):
                    categoria = {"id_categoria":j["id_categoria"],
                                 "nome":j["nome"]}
                    i["categorias"].append(categoria)

                res.append(i)

            return {"itens":res, "qtde":qtde}
              

        elif categoria != 'todas' and regiao !='todas' and nome==None:
            qtde = self.execSql("select_count_estabelecimento_categoria_regiao",
                                 categoria=int(categoria),
                                 regiao=int(regiao)).next()["qtde"]

            for i in self.execSql("select_estabelecimento_categoria_regiao",
                                   categoria=int(categoria),
                                   regiao=int(regiao),
                                   limit=int(limit),
                                   offset=int(offset)):
                i['url'] = self._getUrlByApp(env_site=self.id_site,
                                              schema=self.schema,
                                              id_conteudo=i["id_conteudo"],
                                              exportar=exportar,
                                              admin=admin)
                i['imagem_destaque'] = portal.getUrlByFile(i['imagem_destaque'], id_site=self.id_site)
                i["categorias"]=[]
                for j in self.execSql("select_categoria_estabelecimento", id_conteudo=int(i["id_conteudo"])):
                    categoria = {"id_categoria":j["id_categoria"],
                                 "nome":j["nome"]}
                    i["categorias"].append(categoria)

                res.append(i)

            return {"itens":res, "qtde":qtde}

        elif categoria != 'todas' and regiao !='todas' and nome !=None:

            qtde = self.execSql("select_count_estabelecimento_categoria_regiao_nome",
                                 nome= nome,
                                 categoria=int(categoria),
                                 regiao=int(regiao)).next()["qtde"]

            for i in self.execSql("select_estabelecimento_categoria_regiao_nome",
                                   nome=nome,
                                   categoria=int(categoria),
                                   regiao=int(regiao),
                                   limit=int(limit),
                                   offset=int(offset)):
                i['url'] = self._getUrlByApp(env_site=self.id_site,
                                              schema=self.schema,
                                              id_conteudo=i["id_conteudo"],
                                              exportar=exportar,
                                              admin=admin)
                i['imagem_destaque'] = portal.getUrlByFile(i['imagem_destaque'], id_site=self.id_site)
                i["categorias"]=[]
                for j in self.execSql("select_categoria_estabelecimento", id_conteudo=int(i["id_conteudo"])):
                    categoria = {"id_categoria":j["id_categoria"],
                                 "nome":j["nome"]}
                    i["categorias"].append(categoria)

                res.append(i)

            return {"itens":res, "qtde":qtde}

        else:
        
            qtde = self.execSql("select_estabelecimento_publicado_count").next()["qtde"]
            
            for i in self.execSql("select_estabelecimento_publicado",
                                   limit=int(limit),
                                   offset=int(offset)):
                i['url'] = self._getUrlByApp(env_site=self.id_site,
                                              schema=self.schema,
                                              id_conteudo=i["id_conteudo"],
                                              exportar=exportar,
                                              admin=admin)
                i['imagem_destaque'] = portal.getUrlByFile(i['imagem_destaque'], id_site=self.id_site)
                i["categorias"]=[]
                for j in self.execSql("select_categoria_estabelecimento", id_conteudo=int(i["id_conteudo"])):
                    categoria = {"id_categoria":j["id_categoria"],
                                 "nome":j["nome"]}
                    i["categorias"].append(categoria)

                res.append(i)

            return {"itens":res, "qtde":qtde}
            

    @dbconnectionapp 
    def getlistagemEstabelecimentos(self, limit=None, offset=None):
        """
        """
        res =[]
        for estabelecimento in self.execSql("select_estabelecimento_publicado",
                                            limit=int(limit),
                                            offset=int(offset)):
            estabelecimento["categorias"] =[]
            for j in self.execSql("select_categoria_estabelecimento", id_conteudo=int(estabelecimento["id_conteudo"])):
                categoria = {"id_categoria":j["id_categoria"],
                             "nome":j["nome"]}
                estabelecimento["categorias"].append(categoria)
            res.append(estabelecimento)
        
        qtde = self.execSql("select_estabelecimento_publicado_count").next()["qtde"]
      
        return {"estabelecimento":res, "qtde":qtde}

  
 
    @dbconnectionapp
    def _getEstabelecimentoPublicado(self, id_conteudo=None):
        """Retorna os dados de uma determinado estabelecimento
        """
        estabelecimento = None
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        try:
            if not id_conteudo:
                for estabelecimento in self.execSql("select_estabelecimento_publicado",
                                                    limit=1,
                                                    offset=0):
                    estabelecimento["categorias"]=[]
                    for j in self.execSql("select_categoria_estabelecimento", 
                                          id_conteudo=int(estabelecimento["id_conteudo"])):
                        categoria = {"id_categoria":j["id_categoria"],
                                     "nome":j["nome"]}
                        estabelecimento["categorias"].append(categoria)    

            else:
                for estabelecimento in self.execSql("select_estabelecimento_publicado_unico",
                                       id_conteudo=int(id_conteudo)):
                    estabelecimento["categorias"]=[]
                    for j in self.execSql("select_categoria_estabelecimento", id_conteudo=int(estabelecimento["id_conteudo"])):
                        categoria = {"id_categoria":j["id_categoria"],
                                     "nome":j["nome"]}
                        estabelecimento["categorias"].append(categoria) 
                    
                    soup = BeautifulSoup(estabelecimento["descricao"],
                                 fromEncoding=settings.GLOBAL_ENCODING)
                    for a in soup.findAll("a"):
                        href = unquote(a.get("href", "")).strip()
                        if href.find("#h2href:") >= 0:
                            dados = href.split("#h2href:", 1)[-1]
                            href = self._renderLink(dados=dados)
                        if href.find("javascript") >= 0:
                            href = href.replace("[target=blank]", "")
                        elif href.find("target=blank") >= 0:
                            href = href.replace("[target=blank]", "")
                            a["target"] = "blank"

                        a["href"] = href
                    estabelecimento["descricao"] = unquote( unicode(soup) )


        except StopIteration:
            pass

        return {"estabelecimento":estabelecimento}


    @dbconnectionapp
    def _getCategorias(self):


        categorias= self.execSql("select_categoria")



        return categorias

    

   
    @dbconnectionapp
    def _getRegioes(self):


        regioes= self.execSql("select_regiao")



        return regioes
    

        
                
                
