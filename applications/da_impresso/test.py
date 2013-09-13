# coding: utf-8
#
# Copyright 2009 Prima Tech Informatica LTDA.
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
from app import meta_type, App


class TestCase(unittest.TestCase):
    """
      an test case to test this application
    """

    ## constants variables - probably on other class of Publica
    id_site = 1 # test site
    schema = None # to set on setUp
    request = None
    title = "Noticia - unittest"
    app = None
    lasttest = False


    def setUp(self):
        """
            Provide the test enviroment with these actions:
            install an instance of this application and
            install a portlet with default code of this application and
            install a page with previous portlet and
            install and configure a folder with this application
        """
        if not self.schema:
            self.request = FakeRequest()
            self.request.request["env.mk"] = settings.MAGIC_KEY
            self.schema = "noticia_unittest"
            self.portal = PortalUtils(self.id_site, self.request)
            self.portal.installApp(schema=self.schema,
                                   meta_type=meta_type,
                                   title=self.title)

            self.app = App(id_site=self.id_site,
                           schema=self.schema,
                           request=self.request)

        ## add aplicativo
        ## add portlet, pagina
        ## add folder e configurar aplicativo
        

    def tearDown(self):
        """
            Delete current test enviroment with these actions:
            delete the folder, page, portlet, content of the application(portal)
            delete application
        """
        ## deletar itens usados
        ## deletar pagina, portlet
        ## deletar conteudo aplicativo - portal
        ## deletar aplicativo
        if self.lasttest:
            self.portal.unistallApp(schema=self.schema)
            self.schema = None

    def test_1_tipos(self):
        """
            Test if the table tipo_noticia was populate
        """
        qtde = len([i for i in self.app._getTipo()])
        self.assertTrue(qtde > 0)


    def test_2_addautor(self):
        """
            Test method to add new autors
        """
        for  nome, email, grupo in (("Autor 1", "email@email.com", "grupo 1"),
                                    ("Autor 2", "email@email.com", "")):
            self.app.addAutor(nome=nome,
                              email=email,
                              grupo=grupo)


    def test_3_listautor(self):
        """
          Test methods of listing autors
        """ 
        [i for i in self.app._listarAutores()]
        self.app.getAutores()


    def test_4_getautor(self):
        """
           Test method to get content of autor
        """
        self.app.getAutor(1)


    def test_5_editautor(self):
        """
            Test method of autor dados edit
        """
        for i in self.app._listarAutores():
            self.app.editAutor(id_autor=i["id_autor"],
                               nome="%s-edited" % i["nome"],
                               email="%s-edited" % i["email"],
                               grupo="%s-edited" % i["grupo"])


    def test_6_delautor(self):
        """
        """
        id_autor = [i["id_autor"] for i in self.app._listarAutores()]
        self.app.delAutor(id_autor)


    def test_9999_last(self):
        """
          this test is only to call tearDown for last
        """
        self.lasttest = True
 


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
