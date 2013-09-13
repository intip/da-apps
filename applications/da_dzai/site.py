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
import urllib
from publica.utils.json import encode
from publica.utils.decorators import dbconnectionapp, jsoncallback
from publica.core.portal import Portal


class Site(object):
    """ Metodos publicos
    """

    def _quote(self, texto):
        """Retorna texto formatado
        """
        return urllib.quote(texto)


    @jsoncallback
    def getVideos(self, tags, limit=50, offset=0, serialize=None):
        """
        """
        return self.getVideosSite(tags=tags,
                                  limit=limit,
                                  offset=offset,
                                  serialize=serialize)
 

    @dbconnectionapp
    def getVideosSite(self, tags, limit=50, offset=0, serialize=None):
        """Retorna videos se tiverem alguma tag
        """
        qtde = 0
        items = 0
        tags = tags.strip().split(" ")
        portal = Portal(id_site=self.id_site, request=self.request)
        if tags:
            has = False
            for tag in tags:
                has = True
                self.execSqlBatch("select_videos_count",
                                  tag=tag)
            if has:
                for i in self.execSqlUnion():
                    qtde += i["qtde"]

            for tag in tags:
                self.execSqlBatch("select_videos",
                                  tag=tag,
                                  limit=int(limit),
                                  offset=int(offset))
            items = self.execSqlUnion(order="sea_id DESC", limit=int(limit),
                                                           offset=int(offset))
        copia = items
        if serialize:
            items = [i for i in items]
            for i in items:
                comm = portal._getComentarios(env_site=self.id_site,
                                              schema=self.schema,
                                              id_conteudo=i["id_conteudo"])
                comm = [j for j in comm]
                i["comm"] = comm
                i["url"] = portal.getUrlByApp(env_site=self.id_site,
                                              schema=self.schema,
                                              id_conteudo=i["id_conteudo"],
                                              exportar=1,
                                              admin=1)
            return {"qtde":qtde, "items":items}

        return {"qtde":qtde, "items":items}


    @dbconnectionapp
    @jsoncallback
    def getVideo(self, sea_id):
        """Retorna o video selecionado
        """
        item = self.execSql("select_video",
                            sea_id=int(sea_id)).next()
        portal = Portal(id_site=self.id_site, request=self.request)
        comm = portal._getComentarios(env_site=self.id_site,
                                      schema=self.schema,
                                      id_conteudo=item["id_conteudo"])
        comm = [j for j in comm]
        item["comm"] = comm
        return {"item":item}

    @dbconnectionapp
    def getVideoByid(self, id_conteudo):
        """
            Returns data of videos
        """
        for i in self.execSql("select_video_by_id",
                               id_conteudo=int(id_conteudo)):
            for j in self.execSql("select_destaque_video",
                                  id_conteudo=i['id_conteudo']):
                i["destaque"] = {"id_destaque": j["id_destaque"],
                                 "titulo_destaque": j["titulo"],
                                 "descricao_destaque": j["descricao"],
                                 "imagem_destaque": j["img"],
                                 "peso_destaque": j["peso"]}
            return i

