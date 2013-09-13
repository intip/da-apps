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
    Public methods module.
"""

from publica.utils.decorators import serialize, dbconnectionapp, jsoncallback
from publica.core.portal import Portal
import datetime

SIGNOS = (("Aqu\xe1rio", 120, 218),
          ("Peixes", 219, 319),
          ("\xc1ries", 320, 419),
          ("Touro", 420, 520),
          ("G\xeameos", 521, 619),
          ("C\xe2ncer", 620, 721),
          ("Le\xe3o", 722, 821),
          ("Virgem", 822, 921),
          ("Libra", 922, 1021),
          ("Escorpi\xe3o", 1022, 1121),
          ("Sagit\xe1rio", 1122, 1220),
          ("Capric\xf3rnio", 1221, 119))

FILE = "/home/chacras/horoscopo_files/hor{0}.txt"

class Site:
    """
        Depois de ver tudo que precisa dinamicamente, defino os metodos aqui..
        ou nao =D
    """

    @jsoncallback
    @dbconnectionapp
    def getAscendente(self, data, offset):
        """
            Calcula o anjo para um dia do ano
        """
        i = 0
        data = int(data)
        for signo in SIGNOS:
            if data >= signo[1] and data <= signo[2] or i > 10:
                break
            i+=1
        pos = i + int(offset)
        if pos > 11:
            pos -= 12
        url = SIGNOS[pos][0]
        for i in self.execSql("select_por_titulo", titulo=url):
            portal = Portal(id_site=self.id_site, request=self.request)
            url = portal.getUrlByApp(env_site=self.id_site,
                                              schema=self.schema,
                                              id_conteudo=i["id_conteudo"],
                                              exportar=1,
                                              admin=1,
                                              mkattr=1)
        return {"url":url, "nome":SIGNOS[pos][0]}

    @jsoncallback
    @dbconnectionapp
    def getPar(self, bom=[], ruim=[]):
        lista = set()
        for i in bom:
            for j in self.execSql("select_nome", id_caracteristica=i):
                lista.add(j["id_conteudo"])
        for i in ruim:
            for j in self.execSql("select_nome", id_caracteristica=i):
                if j["id_conteudo"] in lista and len(lista) > 1:
                    lista.remove(j["id_conteudo"])
        for i in lista:
            portal = Portal(id_site=self.id_site, request=self.request)
            url = portal.getUrlByApp(env_site=self.id_site,
                                              schema=self.schema,
                                              id_conteudo=i,
                                              exportar=1,
                                              admin=1,
                                              mkattr=1)
            for i in self.execSql("select_titulo", id_conteudo=i):
                return {"url":url, "nome":i["titulo"]}
        return "404"

    def _getPrevisao(self, signo):
        """

        """
        arq = FILE.format(str(datetime.datetime.now().day).zfill(2))
        with open(arq) as f:
            lines = f.readlines()
            i = 0
            for line in lines:
                if line[:len(signo)] == signo.upper():
                    return lines[i+5]
                i += 1















