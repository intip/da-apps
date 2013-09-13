# coding: utf-8
#
# Copyright 2009 Prima Tech Informatica Ltda.
#
# Licensed under the Environ License, Version 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.cmpsublica.com.br/licenses/ENVIRON-LICENSE-1.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import re
import datetime
from time import strftime, strptime
from urllib import splitquery, splitvalue, unquote, quote
from publica import settings
from publica.core.portal import Portal
from publica.admin.exchange import getDadosSite
from publica.utils.json import encode, decode
from publica.utils.BeautifulSoup import BeautifulSoup
from publica.utils.decorators import dbconnectionapp, serialize, jsoncallback


class Public(object):


    def _dothetags(self, tags):
        """Retornas a tags em umas lista
        """
        if not tags:
            return []

        res = []
        p1 = re.compile('\'(.*?)\'')
        p2 = re.compile('"(.*?)"')
        res += p1.findall(tags)
        res += p2.findall(tags)
        tags = p1.sub('', tags)
        tags = p2.sub('', tags)
        tags = tags.replace('  ', ' ')
        tags = tags.replace('\n', ' ')

        res += tags.strip().split(' ')
        return res


    def _getTags(self, id_conteudo, text=None):
        """
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        for i in portal._getTags(id_site=self.id_site,
                                 id_conteudo=int(id_conteudo),
                                 schema=self.schema,
                                 text=None):
            yield i


    @dbconnectionapp
    def _getNoticiaPublicada(self, id_noticia=None, mkl=None):
        """ Retorna os dados de uma noticia
        """
        noticia = None
        portal = Portal(id_site=self.id_site,
                        request=self.request)

        if not noticia:
            for noticia in self.execSql("select_noticia_publicada_ultima"):
                break

        for noticia in self.execSql("select_noticia_publicada",
                                    id_conteudo=int(id_noticia)):
            break

        if noticia:
            soup = BeautifulSoup(noticia["corpo"],
                                 fromEncoding=settings.GLOBAL_ENCODING)
            for a in soup.findAll("a"):
                href = unquote(a.get("href", "")).strip()
                if href.startswith("#h2href:"):
                    kingkong, dados = href.split("#h2href:", 1)
                    if mkl:
                        href, attrs = mkl(dados=decode(dados))
                        for i in attrs.keys():
                            a[i] = attrs[i]
                    else:
                        href = portal.mklink(dados=dados)

                    if href.find("javascript") >= 0:
                        href = href.replace("[target=blank]", "")
                    elif href.find("target=blank") >= 0:
                        href = href.replace("[target=blank]", "")
                        a["target"] = "blank"

                    a["href"] = href

            noticia["corpo"] = unquote( unicode(soup) )

        return noticia


    @dbconnectionapp
    def _getNoticiaPublicadaUltima(self, id_noticia=None, hash=None, mkl=None):
        """ Retorna os dados de uma noticia ou a ultima do hash
        """
        if id_noticia:
            return self._getNoticiaPublicada(id_noticia=id_noticia,
                                             mkl=mkl)
        elif hash:
            portal = Portal(id_site=self.id_site,
                            request=self.request)

            for i in portal._listarConteudoApp(id_site=self.id_site,
                                               hash=[hash],
                                               comentario=False,
                                               acesso=False,
                                               acesso24h=None,
                                               voto=False,
                                               limit=1)["itens"]:
                return self._getNoticiaPublicada(id_noticia=i["id_conteudo"],
                                                 mkl=mkl)


    @dbconnectionapp
    def _getAutorNoticia(self, id_noticia):
        """Retorna os autores de uma determinada noticia
        """
        return self.execSql("select_autor_noticia",
                            id_conteudo=int(id_noticia))


    def _getAttrNoticia(self, id_noticia):
        """Retorna dados de relação com o portal da noticia
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)

        return portal._getAttrConteudo(id_site=self.id_site,
                                       schema=self.schema,
                                       id_conteudo=id_noticia)


    @dbconnectionapp
    def _getDestaqueSite(self, id_noticia):
        """Retorna as fotos do cadastro de uma noticia
        """
        for i in self.execSql("select_noticia_destaque",
                             id_conteudo=int(id_noticia)):
            return i


    @dbconnectionapp
    def _getFotosSite(self, id_noticia):
        """Retorna as fotos do cadastro de uma noticia
        """
        return self.execSql("select_noticia_fotos",
                            id_conteudo=int(id_noticia))


    @dbconnectionapp
    def _getVideosSite(self, id_noticia):
        """Retorna os videos do cadastro de uma noticia
        """
        return self.execSql("select_videos",
                            id_conteudo=int(id_noticia))


    def _formatarCorpo(self, corpo, fotos=[], editor=None, base_img=None):
        """
        """
        cft = """
        <table width="1" class="foto_noticia" style="float:%(alinhamento)s">
        <tr><td><img src="%(arquivo)s" alt="%(credito)s" title="%(credito)s" border="0"/><td></tr>
        <tr><td>%(legenda)s</td></tr>
        </table>
        """
        if not base_img:
            base_img = ""
        if not corpo:
            corpo = ""
        if not editor:
            corpo = corpo.replace("\n", "<br/>")

        index = 1
        for i in fotos:
            if not i["arquivo"]:
                index += 1
                continue
            if base_img and i["arquivo"].startswith("ns"):
                arquivo = "/".join( i["arquivo"].split("/")[1:] )
                arquivo = "%s%s" % (base_img, arquivo)
            else:
                arquivo = base_img + i["arquivo"]
                
            cfti = cft % {"arquivo":arquivo,
                          "credito": i["credito"],
                          "legenda": i["legenda"],
                          "alinhamento": i["alinhamento"]}

            corpo = corpo.replace("[FOTO%s]" % index, cfti)
            index += 1

        return corpo


    @dbconnectionapp
    def _getSVG(self, id_conteudo):
        """
        """
        dados = {"som":None, "video":None, "galeria":None}
        for i in self.execSql("select_svg",
                              id_conteudo=int(id_conteudo)):
            dados["som"] = i["audio"]
            dados["video"] = i["video"]
            dados["galeria"] = i["galeria"]

        return dados


    @dbconnectionapp
    def _getContentByRetranca(self, retranca):
        """
            Returns the id_conteudo, publicado_em from a content with the field retranca
        """
        for i in self.execSql("select_content_retranca",
                              retranca=retranca):
            return i["id_conteudo"], i["publicado_em"]


    # hurdle

    @jsoncallback
    def getUltimasNoticias(self, hash, limit=20, offset=0,
                                 d1=None, d2=None, qw=None,
                                 exportar=1, corpo=None):
        """
        """
        self.request["exportar"] = exportar
        return self._getUltimasNoticias(hash=hash,
                                        limit=limit,
                                        offset=offset,
                                        d1=d1,
                                        d2=d2,
                                        qw=qw,
                                        exportar=exportar,
                                        render=1,
                                        corpo=corpo)
 

    @dbconnectionapp
    def _getUltimasNoticias(self, hash, limit=20, offset=0,
                                  d1=None, d2=None, qw=None,
                                  exportar=None, render=None,
                                  tags=[], corpo=None):
        """
        """
        if type(hash) is not list:
            hash = [hash]

        portal = Portal(id_site=self.id_site,
                        request=self.request)

        site = getDadosSite(id_site=self.id_site,
                            request=self.request)
        base = site["base_html"]
        base_img = site["base_img"]

        items = portal._listarConteudoApp(id_site=self.id_site,
                                          hash=hash,
                                          comentario=False,
                                          acesso=False,
                                          acesso24h=None,
                                          voto=False,
                                          keywords=qw,
                                          de=d1,
                                          ate=d2,
                                          tags=tags,
                                          limit=limit,
                                          offset=offset,
                                          render=render)
        itens = []
        idcs = []
        idcsd = {}
        items_ = [i for i in items["itens"] 
                                if idcs.append(str(i["id_conteudo"])) or 1]
        if idcs:
            for i in self.execSql("select_svgs",
                                  id_conteudos=buffer(",".join(idcs))):
                idcsd[i["id_conteudo"]] = i

        for i in items_:

            if idcsd.get(i["id_conteudo"]):
                i["audio"] = idcsd.get(i["id_conteudo"])["audio"]
                i["video"] = idcsd.get(i["id_conteudo"])["video"]
                i["galeria"] = idcsd.get(i["id_conteudo"])["galeria"]
            else:
                i["audio"] = None
                i["video"] = None
                i["galeria"] = None

            if corpo:
                res = i["serialized"]()
                if res:
                    corpo = self._formatarCorpo(corpo=res["dados"]["corpo"],
                                                fotos=res["dados"]["foto"],
                                                editor=res["dados"]["editor"],
                                                base_img=base_img)
                    i["corpo"] = corpo
                    i["titulo_categoria"] = res["dados"]["titulo_categoria"]
                    i["autor_nome"] = None
                    i["autor_email"] = None
                    i["autor_grupo"] = None

                    if res["dados"]["autor"]:
                        for x in self.execSql("select_autor_noticia",
                                             id_conteudo=i["id_conteudo"]):
                            i["autor_nome"] = x["nome"]
                            i["autor_email"] = x["email"]
                            i["autor_grupo"] = x["grupo"]
                            break

                    i["serialized"] = res

            itens.append(i)

        return {"res":itens, "qtde":items["qtde"]}


    @jsoncallback
    def getUltimasNoticiasAcessadas(self, hash, limit=20, offset=0,
                                          d1=None, d2=None, qw=None, exportar=1):
        """
        """
        self.request["exportar"] = exportar
        return self._getUltimasNoticiasAcessadas(hash=hash,
                                                 limit=limit,
                                                 offset=offset,
                                                 d1=d1,
                                                 d2=d2,
                                                 qw=qw,
                                                 exportar=exportar,
                                                 render=1)


    @dbconnectionapp
    def _getUltimasNoticiasAcessadas(self, hash, limit=20, offset=0,
                                           d1=None, d2=None, qw=None,
                                           exportar=1, render=None):
        """
        """
        if type(hash) is not list:
            hash = [hash]

        portal = Portal(id_site=self.id_site,
                        request=self.request)
        site = getDadosSite(id_site=self.id_site,
                            request=self.request)
        base = site["base_html"]

        items = portal._listarConteudoApp(id_site=self.id_site,
                                          hash=hash,
                                          comentario=False,
                                          acesso=1,
                                          acesso24h=None,
                                          voto=False,
                                          keywords=qw,
                                          de=d1,
                                          ate=d2,
                                          limit=limit,
                                          offset=offset,
                                          render=render)

        itens = []
        idcs = []
        idcsd = {}
        items_ = [i for i in items["itens"] 
                                if idcs.append(str(i["id_conteudo"])) or 1]
        if idcs:
            for i in self.execSql("select_svgs",
                                  id_conteudos=buffer(",".join(idcs))):
                idcsd[i["id_conteudo"]] = i

        for i in items_:

            if idcsd.get(i["id_conteudo"]):
                i["audio"] = idcsd.get(i["id_conteudo"])["audio"]
                i["video"] = idcsd.get(i["id_conteudo"])["video"]
                i["galeria"] = idcsd.get(i["id_conteudo"])["galeria"]
            else:
                i["audio"] = None
                i["video"] = None
                i["galeria"] = None

            itens.append(i)

        return {"res":itens, "qtde":items["qtde"]}


    @jsoncallback
    def getUltimasNoticiasVotadas(self, hash, limit=20, offset=0,
                                        d1=None, d2=None, qw=None, exportar=1):
        """
        """
        self.request["exportar"] = exportar
        return self._getUltimasNoticiasVotadas(hash=hash,
                                               limit=limit,
                                               offset=offset,
                                               d1=d1,
                                               d2=d2,
                                               qw=qw,
                                               exportar=exportar,
                                               render=1)
 

    @dbconnectionapp
    def _getUltimasNoticiasVotadas(self, hash, limit=20, offset=0,
                                         d1=None, d2=None, qw=None,
                                         exportar=1, render=None):
        """
        """
        if type(hash) is not list:
            hash = [hash]

        portal = Portal(id_site=self.id_site,
                        request=self.request)
        site = getDadosSite(id_site=self.id_site,
                            request=self.request)
        base = site["base_html"]

        items = portal._listarConteudoApp(id_site=self.id_site,
                                          hash=hash,
                                          comentario=False,
                                          acesso=None,
                                          acesso24h=None,
                                          voto=True,
                                          keywords=qw,
                                          de=d1,
                                          ate=d2,
                                          limit=limit,
                                          offset=offset,
                                          rendeer=render)

        itens = []
        idcs = []
        idcsd = {}
        items_ = [i for i in items["itens"] 
                                if idcs.append(str(i["id_conteudo"])) or 1]
        if idcs:
            for i in self.execSql("select_svgs",
                                  id_conteudos=buffer(",".join(idcs))):
                idcsd[i["id_conteudo"]] = i

        for i in items_:

            if idcsd.get(i["id_conteudo"]):
                i["audio"] = idcsd.get(i["id_conteudo"])["audio"]
                i["video"] = idcsd.get(i["id_conteudo"])["video"]
                i["galeria"] = idcsd.get(i["id_conteudo"])["galeria"]
            else:
                i["audio"] = None
                i["video"] = None
                i["galeria"] = None

            itens.append(i)

        return {"res":itens, "qtde":items["qtde"]}


    @jsoncallback
    def getUltimasNoticiasComentadas(self, hash, limit=20, offset=0,
                                           d1=None, d2=None, qw=None, exportar=1):
        """
        """
        self.request["exportar"] = exportar
        return self._getUltimasNoticiasComentadas(hash=hash,
                                                  limit=limit,
                                                  offset=offset,
                                                  d1=d1,
                                                  d2=d2,
                                                  qw=qw,
                                                  exportar=exportar,
                                                  render=1)


    @dbconnectionapp
    def _getUltimasNoticiasComentadas(self, hash, limit=20, offset=0,
                                            d1=None, d2=None, qw=None,
                                            exportar=1, render=None):
        """
        """
        if type(hash) is not list:
            hash = [hash]

        portal = Portal(id_site=self.id_site,
                        request=self.request)
        site = getDadosSite(id_site=self.id_site,
                            request=self.request)
        base = site["base_html"]

        items = portal._listarConteudoApp(id_site=self.id_site,
                                          hash=hash,
                                          comentario=1,
                                          acesso=None,
                                          acesso24h=None,
                                          voto=None,
                                          keywords=qw,
                                          de=d1,
                                          ate=d2,
                                          limit=limit,
                                          offset=offset,
                                          rendeer=render)

        itens = []
        idcs = []
        idcsd = {}
        items_ = [i for i in items["itens"] 
                                if idcs.append(str(i["id_conteudo"])) or 1]
        if idcs:
            for i in self.execSql("select_svgs",
                                  id_conteudos=buffer(",".join(idcs))):
                idcsd[i["id_conteudo"]] = i

        for i in items_:

            if idcsd.get(i["id_conteudo"]):
                i["audio"] = idcsd.get(i["id_conteudo"])["audio"]
                i["video"] = idcsd.get(i["id_conteudo"])["video"]
                i["galeria"] = idcsd.get(i["id_conteudo"])["galeria"]
            else:
                i["audio"] = None
                i["video"] = None
                i["galeria"] = None

            itens.append(i)

        return {"res":itens, "qtde":items["qtde"]}



    @dbconnectionapp
    def maisUltimas(self, limit=20, offset=0, exportar=None, hash=[]):
        """
        """
        exportar = exportar or self.request.get("exportar")
        if not hash:
            hash = [i["hash"] for i in self.execSql("select_treeapp",
                                                    schema=self.schema)]

        return self._getUltimasNoticias(hash=hash,
                                        limit=limit,
                                        offset=offset,
                                        exportar=exportar)


    @dbconnectionapp
    def maisAcessadas(self, limit=20, offset=0, exportar=None, hash=[]):
        """
        """
        exportar = exportar or self.request.get("exportar")
        if not hash:
            hash = [i["hash"] for i in self.execSql("select_treeapp",
                                                   schema=self.schema)]

        return self._getUltimasNoticiasAcessadas(hash=hash,
                                                 limit=limit,
                                                 offset=offset,
                                                 exportar=exportar)


    @dbconnectionapp
    def maisComentadas(self, limit=20, offset=0, exportar=None, hash=[]):
        """
        """
        day = datetime.timedelta(days=2)
        today = datetime.date.today()
        yesterday = today - day

        exportar = exportar or self.request.get("exportar")
        if not hash:
            hash = [i["hash"] for i in self.execSql("select_treeapp",
                                                    schema=self.schema)]

        return self._getUltimasNoticiasComentadas(hash=hash,
                                                  limit=limit,
                                                  offset=offset,
                                                  exportar=exportar,
                                                  d1=yesterday.strftime("%d/%m/%Y"),
                                                  d2=today.strftime("%d/%m/%Y"))


    def getTags(self, limit=10):
        """
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)
 
        return portal._listarTags(id_site=self.id_site,
                                  schema=self.schema,
                                  limit=int(limit))


    @dbconnectionapp
    def maisTag(self, tag, limit=5, exportar=None, offset=0, hash=[]):
        """
        """
        exportar = exportar or self.request.get("exportar")
        if not hash:
            hash = [i["hash"] for i in self.execSql("select_treeapp",
                                                    schema=self.schema)]

        return self._getUltimasNoticias(hash=hash,
                                        tags=[tag],
                                        limit=limit,
                                        offset=offset,
                                        exportar=exportar)


    @dbconnectionapp
    def maisNoticia(self, limit=5, exportar=None, offset=0, hash=[]):
        """
        """
        exportar = exportar or self.request.get("exportar")
        if not hash:
            hash = [i["hash"] for i in self.execSql("select_treeapp",
                                                    schema=self.schema)]

        return self._getUltimasNoticias(hash=hash,
                                        tags=[],
                                        limit=limit,
                                        offset=offset,
                                        exportar=exportar)


    @dbconnectionapp
    def _ultimasAplicativo(self, offset=0, limit=25,
                                 exportar=None, render=None, dt=1):
        """
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)

        items = {"items":[], "qtde":0}
        exportar = self.request.get("exportar") or exportar
        items["qtde"] = self.execSql("select_ultimas_qtde").next()["qtde"]
        for i in self.execSql("select_ultimas",
                              offset=int(offset),
                              limit=int(limit)):
            i["url"] = portal.getUrlByApp(env_site=self.id_site,
                                          schema=self.schema,
                                          id_conteudo=i["id_conteudo"],
                                          exportar=exportar,
                                          admin=render)
            ft = strptime(i["publicado_em"], "%d/%m/%Y %H:%M")
            if dt:
                i["datetime"] = lambda dt,ft=ft: strftime(dt, ft)
            items["items"].append(i)

        return items


    @jsoncallback
    def ultimasAplicativo(self, offset=0, limit=25):
        """
        """
        self.request["exportar"] = 1
        return self._ultimasAplicativo(offset=offset,
                                       limit=limit,
                                       dt=None,
                                       render=1)


    @dbconnectionapp
    def _UltimasApp(self, limit=50, offset=0, exportar=None):
        """
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)

        exportar = self.request.get("exportar") or exportar

        for i in self.execSql("select_ultimas_app",
                              schema=self.schema,
                              limit=int(limit),
                              offset=int(offset)):

            i["url"] = portal.getUrlByApp(env_site=self.id_site,
                                          schema=self.schema,
                                          id_conteudo=i["id_conteudo"],
                                          exportar=exportar)
            yield i


    @dbconnectionapp
    def _maisUltimasApp(self, limit=50, offset=0, exportar=None,
                              dt=1, render=None, samesite=None):
        """
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)

        exportar = self.request.get("exportar") or exportar
 
        res = {"qtde":0, "res":[]} 
        for i in self.execSql("select_ultimas_app",
                              schema=self.schema,
                              limit=int(limit),
                              offset=int(offset)):

            i["url"] = portal.getUrlByApp(env_site=self.id_site,
                                          schema=self.schema,
                                          id_conteudo=i["id_conteudo"],
                                          exportar=exportar,
                                          admin=render,
                                          samesite=samesite)
            if dt:
                i["datetime"] = lambda t, i=i["publicado_em"]:strftime(t, 
                                               strptime(i, "%Y-%m-%d %H:%M:%S"))
            res["res"].append(i)

        res["qtde"] = self.execSql("select_ultimas_app_qtde",
                                   schema=self.schema).next()["qtde"]

        return res


    @jsoncallback
    def maisUltimasApp(self, limit=50, offset=0):
        """
        """
        return self._maisUltimasApp(limit=limit,
                                    offset=offset,
                                    exportar=True,
                                    dt=None,
                                    render=1,
                                    samesite=1)


    @dbconnectionapp
    def UltimaDataEdicao(self, hash, data=None,
                       limit=50, offset=0, exportar=None):
        """
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)

        exportar = self.request.get("exportar") or exportar
        try:
            data = strptime(data, "%d/%m/%Y")
            data = strftime("%Y-%m-%d", data)
        except Exception, e:
            try:
                data = strptime(data, "%Y-%m-%d")
                data = strftime("%Y-%m-%d", data)
            except:
                data = None

        if not data:
            data = strftime("2099-%m-%d")

        if type(hash) is not list:
            hash = [hash]

        for i in hash:
            self.execSqlBatch("select_ultima_data_edicao",
                              hash=i,
                              schema=self.schema,
                              data_edicao=data)

        for i in self.execSqlUnion(limit=int(limit),
                                   order="data_edicao DESC"):
            i["url"] = portal.getUrlByApp(env_site=self.id_site,
                                          schema=self.schema,
                                          id_conteudo=i["id_conteudo"],
                                          exportar=exportar)
            yield i


    @dbconnectionapp
    def maisDataEdicao(self, hash, data=None,
                       limit=50, offset=0, exportar=None, render=None):
        """
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)
 
        exportar = self.request.get("exportar") or exportar
        try:
            data = strptime(data, "%Y-%m-%d")
            data = strftime("%Y-%m-%d", data)
        except Exception, e:
            data = None

        if not data:
            data = strftime("%Y-%m-%d")

        if type(hash) is not list:
            hash = [hash]

        for i in hash:
            self.execSqlBatch("select_data_edicao",
                              hash=i,
                              schema=self.schema,
                              data_edicao=data)

        for i in self.execSqlUnion(limit=int(limit),
                                   order="publicado_em DESC"):
            i["url"] = portal.getUrlByApp(env_site=self.id_site,
                                          schema=self.schema,
                                          id_conteudo=i["id_conteudo"],
                                          exportar=exportar,
                                          admin=render)
            yield i


    @jsoncallback
    def maisDataEdicaoJx(self, hash, data=None,
                         limit=50, offset=0, exportar=None):
        """
        """
        exportar = exportar or self.request.get("exportar")
        return [i for i in self.maisDataEdicao(hash=hash,
                                               data=data,
                                               limit=limit,
                                               offset=offset,
                                               exportar=exportar,
                                               render=1)]
        
    @dbconnectionapp
    def getLastNewsDate(self, hash):
        """
            Returns the data of the last news in the folder with hash=hash
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        for i in self.execSql("select_last_date_by_hash", hash=hash):
            i["url"] = portal.getUrlByApp(env_site=self.id_site,
                                          schema=self.schema,
                                          id_conteudo=i["id_conteudo"],
                                          mkattr=0)
            yield i
    
    @dbconnectionapp
    def getLastNewsIds(self):
        """
            Returns the ids of the last published news
        """
        for i in self.execSql("select_last_ids"):
            yield i
   
 
    @dbconnectionapp
    def getLatestNewsId(self, hash):
        """
            Returns the id of the latest news on a folder
        """
        for i in self.execSql("select_latest", hash=hash):
            return i["id_conteudo"]
    
    
    @dbconnectionapp
    def getContentDate(self, date=None, capa=None, id_conteudo=None):
        """
            Returns the list of id content
        """
        if id_conteudo:
            return [{"id_conteudo": id_conteudo}]

        try:
            date = strptime(date, "%d/%m/%Y")
            date = strftime("%Y-%m-%d", date)
        except:
            date = strftime("%Y-%m-%d")

        if capa:
             return self.execSql("select_content_date_capa",
                                data1="{0} 00:00:00".format(date),
                                data2="{0} 23:59:59".format(date))       
        else:
            return self.execSql("select_content_date",
                                data1="{0} 00:00:00".format(date),
                                data2="{0} 23:59:59".format(date))
