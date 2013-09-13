# -*- encoding: iso8859-1 -*-
#
# Copyright 2010 Prima Tech.
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
from urllib import quote
from publica.admin.exchange import getDadosSite
from publica.utils.decorators import serialize, dbconnectionapp, jsoncallback
from publica.core.portal import Portal
from publica.utils.json import encode


class Site(object):
    """
      public method's
    """


    @dbconnectionapp
    def _getProgramacao(self, id_conteudo=None):
        """
          return the data of conteudo, destaque1, destaque2 and destaque tables
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)

        if id_conteudo:
            items = self.execSql("select_conteudo",
                              id_conteudo=int(id_conteudo))
        else:
            items = self.execSql("select_conteudo2")

        for i in items:
            id_conteudo = i["id_conteudo"]

            i["destaque1"] = []
            for item in self.execSql("select_destaque1",
                                     id_conteudo=int(id_conteudo)):
                item["link"] = portal.mklink(dados=item["link"])
                i["destaque1"].append(item)

            return i


    @dbconnectionapp
    def _getDates(self):
        """
            return all content with date (YYYY-MM-DD)
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)

        for i in self.execSql("select_dates",
                              schema=self.schema):
 

            i["url"] = portal.getUrlByApp(env_site=self.id_site,
                                          schema=self.schema,
                                          id_conteudo=i["id_conteudo"],
                                          url=i["url"],
                                          id_treeapp=i["id_treeapp"])

            yield i


