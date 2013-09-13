# -* encoding: LATIN1 -*-
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
from datetime import datetime
from os import makedirs, chmod
from time import time, strftime, strptime
from publica.core.portal import Portal
from publica.admin.error import UserError
from publica.utils.decorators import serialize, dbconnectionapp, \
                                     Permission, permissioncron, logportal
from publica import settings
from site import Site

haslist = False
haslink = False
title = "DA - Indicador Fin CMA"
meta_type = "da_indicesfincma"
#path_base = "/home/uai/ad-hoc/indicador"

class App(Site):
    """
    """
    title = title
    meta_type = meta_type
    haslist = haslist
    haslink = haslink
    #path_base = path_base

    def __init__(self, id_site, schema=None, request=None):
        """
        """
        self.id_site = id_site
        self.schema = schema
        self.request = request


    @dbconnectionapp
    def _install(self, title, path_base, hash,
                       rss_titulo=None, rss_link=None, rss_descricao=None,
                       rss_idioma=None, rss_categoria=None, rss_copyright=None,
                       rss_imagem_titulo=None, rss_imagem_link=None,
                       rss_imagem=None):
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

        rss = {"titulo":rss_titulo,
               "link":rss_link,
               "descricao":rss_descricao,
               "idioma":rss_idioma,
               "categoria":rss_categoria,
               "copyright":rss_copyright,
               "imagem_titulo":rss_imagem_titulo,
               "imagem_link":rss_imagem_link,
               "rss_imagem":rss_imagem}

        return {"rss":rss, "path_base":path_base, "hash":hash}

    @dbconnectionapp
    @serialize
    @Permission("ADM APP")
    def editApp(self, title, path_base, hash, rss_titulo=None, rss_link=None, rss_descricao=None,
                       rss_idioma=None, rss_categoria=None, rss_copyright=None,
                       rss_imagem_titulo=None, rss_imagem_link=None,
                       rss_imagem=None):
        """Edita os atributos da instancia
        """
        rss = {"titulo":rss_titulo,
               "link":rss_link,
               "descricao":rss_descricao,
               "idioma":rss_idioma,
               "categoria":rss_categoria,
               "copyright":rss_copyright,
               "imagem_titulo":rss_imagem_titulo,
               "imagem_link":rss_imagem_link,
               "rss_imagem":rss_imagem}

        dados = {"rss":rss, "path_base":path_base, "hash":hash}
        portal = Portal(id_site=self.id_site, request=self.request)

        user_dinamic = portal._getUserDinamic(id_site=self.id_site)
        if user_dinamic:
            self.execSqlu("permissions",
                          user=buffer(user_dinamic))

        if settings.USER_PERMISSION:
            for u in settings.USER_PERMISSION:
                self.execSqlu("permissions_admin",
                              user=buffer(u))

        portal._editApp(env_site=self.id_site,
                        schema=self.schema,
                        titulo=title,
                        dados=dados)

        return "Aplicativo configurado com sucesso"

    @Permission("ADM APP")
    def indicadores(self, xmls=['cambio.xml','indices.xml','indicadores.xml'], papeis=['DOL COM','PTAX850','DJI']):
        from packages.elementtree import ElementTree as ET

        portal = Portal(id_site=self.id_site,
                        request=self.request)
        dados = portal._getApp(env_site=self.id_site,
                               schema=self.schema)["dados"]

        path_base = dados["path_base"]

        retorno = []

        for arq_xml in xmls:
            path_xml = path_base + '/' + arq_xml
            root = ET.parse(path_xml).getroot()
            for c in root.getchildren():
                if(c.find('PAPEL').text in papeis):
                    dictSaida = {}
                    for node in c:
                        dictSaida[node.tag] = str(unicode(node.text).encode('latin1')).replace('.',',')

                    retorno.append(dictSaida)

        return retorno

    @serialize
    @logportal
    @permissioncron
    def atualizarDados(self):
        """
        """

        portal = Portal(id_site=self.id_site,
                        request=self.request)
        dados = portal._getApp(env_site=self.id_site,
                               schema=self.schema)["dados"]

        if dados.get("hash"):
            portal._exportarAppSubOne(env_site=self.id_site,
                                      hash=dados["hash"])

        self.logmsg = "Indicador Fin CMA: Atualizando. "
        return self.logmsg
