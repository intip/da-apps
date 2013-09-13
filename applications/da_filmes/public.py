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
from publica.utils.decorators import dbconnectionapp


class Public(object):

    """
        public class of methods of this content
    """

    @dbconnectionapp
    def getFilme(self, id_filme):
        """
        """
        for filme in self.execSql("select_filme", id_conteudo=int(id_filme)):
            filme["paises"] = []
            pais = ''
            for j in self.execSql("select_pais_filme",
                                  id_conteudo=int(filme['id_conteudo'])):
                pais += '/' + j["nome"]

            filme['paises'] = pais[1:]
            return filme

    def _getAttrFilme(self, id_noticia):
        """
            return portal data of content

            >>> self._getAttrNoticia(1)
            {'id_treeapp':, 'id_aplicativo':, 'url':,
             'voto':, 'nvoto':, 'acesso':, 'comentario':, 'tags':}
        """
        return self._getAttrContent(schema=self.schema,
                                    id_conteudo=id_noticia)
