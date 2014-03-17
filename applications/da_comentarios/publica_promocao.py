#!/usr/bin/env python2.6
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

import sys
import optparse

parser = optparse.OptionParser(usage="%prog [options]")
parser.add_option("-p", "--path",
                  action="store", dest="PATH", type="string",
                  help="Path to Publica folder")
parser.add_option("-s", "--schema",
                  action="store", dest="SCHEMA", type="string",
                  help="Schema app")
parser.add_option("-s", "--pathad",
                  action="store", dest="PATHAD", type="string",
                  help="Path ad-hoc")

(options, args) = parser.parse_args()
sys.path.append(options.PATH or "/home/publica/Publica")
sys.path.append(options.PATHAD or "/home/publica/ad-hoc")

import crontab_vars
import publica.settings
from publica.settings import MAGIC_KEY 
from publica.admin.exchange import getDadosSite
from publica.db.resolver import closeConnections
from publica.utils.util import FakeRequest, lockfile, unlockfile
from publica.utils.decorators import serializeit
from publica.aplications.da_promocao.app import App

publica.settings.NONFULLACCESS = True
publica.settings.DATABASE_HOST = crontab_vars.DB_HOST
publica.settings.DATABASE_USER = crontab_vars.DB_USER
publica.settings.DATABASE_PASSWORD = crontab_vars.DB_PASSWORD
publica.settings.DATABASE_PORT = crontab_vars.DB_PORT
publica.settings.USER_OWNER = crontab_vars.USER_ADMIN # superesportes
publica.settings.USER_GROUP = crontab_vars.USER_APACHE # apache

ID_SITE = crontab_vars.ID_SITE
TSIGHUP = crontab_vars.TSIGHUP
TSIGKILL = crontab_vars.TSIGKILL

if not options.SCHEMA:
    print "passar o parametro -s 'schema do app'"
SCHEMA = options.SCHEMA

@serializeit
def action():
    request = FakeRequest()
    request.request["bases"] = getDadosSite(ID_SITE,
                                            request=request)

    app = App(id_site=ID_SITE,
              schema=SCHEMA,
              request=request)
    out = app._autoSort(mk=MAGIC_KEY)
    closeConnections()
    print out
 

lock = lockfile(__file__, TSIGHUP, TSIGKILL)
if lock:   
   out = action()

   unlockfile(lock, __file__)
