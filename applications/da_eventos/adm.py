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
from time import time, strftime, strptime
from datetime import datetime, timedelta
from urllib import unquote
from publica.admin.file import File
from publica.admin.error import UserError
from publica.core.portal import Portal
from publica.utils.json import encode, decode
from publica.utils.decorators import serialize, dbconnectionapp,\
                                     Permission
import base64
class Adm(object):
    """
    """


    def _getDadosApp(self):
        """
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        return portal._getApp(env_site=self.id_site,
                               schema=self.schema)["dados"]    
   
    @dbconnectionapp
    def _getEventos(self, id_post):
        """
        """
        for i in self.execSql("select_todos_eventos",
                              id_post=int(id_post)):
            return i

    @dbconnectionapp
    def _getIds(self):
        """
        retorna os ids dos eventos que estão agendados
        """
        date = (datetime.now() - timedelta(minutes=5)).timetuple()
        publicado_em = strftime("%Y-%m-%d %H:%M", date)
        return self.execSql("select_ids_agendados",
                            publicado_em=publicado_em)


    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def addConteudo(self, id_site, id_treeapp, id_aplicativo,
                    titulo, preco_entrada, consumacao_minima, local, site,
                    categoria, credito_imagem, data_inicio, usuario, email_user, 
                    imagemint, publicado_em, 
                    data_fim=None, telefones=None, email=None,
                    expira_em=None, publicado=None,
                    hora_inicio=None, hora_fim=None,
                    titulo_destaque=None, descricao_destaque=None,
                    imagem_destaque=None, peso_destaque=None,
                    relacionamento=[], tags="", permissao=None,
                    exportar_xml=None, exportar_json=None,
                    exportar=None):
        """
        """
        dadosapp = self._getDadosApp()
        publicado = True if publicado else False
        tags = tags if tags else None
        dt = publicado_em
        try:
            p = strptime(publicado_em, "%d/%m/%Y %H:%M")
            dt2 = strftime("%d/%m/%Y %H:%M", p)
            publicado_em = strftime("%Y-%m-%d %H:%M", p)
        except ValueError:
            dt2 = None
            raise UserError(("Ocorreu um erro: "
                             "Data de publica&ccedil;&aring;o "
                             "inv&aacute;lida (%s)") % publicado_em)

        try:
            p = strptime(data_inicio, "%d/%m/%Y")
            data_inicio = strftime("%Y-%m-%d %H:%M", p)
        except ValueError:
            return "data em formato incorreto"

        try:
            p = strptime(data_fim, "%d/%m/%Y")
            data_fim = strftime("%Y-%m-%d %H:%M", p)
        except ValueError:
            return "data em formato incorreto"

        try:
            p = strptime(expira_em, "%d/%m/%Y %H:%M")
            expira_em = strftime("%Y-%m-%d %H:%M", p)
        except ValueError:
            expira_em = None

        # inserir conteudo
        portal = Portal(id_site=self.id_site, request=self.request)
        id_conteudo = self.execSql("select_nextval_evento").next()["id"]
        id_imagem = self._addFile(arquivo=imagemint,
                                  id_conteudo=id_conteudo,
                                  schema=self.schema,
                                  dt=dt)
        self.execSqlBatch("insert_evento",
                          id_conteudo=int(id_conteudo),
                          titulo=titulo,
                          imagemint=id_imagem,
                          telefones=telefones,
                          email=email,
                          data_inicio=data_inicio,
                          data_fim=data_fim,
                          hora_inicio=hora_inicio,
                          hora_fim=hora_fim,
                          publicado_em=publicado_em,
                          expira_em=expira_em,
                          credito_imagem=credito_imagem,
                          publicado=publicado,
                          preco_entrada=preco_entrada,
                          consumacao_minima=consumacao_minima,
                          local=local,
                          site=site,
                          usuario=usuario,
                          email_user=email_user)

        if type(categoria) is not list:
            categoria =[categoria]
        for i in range(len(categoria)):
            self.execSqlBatch("insert_categoria_evento",
                              id_categoria=int(categoria[i]),
                              id_conteudo=int(id_conteudo))
        # inserindo os destaques
        if not imagem_destaque:
            imagem_destaque = None

        try:
            peso_destaque = int(peso_destaque)
        except:
            peso_destaque = 0
        dados_destaque = []
        id_destaque = self.execSql("select_nextval_destaque").next()["id"]
        if imagem_destaque:
            imagem_destaque = self._addFile(arquivo=imagem_destaque,
                                            id_conteudo=id_conteudo,
                                            schema=self.schema,
                                            dt=dt)

        self.execSqlBatch("insert_destaque",
                          id_destaque=int(id_destaque),
                          id_conteudo=int(id_conteudo),
                          titulo=titulo,
                          descricao=descricao_destaque,
                          img=imagem_destaque,
                          peso=int(peso_destaque))

        self.execSqlCommit()
        # acoes para o portal
        dados = self._setDados(id_conteudo=id_conteudo)
        self._addContentPortal(env_site=self.id_site,
                               id_pk=id_conteudo,
                               schema=self.schema,
                               meta_type=self.meta_type,
                               id_aplicativo=id_aplicativo,
                               id_treeapp=id_treeapp,
                               peso=peso_destaque,
                               titulo=titulo,
                               publicado=publicado,
                               publicado_em=publicado_em,
                               expira_em=expira_em,
                               titulo_destaque=titulo_destaque,
                               descricao_destaque=descricao_destaque,
                               imagem_destaque=imagem_destaque,
                               tags=tags,
                               permissao=permissao,
                               relacionamento=relacionamento,
                               dados=dados)

        if (exportar_xml=='1') or (exportar_json=='1') or (exportar=='1'):
            self._addLog("Novo conteudo cadastrado e publicado '%s'" % titulo)
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

            return ("Conteudo cadastrado com sucesso! "
                    "Publica&ccedil;&atilde;o iniciada.")

        self._addLog("Novo conteudo cadastrada '%s'" % titulo)
        return "Conteudo cadastrado com sucesso."


    @dbconnectionapp
    def getCategorias(self):
        """
            retorna todas categorias
        """
        return self.execSql("select_categorias")

    @dbconnectionapp
    def getCatjson(self):
        """
        """
        return encode([i for i in self.execSql("select_categorias")])

    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def addcategoria(self, nome):
        """
            insert a new categoria

            >>> self.addCategoria(nome=\"name\")
        """
        id_categoria = self.execSql("select_nextval_categoria").next()["id"]
        self.execSqlu("insert_categoria",
                       id_categoria=int(id_categoria),
                       nome_categoria=nome)

        return {"ok":"Categoria adicionada com sucesso!", "id_categoria":id_categoria}

    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def editcategoria(self, nome, id_categoria):

        self.execSqlBatch("update_categoria",
                          nome_categoria= nome,
                          id_categoria=int(id_categoria))
        self.execSqlCommit()

        return {"ok":"categoria editada com sucesso!"}
    
    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def delCategoria(self, id_categoria):

        self.execSqlBatch("delete_categoria",
                          id_categoria=int(id_categoria))
        self.execSqlCommit()

        return {"ok":"ok"}

    @dbconnectionapp
    @Permission("PERM APP")
    def _getConteudo(self, id_conteudo):
        """
        """
        dadosapp = self._getDadosApp()
        for i in self.execSql("select_evento",
                              id_conteudo=int(id_conteudo)):
            p = strptime(i["data_inicio"],"%Y-%m-%d %H:%M:%S")   
            i["data_inicio"] = strftime("%d/%m/%Y", p)
            o = strptime(i["data_fim"],"%Y-%m-%d %H:%M:%S")   
            i["data_fim"] = strftime("%d/%m/%Y", o)
            i["categorias"] =[]
            for j in self.execSql("select_destaque", id_conteudo=id_conteudo):
                i["destaque"] = {"id_destaque": j["id_destaque"],
                                 "titulo_destaque": j["titulo"],
                                 "descricao_destaque": j["descricao"],
                                 "imagem_destaque": j["img"],
                                 "peso_destaque": j["peso"]}
            
            for k in self.execSql("select_categoria_evento", id_conteudo=int(id_conteudo)):
                categoria = {"id_categoria":k["id_categoria"],
                             "nome_categoria":k["nome_categoria"]}
                i["categorias"].append(categoria)
   
            for t in self.execSql("select_temp_imagem",
                                   id_destaque=int(i["destaque"]["id_destaque"])):
                t["imagem_temp"] = {"id_imagem": t["id_imagem"] if t["id_imagem"] else None,
                                    "tempimg": base64.decodestring(t["imagembin"]) if t["imagembin"] else None,
                                    "type": t["tipoarq"] if t["tipoarq"] else None,
                                    "filename": t["nomearq"] if t["nomearq"] else None}

                class FakeReader(object):

                    def __init__(self, source):
                        self.source = source

                    def read(self):
                        return self.source

                class FakeFile(object):
                    """Cria um objeto com atributos de um arquivo enviado por wsgi"""

                    def __init__(self, source, mimetype, filename):
                        self.type = mimetype
                        self.filename = filename
                        self.file = FakeReader(source)

                if (t["imagem_temp"]["tempimg"]):
                    arq = File(request=self.request, id_site=self.id_site)
                    filesource = t["imagem_temp"]["tempimg"]
                    filenome = t["imagem_temp"]["filename"]
                    filetype = t["imagem_temp"]["type"]
                    filenomeint = "i" + t["imagem_temp"]["filename"]
                    fakefile = FakeFile(filesource, filetype, filenome)
                    fakefileint = FakeFile(filesource, filetype, filenome)
                    arquivo = arq.addFileTemp(arquivo=fakefile)
                    arquivoint = arq.addFileTemp(arquivo=fakefileint)
                    cont = self._addFile(arquivo=decode(arquivo)["id"],
                                         id_conteudo=id_conteudo,
                                         schema=self.schema,
                                         dt=i["publicado_em"],
                                         transform={"metodo":dadosapp['redimensionamento'],
                                                    "dimenx":dadosapp['dimenx'],
                                                    "dimeny":dadosapp['dimeny']})
                    cont2 = self._addFile(arquivo=decode(arquivoint)["id"],
                                          id_conteudo=id_conteudo,
                                          schema=self.schema,
                                          dt=i["publicado_em"],
                                          transform={"metodo":dadosapp['redimensionamentog'],
                                                     "dimenx":dadosapp['dimenxg'],
                                                     "dimeny":dadosapp['dimenyg']})
                    i["destaque"]["imagem_destaque"] = cont
                    i["imagemint"] = cont2                   
                    self.execSqlBatch("update_imagem",
                                       id_conteudo=int(id_conteudo),
                                       imagemint=cont2)
                    self.execSqlBatch("update_destaque",
                                      id_destaque=i["destaque"]["id_destaque"],
                                      img=cont)
                    self.execSqlBatch("delete_tempimg",
                                       id_destaque=i["destaque"]["id_destaque"])
                    self.execSqlCommit()
            return i




    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def editConteudo(self, id_conteudo, id_site, id_treeapp, id_aplicativo,
                          titulo, preco_entrada,consumacao_minima,local,site,
                          categoria, credito_imagem, data_inicio,
                          usuario, email_user, imagemint,
                          publicado_em, data_fim = None,telefones=None, email=None, 
                          expira_em=None, publicado=None, hora_inicio=None,
                          titulo_destaque=None, descricao_destaque=None,
                          imagem_destaque=None, peso_destaque=None,
                          relacionamento=[], tags="", permissao=None,
                          exportar_xml=None, exportar_json=None,
                          exportar=None, hora_fim=None):
        """
        """
        publicado = True if publicado else False
        tags = tags if tags else None
        portal = Portal(id_site=self.id_site, request=self.request)
        dt = publicado_em
        try:
            p = strptime(publicado_em, "%d/%m/%Y %H:%M")
            dt2 = strftime("%d/%m/%Y %H:%M", p)
            publicado_em = strftime("%Y-%m-%d %H:%M", p)
        except ValueError, e:
            dt2 = None
            raise UserError(("Ocorreu um erro: "
                             "Data de publica&ccedil;&aring;o "
                             "inv&aacute;lida (%s)") % publicado_em)

        try:
            p = strptime(data_inicio, "%d/%m/%Y")
            data_inicio = strftime("%Y-%m-%d %H:%M", p)
        except ValueError, e:
            return "data em formato incorreto"

        try:
            p = strptime(data_fim, "%d/%m/%Y")
            data_fim = strftime("%Y-%m-%d %H:%M", p)
        except ValueError, e:
            return "data em formato incorreto"

        try:
            p = strptime(expira_em, "%d/%m/%Y %H:%M")
            expira_em = strftime("%Y-%m-%d %H:%M", p)
        except ValueError, e:
           expira_em = None

        id_imagem = portal.addArquivo(arquivo=imagemint,
                                      id_conteudo=id_conteudo,
                                      schema=self.schema,
                                      dt=dt)
        # deletar conteudo tabela destaques ou outras tabelas
        self.execSqlBatch("delete_destaque",
                          id_conteudo=int(id_conteudo))
        self.execSqlBatch("delete_categoria_evento",
                           id_conteudo=int(id_conteudo))
        if type(categoria) is not list:
            categoria =[categoria]
        for i in range(len(categoria)):
            self.execSqlBatch("insert_categoria_evento",
                             id_categoria=int(categoria[i]),
                             id_conteudo=int(id_conteudo))
        if imagem_destaque:
            if type(imagem_destaque) is str:
                try:
                    imagem_destaque.index("tmp")
                    arquivo = imagem_destaque
                    cont = self._addFile(arquivo = arquivo,
                                 id_conteudo=id_conteudo,
                                 schema=self.schema,
                                 dt=dt2)

                except:
                    cont = imagem_destaque
            else:
                arq = File(request={}, id_site=self.id_site)
                arquivo = arq.addFileTemp(arquivo=imagem_destaque)
                cont = self._addFile(arquivo=decode(arquivo)["id"],
                                 id_conteudo=id_conteudo,
                                 schema=self.schema,
                                 dt=dt2)
        else:
            cont = None
        self.execSqlBatch("update_evento",
                          id_conteudo=int(id_conteudo),
                          titulo=titulo,
                          imagemint=id_imagem,
                          telefones = telefones,
                          email = email,
                          data_inicio = data_inicio,
                          data_fim = data_fim,
                          hora_inicio = hora_inicio, 
                          hora_fim = hora_fim,
                          publicado_em=publicado_em,
                          expira_em=expira_em,
                          credito_imagem = credito_imagem,
                          publicado=publicado,
                          preco_entrada = preco_entrada,
                          consumacao_minima = consumacao_minima,
                          local = local,
                          site = site,
                          usuario = usuario,
                          email_user = email_user)

        # inserindo os destaques
        dados_destaque = []
        id_destaque = self.execSql("select_nextval_destaque").next()["id"]
        self.execSqlBatch("insert_destaque",
                          id_destaque=int(id_destaque),
                          id_conteudo=int(id_conteudo),
                          titulo=titulo,
                          descricao=descricao_destaque,
                          img=cont,
                          peso=int(peso_destaque))


        if titulo_destaque or imagem_destaque or descricao_destaque:
            imagem_destaque = self._addFile(arquivo=imagem_destaque,
                                             id_conteudo=id_conteudo,
                                             schema=self.schema,
                                             dt=dt)
            if not imagem_destaque:
                imagem_destaque = None

            try:
                peso_destaque = int(peso_destaque)
            except:
                peso_destaque = 0



        self.execSqlCommit()
        # acoes para o portal
        dados = self._setDados(id_conteudo=id_conteudo)
        self._editContentPortal(env_site=self.id_site,
                                id_pk=id_conteudo,
                                id_aplicativo=int(id_aplicativo),
                                schema=self.schema,
                                id_treeapp=id_treeapp,
                                peso=peso_destaque,
                                titulo=titulo,
                                publicado=publicado,
                                publicado_em=publicado_em,
                                expira_em=expira_em,
                                titulo_destaque=titulo_destaque,
                                descricao_destaque=descricao_destaque,
                                imagem_destaque=cont,
                                permissao=permissao,
                                tags=tags,
                                relacionamento=relacionamento,
                                dados=dados)

        if (exportar_xml=='1') or (exportar_json=='1') or (exportar=='1'):

            self._addLog("Conteudo '%s' editado e publicado" % titulo)
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

            return ("Conteudo editado com sucesso! "
                    "Publica&ccedil;&atilde;o iniciada.")

        self._addLog("Conteudo editado '%s'" % titulo)
        return "Conteudo editado com sucesso."
