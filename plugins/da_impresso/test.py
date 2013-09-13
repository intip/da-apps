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
import sys;sys.path.append("../../../")
import unittest
from publica.admin.appportal import PortalUtils
from publica.utils.util import FakeRequest
from publica import settings
from plug import Plug


class TestCase(unittest.TestCase):
    """
      a test case to test this plugin
    """
    lasttest = False


    def setUp(self):
        """
            Provide the test enviroment
        """
        self._plug = Plug(id_site=1,
                          dados={"titulo":"test",
                                 "path":"/tmp",
                                 "hora":"",
                                 "schema":""})
        self._plug._getImpresso = lambda x=self:self._test

        self._test = [
            {'document': {
                            'docname': 'EVE2505P0005',
                            'id_content': 123456,
                            'Titulo':'Test one',
                            'Bigode':'bigode test',
                            'Autor':'Alexandre Gans',
                            'Titulo_galeria':'Titulo da galeria',
                            'Paragrafo':'Corpo da noticia blah blah blah',
                            'ordem':1,
            },
               'images':[ {'Imagem':'http://host/someimage.gif',
                           'Autor':'autor 1',
                           'Legenda':'legenda 1',
                           'destaque': True},
                          {'Imagem':'http://host/someimage2.gif',
                           'Autor':'autor 2',
                           'Legenda':'legenda 2',
                           'destaque': False},
                        ],
               'videos':[ {'Video':'http://host/video.mp4', 'thumb':'', 'Titulo':'titulo video 1'},
                          {'Video':'http://host/video.mp4', 'thumb':'', 'Titulo':'titulo video 2'},
                        ],
               'correlata':[181664, 181663,]
            },

            {'document': {
                            'docname': 'EVE2505P0004',
                            'id_content': 123455,
                            'Titulo':'Title with non-ascii téste ação <b>test</b>& te4ste',
                            'Bigode':'bigode ação',
                            'Autor':'Alexandre Gáns',
                            'Titulo_galeria':'Título da galêria',
                            'Paragrafo':"""Corpô da notícia blah blah blah
                                          [FOTO1] teste <b>adfasdf <a href="htttp://"> teste
                                          ação &% sadf#$12 test? > test &acute; test
                                        """,
                            'ordem':2,
            },
               'images':[ {'Imagem':'http://host/someimage.gif',
                           'Autor':'autôr 1',
                           'Legenda':'légenda 1',
                           'destaque': True},
                          {'Imagem':'http://host/someimage2.gif',
                           'Autor':'áutor 2',
                           'Legenda':'lêgenda 2',
                           'destaque': False},
                        ],
               'videos':[ {'Video':'http://host/video.mp4', 'thumb':'', 'Titulo':'título video 1'},
                          {'Video':'http://host/video.mp4', 'thumb':'', 'Titulo':'títúlô video 2'},
                        ],
               'correlata':[181665, 181666,]
            },


            ]
        

    def test_1(self):
        """
            test the xml with various data
        """
        self._plug._action(None, None, None, None)
 


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
