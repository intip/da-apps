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
from urllib import unquote
from types import StringTypes
from time import time, strftime, strptime
from publica.core.portal import Portal
from publica.admin.error import UserError
from publica.admin.file import File
from publica.utils.json import encode
from publica.utils.decorators import serialize, dbconnectionapp,\
                                     Permission, logportal
from publica import settings


def _unquote(text):
    if type(text) in StringTypes:
        return unquote(text)
    return text


class Adm(object):
    """
        Metodos relativo ao crud da administração
    """

    @dbconnectionapp
    def _getTipo(self):
        """
        """
        return self.execSql("select_tipo_noticia")


    @dbconnectionapp
    def _listarAutores(self):
        """ Lista autores cadastrados
        """
        return self.execSql("select_autor")


    @dbconnectionapp
    def getAutores(self):
        """ Lista autores cadastrados
        """
        return encode([i for i in self.execSql("select_autor")])


    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def addAutor(self, nome, email, grupo):
        """ Cadastra um novo autor
        """
        self.execSqlu("insert_autor",
                      nome=nome,
                      email=email,
                      grupo=grupo)

        return "Autor adicionado com sucesso!"


    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def delAutor(self, id_autores=[]):
        """ Deleta autores cadastrados
        """
        for i in id_autores:
            self.execSqlBatch("delete_autor",
                              id_autor=int(i))
        self.execSqlCommit()
        return "Autor deletado com sucesso!"


    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def getAutor(self, id_autor):
        """ Seleciona um autor
        """
        return self.execSql("select_autor_unico",
                            id_autor=int(id_autor)).next()


    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def editAutor(self, id_autor, nome, email, grupo):
        """ Edita as informacoes de um autor
        """
        self.execSqlu("update_autor",
                      id_autor=int(id_autor),
                      nome=nome,
                      email=email,
                      grupo=grupo)

        return "Autor editado com sucesso!"


    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def addNoticia(self, id_site, id_treeapp, id_aplicativo, titulo_categoria,
                         titulo, descricao, tipo, corpo, publicado_em,
                         autor=None, videos=[], editor=None, expira_em=None,
                         publicado=None, foto_id=[], foto_grande_id=[],
                         foto_credito=[], foto_legenda=[], foto_link=[],
                         foto_alinhamento=[], video=None, audio=None,
                         galeria=None,
                         titulo_destaque=None, descricao_destaque=None,
                         imagem_destaque=None, peso_destaque=None,
                         data_edicao=None, relacionamento=[], tags="",
                         exportar=None, exportar_xml=None,
                         exportar_json=None, permissao=None, **kargs):
        """ Adiciona uma nova noticia
        """
        if kargs["titulo_capa"] == "null":
            kargs["titulo_capa"] = None
        if kargs["titulo_galeria"] == "null":
            kargs["titulo_galeria"] = None
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        id_conteudo = self.execSql("select_nextval_noticia").next()["id"]
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

        try:
            p = strptime(data_edicao, "%d/%m/%Y")
            data_edicao = strftime("%Y-%m-%d", p)
        except ValueError, e:
            data_edicao = None

        editor = True if editor else False
        video = True if video else False
        audio = True if audio else False
        galeria = True if galeria else False

        # adicionar noticia
        self.execSqlBatch("insert_noticia", 
                          id_conteudo=id_conteudo,
                          video=video,
                          audio=audio,
                          galeria=galeria,
                          titulo_categoria=_unquote(titulo_categoria),
                          titulo=_unquote(titulo),
                          autor=_unquote(autor),
                          descricao=_unquote(descricao),
                          id_tipo_noticia=int(tipo),
                          corpo=_unquote(corpo),
                          publicado_em=publicado_em,
                          expira_em=expira_em,
                          publicado=publicado,
                          data_edicao=data_edicao,
                          editor=editor,
                          ordem=kargs['ordem'],
                          pdf=kargs['pdf'],
                          is_capa=kargs['is_capa'],
                          titulo_capa=_unquote(kargs['titulo_capa']),
                          titulo_galeria=_unquote(kargs['titulo_galeria']))

        # returns application's config data
        dados_app = portal._getApp(env_site=self.id_site,
                                   schema=self.schema)["dados"]

        # fotos
        dados_fotos = []
        for i in range(len(foto_id)):

            arquivo = foto_id[i]
            arquivo_grande = foto_grande_id[i]
            alinhamento = foto_alinhamento[i]
            credito = foto_credito[i]
            legenda = foto_legenda[i]
            link = foto_link[i]
            if arquivo_grande:
                fl = File(id_site=self.id_site, request=self.request)
                arquivo2 = fl._getFileTemp(arquivo_grande)
                arquivo2 = fl._writeTmpFile("res" + arquivo2[1], arquivo2[0])
                arquivon = portal.addArquivo(arquivo=arquivo2,
                                        id_conteudo=id_conteudo,
                                        schema=self.schema,
                                        dt=dt,
                                        originid=1,
                                        filename="resized",
                                        transform={"metodo":"normal_ratio",
                                                   "dimenx":int(dados_app["dim_x"]),
                                                   "dimeny":int(dados_app["dim_y"])})
 
                if arquivon:
                    arquivo = arquivon

            if arquivo_grande:
                arquivogn = portal.addArquivo(arquivo=arquivo_grande,
                                            id_conteudo=id_conteudo,
                                            schema=self.schema,
                                            dt=dt)
 
                if arquivogn:
                    arquivo_grande = arquivogn

            self.execSqlBatch("insert_foto_noticia", 
                              id_conteudo=id_conteudo,
                              arquivo=arquivo,
                              arquivo_grande=arquivo_grande,
                              alinhamento=alinhamento,
                              credito=_unquote(credito),
                              legenda=_unquote(legenda),
                              link=link)

            dados_fotos.append({"arquivo":arquivo,
                                "arquivo_grande":arquivo_grande,
                                "alinhamento":alinhamento,
                                "credito":credito,
                                "legenda":legenda,
                                "link":link})

        # videos
        dados_video = []
        for i in videos:
            self.execSqlBatch("insert_video",
                              id_conteudo=id_conteudo,
                              embed=i)
            dados_video.append({"embed":i})
        

        #videos iPad
        videos_ipad = {"thumbs":kargs["videos_ipad_thumbnail"],
                       "areaudio":kargs["videos_ipad_audio"],
                       "nomes":kargs["videos_ipad_nome"],
                       "links":kargs["videos_ipad_link"]}

        for i in range(len(videos_ipad["thumbs"])):
            self.execSqlBatch("insert_video_ipad",
                              id_conteudo=id_conteudo,
                              nome=_unquote(videos_ipad["nomes"][i]),
                              is_audio=videos_ipad["areaudio"][i],
                              thumb=videos_ipad["thumbs"][i],
                              link=videos_ipad["links"][i])
        
        #fotos iPad
        fotos_ipad = {"ids":kargs["foto_ipad_id"],
                      "creditos":kargs["foto_ipad_credito"],
                      "legendas":kargs["foto_ipad_legenda"]}
        for i in range(len(fotos_ipad["ids"])):
            imagem = portal.addArquivo(arquivo=fotos_ipad["ids"][i],
                                       id_conteudo=id_conteudo,
                                       schema=self.schema,
                                       dt=dt)
            self.execSqlBatch("insert_foto_ipad",
                              id_conteudo=id_conteudo,
                              foto=imagem,
                              credito=_unquote(fotos_ipad["creditos"][i]),
                              legenda=_unquote(fotos_ipad["legendas"][i]))

        # destaque
        try:
            peso_destaque = int(peso_destaque)
        except:
            peso_destaque = 0

        dados_destaque = []
        if titulo_destaque or imagem_destaque or descricao_destaque:
            imagem_destaque = portal.addArquivo(arquivo=imagem_destaque,
                                                id_conteudo=id_conteudo,
                                                schema=self.schema,
                                                dt=dt)
            if not imagem_destaque:
                imagem_destaque = None

            self.execSqlBatch("insert_destaque", 
                              id_conteudo=id_conteudo,
                              titulo=_unquote(titulo_destaque),
                              descricao=_unquote(descricao_destaque),
                              img=imagem_destaque,
                              peso=peso_destaque)

            dados_destaque.append({"titulo":titulo_destaque,
                                   "descricao":descricao,
                                   "img":imagem_destaque,
                                   "peso":peso_destaque})

        self.execSqlCommit()
 
        dados = self._setDados(id_conteudo=id_conteudo)
        portal._addConteudo(env_site=self.id_site,
                            id_pk=id_conteudo,
                            schema=self.schema,
                            meta_type=self.meta_type,
                            id_aplicativo=id_aplicativo,
                            id_treeapp=id_treeapp,
                            peso=peso_destaque,
                            titulo=_unquote(titulo),
                            publicado=publicado,
                            publicado_em=publicado_em,
                            expira_em=expira_em,
                            titulo_destaque=_unquote(titulo_destaque),
                            descricao_destaque=_unquote(descricao_destaque),
                            imagem_destaque=imagem_destaque,
                            tags=tags,
                            permissao=permissao,
                            relacionamento=relacionamento,
                            dados=dados)

        if exportar_xml or exportar_json or exportar:

            portal._insertLog(self.id_site,
                              "Nova not&iacute;cia cadastrada e publicada '%s'" % titulo)

            portal._exportarFormatosConteudo(id_aplicativo=id_aplicativo,
                                             id_conteudo=id_conteudo,
                                             schema=self.schema,
                                             id_treeapp=id_treeapp,
                                             html=exportar,
                                             xml=exportar_xml,
                                             json=exportar_json,
                                             dados=dados,
                                             subitems=None,
                                             add=1)

            return "Not&iacute;cia cadastrada com sucesso! Publica&ccedil;&atilde;o iniciada."
 

        portal._insertLog(self.id_site,
                          "Nova not&iacute;cia cadastrada '%s'" % titulo)
        return "Not&iacute;cia cadastrada com sucesso."


    @dbconnectionapp
    def _getNoticia(self, id_conteudo):
        """
        """
        dic = {}
        noticia = self.execSql("select_noticia",
                               id_conteudo=int(id_conteudo)).next()

        fotos = [i for i in self.execSql("select_noticia_fotos",
                                         id_conteudo=int(id_conteudo))]
        videos = [i for i in self.execSql("select_videos",
                                         id_conteudo=int(id_conteudo))]

        autores = []
        fotos_ipad = [i for i in self.execSql("select_fotos_ipad", 
                                              id_conteudo=id_conteudo)]
        videos_ipad = [i for i in self.execSql("select_videos_ipad",
                                               id_conteudo=id_conteudo)]

        if len(autores) == 1:
            autores.append(None)
        elif len(autores) == 0:
            autores = [None, None]

        return {"noticia":noticia,
                "fotos":fotos,
                "autores":autores,
                "videos":videos,
                "fotosipad":fotos_ipad,
                "videosipad":videos_ipad}


    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def editNoticia(self, id_treeapp, id_aplicativo, id_conteudo, titulo_categoria,
                          titulo, descricao, tipo, corpo, publicado_em,
                          autor=None, videos=[], editor=None, expira_em=None,
                          publicado=None, foto_id=[], foto_grande_id=[],
                          foto_credito=[], foto_legenda=[], foto_link=[],
                          foto_alinhamento=[], video=None, audio=None,
                          galeria=None,
                          titulo_destaque=None, descricao_destaque=None,
                          imagem_destaque=None, peso_destaque=None,
                          id_destaque=None,
                          relacionamento=[], tags=None,
                          data_edicao=None, exportar=None, exportar_json=None,
                          exportar_xml=None, permissao=None, **kargs):
        """
        """
        if kargs["titulo_capa"] == "null":
            kargs["titulo_capa"] = None
        if kargs["titulo_galeria"] == "null":
            kargs["titulo_galeria"] = None
        portal = Portal(id_site=self.id_site, request=self.request)
        publicado = True if publicado else False
        tags = tags if tags else None

        dt = publicado_em
        try:
            publicado_em_t = strptime(publicado_em, "%d/%m/%Y %H:%M")
            publicado_em = strftime("%Y-%m-%d %H:%M", publicado_em_t)
        except ValueError, e:
            raise UserError(("Ocorreu um erro: "
                             "Data de publica&ccedil;&aring;o "
                             "inv&aacute;lida (%s)") % publicado_em)
        try:
            p = strptime(expira_em, "%d/%m/%Y %H:%M")
            expira_em = strftime("%Y-%m-%d %H:%M", p)
        except ValueError, e:
           expira_em = None

        try:
            p = strptime(data_edicao, "%d/%m/%Y")
            data_edicao = strftime("%Y-%m-%d", p)
        except ValueError, e:
           data_edicao = None

        atualizado_em = strftime('%Y-%m-%d %H:%M')
        editor = True if editor else False
        video = True if video else False
        audio = True if audio else False
        galeria = True if galeria else False

        self.execSqlBatch("delete_dados_noticia",
                          id_conteudo=int(id_conteudo))
        # adicionar noticia
        self.execSqlBatch("update_noticia",
                          id_conteudo=int(id_conteudo),
                          video=video,
                          audio=audio,
                          galeria=galeria,
                          titulo_categoria=_unquote(titulo_categoria),
                          titulo=_unquote(titulo),
                          autor=_unquote(autor),
                          descricao=_unquote(descricao),
                          id_tipo_noticia=int(tipo),
                          corpo=_unquote(corpo),
                          publicado_em=publicado_em,
                          expira_em=expira_em,
                          publicado=publicado,
                          atualizado_em=atualizado_em,
                          data_edicao=data_edicao,
                          editor=editor,
                          ordem=kargs['ordem'],
                          pdf=kargs['pdf'],
                          is_capa=kargs['is_capa'],
                          titulo_capa=_unquote(kargs['titulo_capa']),
                          titulo_galeria=_unquote(kargs['titulo_galeria']))

        # returns application's config data
        dados_app = portal._getApp(env_site=self.id_site,
                                   schema=self.schema)["dados"]

        # fotos
        dados_fotos = []
        for i in range(len(foto_id)):
            arquivo = foto_id[i]
            arquivo_grande = foto_grande_id[i]
            alinhamento = foto_alinhamento[i]
            credito = foto_credito[i]
            legenda = foto_legenda[i]
            link = foto_link[i]

            if arquivo_grande:
                fl = File(id_site=self.id_site, request=self.request)
                arquivo2 = fl._getFileTemp(arquivo_grande)
                arquivo2 = fl._writeTmpFile("res" + arquivo2[1], arquivo2[0])
                arquivon = portal.addArquivo(arquivo=arquivo2,
                                        id_conteudo=id_conteudo,
                                        schema=self.schema,
                                        dt=dt,
                                        originid=1,
                                        filename="resized",
                                        transform={"metodo":"normal_ratio",
                                                   "dimenx":int(dados_app["dim_x"]),
                                                   "dimeny":int(dados_app["dim_y"])})
 
                if arquivon:
                    arquivo = arquivon

            if arquivo_grande:
                arquivogn = portal.addArquivo(arquivo=arquivo_grande,
                                            id_conteudo=id_conteudo,
                                            schema=self.schema,
                                            dt=dt)
 
                if arquivogn:
                    arquivo_grande = arquivogn


            self.execSqlBatch("insert_foto_noticia", 
                              id_conteudo=int(id_conteudo), 
                              arquivo_grande=arquivo_grande,
                              arquivo=arquivo,
                              alinhamento=alinhamento,
                              credito=_unquote(credito),
                              legenda=_unquote(legenda),
                              link=link)

            dados_fotos.append({"arquivo":arquivo,
                                "arquivo_grande":arquivo_grande,
                                "alinhamento":alinhamento,
                                "credito":credito,
                                "legenda":legenda,
                                "link":link})


        # videos
        dados_videos = []
        for i in videos:
            self.execSqlBatch("insert_video", 
                              id_conteudo=int(id_conteudo),
                              embed=i)
            dados_videos.append({"embed":i})

        #videos iPad
        videos_ipad = {"thumbs":kargs["videos_ipad_thumbnail"],
                       "areaudio":kargs["videos_ipad_audio"],
                       "nomes":kargs["videos_ipad_nome"],
                       "links":kargs["videos_ipad_link"]}

        for i in range(len(videos_ipad["thumbs"])):
            self.execSqlBatch("insert_video_ipad",
                              id_conteudo=id_conteudo,
                              nome=_unquote(videos_ipad["nomes"][i]),
                              is_audio=videos_ipad["areaudio"][i],
                              thumb=videos_ipad["thumbs"][i],
                              link=videos_ipad["links"][i])
        
        #fotos iPad
        fotos_ipad = {"ids":kargs["foto_ipad_id"],
                      "creditos":kargs["foto_ipad_credito"],
                      "legendas":kargs["foto_ipad_legenda"]}
        for i in range(len(fotos_ipad["ids"])):
            imagem = portal.addArquivo(arquivo=fotos_ipad["ids"][i],
                                       id_conteudo=id_conteudo,
                                       schema=self.schema,
                                       dt=dt)
            self.execSqlBatch("insert_foto_ipad",
                              id_conteudo=id_conteudo,
                              foto=imagem,
                              credito=_unquote(fotos_ipad["creditos"][i]),
                              legenda=_unquote(fotos_ipad["legendas"][i]))

        # destaque
        try:
            peso_destaque = int(peso_destaque)
        except:
            peso_destaque = 0

        dados_destaque = []
        if titulo_destaque or imagem_destaque or descricao_destaque:

            imagem_destaquen = portal.addArquivo(arquivo=imagem_destaque,
                                          id_conteudo=int(id_conteudo),
                                          schema=self.schema,
                                          dt=dt)
 
            if imagem_destaquen:
                imagem_destaque = imagem_destaquen
            elif not imagem_destaque:
                imagem_destaque = None

            if id_destaque:
                self.execSqlBatch("update_destaque", 
                                  id_conteudo=int(id_conteudo),
                                  id_destaque=int(id_destaque),
                                  titulo=titulo_destaque,
                                  descricao=descricao_destaque,
                                  img=imagem_destaque,
                                  peso=peso_destaque)
            else:
                self.execSqlBatch("insert_destaque", 
                                  id_conteudo=int(id_conteudo),
                                  titulo=titulo_destaque,
                                  descricao=descricao_destaque,
                                  img=imagem_destaque,
                                  peso=peso_destaque)
        elif id_destaque:
            self.execSqlBatch("delete_destaque",
                              id_destaque=int(id_destaque))
            titulo_destaque = titulo_destaque
            descricao_destaque = descricao_destaque
            imagem_destaque = imagem_destaque

        dados_destaque.append({"titulo":titulo_destaque,
                               "descricao":descricao_destaque,
                               "img":imagem_destaque,
                               "peso":peso_destaque})

        self.execSqlCommit()

        dados = self._setDados(id_conteudo=id_conteudo)
        portal._editConteudo(env_site=self.id_site,
                             id_pk=id_conteudo,
                             id_aplicativo=int(id_aplicativo),
                             schema=self.schema,
                             id_treeapp=id_treeapp,
                             peso=peso_destaque,
                             titulo=_unquote(titulo),
                             publicado=publicado,
                             publicado_em=publicado_em,
                             expira_em=expira_em,
                             titulo_destaque=_unquote(titulo_destaque),
                             descricao_destaque=_unquote(descricao_destaque),
                             imagem_destaque=imagem_destaque,
                             permissao=permissao,
                             tags=tags,
                             relacionamento=relacionamento,
                             dados=dados)

        if exportar_xml or exportar_json or exportar:

            portal._insertLog(self.id_site,
                              "Not&iacute;cia '%s' editada e publicada" % titulo)

            portal._exportarFormatosConteudo(id_aplicativo=id_aplicativo,
                                             id_conteudo=id_conteudo,
                                             schema=self.schema,
                                             id_treeapp=id_treeapp,
                                             html=exportar,
                                             xml=exportar_xml,
                                             json=exportar_json,
                                             dados=dados,
                                             subitems=None,
                                             edit=1)

            return ("Not&iacute;cia editada com sucesso! "
                    "Publica&ccedil;&atilde;o iniciada.")

        portal._insertLog(self.id_site,
                          "Not&iacute;cia '%s' editada" % titulo)
        return "Not&iacute;cia editada com sucesso."


    @dbconnectionapp
    def _getDateTimeHash(self, id_treeapp, id_aplicativo):
        """
            Returns the last datetime of one tree, if exist a content
        """
        for i in self.execSql("select_datetime_hash",
                              id_treeapp=int(id_treeapp),
                              id_aplicativo=int(id_aplicativo)):
            return i["publicado_em"]

