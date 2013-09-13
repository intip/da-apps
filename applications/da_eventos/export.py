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

import sys
sys.path.append('/home/icaro/Publica')
#NEW
from time import time, strftime, strptime
from datetime import datetime, timedelta
from publica.utils.util import FakeRequest
from publica.core.portal import Portal
from publica.admin.user import User
from publica.aplications.da_eventos.app import App

from config import ID_SITE, ID_USER, ID_APLICATIVO, SCHEMA, ID_TREE

request = FakeRequest()
request.getCookie = lambda id_usuario:""
user = User(ID_SITE, request)
hsession = user._sessionInit(id_usuario=ID_USER)
request["env.usuario"] = {"id_usuario":ID_USER}
request.request["env_usuario"] = {"id_usuario":ID_USER}
request.getCookie = lambda id_usuario:hsession
portal = Portal(ID_SITE, request)
eventos = App(id_site=ID_SITE,
              schema=SCHEMA,
              request=request)
ids = eventos._getIds()
date = (datetime.now() - timedelta(minutes=3)).timetuple()
publicado_neg = strftime("%Y-%m-%d %H:%M", date)
date2 = (datetime.now() + timedelta(minutes=4)).timetuple()
publicado_pos = strftime("%Y-%m-%d %H:%M", date2)
if ids:
    for i in ids:
        eventos._getConteudo(int(i["id_conteudo"]))        
        if (i["publicado_em"] >= publicado_neg) and (i["publicado_em"] <= publicado_pos):
            portal.exportarConteudo(ID_TREE, [{'id_site_conteudo':ID_SITE, \
                                    'id_aplicativo':ID_APLICATIVO,'id_conteudo':i["id_conteudo"], 'schema':SCHEMA}])
            


