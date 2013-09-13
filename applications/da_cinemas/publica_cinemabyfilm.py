#!/usr/bin/python2.6
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
cron utilizada para publicação de todos os cinemas
e filmes que tem um seção vinculada.
"""
import sys
sys.path.append('/home/divirta-se/Publica')
#NEW
from time import time, strftime, strptime
from datetime import datetime, timedelta
from publica.utils.util import FakeRequest
from publica.core.portal import Portal
from publica.admin.user import User
from publica.aplications.da_cinemas.app import App
#site
ID_SITE = 48
ID_USER = 1

#cinema
ID_TREE = 49
ID_APLICATIVO = 71
SCHEMA = "da_cinemas_135162308514"

#filme
SCHEMAFILM ="da_filmes_135177601981"
ID_APLICATIVOFILM = 74
ID_TREEFILM = 54

request = FakeRequest()
request.getCookie = lambda id_usuario:""
user = User(ID_SITE, request)
hsession = user._sessionInit(id_usuario=ID_USER)
request["env.usuario"] = {"id_usuario":ID_USER}
request.request["env_usuario"] = {"id_usuario":ID_USER}
request.getCookie = lambda id_usuario:hsession
portal = Portal(ID_SITE, request)
cinema = App(id_site=ID_SITE,
              schema=SCHEMA,
              request=request)
ids = cinema.getSessaoByCinemaAndFilm()
request.request["bases"] = getDadosSite(ID_SITE, request=request)

if ids['filme']:
    for i in ids['filme']:
        print portal.exportarConteudo(ID_TREEFILM, [{'id_site_conteudo':ID_SITE, \
                                     'id_aplicativo':ID_APLICATIVOFILM,'id_conteudo':i["id_filme"], 'schema':SCHEMAFILM}])
if ids['cinema']:
    for i in ids['cinema']:
       print portal.exportarConteudo(ID_TREE, [{'id_site_conteudo':ID_SITE, \
                                    'id_aplicativo':ID_APLICATIVO,'id_conteudo':i["id_conteudo"], 'schema':SCHEMA}])




