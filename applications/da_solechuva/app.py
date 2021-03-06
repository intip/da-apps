# -*- encoding: LATIN1 -*-
#
# Copyright 2010 Prima Tech.
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
import datetime
from time import time
from urllib import urlopen
from publica.core.portal import Portal
from publica.admin.error import UserError
from publica.utils.json import encode
from publica.utils.decorators import serialize, dbconnectionapp,\
                                     Permission, permissioncron, logportal
from publica.utils.BeautifulSoup import BeautifulStoneSoup
from publica import settings
from site import Site

haslist = False
haslink = False
title = "DA - SoleChuva"
meta_type = "da_solechuva"


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
    def _install(self, title, cidades, url_xml, hash="",
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
        portal = Portal(id_site=self.id_site,
                        request=self.request)
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

        return {"rss":rss,
                "cidades":cidades,
                "url_xml":url_xml,
                "hash":hash}

    @dbconnectionapp
    @serialize
    @Permission("ADM APP")
    def editApp(self, title, cidades, url_xml, hash="",
                       rss_titulo=None, rss_link=None, rss_descricao=None,
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

        dados = {"rss":rss,
                 "cidades":cidades,
                 "url_xml":url_xml,
                 "hash":hash}
        portal = Portal(id_site=self.id_site, request=self.request)
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


    # Hurdle

    def _getDados(self):
        """
        """
        portal = Portal(id_site=self.id_site, request=self.request)
        dados = portal._getApp(env_site=self.id_site,
                               schema=self.schema)["dados"]

        return dados


    def _getXml(self, url):
        """
        """
        return urlopen(url)


    def _extrairDados(self, cidade, p):
        """
        """
        ano = datetime.date.today().year
        root = p.weather.nacional

        for cidade in root.findAll("cidade", nome=cidade):
            l = []
            for d in cidade.findAll(recursive=True):

                data = d["data"]
                icone = d["icone"]
                precipitacao = d["volume"]
                tmin, tmax = d["tmin"], d["tmax"]

                # DATA
                if (data):
                    dia, mes = data.split("/")
                    data = datetime.date(ano, int(mes.strip()), int(dia.strip()))

                    tempo = icone
                    precipitacao = int(precipitacao.split("mm")[0].strip())
                    tmin = int(tmin.split(u"\xba")[0].strip())
                    tmax = int(tmax.split(u"\xba")[0].strip())

                    l.append({
                        'data': data.strftime("%Y-%m-%d"),
                        'tempo': tempo,
                        'precipitacao': precipitacao,
                        'temperatura_minima': tmin,
                        'temperatura_maxima': tmax
                    })

            return l


    @dbconnectionapp
    def _salvarDados(self, cidade, dados):
        """
        """
        self.execSqlBatch("delete_previsao",
                          cidade=cidade)
        
        for p in dados:

            self.execSqlBatch("insert_previsao",
                              cidade_id=cidade,
                              tempo=p["tempo"],
                              data=p["data"],
                              precipitacao=p["precipitacao"],
                              temperatura_minima=p["temperatura_minima"],
                              temperatura_maxima=p["temperatura_maxima"])

            self.execSqlCommit()




    @serialize
    @logportal
    @permissioncron
    def atualizarDados(self, cidades=[]):
        """
        """
        log = ""
        dados = self._getDados()
        if not cidades:
            cidades = dados["cidades"].strip().split("\n")

        xml = self._getXml(dados["url_xml"])
        p = BeautifulStoneSoup(xml)

        for cidade in cidades:
            cidade = cidade.strip()
            if cidade:
                log += " %s" % cidade
                prev = self._extrairDados(cidade, p)
                self._salvarDados(cidade, prev)

        if dados.get("hash"):
            portal = Portal(id_site=self.id_site,
                            request=self.request)
            portal._exportarAppSubOne(env_site=self.id_site,
                                      hash=dados["hash"])

        self.logmsg = "SoleChuva: Atualizado as cidades: %s" % log
        return self.logmsg


