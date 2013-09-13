# coding: utf-8
#
# Copyright 2010 Prima Tech.
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

from urllib import quote
from publica.admin.exchange import getDadosSite
from publica.utils.decorators import serialize, dbconnectionapp, \
                                     Permission, jsoncallback
from publica.core.portal import Portal
from publica.utils.json import encode
from publica.utils import util
from publica.admin.exchange import getDadosSite
from publica.utils.postal import Email
from config import ID_USER

class Site(object):
    """
        Controllers of this app
    """


    @dbconnectionapp
    def _listranking(self, modelo=None, limit=20, offset=0):
        """
            Retorna as avaliacoes ordenadas pelo ranking
        """
        if modelo:
            return self.execSql("select_ranking_geral_modelo",
                                modelo=modelo,
                                limit=int(limit),
                                offset=int(offset))
        else:
            return self.execSql("select_ranking_geral",
                                limit=int(limit),
                                offset=int(offset))


    @dbconnectionapp
    def _getcontent(self, id_conteudo, limit=10, offset=0):
        """
        """
        for i in self.execSql("select_conteudo_site",
                              id_conteudo=int(id_conteudo)):

            return i


    @dbconnectionapp
    def _addavaliacao(self, i, op_design, op_performance, op_conforto,
                            op_dirigibilidade, op_consumo, op_manutencao,
                            op_custo, pontos_positivos, pontos_negativos,
                            comentario, titulo, apelido, recomenda=None):
        """
            Error: 0 - erro generico
                   1 - usuario nao autenticado
                   2 - usuario ja fez avaliacao
        """
        res = {"ok":None, "error":0}
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        dados = portal._getApp(env_site=self.id_site,
                               schema=self.schema)["dados"]

        if dados.get("app_wad", None):

            app_wad = portal._getAplication(id_site=self.id_site,
                                            schema=dados["app_wad"])
            # verifica se o usuario esta logado
            user_data = app_wad._isSessionActive()
            #user_data = {"email":"a@a.com", "nome": "aaaa"}
            #raise Exception("{0}-{1}".format(self.id_site, dados))
            if user_data:

                email = user_data["email"]
                nome = user_data["nome"]
                cpf = ""
                id_wad = -1
                apelido = apelido if apelido else None
                titulo_opiniao = titulo if titulo else None
                hasaval = False
                # verifica se o usuario ja fez a avaliacao
                for i in self.execSql("seleciona_avaliacao_user",
                                      id_conteudo=int(i),
                                      email=email):
                    hasaval = True

                if not hasaval:

                    try:
                        op_design = int(op_design)
                    except Exception:
                        op_design = 0
                    if op_design < 0:
                        op_design = 0
                    if op_design > 10:
                        op_design = 10

                    try:
                        op_performance = int(op_performance)
                    except Exception:
                        op_performance = 0
                    if op_performance > 10:
                        op_performance = 10
                    if op_performance < 0:
                        op_performance = 0

                    try:
                        op_conforto = int(op_conforto)
                    except Exception:
                        op_conforto = 0
                    if op_conforto > 10:
                        op_conforto = 10
                    if op_conforto < 0:
                        op_conforto = 0

                    try:
                        op_dirigibilidade = int(op_dirigibilidade)
                    except Exception:
                        op_dirigibilidade = 0
                    if op_dirigibilidade > 10:
                        op_dirigibilidade = 10
                    if op_dirigibilidade < 0:
                        op_dirigibilidade = 0

                    try:
                        op_consumo = int(op_consumo)
                    except Exception:
                        op_consumo = 0
                    if op_consumo > 10:
                        op_consumo = 10
                    if op_consumo < 0:
                        op_consumo = 0

                    try:
                        op_manutencao = int(op_manutencao)
                    except Exception:
                        op_manutencao = 0
                    if op_manutencao > 10:
                        op_manutencao = 10
                    if op_manutencao < 0:
                        op_manutencao = 0

                    try:
                        op_custo = int(op_custo)
                    except Exception:
                        op_custo = 0
                    if op_custo > 10:
                        op_custo = 10
                    if op_custo < 0:
                        op_custo = 0

                    self.execSqlu("insert_user_avaliacao",
                                  id_conteudo=int(i),
                                  id_wad=id_wad,
                                  nome=nome,
                                  cpf=cpf,
                                  email=email,
                                  apelido=apelido,
                                  titulo_opiniao=titulo_opiniao,
                                  recomenda=True if recomenda else False,
                                  pontos_positivos=pontos_positivos[:1000],
                                  pontos_negativos=pontos_negativos[:1000],
                                  comentario=comentario[:1000],
                                  aval_design=op_design,
                                  aval_performance=op_performance,
                                  aval_conforto_acabamento=op_conforto,
                                  aval_dirigibilidade=op_dirigibilidade,
                                  aval_consumo=op_consumo,
                                  aval_manutencao=op_manutencao,
                                  aval_custo_beneficio=op_custo
                                  )
                    self.execSqlu("update_conteudo_avaliacao",
                                  id_conteudo=int(i),
                                  aval_design=op_design,
                                  aval_performance=op_performance,
                                  aval_conforto_acabamento=op_conforto,
                                  aval_dirigibilidade=op_dirigibilidade,
                                  aval_consumo=op_consumo,
                                  aval_manutencao=op_manutencao,
                                  aval_custo_beneficio=op_custo)
                    # TODO: conta rank
                    self._setRanking()
                    # marca app para publicar
                    # e subitens 

                    res["ok"] = 1

                else:
                    res["error"] = 2

            else:
                res["error"] = 1


        return res


    @dbconnectionapp
    def _getopiniao(self, id_conteudo, limit=10, offset=0, asc=None, desc=None, minor=None):
        """
            Retorna as opinioes de um determinado conteudo
        """
        
        qtde = 0
        for i in self.execSql("select_opiniao_count",
                              id_conteudo=int(id_conteudo)):
            qtde = i["qtde"]
        if asc or desc:
            if asc:
                res = self.execSql("select_opiniao_asc",
                                   id_conteudo=int(id_conteudo),
                                   limit=int(limit),
                                   offset=int(offset))
            else:
                res = self.execSql("select_opiniao_desc",
                                   id_conteudo=int(id_conteudo),
                                   limit=int(limit),
                                   offset=int(offset))
        else:
            if minor:
                res = self.execSql("select_opiniao_minor",
                                   id_conteudo=int(id_conteudo),
                                   limit=int(limit),
                                   offset=int(offset))
            else:
                res = self.execSql("select_opiniao",
                                   id_conteudo=int(id_conteudo),
                                   limit=int(limit),
                                   offset=int(offset))
        return {"qtde":qtde, "res":res}


    # ajax like methods

    @jsoncallback
    def getranking(self, modelo=None, limit=20, offset=0):
        """
            Retorna as avaliações filtrado ou não pelo modelo
        """
        portal = Portal(self.id_site, self.request)
        lr = self._listranking(modelo=modelo, limit=limit, offset=offset)
        res = []
        for i in lr:
            #i["imagem"] = portal.getUrlByFile(source=i["imagem"] )
            i["url"] = portal.getUrlByApp(env_site=self.id_site,
                                          schema=self.schema,
                                          id_conteudo=i["id_conteudo"],
                                          render=True,
                                          admin=1,
                                          exportar=1)
            res.append(i)
        
        return res


    @jsoncallback
    def getopiniao(self, id_conteudo, limit=10, offset=0, asc=None, desc=None, minor=None):
        """
        """
        data = self._getopiniao(id_conteudo=id_conteudo,
                               limit=limit,
                               offset=offset,
                               asc=asc,
                               desc=desc,
                               minor=minor)
        data["res"] = [i for i in data["res"]]
        return data


    @jsoncallback
    def getcontent(self, i):
        """
            Retorna os dados de uma avaliacao serializado como json
            para consultas ajax
        """
        data = self._getcontent(id_conteudo=i)
        if data:

            portal = Portal(id_site=self.id_site,
                            request=self.request)
            dados = portal._getApp(env_site=self.id_site,
                                   schema=self.schema)["dados"]

            app_wad = portal._getAplication(id_site=self.id_site,
                                            schema=dados["app_wad"])
            # verifica se o usuario esta logado
            user_data = app_wad._isSessionActive()
            if user_data:

                data["email"] = user_data["email"]
                data["nome"] = user_data["nome"]

            return data
        return None


    @dbconnectionapp
    def _verify_ext(self, fabricante=None, modelo=None, modelo_ext=None,
                         ano_fabricacao=None, ano_modelo=None, 
                         codigo_fipe=None, hashtree= None):
        i = -1
        if not hashtree:
            return
        self.request["env.usuario"] = {"id_usuario":ID_USER}    
        if fabricante and modelo and modelo_ext and ano_fabricacao and ano_modelo and codigo_fipe:
            try:
                fabricante = fabricante.decode("utf-8").encode("latin1")
                modelo= modelo.decode("utf-8").encode("latin1")
                modelo_ext = modelo_ext.decode("utf-8").encode("latin1")
                ano_fabricacao = ano_fabricacao.decode("utf-8").encode("latin1")
                ano_modelo=ano_modelo.decode("utf-8").encode("latin1")
                codigo_fipe = codigo_fipe.decode("utf-8").encode("latin1")
            except:
                pass
                #didn't encode params from vehicle
            ids = self.execSql("select_id_conteudo",
                                fabricante=fabricante,
                                modelo=modelo,
                                modelo_ext=modelo_ext,
                                ano_fabricacao=ano_fabricacao,
                                ano_modelo=ano_modelo)
            if ids:
                for id in ids:
                    i = id['id_conteudo']
                    break
        dados_f = ''
        if i == -1:
            id_conteudo = self.execSql("select_nextval_conteudo").next()["id"]
            i = id_conteudo
            agora = util.dtnow('%Y-%m-%d %H:%M')
            self.execSqlBatch("insert_conteudo",
                               id_conteudo=id_conteudo,
                               fabricante=fabricante,
                               modelo=modelo,
                               modelo_extendido=modelo_ext,
                               ano_modelo=ano_modelo,
                               ano_fabricacao=ano_fabricacao,
                               titulo=modelo_ext+" - "+ano_fabricacao+"/"+ano_modelo,
                               codigo_fipe=codigo_fipe,
                               ordem=0,
                               aval_design=0.0,
                               aval_performance=0.0,
                               aval_conforto_acabamento=0.0,
                               aval_dirigibilidade=0.0,
                               aval_consumo=0.0,
                               aval_manutencao=0.0,
                               aval_custo_beneficio=0.0,
                               publicado=True,
                               publicado_em=agora,
                               expira_em=None)

            self.execSqlCommit()
            self._setRanking()
            dados = self._setDados(id_conteudo=id_conteudo) 
            dados_f = dados
            portal = Portal(id_site=self.id_site,
                            request=self.request)
            tree = portal._getTreeAppByHash(env_site=self.id_site, hash=hashtree)
            id_tree = tree['id_treeapp']
            dados = self._setDados(id_conteudo=id_conteudo)
            id_aplicativo = portal._getIdAplicativo(env_site=self.id_site, schema=self.schema)
            portal._addConteudo(env_site=self.id_site,
                                id_pk=id_conteudo,
                                schema=self.schema,
                                meta_type=self.meta_type,
                                id_treeapp=id_tree,
                                titulo=modelo_ext+" - "+ano_fabricacao+"/"+ano_modelo,
                                publicado=True,
                                publicado_em=agora,
                                titulo_destaque='',
                                descricao_destaque='',
                                imagem_destaque='',
                                dados=dados,
                                id_aplicativo=id_aplicativo)
            try:
                portal._exportarFormatosConteudo(id_aplicativo=id_aplicativo,
                                                 id_conteudo=id_conteudo,
                                                 schema=self.schema,
                                                 id_treeapp=id_tree,
                                                 html=1,
                                                 dados=dados,
                                                 subitems=None,
                                                 add=1)
            except:
                pass
        else:
            dados_f = self._setDados(id_conteudo=i)
 
        return {'i':i, 'dados':dados_f}


    @dbconnectionapp
    def _delete_opiniao(self, email=None, cpf=None):
        """
        """
        self.execSqlu("delete_opiniao",
                      email=email,
                      cpf=cp)
        
        self.execSqlCommit()
        self._setRanking()
        return {"ok":"Esta opini&atilde;o foi deletada do sistema!"}


    def delete_opiniao(self, email=None, cpf=None):
        """
        """
        return self._delete_opiniao(email=email, 
                                    cpf=cpf)


    def deleteOpById(self, id_opiniao):
        """
        """
        return self._deleteOpById(id_opiniao=id_opiniao)

    @dbconnectionapp
    def _updateMinus(self, i, op_design, op_performance,
                       op_conforto, op_dirigibilidade,
                       op_consumo, op_manutencao, op_custo):

        self.execSqlu("update_conteudo_avaliacao_minus",
                                  id_conteudo=int(i),
                                  aval_design=op_design,
                                  aval_performance=op_performance,
                                  aval_conforto_acabamento=op_conforto,
                                  aval_dirigibilidade=op_dirigibilidade,
                                  aval_consumo=op_consumo,
                                  aval_manutencao=op_manutencao,
                                  aval_custo_beneficio=op_custo)

    @jsoncallback
    @dbconnectionapp
    def verOpById(self, id_opiniao):
        """
        """
        dados = [i for i in self.execSql('select_opiniao_simples',
                                         id_opiniao=int(id_opiniao))]
        try:
            return {'ok':{'comentario':dados[0]['comentario']}, 'error':[]}       
        except:
            return {'ok':{'comentario':'Opini&atilde;o n&atilde;o cadastrada no sistema'}, 'error':[]}
    @jsoncallback
    @dbconnectionapp
    def _deleteOpById(self, id_opiniao):
        """
        """
        dado = [i for i in self.execSql("select_opiniao_conteudo",
                                        id_opiniao=int(id_opiniao))]
        
        try:
            conteudo = dado[0]
            self.execSqlu("delete_opiniao_id",
                          id_opiniao=int(id_opiniao))

            self.execSqlCommit()
            self._updateMinus(i=conteudo['id_conteudo'], 
                              op_design=conteudo['aval_design'],
                              op_performance=conteudo['aval_performance'],
                              op_conforto=conteudo['aval_conforto_acabamento'],
                              op_dirigibilidade=conteudo['aval_dirigibilidade'],
                              op_consumo=conteudo['aval_consumo'],
                              op_manutencao=conteudo['aval_manutencao'],
                              op_custo=conteudo['aval_custo_beneficio'])

            self._setRanking()
            return {"ok":"Esta opini&atilde;o foi deletada do sistema!"}
        except:
            return {"error":["Opini&atilde;o n&atilde;o cadastrada no sistema."]}


    def _sendRemove(self, method_name, to_mail, 
                    host, port, corpo, assunto, from_mail=None, user_mail=None, 
                    user_cpf=None):
        """
        Send mail to get to remove comment
        """
        site = getDadosSite(id_site=self.id_site,
                            request=self.request)
        url = "{0}{1}{2},{3}/{4}?email={5}&cpf={6}".format(site['url_adm'],
                                                           "da_vrumopiniao/",
                                                           self.schema,
                                                           self.id_site,
                                                           method_name,
                                                           user_email,
                                                           user_cpf)

       


        if not from_mail:
            from_mail = to_mail
        email = Email()
        email.enviarEmail(subject=assunto,
                          to=who_mail.encode("latin1"),
                          fro=from_mail,
                          text=corpo.encode("latin1"),
                          returnpath=from_mail,
                          host=host,
                          port=port,
                          type="text/plain")
        return {"ok": "Email com link de remoção enviado"}


    @jsoncallback
    def sendRemove(self, method_name, to_mail,
                   host, port, corpo, assunto, from_mail=None, user_mail=None,
                   user_cpf=None):
        """
        """
        return self._sendRemove(method_name=method_name, 
                                to_mail=to_mail,
                                host=host, 
                                port=port, 
                                corpo=corpo,
                                assunto=assunto, 
                                from_mail=from_mail, 
                                user_mail=user_mail,
                                user_cpf=user_cpf)

    @jsoncallback
    @dbconnectionapp
    def addavaliacao(self, op_design, op_performance, op_conforto,
                           op_dirigibilidade, op_consumo, op_manutencao,
                           op_custo, pontos_positivos, pontos_negativos,
                           comentario, titulo, apelido, i=None, recomenda=None,
                           fabricante=None, modelo=None, modelo_ext=None,
                           ano_fabricacao=None, ano_modelo=None, codigo_fipe=None,
                           hashtree=None):
        """
            Chama metodo para adicionar uma nova avaliacao de um usuario logado.
            Retorna um dicionario, {'ok': ,'erro'}
        """

        r = self._verify_ext(fabricante=fabricante,
                             modelo=modelo, modelo_ext=modelo_ext,
                             ano_fabricacao=ano_fabricacao,
                             ano_modelo=ano_modelo,
                             codigo_fipe=codigo_fipe,
                             hashtree=hashtree)
        i = r['i']

        if not hashtree:
            return {"error":0}
        if i ==" undefined" or i == -1:
            if fabricante and modelo and modelo_ext and ano_fabricacao and ano_modelo:
                try:
                    fabricante = fabricante.decode("utf-8").encode("latin1")
                    modelo= modelo.decode("utf-8").encode("latin1")
                    modelo_ext = modelo_ext.decode("utf-8").encode("latin1")
                    ano_fabricacao = ano_fabricacao.decode("utf-8").encode("latin1")
                    ano_modelo=ano_modelo.decode("utf-8").encode("latin1")
                    codigo_fipe = codigo_fipe.decode("utf-8").encode("latin1")
                except:
                    pass
                    # didn't encode params from vehicle
                ids = self.execSql("select_id_conteudo",
                                    fabricante=fabricante,
                                    modelo=modelo,
                                    modelo_ext=modelo_ext,
                                    ano_fabricacao=ano_fabricacao,
                                    ano_modelo=ano_modelo)
                if ids:
                    for id in ids:
                        i = id['id_conteudo']
                        break
        if not i or i == "undefined" or i == -1:
            return {"error":0}
        avaliacao = self._addavaliacao(i=i,
                                      op_design=op_design,
                                      op_performance=op_performance,
                                      op_conforto=op_conforto,
                                      op_dirigibilidade=op_dirigibilidade,
                                      op_consumo=op_consumo,
                                      op_manutencao=op_manutencao,
                                      op_custo=op_custo,
                                      pontos_positivos=pontos_positivos,
                                      pontos_negativos=pontos_negativos,
                                      comentario=comentario,
                                      titulo=titulo,
                                      apelido=apelido,
                                      recomenda=recomenda)

        if avaliacao['error']:
            return {"avaliacao":avaliacao, "url":0}

        agora = util.dtnow('%Y-%m-%d %H:%M')

        self.request["env_usuario"] = {"id_usuario":ID_USER}
        self.request["env.usuario"] = {"id_usuario":ID_USER}
        portal = Portal(id_site=self.id_site,
                        request=self.request)

        tree = portal._getTreeAppByHash(env_site=self.id_site, hash=hashtree)
        id_tree = tree['id_treeapp']
        self.execSqlCommit()
        self._setRanking()
        dados = r['dados']#self._setDados(id_conteudo=i)
        id_aplicativo = portal._getIdAplicativo(env_site=self.id_site, schema=self.schema)
        """ 
        self.editContent(id_conteudo=i,
                          id_treeapp=id_tree,
                          id_aplicativo=id_aplicativo,
                          publicado_em=str(util.dtnow('%d/%m/%Y %H:%M')),
                          expira_em="",
                          fabricante=fabricante,
                          modelo=modelo,
                          modelo_extendido=modelo_ext,
                          codigo_fipe=codigo_fipe,
                          ano_modelo=ano_modelo,
                          ano_fabricacao=ano_fabricacao,
                          titulo=modelo_ext+" - "+ano_fabricacao+"/"+ano_modelo,
                          ordem=0,
                          publicado=1,
                          exportar=1)
        """
        portal._exportarFormatosConteudo(id_aplicativo=id_aplicativo, 
                            id_conteudo=i, 
                            schema=self.schema,
                            id_treeapp=id_tree,
                            html=1,
                            dados=dados,
                            subitems=None, 
                            add=1)

        url = "javascript:void(0)"
        try: 
            url = portal.getUrlByApp(env_site=self.id_site, 
                                     schema=self.schema, 
                                     id_conteudo=i, 
                                     exportar=1,
                                     render=1,
                                     admin=1)
        except:
            pass

        try:
            portal.exportarConteudo(id_tree, [{'id_site_conteudo':self.id_site, \
                                               'id_aplicativo':id_aplicativo, 'schema':self.schema,\
                                               'id_conteudo':i}])
        except Exception, e:
            pass
        return {"avaliacao":avaliacao,"url":url}#dados['url']}
