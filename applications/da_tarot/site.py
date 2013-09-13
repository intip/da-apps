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
import unicodedata

MAPA = [{"nome":"Rato", "datas":[(datetime.date(1948, 02, 10),
                                  datetime.date(1949, 01, 28)),
                                 (datetime.date(1960, 01, 28),
                                  datetime.date(1961, 02, 14)),
                                 (datetime.date(1972, 02, 10),
                                  datetime.date(1973, 02, 02)),
                                 (datetime.date(1984, 02, 02),
                                  datetime.date(1985, 02, 19)),
                                 (datetime.date(1996, 02, 19),
                                  datetime.date(1997, 02, 06)),
                                 (datetime.date(2008, 02, 07),
                                  datetime.date(2009, 01, 25))]},
        {"nome":"Boi", "datas":[(datetime.date(1949, 01, 29),
                                 datetime.date(1950, 02, 16)),
                                (datetime.date(1961, 02, 15),
                                 datetime.date(1962, 02, 04)),
                                (datetime.date(1973, 02, 03),
                                 datetime.date(1974, 01, 22)),
                                (datetime.date(1985, 02, 20),
                                 datetime.date(1986, 02, 8)),
                                (datetime.date(1997, 02, 07),
                                 datetime.date(1998, 01, 27)),
                                (datetime.date(2009, 01, 26),
                                 datetime.date(2010, 02, 13))]},
        {"nome":"Tigre", "datas":[(datetime.date(1950, 02, 17),
                                   datetime.date(1951, 02, 05)),
                                  (datetime.date(1962, 02, 05),
                                   datetime.date(1963, 01, 24)),
                                  (datetime.date(1974, 01, 23),
                                   datetime.date(1975, 02, 10)),
                                  (datetime.date(1986, 02, 9),
                                   datetime.date(1987, 01, 28)),
                                  (datetime.date(1998, 01, 28),
                                   datetime.date(1999, 02, 15)),
                                  (datetime.date(2010, 02, 14),
                                   datetime.date(2011, 02, 02))]},
        {"nome":"Coelho", "datas":[(datetime.date(1951, 02, 06),
                                    datetime.date(1952, 01, 26)),
                                   (datetime.date(1963, 01, 25),
                                    datetime.date(1964, 02, 12)),
                                   (datetime.date(1975, 02, 11),
                                    datetime.date(1976, 01, 30)),
                                   (datetime.date(1987, 01, 29),
                                    datetime.date(1988, 02, 16)),
                                   (datetime.date(1999, 02, 16),
                                    datetime.date(2000, 02, 04)),
                                   (datetime.date(2011, 02, 03),
                                    datetime.date(2012, 01, 22))]},
        {"nome":"Drag\xe3o", "datas":[(datetime.date(1952, 01, 27),
                                       datetime.date(1953, 02, 13)),
                                      (datetime.date(1964, 02, 13),
                                       datetime.date(1965, 02, 01)),
                                      (datetime.date(1976, 01, 31),
                                       datetime.date(1977, 02, 17)),
                                      (datetime.date(1988, 02, 17),
                                       datetime.date(1989, 02, 05)),
                                      (datetime.date(2000, 02, 05),
                                       datetime.date(2001, 01, 24)),
                                      (datetime.date(2012, 01, 23),
                                       datetime.date(2013, 02, 9))]},
        {"nome":"Serpente", "datas":[(datetime.date(1953, 02, 14),
                                      datetime.date(1954, 02, 02)),
                                     (datetime.date(1965, 02, 02),
                                      datetime.date(1966, 01, 20)),
                                     (datetime.date(1977, 02, 18),
                                      datetime.date(1978, 02, 06)),
                                     (datetime.date(1989, 02, 06),
                                      datetime.date(1990, 01, 26)),
                                     (datetime.date(2001, 01, 25),
                                      datetime.date(2002, 02, 11)),
                                     (datetime.date(2013, 02, 10),
                                      datetime.date(2014, 01, 30))]},
        {"nome":"Cavalo", "datas":[(datetime.date(1954, 02, 03),
                                    datetime.date(1955, 01, 23)),
                                   (datetime.date(1966, 01, 21),
                                    datetime.date(1967, 02, 8)),
                                   (datetime.date(1978, 02, 07),
                                    datetime.date(1979, 01, 27)),
                                   (datetime.date(1990, 01, 27),
                                    datetime.date(1991, 02, 14)),
                                   (datetime.date(2002, 02, 12),
                                    datetime.date(2003, 01, 31)),
                                   (datetime.date(2014, 01, 31),
                                    datetime.date(2015, 02, 19))]},
        {"nome":"Cabra", "datas":[(datetime.date(1955, 01, 24),
                                   datetime.date(1956, 02, 11)),
                                  (datetime.date(1967, 02, 9),
                                   datetime.date(1968, 01, 29)),
                                  (datetime.date(1979, 01, 28),
                                   datetime.date(1980, 02, 15)),
                                  (datetime.date(1991, 02, 15),
                                   datetime.date(1992, 03, 02)),
                                  (datetime.date(2003, 02, 01),
                                   datetime.date(2004, 01, 21)),
                                  (datetime.date(2015, 02, 19),
                                   datetime.date(2016, 02, 07))]},
        {"nome":"Macaco", "datas":[(datetime.date(1956, 02, 12),
                                    datetime.date(1957, 01, 30)),
                                   (datetime.date(1968, 01, 30),
                                    datetime.date(1969, 02, 16)),
                                   (datetime.date(1980, 02, 16),
                                    datetime.date(1981, 02, 04)),
                                   (datetime.date(1992, 02, 04),
                                    datetime.date(1993, 01, 22)),
                                   (datetime.date(2004, 01, 22),
                                    datetime.date(2005, 02, 8)),
                                   (datetime.date(2016, 02, 8),
                                    datetime.date(2017, 01, 27))]},
        {"nome":"Galo", "datas":[(datetime.date(1957, 01, 31),
                                  datetime.date(1958, 02, 17)),
                                 (datetime.date(1969, 02, 17),
                                  datetime.date(1970, 02, 05)),
                                 (datetime.date(1981, 02, 05),
                                  datetime.date(1982, 01, 24)),
                                 (datetime.date(1993, 01, 23),
                                  datetime.date(1994, 02, 9)),
                                 (datetime.date(2005, 02, 9),
                                  datetime.date(2006, 01, 28)),
                                 (datetime.date(2017, 01, 28),
                                  datetime.date(2018, 02, 18))]},
        {"nome":"C\xe3o", "datas":[(datetime.date(1958, 02, 18),
                                 datetime.date(1959, 02, 07)),
                                (datetime.date(1970, 02, 06),
                                 datetime.date(1971, 01, 26)),
                                (datetime.date(1982, 01, 25),
                                 datetime.date(1983, 02, 12)),
                                (datetime.date(1994, 02, 10),
                                 datetime.date(1995, 01, 30)),
                                (datetime.date(2006, 01, 29),
                                 datetime.date(2007, 02, 17)),
                                (datetime.date(2018, 02, 19),
                                 datetime.date(2019, 02, 04))]},
        {"nome":"Porco", "datas":[(datetime.date(1959, 02, 8),
                                   datetime.date(1960, 01, 27)),
                                  (datetime.date(1971, 01, 27),
                                   datetime.date(1972, 02, 14)),
                                  (datetime.date(1983, 02, 13),
                                   datetime.date(1984, 02, 01)),
                                  (datetime.date(1995, 01, 31),
                                   datetime.date(1996, 02, 18)),
                                  (datetime.date(2007, 02, 18),
                                   datetime.date(2008, 02, 06)),
                                  (datetime.date(2019, 02, 05),
                                   datetime.date(2020, 01, 24))]}]

class Site:
    """
        Depois de ver tudo que precisa dinamicamente, defino os metodos aqui..
        ou nao =D
    """

    @jsoncallback
    @dbconnectionapp
    def getNumerologia(self, nome):
        """
            Calcula a soma numerologica para um nome

            O nome possui os espacos e caracteres especiasi removidos ou
            transformados. O calculo eh feito utilizando o inteiro
            correspondente ao caractere ascii minusculo
        """
        nome = unicode(nome, "latin1")
        soma = 0
        nome = nome.replace(" ", "")
        nome = ''.join((c for c in unicodedata.normalize('NFD', nome)
                        if unicodedata.category(c) != 'Mn'))
        nome = nome.lower()
        for letra in nome:
            soma += ord(letra) - 96

        while len(str(soma)) > 1:
            soma2 = 0
            for digito in str(soma):
                soma2 += int(digito)
            soma = soma2
        url = ""
        if soma > 9:
            soma = 9
        if soma < 0:
            soma = 0
        for i in self.execSql("select_por_titulo2", titulo=str(soma)):
            portal = Portal(id_site=self.id_site, request=self.request)
            url = portal.getUrlByApp(env_site=self.id_site,
                                              schema=self.schema,
                                              id_conteudo=i["id_conteudo"],
                                              exportar=1,
                                              admin=1,
                                              mkattr=1)
        return url

    @jsoncallback
    @dbconnectionapp
    def getAnjo(self, dia, mes):
        """
            Calcula o anjo para um dia do ano
        """
        url="404"
        for i in self.execSql("select_por_titulo", data=str("2013"+"-"+mes+"-"+dia)):
            portal = Portal(id_site=self.id_site, request=self.request)
            url = portal.getUrlByApp(env_site=self.id_site,
                                              schema=self.schema,
                                              id_conteudo=i["id_conteudo"],
                                              exportar=1,
                                              admin=1,
                                              mkattr=1)
        return url

    @jsoncallback
    @dbconnectionapp
    def getSignoChines(self, dia, mes, ano):
        """
            Calcula o signo chines para uma data
        """
        data = datetime.date(int(ano), int(mes), int(dia))
        match = None
        for signo in MAPA:
            for datas in signo["datas"]:
                if datas[0] <= data and data <= datas[1]:
                    match = signo["nome"]
                    break

        url = "404"
        if match:
            url = match
        for i in self.execSql("select_por_titulo2", titulo=match):
            portal = Portal(id_site=self.id_site, request=self.request)
            url = portal.getUrlByApp(env_site=self.id_site,
                                              schema=self.schema,
                                              id_conteudo=i["id_conteudo"],
                                              exportar=1,
                                              admin=1,
                                              mkattr=1)
        return url

    @jsoncallback
    @dbconnectionapp
    def getSorte(self):
        """
            Seleciona um item aleatorio
        """
        url = "404"
        for i in self.execSql("select_sorte"):
            portal = Portal(id_site=self.id_site, request=self.request)
            url = portal.getUrlByApp(env_site=self.id_site,
                                              schema=self.schema,
                                              id_conteudo=i["id_conteudo"],
                                              exportar=1,
                                              admin=1,
                                              mkattr=1)
        return url



    @dbconnectionapp
    def getSorte2(self):
        """
            Seleciona um item aleatorio
        """
##        return self.execSql("select_sorte")

        conteuto = {}
        for i in self.execSql("select_sorte"):
            conteuto['id_conteudo'] = i["id_conteudo"]
            conteuto['descricao'] = i["descricao"].replace("<div>", "").replace("</div>", "")
            conteuto['titulo'] = i["titulo"]

        return conteuto







