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
from time import time, strftime, strptime
from publica import settings
from publica.utils.json import encode, decode
from publica.utils.decorators import dbconnectionapp, serialize, jsoncallback
from publica.core.portal import Portal
import json

class Public(object):

    """
        public class of methods of this content
    """

    @dbconnectionapp
    def getProgramaNoAr(self, limit):
        """
        Retorna para o portlet os programas que estão no ar e os proximos
        """
        portal = Portal(id_site=self.id_site, request=self.request)
        from datetime import datetime, date, time
        today = datetime.now()
        hora_atual =  str(today.hour)+":"+str(today.minute)
        data_atual = str(today.date())
        res = []
        for i in self.execSql("select_programas_no_ar",
                               hora_atual=hora_atual,
                               data_atual=data_atual,
                               limit=int(limit)):
            if i["link"]:
                the_link = portal.renderLink(dados=i["link"],
                                             exportar=1,
                                             render=1)
                if "[target" in the_link:
                    i['link_target'] = the_link.split("[target")[1].replace("]", "")
                    i['link'] = the_link.split("[target")[0]
                else:
                    i["link"] = the_link 
            res.append(i)       
        return res

    @dbconnectionapp
    def getProgramas(self):
        """ busca todos os programas cadastrados para popular o combo-box """

        return list(self.execSql("select_programas"))

    @dbconnectionapp
    def getSessoes(self):
        """ busca todos as sessões cadastrados para popular o combo-box """

        return list(self.execSql("select_secaos"))

    @dbconnectionapp
    def _getProgramasByData(self, data):
        """ busca todos os programas vinculados a tabela associativa """
        portal = Portal(id_site=self.id_site, request=self.request)
        base = portal._getBases()["base_html"]
        try:
            p = strptime(data, "%d/%m/%Y")
            data = strftime("%Y-%m-%d", p)
        except ValueError, e:
            raise UserError(("Ocorreu um erro: "
                             "Data de publica&ccedil;&aring;o "
                             "inv&aacute;lida (%s)") % data)
        res=[]
        for i in self.execSql("select_programas_by_data",
                                  data=str(data)):
            if i["link"]:
                link = json.loads(i["link"])
                if link.get("link", None):
                    i["link_target"] = link["opcoes"]["abrir"] if link["opcoes"]["abrir"] == 'blank' else None
                    i["link"] = link["link"]

                else:
                    the_link = portal.renderLink(dados=i["link"],
                                                 exportar=1,
                                                 render=1)
                    the_link = the_link.replace('<!--#echo var="urlsite" -->', '')
                    the_link = base + the_link
                    if "[target" in the_link:
                        i['link_target'] = the_link.split("[target")[1].replace("]", "")
                        i['link'] = the_link.split("[target")[0]
                    else:
                        i["link"] = the_link

            res.append(i)            
        return res

    @jsoncallback
    def getProgramasByData(self, data):
        """
           retorna todos os programas callback
        """
        return self._getProgramasByData(data)
