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
import re
from random import randint
from os.path import join
from os import walk, remove
from time import time, strftime, strptime
from xml.etree import ElementTree as ET
from publica.core.portal import Portal
from publica.admin.error import UserError
from publica.utils.json import encode
from publica.utils.log import Log
from publica.utils.decorators import serialize, dbconnectionapp,\
                                     Permission, permissioncron, logportal
try:
    from publica.db.datagateway import DataGateway
except ImportError:
    # not in version 1.1.5
    DataGateway = None

from publica.admin.exchange import getDadosSite
from publica import settings

hasapp = False
haspage = False
haslist = True
hasportlet = False
title = "DA - Impresso"
meta_type = "da_impresso"
ID_FIM = "EFI{0}{1}P0001.FIM"
XML_ENCODING = "ISO-8859-1"


def CDATA(text=None):
    element = ET.Element(CDATA)
    element.text = text
    return element


class ElementTreeCDATA(ET.ElementTree):
    def _write(self, file, node, encoding, namespaces):
        if node.tag is CDATA:
            text = node.text.encode(encoding)
            file.write("<![CDATA[%s]]>" % text)
        else:
            ET.ElementTree._write(self, file, node, encoding, namespaces)


class Plug(object):
    """
        This plugin create the xml from the content impresso
    """
    title = title
    meta_type = meta_type
    hasapp = hasapp
    haspage = haspage
    haslist = haslist
    hasportlet = hasportlet


    def __init__(self, id_site, id_plugin=None, request=None, dados={}):
        """
        """
        self.id_plugin = id_plugin
        self.id_site = id_site
        self.request = request
        self.dados = dados
        self._l = None

        if id_plugin and not dados:
            portal = Portal(id_site, {})
            plug = portal._getPlug(env_site=id_site,
                                   id_plugin=int(id_plugin))
            self.dados = plug["dados"] 


    def _install(self, title, path, path_vejatambem, path_log, schema, id_fim):
        """
            Install the plugin instance
        """
        return {"titulo":title,
                "path":path,
                "path_vejatambem":path_vejatambem,
                "path_log":path_log,
                "schema":schema,
                "id_fim":id_fim}


    @property
    def _log(self):
        """
            Returns the data from log file
        """
        try:
            fl = open(self.dados["path_log"])
        except Exception,e:
            return ("Could not open the log file "
                    "{0}: {1}").format(self.dados["path_log"], str(e))
        return fl.read()

    @_log.setter
    def _log(self, value):
        """
            Add the new text log in the file
        """
        if not self._l:
            self._l = Log(filename=self.dados["path_log"],
                          name="DA Impresso")
        self._l.info(value)


    def _getId_content(self, id_site, id_conteudo, schema):
        """
            Returns the global id of the content
        """
        if DataGateway:
            db = DataGateway()
            return db._DataGateway__getId_content(id_site=id_site,
                                                 id_conteudo=id_conteudo,
                                                 schema=schema)
        else:
            portal = Portal(id_site, {})
            return portal._getIdContent(id_site=id_site,
                                        id_conteudo=id_conteudo,
                                        schema=schema)


    @serialize
    @Permission("ADM PLUG")
    def editPlug(self, title, path, path_vejatambem, path_log, schema, id_fim):
        """
            Edit the plugin attributes
        """
        dados = {"titulo":title,
                 "path":path,
                 "path_vejatambem":path_vejatambem,
                 "path_log":path_log,
                 "schema":schema,
                 "id_fim":id_fim}
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        portal._editPlug(env_site=self.id_site,
                         id_plugin=self.id_plugin, 
                         title=title, 
                         dados=dados)
        return "Plugin configurado com sucesso"


    def _now(self):
        """
            return current timestamp
        """
        return strftime("%d/%m/%Y %H:%M:%S")

       
    def _clean(self):
        """
            clean the folders before write
        """
        path = self.dados["path"]
        for w in walk(path):
            for i in w[2]:
                path_ = join(path, i)
                remove(path_)
            break

        # should clean this one too?
        #path = self.dados["path_vejatambem"]
        #for w in walk(path):
        #    for i in w[2]:
        #        path_ = join(path, i)
        #        remove(path_)
        #    break


    def _cleanBody(self, text):
        """
            removes the [FOTO01], [VIDEO02], etc from the text
        """
        r = re.compile("\[[A-Z0-9]*?\]")
        return r.sub("", text)


    def _getImpresso(self, data=None, capa=None, id_fim=None, 
                           id_site=None, schema=None, id_conteudo=None,
                           saibamais=[]):
        """
            Get the list of impresso content (da_impresso) and format the
            data to xml parser
        """
        portal = Portal(self.id_site, {})
        if not id_site or not schema:
            id_site, schema = self.dados["schema"].split(",")
        app = portal._getAplication(id_site=id_site,
                                    meta_type="da_impresso",
                                    schema=schema)
        enc = settings.GLOBAL_ENCODING
        id_pdf = None
        docs = []

        for i in app.getContentDate(date=data, capa=capa, id_conteudo=id_conteudo):

            data = app._setDados(i["id_conteudo"])
            id_content = self._getId_content(id_site=id_site,
                                             id_conteudo=i["id_conteudo"],
                                             schema=schema)

            if capa:
                titulo = data["dados"]["titulo_capa"]
            else:
                titulo = data["titulo"]
            src = {"document": {
                                "docname": unicode(id_fim if capa else data["dados"]["pdf"], enc),
                                "id_content": str(id_content),
                                "Titulo": unicode(titulo, enc),
                                "Bigode": unicode(data["dados"]["descricao"], enc),
                                "Autor": unicode(" e ".join(data["creators"]), enc),
                                "Titulo_galeria": unicode("" if not data["dados"]["titulo_galeria"] else data["dados"]["titulo_galeria"], enc),
                                "Paragrafo": unicode(data["dados"]["corpo"], enc),
                                "ordem": str(data["dados"]["ordem"]),
                  },
                   "images":[],
                   "videos":[],
                   "correlata":[],
                   "vejatambem":[],
                   "saibamais":[],
                  }

            dest = None
            for img in data["dados"]["foto"]:
                if not img["arquivo_grande"]:
                    continue
                img_ = {"Imagem": unicode(portal.retornarUrl(img["arquivo_grande"]), enc),
                        "Autor": unicode(img["credito"], enc),
                        "Legenda": unicode(img["legenda"], enc),
                        "destaque": True if not dest else False}
                dest = 1
                src["images"].append(img_)

            for img in data["dados"]["fotos_ipad"]:
                if not img["arquivo"]:
                    continue
                img_ = {"Imagem": unicode(portal.retornarUrl(img["arquivo"]), enc),
                        "Autor": unicode(img["credito"], enc),
                        "Legenda": unicode(img["legenda"], enc),
                        "destaque": False}
                src["images"].append(img_)


            for video in data["dados"]["videos_ipad"]:
                if video["link"] or video["thumb"] or video["nome"]:
                    video_ = {"Video": unicode(video["link"], enc),
                              "thumb": unicode(video["thumb"], enc),
                              "Titulo": unicode(video["nome"], enc)}
                    src["videos"].append(video_)

            # correlata
            for r in portal._getRelacionamentoConteudo(id_site=id_site,
                                                       schema=schema,
                                                       id_conteudo=i["id_conteudo"],
                                                       level=None):
                if r["meta_type"] == "da_impresso":
                    src["correlata"].append(r["id_content"])
                elif r["meta_type"] == "noticia":

                    app_ = portal._getAplication(id_site=r["id_site"],
                                                 meta_type="noticia",
                                                 schema=r["schema"])
                    dados_ = app_._setDados(r["id_pk"])["dados"]
                    imagens = []
                    for i in dados_["foto"]:
                        if i["arquivo"]:
                            imagens.append({"arquivo": unicode(portal.retornarUrl(i["arquivo"]), enc),
                                            "autor": unicode(i["credito"], enc),
                                            "legenda": unicode(i["legenda"], enc)})

                    autor = " e ".join(i["nome"] for i in dados_["autor"] )

                    src["vejatambem"].append( {"id_content":str(r["id_content"]),
                                               "titulo": unicode(dados_["titulo"], enc),
                                               "bigode": unicode(dados_["descricao"], enc),
                                               "autor": unicode(autor, enc),
                                               "corpo": unicode(self._cleanBody(dados_["corpo"]), enc),
                                               "imagens":imagens} )


            for s in saibamais:
                app_ = portal._getAplication(id_site=s["id_site"],
                                             meta_type="noticia",
                                             schema=s["schema"])
                dados_ = app_._setDados(s["id_conteudo"])["dados"]
                imagens = []
                for i in dados_["foto"]:
                    if i["arquivo"]:
                        imagens.append({"arquivo": unicode(portal.retornarUrl(i["arquivo"]), enc),
                                        "autor": unicode(i["credito"], enc),
                                        "legenda": unicode(i["legenda"], enc)})

                autor = " e ".join(i["nome"] for i in dados_["autor"] )
                id_content = self._getId_content(id_site=s["id_site"],
                                                 id_conteudo=s["id_conteudo"],
                                                 schema=s["schema"])

                src["saibamais"].append( {"id_content":str(id_content),
                                          "titulo": unicode(dados_["titulo"], enc),
                                          "bigode": unicode(dados_["descricao"], enc),
                                          "autor": unicode(autor, enc),
                                          "corpo": unicode(dados_["corpo"], enc),
                                          "images":imagens} )


            if id_pdf is None or id_pdf == unicode(data["dados"]["pdf"], enc) or capa:
                docs.append(src)
            else:
                yield id_pdf, docs
                docs = [src]

            id_pdf = unicode(data["dados"]["pdf"], enc)

        yield id_pdf, docs


    def _createXml(self, dados):
        """
        Create the xml source 

        Example of xml:

            <?xml version="1.0" encoding="ISO-8859-1" ?>
            <Pagina docname="EVE2505P0005">
                <Document docname="181660">
                    <Content>
                        <Titulo><![CDATA[ data ]]></Titulo>
                        <Bigode><![CDATA[ data ]]></Bigode>
                        <Autor><![CDATA[ data ]]></Autor>
                        <Titulo_galeria><![CDATA[ data ]]></Titulo_galeria>
                        <Materia>
                            <Paragrafo ordem="1"><![CDATA[ data ]]></Paragrafo>
                        </Materia>
                        <Imagens>
                            <Imagem publicada="true" destaque="true" link="http://.jpg" />
                                <Autor><![CDATA[ data ]]></Autor>
                                <Legenda><![CDATA[ data ]]></Legenda>
                            </Imagem>
                        </Imagens>
                        <Videos>
                            <Video link="http://.mp4" yhumb="http://.jpg">
                                <Titulo><![CDATA[ data ]]></Titulo>
                            </Video>
                        </Videos>
                        <Correlatas>
                            <Correlata docname="181664"></Correlata>
                            <Correlata docname="181663"></Correlata>
                        </Correlatas>
                    </Content>
                </Document>
            </Pagina>
        """
        if not dados:
            return None

        id_pdf = None
        root = ET.Element("Pagina")

        for doc in dados:

            if not id_pdf:
                id_pdf = doc["document"]["docname"]
                root.attrib["docname"] = id_pdf

            document = ET.SubElement(root, "Document")
            document.attrib["docname"] = doc["document"]["id_content"]
            content = ET.SubElement(document, "Content")

            titulo = ET.SubElement(content, "Titulo")
            titulo.append(CDATA(doc["document"]["Titulo"]))

            bigode = ET.SubElement(content, "Bigode")
            bigode.append(CDATA(doc["document"]["Bigode"]))

            if doc["document"]["Autor"]:
                autor = ET.SubElement(content, "Autor")
                autor.append(CDATA(doc["document"]["Autor"]))

            if doc["document"]["Titulo_galeria"]:
                titulo_galeria = ET.SubElement(content, "Titulo_galeria")
                titulo_galeria.append(CDATA(doc["document"]["Titulo_galeria"]))

            materia = ET.SubElement(content, "Materia")
            paragrafo = ET.SubElement(materia, "Paragrafo")
            paragrafo.attrib["ordem"] = "1" #doc["document"]["ordem"]
            paragrafo.append(CDATA(self._cleanBody(doc["document"]["Paragrafo"])))

            # <Pagina><Document><Content><Imagens>
            if doc["images"]:

                imagens = ET.SubElement(content, "Imagens")
                for i in doc["images"]:

                    imagem = ET.SubElement(imagens, "Imagem")
                    imagem.attrib["publicada"] = "true"
                    imagem.attrib["destaque"] = "true" if i["destaque"] else "false"
                    imagem.attrib["link"] = i["Imagem"]

                    autor = ET.SubElement(imagem, "Autor")
                    autor.append(CDATA(i["Autor"]))
                    legenda = ET.SubElement(imagem, "Legenda")
                    legenda.append(CDATA(i["Legenda"]))

            # <Pagina><Document><Content><Imagens>
            if doc["videos"]:

                videos = ET.SubElement(content, "Videos")
                for i in doc["videos"]:

                    video = ET.SubElement(videos, "Video")
                    video.attrib["link"] = i["Video"]
                    video.attrib["thumb"] = i["thumb"]

                    titulo =  ET.SubElement(video, "Titulo")
                    titulo.append(CDATA(i["Titulo"]))

            # <Pagina><Document><Content><Correlatas>
            if doc["correlata"]:

                correlatas = ET.SubElement(content, "Correlatas")
                for i in doc["correlata"]:
                    correlata = ET.SubElement(correlatas, "Correlata")
                    correlata.attrib["docname"] = str(i)

            # <Pagina><Document><Content><VejaTambem>
            if doc["vejatambem"]:

                vejatambem = ET.SubElement(content, "VejaTambem")
                contents = ET.SubElement(vejatambem, "Contents")

                for vj in doc["vejatambem"]:

                    content = ET.SubElement(contents, "Content")
                    content.attrib["id"] = str(vj["id_content"])

                    titulo = ET.SubElement(content, "Titulo")
                    titulo.append(CDATA(vj["titulo"]))

                    if vj["bigode"]:        
                        bigode = ET.SubElement(content, "Bigode")
                        bigode.append(CDATA(vj["bigode"]))

                    if vj["autor"]:
                        autor = ET.SubElement(content, "Autor")
                        autor.append(CDATA(vj["autor"]))

                    materia = ET.SubElement(content, "Materia")
                    paragrafo = ET.SubElement(materia, "Paragrafo")
                    paragrafo.attrib["ordem"] = "1"
                    paragrafo.append(CDATA(vj["corpo"]))

                    if vj["imagens"]:

                        Imagens = ET.SubElement(content, "Imagens")
                        for im in vj["imagens"]:

                            imagem = ET.SubElement(Imagens, "Imagem")
                            imagem.attrib["publicada"] = "true"
                            imagem.attrib["destaque"] = "true"
                            imagem.attrib["link"] = im["arquivo"]
                        
                            autor = ET.SubElement(imagem, "Autor")
                            autor.append(CDATA(im["autor"]))

                            legenda = ET.SubElement(imagem, "Legenda")
                            legenda.append(CDATA(im["legenda"]))

        return root


    def _createXmls(self, dados):
        """
        Create the xml source for saibamais 

        Example of xml:

        <?xml version="1.0" encoding="ISO-8859-1" ?>
        <SaibaMais>
            <Contents>
                <Content id="1">
                    <Titulo><![CDATA[A cura pode vir do dente Veja Também]]></Titulo>
                    <Bigode><![CDATA[]]></Bigode>
                    <Autor><![CDATA[Márcia Maria Cruz]]></Autor>
                    <Materia>
                        <Paragrafo ordem="1"><![CDATA[ ... ]]></Paragrafo>
                    </Materia>
                    <Imagens>
                        <Imagem publicada="true" destaque="true" link="http://ipad.jpg">
                            <Autor><![CDATA[Marcos Vieira/EM/D.A Press]]></Autor>
                            <Legenda><![CDATA[]]></Legenda>
                        </Imagem>
                   </Imagens>
                </Content>
                <Content id="2">
                    <Titulo><![CDATA[A cura pode vir do dente Veja Também2]]></Titulo>
                    <Bigode><![CDATA[]]></Bigode>
                    <Autor><![CDATA[Márcia Maria Cruz]]></Autor>
                    <Materia>
                        <Paragrafo ordem="1"><![CDATA[ ...  ]]></Paragrafo>
                    </Materia>
                    <Imagens>
                        <Imagem publicada="true" destaque="true" link="http://ipad.jpg">
                            <Autor><![CDATA[Marcos Vieira/EM/D.A Press]]></Autor>
                            <Legenda><![]]></Legenda>
                        </Imagem>
                    </Imagens>
                </Content>
            </Contents>
        </SaibaMais>

        """
        if not dados:
            return None

        id_pdf = None
        root = ET.Element("SaibaMais")
        contents = ET.SubElement(root, "Contents")
        id_content_im = None

        for doc in dados:

            id_content_im = doc['document']['id_content']

            for sb in doc["saibamais"]:

                content = ET.SubElement(contents, "Content")
                content.attrib["id"] = str(id_content_im) #str(sb["id_content"])

                titulo = ET.SubElement(content, "Titulo")
                titulo.append(CDATA(sb["titulo"]))

                if sb["bigode"]:
                    bigode = ET.SubElement(content, "Bigode")
                    bigode.append(CDATA(sb["bigode"]))

                if sb["autor"]:
                    autor = ET.SubElement(content, "Autor")
                    autor.append(CDATA(sb["autor"]))

                materia = ET.SubElement(content, "Materia")
                paragrafo = ET.SubElement(materia, "Paragrafo")
                paragrafo.attrib["ordem"] = "1"
                paragrafo.append(CDATA(self._cleanBody(sb["corpo"])))

                # <Pagina><Document><Content><Imagens>

                destaque = False
                if sb["images"]:

                    imagens = ET.SubElement(content, "Imagens")
                    for i in sb["images"]:

                        if i["arquivo"]:

                            imagem = ET.SubElement(imagens, "Imagem")
                            imagem.attrib["publicada"] = "true"
                            imagem.attrib["link"] = i["arquivo"]

                            if i["autor"]:
                                autor = ET.SubElement(imagem, "Autor")
                                autor.append(CDATA(i["autor"]))
                            if i["legenda"]:
                                legenda = ET.SubElement(imagem, "Legenda")
                                legenda.append(CDATA(i["legenda"]))

                            if not destaque:
                                destaque = True
                                imagem.attrib["destaque"] = "true"
                            else:
                                imagem.attrib["destaque"] = "false"

        ##contents.attrib["id"] = id_content_im
        return root


    def _writeXml(self, source, id_xml, saibamais=None):
        """
            Write the xml source at the configured path
        """
        if saibamais:
            path = join(self.dados["path_vejatambem"], id_xml)
        else:
            path = join(self.dados["path"], id_xml)
        ElementTreeCDATA(source).write(path, encoding=XML_ENCODING)


    def _action(self, id_treeapp, schema, id_conteudo, link,
                      add=None, edit=None, delete=None, dados={}, **kargs):
        """
            This plugin has not action on content
        """
        pass


    def _routine(self, id_treeapp, schema, id_conteudo, link,
                       add=None, edit=None, delete=None, dados={}, **kargs):
        """
            Call the methods to generate the xml:
                * xml of all data on specific date
                * xml only of the capa attribute
        """
        self._clean()
        errs = False
        data = kargs.get("data", None)
        if not data:
            data = strftime("%d/%m/%Y")

        self._log = ("Begin the routine of impresso - "
                "date: {0} ").format(data)

        for id_pdf, i in self._getImpresso(data=data):

            try:
                xml = self._createXml(i)
                if not xml:
                    continue
                id_xml = "{0}.xml".format(id_pdf.upper())
                self._writeXml(source=xml,
                               id_xml=id_xml)
                self._log = "Exported {0}".format(id_xml)
            except Exception, e:
                errs = True
                self._log = "Error {0} - {1}".format(str(i), str(e))


        self._log = "End the routine of impresso"
        self._log = "Begin the routine of impresso capa"

        # capas
        dt_ = strptime(data, "%d/%m/%Y")
        if self.dados.get("id_fim"):
            id_xml_ = self.dados["id_fim"] % {"DAY":strftime("%d", dt_),
                                              "MONTH":strftime("%m", dt_),
                                              "YEAR":strftime("%Y", dt_)}
        else:
            id_xml_ = ID_FIM.format(strftime("%d", dt_), strftime("%m", dt_))
        for id_xml, i in self._getImpresso(data=data, capa=1, id_fim=id_xml_):

            try:
                xml = self._createXml(i)
                if not xml:
                    continue

                self._writeXml(source=xml,
                               id_xml=id_xml_)
                self._log = "Exported {0}".format(id_xml_)
            except Exception, e:
                errs = True
                self._log = "Error {0} - {1}".format(str(i), str(e))

        self._log = "Ended routine impresso capa"
        self.editPlug(title=unicode(self.dados["titulo"]).encode("iso-8859-1"),
                      path=self.dados["path"],
                      path_vejatambem=self.dados["path_vejatambem"],
                      path_log=self.dados["path_log"],
                      schema=self.dados["schema"])
                        
        return errs


    @serialize
    @permissioncron
    def doExport(self, data=None):
        """
            Exec the export routine from crontab job
        """
        if not self._routine(None, None, None, None, data=data):
            return "Exporta&ccedil;&atilde;o efetuada com sucesso!"
        else:
            return ("Exporta&ccedil;&atilde;o efetuada, mas acontenceu alguns "
                    "erros, verifique o log para mais informa&ccedil;&otilde;es")


    @serialize
    @Permission("ADM PLUG")
    def doExportAdm(self, data=None):
        """
            Exec the export routine from admin form
        """
        self._routine(None, None, None, None, data=data)
        return "Exporta&ccedil;&atilde;o efetuada com sucesso!"
     

    @serialize
    @Permission("ADM PLUG")
    def actionWidget(self, **kargs):
        """
        """
        if kargs.get("meta_type", "") == "noticia":

            return {"open":("/plug/da_impresso/getrel.env?id_site={0}"
                            "&id_plugin={1}&id_site_app={2}&schema_app={3}"
                            "&id_conteudo_app={4}".format(self.id_site,
                                                          self.id_plugin, 
                                                          kargs["id_site"], 
                                                          kargs["schema"], 
                                                          kargs["id_conteudo"])),
                    "dados": ("'status=no, toolbar=no, menubar=no, personalbar=no,"
                              "resizable=yes, scrollbars=yes, width=%(largura)s,"
                              "height=%(altura)s, left=' + ((screen.width - "
                              "%(largura)s)/2)  + ', top=' + ((screen.height - "
                              "%(altura)s)/2)") % {"largura":500, "altura":450}}
        else:
            return {"alert_err": ("N&atilde;o &eacute; poss&iacute;vel exportar "
                                  "um conte&uacute;do que n&atilde;o seja do "
                                  "tipo not&iacute;cia.")}


    @serialize
    @Permission("PERM APP")
    def exportSaibaMais(self, id_site_app, schema_app, id_conteudo_app,
                              id_site_im, schema_im, id_conteudo_im):
        """
        """
        assert schema_im.find("da_impresso") >= 0, "wrong meta_type"

        for id_pdf, i in self._getImpresso(id_site=id_site_im,
                                           schema=schema_im,
                                           id_conteudo=id_conteudo_im,
                                           saibamais=[{"id_site":id_site_app,
                                                       "schema":schema_app,
                                                       "id_conteudo":id_conteudo_app}]):

            xml = self._createXmls(i)
            id_xml = "{0}{1}.xml".format(strftime("%Y%m%d%H%M%S"),
                                         randint(10000, 99999))
            self._writeXml(source=xml,
                           id_xml=id_xml,
                           saibamais=True)

            return "Conte%FAdo saiba mais exportado com sucesso!"

        raise UserError("N&atilde;o foi poss&iacute;vel encontrar o conte&uacute;do.")
