# -* encoding: LATIN1 -*-
#
# Copyright 2009 Prima Tech.
#
# Licensed under the Environ License, Version 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.intip.com.br/licenses/ENVIRON-LICENSE-1.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from datetime import datetime
from os import makedirs, chmod
from time import time, strftime, strptime
from publica.core.portal import Portal
from publica.admin.error import UserError
from publica.utils.decorators import serialize, dbconnectionapp, \
                                     Permission, permissioncron
from site import Site

haslist = True
haslink = True
title = "DA - Ao Vivo"
meta_type = "da_aovivo"
path_base = "/home/superesportes/adhoc/xmls_aovivo/"

class App(Site):
    """
    """
    title = title
    meta_type = meta_type
    haslist = haslist
    haslink = haslink
    path_base = path_base


    def __init__(self, id_site, schema=None, request=None):
        """
        """
        self.id_site = id_site
        self.schema = schema
        self.request = request


    @dbconnectionapp
    def _install(self, title,
                       rss_titulo=None, rss_link=None, rss_descricao=None,
                       rss_idioma=None, rss_categoria=None, rss_copyright=None,
                       rss_imagem_titulo=None, rss_imagem_link=None,
                       rss_imagem=None):
        """Adiciona uma instancia do produto
        """
        nid = str(time()).replace(".", "")
        self.schema = "%s_%s" % (meta_type, nid)
        self.execSqlu("structure")

        rss = {"titulo":rss_titulo,
               "link":rss_link,
               "descricao":rss_descricao,
               "idioma":rss_idioma,
               "categoria":rss_categoria,
               "copyright":rss_copyright,
               "imagem_titulo":rss_imagem_titulo,
               "imagem_link":rss_imagem_link,
               "rss_imagem":rss_imagem}

        return {"rss":rss}


    @dbconnectionapp
    @serialize
    @Permission("ADM APP")
    def editApp(self, title, identificador_pasta_app=None,
                       identificador_pasta_pag=None, id_pagina_aovivo=None,
                       id_pagina_clone=None, id_portlet_preenchido=None,
                       id_campeonato_aovivo=None, nome_campeonato=None,
                       rss_titulo=None, rss_link=None, rss_descricao=None,
                       rss_idioma=None, rss_categoria=None, rss_copyright=None,
                       rss_imagem_titulo=None, rss_imagem_link=None,
                       rss_imagem=None):
        """Edita os atributos da instancia
        """
        rss = {"titulo":rss_titulo,
               "link":rss_link,
               "descricao":rss_descricao,
               "idioma":rss_idioma,
               "categoria":rss_categoria,
               "copyright":rss_copyright,
               "imagem_titulo":rss_imagem_titulo,
               "imagem_link":rss_imagem_link,
               "rss_imagem":rss_imagem}

        dados = {"rss":rss,"identificador_pasta_app":identificador_pasta_app,
                 "identificador_pasta_pag":identificador_pasta_pag,
                 "id_pagina_aovivo":id_pagina_aovivo,
                 "id_pagina_clone":id_pagina_clone,
                 "id_portlet_preenchido":id_portlet_preenchido}

        portal = Portal(id_site=self.id_site, request=self.request)
        portal._editApp(env_site=self.id_site,
                        schema=self.schema,
                        titulo=title,
                        dados=dados)

        if(id_campeonato_aovivo):
            id_campeonato_h2 = self.execSql("select_next_campeonato_seq").next()["next"]

            id_tree_page = portal._getTreePageByHash(env_site=self.id_site,
                                               hash=identificador_pasta_pag)

            hash_pasta_criada = portal._mkTreePage(env_site=self.id_site,
                                                  id_tree=id_tree_page['id_treepage'],
                                                  titulo=nome_campeonato)

            dictPortlets = {}
            dictPortletsValores = {"id_campeonato":id_campeonato_h2}
            for i in id_portlet_preenchido.split(','):
                dictPortlets[int(i)] = dictPortletsValores

            listaPaginas = []
            for i in id_pagina_clone.split(','):
                listaPaginas.append(int(i))

            paginas_portlets_clonados = portal._addPaginaClone(env_site=self.id_site,
                                                               hash=hash_pasta_criada,
                                                               id_pagina=listaPaginas,
                                                               vl_default=dictPortlets)

            portal.publicarPagina(env_site=self.id_site,
                                  paginas=paginas_portlets_clonados.keys())

            id_tree_app = portal._getTreeAppByHash(env_site=self.id_site,
                                               hash=identificador_pasta_app)
            hash_pasta_criada_app = portal._mkTreeApp(env_site=self.id_site,
                                            id_tree=id_tree_app['id_treeapp'],
                                            titulo=nome_campeonato,
                                            pagina={"pagina":int(id_pagina_aovivo),
                                                    "abrir":"_self",
                                                    "altura":"",
                                                    "largura":"",
                                                    "centralizado":"",
                                                    "scroll":"",
                                                    "dinamico":""},
                                            publicacao={"exportar":True,
                                                        "paginas": {}})
##                                            paginas: {id_pagina:[id_portlet_valor, id_portlet_valor, ...], id_pagina:[]}


            id_tree_criada_app = portal._getTreeAppByHash(env_site=self.id_site,
                                               hash=hash_pasta_criada_app)

            self.execSqlu("insert_campeonato",
                          id_campeonato=int(id_campeonato_h2),
                          id_campeonato_aovivo=int(id_campeonato_aovivo),
                          nome_campeonato=nome_campeonato,
                          id_tree=id_tree_criada_app['id_treeapp'],
                          ids_pagina_portlet=str(paginas_portlets_clonados).replace('L',''))

        return "Aplicativo configurado com sucesso"


    @dbconnectionapp
    def _getTitleDados(self, id_pk):
        """
        """
        for i in self.execSql("select_titulo",
                              id_conteudo=int(id_pk)):
            return {"title":i["titulo"]}


    @dbconnectionapp
    def _getDublinCore(self, id_pk):
        """
        """
        dados = {"title":"",
                 "created":"",
                 "modified":"",
                 "description":"",
                 "keywords":""}

        for i in self.execSql("select_dublic_core",
                              id_conteudo=int(id_pk)):

            portal = Portal(id_site=self.id_site,
                            request=self.request)

            tags = [j["tag"] for j in portal._getTags(id_site=self.id_site,
                                                      id_conteudo=int(id_pk),
                                                      schema=self.schema,
                                                      text=None)]
            tags = " ".join(tags)

            dados["title"] = i["titulo"]
            dados["created"] = i["publicado_em"]
            dados["modified"] = i["atualizado_em"]
            #dados["description"] = i["descricao"][:80]
            dados["keywords"] = tags

        return dados

    # Hurdle

    @dbconnectionapp
    def _get_campeonatos_aovivo(self):
        return self.execSql("select_campeonatos_aovivo")

    @dbconnectionapp
    def _get_campeonatos(self):
        return self.execSql("select_campeonatos")

    @dbconnectionapp
    def _get_campeonatos_atual(self):
        return self.execSql("select_campeonatos_atual")

    @dbconnectionapp
    def _get_artilharia(self,id_campeonato):
        try:
            r = self.execSql("select_artilharia_grupo",id_campeonato=int(id_campeonato))

            if (self.possuiDados(r)):
                return self.execSql("select_artilharia_grupo",id_campeonato=int(id_campeonato))
            else:
                return self.execSql("select_artilharia",id_campeonato=int(id_campeonato))
        except Exception,e:
            import traceback as t
            erros = chr(13) + chr(10) + str(e) + '  ' + chr(13) + chr(10) + str(t.format_exc())

            return self.execSql("select_artilharia",id_campeonato=int(id_campeonato))

    @dbconnectionapp
    def _get_classificacao(self,id_campeonato):
        return self.execSql("select_classificacao", id_campeonato=int(id_campeonato))

    @dbconnectionapp
    def _get_classificacao_by_idconteudo(self,id_conteudo):
        return self.execSql("select_classificacao_by_idconteudo",id_conteudo=int(id_conteudo))

    @dbconnectionapp
    def _get_partidas_by_time(self, id_campeonato, id_time_externo, show_all=0):
        if (show_all == 0):
            r = self.execSql("select_partidas_by_time",
                            id_campeonato=int(id_campeonato),
                            id_time_externo=int(id_time_externo))
        else:
            r = self.execSql("select_partidas_by_time_all",
                            id_campeonato=int(id_campeonato),
                            id_time_externo=int(id_time_externo))

        if (r):
            m = 0
            v = 0
            h = ''
            for i in r:
                if (int(i['t1_id_time_externo']) == int(id_time_externo)):
                    h = h + 'pam[' + str(m) + ']=new pt("' + i['data_f'] + '",' + \
                            '"' + i['t1_nome'] + '",' + \
                            '"' + str(i['t1_sigla']).lower() + '",' + \
                            '"' + str(i['t1_gols']) + '",' + \
                            '"' + i['t2_nome'] + '",' + \
                            '"' + str(i['t2_sigla']).lower() + '",' + \
                            '"' + str(i['t2_gols']) + '");'

                    m = m + 1
                else:
                    h = h + 'pav[' + str(v) + ']=new pt("' + i['data_f'] + '",' + \
                            '"' + i['t1_nome'] + '",' + \
                            '"' + str(i['t1_sigla']).lower() + '",' + \
                            '"' + str(i['t1_gols']) + '",' + \
                            '"' + i['t2_nome'] + '",' + \
                            '"' + str(i['t2_sigla']).lower() + '",' + \
                            '"' + str(i['t2_gols']) + '");'

                    v = v + 1

            if (h):
                h = 'abrirPartidas(\'' + h + '\')'

            return h

        return ''


    @dbconnectionapp
    def _get_estatisticas(self, id_conteudo):
        try:
            import datetime, time

            r = self.execSql("select_estatistica_xml",id_conteudo=int(id_conteudo))

            ret = {}

            for i in r:
                if (not ret.has_key(int(i['id_time']))):
                    d1 = datetime.datetime.strptime(i['data_hora'], '%Y-%m-%d %H:%M:%S')
                    d2 = datetime.datetime.strftime(d1, '%d/%m/%Y %Hh%M')

                    ret[int(i['id_time'])] = {
                        'dados' : i['dados'],
                        'id_time' : i['id_time'],
                        'time_nome' : i['t_nome'],
                        'time_sigla' : i['t_sigla'],
                        'time_gols' : i['t_gols'],
                        'tecnico' : i['tecnico'],
                        'arbitro' : i['arbitro'],
                        'auxiliar1' : i['auxiliar1'],
                        'auxiliar2' : i['auxiliar2'],
                        'data_hora' : str(d2),
                        'local' : i['local'],
                        'estadio' : i['estadio']
                    }
                else:
                    ret[int(i['id_time'])]['dados'] = ret[int(i['id_time'])]['dados'] + ';' + i['dados']

            k = 1
            h = ''
            for i in ret:
                h = h + 'var dados' + str(k) + ' = "' + ret[i]['dados'] + '";'
                h = h + 'var id_time' + str(k) + ' = "' + str(ret[i]['id_time']) + '";'
                h = h + 'var time_nome' + str(k) + ' = "' + ret[i]['time_nome'] + '";'
                h = h + 'var time_sigla' + str(k) + ' = "' + str(ret[i]['time_sigla']).lower() + '";'
                h = h + 'var time_gols' + str(k) + ' = "' + str(ret[i]['time_gols']) + '";'
                h = h + 'var tecnico' + str(k) + ' = "' + str(ret[i]['tecnico']) + '";'
                h = h + 'var arbitro = "' + str(ret[i]['arbitro']) + '";'
                h = h + 'var auxiliar1 = "' + str(ret[i]['auxiliar1']) + '";'
                h = h + 'var auxiliar2 = "' + str(ret[i]['auxiliar2']) + '";'
                h = h + 'var data_hora = "' + str(ret[i]['data_hora']) + '";'
                h = h + 'var local = "' + str(ret[i]['local']) + '";'
                h = h + 'var estadio = "' + str(ret[i]['estadio']) + '";'

                k = k + 1

            if (h):
                h = 'javascript: abrirStats(\'' + h + 'var k = ' + str(k) + ';\')'

            return h
        except Exception, e:
            return str(e)
            #return ''

    @dbconnectionapp
    def _get_possui_narracao(self, id_conteudo):
        try:
            return self.execSql("select_possui_narracao",id_conteudo=int(id_conteudo), id_aplicativo=41).next()
        except:
            return ''

    @dbconnectionapp
    def _get_resultados(self,id_campeonato):
        return self.execSql("select_resultados",id_campeonato=int(id_campeonato))

    @dbconnectionapp
    def _get_resultados_pagina_res(self,id_campeonato):
        from operator import itemgetter
        resultados = self.execSql("select_resultados_pagina_res",id_campeonato=int(id_campeonato))
        lista_aux = []

        ordem_alpha = {'Oitavas de final':996,'Quartas de final':997,'Semifinal':998,'Final':999}
        ordem_alpha_reverso = {996:'Oitavas de final',997:'Quartas de final',998:'Semifinal',999:'Final'}

        for i in resultados:
            if(not(i['fase'].isdigit())):
                i['fase'] = ordem_alpha.get(i['fase'],995)
            else:
                i['fase'] = int(i['fase'])
            lista_aux.append(i)

        lista_ordenada = []
        lista_ordenada = sorted(lista_aux, key=itemgetter('fase'))

        for i in lista_ordenada:
            i['fase'] = ordem_alpha_reverso.get(i['fase'],str(i['fase']))

        return lista_ordenada

    @dbconnectionapp
    def _get_resultados_toCapa(self,id_campeonato):
        import datetime

        if (id_campeonato):
            agora    = datetime.datetime.now()
            amanha   = agora + datetime.timedelta(days=1)
            data_ini = str(agora.year) + '-' + str(agora.month) + '-' + str(agora.day) + ' 00:00'
            data_fim = str(amanha.year) + '-' + str(amanha.month) + '-' + str(amanha.day) + ' 00:00'

        try:
            r = self.execSql("select_resultados_max_o1_grupo",id_campeonato=int(id_campeonato), data_ini=data_ini, data_fim=data_fim)
            if (self.possuiDados(r)):
                return self.execSql("select_resultados_max_o1_grupo",id_campeonato=int(id_campeonato), data_ini=data_ini, data_fim=data_fim)

            r = self.execSql("select_resultados_max_o2_grupo",id_campeonato=int(id_campeonato), data_ini=data_ini)
            if (self.possuiDados(r)):
                return self.execSql("select_resultados_max_o2_grupo",id_campeonato=int(id_campeonato), data_ini=data_ini)

            r = self.execSql("select_resultados_max_o3_grupo",id_campeonato=int(id_campeonato))
            if (self.possuiDados(r)):
                return self.execSql("select_resultados_max_o3_grupo",id_campeonato=int(id_campeonato))
        except:
            pass

        r = self.execSql("select_resultados_max_10_o1",id_campeonato=int(id_campeonato), data_ini=data_ini, data_fim=data_fim)
        if (self.possuiDados(r)):
            return self.execSql("select_resultados_max_10_o1",id_campeonato=int(id_campeonato), data_ini=data_ini, data_fim=data_fim)

        r = self.execSql("select_resultados_max_10_o2",id_campeonato=int(id_campeonato), data_ini=data_ini)
        if (self.possuiDados(r)):
            return self.execSql("select_resultados_max_10_o2",id_campeonato=int(id_campeonato), data_ini=data_ini)

        r = self.execSql("select_resultados_max_10_o3",id_campeonato=int(id_campeonato))
        if (self.possuiDados(r)):
            return self.execSql("select_resultados_max_10_o3",id_campeonato=int(id_campeonato))

    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def delete_campeonato(self,id_camp_del):
        self.execSqlu("delete_campeonato",
                      id_campeonato=int(id_camp_del))

        return "Campeonato excluído com sucesso."

    @staticmethod
    def retornarWidgets():
        """ Retorna os itens para a listagem
        """
        return ({"action":"viewd",
                 "img":"/imgs/preview.gif",
                 "titulo":"Din&aacute;mico",
                 "url":""},
                {"action":"viewe",
                 "img":"/imgs/previewe.gif",
                 "titulo":"Est&aacute;tico",
                 "url":"",
                 "target":""},
                {"action":"view",
                 "img":"/imgs/env.edit.png",
                 "titulo":"Tempo",
                 "url":"listtempo.env",
                 "target":"listagem"},
                {"action":"viewp",
                 "img":"/imgs/env.comment.png",
                 "titulo":"Coment&aacute;rios",
                 "url":"/app/listcomentapp.env",
                 "target":"edicao"},
                {"action":"viewp",
                 "img":"/imgs/env.comment.mod.png",
                 "titulo":"Modera&ccedil;&atilde;o",
                 "url":"/app/addcomentmod.env",
                 "target":"edicao"},
                {"action":"qrcode",
                 "img":"/imgs/qrcode.png",
                 "titulo":"Qrcode",
                 "url":""})

    # hurdle

    @dbconnectionapp
    def getEsquemaTatico(self):
        """Retorna a lista de esquema tatico cadastrados
        """
        return self.execSql("select_esquema_tatico")


    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def addJogo(self, titulo, descricao, embed, videos, schema, id_site,
                      time1_titulo, time1_tecnico, time1_esquema, time1_imagem,
                      time2_titulo, time2_tecnico, time2_esquema, time2_imagem,
                      titulo_destaque, descricao_destaque, imagem_destaque,
                      publicado_em, id_aplicativo, id_treeapp, foto=[],
                      time1_titular_nome=[], time1_titular_camisa=[],
                      time1_reservas_nome=[], time1_reservas_camisa=[],
                      time2_titular_nome=[], time2_titular_camisa=[],
                      time2_reservas_nome=[], time2_reservas_camisa=[],
                      expira_em=None, publicado=None, exportar=None,
                      relacionamento=[], tags="", permissao=None):
        """Adiciona um novo jogo
        """

        dt = publicado_em
        try:
            p = strptime(publicado_em, "%d/%m/%Y %H:%M")
            publicado_em = strftime("%Y-%m-%d %H:%M", p)
        except ValueError, e:
            raise UserError("Data de publica&ccedil;&aring;o"
                            " inv&aacute;lida (%s)" % publicado_em)
        try:
            p = strptime(expira_em, "%d/%m/%Y %H:%M")
            expira_em = strftime("%Y-%m-%d %H:%M", p)
        except ValueError, e:
           expira_em = buffer("NULL")

        id_time1 = self.execSql("select_next_time_seq").next()["next"]
        id_time2 = self.execSql("select_next_time_seq").next()["next"]
        id_conteudo = self.execSql("select_next_conteudo_seq").next()["next"]

        portal = Portal(id_site=self.id_site, request=self.request)
        time1_imagem = portal.addArquivo(arquivo=time1_imagem,
                                         id_conteudo=id_conteudo,
                                         schema=self.schema,
                                         dt=dt)

        time2_imagem = portal.addArquivo(arquivo=time2_imagem,
                                         id_conteudo=id_conteudo,
                                         schema=self.schema,
                                         dt=dt)

        self.execSqlBatch("insert_time",
                          id_time=id_time1,
                          id_esquema_tatico=int(time1_esquema),
                          titulo=time1_titulo,
                          tecnico=time1_tecnico,
                          imagem=time1_imagem)

        self.execSqlBatch("insert_time",
                          id_time=id_time2,
                          id_esquema_tatico=int(time2_esquema),
                          titulo=time2_titulo,
                          tecnico=time2_tecnico,
                          imagem=time2_imagem)

        j = 0
        for nome, camisa in zip(time1_titular_nome, time1_titular_camisa):
            self.execSqlBatch("insert_escalacao",
                              id_time=id_time1,
                              camisa=int(camisa),
                              nome=nome,
                              titular=True,
                              ordem=j,
                              amarelo=False,
                              vermelho=False,
                              substituido=False,
                              escalado=False)
            j += 1

        for nome, camisa in zip(time1_reservas_nome, time1_reservas_camisa):
            self.execSqlBatch("insert_escalacao",
                              id_time=id_time1,
                              camisa=int(camisa),
                              nome=nome,
                              titular=False,
                              ordem=j,
                              amarelo=False,
                              vermelho=False,
                              substituido=False,
                              escalado=False)
            j += 1

        j = 0
        for nome, camisa in zip(time2_titular_nome, time2_titular_camisa):
            self.execSqlBatch("insert_escalacao",
                              id_time=id_time2,
                              camisa=int(camisa),
                              nome=nome,
                              titular=True,
                              ordem=j,
                              amarelo=False,
                              vermelho=False,
                              substituido=False,
                              escalado=False)
            j += 1

        for nome, camisa in zip(time2_reservas_nome, time2_reservas_camisa):
            self.execSqlBatch("insert_escalacao",
                              id_time=id_time2,
                              camisa=int(camisa),
                              nome=nome,
                              titular=False,
                              ordem=j,
                              amarelo=False,
                              vermelho=False,
                              substituido=False,
                              escalado=False)
            j += 1


        self.execSqlBatch("insert_jogo",
                           id_conteudo=id_conteudo,
                           id_time1=id_time1,
                           id_time2=id_time2,
                           titulo=titulo,
                           descricao=descricao,
                           embed=embed,
                           html_videos=videos,
                           finalizado=False,
                           publicado_em=publicado_em,
                           expira_em=expira_em,
                           publicado=True if publicado else False)


        for i in foto:
            img = portal.addArquivo(arquivo=i["arquivo"],
                                    id_conteudo=id_conteudo,
                                    schema=self.schema,
                                    dt=dt)
            if img:
                self.execSqlBatch("insert_foto",
                                  id_conteudo=id_conteudo,
                                  arquivo=img,
                                  alinhamento=i["alinhamento"],
                                  credito=i["credito"],
                                  legenda=i["legenda"],
                                  link=i["link"])

        if titulo_destaque or imagem_destaque or descricao_destaque:
            if not imagem_destaque:
                imagem_destaque = None
            else:
                imagem_destaque = portal.addArquivo(arquivo=imagem_destaque,
                                                    id_conteudo=id_conteudo,
                                                    schema=self.schema,
                                                    dt=dt)

            self.execSqlBatch("insert_destaque",
                              id_conteudo=int(id_conteudo),
                              titulo=titulo_destaque,
                              descricao=descricao_destaque,
                              imagem=imagem_destaque)

        portal = Portal(id_site=self.id_site, request=self.request)
        portal._addConteudo(env_site=self.id_site,
                            id_pk=id_conteudo,
                            schema=self.schema,
                            meta_type=self.meta_type,
                            id_aplicativo=id_aplicativo,
                            id_treeapp=id_treeapp,
                            titulo=titulo,
                            publicado=publicado,
                            publicado_em=publicado_em,
                            expira_em=expira_em,
                            titulo_destaque=titulo_destaque,
                            descricao_destaque=descricao_destaque,
                            imagem_destaque=imagem_destaque,
                            permissao=permissao,
                            tags=tags)

        self.execSqlCommit()
        if exportar:
            portal._exportarConteudof(schema=self.schema,
                                      id_aplicativo=id_aplicativo,
                                      id_conteudo=id_conteudo)
            return "Jogo adicionado! Publica&ccedil;&atilde;o iniciada."

        return "Jogo adicionado com sucesso"


    @dbconnectionapp
    @Permission("PERM APP")
    def delConteudo(self, id_conteudo):
        """Deleta jogos do banco de dados
        """
        self.execSqlu("delete_conteudo",
                      id_conteudo=int(id_conteudo))


    @dbconnectionapp
    def _getJogo(self, id_jogo=None, id_tempo=None):
        """ Retorna os dados de um determinado jogo
        """
        if not id_jogo and id_tempo:
            id_jogo = self.execSql("select_id_jogo_tempo",
                                   id_tempo=int(id_tempo)).next()["id_conteudo"]

        jogo = self.execSql("select_jogo",
                            id_conteudo=int(id_jogo)).next()

        tags = ""
        foto = self.execSql("select_foto",
                            id_conteudo=int(id_jogo))
        escalacao1 = self.execSql("select_escalacao",
                                  id_time=jogo["id_time1"],
                                  titular=True)
        escalacao2 = self.execSql("select_escalacao",
                                  id_time=jogo["id_time2"],
                                  titular=True)
        reservas1 = self.execSql("select_escalacao",
                                  id_time=jogo["id_time1"],
                                  titular=False)
        reservas2 = self.execSql("select_escalacao",
                                  id_time=jogo["id_time2"],
                                  titular=False)

        return {"jogo":jogo,
                "foto":foto,
                "escalacao1":escalacao1,
                "escalacao2":escalacao2,
                "reservas1":reservas1,
                "reservas2":reservas2,
                "tags":tags}

    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def editJogov2(self, id_conteudo, id_treeapp, id_aplicativo, url_radio=None,
                   relacionamento=[], tags=None, permissao=None):
        """Edita um jogo
        """
        portal = Portal(id_site=self.id_site, request=self.request)

        self.execSqlBatch("update_partida_radio",
                          url_radio=url_radio,
                          id_conteudo=int(id_conteudo))

##        portal._editConteudo(env_site=self.id_site,
##                             id_pk=id_conteudo,
##                             id_aplicativo=int(id_aplicativo),
##                             schema=self.schema,
##                             id_treeapp=id_treeapp,
##                             titulo=titulo,
##                             publicado=publicado,
##                             publicado_em=publicado_em,
##                             expira_em=expira_em,
##                             titulo_destaque=titulo_destaque,
##                             descricao_destaque=descricao_destaque,
##                             imagem_destaque=imagem_destaque,
##                             permissao=permissao,
##                             tags=tags)

        self.execSqlCommit()

        portal._exportarConteudo(schema=self.schema,
                                 id_aplicativo=None,
                                 id_conteudo=int(id_conteudo))

        return "Jogo editado sucesso! Publica&ccedil;&atilde;o iniciada."


    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def editJogo(self, id_conteudo, titulo, descricao, embed, videos,
                       id_treeapp, id_aplicativo,
                       id_time1, time1_titulo, time1_tecnico, time1_esquema, time1_imagem,
                       id_time2, time2_titulo, time2_tecnico, time2_esquema, time2_imagem,
                       titulo_destaque, descricao_destaque, imagem_destaque,
                       publicado_em, id_destaque=None, foto=[],
                       time1_titular_nome=[], time1_titular_camisa=[],
                       time1_titular_id=[],
                       time1_reservas_nome=[], time1_reservas_camisa=[],
                       time1_reservas_id=[],
                       time2_titular_nome=[], time2_titular_camisa=[],
                       time2_titular_id=[],
                       time2_reservas_nome=[], time2_reservas_camisa=[],
                       time2_reservas_id=[],
                       escalado_del=[],
                       finalizado=None, expira_em=None, publicado=None,
                       exportar=None, relacionamento=[], tags=None, permissao=None):
        """Edita um jogo
        """

        dt = publicado_em
        try:
            p = strptime(publicado_em, "%d/%m/%Y %H:%M")
            publicado_em = strftime("%Y-%m-%d %H:%M", p)
        except ValueError, e:
            raise UserError("Data de publica&ccedil;&aring;o"
                            " inv&aacute;lida (%s)" % publicado_em)
        try:
            p = strptime(expira_em, "%d/%m/%Y %H:%M")
            expira_em = strftime("%Y-%m-%d %H:%M", p)
        except ValueError, e:
           expira_em = buffer("NULL")

        portal = Portal(id_site=self.id_site, request=self.request)
        if time1_imagem:
            img = portal.addArquivo(arquivo=time1_imagem,
                                    id_conteudo=id_conteudo,
                                    schema=self.schema,
                                    dt=dt)
            time1_imagem = img if img else time1_imagem
        else:
            time1_imagem = None

        if time2_imagem:
            img = portal.addArquivo(arquivo=time2_imagem,
                                    id_conteudo=id_conteudo,
                                    schema=self.schema,
                                    dt=dt)
            time2_imagem = img if img else time2_imagem
        else:
            time2_imagem = None

        self.execSqlBatch("update_time",
                          id_time=int(id_time1),
                          id_esquema_tatico=int(time1_esquema),
                          titulo=time1_titulo,
                          tecnico=time1_tecnico,
                          imagem=time1_imagem)

        self.execSqlBatch("update_time",
                          id_time=int(id_time2),
                          id_esquema_tatico=int(time2_esquema),
                          titulo=time2_titulo,
                          tecnico=time2_tecnico,
                          imagem=time2_imagem)

        j = 0
        for nome, camisa, id_escalacao in zip(time1_titular_nome,
                                              time1_titular_camisa,
                                              time1_titular_id):
            if id_escalacao:
                self.execSqlBatch("update_escalacao",
                                  id_escalacao=int(id_escalacao),
                                  camisa=int(camisa),
                                  nome=nome,
                                  ordem=j)

            else:
                self.execSqlBatch("insert_escalacao",
                                  id_time=int(id_time1),
                                  camisa=int(camisa),
                                  nome=nome,
                                  titular=True,
                                  ordem=j,
                                  amarelo=False,
                                  vermelho=False,
                                  substituido=False,
                                  escalado=False)
            j += 1

        for nome, camisa, id_escalacao in zip(time1_reservas_nome,
                                              time1_reservas_camisa,
                                              time1_reservas_id):
            if id_escalacao:
                self.execSqlBatch("update_escalacao",
                                  id_escalacao=int(id_escalacao),
                                  camisa=int(camisa),
                                  nome=nome,
                                  ordem=j)

            else:
                self.execSqlBatch("insert_escalacao",
                                  id_time=int(id_time1),
                                  camisa=int(camisa),
                                  nome=nome,
                                  titular=False,
                                  ordem=j,
                                  amarelo=False,
                                  vermelho=False,
                                  substituido=False,
                                  escalado=False)
            j += 1

        j = 0
        for nome, camisa, id_escalacao in zip(time2_titular_nome,
                                              time2_titular_camisa,
                                              time2_titular_id):
            if id_escalacao:
                self.execSqlBatch("update_escalacao",
                                  id_escalacao=int(id_escalacao),
                                  camisa=int(camisa),
                                  nome=nome,
                                  ordem=j)

            else:
                self.execSqlBatch("insert_escalacao",
                                  id_time=int(id_time2),
                                  camisa=int(camisa),
                                  nome=nome,
                                  titular=True,
                                  ordem=j,
                                  amarelo=False,
                                  vermelho=False,
                                  substituido=False,
                                  escalado=False)
            j += 1

        for nome, camisa, id_escalacao in zip(time2_reservas_nome,
                                              time2_reservas_camisa,
                                              time2_reservas_id):
            if id_escalacao:
                self.execSqlBatch("update_escalacao",
                                  id_escalacao=int(id_escalacao),
                                  camisa=int(camisa),
                                  nome=nome,
                                  ordem=j)

            else:
                self.execSqlBatch("insert_escalacao",
                                  id_time=int(id_time2),
                                  camisa=int(camisa),
                                  nome=nome,
                                  titular=False,
                                  ordem=j,
                                  amarelo=False,
                                  vermelho=False,
                                  substituido=False,
                                  escalado=False)
            j += 1

        self.execSqlBatch("update_jogo",
                           id_conteudo=id_conteudo,
                           titulo=titulo,
                           descricao=descricao,
                           embed=embed,
                           html_videos=videos,
                           finalizado=True if finalizado else False,
                           publicado_em=publicado_em,
                           expira_em=expira_em,
                           publicado=True if publicado else False)

        if len(escalado_del) > 0:
            escalado_del = ",".join(escalado_del)
            self.execSqlBatch("delete_escalacao", escalado=buffer(escalado_del))


        self.execSqlBatch("delete_foto", id_conteudo=int(id_conteudo))
        for i in foto:

            img = portal.addArquivo(arquivo=i["arquivo"],
                                    id_conteudo=id_conteudo,
                                    schema=self.schema,
                                    dt=dt)
            self.execSqlBatch("insert_foto",
                              id_conteudo=int(id_conteudo),
                              arquivo=img if img else i['arquivo'],
                              alinhamento=i['alinhamento'],
                              credito=i['credito'],
                              legenda=i['legenda'],
                              link=i['link'])

        if titulo_destaque or imagem_destaque or descricao_destaque:
            if not imagem_destaque:
                imagem_destaque = None
            else:
                imagem_destaque = portal.addArquivo(arquivo=imagem_destaque,
                                                    id_conteudo=id_conteudo,
                                                    schema=self.schema,
                                                    dt=dt)

            if id_destaque:
                self.execSqlBatch("update_destaque",
                                  id_destaque=int(id_destaque),
                                  titulo=titulo_destaque,
                                  descricao=descricao_destaque,
                                  imagem=imagem_destaque)
            else:
                self.execSqlBatch("insert_destaque",
                                  id_conteudo=int(id_conteudo),
                                  titulo=titulo_destaque,
                                  descricao=descricao_destaque,
                                  imagem=imagem_destaque)
        elif id_destaque:
            self.execSqlBatch("delete_destaque",
                              id_destaque=int(id_destaque))
            imagem_destaque = None
            titulo_destaque = None
            descricao_destaque = None

        portal._editConteudo(env_site=self.id_site,
                             id_pk=id_conteudo,
                             id_aplicativo=int(id_aplicativo),
                             schema=self.schema,
                             id_treeapp=id_treeapp,
                             titulo=titulo,
                             publicado=publicado,
                             publicado_em=publicado_em,
                             expira_em=expira_em,
                             titulo_destaque=titulo_destaque,
                             descricao_destaque=descricao_destaque,
                             imagem_destaque=imagem_destaque,
                             permissao=permissao,
                             tags=tags)

        self.execSqlCommit()

        if exportar:
            portal._exportarConteudof(schema=self.schema,
                                      id_aplicativo=id_aplicativo,
                                      id_conteudo=id_conteudo)
            return "Jogo editado sucesso! Publica&ccedil;&atilde;o iniciada."

        return "Jogo editado com sucesso"


    @dbconnectionapp
    def _listarTempo(self, id_conteudo):
        """Retorna a lista de tempos de um determinado jogo
        """
        return self.execSql("select_tempos",
                            id_conteudo=int(id_conteudo))


    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def addTempo(self, id_conteudo, nome, inicio, intervalo=None):
        """Adiciona um novo tempo a um determinado jogo
        """
        try:
            p = strptime(inicio, "%d/%m/%Y %H:%M")
            inicio = strftime("%Y-%m-%d %H:%M", p)
        except ValueError, e:
            raise UserError("Data de in&iacute;cio "
                            " inv&aacute;lida (%s)" % inicio)
        intervalo = True if intervalo else False
        self.execSqlu("insert_tempo",
                      id_conteudo=int(id_conteudo),
                      nome=nome,
                      inicio=inicio,
                      intervalo=intervalo)

        return "Tempo adicionado com sucesso!"


    @dbconnectionapp
    def _getTempo(self, id_tempo):
        """Retorna os dados de um determinado tempo
        """
        for i in self.execSql("select_tempo",
                              id_tempo=int(id_tempo)):
            return i


    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def editTempo(self, id_tempo, nome, inicio, intervalo=None):
        """Edita um determinado tempo
        """
        try:
            p = strptime(inicio, "%d/%m/%Y %H:%M")
            inicio = strftime("%Y-%m-%d %H:%M", p)
        except ValueError, e:
            raise UserError("Data de in&iacute;cio "
                            " inv&aacute;lida (%s)" % inicio)
        intervalo = True if intervalo else False
        self.execSqlu("update_tempo",
                      id_tempo=int(id_tempo),
                      nome=nome,
                      inicio=inicio,
                      intervalo=intervalo)

        return "Tempo editado com sucesso"


    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def delTempo(self, id_tempo=[]):
        """Deleta um lance selecionado na administracao
        """
        for i in id_tempo:
            self.execSqlBatch("delete_tempo",
                              id_tempo=int(i))

        self.execSqlCommit()
        return "Tempo deletado com sucesso!"


    @dbconnectionapp
    def _listLance(self, id_tempo):
        """Retorna a lista de lances de um determinado tempo
        """
        return self.execSql("select_lances",
                            id_tempo=int(id_tempo))


    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def addLance(self, id_tempo, minuto, descricao,
                       id_time1, id_time2, icon_gol=None, icon_amarelo=None,
                       icon_vermelho=None,
                       time_amarelo=[], time_vermelho=[], time_substituido=[],
                       time_escalado=[], id_gol=None, exportar=None):
        """Adiciona um novo lance a um determinado tempo
        """
        if id_gol:
           id_seq_gol = self.execSql("select_next_conteudo_seq").next()["next"]
           self.execSqlBatch("insert_gol",
                             id_gol=id_seq_gol,
                             id_escalacao=int(id_gol),
                             minuto=int(minuto))
           id_gol = id_seq_gol
        else:
            id_gol = "NULL"

        self.execSqlBatch("insert_lance",
                          id_tempo=int(id_tempo),
                          id_gol=buffer(str(id_gol)),
                          descricao=descricao,
                          minuto=int(minuto),
                          gol=True if icon_gol else False,
                          amarelo=True if icon_amarelo else False,
                          vermelho=True if icon_vermelho else False,
                          substituicao=True if len(time_substituido) > 0 else False)

        time_amarelo.append("-1")
        time_vermelho.append("-1")
        time_substituido.append("-1")
        time_escalado.append("-1")

        self.execSqlBatch("update_time_tipo",
                          id_time1=int(id_time1),
                          id_time2=int(id_time2),
                          amarelo=buffer(",".join(time_amarelo)),
                          vermelho=buffer(",".join(time_vermelho)),
                          substituido=buffer(",".join(time_substituido)),
                          escalado=buffer(",".join(time_escalado)))

        self.execSqlCommit()
        return "Lance adicionado com sucesso"


    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def delLance(self, id_lance=[]):
        """Deleta os lances selecionados na administracao
        """
        for i in id_lance:
            self.execSqlBatch("delete_lance",
                              id_lance=int(i))

        self.execSqlCommit()
        return "Lance deletado com sucesso"


    @dbconnectionapp
    def _getLance(self, id_lance):
        """Retorna os dados de um determinado lance
        """
        lance = self.execSql("select_lance",
                             id_lance=int(id_lance)).next()

        gol = {'id_escalacao':None, 'id_gol':None}
        if lance["id_gol"]:
            for i in self.execSql("select_gol",
                                  id_gol=lance["id_gol"]):
                gol["id_escalacao"] = i["id_escalacao"]
                gol["id_gol"] = i["id_gol"]
                break

        return {"lance":lance, "gol":gol}


    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def editLance(self, id_lance, id_tempo, minuto, descricao,
                        id_time1, id_time2, id_gol=None, icon_gol=None,
                        icon_amarelo=None, icon_vermelho=None,
                        time_amarelo=[], time_vermelho=[], time_substituido=[],
                        time_escalado=[], gol=None, exportar=None):
        """
        """
        if gol and id_gol:
            self.execSqlBatch("update_gol",
                              id_gol=int(id_gol),
                              id_escalacao=int(gol),
                              minuto=int(minuto))
        elif gol and not id_gol:
           id_seq_gol = self.execSql("select_next_conteudo_seq").next()["next"]
           self.execSqlBatch("insert_gol",
                             id_gol=id_seq_gol,
                             id_escalacao=int(gol),
                             minuto=int(minuto))
           id_gol = id_seq_gol
        elif id_gol and not gol:
            self.execSqlBatch("delete_gol",
                              id_gol=int(id_gol))
            id_gol = "NULL"

        if not id_gol:
            id_gol = "NULL"

        self.execSqlBatch("update_lance",
                          id_lance=int(id_lance),
                          id_gol=buffer(str(id_gol)),
                          descricao=descricao,
                          minuto=int(minuto),
                          gol=icon_gol,
                          amarelo=icon_amarelo,
                          vermelho=icon_vermelho,
                          substituicao=True if len(time_substituido) > 0 else False)

        time_amarelo.append("-1")
        time_vermelho.append("-1")
        time_substituido.append("-1")
        time_escalado.append("-1")

        self.execSqlBatch("update_time_tipo",
                          id_time1=int(id_time1),
                          id_time2=int(id_time2),
                          amarelo=buffer(",".join(time_amarelo)),
                          vermelho=buffer(",".join(time_vermelho)),
                          substituido=buffer(",".join(time_substituido)),
                          escalado=buffer(",".join(time_escalado)))

        self.execSqlCommit()
        return "Lance editado com sucesso!"

    @dbconnectionapp
    def _get_times_partida(self,id_conteudo):
        return self.execSql("select_times_partida",id_conteudo=int(id_conteudo))

    @dbconnectionapp
    def _get_escalacao_partida(self,id_time):
        return self.execSql("select_escalacao_partida",id_time=int(id_time))

    @dbconnectionapp
    def _get_partida_narracao(self,id_conteudo):
        return self.execSql("select_narracao_partida",id_conteudo=int(id_conteudo))

    @dbconnectionapp
    def _get_ficha_partida(self,id_conteudo):
        return self.execSql("select_ficha_partida",id_conteudo=int(id_conteudo))

    @dbconnectionapp
    def _get_placar_partida(self,id_conteudo=0):
        return self.execSql("select_placar_partida",id_conteudo=int(id_conteudo))

    @dbconnectionapp
    def _get_dados_partida(self,id_conteudo=0):
        return self.execSql("select_partida",id_conteudo=int(id_conteudo))

    @dbconnectionapp
    def _get_dados_partida_radio(self,id_conteudo=0):
        return self.execSql("select_partida_radio",id_conteudo=int(id_conteudo))

    @dbconnectionapp
    def _get_partidas_simultaneas(self, id_conteudo=0):
        import datetime
        agora = datetime.datetime.now()
        amanha   = agora + datetime.timedelta(days=1)
        data_ini = str(agora.year) + '-' + str(agora.month) + '-' + str(agora.day) + ' 00:00'
        data_fim = str(amanha.year) + '-' + str(amanha.month) + '-' + str(amanha.day) + ' 00:00'
        return self.execSql("select_partidas_simultaneas", data_ini=data_ini, data_fim=data_fim, id_conteudo=int(id_conteudo))

    @dbconnectionapp
    def _get_partida_portlet_capa_parceiro(self,id_conteudo=0):
        portal = Portal(id_site=self.id_site, request=self.request)
        for i in self.execSql("select_partida_portlet_capa",id_conteudo=int(id_conteudo)):
            i["url"] = portal.getUrlByApp(env_site=self.id_site,
                                          schema=self.schema,
                                          id_conteudo=i["id_conteudo"],
                                          exportar=True)
            yield i

    @dbconnectionapp
    def _get_partida_portlet_capa(self,id_conteudo=0):
        return self.execSql("select_partida_portlet_capa",id_conteudo=int(id_conteudo))

    def possuiDados(self, objGenerator):
        if(str(type(objGenerator)) == "<type 'generator'>"):

            try:
                objGenerator.next()
                return True
            except StopIteration:
                return False
        elif(objGenerator == True):
            return True
        else:
            return False


    @permissioncron
    @serialize
    def filtra_xmls(self):
        import os
        import shutil
        arquivos = os.listdir(path_base)

        for i in arquivos:
            if (i.lower().find('.xml') != -1):
                try:
                    arquivo_valido = True
                    try:
                        int(i.split('_')[3])
                    except:
                        arquivo_valido = False

                    if(arquivo_valido or i.lower().find('campeonatos') > 0):
                        xml_ok = False
                        #arq    = self.checa_xmls_processados(i)
                        xml_ok = self.checa_campeonatos_h2(i)

                        if self.possuiDados(xml_ok):
                            if(i.lower().find('alt') > 0):
                                if(i.lower().find('par_alt.') > 0):
                                    self.atualiza_partidas_alteradas(i)
                                else:
                                    pass
                            elif(i.lower().find('sts.') > 0):
                                self.atualiza_estatisticas_xml(i)
                            elif(i.lower().find('par_') > 0):
                                self.atualiza_partida_xml(i)
                            elif(i.lower().find('par.') > 0):
                                self.atualiza_resultados_xml(i)
                            elif(i.lower().find('tab.') > 0):
                                self.atualiza_classificacao_xml(i)
                            elif(i.lower().find('art.') > 0):
                                self.atualiza_artilharia_xml(i)
                            elif(i.lower().find('campeonatos') > 0):
                                self.atualiza_campeonatos_xml(i)

                    if(i.find('xmls_processados') == -1):
                        if (len(i.split('_')) > 3):
                            d1 = datetime.now()
                            d2 = d1.strftime('%Y-%m-%d.%Hh%Mm%Ss')

                            dir_dest = self.path_base + "xmls_processados/" + i.split('_')[3].replace('.xml', '') + "/"
                            arq_dest = dir_dest + i.replace('.xml', '_' + d2 + '.xml')

                            try:
                                makedirs(dir_dest)
                                chmod(dir_dest, 0777)
                            except:
                                pass

                            shutil.move(self.path_base + i, arq_dest)
                        else:
                            shutil.move(self.path_base + i, self.path_base + "xmls_processados/" + i)
                except Exception,e:
                    import traceback as t
##                    from enviaEmailAnexo import enviamail
                    erros = chr(13) + chr(10) + str(e) + '  ' + chr(13) + chr(10) + str(t.format_exc())

                    to = ["alexandre.mendes@uai.com.br",
                           "leonardocosta.mg@diariosassociados.com.br"#,
                           #"rosa.borges@uai.com.br",
                           #"mpilarurban.mg@diariosassociados.com.br",
                           #"kurt@uai.com.br",
                           #"suporte.em@uai.com.br"
                           ]

                    orig    = "superesportes@uai.com.br"
                    subject = "SUPERESPORTES - AoVivo - Erro ao processar XML"
                    arq_xml = i
                    arq_log = { 'name' : i.replace('.xml', '.log'), 'content' : erros }

                    try:
##                        res = enviamail(_subject = subject,
##                                         _from = orig,
##                                         _to = to,
##                                         _smtp = "smtp.em.com.br",
##                                         _body = "Ocorreu um erro no processamento do XML.\n\nContactar: Boné: 8887-1441, Leonardo: 8484-1364, Rosa: 9292-9499",
##                                         _files = [ arq_xml ],
##                                         _content_files = [ arq_log ])

                        dir_erro = self.path_base + "xmls_erro/"

                        try:
                            makedirs(dir_erro)
                            chmod(dir_erro, 0777)
                        except:
                            pass

                        log_erro = open(dir_erro + i.replace('.xml', '.log'), 'ab')
                        log_erro.write(erros)
                        log_erro.close()

                        chmod(dir_erro + i.replace('.xml', '.log'), 0777)

                        shutil.move(self.path_base + i, dir_erro + i)
                    except Exception,e:
                        import traceback as t
                        errrr = chr(13) + chr(10) + str(e) + '  ' + chr(13) + chr(10) + str(t.format_exc())

                        log_erro = open('/tmp/teste-email-aovivo.txt', 'ab')
                        log_erro.write(errrr)
                        log_erro.close()
                        chmod('/tmp/teste-email-aovivo.txt', 0777)
                        pass


    @dbconnectionapp
    @Permission("PERM APP")
    def checa_xmls_processados(self, arq_xml):
        return self.execSql("select_xmls_processados",nome_xml=arq_xml)

    @dbconnectionapp
    @Permission("PERM APP")
    def checa_campeonatos_h2(self, arq_xml):
        if(arq_xml.lower().find('campeonatos') > 0):
            return True
        id_campeonato_aovivo = arq_xml.split('_')[3]
        return self.execSql("select_campeonatos_h2",id_campeonato_aovivo=int(id_campeonato_aovivo))

    @dbconnectionapp
    def checa_partida(self, id_conteudo):
        return self.execSql("select_checa_partida",id_conteudo=int(id_conteudo))

    def trataHora(self, sHora):
        h1 = []
        h2 = sHora.replace('h', '').replace(':', '')
        h = sHora
        m = ''

        if (sHora.find('h') != -1):
            h1 = sHora.split('h')
        elif (sHora.find(':') != -1):
            h1 = sHora.split(':')

        if (len(h1) > 0):
            if (len(h1) == 2):
                h = h1[0]
                m = h1[1]
            else:
                h = h1[0]
                m = '00'

        if (len(h) == 1):
            h = '0' + h

        if (len(m) == 0):
            m = '00'
        elif (len(m) == 1):
            m = '0' + m

        h2 = h + m

        return h2

    @dbconnectionapp
    def atualiza_partida_xml(self, arq_xml):
        #import elementtree.ElementTree as ET
        from packages.elementtree import ElementTree as ET
        path_xml = self.path_base + arq_xml
        root = ET.parse(path_xml)
        try:
            root = ET.parse(path_xml)
        except:
            return ''

        dir_erro = self.path_base + "xmls_erro/"

        try:
            makedirs(dir_erro)
            chmod(dir_erro, 0777)
        except:
            pass

        log_erro = open(dir_erro + arq_xml.replace('.xml', '.log'), 'ab')

        id_campeonato    = arq_xml.split('_')[3]
        campeonato_h2    = self.execSql("select_campeonato_h2", id_campeonato_aovivo=int(id_campeonato)).next()
        id_campeonato_h2 = campeonato_h2['id_campeonato']
        id_conteudo      = arq_xml.split('_')[5].replace('.xml','')
        portal           = Portal(id_site=self.id_site, request=self.request)

        agora = datetime.now()

        registros = []
        for node in root.getiterator('partida'):
            dictSaida = {}
            for n in node:
                dictSaida[n.tag] = unicode(n.text).encode('latin1')
            registros.append(dictSaida)

        reg_narracao = []
        for node in root.getiterator('minuto'):
            dictSaida = {}
            for n in node:
                dictSaida[n.tag] = unicode(n.text).encode('latin1')
            reg_narracao.append(dictSaida)

#        log_erro.write('22[' + str(reg_narracao) + ']\n')

        if self.possuiDados(self.checa_partida(id_conteudo=id_conteudo)):
            for i in registros:
                if i['jogoini'] == None or i['jogoini'] == 'None' : i['jogoini'] = 0
                if i['jogofim'] == None or i['jogofim'] == 'None' : i['jogofim'] = 0

                iniciado   = int(i['jogoini'])
                finalizado = int(i['jogofim'])
                hora_jogo  = self.trataHora(i['hora'])

                data_hora_partida = datetime.strptime(i['data'] + ' ' + hora_jogo,'%d/%m/%Y %H%M').strftime('%Y-%m-%d %H:%M')

                self.execSqlBatch("update_partida_com_completo",
                                      iniciado=iniciado,
                                      finalizado=finalizado,
                                      arbitro=i['arbitro'],
                                      auxiliar1=i['auxiliar1'],
                                      auxiliar2=i['auxiliar2'],
                                      local=i['local'],
                                      estadio=i['estadio'],
                                      data_hora=data_hora_partida,
                                      id_conteudo=int(id_conteudo))

                self.execSqlCommit()

                partida = self.execSql("select_partida", id_conteudo=int(id_conteudo)).next()
                registrosEscalacao = []
                registrosSubstituicoes = []
                id_time1 = None
                id_time2 = None

                if (partida['id_time1'] == None or partida['id_time2'] == None):
                    registros = []
                    for node in root.getiterator('time1'):
                        dictSaida = {}
                        for n in node:
                            dictSaida[n.tag] = unicode(n.text).encode('latin1')
                            if n.tag == 'escalacao':
                                registrosEscalacao = []
                                for child in n.getiterator('jogador'):
                                    dictSaidaEscalacao = {}
                                    for c in child:
                                        dictSaidaEscalacao[c.tag] = unicode(c.text).encode('latin1')
                                    registrosEscalacao.append(dictSaidaEscalacao)
                            if n.tag == 'substituicoes':
                                registrosSubstituicoes = []
                                for child in n.getiterator('novo_jogador'):
                                    dictSaidaSubstituicao = {}
                                    for c in child:
                                        dictSaidaSubstituicao[c.tag] = unicode(c.text).encode('latin1')
                                    registrosSubstituicoes.append(dictSaidaSubstituicao)
                        registros.append(dictSaida)

                    for i in registros:
                        id_time1 = self.execSql("select_next_time_xml_seq").next()["next"]
                        nome_time1 = i['nome']
                        self.execSqlBatch("insert_time_xml",
                                          id_time=id_time1,
                                          id_conteudo=int(id_conteudo),
                                          nome=i['nome'],
                                          sigla=i['sigla'],
                                          esquema_tatico=i['formacao'],
                                          tecnico=i.get('tecnico',None),
                                          gols=int(i['gols']),
                                          penalts=int(i['penalts']),
                                          id_time_externo=int(i['id']))
                        self.execSqlCommit()

                    for i in registrosEscalacao:
                        self.execSqlBatch("insert_escalacao_xml",
                                          id_time=id_time1,
                                          nome=i['nome'],
                                          posicao=i['posicao'],
                                          gols=int(i['gol']),
                                          amarelo=int(i['amarelo']),
                                          amarelo2=int(i['amarelo2']),
                                          vermelho=int(i['vermelho']),
                                          substituido=int(i['substituir']),
                                          id_jogador=int(i['id']),
                                          gol_contra=int(i['golcontra']))
                        self.execSqlCommit()

                    for i in registrosSubstituicoes:
                        self.execSqlBatch("insert_substituicoes",
                                          id_time=id_time1,
                                          nome=i['nome'],
                                          posicao=i['posicao'],
                                          gols=int(i['gol']),
                                          amarelo=int(i['amarelo']),
                                          amarelo2=int(i['amarelo2']),
                                          vermelho=int(i['vermelho']),
                                          substituido=int(i['substituir']),
                                          id_jogador=int(i['id']),
                                          id_jogador_substituido=int(i['id_jogador_substituido']),
                                          gol_contra=int(i['golcontra']))
                        self.execSqlCommit()

                    registros = []
                    for node in root.getiterator('time2'):
                        dictSaida = {}
                        for n in node:
                            dictSaida[n.tag] = unicode(n.text).encode('latin1')
                            if n.tag == 'escalacao':
                                registrosEscalacao = []
                                for child in n.getiterator('jogador'):
                                    dictSaidaEscalacao = {}
                                    for c in child:
                                        dictSaidaEscalacao[c.tag] = unicode(c.text).encode('latin1')
                                    registrosEscalacao.append(dictSaidaEscalacao)
                            if n.tag == 'substituicoes':
                                registrosSubstituicoes = []
                                for child in n.getiterator('novo_jogador'):
                                    dictSaidaSubstituicao = {}
                                    for c in child:
                                        dictSaidaSubstituicao[c.tag] = unicode(c.text).encode('latin1')
                                    registrosSubstituicoes.append(dictSaidaSubstituicao)
                        registros.append(dictSaida)

                    for i in registros:
                        id_time2 = self.execSql("select_next_time_xml_seq").next()["next"]
                        nome_time2 = i['nome']
                        self.execSqlBatch("insert_time_xml",
                                          id_time=id_time2,
                                          id_conteudo=int(id_conteudo),
                                          nome=i['nome'],
                                          sigla=i['sigla'],
                                          esquema_tatico=i['formacao'],
                                          tecnico=i.get('tecnico',None),
                                          gols=int(i['gols']),
                                          penalts=int(i['penalts']),
                                          id_time_externo=int(i['id']))
                        self.execSqlCommit()

                    for i in registrosEscalacao:
                        self.execSqlBatch("insert_escalacao_xml",
                                          id_time=id_time2,
                                          nome=i['nome'],
                                          posicao=i['posicao'],
                                          gols=int(i['gol']),
                                          amarelo=int(i['amarelo']),
                                          amarelo2=int(i['amarelo2']),
                                          vermelho=int(i['vermelho']),
                                          substituido=int(i['substituir']),
                                          id_jogador=int(i['id']),
                                          gol_contra=int(i['golcontra']))
                        self.execSqlCommit()

                    for i in registrosSubstituicoes:
                        self.execSqlBatch("insert_substituicoes",
                                          id_time=id_time2,
                                          nome=i['nome'],
                                          posicao=i['posicao'],
                                          gols=int(i['gol']),
                                          amarelo=int(i['amarelo']),
                                          amarelo2=int(i['amarelo2']),
                                          vermelho=int(i['vermelho']),
                                          substituido=int(i['substituir']),
                                          id_jogador=int(i['id']),
                                          id_jogador_substituido=int(i['id_jogador_substituido']),
                                          gol_contra=int(i['golcontra']))
                        self.execSqlCommit()
                else:
#------------------------
                    id_time1 = int(partida['id_time1'])
                    id_time2 = int(partida['id_time2'])

                    self.execSqlu("limpa_escalacao_xml", id_time=int(partida['id_time1']))

                    registrosEscalacao = []
                    registrosSubstituicoes = []
                    registros = []
                    for node in root.getiterator('time1'):
                        dictSaida = {}
                        for n in node:
                            dictSaida[n.tag] = unicode(n.text).encode('latin1')
                            if n.tag == 'escalacao':
                                registrosEscalacao = []
                                for child in n.getiterator('jogador'):
                                    dictSaidaEscalacao = {}
                                    for c in child:
                                        dictSaidaEscalacao[c.tag] = unicode(c.text).encode('latin1')
                                    registrosEscalacao.append(dictSaidaEscalacao)
                            if n.tag == 'substituicoes':
                                registrosSubstituicoes = []
                                for child in n.getiterator('novo_jogador'):
                                    dictSaidaSubstituicao = {}
                                    for c in child:
                                        dictSaidaSubstituicao[c.tag] = unicode(c.text).encode('latin1')
                                    registrosSubstituicoes.append(dictSaidaSubstituicao)
                        registros.append(dictSaida)

                    for i in registros:
                        nome_time1 = i['nome']
                        self.execSqlBatch("update_time_xml",
                                          gols=int(i['gols']),
                                          penalts=int(i['penalts']),
                                          tecnico=i.get('tecnico',None),
                                          id_time=partida['id_time1'],
                                          id_time_externo=int(i['id']))
                        self.execSqlCommit()

                    for i in registrosEscalacao:
                        self.execSqlBatch("insert_escalacao_xml",
                                          id_time=partida['id_time1'],
                                          nome=i['nome'],
                                          posicao=i['posicao'],
                                          gols=int(i['gol']),
                                          amarelo=int(i['amarelo']),
                                          amarelo2=int(i['amarelo2']),
                                          vermelho=int(i['vermelho']),
                                          substituido=int(i['substituir']),
                                          id_jogador=int(i['id']),
                                          gol_contra=int(i['golcontra']))
                        self.execSqlCommit()

                    for i in registrosSubstituicoes:
                        self.execSqlBatch("insert_substituicoes",
                                          id_time=partida['id_time1'],
                                          nome=i['nome'],
                                          posicao=i['posicao'],
                                          gols=int(i['gol']),
                                          amarelo=int(i['amarelo']),
                                          amarelo2=int(i['amarelo2']),
                                          vermelho=int(i['vermelho']),
                                          substituido=int(i['substituir']),
                                          id_jogador=int(i['id']),
                                          id_jogador_substituido=int(i['id_jogador_substituido']),
                                          gol_contra=int(i['golcontra']))
                        self.execSqlCommit()

                    self.execSqlu("limpa_escalacao_xml", id_time=int(partida['id_time2']))

                    registrosEscalacao = []
                    registrosSubstituicoes = []
                    registros = []
                    for node in root.getiterator('time2'):
                        dictSaida = {}
                        for n in node:
                            dictSaida[n.tag] = unicode(n.text).encode('latin1')
                            if n.tag == 'escalacao':
                                registrosEscalacao = []
                                for child in n.getiterator('jogador'):
                                    dictSaidaEscalacao = {}
                                    for c in child:
                                        dictSaidaEscalacao[c.tag] = unicode(c.text).encode('latin1')
                                    registrosEscalacao.append(dictSaidaEscalacao)
                            if n.tag == 'substituicoes':
                                registrosSubstituicoes = []
                                for child in n.getiterator('novo_jogador'):
                                    dictSaidaSubstituicao = {}
                                    for c in child:
                                        dictSaidaSubstituicao[c.tag] = unicode(c.text).encode('latin1')
                                    registrosSubstituicoes.append(dictSaidaSubstituicao)
                        registros.append(dictSaida)

                    for i in registros:
                        nome_time2 = i['nome']
                        self.execSqlBatch("update_time_xml",
                                          gols=int(i['gols']),
                                          penalts=int(i['penalts']),
                                          tecnico=i.get('tecnico',None),
                                          id_time=partida['id_time2'],
                                          id_time_externo=int(i['id']))
                        self.execSqlCommit()

                    for i in registrosEscalacao:
                        self.execSqlBatch("insert_escalacao_xml",
                                          id_time=partida['id_time2'],
                                          nome=i['nome'],
                                          posicao=i['posicao'],
                                          gols=int(i['gol']),
                                          amarelo=int(i['amarelo']),
                                          amarelo2=int(i['amarelo2']),
                                          vermelho=int(i['vermelho']),
                                          substituido=int(i['substituir']),
                                          id_jogador=int(i['id']),
                                          gol_contra=int(i['golcontra']))
                        self.execSqlCommit()

                    for i in registrosSubstituicoes:
                        self.execSqlBatch("insert_substituicoes",
                                          id_time=partida['id_time2'],
                                          nome=i['nome'],
                                          posicao=i['posicao'],
                                          gols=int(i['gol']),
                                          amarelo=int(i['amarelo']),
                                          amarelo2=int(i['amarelo2']),
                                          vermelho=int(i['vermelho']),
                                          substituido=int(i['substituir']),
                                          id_jogador=int(i['id']),
                                          id_jogador_substituido=int(i['id_jogador_substituido']),
                                          gol_contra=int(i['golcontra']))
                        self.execSqlCommit()
#------------------------
                if (id_time1 and id_time2):
                    titulo = nome_time1 + " X " + nome_time2

                    if (len(registrosEscalacao) > 0):
                        possui_narracao = '1'
                    else:
                        possui_narracao = '0'

                    self.execSqlBatch("update_partida_xml_addtime",
                                      id_time1=int(id_time1),
                                      id_time2=int(id_time2),
                                      titulo=titulo,
                                      possui_narracao=possui_narracao,
                                      id_conteudo=int(id_conteudo))

                primeiro_acesso = False

        else:
            for i in registros:
                if i['jogoini'] == None or i['jogoini'] == 'None' : i['jogoini'] = 0
                if i['jogofim'] == None or i['jogofim'] == 'None' : i['jogofim'] = 0

                iniciado   = int(i['jogoini'])
                finalizado = int(i['jogofim'])
                hora_jogo  = self.trataHora(i['hora'])

                data_hora_partida = datetime.strptime(i['data'] + ' ' + hora_jogo,'%d/%m/%Y %H%M').strftime('%Y-%m-%d %H:%M')

                self.execSqlBatch("insert_partida_xml",
                                  id_conteudo=int(id_conteudo),
                                  id_campeonato=int(id_campeonato_h2),
                                  publicado_em=data_hora_partida,
                                  iniciado=iniciado,
                                  finalizado=finalizado,
                                  arbitro=i['arbitro'],
                                  auxiliar1=i['auxiliar1'],
                                  auxiliar2=i['auxiliar2'],
                                  rodada=i['rodada'],
                                  #data_hora=agora,
                                  data_hora=data_hora_partida,
                                  local=i['local'],
                                  estadio=i['estadio'])

                self.execSqlCommit()
                primeiro_acesso = True

            registrosEscalacao = []
            registrosSubstituicoes = []
            registros = []
            for node in root.getiterator('time1'):
                dictSaida = {}
                for n in node:
                    dictSaida[n.tag] = unicode(n.text).encode('latin1')
                    if n.tag == 'escalacao':
                        registrosEscalacao = []
                        for child in n.getiterator('jogador'):
                            dictSaidaEscalacao = {}
                            for c in child:
                                dictSaidaEscalacao[c.tag] = unicode(c.text).encode('latin1')
                            registrosEscalacao.append(dictSaidaEscalacao)
                    if n.tag == 'substituicoes':
                        registrosSubstituicoes = []
                        for child in n.getiterator('novo_jogador'):
                            dictSaidaSubstituicao = {}
                            for c in child:
                                dictSaidaSubstituicao[c.tag] = unicode(c.text).encode('latin1')
                            registrosSubstituicoes.append(dictSaidaSubstituicao)
                registros.append(dictSaida)

            for i in registros:
                id_time1 = self.execSql("select_next_time_xml_seq").next()["next"]
                nome_time1 = i['nome']
                self.execSqlBatch("insert_time_xml",
                                  id_time=id_time1,
                                  id_conteudo=int(id_conteudo),
                                  nome=i['nome'],
                                  sigla=i['sigla'],
                                  esquema_tatico=i['formacao'],
                                  tecnico=i.get('tecnico',None),
                                  gols=int(i['gols']),
                                  penalts=int(i['penalts']),
                                  id_time_externo=int(i['id']))
                self.execSqlCommit()

            for i in registrosEscalacao:
                self.execSqlBatch("insert_escalacao_xml",
                                  id_time=id_time1,
                                  nome=i['nome'],
                                  posicao=i['posicao'],
                                  gols=int(i['gol']),
                                  amarelo=int(i['amarelo']),
                                  amarelo2=int(i['amarelo2']),
                                  vermelho=int(i['vermelho']),
                                  substituido=int(i['substituir']),
                                  id_jogador=int(i['id']),
                                  gol_contra=int(i['golcontra']))
                self.execSqlCommit()

            for i in registrosSubstituicoes:
                self.execSqlBatch("insert_substituicoes",
                                  id_time=id_time1,
                                  nome=i['nome'],
                                  posicao=i['posicao'],
                                  gols=int(i['gol']),
                                  amarelo=int(i['amarelo']),
                                  amarelo2=int(i['amarelo2']),
                                  vermelho=int(i['vermelho']),
                                  substituido=int(i['substituir']),
                                  id_jogador=int(i['id']),
                                  id_jogador_substituido=int(i['id_jogador_substituido']),
                                  gol_contra=int(i['golcontra']))
                self.execSqlCommit()

            registros = []
            for node in root.getiterator('time2'):
                dictSaida = {}
                for n in node:
                    dictSaida[n.tag] = unicode(n.text).encode('latin1')
                    if n.tag == 'escalacao':
                        registrosEscalacao = []
                        for child in n.getiterator('jogador'):
                            dictSaidaEscalacao = {}
                            for c in child:
                                dictSaidaEscalacao[c.tag] = unicode(c.text).encode('latin1')
                            registrosEscalacao.append(dictSaidaEscalacao)
                    if n.tag == 'substituicoes':
                        registrosSubstituicoes = []
                        for child in n.getiterator('novo_jogador'):
                            dictSaidaSubstituicao = {}
                            for c in child:
                                dictSaidaSubstituicao[c.tag] = unicode(c.text).encode('latin1')
                            registrosSubstituicoes.append(dictSaidaSubstituicao)
                registros.append(dictSaida)

            for i in registros:
                id_time2 = self.execSql("select_next_time_xml_seq").next()["next"]
                nome_time2 = i['nome']
                self.execSqlBatch("insert_time_xml",
                                  id_time=id_time2,
                                  id_conteudo=int(id_conteudo),
                                  nome=i['nome'],
                                  sigla=i['sigla'],
                                  esquema_tatico=i['formacao'],
                                  tecnico=i.get('tecnico',None),
                                  gols=int(i['gols']),
                                  penalts=int(i['penalts']),
                                  id_time_externo=int(i['id']))
                self.execSqlCommit()

            for i in registrosEscalacao:
                self.execSqlBatch("insert_escalacao_xml",
                                  id_time=id_time2,
                                  nome=i['nome'],
                                  posicao=i['posicao'],
                                  gols=int(i['gol']),
                                  amarelo=int(i['amarelo']),
                                  amarelo2=int(i['amarelo2']),
                                  vermelho=int(i['vermelho']),
                                  substituido=int(i['substituir']),
                                  id_jogador=int(i['id']),
                                  gol_contra=int(i['golcontra']))
                self.execSqlCommit()

            for i in registrosSubstituicoes:
                self.execSqlBatch("insert_substituicoes",
                                  id_time=id_time2,
                                  nome=i['nome'],
                                  posicao=i['posicao'],
                                  gols=int(i['gol']),
                                  amarelo=int(i['amarelo']),
                                  amarelo2=int(i['amarelo2']),
                                  vermelho=int(i['vermelho']),
                                  substituido=int(i['substituir']),
                                  id_jogador=int(i['id']),
                                  id_jogador_substituido=int(i['id_jogador_substituido']),
                                  gol_contra=int(i['golcontra']))
                self.execSqlCommit()

            #self.insere_xml_processado(arq_xml=arq_xml)
            self.execSqlCommit()
            titulo = nome_time1 + " X " + nome_time2

            if (len(registrosEscalacao) > 0):
                possui_narracao = '1'
            else:
                possui_narracao = '0'

            self.execSqlBatch("update_partida_xml_addtime",
                              id_time1=int(id_time1),
                              id_time2=int(id_time2),
                              titulo=titulo,
                              possui_narracao=possui_narracao,
                              id_conteudo=int(id_conteudo))
            self.execSqlCommit()
            #if primeiro_acesso:
            try:
                portal._addConteudo(env_site=self.id_site,
                                id_pk=int(id_conteudo),
                                schema=self.schema,
                                meta_type=self.meta_type,
                                id_aplicativo=None,
                                id_treeapp=campeonato_h2['id_tree'],
                                titulo=titulo,
                                publicado=True,
                                #publicado_em=agora,
                                publicado_em=data_hora_partida,
                                expira_em=agora,
                                titulo_destaque="",
                                descricao_destaque="",
                                imagem_destaque="",
                                permissao=None,
                                tags='aovivo')
            except Exception, e:
                import traceback as t

                erros = chr(13) + chr(10) + str(e) + '  ' + chr(13) + chr(10) + str(t.format_exc())

                log_erro.write('------------------\n')
                log_erro.write(erros + '\n')
                log_erro.write('------------------\n')

            portal._exportarConteudo(schema=self.schema,
                                      id_aplicativo=None,
                                      id_conteudo=int(id_conteudo))

        if iniciado: #and not(finalizado):

            self.execSqlu("limpa_narracao_xml", id_conteudo=int(id_conteudo))

            for i in reg_narracao:
                if (len(i) > 0):
                    if (i['tempo'] == '1º Tempo'):
                        tempo1 = 1
                    elif(i['tempo'] == '2º Tempo'):
                        tempo1 = 2
                    elif(i['tempo'] == '1º Prorrogação'):
                        tempo1 = 3
                    elif(i['tempo'] == '2º Prorrogação'):
                        tempo1 = 4
                    elif(i['tempo'] == 'Penalts'):
                        tempo1 = 5

                    self.execSqlBatch("insert_narracao_xml",
                                  id_narracao=int(i['id']),
                                  id_conteudo=int(id_conteudo),
                                  acao=i['acao'],
                                  jogador1=i['jogador1'],
                                  jogador2=i['jogador2'],
                                  tempo=tempo1,
                                  texto=i['texto'],
                                  minuto=int(i['minuto']),
                                  time=i['time'])
            self.execSqlCommit()

            partida = self.execSql("select_partida", id_conteudo=int(id_conteudo)).next()

            self.execSqlu("limpa_escalacao_xml", id_time=int(partida['id_time1']))

            registrosEscalacao = []
            registrosSubstituicoes = []
            registros = []
            for node in root.getiterator('time1'):
                dictSaida = {}
                for n in node:
                    dictSaida[n.tag] = unicode(n.text).encode('latin1')
                    if n.tag == 'escalacao':
                        registrosEscalacao = []
                        for child in n.getiterator('jogador'):
                            dictSaidaEscalacao = {}
                            for c in child:
                                dictSaidaEscalacao[c.tag] = unicode(c.text).encode('latin1')
                            registrosEscalacao.append(dictSaidaEscalacao)
                    if n.tag == 'substituicoes':
                        registrosSubstituicoes = []
                        for child in n.getiterator('novo_jogador'):
                            dictSaidaSubstituicao = {}
                            for c in child:
                                dictSaidaSubstituicao[c.tag] = unicode(c.text).encode('latin1')
                            registrosSubstituicoes.append(dictSaidaSubstituicao)
                registros.append(dictSaida)

            for i in registros:
                nome_time1 = i['nome']
                self.execSqlBatch("update_time_xml",
                                  gols=int(i['gols']),
                                  penalts=int(i['penalts']),
                                  tecnico=i.get('tecnico',None),
                                  id_time=partida['id_time1'],
                                  id_time_externo=int(i['id']))
                self.execSqlCommit()

            for i in registrosEscalacao:
                self.execSqlBatch("insert_escalacao_xml",
                                  id_time=partida['id_time1'],
                                  nome=i['nome'],
                                  posicao=i['posicao'],
                                  gols=int(i['gol']),
                                  amarelo=int(i['amarelo']),
                                  amarelo2=int(i['amarelo2']),
                                  vermelho=int(i['vermelho']),
                                  substituido=int(i['substituir']),
                                  id_jogador=int(i['id']),
                                  gol_contra=int(i['golcontra']))
                self.execSqlCommit()

            for i in registrosSubstituicoes:
                self.execSqlBatch("insert_substituicoes",
                                  id_time=partida['id_time1'],
                                  nome=i['nome'],
                                  posicao=i['posicao'],
                                  gols=int(i['gol']),
                                  amarelo=int(i['amarelo']),
                                  amarelo2=int(i['amarelo2']),
                                  vermelho=int(i['vermelho']),
                                  substituido=int(i['substituir']),
                                  id_jogador=int(i['id']),
                                  id_jogador_substituido=int(i['id_jogador_substituido']),
                                  gol_contra=int(i['golcontra']))
                self.execSqlCommit()

            self.execSqlu("limpa_escalacao_xml", id_time=int(partida['id_time2']))

            registrosEscalacao = []
            registrosSubstituicoes = []
            registros = []
            for node in root.getiterator('time2'):
                dictSaida = {}
                for n in node:
                    dictSaida[n.tag] = unicode(n.text).encode('latin1')
                    if n.tag == 'escalacao':
                        registrosEscalacao = []
                        for child in n.getiterator('jogador'):
                            dictSaidaEscalacao = {}
                            for c in child:
                                dictSaidaEscalacao[c.tag] = unicode(c.text).encode('latin1')
                            registrosEscalacao.append(dictSaidaEscalacao)
                    if n.tag == 'substituicoes':
                        registrosSubstituicoes = []
                        for child in n.getiterator('novo_jogador'):
                            dictSaidaSubstituicao = {}
                            for c in child:
                                dictSaidaSubstituicao[c.tag] = unicode(c.text).encode('latin1')
                            registrosSubstituicoes.append(dictSaidaSubstituicao)
                registros.append(dictSaida)

            for i in registros:
                nome_time2 = i['nome']
                self.execSqlBatch("update_time_xml",
                                  gols=int(i['gols']),
                                  penalts=int(i['penalts']),
                                  tecnico=i.get('tecnico',None),
                                  id_time=partida['id_time2'],
                                  id_time_externo=int(i['id']))
                self.execSqlCommit()

            for i in registrosEscalacao:
                self.execSqlBatch("insert_escalacao_xml",
                                  id_time=partida['id_time2'],
                                  nome=i['nome'],
                                  posicao=i['posicao'],
                                  gols=int(i['gol']),
                                  amarelo=int(i['amarelo']),
                                  amarelo2=int(i['amarelo2']),
                                  vermelho=int(i['vermelho']),
                                  substituido=int(i['substituir']),
                                  id_jogador=int(i['id']),
                                  gol_contra=int(i['golcontra']))
                self.execSqlCommit()

            for i in registrosSubstituicoes:
                self.execSqlBatch("insert_substituicoes",
                                  id_time=partida['id_time2'],
                                  nome=i['nome'],
                                  posicao=i['posicao'],
                                  gols=int(i['gol']),
                                  amarelo=int(i['amarelo']),
                                  amarelo2=int(i['amarelo2']),
                                  vermelho=int(i['vermelho']),
                                  substituido=int(i['substituir']),
                                  id_jogador=int(i['id']),
                                  id_jogador_substituido=int(i['id_jogador_substituido']),
                                  gol_contra=int(i['golcontra']))
                self.execSqlCommit()

            titulo = nome_time1 + " X " + nome_time2

            if (len(registrosEscalacao) > 0):
                possui_narracao = '1'

                self.execSqlBatch("update_partida_xml_addtime",
                                  id_time1=int(partida['id_time1']),
                                  id_time2=int(partida['id_time2']),
                                  titulo=titulo,
                                  possui_narracao=possui_narracao,
                                  id_conteudo=int(id_conteudo))
                self.execSqlCommit()

##            titulo = nome_time1 + " X " + nome_time2
##            portal._editConteudo(env_site=self.id_site,
##                                 id_pk=int(id_conteudo),
##                                 id_aplicativo=None,
##                                 schema=self.schema,
##                                 id_treeapp=campeonato_h2['id_tree'],
##                                 titulo=titulo,
##                                 publicado=True,
##                                 publicado_em=agora,
##                                 expira_em=agora,
##                                 titulo_destaque="",
##                                 descricao_destaque="",
##                                 imagem_destaque="",
##                                 permissao=None,
##                                 tags='aovivo')

            try:
                portal._exportarConteudo(schema=self.schema,
                                      id_aplicativo=None,
                                      id_conteudo=int(id_conteudo))
            except Exception, e:
                import traceback as t

                erros = chr(13) + chr(10) + str(e) + '  ' + chr(13) + chr(10) + str(t.format_exc())

                log_erro.write('------------------\n')
                log_erro.write(erros + '\n')
                log_erro.write('------------------\n')

        log_erro.close()


    @dbconnectionapp
    @Permission("PERM APP")
    def atualiza_estatisticas_xml(self, arq_xml):
        log_erro = open('/tmp/_atualiza_estatisticas_xml.txt', 'ab')
        log_erro.write('--I\n')
        try:
            registros   = self.parser_xml_stats(arq_xml)
            id_conteudo = arq_xml.split('_')[5]

            partida = self.execSql("select_partida", id_conteudo=int(id_conteudo)).next()

            if (partida['id_time1'] != None):
                self.execSqlu("limpa_estatistica_xml", id_time=int(partida['id_time1']))

                k = 0
                while k < registros['time1']['num_itens']:
                    k = k + 1
                    self.execSqlBatch("insert_estatistica_xml",
                                      id_time=int(partida['id_time1']),
                                      descricao=str(registros['time1']['descricao' + str(k)]).title().replace('ÇÕE', 'çõe').replace('ÃO', 'ão'),
                                      valor=int(registros['time1']['valor' + str(k)]))

            if (partida['id_time2'] != None):
                self.execSqlu("limpa_estatistica_xml", id_time=int(partida['id_time2']))

                k = 0
                while k < registros['time2']['num_itens']:
                    k = k + 1
                    self.execSqlBatch("insert_estatistica_xml",
                                      id_time=int(partida['id_time2']),
                                      descricao=str(registros['time2']['descricao' + str(k)]).title().replace('ÇÕE', 'çõe').replace('ÃO', 'ão'),
                                      valor=int(registros['time2']['valor' + str(k)]))
            self.execSqlCommit()
        except Exception, e:
            import traceback as t

            erros = chr(13) + chr(10) + str(e) + '  ' + chr(13) + chr(10) + str(t.format_exc())
            log_erro.write(erros + '\n')

        log_erro.write('--F\n')
        log_erro.write('------------------------------\n')
        log_erro.close()
        chmod('/tmp/_atualiza_estatisticas_xml.txt', 0777)


    @Permission("PERM APP")
    def parser_xml_stats(self, arq_xml):
        from packages.elementtree import ElementTree as ET

        path_xml = self.path_base + arq_xml

        try:
            root = ET.parse(path_xml)
        except:
            return ''

        dictSaida = {}

        for node in root.getiterator('partida'):
            for n in node:
                dictSaida[n.tag] = unicode(n.text).encode('latin1')

        for node in root.getiterator('time1'):
            time1 = {}
            for n in node:
                if n.tag == 'estatisticas':
                    k = 0
                    for n2 in n.getiterator('item'):
                        key = ''
                        val = ''
                        for n3 in n2:
                            if (n3.tag == 'descricao'):
                                key = unicode(n3.text).encode('latin1')
                            elif (n3.tag == 'valor'):
                                val = unicode(n3.text).encode('latin1')

                        k = k + 1

                        if (key != ''):
                            time1['descricao' + str(k)] = key
                            time1['valor' + str(k)] = val

                    time1['num_itens'] = k
                else:
                    time1[n.tag] = unicode(n.text).encode('latin1')

            dictSaida['time1'] = time1

        for node in root.getiterator('time2'):
            time2 = {}
            for n in node:
                if n.tag == 'estatisticas':
                    k = 0
                    for n2 in n.getiterator('item'):
                        key = ''
                        val = ''
                        for n3 in n2:
                            if (n3.tag == 'descricao'):
                                key = unicode(n3.text).encode('latin1')
                            elif (n3.tag == 'valor'):
                                val = unicode(n3.text).encode('latin1')

                        k = k + 1

                        if (key != ''):
                            time2['descricao' + str(k)] = key
                            time2['valor' + str(k)] = val

                    time2['num_itens'] = k
                else:
                    time2[n.tag] = unicode(n.text).encode('latin1')

            dictSaida['time2'] = time2

        return dictSaida

    @dbconnectionapp
    @Permission("PERM APP")
    def atualiza_campeonatos_xml(self, arq_xml):
        registros = self.parser_xml_padrao(arq_xml)

        self.execSqlu("limpa_campeonatos_aovivo_xml")

        for i in registros:
            self.execSqlBatch("insert_campeonato_xml",
                              id_campeonato_aovivo=int(i['id']),
                              nome=i['campeonato'])

        #self.insere_xml_processado(arq_xml=arq_xml)
        self.execSqlCommit()

    @dbconnectionapp
    @Permission("PERM APP")
    def insere_xml_processado(self, arq_xml):
        agora = datetime.now()
        try:
            arq_aberto = open(self.path_base + arq_xml, 'rb')
            arq_content = arq_aberto.read()
            bytes_xml = len(arq_content)
        finally:
            arq_aberto.close()
        xmls_processados = self.checa_xmls_processados(arq_xml=arq_xml)
        if self.possuiDados(xmls_processados):
            xmls_processados.next()
            self.execSqlBatch("update_xmls_processados",
                               bytes_xml=bytes_xml,
                               ultima_alteracao=agora,
                               id_xml=int(xmls_processados.next()['id_xml']))
        else:
            self.execSqlBatch("insert_xmls_processados",
                               nome_xml=arq_xml,
                               bytes_xml=bytes_xml,
                               ultima_alteracao=agora)

    @Permission("PERM APP")
    def parser_xml_padrao(self, arq_xml):
        #import elementtree.ElementTree as ET
        from packages.elementtree import ElementTree as ET
        registros = []
        path_xml = self.path_base + arq_xml
        try:
            root = ET.parse(path_xml)
        except:
            return ''
        for node in root.getiterator('item'):
            dictSaida = {}
            for n in node:
                dictSaida[n.tag] = unicode(n.text).encode('latin1')
            registros.append(dictSaida)
        return registros

    @Permission("PERM APP")
    def getDadosXML(self, arq_xml, nome_no):
        from packages.elementtree import ElementTree as ET
        path_xml = self.path_base + arq_xml

        try:
            root = ET.parse(path_xml)
        except:
            return ''

        for node in root.getiterator(nome_no):
            return unicode(node.text).encode('latin1')

    @dbconnectionapp
    @Permission("PERM APP")
    def atualiza_artilharia_xml(self, arq_xml):
        registros = self.parser_xml_padrao(arq_xml)
        id_campeonato = arq_xml.split('_')[3]
        id_campeonato_h2 = self.execSql("select_campeonato_h2", id_campeonato_aovivo=int(id_campeonato)).next()
        id_campeonato_h2 = id_campeonato_h2['id_campeonato']

        self.execSqlu("limpa_artilharia_xml", id_campeonato=int(id_campeonato_h2))

        for i in registros:
            self.execSqlBatch("insert_artilharia_xml",
                              id_campeonato=int(id_campeonato_h2),
                              nome_jogador=i['jogador'],
                              quantidade_gols=int(i['gols']),
                              time_jogador=i['time'])

        #self.insere_xml_processado(arq_xml=arq_xml)
        self.execSqlCommit()

    @dbconnectionapp
    @Permission("PERM APP")
    def atualiza_classificacao_xml(self, arq_xml):
        registros = self.parser_xml_padrao(arq_xml)
        id_campeonato = arq_xml.split('_')[3]
        campeonato_h2 = self.execSql("select_campeonato_h2", id_campeonato_aovivo=int(id_campeonato)).next()
        id_campeonato_h2 = campeonato_h2['id_campeonato']

        self.execSqlu("limpa_classificacao_xml", id_campeonato=int(id_campeonato_h2))

        for i in registros:
            self.execSqlBatch("insert_classificacao_xml",
                              id_campeonato=int(id_campeonato_h2),
                              sigla_time=i['sigla'],
                              id_time=int(i['id']),
                              nome_time=i['time'],
                              pontos=int(i['pg']),
                              vitorias=int(i['v']),
                              empates=int(i['e']),
                              derrotas=int(i['d']),
                              gols_marcados=int(i['gp']),
                              qtd_jogos=int(i['j']),
                              gols_sofridos=int(i['gc']),
                              saldo_gols=int(i['sg']),
                              ordem=int(i['ordem']))
        #self.insere_xml_processado(arq_xml=arq_xml)
        self.execSqlCommit()

        ids_portlets = campeonato_h2.get('ids_pagina_portlet', None)

        if(ids_portlets):
            ids_portlets = eval(ids_portlets)
            lista_ids_portlets = []
            for i in ids_portlets:
                for j in ids_portlets[i]:
                    lista_ids_portlets.append(j)
            portal = Portal(id_site=self.id_site, request=self.request)
            portal.publicarPortlet(env_site=self.id_site,
                               portlets=lista_ids_portlets)

    @dbconnectionapp
    @Permission("PERM APP")
    def atualiza_resultados_xml(self, arq_xml):
        portal    = Portal(id_site=self.id_site, request=self.request)
        registros = self.parser_xml_padrao(arq_xml)

        id_campeonato    = arq_xml.split('_')[3]
        campeonato_h2    = self.execSql("select_campeonato_h2", id_campeonato_aovivo=int(id_campeonato)).next()
        id_campeonato_h2 = campeonato_h2['id_campeonato']
        agora            = datetime.now()

        titulo = self.getDadosXML(arq_xml, 'titulo')
        texto  = self.getDadosXML(arq_xml, 'texto')

        self.execSqlu("limpa_resultados_xml", id_campeonato=int(id_campeonato_h2))

        for i in registros:
            if i['ini'] == None or i['ini'] == 'None' : i['ini'] = 0
            if i['fim'] == None or i['fim'] == 'None' : i['fim'] = 0
            data_hora = i['data'] + " " + i['hora'].replace('h','').ljust(4,'0')
            d = strptime(data_hora, "%d/%m/%Y %H%M")
            data_hora = strftime("%Y-%m-%d %H%M", d)
            self.execSqlBatch("insert_resultados_xml",
                              id_campeonato=int(id_campeonato_h2),
                              id_partida_aovivo=int(i['id']),
                              nome_time1=i['time1'],
                              nome_time2=i['time2'],
                              sigla_time1=i.get('sigla1',''),
                              sigla_time2=i.get('sigla2',''),
                              data_hora=data_hora,
                              fase=i['rodada'],
                              estadio=i['estadio'],
                              cidade=i['local'],
                              gols_time1=int(i['gol1']),
                              gols_time2=int(i['gol2']),
                              inicio=int(i['ini']),
                              fim=int(i['fim']))
            self.execSqlCommit()

            data_hora_partida = datetime.strptime(i['data'] + ' ' +
                                    i['hora'].replace('h', '').replace(':', ''),'%d/%m/%Y %H%M').strftime('%Y-%m-%d %H:%M')

            if not self.possuiDados(self.checa_partida(id_conteudo=int(i['id']))):
                    self.gera_xml_partida(id_campeonato,
                                        titulo,
                                        texto,
                                        i['id'],
                                        i['rodada'],
                                        i['data'],
                                        i['hora'],
                                        i['local'],
                                        i['estadio'],
                                        i['tid1'],
                                        i['time1'],
                                        i['sigla1'],
                                        i['tid2'],
                                        i['time2'],
                                        i['sigla2'])

        self.execSqlCommit()

    @dbconnectionapp
    @Permission("PERM APP")
    def atualiza_partidas_alteradas(self, arq_xml):
        portal    = Portal(id_site=self.id_site, request=self.request)
        registros = self.parser_xml_padrao(arq_xml)

        id_campeonato    = arq_xml.split('_')[3]
        campeonato_h2    = self.execSql("select_campeonato_h2", id_campeonato_aovivo=int(id_campeonato)).next()
        id_campeonato_h2 = campeonato_h2['id_campeonato']
        agora            = datetime.now()

        for i in registros:
            import time
            data_atual_comp = str(time.strftime('%Y')) + str(time.strftime('%m')) + str(time.strftime('%d'))
            #data_atual_comp = str(agora.year) + str(agora.month) + str(agora.day)
            data_jogo_comp = i['data'].split('/')
            data_jogo_comp = str(data_jogo_comp[2]) + str(data_jogo_comp[1]) + str(data_jogo_comp[0])
            if(int(data_jogo_comp) >= int(data_atual_comp)):
                titulo = str(i['time1']) + " X " + str(i['time2'])
                hora_jogo  = self.trataHora(i['hora'])
                data_hora_partida = datetime.strptime(i['data'] + ' ' + hora_jogo,'%d/%m/%Y %H%M').strftime('%Y-%m-%d %H:%M')

                portal._editConteudo(env_site=self.id_site,
                         id_pk=int(i['id']),
                         id_aplicativo=41,
                         schema=self.schema,
                         id_treeapp=campeonato_h2['id_tree'],
                         titulo=titulo,
                         publicado=True,
                         publicado_em=data_hora_partida,
                         expira_em=agora,
                         titulo_destaque="",
                         descricao_destaque="",
                         imagem_destaque="",
                         permissao=None,
                         tags='aovivo')

                self.execSqlBatch("update_partida_alterada",
                                   titulo=titulo,
                                   data_hora=data_hora_partida,
                                   local=i['local'],
                                   estadio=i['estadio'],
                                   id_conteudo=int(i['id']))

                self.execSqlBatch("update_time_partida_alterada",
                                   nome=i['time1'],
                                   sigla=i['sigla1'],
                                   id_conteudo=int(i['id']),
                                   id_time_externo=int(i['tid1']))

                self.execSqlBatch("update_time_partida_alterada",
                                   nome=i['time2'],
                                   sigla=i['sigla2'],
                                   id_conteudo=int(i['id']),
                                   id_time_externo=int(i['tid2']))
                #NOTE: Export
                portal._addExportSub(id_site=self.id_site,
                                     id_treeapp=campeonato_h2['id_tree'],
                                     id_conteudo=int(i['id']))

        self.execSqlCommit()



    def gera_xml_partida(self, campeonato_id,
                                titulo,
                                texto,
                                partida_id,
                                rodada,
                                data,
                                hora,
                                local,
                                estadio,
                                t1_id,
                                t1_nome,
                                t1_sigla,
                                t2_id,
                                t2_nome,
                                t2_sigla):
        import shutil

        if (local == None or local == 'None' or local == ''):
            local = "-"

        if (estadio == None or estadio == 'None' or estadio == ''):
            estadio = "-"

        arq_name = "cli_8_cam_" + campeonato_id + "_par_" + partida_id + ".xml";

        arq = open('/tmp/' + arq_name, 'w')

        arq.write("<?xml version=\"1.0\" encoding=\"iso-8859-1\"?>")
        arq.write("<campeonato><id>" + str(campeonato_id) + "</id>")
        arq.write("<titulo>" + str(titulo) + "</titulo>")
        arq.write("<texto>" + str(texto) + "</texto>")
        arq.write("<partida><id>" + str(partida_id) + "</id>")
        arq.write("<rodada>" + str(rodada) + "</rodada>")
        arq.write("<data>" + str(data) + "</data>")
        arq.write("<hora>" + str(hora) + "</hora>")
        arq.write("<jogoini>0</jogoini><jogofim>0</jogofim>")
        arq.write("<intervalo></intervalo>")
        arq.write("<local>" + str(local) + "</local>")
        arq.write("<estadio>" + str(estadio) + "</estadio>")
        arq.write("<arbitro>-</arbitro>")
        arq.write("<auxiliar1>-</auxiliar1>")
        arq.write("<auxiliar2>-</auxiliar2>")
        arq.write("<top></top>")
        arq.write("<time1><id>" + str(t1_id) + "</id>")
        arq.write("<nome>" + str(t1_nome) + "</nome>")
        arq.write("<sigla>" + str(t1_sigla) + "</sigla>")
        arq.write("<formacao>3-5-2</formacao>")
        arq.write("<gols>0</gols><penalts>0</penalts><tecnico>-</tecnico>")
        arq.write("<escalacao></escalacao></time1>")
        arq.write("<time2><id>" + str(t2_id) + "</id>")
        arq.write("<nome>" + str(t2_nome) + "</nome>")
        arq.write("<sigla>" + str(t2_sigla) + "</sigla>")
        arq.write("<formacao>3-5-2</formacao>")
        arq.write("<gols>0</gols><penalts>0</penalts><tecnico>-</tecnico>")
        arq.write("<escalacao></escalacao></time2>")
        arq.write("</partida></campeonato>")
        arq.close()

        try:
            shutil.move('/tmp/' + arq_name, self.path_base + "/" + arq_name)
            chmod(self.path_base + "/" + arq_name, 0777)
        except:
            pass


    @dbconnectionapp
    def _get_resultados_aovivo(self, id_campeonato):
        try:
            import datetime

            if (id_campeonato):
                agora    = datetime.datetime.now()
                amanha   = agora + datetime.timedelta(days=1)
                data_fim = str(amanha.year) + '-' + str(amanha.month) + '-' + str(amanha.day) + ' 00:00'

                res = self.execSql("select_max_data_resultados_aovivo_rodada_o1", id_campeonato=int(id_campeonato), data_fim=data_fim)
                if (self.possuiDados(res)):
                    res = self.execSql("select_max_data_resultados_aovivo_rodada_o1", id_campeonato=int(id_campeonato), data_fim=data_fim).next()
                    return self.execSql("select_resultados_aovivo_rodada",
                                        id_campeonato=int(id_campeonato),
                                        id_aplicativo=41,
                                        rodada=str(res['rodada']))
                else:
                    res = self.execSql("select_max_data_resultados_aovivo_rodada_o2", id_campeonato=int(id_campeonato))

                    if (self.possuiDados(res)):
                        res = self.execSql("select_max_data_resultados_aovivo_rodada_o2", id_campeonato=int(id_campeonato)).next()
                        return self.execSql("select_resultados_aovivo_rodada",
                                        id_campeonato=int(id_campeonato),
                                        id_aplicativo=41,
                                        rodada=str(res['rodada']))
        except Exception, e:
            import traceback as t

            erros = chr(13) + chr(10) + str(e) + '  ' + chr(13) + chr(10) + str(t.format_exc())

    @dbconnectionapp
    def _get(self, sql, _id):
        return self.execSql(sql, _id = _id)




#portal.deleteConteudo(env_site=id_site, id_treeapp,=id_treeapp, items=[{"id_aplicativo":123, id_conteudo":213423, meta_type":"meta_type", "schema":"schema_9879879"}, ...])
