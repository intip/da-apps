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
                                     Permission, permissioncron
from site import Site

haslist = False
haslink = False
title = "DA - Indicador Fin Reuters"
meta_type = "da_indicesfinreuters"

class App(Site):
    """
    """
    title = title
    meta_type = meta_type
    haslist = haslist
    haslink = haslink

    def __init__(self, id_site, schema=None, request=None):
        """
        """
        self.id_site = id_site
        self.schema = schema
        self.request = request


    @dbconnectionapp
    def _install(self, title,
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

        rss = {"titulo":rss_titulo,
               "link":rss_link,
               "descricao":rss_descricao,
               "idioma":rss_idioma,
               "categoria":rss_categoria,
               "copyright":rss_copyright,
               "imagem_titulo":rss_imagem_titulo,
               "imagem_link":rss_imagem_link,
               "rss_imagem":rss_imagem}

        return {"rss":rss}

    @dbconnectionapp
    @serialize
    @Permission("ADM APP")
    def editApp(self, title, rss_titulo=None, rss_link=None, rss_descricao=None,
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

        dados = {"rss":rss}

        portal = Portal(id_site=self.id_site, request=self.request)
        portal._editApp(env_site=self.id_site,
                        schema=self.schema,
                        titulo=title,
                        dados=dados)

        return "Aplicativo configurado com sucesso"

##from os.path import normpath, join, dirname
##from publica.core.portal import Portal
##from publica.core.modulo import Modulo
##from site import Site
##
##
##class App(Modulo, Site):
##    """
##    """
##    meta_type = 'Indicador'
##    tipo = 'indicador'
##
##    def __init__(self, *args, **kargs):
##        """
##        """
##        pass
