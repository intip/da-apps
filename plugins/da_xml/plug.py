# -*- encoding: iso8859-1 -*-
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
from time import time, strftime, strptime
from publica.core.portal import Portal
from publica.admin.error import UserError
from publica.utils.json import encode
from publica.utils.decorators import serialize, dbconnectionapp,\
                                     Permission, logportal
from publica.utils.BeautifulSoup import BeautifulSoup, Tag
from publica.admin.exchange import getDadosSite
from publica import settings

hasapp = True
haspage = False
haslist = False
title = "DA - Xml"
meta_type = "da_xml"


class Plug:
    """
    """
    title = title
    meta_type = meta_type
    hasapp = hasapp
    haspage = haspage
    haslist = haslist


    def __init__(self, id_site, id_plugin=None, request=None, dados={}):
        """
        """
        self.id_plugin = id_plugin
        self.id_site = id_site
        self.request = request
        self.dados = dados


    def _install(self, title, path):
        """Adiciona uma instancia do plugin
        """
        return {"titulo":title,
                "path":path}


    @serialize
    @Permission("ADM PLUG")
    def editPlug(self, title, path):
        """Edita os atributos do plugin
        """
        dados = {"titulo":title,
                 "path":path}
        portal = Portal(id_site=self.id_site, request=self.request)
        portal._editPlug(env_site=self.id_site,
                         id_plugin=self.id_plugin,
                         title=title,
                         dados=dados)

        return "Plugin configurado com sucesso"


    def _action(self, id_treeapp, schema, id_conteudo, link,
                      add=None, edit=None, delete=None, dados={}):
        """
        """
        if not link:
            return
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        link = "/".join( link.split("/")[:-1] )
        
        src = portal._readFile(path="htmls/%s/index.xml" % link)
        if src:
            
            fd = open("%s%s,%s,%s.xml" % (self.dados["path"],
                                         schema,
                                         self.id_site,
                                         id_conteudo), "w")
            
            soup = BeautifulSoup(src,
                                 fromEncoding=settings.GLOBAL_ENCODING)

            for item in soup.findAll("rdf:description"):
                if add:
                    site = getDadosSite(id_site=self.id_site,
                            request=self.request)
                    base = site["base_html"]
                    tit = portal._getConteudoSite(env_site=self.id_site,
                                                  id_conteudo=id_conteudo, 
                                                  schema=schema)['url']
                    item.__setitem__("rdf:about", base+tit)
                ## push para alertar usuário de uma notícia importante
                ## Neste metodo sempre envia false
                tag = Tag(soup, "dc:push", [])
                tag['rdf:enviar'] = 'false'
                item.insert(0, tag)


                if add:
                    status = "added"
                elif edit:
                    status = "edited"
                elif delete:
                    status = "deleted"
                else:
                    status = "added"
                tag = Tag(soup, "dc:status", [])
                tag.insert(0, status)
                item.insert(0, tag)


                dadosite = getDadosSite(self.id_site)

                veiculo = dadosite["titulo"]
                tag = Tag(soup, "dc:veiculo", [])
                tag.insert(0, veiculo)
                item.insert(0, tag)

                base_img = dadosite["base_app"]
                tag = Tag(soup, "dc:base_img", [])
                tag.insert(0, base_img)
                item.insert(0, tag)

                src = unicode(soup)
                src = src.replace("<?xml version='1.0' encoding='utf-8'?>",
                                  "<?xml version='1.0' encoding='latin1'?>")

            fd.write(src.encode(settings.GLOBAL_ENCODING))
            fd.close()


    @serialize
    def actionWidget(self):
        """
        """
        return {"show":""}




