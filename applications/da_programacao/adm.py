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
from urllib import unquote
from publica.admin.file import File
from publica.admin.error import UserError
from publica.utils.json import encode, decode
from publica.core.portal import Portal
from publica.utils.decorators import serialize, jsoncallback, dbconnectionapp,\
                                     Permission
from datetime import timedelta, datetime


class Adm(object):
    """
    """
    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def addConteudo(self, id_site, id_treeapp, id_aplicativo,
                          titulo, descricao, data, publicado_em,
                          expira_em=None, publicado=None, titulo_destaque=None,
                          descricao_destaque=None, imagem_destaque=None,
                          peso_destaque=None, relacionamento=[], tags="",
                          permissao=None, exportar_xml=None,
                          exportar_json=None, exportar=None):
        """inseri dados na tabela conteudo criando a programação semanal"""
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
            p = strptime(data, "%d/%m/%Y")
            data = strftime("%Y-%m-%d", p)
        except ValueError, e:
            raise UserError(("Ocorreu um erro: "
                             "Data de publica&ccedil;&aring;o "
                             "inv&aacute;lida (%s)") % data)
        # inserir conteudo
        select_nexval = "select_nextval_programa_diaria"
        id_conteudo = self.execSql(select_nexval).next()["id"]

        self.execSqlBatch("insert_conteudo",
                          id_conteudo=id_conteudo,
                          titulo=titulo,
                          data=data,
                          descricao=descricao,
                          publicado_em=publicado_em,
                          expira_em=expira_em,
                          publicado=True)

        # inserindo os destaques
        dados_destaque = []
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

            self.execSqlBatch("insert_destaque",
                              id_conteudo=id_conteudo,
                              titulo=titulo_destaque,
                              descricao=descricao_destaque,
                              img=imagem_destaque,
                              peso=peso_destaque)

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

        if exportar_xml or exportar_json or exportar:

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
    @jsoncallback
    def delprograma_vinculado(self, id_programa_programacao_diaria):
        """Deleta os arquivos vinculados a programação diaria,
        o delete acontece na tabela derivada "programa_programacao_diaria" """

        self.execSqlBatch("del_programa_vinculado",
        id_programa_programacao_diaria=int(id_programa_programacao_diaria))

        self.execSqlCommit()
        return "item deletado com sucesso"

    @dbconnectionapp
    @jsoncallback
    def delsecao(self, id_secao):
        """deleta a seção selecionada"""

        self.execSqlBatch("del_secao",
        id_secao=int(id_secao))

        self.execSqlCommit()
        return {"msg": "seção deletado com sucesso"}

    @dbconnectionapp
    @jsoncallback
    def delprograma(self, id_programa, confere=None):
        """confere viculo do programa com outras tabelas atraves do
        id_programa, caso não exista deleta o programa cadastrados
        na tabela programas"""
        if confere:
            vinculo = list(self.execSql("search_vinculo",
                           id_programa=int(id_programa)))
            if(len(vinculo) > 0):
                return {"ok":"2"}
            else:
                return {"ok":"1"} 
        else:
            self.execSqlBatch("del_programa", id_programa=int(id_programa))
            self.execSqlCommit()
            return {"ok":"item deletado com sucesso"}


    @dbconnectionapp
    @Permission("PERM APP")
    def _getConteudo(self, id_conteudo):
        """
        """
        for i in self.execSql("select_conteudo",
                              id_conteudo=int(id_conteudo)):
            return i

    def _getDates(dados):
        res = {}
        for i in dados:
            if not res.get(i['data']):
                res[i['data']] = i['url']
        return res

    def _getdate(self):
        import time
        return time.strftime('%d'), time.strftime('%m'), time.strftime('%Y')

    @dbconnectionapp
    def _getProgramasById_Conteudo(self, id_conteudo):
        """ busca todos programas vinculados a tabela programação diaria """

        return self.execSql("select_programas_id_conteudo",
                    id_programacao_diaria=int(id_conteudo))
    
    @dbconnectionapp
    @jsoncallback
    def verData(self, dt=[]):
        """
            verifica se ja existe a data para mudar a class
        """
        res = []
        for i in range(len(dt)):
            p = strptime(dt[i], "%d/%m/%Y")
            data = strftime("%Y-%m-%d", p)
            conteudo = [j["id_conteudo"] for j in self.execSql("select_conteudo_date", dt=str(data))]
            if conteudo:
                resp = True 
            else:
                resp = False
            res.append(resp)
        return {"ok":res}
            
                
    
    @dbconnectionapp
    def get_unit_programa_vinculado(self, id_conteudo):
        """Buscar um unico programa vinculado para ser editado """

        return self.execSql("select_unit_programa_programacao_diaria",
                            id_programa_programacao_diaria=int(id_conteudo))

    @dbconnectionapp
    def get_unit_secao(self, id_secao):
        """Buscar uma unica seção para ser editada """

        return self.execSql("select_unit_secao",
                    id_secao=int(id_secao))

    @dbconnectionapp
    def get_unit_programa(self, id_programa):
        """busca um unico programa para ser editado"""

        return self.execSql("select_unit_programa",
                    id_programa=int(id_programa))


    @dbconnectionapp
    def compareProgramacao(self, hora_inicio, hora_fim, data,
                           id_programa_programacao_diaria=None, extend=None):
        """
            compara se existe progamação já no horario
        """
        hour_fim = timedelta(hours=int(hora_fim[:2]), minutes=int(hora_fim[3: ]))
        hour_fim = str(hour_fim - timedelta(minutes=1)).replace("-1 day, ", "")
        hour_start = timedelta(hours=int(hora_inicio[:2]), minutes=int(hora_inicio[3: ]))
        hour_start = str(hour_start + timedelta(minutes=1)).replace("-1 day, ", "")
        result = []
        if extend:
            for i in range(len(extend)):
                data = list(self.get_unit_programa_vinculado(extend[i]))[0]['data']
                compare = list(self.execSql("select_compare_hour_edit",
                                            id_programa_programacao_diaria=int(extend[i]),
                                            data=data,
                                            hora_inicio=hour_start,
                                            hora_fim=hour_fim))[0]['count']
                if int(compare):                    
                    result.append(data)
            return result
        else:
            compare = list(self.execSql("select_compare_hour_edit",
                                         id_programa_programacao_diaria=int(id_programa_programacao_diaria),
                                         data=data,
                                         hora_inicio=hour_start,
                                         hora_fim=hour_fim))[0]['count'] 
            return compare     

    @jsoncallback
    @dbconnectionapp
    def editProgramaInProgramacaoDia(self, id_programa, hora_inicio,
                                     id_programacao_diaria, hora_fim,
                                     id_programa_programacao_diaria, data, extend=[]):
        """ recebe parametros para a tabela associativa
        programa_programacao_diaria """                       
        if extend:
            if type(extend) is not list:
                ids = extend 
                extend = []
                extend.append(ids)
            extend.append(id_programa_programacao_diaria)
            compare = self.compareProgramacao(hora_inicio=hora_inicio,
                                              hora_fim=hora_fim,
                                              extend=extend,
                                              data=data)
            if not compare:
                for i in range(len(extend)):
                    self.execSqlBatch("update_full_programa_programacao_diaria",
                                       hora_inicio = hora_inicio,
                                       id_programa_programacao_diaria = int(extend[i]),
                                       hora_fim = hora_fim)
                    retorno = {"msg": """programa editado com sucesso, Todos
                                     os programas que tinham o mesmo horario
                                     anterior e o mesmo titulo assim como titulo 
                                     foram editados.""",
                               "ok":'true'}
                self.execSqlCommit()
            else:
                result=""
                for i in compare:
                    data = strptime(i, "%Y-%m-%d")
                    data = strftime("%d/%m/%Y", data)
                    result += data +",  " 
                retorno = {"error": """As seguintes datas n&atilde;o podem ser replicadas
                                    pois h&aacute; horarios de outra programa&ccedil;&atilde;o
                                    nesse intervalo:    """+result}
        else:
            compare = self.compareProgramacao(hora_inicio=hora_inicio,
                                              hora_fim=hora_fim,
                                              id_programa_programacao_diaria=id_programa_programacao_diaria,
                                              data=data)
            if not int(compare):
                self.execSqlBatch("update_programa_programacao_diaria",
                                   id_programa=int(id_programa),
                                   id_programacao_diaria=int(id_programacao_diaria),
                                   hora_inicio=hora_inicio,
                                   hora_fim=hora_fim,
                                   id_programa_programacao_diaria=int(
                                               id_programa_programacao_diaria))
                
                retorno = {"msg": 'programa editado com sucesso',
                           "id": id_programacao_diaria,
                           "ok":'true'}
                self.execSqlCommit()
            else:
                retorno = {"error": 'j&aacute; existe programa nesse intervalo de horario'}

        return retorno

    @jsoncallback
    @dbconnectionapp
    def editsecao(self, id_secao, nome):
        """ edita a tabla secao onde o id sera igual a id_secao """

        self.execSqlBatch("update_secao",
                          id_secao=int(id_secao),
                          nome=nome)

        self.execSqlCommit()
        retorno = {"msg": "seção editada com sucesso",
                    "id": id_secao}
        return retorno

    @jsoncallback
    @dbconnectionapp
    @Permission("PERM APP")
    def clonardata(self, data_txt, data_para_txt, data_para, data_de, id_aplicativo, id_treeapp):
        """ clona a data enviadas por parametro """

        data_txt_list = type(data_txt) is list
        data_para_list = type(data_para_txt) is list
        publicado_em = None
        from datetime import datetime, date, time
        today = datetime.now()
        publicado_em = today.strftime("%Y-%m-%d %H:%M")
        dt = str(today.date())
        if(data_para_list):          
            cont = 0
            data_inicio = 0
            if(len(data_txt)>5):
                data_inicio_date = date(int(data_de[0][6:10]),
                                        int(data_de[0][3:5]),
                                        int(data_de[0][0:2]))

                data_inicio = str(data_inicio_date.weekday())
                for x in range(13):
                    data_corrente_date = date(int(data_para[x][6:10]), 
                                              int(data_para[x][3:5]), 
                                              int(data_para[x][0:2]))
                    data_corrente = str(data_corrente_date.weekday())
                    if(data_corrente == data_inicio):
                        data_inicio = int(x)
                        break

            for cont in range(data_inicio,len(data_para_txt)):

                dados_data= []
                dados_data = list(self.execSql("select_clone_programas",
                                       titulo=data_txt[cont]))
                p = strptime(data_para[cont], "%d/%m/%Y")
                data = strftime("%Y-%m-%d", p)
                select_nexval = "select_nextval_programa_diaria"
                id_conteudo = self.execSql(select_nexval).next()["id"]
                msg = ""
                if(data_de[cont] != None):
                    msg = "copiado do dia  " + str(data_de[cont])

                self.execSqlBatch("insert_conteudo",
                                    id_conteudo=id_conteudo,
                                    titulo=data_para_txt[cont],
                                    data=str(data),
                                    descricao=msg,
                                    publicado_em=publicado_em,
                                    expira_em=None,
                                    publicado=True)
                self.execSqlCommit()
                dados = self._setDados(id_conteudo=id_conteudo)
                self._addContentPortal(env_site=self.id_site,
                                        id_pk=id_conteudo,
                                        schema=self.schema,
                                        meta_type=self.meta_type,
                                        id_aplicativo=id_aplicativo,
                                        id_treeapp=id_treeapp,
                                        peso=None,
                                        titulo=data_para_txt[cont],
                                        publicado=True,
                                        publicado_em=publicado_em,
                                        expira_em=None,
                                        titulo_destaque=None,
                                        descricao_destaque=None,
                                        imagem_destaque=None,
                                        tags=None,
                                        permissao=None,
                                        relacionamento=[],
                                        dados=dados)
                for i in dados_data:
                    nexval = "select_nextval_programa_programacao_diaria"
                    id_programa_programacao_diaria = self.execSql(nexval).next()["id"]
                    self.execSqlu("insert_programa_programacao_dia",
                    id_programa_programacao_diaria=id_programa_programacao_diaria,
                    id_programa=i['id_programa'],
                    id_programacao_diaria=id_conteudo,
                    hora_inicio=i['hora_inicio'],
                    hora_fim=i['hora_fim'],
                    data=str(data))
                    self.execSqlCommit()
        else:
            date = strptime(data_para,"%d/%m/%Y")
            dt = strftime("%Y-%m-%d", date)
            select_nexval = "select_nextval_programa_diaria"
            id_conteudo = self.execSql(select_nexval).next()["id"]

            dados_data = list(self.execSql("select_clone_programas",
                                            titulo=str(data_txt)))

            self.execSqlBatch("insert_conteudo",
                               id_conteudo=id_conteudo,
                               titulo=data_para_txt,
                               data=dt,
                               descricao="copiado do dia " + str(data_de),
                               publicado_em=publicado_em,
                               expira_em=None,
                               publicado=True)
            self.execSqlCommit()

            dados = self._setDados(id_conteudo=id_conteudo)
            self._addContentPortal(env_site=self.id_site,
                                   id_pk=id_conteudo,
                                   schema=self.schema,
                                   meta_type=self.meta_type,
                                   id_aplicativo=id_aplicativo,
                                   id_treeapp=id_treeapp,
                                   peso=None,
                                   titulo=data_para_txt,
                                   publicado=True,
                                   publicado_em=publicado_em,
                                   expira_em=None,
                                   titulo_destaque=None,
                                   descricao_destaque=None,
                                   imagem_destaque=None,
                                   tags=None,
                                   permissao=None,
                                   relacionamento=[],
                                   dados=dados)

            for i in dados_data:
                nexval = "select_nextval_programa_programacao_diaria"
                id_programa_programacao_diaria = self.execSql(nexval).next()["id"]

                self.execSqlu("insert_programa_programacao_dia",
                id_programa_programacao_diaria=id_programa_programacao_diaria,
                id_programa=i['id_programa'],
                id_programacao_diaria=id_conteudo,
                hora_inicio=i['hora_inicio'],
                hora_fim=i['hora_fim'],
                data=dt)

                self.execSqlCommit()
            
        return {'ok':True}

    @jsoncallback
    @dbconnectionapp
    @Permission("PERM APP")
    def editPrograma(self, id_programa, slogan, id_tipo,
                           nome, link=None, imagem=None,
                           imagem_inalterada=None, id_secao=None):
        """ edita a tabela programas """

        from datetime import datetime
        today = datetime.now()
        data = str(today.date())
        p = datetime.now().strftime("%d/%m/%Y %H:%M")
        if(imagem_inalterada):
            imagem = imagem_inalterada
        else:
            portal = Portal(id_site=self.id_site, request=self.request)
            imagem = portal.addArquivo(arquivo=imagem,
                                       id_conteudo=id_programa,
                                       schema=self.schema,
                                       dt=p)

        if id_secao:
            self.execSqlBatch("update_programa",
                              id_programa=int(id_programa),
                              id_tipo=int(id_tipo),
                              id_secao=int(id_secao),
                              link=link,
                              nome=nome,
                              imagem=imagem,
                              slogan=slogan)
        else:
            self.execSqlBatch("update_programa_nsec",
                              id_programa=int(id_programa),
                              id_tipo=int(id_tipo),
                              link=link,
                              nome=nome,
                              imagem=imagem,
                              slogan=slogan)  

        self.execSqlCommit()

        retorno = {"msg": "programa editado com sucesso",
                   "id": id_programa, "ok": True}
        return retorno

    @jsoncallback
    @dbconnectionapp
    def getDateDayProg(self, data, hora_inicio, hora_fim, id_conteudo,
                       id_programa):
        """
            Retorna o dia da semana que possuem programacao
        """
        items = []
        dat = datetime.strptime(data, "%Y-%m-%d")
        dia = str(dat.isoweekday())
        for i in self.execSql("select_full_programa_programacao_diaria",
                               hora_inicio=hora_inicio,
                               hora_fim=hora_fim,
                               id_programa=int(id_programa),
                               dia=dia,
                               id_conteudo=int(id_conteudo),
                               data=data):
            items.append(i)
        return items

    @jsoncallback
    @dbconnectionapp
    def _getProgramaVinculado(self, id_programa_programacao_diaria):
        """ busca todos os programas vinculados a tabela associativa """

        return list(self.execSql("select_programas_vinculado",
                                   id_programa_programacao_diaria=int(
                                         id_programa_programacao_diaria)))

    @jsoncallback
    @dbconnectionapp
    @Permission("PERM APP")
    def addProgramaInProgramacaoDia(self, id_programa, id_programacao_diaria,
                                    hora_inicio, hora_fim, data=None):
        """adiciona uma Fk da tabela programas, e da tabela programacao_diaria
        na tabela associativa programa_programacao_diaria"""
        if(data == None):
            from datetime import datetime
            today = datetime.now()
            data = str(today.date())
        else:
            p = strptime(data, "%d/%m/%Y")
            data = strftime("%Y-%m-%d", p)
        hour_fim = timedelta(hours=int(hora_fim[:2]), minutes=int(hora_fim[3: ]))
        hour_end = hour_fim - timedelta(minutes=1)
        hour_end = str(hour_end).replace('-1 day, ', '')
        hour_start = timedelta(hours=int(hora_inicio[:2]), minutes=int(hora_inicio[3: ]))
        hour_start = hour_start + timedelta(minutes=1)
        hour_start = str(hour_start).replace('-1 day, ', '')
        compare = list(self.execSql("select_compare_hour",
                                     data=data,
                                     hora_inicio=str(hour_start),
                                     hora_fim=str(hour_end)))[0]['count']
        if not int(compare):  
            nexval = "select_nextval_programa_programacao_diaria"
            id_programa_programacao_diaria = self.execSql(nexval).next()["id"]
            self.execSqlu("insert_programa_programacao_dia",
                          id_programa_programacao_diaria=id_programa_programacao_diaria,
                          id_programa=int(id_programa),
                          id_programacao_diaria=int(id_programacao_diaria),
                          hora_inicio=hora_inicio,
                          hora_fim=hora_fim,
                          data=data)

            self.execSqlCommit()
            retorno = {"msg": 'programa inserido com sucesso',
                       "id": id_programacao_diaria, "ok":'true'}
        else:
            retorno = {"error": 'j&aacute; existe programa nesse intervalo de horario'}
        return retorno

    @jsoncallback
    @dbconnectionapp
    def addSecao(self, nome):
        """Adiciona um item na tabela Secao"""

        nexval = "select_nextval_secao"
        id_secao = self.execSql(nexval).next()["id"]

        self.execSqlu("insert_secao", nome=nome,
                       id_secao= id_secao)

        self.execSqlCommit()
        retorno = {"msg": "seção inserida com sucesso",
                   "id": id_secao}
        return retorno

    @dbconnectionapp
    def getProgramas(self):
        """ busca todos os programas cadastrados para popular o combo-box """

        return list(self.execSql("select_programas"))

    @dbconnectionapp
    def getSecaos(self):
        """ busca todos as seções cadastrados para popular o combo-box """

        return list(self.execSql("select_secaos"))

    @jsoncallback
    @dbconnectionapp
    def getSessoes(self):
        """ busca todos as seções cadastrados para popular o combo-box """

        return list(self.execSql("select_secaos"))

    @dbconnectionapp
    def getTipos(self):
        """ busca todos os tipos cadastrados para popular o combo-box """

        return list(self.execSql("select_tipos"))

    @dbconnectionapp
    @jsoncallback
    @Permission("PERM APP")
    def addPrograma(self, id_tipo, nome, imagem,
                    slogan=None, link = None, descricao=None, data=None, id_secao=None):
        """adiciona dados na tabela programa"""
        from datetime import datetime
        today = datetime.now()
        data = str(today.date())
        p = datetime.now().strftime("%d/%m/%Y %H:%M")
        portal = Portal(id_site=self.id_site, request=self.request)
        id_programa = self.execSql("select_nextval_programa").next()["id"]
        imagem = portal.addArquivo(arquivo=imagem,
                                   id_conteudo=id_programa,
                                   schema=self.schema,
                                   dt=p)
        if id_secao:
            self.execSqlu("insert_programa",
                          nome=nome,
                          id_secao=int(id_secao),
                          id_tipo=int(id_tipo),
                          link=link,
                          imagem=imagem,
                          slogan=slogan,
                          descricao=descricao,
                          data=data)
        else:
            self.execSqlu("insert_programa_nsec",
                          nome=nome,
                          id_tipo=int(id_tipo),
                          link=link,
                          imagem=imagem,
                          slogan=slogan,
                          descricao=descricao,
                          data=data)

        self.execSqlCommit()
        retorno = {"msg": 'Programa inserido com sucesso!',
                   "id_programa": id_programa, "nome": nome, "ok": 'true'}
        return retorno

    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def editConteudo(self, id_conteudo, id_site, id_treeapp, id_aplicativo,
                          titulo, data, publicado_em,
                          descricao=None,expira_em=None, publicado=None,
                          titulo_destaque=None, descricao_destaque=None,
                          imagem_destaque=None, peso_destaque=None,
                          relacionamento=[], tags="", permissao=None,
                          exportar_xml=None, exportar_json=None,
                          exportar=None):
        """
        """
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
            p = strptime(data, "%d/%m/%Y")
            data = strftime("%Y-%m-%d", p)
        except ValueError, e:
            raise UserError(("Ocorreu um erro: "
                             "Data de publica&ccedil;&aring;o "
                             "inv&aacute;lida (%s)") % data)

        # deletar conteudo tabela destaques ou outras tabelas
        programas_vinculados = list(self._getProgramasById_Conteudo(id_conteudo))
        if programas_vinculados:
            for i in programas_vinculados:
                self.execSqlu("update_programa_programacao_diaria_date",
                              id_programa_programacao_diaria=int(i["id_programa_programacao_diaria"]),
                              data=data)
                
        self.execSqlBatch("update_conteudo",
                          id_conteudo=int(id_conteudo),
                          titulo=titulo,
                          data = str(data),
                          descricao=descricao,
                          publicado_em=publicado_em,
                          expira_em=expira_em,
                          publicado=publicado)
        
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
                                imagem_destaque=imagem_destaque,
                                permissao=permissao,
                                tags=tags,
                                relacionamento=relacionamento,
                                dados=dados)

        return ("Conteudo editado com sucesso! "
                    "Publica&ccedil;&atilde;o iniciada.")

        self._addLog("Conteudo editado '%s'" % titulo)
        return "Conteudo editado com sucesso."
