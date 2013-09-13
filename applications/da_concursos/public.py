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
from publica.utils.decorators import dbconnectionapp, jsoncallback
from publica.core.portal import Portal


class Public(object):

    """
        public class of methods of this content
    """

    def _getPlugAuth(self):
        """
            retorna os dados do app
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        dados = self._getDados()
        return portal._getPlug(env_site=self.id_site,
                               id_plugin=dados['auth_id'])['app']

    @dbconnectionapp
    def _getFiles(self, id_conteudo):
        """
          return file content
        """
        files = []
        for i in self.execSql("select_file",
                              id_conteudo=int(id_conteudo)):
            files.append(i)
        return files

    @dbconnectionapp
    def _verifyUser(self, id_usuario_wad=None, email=None):
        """
            verifica se o usuário
            possui id cadastrado
            na table do app
        """
        result = []
        if id_usuario_wad:
            id_usuario = id_usuario_wad
            result = [i for i in self.execSql("select_user_id_wad",
                                              id_usuario_wad=int(id_usuario))]
        else:
            result = [i for i in self.execSql("select_user_email",
                                              email=email)]
        return result

    @dbconnectionapp
    def _addUser(self, dados):
        """
            adiciona o usuário logado
            na table do app
        """
        verification = self._verifyUser(id_usuario_wad=dados['id'])
        if not verification:
            self.execSqlu("insert_usuario",
                          id_usuario_wad=int(dados['id']),
                          email=dados['email'],
                          nome=dados['nome'])

    @dbconnectionapp
    def _getEstadosConcurso(self, id_conteudo):
        """
            retorna lista de estados
        """
        estados = []
        for i in self.execSql("select_estados_concurso",
                              id_conteudo=int(id_conteudo)):
            estados.append(i)
        return estados

    @dbconnectionapp
    def _getConcurso(self, id_conteudo):
        """
            retorna o conteudo e seus arquivos
        """
        for i in self.execSql("select_conteudo",
                              id_conteudo=int(id_conteudo)):
            i['arquivos'] = self._getFiles(id_conteudo)
            i['estados'] = self._getEstadosConcurso(id_conteudo)
            return i

    @dbconnectionapp
    def _getConcursosStatus(self, status='', limit=10,
                            offset=0):
        """
            retorna lista de concursos de acordo
            com os parametros passados.
            status podem ser
            inscricoes, andamentos, previstos
            finalizados ou novos
        """
        if status:
            concursos = []
            sql = "select_concursos_" + status
            cont = 0
            for i in self.execSql(sql,
                                  limit=int(limit),
                                  offset=int(offset)):
                cont += 1
                concursos.append(i)
            return {"concursos": concursos, "total": cont}
        else:
            return self.execSql('select_concursos',
                                limit=int(limit),
                                offset=int(offset))

    @dbconnectionapp
    def _getTotalVagas(self, filtro=False):
        """
            retorna total de vagas no id_site
        """
        if filtro:
            sql = "select_soma_concursos_filtro"
        else:
            sql = "select_soma_vagas"
        total = list(self.execSql(sql))[0]['sum']
        return total

    @dbconnectionapp
    def _addFavorite(self, id_usuario, id_concurso):
        """
            adiciona favorito para um
            determinado usuário
            sem callback
        """
        from datetime import datetime
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.execSqlu("insert_favorito",
                      id_usuario=int(id_usuario),
                      id_conteudo=int(id_concurso),
                      data=data)

    @dbconnectionapp
    def _delFavorite(self, id_usuario, id_concurso):
        """
            adiciona favorito para um
            determinado usuário
            sem callback
        """
        self.execSqlu("delete_favorito",
                      id_usuario=int(id_usuario),
                      id_conteudo=int(id_concurso))

    @dbconnectionapp
    def _getConcursosFavoritos(self, email, limit=10, offset=0):
        """
            retorna os concursos
            favoritados por um
            usuário
        """
        res = [i for i in self.execSql("select_concursos_favoritos",
                                       email=email,
                                       limit=int(limit),
                                       offset=int(offset))]
        return res

    @jsoncallback
    def autenticar(self, email, senha):
        """
            autentica o usuário
        """
        central = self._getPlugAuth()
        autenticar = central._autenticar(email,
                                         senha)
        if autenticar['id'] == '1' or autenticar['id'] == '2':
            dados = central._getUserData(email)
            self._addUser(dados)
            return autenticar
        else:
            return autenticar

    @jsoncallback
    def logoff(self):
        """
           logoff do usuario logado
        """
        central = self._getPlugAuth()
        return central._logoff()

    @jsoncallback
    def favoritar(self, id_concurso):
        """
            Favorita o concurso
            para um determinado
            usuário.
        """
        central = self._getPlugAuth()
        usuario = central._isSessionActive()
        if usuario:
            usuario_app = self._verifyUser(email=usuario['email'])
            self._addFavorite(usuario_app[0]['id_usuario'], id_concurso)
            return {"id": "1",
                    "type": "ok",
                    "description": "Adicionado com sucesso"}
        else:
            return {"id": "2",
                    "type": "error",
                    "description": "usuario nao autenticado"}

    @jsoncallback
    def delFavorito(self, id_concurso):
        """
            deleta favorito
            do usuário
        """
        central = self._getPlugAuth()
        usuario = central._isSessionActive()
        if usuario:
            usuario_app = self._verifyUser(email=usuario['email'])
            self._delFavorite(usuario_app[0]['id_usuario'], id_concurso)
            return {"id": "1",
                    "type": "ok",
                    "description": "Deletado com sucesso"}
        else:
            return {"id": "2",
                    "type": "error",
                    "description": "usuario nao autenticado"}

    @jsoncallback
    def getConcursosStatus(self, status='', limit=10,
                           offset=0):
        """
            retorna concursos
            por status callback
        """
        return self._getConcursosStatus(status, limit,
                                        offset)

    @jsoncallback
    def getConcursosFavoritos(self, email='', limit=10,
                              offset=0):
        """
            retorna concursos
            por status callback
        """
        central = self._getPlugAuth()
        usuario = central._isSessionActive()
        if usuario:
            return {"id": "1",
                    "res": self._getConcursosFavoritos(email,
                                                       limit,
                                                       offset)}
        else:
            return {"id": "2",
                    "type": "error",
                    "description": "usuario nao autenticado"}
