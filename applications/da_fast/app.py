# -*r encoding: LATIN1 -*-
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
from time import time
from publica.core.portal import Portal
from publica.utils.decorators import serialize, dbconnectionapp, Permission
from publica import settings
from site import Site

haslist = False
haslink = False
title = "DA - Fast"
meta_type = "da_fast"


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
    def _install(self, title, url):
        """Adiciona uma instancia do produto
        """
        nid = str(time()).replace(".", "")
        if not self.schema:
            self.schema = "%s_%s" % (meta_type, nid)

        return {"url":url,
                "title":title}


    @dbconnectionapp
    @serialize
    @Permission("ADM APP")
    def editApp(self, title, url):
        """Edita os atributos da instancia
        """
        dados = {"title":title,
                 "url":url}

        portal = Portal(id_site=self.id_site,
                        request=self.request)
        portal._editApp(env_site=self.id_site, 
                        schema=self.schema,
                        titulo=title, 
                        dados=dados)

        return "Aplicativo configurado com sucesso"


    # hurdle


