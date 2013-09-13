# -*- encoding: iso8859-1 -*-
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
from datetime import datetime
from time import time, strftime, strptime
from publica.utils.decorators import serialize, dbconnectionapp,\
                                     Permission, logportal
from publica.core.portal import Portal
from publica.admin.error import UserError
from publica.utils.json import encode


class Adm(object):
    """
    """
    #id_categoria, imagem, 
    @dbconnectionapp
    @serialize
    @Permission("PERM APP")
    def addContent(self, id_treeapp, id_aplicativo, publicado_em,
                         fabricante, modelo, modelo_extendido, 
                         ano_modelo, codigo_fipe,  
                         ano_fabricacao, titulo, ordem,
                         titulo_destaque=None, descricao_destaque=None,
                         imagem_destaque=None, tags="",
                         relacionamento=[], expira_em=None,
                         publicado=None, permissao=None,
                         exportar=None, exportar_json=None, exportar_xml=None):
        """
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        id_conteudo = self.execSql("select_nextval_conteudo").next()["id"]

        publicado = True if publicado else False
        tags = tags if tags else None

        dt = publicado_em
        try:
            p = strptime(publicado_em, '%d/%m/%Y %H:%M')
            publicado_em = strftime('%Y-%m-%d %H:%M', p)
        except ValueError, e:
            raise UserError(("Ocorreu um erro: "
                             "Data de publica&ccedil;&aring;o "
                             "inv&aacute;lida (%s)" % publicado_em))

        try:
            p = strptime(expira_em, "%d/%m/%Y %H:%M")
            expira_em = strftime("%Y-%m-%d %H:%M", p)
        except ValueError, e:
           expira_em = None

        #if not imagem: 
        #    imagem = None
        #else:
        #    imagem = portal.addArquivo(arquivo=imagem,
        #                               id_conteudo=id_conteudo,
        #                               schema=self.schema,
        #                              dt=dt)
        try:
            ordem = int(ordem)
        except Exception:
            raise UserError(("A ordem deve ser um inteiro"))

        self.execSqlBatch("insert_conteudo",
                          id_conteudo=id_conteudo,
                          #id_categoria=int(id_categoria),
                          fabricante=fabricante,
                          modelo=modelo,
                          modelo_extendido=modelo_extendido,
                          ano_modelo=ano_modelo,
                          ano_fabricacao=ano_fabricacao,
                          titulo=titulo,
                          codigo_fipe=codigo_fipe,
                          #imagem=imagem,
                          ordem=ordem,
                          aval_design=0.0,
                          aval_performance=0.0,
                          aval_conforto_acabamento=0.0,
                          aval_dirigibilidade=0.0,
                          aval_consumo=0.0,
                          aval_manutencao=0.0,
                          aval_custo_beneficio=0.0,
                          publicado=publicado,
                          publicado_em=publicado_em,
                          expira_em=expira_em)

        if titulo_destaque or imagem_destaque or descricao_destaque:
            if not imagem_destaque: 
                imagem_destaque = None
            else:
                imagem_destaque = portal.addArquivo(arquivo=imagem_destaque,
                                                    id_conteudo=id_conteudo,
                                                    schema=self.schema,
                                                    dt=dt)
            self.execSqlBatch("insert_destaque",
                              id_conteudo=id_conteudo,
                              titulo=titulo_destaque,
                              descricao=descricao_destaque,
                              imagem=imagem_destaque)


        self.execSqlCommit() 
        self._setRanking()
        dados = self._setDados(id_conteudo=id_conteudo)
        portal._addConteudo(env_site=self.id_site,
                            id_pk=id_conteudo,
                            id_aplicativo=id_aplicativo,
                            schema=self.schema,
                            meta_type=self.meta_type,
                            id_treeapp=id_treeapp,
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

        if exportar or exportar_json or exportar_xml:
            portal._insertLog(self.id_site,
            "Vrum Avalia&ccedil;&atilde;o '%s' adicionada e publicada" % titulo)

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

            return ("Vrum Avalia&ccedil;&atilde;o adicionada com sucesso! "
                    "Publica&ccedil;&atilde;o iniciada.")

        portal._insertLog(self.id_site,
                       "Vrum Avalia&ccedil;&atilde;o '%s' publicada" % titulo)
        return "Vrum Avalia&ccedil;&atilde;o adicionada com sucesso!"

    #id_categoria, imagem, 
    @dbconnectionapp
    @serialize
    #@Permission("PERM APP")
    def editContent(self, id_conteudo, id_treeapp, id_aplicativo, publicado_em,
                          fabricante, modelo, modelo_extendido, codigo_fipe,
                          ano_modelo, ano_fabricacao, titulo,ordem,
                          titulo_destaque=None, descricao_destaque=None,
                          imagem_destaque=None, tags="",
                          relacionamento=[], expira_em=None,
                          publicado=None, permissao=None,
                          exportar=None, exportar_json=None, exportar_xml=None):
        """
        """
        id_conteudo = int(id_conteudo)
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        publicado = True if publicado else False
        tags = tags if tags else None

        dt = publicado_em
        try:
            p = strptime(publicado_em, '%d/%m/%Y %H:%M')
            publicado_em = strftime('%Y-%m-%d %H:%M', p)
        except ValueError, e:
            raise UserError(("Ocorreu um erro: "
                             "Data de publica&ccedil;&aring;o "
                             "inv&aacute;lida (%s)" % publicado_em))

        try:
            p = strptime(expira_em, "%d/%m/%Y %H:%M")
            expira_em = strftime("%Y-%m-%d %H:%M", p)
        except ValueError, e:
           expira_em = None

        try:
            ordem = int(ordem)
        except Exception:
            raise UserError(("A ordem deve ser um inteiro"))

        #if not imagem: 
        #    imagem = None
        #else:
        #    imagem = portal.addArquivo(arquivo=imagem,
        #                               id_conteudo=id_conteudo,
        #                               schema=self.schema,
        #                               dt=dt)

        self.execSqlBatch("delete_destaque",
                          id_conteudo=id_conteudo)

        self.execSqlBatch("update_conteudo",
                          id_conteudo=id_conteudo,
                          #id_categoria=int(id_categoria),
                          fabricante=fabricante,
                          modelo=modelo,
                          modelo_extendido=modelo_extendido,
                          ano_modelo=ano_modelo,
                          ano_fabricacao=ano_fabricacao,
                          titulo=titulo,
                          codigo_fipe=codigo_fipe,
                          #imagem=imagem,
                          ordem=ordem,
                          publicado=publicado,
                          publicado_em=publicado_em,
                          expira_em=expira_em)

        if titulo_destaque or imagem_destaque or descricao_destaque:
            if not imagem_destaque: 
                imagem_destaque = None
            else:
                imagem_destaque = portal.addArquivo(arquivo=imagem_destaque,
                                                    id_conteudo=id_conteudo,
                                                    schema=self.schema,
                                                    dt=dt)
            self.execSqlBatch("insert_destaque",
                              id_conteudo=id_conteudo,
                              titulo=titulo_destaque,
                              descricao=descricao_destaque,
                              imagem=imagem_destaque)


        self.execSqlCommit()
        self._setRanking()
        dados = self._setDados(id_conteudo=id_conteudo)
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
                             tags=tags,
                             relacionamento=relacionamento,
                             dados=dados)

        if exportar or exportar_xml or exportar_json:
            try:
                portal._insertLog(self.id_site,
                    "Vrum Avalia&ccedil;&atilde;o '%s' editada e publicada" % titulo)
            except:
                pass

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

            return ("Vrum Avalia&ccedil;&atilde;o editada com sucesso!"
                    " Publica&ccedil;&atilde;o iniciada.")

        portal._insertLog(self.id_site,
                          "Vrum Avalia&ccedil;&atilde;o '%s' editada" % titulo)
        return "Vrum Avalia&ccedil;&atilde;o editada com sucesso!"


    def _setRanking(self):
        """
            Algoritmo para setar o ranking:
            Existe uma tabela de indexacao ranking onde é armazenado 
            a informacao do ranking geral e 
            Sempre que algum avaliacao e adicionada/editada e alguma opiniao 
            e publica e refeito este procedimento.
        """
        aval_geral = []
        #aval_categoria = {} por categoria.

        self.execSqlBatch("delete_ranking")
        for i in self.execSql("select_conteudos"):
            total = i["aval_design"]
            total += i["aval_performance"]
            total += i["aval_conforto_acabamento"]
            total += i["aval_dirigibilidade"]
            total += i["aval_consumo"]
            total += i["aval_manutencao"]
            total += i["aval_custo_beneficio"]

            qtde = 0
            for j in self.execSql("select_opiniao_count",
                                  id_conteudo=int(i['id_conteudo'])):
                qtde = j['qtde']

            if qtde == 0:
                qtde = qtde+1
            rank = 0.0
            if total > 0.0:
                rank = total/7.0
            rank = float(rank)/float(qtde)
            aval_geral.append({"rank":rank,
                               "id_conteudo":i["id_conteudo"]})


           
                               #,"id_categoria":i["id_categoria"]

            #if not aval_categoria.get(i["id_categoria"], None):
            #    aval_categoria[i["id_categoria"]] = []
            #aval_categoria[i["id_categoria"]].append(
            #          {"rank":rank,
            #           "id_conteudo":i["id_conteudo"],
            #           "id_categoria":i["id_categoria"]})

        aval_geral = sorted(aval_geral, key=lambda x:x['rank'])
        aval_geral.reverse()
        #for i in aval_categoria:
        #    aval_categoria[i] = sorted(aval_categoria[i], key=lambda x:x["rank"])
        #    aval_categoria[i].reverse()

        rank = 1
        for i in aval_geral:

            #rank_categoria = 1
            #for j in aval_categoria[i["id_categoria"]]:
            #   if j["id_conteudo"] == i["id_conteudo"]:
            #        break
            #    rank_categoria += 1
        
            self.execSqlBatch("insert_ranking",
                              id_conteudo=i["id_conteudo"],
                              rank_geral=rank)
                              #,id_categoria=i["id_categoria"],
                              #rank_categoria=rank_categoria)
            rank += 1

        self.execSqlCommit()

    @dbconnectionapp
    @Permission("PERM APP")
    def _getIds(self):
        ids = []
        for i in self.execSql("select_ids"):
            ids.append(i['id_conteudo'])
        return ids

    @dbconnectionapp
    @Permission("PERM APP")
    def _getContent(self, id_conteudo):
        """
        """
        for i in self.execSql("select_conteudo_",
                            id_conteudo=int(id_conteudo)):
            return i


    #@dbconnectionapp
    #@Permission("PERM APP")
    #def _getCategorias(self):
    #    """
    #    """
    #    return self.execSql("select_categorias")


