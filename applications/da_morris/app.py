# encoding: LATIN1 -*-
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
from time import time
from publica.core.portal import Portal
from publica.utils.decorators import serialize, dbconnectionapp, \
                                     Permission, permissioncron, logportal
from publica import settings
from site import Site

haslist = False
haslink = False
title = "DA - Morris"
meta_type = "da_morris"


class App(Site):
    """
    """
    title = title
    meta_type = meta_type
    haslist = haslist
    haslink = haslink
    haslogin = False
    auth_schema = False


    def __init__(self, id_site, schema=None, request=None):
        """
        """
        self.id_site = id_site
        self.schema = schema
        self.request = request


    @dbconnectionapp
    def _install(self, title, path, pagina):
        """Adiciona uma instancia do produto
        """
        nid = str(time()).replace(".", "")
        if not self.schema:
            self.schema = "%s_%s" % (meta_type, nid)

        return {"path":path,
                "pagina":pagina}


    @dbconnectionapp
    @serialize
    @Permission("ADM APP")
    def editApp(self, title, path, pagina):
        """Edita os atributos da instancia
        """
        dados = {"path":path,
                 "pagina":pagina}

        portal = Portal(id_site=self.id_site,
                        request=self.request)
        portal._editApp(env_site=self.id_site, 
                        schema=self.schema,
                        titulo=title, 
                        dados=dados)

        self.__exportInclude()
        return "Aplicativo configurado com sucesso"


    # hurdle

    def __exportInclude(self):
        """
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)

        dados = portal._getApp(env_site=self.id_site,
                               schema=self.schema)

        id_pagina = dados["dados"]["pagina"]
        path = dados["dados"]["path"]
        url = portal.getUrlByPagina(id_pagina=id_pagina,
                                    exportar=1,
                                    adm=1)

        source = urllib.urlopen(url).read()
        if source:

            topo, rodape = source.split("morris-cut")
            portal._addHtml(path=path,
                            filename="topo.html",
                            source=topo)
            portal._addHtml(path=path,
                            filename="rodape.html",
                            source=rodape)

            return "Includes criados"

        return "Ocorreu um problema ao gerar os includes"


    @serialize
    @logportal                           
    @permissioncron
    def _exportInclude(self):
        """
        """
        self.logmsg = ("Includes Morris "
                       "atualizados, site: %s.")  % self.id_site

        return self.__exportInclude()
 
