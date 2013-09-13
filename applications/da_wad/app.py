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
from time import time
from publica.core.portal import Portal
from publica.utils.decorators import serialize, dbconnectionapp, Permission
from publica import settings
from site import Site

haslist = False
haslink = False
title = "DA - Wad"
meta_type = "da_wad"


class App(Site):
    """
    """
    title = title
    meta_type = meta_type
    haslist = haslist
    haslink = haslink
    haslogin = True
    auth_schema = True


    def __init__(self, id_site, schema=None, request=None):
        """
        """
        self.id_site = id_site
        self.schema = schema
        self.request = request


    @dbconnectionapp
    def _install(self, title, wad_sid, wad_user, wad_password,
                       site, from_host, return_path, titulo, id_servico,
                       url_wsdl, origin_wsdl):
        """Adiciona uma instancia do produto
        """
        nid = str(time()).replace(".", "")
        if not self.schema:
            self.schema = "%s_%s" % (meta_type, nid)
        self.execSqlu("structure")

        portal = Portal(id_site=self.id_site, request=self.request)
        user_dinamic = portal._getUserDinamic(id_site=self.id_site)
        if user_dinamic:
            self.execSqlu("permissions",
                          user=buffer(user_dinamic))

        if settings.USER_PERMISSION:
            for u in settings.USER_PERMISSION:
                self.execSqlu("permissions_admin",
                              user=buffer(u))

        return {
                "wad_sid":wad_sid,
                "wad_user":wad_user,
                "wad_password":wad_password,
                "from_host":from_host,
                "site":site,
                "return_path":return_path,
                "titulo":titulo,
                "id_servico":int(id_servico),
                "url_wsdl":url_wsdl,
                "origin_wsdl":origin_wsdl}


    @dbconnectionapp
    @serialize
    @Permission("ADM APP")
    def editApp(self, title, wad_sid, wad_user, wad_passwd, 
                      site, from_host, return_path, titulo, id_servico,
                      url_wsdl, origin_wsdl):
        """Edita os atributos da instancia
        """
        dados = {
                 "wad_sid":wad_sid,
                 "wad_user":wad_user,
                 "wad_password":wad_passwd,
                 "from_host":from_host,
                 "site":site,
                 "return_path":return_path,
                 "titulo":titulo,
                 "id_servico":int(id_servico),
                 "url_wsdl":url_wsdl,
                 "origin_wsdl":origin_wsdl}

        portal = Portal(id_site=self.id_site,
                        request=self.request)
        portal._editApp(env_site=self.id_site, 
                        schema=self.schema,
                        titulo=title, 
                        dados=dados)

        user_dinamic = portal._getUserDinamic(id_site=self.id_site)
        if user_dinamic:
            self.execSqlu("permissions",
                          user=buffer(user_dinamic))

        if settings.USER_PERMISSION:
            for u in settings.USER_PERMISSION:
                self.execSqlu("permissions_admin",
                              user=buffer(u))

        return "Aplicativo configurado com sucesso"


