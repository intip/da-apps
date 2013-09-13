# coding: utf-8
#
# Copyright 2009 Prima Tech Informatica Ltda.
#
# Licensed under the Environ License, Version 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.cmspublic.com.br/licenses/ENVIRON-LICENSE-1.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from random import random
from os import rename
from time import time, strftime, strptime
from publica.core.portal import Portal
from publica.admin.error import UserError
from publica.utils.json import encode
from publica.utils.decorators import serialize, dbconnectionapp,\
                                     Permission, logportal
from publica.utils.BeautifulSoup import BeautifulSoup, Tag
from publica.admin.exchange import getDadosSite
from publica import settings
from fast.daFastXmlFileNoticia import daFastXmlFileNoticia
from fast.daFastXmlFileFoto import daFastXmlFileFoto
try:
    from conf_sites import conf_sites
except ImportError:
    conf_sites = None

hasapp = True
haspage = False
haslist = False
hasportlet = False
title = "DA - Fast Export"
meta_type = "da_fast_export"


class Plug:
    """
    """
    title = title
    meta_type = meta_type
    hasapp = hasapp
    haspage = haspage
    haslist = haslist


    def __init__(self, id_site, id_plugin=None, request=None, dados={}):
        """
        """
        self.id_plugin = id_plugin
        self.id_site = id_site
        self.request = request
        self.dados = dados


    def _install(self, title, path, origem, portal):
        """Adiciona uma instancia do plugin
        """
        if not path.endswith("/"):
            path = path + "/"

        return {"titulo":title,
                "path":path,
                "origem":origem,
                "portal":portal}


    @serialize
    @Permission("ADM PLUG")
    def editPlug(self, title, path, origem, portal):
        """Edita os atributos do plugin
        """
        if not path.endswith("/"):
            path = path + "/"


        dados = {"titulo":title,
                 "path":path,
                 "origem":origem,
                 "portal":portal}

        portal = Portal(id_site=self.id_site,
                        request=self.request)
        portal._editPlug(env_site=self.id_site,
                         id_plugin=self.id_plugin, 
                         title=title, 
                         dados=dados)

        return "Plugin configurado com sucesso"


    @serialize
    def actionWidget(self):
        """
          This plugin does not use actions on application's list
        """
        return {"show":""}


    def _action(self, id_treeapp, schema, id_conteudo, link,
                      add=None, edit=None, delete=None, dados={}):
        """
           Get data from content and call the fast writer 
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)

	if not dados:
            dados = portal._getContentLink({"modulo":
                   {"id_site":self.id_site , "schema":schema,
                    "id_pk":id_conteudo}})
            if not dados:
                return
            dados = dados["serialized"]()


        if schema.find("foto") >= 0:

            """
            {"atualizado_em": "04/12/2010 12:07", 
             "dados": {"destaque": [{"titulo": "", "img": "", "descricao": ""}],
                       "foto": [{"ordem": 0, "img": "ns2/...", "credito": "",
                                 "link": "javascript:void(0)",
                                 "embed": "", "thumbnail": "", "descricao": ""},...],
                       "tags": [], "id_marca": "", "titulo": "",
                       "alinhamento": "topo_esquerda", "descricao": ""},
             "nvoto": 0, "expira_em": null, "voto": 0.0, "acesso": 0,
             "comentario": 0, "publicado_em": "04/12/2010 12:02",
             "url": "javascript:void(0)", "id_conteudo": "7",
             "meta_type": "foto", "titulo": "", "creators": []}
           """
            dafast = daFastXmlFileFoto(portal=self.dados["portal"],
                                       origem=self.dados["origem"])

            self._writer(dafast=dafast,
                         port=self.dados["portal"],
                         origem=self.dados["origem"],
                         path=self.dados["path"],
                         tipoconteudo="foto",
                         id_conteudo=id_conteudo,
                         delete=delete,
                         dados=dados,
                         id_treeapp=id_treeapp,
                         get=self._getFoto,
                         getdel=self._getFotoDelete)

            if not conf_sites:
                return

            for i in portal._getTreeShared(id_site=self.id_site,
                                           id_treeapp=id_treeapp):

                if i["id_site"] != int(self.id_site):

                    try:
                        url = portal.getUrlByApp(env_site=i["id_site"],
                                                 schema=schema,
                                                 id_conteudo=id_conteudo,
                                                 exportar=1,
                                                 id_treeapp=i["id_treeapp"],
                                                 id_site_compartilhar=self.id_site,
                                                 id_tree_compartilhar=id_treeapp,
                                                 admin=1)
                    except Exception, e:
                        url = "javascript:void(0)"

                    if not url.startswith("javascript:void(0)"):
                        dados["url"] = url
                        port, origem = conf_sites.get(i["id_site"], (None, None))
                        if port and origem:

                            dafast = daFastXmlFileFoto(portal=port,
                                                       origem=origem)

                            self._writer(dafast=dafast,
                                         port=port,
                                         origem=origem,
                                         path=self.dados["path"],
                                         tipoconteudo="foto",
                                         id_conteudo="%s_%s" % (self.dados["origem"], id_conteudo),
                                         delete=delete,
                                         dados=dados,
                                         id_treeapp=id_treeapp,
                                         get=self._getFoto,
                                         getdel=self._getFotoDelete)


        elif schema.find("noticia") >= 0:

            """
            {
            'id_conteudo': '279', 
            'atualizado_em': '2010-11-06 19:15', 
            'meta_type': 'noticia', 
            'publicado_em': '2010-10-20 18:23', 
            'dados': {'destaque': [{'titulo': '', 'img': '', 'descricao': ''}], 
                      'foto': [{'arquivo_grande': '', 'credito': '', 
                                'link': 'javascript:void(0)', 'legenda': '', 
                                'arquivo': '', 'alinhamento': 'left'}], 
                      'autor': [], 
                      'video': [{'embed': ''}], 
                      'tipo_noticia': 6, 
                      'corpo': '', 
                      'titulo_categoria': '', 
                      'has_galeria': False, 
                      'has_audio': False, 
                      'data_edicao': None, 
                      'has_video': False, 
                      'editor': True, 
                      'titulo': 'teste', 
                      'descricao': 'teste'}, 
            'expira_em': None, 
            'url': '', 
            'titulo': 'teste', 
            'creators': []}
            """

            dafast = daFastXmlFileNoticia(portal=self.dados["portal"],
                                          origem=self.dados["origem"],
                                          tipoconteudo="noticia")

            self._writer(dafast=dafast,
                         port=self.dados["portal"],
                         origem=self.dados["origem"],
                         path=self.dados["path"],
                         tipoconteudo="noticia",
                         id_conteudo=id_conteudo,
                         delete=delete,
                         dados=dados,
                         id_treeapp=id_treeapp, 
                         get=self._getNoticia,
                         getdel=self._getNoticiaDelete)

            if not conf_sites:
                return

            for i in portal._getTreeShared(id_site=self.id_site,
                                           id_treeapp=id_treeapp):

                if i["id_site"] != int(self.id_site):

                    try:
                        url = portal.getUrlByApp(env_site=i["id_site"],
                                                 schema=schema,
                                                 id_conteudo=id_conteudo,
                                                 exportar=1,
                                                 id_treeapp=i["id_treeapp"],
                                                 id_site_compartilhar=self.id_site,
                                                 id_tree_compartilhar=id_treeapp,
                                                 admin=1)
                    except Exception, e:
                        url = "javascript:void(0)"

                    if not url.startswith("javascript:void(0)"):
                        dados["url"] = url
                        port, origem = conf_sites.get(i["id_site"], (None, None))
                        if port and origem:

                            dafast = daFastXmlFileNoticia(portal=port,
                                                          origem=origem,
                                                          tipoconteudo="noticia")

                            self._writer(dafast=dafast,
                                         port=port,
                                         origem=origem,
                                         path=self.dados["path"],
                                         tipoconteudo="noticia",
                                         id_conteudo="%s_%s" % (self.dados["origem"], id_conteudo),
                                         delete=delete,
                                         dados=dados,
                                         id_treeapp=id_treeapp, 
                                         get=self._getNoticia,
                                         getdel=self._getNoticiaDelete)



    def _getFotoDelete(self, dafast, contentid):
        """
        """
        dafast.add(contentid=contentid,
                   titulogaleria=None,
                   descricaofoto=None,
                   descricaogaleria=None,
                   fontemidia=None,
                   dataexpiracao=None,
                   datainsercao=None,
                   datapublicacao=None,
                   dataranking=None,
                   secao=None,
                   autores=None,
                   tags=None,
                   statusinterno="1",
                   statusativacao="0",
                   statusmidiavisivel="1",
                   ranking=None,
                   qtdestrelas=None,
                   urldestino=None,
                   urlthumb=None,
                   urlautor=None)


    def _getFoto(self, dafast, contentid, dados, id_treeapp):
        """
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)

        folder = portal._getFoldersTreeApp(env_site=self.id_site,
                                           id_treeapp=id_treeapp)
        folder = "/".join(folder)

        tags = dados["dados"]["tags"]
        if tags:
            tags = tags.replace("\n", " ")
            tags = "#".join( [i for i in tags.split(" ") if i] )
        else:
            tags = ""

        autores = ""
        qtdestrelas = dados["nvoto"]
        qtdcomentarios = ""
        expira_em = dados["expira_em"]
        if expira_em:
            expira_em = expira_em + ":00"

        statusinterno = "1" # 
        statusativacao = "1" # 0: deletado,rascunho  - 1: no ar
        statusmidiavisivel = "1" # 

        for foto in dados["dados"]["foto"]:

            dafast.add(contentid=contentid,
                       titulogaleria=dados["dados"]["titulo"],
                       descricaofoto=foto["descricao"],
                       descricaogaleria=None,
                       fontemidia=None,
                       urldestino="%s#photo_%s" % (dados["url"], foto["ordem"]),
                       urlthumb=portal.retornarUrl(arquivo=foto["thumbnail"],
                                                   base=True),
                       dataexpiracao=expira_em,
                       datainsercao=strftime("%Y-%m-%d %H:%M:%S"),
                       datapublicacao="%s:00" % dados["publicado_em"],
                       dataranking=None,
                       secao=folder,
                       autores=autores,
                       tags=tags,
                       statusinterno=statusinterno,
                       statusativacao=statusativacao,
                       statusmidiavisivel=statusmidiavisivel,
                       ranking=None,
                       qtdestrelas=qtdestrelas,
                       urlautor=None)


    def _getNoticiaDelete(self, dafast, contentid):
        """
        """
        dafast.add(contentid=contentid,
                   dataexpiracao=None,
                   datainsercao=None,
                   datapublicacao=None,
                   dataranking=None,
                   secao=None,
                   autores=None,
                   corpoconteudo=None,
                   tags=None,
                   tagsrelacionadas=None,
                   statusinterno="1",
                   statusativacao="0",
                   statusmidiavisivel="1",
                   ranking=None,
                   qtdestrelas=None,
                   qtdcomentarios=None,
                   titulo=None,
                   categoria=None,
                   resumo=None,
                   urldestino=None,
                   urlthumb=None,
                   tituloblog=None,
                   idblog=None,
                   urlautor=None)


    def _getNoticia(self, dafast, contentid, dados, id_treeapp):
        """
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)

        folder = portal._getFoldersTreeApp(env_site=self.id_site,
                                           id_treeapp=id_treeapp)
        folder = "/".join(folder)

        tags = dados["dados"]["tags"]
        if tags:
            tags = tags.replace("\n", " ")
            tags = "#".join( [i for i in tags.split(" ") if i] )
        else:
            tags = ""

        autores = "#".join([i["nome"] for i in dados["dados"]["autor"]])
        qtdestrelas = dados["nvoto"]
        qtdcomentarios = ""
        expira_em = dados["expira_em"]
        if expira_em:
            expira_em = expira_em + ":00"

        statusinterno = "1" # 
        statusativacao = "1" # 0: deletado,rascunho  - 1: no ar
        statusmidiavisivel = "1" # 

        dafast.add(contentid=contentid,
                   dataexpiracao=expira_em,
                   datainsercao=strftime("%Y-%m-%d %H:%M:%S"),
                   datapublicacao="%s:00" % dados["publicado_em"],
                   dataranking=None,
                   secao=folder,
                   autores=autores,
                   corpoconteudo=dados["dados"]["corpo"],
                   tags=tags,
                   tagsrelacionadas=None,
                   statusinterno=statusinterno,
                   statusativacao=statusativacao,
                   statusmidiavisivel=statusmidiavisivel,
                   ranking=None,
                   qtdestrelas=qtdestrelas,
                   qtdcomentarios=qtdcomentarios,
                   titulo=dados["titulo"],
                   categoria=dados["dados"]["titulo_categoria"],
                   resumo=dados["dados"]["descricao"],
                   urldestino=dados["url"],
                   urlthumb=None,
                   tituloblog=None,
                   idblog=None,
                   urlautor=None)


    def _writer(self, dafast, port, origem, path,
                      tipoconteudo, id_conteudo, delete,
                      dados, id_treeapp, get, getdel):
        """
        """
        contentid = ("%s_%s_%s_%s" % (port,
                                      origem,
                                      tipoconteudo,
                                      id_conteudo)).lower()

        if delete:
            getdel(dafast, contentid)
        else:
            get(dafast,
                contentid,
                dados,
                id_treeapp)

        path = "%s%s_%s.xml" % (path, contentid, random())
        pathtmp = "%s%s.tmp" % (path, contentid)
        dafast.write(pathtmp, comments=True)
        rename(pathtmp, path)


