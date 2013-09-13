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
from urllib import quote
from packages.elementtree import ElementTree as ET
from publica.core.portal import Portal
from publica.utils.json import encode, decode


class Site(object):
    """
    """

    def qt(self, text):
        """
        """
        return quote(text)


    def getMenuItem(self, id_menu):
        """
        """
        menu = self.getMenu(id_menu)
        return decode(menu['json'])


    def mkfather(self, item, tag='ul', builder=None, ignore=False,
                       ignf=False, ignl=False, uln=[], lin=[], la=[],
                       nivelu=0, nivell=0,proximoitem=None):
        """
        """
        el = None
        semTexto = item['attributes'].get('semTexto', None)

        if not ignf:

            try:
                attr = uln[nivelu]
            except:
                attr = {}

            if semTexto == 'true':
                attr['id'] = item['data'].lower()

            el = builder.start(tag, attr)

        self.mkson(item, builder, ignore=ignore, uln=uln,
                   lin=lin, la=la, nivelu=nivelu, nivell=nivell)

        regx = re.compile("\[<Element None at [a-zA-Z0-9]+>, <Element 'ul' at [a-zA-Z0-9]+>\]")
        if regx.match(str(builder._elem)):
            builder.end(tag)
            try:
                attr = uln[nivelu]
            except:
                attr = {}
            if proximoitem:
                attr['id'] = proximoitem['data'].lower()
                builder.start(tag,attr)
            else:
                ignl = True

        if not ignl:
            builder.end(tag)

        return el


    def mkson(self, item, builder, tag='li', ignore=False,
                    exportar=None, uln=[], lin=[], la=[], nivelu=0, nivell=0):
        """
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        link = item['attributes'].get('jtext', None)
        classe = item['attributes'].get('classe', None)
        semTexto = item['attributes'].get('semTexto', None)
        scriptBanner = item['attributes'].get('scriptBanner', None)

        if not ignore:

            try:
                attr = lin[nivell]
            except:
                attr = {}

            try:
                attra = la[nivell]
            except:
                attra = {}

            if classe:
                attr['class'] = classe
            builder.start(tag, attr)

            if link:
                attra['href'] = portal.mklink(dados=link, exportar=exportar)
                if attra["href"].find("[target=blank]") >= 0:
                    attra["href"] = attra["href"].replace("[target=blank]", "")
                    if attra['href'].find('window.open') < 0:
                        attra["target"] = "blank"
                builder.start('a', attra)

	    if scriptBanner:
                builder.start('script',{})
                builder.data(scriptBanner)

            if not(semTexto == 'true'):
                builder.data(item['data'])

        if not ignore:
            if link:
                builder.end('a')
	    if scriptBanner:
                builder.end('script')

        nivelu+=1
        itens = item.get('children', [])
        nitens = len(itens)
        for i in xrange(nitens):
            if i == 0:
                ignf = False
                ignl = True
            elif i == (nitens-1):
                ignf = True
                ignl = False
            else:
                ignf = True
                ignl = True

            if nitens == 1:
                ignl = False

            if (i + 1) < nitens:
                proximoitem=itens[i+1]
            else:
                proximoitem=None

            self.mkfather(itens[i], builder=builder, ignf=ignf, ignl=ignl, uln=uln,
                          lin=lin, la=la, nivelu=nivelu, nivell=nivell+1, proximoitem=proximoitem)

        if not ignore:
            builder.end(tag)


    def getMenuHtml(self, id_menu, tag, ignore=True, uln=[], lin=[], la=[]):
        """
        """
        builder = ET.TreeBuilder()
        oxml = self.mkfather(self.getMenuItem(id_menu), tag=tag,
                             builder=builder, ignore=ignore, uln=uln, lin=lin, la=la)
        return ET.tostring(oxml).replace('&apos;', '\'')

