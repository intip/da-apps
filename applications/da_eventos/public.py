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
from datetime import datetime, timedelta
from decimal import *
import math
from time import time, strftime, strptime
from urllib import unquote
from publica import settings
from publica.core.portal import Portal
from publica.admin.file import File
from publica.utils.json import encode, decode
from publica.utils.decorators import dbconnectionapp, serialize, jsoncallback
import base64

class Public(object):

    """
        public class of methods of this content
    """

    def _getAppAuth(self):
        """
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        dados = portal._getApp(env_site=self.id_site,
                               schema=self.schema)["dados"]
        if dados.get("auth_plug", None):

            return portal._getPlug(env_site=self.id_site,
                                   id_plugin=dados["auth_plug"])['app']

        if dados.get("auth_schema", None):

            return portal._getAplication(id_site=self.id_site,
                                         meta_type=dados["auth_type"],
                                         schema=dados["auth_schema"])

    def _getDadosApp(self):
        """
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        return portal._getApp(env_site=self.id_site,
                              schema=self.schema)["dados"]

    def _verifyUser(self):
        """
        Verifica se o user esta autenticado
        """
        app = self._getAppAuth()
        session = app._isSessionActive()
        if session:
            return session
        else:
            return 0

    @jsoncallback
    def verifyUser(self):
        q = self._verifyUser()
        if q:
            return {"ok":1, "error":0}
        else:
            app = self._getAppAuth()
            app.expiresUser()
            return {"ok":0, "error":1}

    @dbconnectionapp
    @jsoncallback
    def gravardados(self, id_site, id_treeapp, id_aplicativo, titulo, descricao,
                    data_inicio, data_fim, hora_inicio, hora_fim,
                    local, site, preco_entrada, categoria, consumacao_minima,
                    imagem, credito_imagem, telefones=None, email=None,
                    publicado=None, exportar=None, exportar_xml=None,
                    exportar_json=None, relacionamento=[], permissao=None):
        """Stores an answer to a form.

        It uses the kwargs list to generate de fields.
        May receive a list of files in 'arquivos'"""
        dadosapp = self._getDadosApp()
        session = self._verifyUser()
        if session:
            usuario = int(dadosapp['id_usuario'])
            today = datetime.now()
            #publicado_em =  str(today.day) + "/"+ str(today.month) +"/" + str(today.year)
            publicado_em = None
            expira_em = None
            id_conteudo = self.execSql("select_nextval_evento").next()["id"]
            id_destaque = self.execSql("select_nextval_destaque").next()["id"]
            self.request.request["env.mk"] = settings.MAGIC_KEY
            self.request.request["env.usuario"] = {"id_usuario":usuario}
            dt = publicado_em
            try:
                p = strptime(data_inicio, "%d/%m/%Y")
                data_inicio = strftime("%Y-%m-%d", p)
            except ValueError, e:
                return "data em formato incorreto"
            try:
                p = strptime(data_fim, "%d/%m/%Y")
                data_fim = strftime("%Y-%m-%d", p)
            except ValueError, e:
                return "data em formato incorreto"
            nomearq = imagem.filename
            tipoarq = imagem.type
            if dadosapp['publicacao'] == 'moderada':
                publicado = False
                publicado_em = today.now()
                try:
                    publicado_em = strftime("%Y-%m-%d %H:%M")
                except ValueError, e:
                    return "data em formato incorreto"
            else:
                publicado = True
                dt = today.now() + timedelta(minutes=2)
                dt = dt.timetuple()
                try:
                    publicado_em = strftime("%Y-%m-%d %H:%M", dt)
                except ValueError, e:
                    return "data em formato incorreto"
            class a:
                def __init__(self, b):
                    self.x = b
                def __pg_repr__(self):
                    return self.x
            imagem = base64.encodestring(imagem.file.read())
            sucesso = self.execSqlBatch("insert_evento_ext",
                                        id_conteudo=id_conteudo,
                                        titulo=titulo.capitalize().decode("utf-8").encode("latin1"),
                                        publicado_em=publicado_em,
                                        atualizado_em = None,
                                        expira_em=None,
                                        publicado=publicado,
                                        local=local.capitalize().decode("utf-8").encode("latin1"),
                                        site=site.lower(),
                                        email = email.lower(),
                                        telefones = telefones,
                                        data_inicio = data_inicio,
                                        data_fim = data_fim,
                                        hora_inicio = hora_inicio,
                                        hora_fim = hora_fim,
                                        preco_entrada = preco_entrada,
                                        consumacao_minima = consumacao_minima,
                                        credito_imagem = credito_imagem.capitalize(),
                                        usuario = session["nome"],
                                        email_user = session["email"])
            dados_destaque = []
            self.execSqlBatch("insert_destaque",
                              id_conteudo=id_conteudo,
                              id_destaque=id_destaque,
                              titulo=titulo.capitalize().decode("utf-8").encode("latin1"),
                              descricao=descricao.capitalize().decode("utf-8").encode("latin1"),
                              img=None,
                              peso=0)
            self.execSqlBatch("insert_tempimg",
                               id_destaque=id_destaque,
                               imagembin = a(imagem),
                               tipoarq = tipoarq,
                               nomearq = nomearq)

            if type(categoria) is not list:
                categoria =[categoria]
            for i in range(len(categoria)):
                self.execSqlBatch("insert_categoria_evento",
                                  id_categoria=int(categoria[i]),
                                  id_conteudo=int(id_conteudo))
            self.execSqlCommit()
            dados = self._setDados(id_conteudo=id_conteudo)
            self._addContentPortal(env_site=self.id_site,
                                   id_pk=id_conteudo,
                                   id_aplicativo=id_aplicativo,
                                   schema=self.schema,
                                   meta_type=self.meta_type,
                                   id_treeapp=id_treeapp,
                                   titulo=titulo,
                                   publicado = publicado,
                                   publicado_em=publicado_em,
                                   expira_em=expira_em,
                                   titulo_destaque=None,
                                   descricao_destaque=None,
                                   imagem_destaque=None,
                                   permissao=None,
                                   tags=None,
                                   relacionamento=relacionamento,
                                   dados=dados)
            if exportar_xml or exportar_json or exportar:
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
                return ("Evento gravado com sucesso! "
                        "Publica&ccedil;&atilde;o iniciada.")
            return {"ok":"Evento gravado com sucesso.", "error":""}
        else:
            return {"ok":"", "error":"usuario nao autenticado"}

    @dbconnectionapp
    def getCategorias(self):
        """
            retorna todas categorias
        """
        return self.execSql("select_categorias")

    @dbconnectionapp
    def _getAttrEvento(self, id_evento):
        """
            return portal data of content

            >>> self._getAttrNoticia(1)
            {'id_treeapp':, 'id_aplicativo':, 'url':,
             'voto':, 'nvoto':, 'acesso':, 'comentario':, 'tags':}
        """
        return self._getAttrContent(schema=self.schema,
                                     id_conteudo=id_evento)

    @dbconnectionapp
    def getEventos(self, limit=10, orderby=False):
        """
            returns the data from a news content

            @mkl: overwrites de default render method of links

            >>> self._getNoticiaPublicada(id_noticia=1)
            {'id_conteudo':, 'titulo_categoria':, 'titulo':, 'descricao':,
             'id_tipo_noticia':, 'editor':, 'corpo':, 'video':, 'audio':,
             'galeria':, 'publicado_em':, 'publicado':, 'atualizado_em':,
             'id_destaque':, 'titulo_destaque':, 'descricao_destaque':,
             'imagem_destaque':, 'titulo_tree':, 'breadcrump':}
        """
        today = datetime.now()
        data_inicio =  str(today.date())
        evento = None
        if orderby:
            select = "select_eventos_publicado_order"
        else:
            select = "select_eventos_publicado"

        for evento in self.execSql(select,
                                   limit=limit,
                                   data_inicio=data_inicio):
            evento["categorias"]=[]
            for k in self.execSql("select_categoria_evento", id_conteudo=int(evento['id_conteudo'])):
                categoria = {"id_categoria":k["id_categoria"],
                             "nome_categoria":k["nome_categoria"]}
                evento["categorias"].append(categoria)
            for j in self.execSql("select_destaque",
                                  id_conteudo=evento["id_conteudo"]):

                evento["destaque"] = {"id_destaque": j["id_destaque"],
                                      "titulo_destaque": j["titulo"],
                                      "descricao_destaque": j["descricao"],
                                      "imagem_destaque": j["img"],
                                      "peso_destaque": j["peso"]}

            yield evento


    @jsoncallback
    @dbconnectionapp
    def getMoreEventos(self, limit, date, titulo, num, flag, date_limit = None):
        """
        returns more events
        """
        titulo = titulo.decode('utf-8').encode('latin-1')
        limit = int(limit)
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        num = int(num)
        de = (num-1) * limit
        ate = limit
        evento = None
        lista = []
        flag = int(flag)
        if flag:
            select = "select_more_eventos_inicial"
            select_count = "select_more_eventos_inicial_count"
        else:
            select = "select_more_eventos_by_calendar"
            select_count = "select_more_eventos_by_calendar_count"

        if titulo!='todos' and date !='todas':

            for evento in self.execSql("select_eventos_by_calendar_and_title",
                                       de=int(de),
                                       ate=int(ate),
                                       date = str(date),
                                       titulo=titulo):
                
                evento["link"] = \
                portal.getUrlByApp(env_site=self.id_site,
                                   schema=self.schema,
                                   id_conteudo=evento["id_conteudo"],
                                   exportar=1,
                                   admin=1)
                p = strptime(evento["data_inicio"], "%Y-%m-%d %H:%M:%S")
                evento["data_inicio"] = strftime("%d/%m/%Y", p)
                evento["categorias"]=[]
                for k in self.execSql("select_categoria_evento", id_conteudo=int(evento['id_conteudo'])):
                    categoria = {"id_categoria":k["id_categoria"],
                                 "nome_categoria":k["nome_categoria"]}
                    evento["categorias"].append(categoria)
                for j in self.execSql("select_destaque",
                                      id_conteudo=evento["id_conteudo"]):

                    evento["destaque"] = {"id_destaque": j["id_destaque"],
                                          "titulo_destaque": j["titulo"],
                                          "descricao_destaque": j["descricao"],
                                          "imagem_destaque": j["img"],
                                          "peso_destaque": j["peso"]}
                    evento['destaque']['imagem_destaque'] = \
                    portal.getUrlByFile(evento['destaque']['imagem_destaque'],
                                        id_site=self.id_site)
                lista.append(evento)

        elif titulo=='todos' and date !='todas':

            for evento in self.execSql(select,
                                       de=int(de),
                                       ate=int(ate),
                                       date = str(date)):

                evento["link"] = \
                portal.getUrlByApp(env_site=self.id_site,
                                   schema=self.schema,
                                   id_conteudo=evento["id_conteudo"],
                                   exportar=1,
                                   admin=1)
                p = strptime(evento["data_inicio"], "%Y-%m-%d %H:%M:%S")
                evento["data_inicio"] = strftime("%d/%m/%Y", p)
                evento["categorias"]=[]
                for k in self.execSql("select_categoria_evento", id_conteudo=int(evento['id_conteudo'])):
                    categoria = {"id_categoria":k["id_categoria"],
                                 "nome_categoria":k["nome_categoria"]}
                    evento["categorias"].append(categoria)
                for j in self.execSql("select_destaque",
                                      id_conteudo=evento["id_conteudo"]):

                    evento["destaque"] = {"id_destaque": j["id_destaque"],
                                          "titulo_destaque": j["titulo"],
                                          "descricao_destaque": j["descricao"],
                                          "imagem_destaque": j["img"],
                                          "peso_destaque": j["peso"]}
                    evento['destaque']['imagem_destaque'] = \
                    portal.getUrlByFile(evento['destaque']['imagem_destaque'],
                                        id_site=self.id_site)
                lista.append(evento)

        elif titulo !='todos' and date=='todas':

            for evento in self.execSql("select_more_eventos_by_titulo",
                                       de=int(de),
                                       ate=int(ate),
                                       titulo=titulo):

                evento["link"] = portal.getUrlByApp(env_site=self.id_site,
                                                    schema=self.schema,
                                                    id_conteudo=evento["id_conteudo"],
                                                    exportar=1,
                                                    admin=1)

                p = strptime(evento["data_inicio"],
                             "%Y-%m-%d %H:%M:%S")

                evento["data_inicio"] = strftime("%d/%m/%Y", p)
                evento["categorias"]=[]
                for k in self.execSql("select_categoria_evento", id_conteudo=int(evento['id_conteudo'])):
                    categoria = {"id_categoria":k["id_categoria"],
                                 "nome_categoria":k["nome_categoria"]}
                    evento["categorias"].append(categoria)
                for j in self.execSql("select_destaque",
                                      id_conteudo=evento["id_conteudo"]):

                    evento["destaque"] = {"id_destaque": j["id_destaque"],
                                          "titulo_destaque": j["titulo"],
                                          "descricao_destaque": j["descricao"],
                                          "imagem_destaque": j["img"],
                                          "peso_destaque": j["peso"]}

                    evento['destaque']['imagem_destaque'] = \
                    portal.getUrlByFile(evento['destaque']['imagem_destaque'],
                                        id_site=self.id_site)

                lista.append(evento)

        #verifica se a data é a atual e coloca da um set no "ate"
        if(date_limit):

            date_limit = date_limit

        else:

            date_limit = date

        #monta a paginação
        if titulo!='todos' and date !='todas':

            cont = list(self.execSql("select_eventos_by_calendar_title_count",
                                     date=str(date),
                                     titulo=titulo))

        if titulo=='todos' and date !='todas':

            cont = list(self.execSql(select_count,
                                     date = str(date)))

        if titulo !='todos' and date=='todas':

            cont = list(self.execSql("select_more_eventos_by_titulo_count",
                        titulo = titulo))

        num = cont[0].get("count")

        if num>limit:

            result = (num /float(limit))
            result = math.ceil(result)

        else:

            result = 1

        x = ""

        for x in range(int(result)):

            paginas = {}
            pagina_int = x+1
            pagina = str(pagina_int)
            paginas["pagina"]=pagina
            lista.append(paginas)

        #transforma os dados em string pra retornar na lista
        if titulo != 'todos' and date != 'todas':

            cabecalho_lista = {"paginas":result,
                               "total":num}
            lista.append(cabecalho_lista)
            return lista

        if titulo == 'todos' and date != 'todas':

            p = strptime(date, "%Y-%m-%d")
            dated = strftime("%d/%m/%Y", p)
            date = str(dated)
            result = str(result)
            num = str(num)
            #total_eventos= list(self.execSql("select_count_eventos"))
            #total = total_eventos[0].get("count")
            #ultima_data= list(self.execSql("select_ultima_data",
            #                               ultima_date = int(total-1)))
            #date_down= ultima_data[0].get("data_inicio")
            #o = strptime(date_down, "%Y-%m-%d %H:%M:%S")
            #dateli = strftime("%d/%m/%Y", o)
            #date_limit = str(dateli)
            cabecalho_lista = {"paginas":result,
                               "de":date,
                               "total":num}

            lista.append(cabecalho_lista)
            return lista

        if titulo != 'todos' and date == 'todas':

            cabecalho_lista = {"paginas":result,
                               "total":num}
            lista.append(cabecalho_lista)
            return lista

    @jsoncallback
    @dbconnectionapp
    def getMoreEventosNew(self, categoria=None, data1=None, data2=None, titulo=None, limit=20, num=1):
        """
        returns more events
        """
        titulo = titulo.decode('utf-8').encode('latin-1')
        if not categoria and not data1 and not data2 and not titulo:
            return "Os dados de busca não foram preenchidos."
        limit = int(limit)
        num = int(num)
        de = (num-1) * limit
        ate = limit
        portal = Portal(id_site=self.id_site,
                        request=self.request)

        if data1:
            try:
                data1 = data1+" 00:00"
                dt1 = strptime(data1, "%d/%m/%Y %H:%M")
                data1 = strftime("%Y-%m-%d %H:%M", dt1)
            except ValueError, e:
                return "Data informada em formato inválido"

        if data2:
            try:
                data2 = data2+" 00:00"
                dt2 = strptime(data2, "%d/%m/%Y %H:%M")
                data2 = strftime("%Y-%m-%d %H:%M", dt2)
            except ValueError, e:
                return "Data informada em formato inválido"

        todos_os_eventos = []
        cont = [{"count":0}]
        # se tiver categoria
        #1
        if categoria and not data1 and not data2 and not titulo:
            todos_os_eventos = self.execSql("select_eventos_by_categoria",
                                            categoria=int(categoria),
                                            de=de,
                                            ate=ate)
            cont = list(self.execSql("select_eventos_by_categoria_count",
                                     categoria=int(categoria)))
        #2
        elif categoria and data1 and not data2 and not titulo:
            todos_os_eventos = self.execSql("select_eventos_by_categoria_data1",
                                            categoria=int(categoria),
                                            data1=data1,
                                            de=de,
                                            ate=ate)
            cont = list(self.execSql("select_eventos_by_categoria_data1_count",
                                     categoria=int(categoria),
                                     data1=data1))
        #3
        elif categoria and data1 and data2 and not titulo:
            todos_os_eventos = self.execSql("select_eventos_by_categoria_data1_2",
                                            categoria=int(categoria),
                                            data1=data1,
                                            data2=data2,
                                            de=de,
                                            ate=ate)
            cont = list(self.execSql("select_eventos_by_categoria_data1_2_count",
                                     categoria=int(categoria),
                                     data1=data1,
                                     data2=data2))
        #4
        elif categoria and data1 and data2 and titulo:
            todos_os_eventos = self.execSql("select_eventos_by_categoria_data1_2_titulo",
                                            categoria=int(categoria),
                                            data1=data1,
                                            data2=data2,
                                            titulo=titulo,
                                            de=de,
                                            ate=ate)
            cont = list(self.execSql("select_eventos_by_categoria_data1_2_titulo_count",
                                     categoria=int(categoria),
                                     data1=data1,
                                     data2=data2,
                                     titulo=titulo))
        #5
        elif categoria and not data1 and data2 and titulo:
            todos_os_eventos = self.execSql("select_eventos_by_categoria_data2_titulo",
                                            categoria=int(categoria),
                                            data2=data2,
                                            titulo=titulo,
                                            de=de,
                                            ate=ate)
            cont = list(self.execSql("select_eventos_by_categoria_data2_titulo_count",
                                     categoria=int(categoria),
                                     data2=data2,
                                     titulo=titulo))
        #5.1
        elif categoria and data1 and not data2 and titulo:
            todos_os_eventos = self.execSql("select_eventos_by_categoria_data1_titulo",
                                            categoria=int(categoria),
                                            data1=data1,
                                            titulo=titulo,
                                            de=de,
                                            ate=ate)
            cont = list(self.execSql("select_eventos_by_categoria_data1_titulo_count",
                                     categoria=int(categoria),
                                     data1=data1,
                                     titulo=titulo))
        #6
        elif categoria and not data1 and data2 and not titulo:
            todos_os_eventos = self.execSql("select_eventos_by_categoria_data2",
                                            categoria=int(categoria),
                                            data2=data2,
                                            de=de,
                                            ate=ate)
            cont = list(self.execSql("select_eventos_by_categoria_data2_count",
                                     categoria=int(categoria),
                                     data2=data2))
        #7
        elif categoria and not data1 and not data2 and titulo:
            todos_os_eventos = self.execSql("select_eventos_by_categoria_titulo",
                                            categoria=int(categoria),
                                            titulo=titulo,
                                            de=de,
                                            ate=ate)
            cont = list(self.execSql("select_eventos_by_categoria_titulo_count",
                                     categoria=int(categoria),
                                     titulo=titulo))

        # se não tiver categoria
        #8
        elif not categoria and not data1 and data2 and not titulo:
            todos_os_eventos = self.execSql("select_eventos_by_data2",
                                            data2=data2,
                                            de=de,
                                            ate=ate)
            cont = list(self.execSql("select_eventos_by_data2_count",
                                     data2=data2))
        #9
        if not categoria and data1 and not data2 and not titulo:
            todos_os_eventos = self.execSql("select_eventos_by_data1",
                                            data1=data1,
                                            de=de,
                                            ate=ate)
            cont = list(self.execSql("select_eventos_by_data1_count",
                                     data1=data1))
        #10
        if not categoria and data1 and data2 and not titulo:
            todos_os_eventos = self.execSql("select_eventos_by_data1_2",
                                            data1=data1,
                                            data2=data2,
                                            de=de,
                                            ate=ate)
            cont = list(self.execSql("select_eventos_by_data1_2_count",
                                     data1=data1,
                                     data2=data2))
        #11
        elif not categoria and data1 and data2 and titulo:
            todos_os_eventos = self.execSql("select_eventos_by_data1_2_titulo",
                                            data1=data1,
                                            data2=data2,
                                            titulo=titulo,
                                            de=de,
                                            ate=ate)
            cont = list(self.execSql("select_eventos_by_data1_2_titulo_count",
                                     data1=data1,
                                     data2=data2,
                                     titulo=titulo))
        #12
        elif not categoria and not data1 and data2 and titulo:
            todos_os_eventos = self.execSql("select_eventos_by_data2_titulo",
                                            data2=data2,
                                            titulo=titulo,
                                            de=de,
                                            ate=ate)
            cont = list(self.execSql("select_eventos_by_data2_titulo_count",
                                     data2=data2,
                                     titulo=titulo))
        #13
        elif not categoria and data1 and not data2 and titulo:
            todos_os_eventos = self.execSql("select_eventos_by_data1_titulo",
                                            data1=data1,
                                            titulo=titulo,
                                            de=de,
                                            ate=ate)
            cont = list(self.execSql("select_eventos_by_data1_titulo_count",
                                     data1=data1,
                                     titulo=titulo))

        evento = None
        lista = []

        if not todos_os_eventos:
            todos_os_eventos = []
        for evento in todos_os_eventos:
                
            evento["link"] = \
            portal.getUrlByApp(env_site=self.id_site,
                               schema=self.schema,
                               id_conteudo=evento["id_conteudo"],
                               exportar=1,
                               admin=1)
            p = strptime(evento["data_inicio"], "%Y-%m-%d %H:%M:%S")
            evento["data_inicio"] = strftime("%d/%m/%Y", p)
            evento["categorias"]=[]
            for k in self.execSql("select_categoria_evento", id_conteudo=int(evento['id_conteudo'])):
                categoria = {"id_categoria":k["id_categoria"],
                             "nome_categoria":k["nome_categoria"]}
                evento["categorias"].append(categoria)
            for j in self.execSql("select_destaque",
                                  id_conteudo=evento["id_conteudo"]):

                evento["destaque"] = {"id_destaque": j["id_destaque"],
                                      "titulo_destaque": j["titulo"],
                                      "descricao_destaque": j["descricao"],
                                      "imagem_destaque": j["img"],
                                      "peso_destaque": j["peso"]}
                evento['destaque']['imagem_destaque'] = \
                portal.getUrlByFile(evento['destaque']['imagem_destaque'],
                                    id_site=self.id_site)
            lista.append(evento)

        #monta a paginação
        num = cont[0].get("count")

        if num>limit:

            result = (num /float(limit))
            result = math.ceil(result)

        else:

            result = 1

        x = ""

        for x in range(int(result)):

            paginas = {}
            pagina_int = x+1
            pagina = str(pagina_int)
            paginas["pagina"]=pagina
            lista.append(paginas)

        #transforma os dados em string pra retornar na lista
        cabecalho_lista = {"paginas":result,
                           "total":num}
        lista.append(cabecalho_lista)
        return lista

    @dbconnectionapp
    def _getEventoPublicado(self,id_evento):
        """
        returns published event
        """

        evento = None
        evento = self.execSql("select_evento_publicado",
                              id_evento=int(id_evento))
        if evento:

            evento = list(evento)[0]
            evento["categorias"]=[]
            for k in self.execSql("select_categoria_evento", id_conteudo=int(evento['id_conteudo'])):
                categoria = {"id_categoria":k["id_categoria"],
                             "nome_categoria":k["nome_categoria"]}
                evento["categorias"].append(categoria)
            for j in self.execSql("select_destaque",
                                  id_conteudo=evento["id_conteudo"]):
                
                evento["destaque"] = {"id_destaque": j["id_destaque"],
                                      "titulo_destaque": j["titulo"],
                                      "descricao_destaque": j["descricao"],
                                      "imagem_destaque": j["img"],
                                      "peso_destaque": j["peso"]}

        return evento

    @dbconnectionapp
    def paginator(self):

        cont = list(self.execSql("select_count_eventos"))
        num = cont[0].get("count")

        if num>10:

            result = (num /10)

        else:

            result = 1

        return result
