# -*- encoding: LATIN1 -*-
#
# Copyright 2008 Intip.
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
#import elementtree.ElementTree as ET
from packages.elementtree import ElementTree as ET
import urllib #cb
import xml.dom.minidom #cb
import sys #cb
from urllib import unquote

class Site(object):
    """
    """

    def getDivirtase(self, xml='divirtase.xml'):
        """
        """
        retorno = []

        path_xml = self.path_base + '/' + xml
        f = open(path_xml, 'r')
        source = unquote(f.read())
        f.close()
        root = ET.fromstring(source)

        for c in root.getchildren():
            id_filme = c.find('id_filme').text
            titulo = c.find('titulo').text
            retorno.append({'id':id_filme, 'titulo':titulo})

        return retorno


    def indicadores(self, xmls=['cambio.xml','indices.xml','indicadores.xml'], papeis=['DOL COM','PTAX850','DJI']):
        retorno = []

        for arq_xml in xmls:
            path_xml = self.path_base + '/' + arq_xml
            root = ET.parse(path_xml).getroot()
            for c in root.getchildren():
                if(c.find('PAPEL').text in papeis):
                    dictSaida = {}
                    for node in c:
                        dictSaida[node.tag] = str(node.text).replace('.',',')

                    retorno.append(dictSaida)

        return retorno


