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
import urllib
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
hasportlet = True
title = "DA - Morris"
meta_type = "da_morris"


class Plug:
    """
    """
    title = title
    meta_type = meta_type
    hasapp = hasapp
    haspage = haspage
    haslist = haslist
    hasportlet = hasportlet


    def __init__(self, id_site, id_plugin=None, request=None, dados={}):
        """
        """
        self.id_plugin = id_plugin
        self.id_site = id_site
        self.request = request
        self.dados = dados


    def _install(self, title, path, pagina):
        """Adiciona uma instancia do plugin
        """
        return {"titulo":title,
                "path":path,
                "pagina":pagina}


    @serialize
    @Permission("ADM PLUG")
    def editPlug(self, title, path, pagina):
        """Edita os atributos do plugin
        """
        dados = {"titulo":title,
                 "path":path,
                 "pagina":pagina}
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        portal._editPlug(env_site=self.id_site,
                         id_plugin=self.id_plugin, 
                         title=title, 
                         dados=dados)

        return "Plugin configurado com sucesso"


    @serialize
    def actionWidget(self):
        """
        """
        return {"show":""} 


    def _action(self, id_treeapp, schema, id_conteudo, link,
                      add=None, edit=None, delete=None, dados={}):
        """ this plugin doesn't use action on application
        """
        pass


    def _actionPortlet(self, id_portlet, dados={}):
        """
        """
        self.__exportInclude()


    def __exportInclude(self):
        """
        """
        portal = Portal(id_site=self.id_site,
                        request={"exportar":1})

        id_pagina = self.dados["pagina"]
        path = self.dados["path"]
        url = portal.getUrlByPagina(id_pagina=id_pagina,
                                    exportar=1,
                                    adm=1)

        source = urllib.urlopen(url).read()
        if source:

            source = source.split("morris-cut")
            if len(source) == 2:
                topo, rodape = source
                portal._addHtml(path=path,
                                filename="topo.html",
                                source=topo)
                portal._addHtml(path=path,
                                filename="rodape.html",
                                source=rodape)

                self.logmsg = ("Includes Morris "
                               "atualizados, site: %s.")  % self.id_site
                return "Includes criados"
            else:
                raise UserError(("A P&aacute;gina n&atilde;o &eacute; "
                                "um include Morris v&aacute;lido. "
                                "eg. morris-cut %s") % url)

        raise UserError(("Ocorreu um problema ao gerar os includes: "
                                "a p&aacute;gina n&atilde;o retornou conte&uacute;do"))


