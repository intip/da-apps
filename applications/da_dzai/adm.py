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
import urllib2
import xml.etree.ElementTree as ET
from os import rename
from time import time, strftime, strptime
from publica.core.portal import Portal
from publica.admin.error import UserError
from publica.utils.decorators import serialize, dbconnectionapp, \
                                     Permission, permissioncron, logportal
from publica import settings
from fast.daFastXmlFileVideo import daFastXmlFileVideo


class Adm(object):
    """
      Administrative methods
    """


    def _writeFast(self, id_conteudo, path, portal, origem,
                         titulo, descricao, tags, url, thumb):
        """
           Write an file with video's information to Fast
        """

        dafast = daFastXmlFileVideo(portal=portal,
                                    origem=origem)

        contentid = ("%s_%s_video_%s" % (portal,
                                         origem,
                                         id_conteudo)).lower()

        if tags:
            tags = tags.replace("\n", " ")
            tags = "#".join( [i for i in tags.split(" ") if i] )
        else:
            tags = ""

        statusinterno = "1" # 
        statusativacao = "1" # 0: deletado,rascunho  - 1: no ar
        statusmidiavisivel = "1" # 

        dafast.add(contentid=contentid,
                   dataexpiracao=None,
                   datainsercao=strftime("%Y-%m-%d %H:%M:%S"),
                   datapublicacao=strftime("%Y-%m-%d %H:%M:%S"),
                   dataranking=None,
                   secao=None,
                   autores=None,
                   tempoduracao=None,
                   fontemidia=None,
                   titulovideo=titulo,
                   descricaovideo=descricao,
                   statusinterno=statusinterno,
                   statusativacao=statusativacao,
                   statusmidiavisivel=statusmidiavisivel,
                   ranking=None,
                   qtdestrelas=0,
                   urldestino=url,
                   urlthumb=thumb,
                   urlautor=None,
                   tags=tags)

        path_ = "%s%s.xml" % (path, contentid)
        pathtmp = "%s%s.tmp" % (path, contentid)
        dafast.write(pathtmp, comments=True)
        rename(pathtmp, path_)

    @dbconnectionapp
    def _getConteudo(self, id_conteudo):
        """
            get data of content
        """
        for i in self.execSql("select_conteudo_id",
                               id_conteudo=int(id_conteudo)):
            return i        

    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def editConteudo(self, id_conteudo, sea_id, id_aplicativo,
                      id_treeapp,  titulo,
                      descricao, embed, thumb, publicado_em=None,
                      expira_em=None, publicado=None,
                      titulo_destaque=None, descricao_destaque=None,
                      imagem_destaque=None, peso_destaque=None,
                      relacionamento=[], tags="", permissao=None,
                      exportar_xml=None, exportar_json=None, atualizado_em=None,
                      data_edicao=None, exportado=False, exportar=None):
        """
            edit data of content
        """
        portal = Portal(id_site=self.id_site, request=self.request)
        publicado = True if publicado else False
        tags = tags if tags else None 
        dt = publicado_em
        try:
            p = strptime(publicado_em, "%d/%m/%Y %H:%M")
            publicado_em = strftime("%Y-%m-%d %H:%M", p)
        except ValueError, e:
            raise UserError(("Ocorreu um erro: "
                             "Data de publica&ccedil;&aring;o "
                             "inv&aacute;lida (%s)") % publicado_em)

        try:
            p = strptime(expira_em, "%d/%m/%Y %H:%M")
            expira_em = strftime("%Y-%m-%d %H:%M", p)
        except ValueError, e:
            expira_em = None      
        if "http://" in thumb:
            id_imagem = thumb
        else:
            id_imagem = portal.addArquivo(arquivo=thumb,
                                          id_conteudo=id_conteudo,
                                          schema=self.schema,
                                          dt=dt)
        ta=tags
        # deletar conteudo tabela destaques ou outras tabelas
        self.execSqlBatch("delete_destaque",
                          id_conteudo=int(id_conteudo))
        self.execSqlBatch("update_conteudo",
                           id_conteudo = int(id_conteudo),
                           titulo= titulo,
                           descricao= descricao,
                           sea_id = sea_id,
                           embed = embed,
                           thumb = id_imagem,
                           tags = tags.replace("\n"," "),
                           publicado = publicado,
                           expira_em = expira_em,
                           publicado_em = publicado_em,
                           atualizado_em = atualizado_em,
                           data_edicao = data_edicao,
                           exportado = exportado)

        dados_destaque = []
        if titulo_destaque or imagem_destaque or descricao_destaque:
            if not imagem_destaque:
                imagem_destaque = None 
            elif "http://" in imagem_destaque:
                imagem_desq = imagem_destaque
            elif "http://" not in imagem_destaque:
                imagem_destaque = self._addFile(arquivo=imagem_destaque,
                                                id_conteudo=id_conteudo,
                                                schema=self.schema,
                                                dt=dt)
            try:
                peso_destaque = int(peso_destaque)
            except:
                peso_destaque = 0

            self.execSqlBatch("insert_destaque", 
                              id_conteudo=int(id_conteudo),
                              titulo=titulo_destaque,
                              descricao=descricao_destaque,
                              img=imagem_destaque,
                              peso=peso_destaque)
        self.execSqlCommit()
        # acoes para o portal
        dados = self._setDados(id_conteudo=id_conteudo)
        portal._editConteudoPortal(id_site=self.id_site,
                                id_conteudo=id_conteudo,
                                id_aplicativo=int(id_aplicativo),
                                schema=self.schema,
                                id_treeapp=id_treeapp,
                                peso=peso_destaque,
                                titulo=titulo,
                                publicado=publicado,
                                publicado_em=publicado_em,
                                expira_em=expira_em,
                                titulo_destaque=titulo_destaque,
                                descricao_destaque=descricao_destaque,
                                imagem_destaque=imagem_destaque,
                                tags=ta,
                                permissao=permissao,
                                relacionamento=relacionamento,
                                dados=dados)

        if (exportar_xml=='1') or (exportar_json=='1') or (exportar=='1'):
            self._addLog("Conteudo '%s' editado e publicado" % titulo)
            self._exportContent(id_aplicativo=id_aplicativo,
                                id_conteudo=id_conteudo,
                                schema=self.schema,
                                id_treeapp=id_treeapp,
                                html=exportar,
                                xml=exportar_xml,
                                json=exportar_json,
                                dados=dados,
                                subitems=None,
                                add=1)

            return ("Conteudo editado com sucesso! "
                    "Publica&ccedil;&atilde;o iniciada.")

        self._addLog("Conteudo editado '%s'" % titulo)
        return "Conteudo editado com sucesso."
           
    
    @dbconnectionapp
    def _addVideo(self, id_conteudo, titulo, sea_id, descricao, embed,
                        thumb, tags, fast_path, fast_portal, fast_origem,
                        id_pagina, id_treeapp, exists=None):
        """
        """
        tags = tags.encode('latin1', "xmlcharrefreplace")
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        publicado_em = strftime("%Y-%m-%d %H:%M")
        self.execSqlu("insert_videos",
                      id_conteudo=id_conteudo,
                      titulo=titulo,
                      sea_id=int(sea_id),
                      publicado_em=publicado_em,
                      descricao=descricao,
                      embed=embed,
                      thumb=thumb,
                      tags=tags)
        self.execSqlu("insert_destaque", 
                          id_conteudo=int(id_conteudo),
                          titulo=titulo,
                          descricao=descricao,
                          img=thumb,
                          peso=None)
        permissao = {"data":None,   
                     "exclusiva":None,    
                     "livre":1}
        dados = {"titulo":titulo,
                 "meta_type":self.meta_type,
                 "id_conteudo":id_conteudo,
                 "publicado_em":publicado_em,
                 "expira_em":None,
                 "atualizado_em":None,
                 "url":None,
                 "creators":[],
                 "dados":{"titulo":titulo,
                          "sea_id":sea_id,
                          "descricao":descricao,
                          "embed":embed,
                          "thumb":thumb,
                          "tags":tags}
                 } 

        self._addContentPortal(env_site=self.id_site,
                               id_pk=id_conteudo,
                               schema=self.schema,
                               meta_type=self.meta_type,
                               id_treeapp=id_treeapp,
                               peso=0,
                               titulo=titulo,
                               publicado=True,
                               publicado_em=publicado_em,
                               expira_em=None,
                               titulo_destaque=titulo,
                               descricao_destaque=descricao,
                               imagem_destaque=thumb,
                               tags=tags,
                               permissao=permissao,
                               relacionamento=[],
                               dados=dados)
        portal._exportarFormatosConteudo(id_aplicativo=None,
                                          id_conteudo=id_conteudo,
                                          schema=self.schema,
                                          id_treeapp=None,
                                          html=1,
                                          xml=None,
                                          json=None,
                                          dados=dados,
                                          subitems=None,
                                          add=1)

        if fast_path:

            if id_pagina:
                url = portal.getUrlByPagina(id_pagina=id_pagina,
                                            exportar=1,
                                            adm=1)
                url = "%s#video_%s" % (url, sea_id)
            else:
                url = ""

            self._writeFast(id_conteudo=sea_id,
                            path=fast_path,
                            portal=fast_portal,
                            origem=fast_origem,
                            titulo=titulo,
                            descricao=descricao,
                            tags=tags,
                            url=url,
                            thumb=thumb)


    @dbconnectionapp
    def _updateVideos(self):
        """
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        dados = portal._getApp(env_site=self.id_site,
                               schema=self.schema)["dados"]

        h = dados.get("hash", "")
        dados_h = portal._getTreeAppByHash(env_site=self.id_site,
                                           hash=h)
        if not dados_h:
            raise UserError(("Para atualizar o aplicativo da_dzai &eacute; "
                             "necess&aacute;rio que o mesmo tenha um "
                             "hash v&aacute;lido. id_site: %s") % self.id_site)

        hasupdate = False
        items = []

        for id_usuario in dados["id_usuario"].split("\n"):
            limit = 50
            offset = 0
            xml = urllib2.urlopen("%s?idusuario=%s&limit=%s&offset=%s" 
                                    % (dados["url"], id_usuario, limit, offset))
            EL = ET.fromstring(xml.read())
            total = int(EL.attrib["totalregistros"])
            for el in EL.findall(".//row"):
                descricao = el.findtext("./sea_descricao").encode("latin1")
                sea_id = el.findtext("./sea_id")
                embed = el.findtext("./sea_embed")
                tags = el.findtext("./sea_tags")
                thumb = el.findtext("./sea_thumb")
                titulo = el.findtext("./sea_titulo").encode("latin1")
                hasupdate = True

                id_conteudo = None
                exists = False
                for i in self.execSql("select_sea",
                                      sea_id=int(sea_id)):
                    id_conteudo = i["id_conteudo"]
                    exists = True
                if not id_conteudo:
                    id_conteudo = self.execSql(
                            "select_nextval_conteudo").next()["id"]
                if not exists:
                    self._addVideo(id_conteudo=id_conteudo,
                                   titulo=titulo,
                                   sea_id=int(sea_id),
                                   descricao=descricao,
                                   embed=embed,
                                   thumb=thumb,
                                   tags=tags,
                                   exists=exists,
                                   fast_path=dados.get("fast_path"),
                                   fast_portal=dados.get("fast_portal"),
                                   fast_origem=dados.get("fast_origem"),
                                   id_pagina=dados.get("id_pagina"),
                                   id_treeapp=dados_h["id_treeapp"])

        if dados.get("hash"):
            portal._exportarAppSubOne(env_site=self.id_site,
                                      hash=dados["hash"])
        return "ok"


    @dbconnectionapp
    def _fastVideos(self):
        """
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        dados = portal._getApp(env_site=self.id_site,
                               schema=self.schema)["dados"]

        h = dados.get("hash", "")
        dados_h = portal._getTreeAppByHash(env_site=self.id_site,
                                           hash=h)
        if not dados_h:
            raise UserError(("Para atualizar o aplicativo da_dzai &eacute; "
                             "necess&aacute;rio que o mesmo tenha um "
                             "hash v&aacute;lido. id_site: %s") % self.id_site)

        hasupdate = False
        items = []

        for i in self.execSql("select_conteudo"):


            sea_id = i["sea_id"]
            id_pagina = dados.get("id_pagina")
            if id_pagina:
                url = portal.getUrlByPagina(id_pagina=id_pagina,
                                            exportar=1,
                                            adm=1)
                url = "%s#video_%s" % (url, sea_id)
            else:
                url = ""

            self._writeFast(id_conteudo=i["sea_id"],
                            path=dados.get("fast_path"),
                            portal=dados.get("fast_portal"),
                            origem=dados.get("fast_origem"),
                            titulo=i["titulo"],
                            descricao=i["descricao"],
                            tags=i["tags"],
                            url=url,
                            thumb=i["thumb"])

        return "ok"

    @dbconnectionapp
    def _getTotalVideos(self):
        """
          returns total videos
        """
        count = list(self.execSql("select_count_videos"))[0]['qtde']
        return count

    @serialize
    @logportal
    @Permission("PERM APP")
    def updateVideosAdm(self):
        """
        """
        self._updateVideos()
        self.logmsg = ("V&iacute;deos dzai '%s' "
                       "atualizados, site: %s.")  % (self.schema,
                                                     self.id_site)
        return "V&iacute;deos carregados com sucesso!"


    @serialize
    @logportal
    @Permission("PERM APP")
    def fastVideosAdm(self):
        """
        """
        self._fastVideos()
        self.logmsg = ("Xml dzai '%s' "
                       "atualizados, site: %s.")  % (self.schema,
                                                     self.id_site)
        return "Xml criado com sucesso!"


    @serialize
    @logportal
    @permissioncron
    def updateVideos(self):
        """
            public call to download videos from dzai
        """
        self._updateVideos()
        self.logmsg = ("V&iacute;deos dzai '%s' "
                       "atualizados, site: %s.")  % (self.schema,
                                                     self.id_site)
        return "ok"
