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

##select_resultados_aovivo    = ("SELECT t1.id_time AS t1_id_time, t1.id_conteudo AS t1_id_conteudo, t1.nome AS t1_nome, t1.sigla AS t1_sigla, t1.esquema_tatico AS t1_esquema_tatico, t1.tecnico AS t1_tecnico, t1.gols AS t1_gols, t1.penalts AS t1_penalts,"
##                                " t2.id_time AS t2_id_time, t2.id_conteudo AS t2_id_conteudo, t2.nome AS t2_nome, t2.sigla AS t2_sigla, t2.esquema_tatico AS t2_esquema_tatico, t2.tecnico AS t2_tecnico, t2.gols AS t2_gols, t2.penalts AS t2_penalts,"
##                                " cr.id_conteudo AS con_id_conteudo, cr.id_time1 AS con_id_time1, cr.id_time2 AS con_id_time2, cr.id_idioma AS con_id_idioma, cr.titulo AS con_titulo, cr.descricao AS con_descricao, cr.embed AS con_embed,"
##                                " cr.html_videos AS con_html_videos, cr.publicado_em AS con_publicado_em, cr.expira_em AS con_expira_em, cr.publicado AS con_publicado, cr.id_campeonato AS con_id_campeonato, cr.iniciado AS con_iniciado,"
##                                " cr.finalizado AS con_finalizado, cr.arbitro AS con_arbitro, cr.auxiliar1 AS con_auxiliar1, cr.auxiliar2 AS con_auxiliar2, cr.data_hora AS con_data_hora, cr.local AS con_local, cr.estadio AS con_estadio,"
##                                " cr.rodada AS con_rodada, cr.data_hora_inicio AS con_data_hora_inicio, cr.intervalo AS con_intervalo, cr.possui_narracao AS con_possui_narracao, ce.url AS con_url"
##                                " FROM rschemar.conteudo cr"
##                                " INNER JOIN rschemar.time_xml t1 ON (t1.id_time = cr.id_time1)"
##                                " INNER JOIN rschemar.time_xml t2 ON (t2.id_time = cr.id_time2)"
##                                " INNER JOIN envsite.conteudo ce ON (cr.id_conteudo = ce.id_conteudo AND id_aplicativo = %(id_aplicativo)i)"
##                                " WHERE (cr.data_hora BETWEEN %(data_ini)s AND %(data_fim)s) AND cr.id_campeonato = %(id_campeonato)i"
##                                " ORDER BY cr.data_hora")

select_resultados_aovivo    = ("SELECT"
                                " t1.id_time AS t1_id_time, t1.id_conteudo AS t1_id_conteudo, t1.nome AS t1_nome, t1.sigla AS t1_sigla,"
                                " t1.esquema_tatico AS t1_esquema_tatico, t1.tecnico AS t1_tecnico, t1.gols AS t1_gols, t1.penalts AS t1_penalts,"
                                " t2.id_time AS t2_id_time, t2.id_conteudo AS t2_id_conteudo, t2.nome AS t2_nome, t2.sigla AS t2_sigla,"
                                " t2.esquema_tatico AS t2_esquema_tatico, t2.tecnico AS t2_tecnico, t2.gols AS t2_gols, t2.penalts AS t2_penalts,"
                                " cr.id_conteudo AS con_id_conteudo, cr.id_time1 AS con_id_time1, cr.id_time2 AS con_id_time2,"
                                " cr.id_idioma AS con_id_idioma, cr.titulo AS con_titulo, cr.descricao AS con_descricao, cr.embed AS con_embed,"
                                " cr.html_videos AS con_html_videos, cr.publicado_em AS con_publicado_em, cr.expira_em AS con_expira_em,"
                                " cr.publicado AS con_publicado, cr.id_campeonato AS con_id_campeonato, cr.iniciado AS con_iniciado,"
                                " cr.finalizado AS con_finalizado, cr.arbitro AS con_arbitro, cr.auxiliar1 AS con_auxiliar1,"
                                " cr.auxiliar2 AS con_auxiliar2, cr.data_hora AS con_data_hora, cr.local AS con_local, cr.estadio AS con_estadio,"
                                " cr.rodada AS con_rodada, cr.data_hora_inicio AS con_data_hora_inicio, cr.intervalo AS con_intervalo,"
                                " cr.possui_narracao AS con_possui_narracao,"
                                " (SELECT max(ce.url) FROM envsite.conteudo ce WHERE id_aplicativo = %(id_aplicativo)i AND cr.id_conteudo = ce.id_conteudo) AS con_url"
                                " FROM rschemar.conteudo cr"
                                " INNER JOIN rschemar.time_xml t1 ON (t1.id_time = cr.id_time1)"
                                " INNER JOIN rschemar.time_xml t2 ON (t2.id_time = cr.id_time2)"
                                " WHERE (cr.data_hora BETWEEN %(data_ini)s AND %(data_fim)s)"
                                " AND (SELECT max(ce.url) FROM envsite.conteudo ce WHERE id_aplicativo = %(id_aplicativo)i AND cr.id_conteudo = ce.id_conteudo) is not null"
                                " AND cr.id_campeonato = %(id_campeonato)i"
                                " ORDER BY cr.data_hora")

select_resultados_aovivo_rodada = ("SELECT"
                                " t1.id_time AS t1_id_time, t1.id_conteudo AS t1_id_conteudo, t1.nome AS t1_nome, t1.sigla AS t1_sigla,"
                                " t1.esquema_tatico AS t1_esquema_tatico, t1.tecnico AS t1_tecnico, t1.gols AS t1_gols, t1.penalts AS t1_penalts,"
                                " t2.id_time AS t2_id_time, t2.id_conteudo AS t2_id_conteudo, t2.nome AS t2_nome, t2.sigla AS t2_sigla,"
                                " t2.esquema_tatico AS t2_esquema_tatico, t2.tecnico AS t2_tecnico, t2.gols AS t2_gols, t2.penalts AS t2_penalts,"
                                " cr.id_conteudo AS con_id_conteudo, cr.id_time1 AS con_id_time1, cr.id_time2 AS con_id_time2,"
                                " cr.id_idioma AS con_id_idioma, cr.titulo AS con_titulo, cr.descricao AS con_descricao, cr.embed AS con_embed,"
                                " cr.html_videos AS con_html_videos, cr.publicado_em AS con_publicado_em, cr.expira_em AS con_expira_em,"
                                " cr.publicado AS con_publicado, cr.id_campeonato AS con_id_campeonato, cr.iniciado AS con_iniciado,"
                                " cr.finalizado AS con_finalizado, cr.arbitro AS con_arbitro, cr.auxiliar1 AS con_auxiliar1,"
                                " cr.auxiliar2 AS con_auxiliar2, cr.data_hora AS con_data_hora, cr.local AS con_local, cr.estadio AS con_estadio,"
                                " cr.rodada AS con_rodada, cr.data_hora_inicio AS con_data_hora_inicio, cr.intervalo AS con_intervalo,"
                                " cr.possui_narracao AS con_possui_narracao,"
                                " (SELECT max(ce.url) FROM envsite.conteudo ce WHERE id_aplicativo = %(id_aplicativo)i AND cr.id_conteudo = ce.id_conteudo) AS con_url"
                                " FROM rschemar.conteudo cr"
                                " INNER JOIN rschemar.time_xml t1 ON (t1.id_time = cr.id_time1)"
                                " INNER JOIN rschemar.time_xml t2 ON (t2.id_time = cr.id_time2)"
                                " WHERE (cr.rodada = %(rodada)s)"
                                " AND (SELECT max(ce.url) FROM envsite.conteudo ce WHERE id_aplicativo = %(id_aplicativo)i AND cr.id_conteudo = ce.id_conteudo) is not null"
                                " AND cr.id_campeonato = %(id_campeonato)i"
                                " ORDER BY cr.data_hora")

select_max_data_resultados_aovivo = ("SELECT MAX(data_hora) as max_data_hora FROM rschemar.conteudo "
                                    " WHERE id_campeonato = %(id_campeonato)i AND data_hora <= %(data_fim)s")

select_max_data_resultados_aovivo_rodada_o1 = ("SELECT data_hora, rodada FROM rschemar.conteudo "
                                    " WHERE id_campeonato = %(id_campeonato)i AND data_hora <= %(data_fim)s "
                                    " ORDER BY data_hora DESC LIMIT 1 OFFSET 0")

select_max_data_resultados_aovivo_rodada_o2 = ("SELECT data_hora, rodada FROM rschemar.conteudo "
                                    " WHERE id_campeonato = %(id_campeonato)i "
                                    " ORDER BY data_hora LIMIT 1 OFFSET 0")

select_resultados_max_4     = ("SELECT nome_time1, nome_time2, gols_time1, gols_time2, fase, to_char(data_hora, 'dd/mm/YYYY HH24:MI') as data_hora_f, data_hora, inicio"
                               " FROM rschemar.resultados"
                               " WHERE id_campeonato=%(id_campeonato)i"
                               " ORDER BY data_hora DESC LIMIT 4 OFFSET 0")

select_resultados_max_10_o1  = ("SELECT nome_time1, nome_time2, sigla_time1, sigla_time2, gols_time1, gols_time2, fase, to_char(data_hora, 'dd/mm/YYYY HH24:MI') as data_hora_f, data_hora, inicio, fim"
                               " FROM rschemar.resultados"
                               " WHERE id_campeonato = %(id_campeonato)i AND (data_hora BETWEEN %(data_ini)s AND %(data_fim)s)"
                               " ORDER BY data_hora LIMIT 10 OFFSET 0")

select_resultados_max_10_o2  = ("SELECT nome_time1, nome_time2, sigla_time1, sigla_time2, gols_time1, gols_time2, fase, to_char(data_hora, 'dd/mm/YYYY HH24:MI') as data_hora_f, data_hora, inicio, fim"
                               " FROM rschemar.resultados"
                               " WHERE id_campeonato = %(id_campeonato)i AND data_hora < %(data_ini)s"
                               " ORDER BY data_hora DESC LIMIT 10 OFFSET 0")

select_resultados_max_10_o3  = ("SELECT nome_time1, nome_time2, sigla_time1, sigla_time2, gols_time1, gols_time2, fase, to_char(data_hora, 'dd/mm/YYYY HH24:MI') as data_hora_f, data_hora, inicio, fim"
                               " FROM rschemar.resultados"
                               " WHERE id_campeonato = %(id_campeonato)i"
                               " ORDER BY data_hora LIMIT 10 OFFSET 0")

select_resultados_max_o1_grupo = ("SELECT r.nome_time1, r.nome_time2, r.sigla_time1, r.sigla_time2, r.gols_time1, r.gols_time2, r.fase,"
                               " to_char(r.data_hora, 'dd/mm/YYYY HH24:MI') as data_hora_f, r.data_hora, r.inicio, r.fim"
                               " FROM rschemar.resultados r"
                               " INNER JOIN rschemar.campeonato c "
                               " ON r.id_campeonato = c.id_campeonato AND c.id_campeonato_aovivo IN (SELECT ocg2.id_campeonato "
                               " FROM rschemar.campeonato oc"
                               " LEFT JOIN rschemar.campeonato_grupo_rel ocg ON oc.id_campeonato_aovivo = ocg.id_campeonato"
                               " LEFT JOIN rschemar.campeonato_grupo_rel ocg2 ON ocg2.id_grupo = ocg.id_grupo"
                               " WHERE oc.id_campeonato = %(id_campeonato)i)"
                               " WHERE r.fase IN (SELECT r.fase"
                               " FROM rschemar.resultados r"
                               " INNER JOIN rschemar.campeonato c "
                               " ON r.id_campeonato = c.id_campeonato AND c.id_campeonato_aovivo IN (SELECT ocg2.id_campeonato "
                               " FROM rschemar.campeonato oc"
                               " LEFT JOIN rschemar.campeonato_grupo_rel ocg ON oc.id_campeonato_aovivo = ocg.id_campeonato"
                               " LEFT JOIN rschemar.campeonato_grupo_rel ocg2 ON ocg2.id_grupo = ocg.id_grupo"
                               " WHERE oc.id_campeonato = %(id_campeonato)i)"
                               " WHERE r.data_hora BETWEEN %(data_ini)s AND %(data_fim)s LIMIT 1) ORDER BY r.data_hora")

select_resultados_max_o2_grupo = ("SELECT r.nome_time1, r.nome_time2, r.sigla_time1, r.sigla_time2, r.gols_time1, r.gols_time2, r.fase,"
                               " to_char(r.data_hora, 'dd/mm/YYYY HH24:MI') as data_hora_f, r.data_hora, r.inicio, r.fim"
                               " FROM rschemar.resultados r"
                               " INNER JOIN rschemar.campeonato c "
                               " ON r.id_campeonato = c.id_campeonato AND c.id_campeonato_aovivo IN (SELECT ocg2.id_campeonato "
                               " FROM rschemar.campeonato oc"
                               " LEFT JOIN rschemar.campeonato_grupo_rel ocg ON oc.id_campeonato_aovivo = ocg.id_campeonato"
                               " LEFT JOIN rschemar.campeonato_grupo_rel ocg2 ON ocg2.id_grupo = ocg.id_grupo"
                               " WHERE oc.id_campeonato = %(id_campeonato)i)"
                               " WHERE r.fase IN (SELECT r.fase"
                               " FROM rschemar.resultados r"
                               " INNER JOIN rschemar.campeonato c "
                               " ON r.id_campeonato = c.id_campeonato AND c.id_campeonato_aovivo IN (SELECT ocg2.id_campeonato "
                               " FROM rschemar.campeonato oc"
                               " LEFT JOIN rschemar.campeonato_grupo_rel ocg ON oc.id_campeonato_aovivo = ocg.id_campeonato"
                               " LEFT JOIN rschemar.campeonato_grupo_rel ocg2 ON ocg2.id_grupo = ocg.id_grupo"
                               " WHERE oc.id_campeonato = %(id_campeonato)i)"
                               " WHERE r.data_hora < %(data_ini)s ORDER BY data_hora DESC LIMIT 1) ORDER BY r.data_hora")

select_resultados_max_o3_grupo = ("SELECT r.nome_time1, r.nome_time2, r.sigla_time1, r.sigla_time2, r.gols_time1, r.gols_time2, r.fase,"
                               " to_char(r.data_hora, 'dd/mm/YYYY HH24:MI') as data_hora_f, r.data_hora, r.inicio, r.fim"
                               " FROM rschemar.resultados r"
                               " INNER JOIN rschemar.campeonato c "
                               " ON r.id_campeonato = c.id_campeonato AND c.id_campeonato_aovivo IN (SELECT ocg2.id_campeonato "
                               " FROM rschemar.campeonato oc"
                               " LEFT JOIN rschemar.campeonato_grupo_rel ocg ON oc.id_campeonato_aovivo = ocg.id_campeonato"
                               " LEFT JOIN rschemar.campeonato_grupo_rel ocg2 ON ocg2.id_grupo = ocg.id_grupo"
                               " WHERE oc.id_campeonato = %(id_campeonato)i)"
                               " WHERE r.fase IN (SELECT r.fase"
                               " FROM rschemar.resultados r"
                               " INNER JOIN rschemar.campeonato c "
                               " ON r.id_campeonato = c.id_campeonato AND c.id_campeonato_aovivo IN (SELECT ocg2.id_campeonato "
                               " FROM rschemar.campeonato oc"
                               " LEFT JOIN rschemar.campeonato_grupo_rel ocg ON oc.id_campeonato_aovivo = ocg.id_campeonato"
                               " LEFT JOIN rschemar.campeonato_grupo_rel ocg2 ON ocg2.id_grupo = ocg.id_grupo"
                               " WHERE oc.id_campeonato = %(id_campeonato)i) ORDER BY data_hora LIMIT 1) ORDER BY r.data_hora")

select_next_campeonato_seq  = ("SELECT nextval('rschemar.campeonato_id_campeonato_seq') as next")

select_next_time_seq        = ("SELECT nextval('rschemar.time_id_time_seq') as next")

select_next_conteudo_seq    = ("SELECT nextval('rschemar.conteudo_id_conteudo_seq') as next")

select_id_gol_seq           = ("SELECT nextval('rschemar.gol_id_gol_seq') as next")

select_id_jogo_tempo        = ("SELECT id_conteudo FROM rschemar.tempo WHERE id_tempo=%(id_tempo)i")

select_app_adm              = ("SELECT J.id_conteudo, J.titulo, J.publicado_em, "
                               "(J.publicado=True AND J.publicado_em <= now() AND "
                               "(J.expira_em > now() OR J.expira_em IS NULL)) as publicado "
                               "FROM rschemar.conteudo J "
                               "ORDER BY J.publicado_em DESC LIMIT %(limit)i OFFSET %(offset)i ")

select_titulo               = ("SELECT titulo FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

select_dublic_core          = ("SELECT titulo, descricao, "
                              "to_char(atualizado_em, 'YYYY-MM-DD HH24:MI:SS') as atualizado_em, "
                              "to_char(publicado_em, 'YYYY-MM-DD HH24:MI:SS') as publicado_em "
                              "FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

select_app_admc             = ("SELECT count(*) as qtde FROM rschemar.conteudo")

select_esquema_tatico       = ("SELECT id_esquema_tatico, titulo, descricao, imagem FROM "
                               "rschemar.esquema_tatico ORDER BY titulo")

select_jogo                 = ("SELECT C.id_conteudo, C.finalizado, C.id_time2, C.id_time1, C.id_idioma, "
                               "C.titulo, C.descricao, C.embed, C.html_videos, C.publicado_em, "
                               "to_char(C.publicado_em, 'dd/mm/YYYY HH24:MI') as publicado_em, to_char(C.expira_em, 'dd/mm/YYYY HH24:MI') as expira_em, C.publicado, "
                               "D.id_destaque, D.titulo as titulo_destaque, D.descricao as descricao_destaque, D.imagem as imagem_destaque, "
                               "T1.id_esquema_tatico as id_esquema_tatico_t1, T1.titulo as titulo_t1, T1.tecnico as tecnico_t1, T1.imagem as imagem_t1, "
                               "T2.id_esquema_tatico as id_esquema_tatico_t2, T2.titulo as titulo_t2, T2.tecnico as tecnico_t2, T2.imagem as imagem_t2 "
                               "FROM rschemar.conteudo C "
                               "LEFT JOIN rschemar.destaque D ON(C.id_conteudo=D.id_conteudo) "
                               "INNER JOIN rschemar.time T1 ON(C.id_time1=T1.id_time) "
                               "INNER JOIN rschemar.time T2 ON(C.id_time2=T2.id_time) "
                               "WHERE C.id_conteudo=%(id_conteudo)i")

select_escalacao            = ("SELECT E.id_escalacao, E.id_time, E.camisa, E.nome, E.titular, E.ordem, E.amarelo, E.vermelho, E.substituido, E.escalado "
                               "FROM rschemar.escalacao E "
                               "WHERE E.id_time=%(id_time)i AND E.titular=%(titular)s "
                               "ORDER BY E.ordem")

select_foto                 = ("SELECT F.id_foto, F.id_conteudo, F.arquivo, F.alinhamento, F.credito, F.legenda, F.link "
                               "FROM rschemar.foto F "
                               "WHERE id_conteudo=%(id_conteudo)i")

select_tempos               = ("SELECT id_tempo, nome, intervalo, to_char(inicio, 'dd/mm/YYYY HH24:MI') as inicio "
                               "FROM rschemar.tempo WHERE id_conteudo=%(id_conteudo)i ORDER BY inicio DESC")

select_tempo                = ("SELECT id_tempo, nome, intervalo, to_char(inicio, 'dd/mm/YYYY HH24:MI') as inicio "
                               "FROM rschemar.tempo WHERE id_tempo=%(id_tempo)i")

select_lances               = ("SELECT id_lance, id_gol, id_tempo, descricao, minuto, amarelo, vermelho, gol, substituicao "
                               "FROM rschemar.lance WHERE id_tempo=%(id_tempo)i ORDER BY id_lance DESC")

select_lance                = ("SELECT id_lance, id_gol, id_tempo, descricao, minuto, amarelo, vermelho, gol, substituicao "
                               "FROM rschemar.lance WHERE id_lance=%(id_lance)i")

select_gol                  = ("SELECT id_gol, id_escalacao, minuto FROM rschemar.gol WHERE id_gol=%(id_gol)i")

insert_time                 = ("INSERT INTO rschemar.time (id_time, id_esquema_tatico, titulo, tecnico, imagem) "
                               "VALUES (%(id_time)i, %(id_esquema_tatico)i, %(titulo)s, %(tecnico)s, %(imagem)s)")

insert_escalacao            = ("INSERT INTO rschemar.escalacao (id_time, camisa, nome, titular, "
                               "ordem, amarelo, vermelho, substituido, escalado) VALUES "
                               "(%(id_time)i, %(camisa)i, %(nome)s, %(titular)s, %(ordem)i, "
                               "%(amarelo)s, %(vermelho)s, %(substituido)s, %(escalado)s)")

insert_jogo                 = ("INSERT INTO rschemar.conteudo (id_conteudo, id_time2, id_time1, titulo, "
                               "descricao, embed, html_videos, publicado_em, expira_em, "
                               "publicado, finalizado) VALUES (%(id_conteudo)i, %(id_time2)i, %(id_time1)i, "
                               "%(titulo)s, %(descricao)s, %(embed)s, %(html_videos)s, %(publicado_em)s, "
                               "%(expira_em)s, %(publicado)s, %(finalizado)s)")

insert_destaque             = ("INSERT INTO rschemar.destaque (id_conteudo, titulo, descricao, imagem) VALUES "
                               "(%(id_conteudo)i, %(titulo)s, %(descricao)s, %(imagem)s)")

insert_foto                 = ("INSERT INTO rschemar.foto (id_conteudo, arquivo, alinhamento, credito, legenda, link) VALUES "
                               "(%(id_conteudo)i, %(arquivo)s, %(alinhamento)s, %(credito)s, %(legenda)s, %(link)s)")

insert_tempo                = ("INSERT INTO rschemar.tempo (id_conteudo, nome, inicio, intervalo) VALUES "
                               "(%(id_conteudo)i, %(nome)s, %(inicio)s, %(intervalo)s)")

insert_gol                  = ("INSERT INTO rschemar.gol (id_gol, id_escalacao, minuto) VALUES "
                               "(%(id_gol)i, %(id_escalacao)i, %(minuto)i)")

insert_lance                = ("INSERT INTO rschemar.lance (id_gol, id_tempo, descricao, minuto, amarelo, vermelho, gol, substituicao) VALUES "
                               "(%(id_gol)s, %(id_tempo)i, %(descricao)s, %(minuto)i, %(amarelo)s, %(vermelho)s, %(gol)s, %(substituicao)s)")

update_time                 = ("UPDATE rschemar.time SET id_esquema_tatico=%(id_esquema_tatico)i, titulo=%(titulo)s, "
                               "tecnico=%(tecnico)s, imagem=%(imagem)s WHERE id_time=%(id_time)i")

update_escalacao            = ("UPDATE rschemar.escalacao SET camisa=%(camisa)i, nome=%(nome)s, ordem=%(ordem)i "
                               "WHERE id_escalacao=%(id_escalacao)i")

update_jogo                 = ("UPDATE rschemar.conteudo SET "
                               "titulo=%(titulo)s, descricao=%(descricao)s, embed=%(embed)s, html_videos=%(html_videos)s, "
                               "finalizado=%(finalizado)s, publicado_em=%(publicado_em)s, expira_em=%(expira_em)s, "
                               "publicado=%(publicado)s, atualizado_em=now() "
                               "WHERE id_conteudo=%(id_conteudo)s")

update_destaque             = ("UPDATE rschemar.destaque SET titulo=%(titulo)s, descricao=%(descricao)s, imagem=%(imagem)s "
                               "WHERE id_destaque=%(id_destaque)i")

update_tempo                = ("UPDATE rschemar.tempo SET nome=%(nome)s, inicio=%(inicio)s, intervalo=%(intervalo)s "
                               "WHERE id_tempo=%(id_tempo)i")

update_time_tipo            = ("UPDATE rschemar.escalacao "
                               "SET amarelo='False', vermelho='False', substituido='False', escalado='False' "
                               "WHERE id_time IN (%(id_time1)s, %(id_time2)i); "
                               "UPDATE rschemar.escalacao SET amarelo='True' WHERE id_escalacao IN (%(amarelo)s); "
                               "UPDATE rschemar.escalacao SET vermelho='True' WHERE id_escalacao IN (%(vermelho)s); "
                               "UPDATE rschemar.escalacao SET substituido='True' WHERE id_escalacao IN (%(substituido)s); "
                               "UPDATE rschemar.escalacao SET escalado='True' WHERE id_escalacao IN (%(escalado)s);")

update_gol                  = ("UPDATE rschemar.gol SET id_escalacao=%(id_escalacao)i, minuto=%(minuto)s WHERE id_gol=%(id_gol)i")

update_lance                = ("UPDATE rschemar.lance SET id_gol=%(id_gol)s, descricao=%(descricao)s, "
                               "minuto=%(minuto)i, amarelo=%(amarelo)s, vermelho=%(vermelho)s, "
                               "gol=%(gol)s, substituicao=%(substituicao)s WHERE id_lance=%(id_lance)i")

delete_conteudo             = ("BEGIN;"
                               "DELETE FROM rschemar.time WHERE id_time=(SELECT id_time1 as id_time FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i);"
                               "DELETE FROM rschemar.time WHERE id_time=(SELECT id_time2 as id_time FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i);"
                               "DELETE FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i;"
                               "END;")

delete_escalacao            = ("DELETE FROM rschemar.escalacao WHERE id_escalacao IN (%(escalado)s)")

delete_foto                 = ("DELETE FROM rschemar.foto WHERE id_conteudo=%(id_conteudo)i")

delete_destaque             = ("DELETE FROM rschemar.destaque WHERE id_destaque=%(id_destaque)i")

delete_tempo                = ("DELETE FROM rschemar.gol WHERE id_gol IN ("
                               "SELECT id_gol FROM rschemar.lance WHERE id_tempo=%(id_tempo)i"
                               ");"
                               "DELETE FROM rschemar.tempo WHERE id_tempo=%(id_tempo)i")

delete_gol                  = ("DELETE FROM rschemar.gol WHERE id_gol=%(id_gol)i")

delete_lance                = ("DELETE FROM rschemar.gol WHERE id_gol=(SELECT id_gol FROM rschemar.lance WHERE id_lance=%(id_lance)i);"
                               "DELETE FROM rschemar.lance WHERE id_lance=%(id_lance)i;")

select_campeonatos_aovivo   = ("SELECT id_campeonato_aovivo, nome FROM rschemar.campeonato_aovivo")

select_campeonatos          = ("SELECT id_campeonato, nome FROM rschemar.campeonato ORDER BY nome")

delete_campeonato           = ("DELETE FROM rschemar.campeonato WHERE id_campeonato=%(id_campeonato)i")

insert_campeonato           = ("INSERT INTO rschemar.campeonato (id_campeonato, id_campeonato_aovivo, nome, id_tree)"
                               "VALUES (%(id_campeonato)i, %(id_campeonato_aovivo)i, %(nome_campeonato)s, %(id_tree)i)")

select_artilharia           = ("SELECT nome_jogador, quantidade_gols, time_jogador FROM rschemar.artilharia WHERE id_campeonato=%(id_campeonato)i ORDER BY quantidade_gols DESC")

##select_artilharia_grupo     = ("SELECT nome_jogador, quantidade_gols, time_jogador, id_campeonato "
##                               " FROM rschemar.artilharia WHERE id_campeonato IN ( "
##                               " SELECT id_campeonato FROM rschemar.campeonato_grupo_rel "
##                               " WHERE id_grupo IN (SELECT id_grupo FROM rschemar.campeonato_grupo_rel WHERE id_campeonato = %(id_campeonato)i)) "
##                               " ORDER BY quantidade_gols DESC ")

select_artilharia_grupo     = ("SELECT a.nome_jogador, a.time_jogador, a.quantidade_gols"
                               " FROM rschemar.artilharia a"
                               " INNER JOIN rschemar.campeonato c"
                               " ON a.id_campeonato = c.id_campeonato AND c.id_campeonato_aovivo IN (SELECT ocg2.id_campeonato"
                               " FROM rschemar.campeonato oc"
                               " LEFT JOIN rschemar.campeonato_grupo_rel ocg ON oc.id_campeonato_aovivo = ocg.id_campeonato"
                               " LEFT JOIN rschemar.campeonato_grupo_rel ocg2 ON ocg2.id_grupo = ocg.id_grupo"
                               " WHERE oc.id_campeonato = %(id_campeonato)i)"
                               " GROUP BY a.nome_jogador, a.time_jogador, a.quantidade_gols"
                               " ORDER BY a.quantidade_gols DESC")

select_resultados_grupo     = ("SELECT nome_jogador, quantidade_gols, time_jogador, id_campeonato "
                               " FROM rschemar.artilharia WHERE id_campeonato IN ( "
                               " SELECT id_campeonato FROM rschemar.campeonato_grupo_rel "
                               " WHERE id_grupo IN (SELECT id_grupo FROM rschemar.campeonato_grupo_rel WHERE id_campeonato = %(id_campeonato)i)) "
                               " ORDER BY quantidade_gols DESC ")

select_classificacao        = ("SELECT id_time, sigla_time, nome_time, pontos, vitorias, "
                               "empates, derrotas, gols_marcados, qtd_jogos, gols_sofridos, saldo_gols, ordem "
                               "FROM rschemar.classificacao WHERE id_campeonato=%(id_campeonato)i ORDER BY ordem ASC, pontos DESC, vitorias DESC, saldo_gols DESC")

select_resultados           = ("SELECT id_partida_aovivo, nome_time1, nome_time2, gols_time1, gols_time2, fase, to_char(data_hora, 'dd/mm/YYYY HH24:MI') as data_hora_f, data_hora, inicio FROM rschemar.resultados WHERE id_campeonato=%(id_campeonato)i ORDER BY data_hora")

select_resultados_pagina_res = ("SELECT id_partida_aovivo, nome_time1, nome_time2, gols_time1, gols_time2, fase, to_char(data_hora, 'dd/mm/YYYY HH24:MI') as data_hora_f, data_hora, inicio FROM rschemar.resultados WHERE id_campeonato=%(id_campeonato)i ORDER BY fase, data_hora")

insert_artilharia_xml       = ("INSERT INTO rschemar.artilharia (id_campeonato, nome_jogador, quantidade_gols, time_jogador)"
                               "VALUES (%(id_campeonato)i, %(nome_jogador)s, %(quantidade_gols)i, %(time_jogador)s)")

insert_classificacao_xml    = ("INSERT INTO rschemar.classificacao (id_campeonato, id_time, "
                               "sigla_time, nome_time, pontos, vitorias, "
                               "empates, derrotas, gols_marcados, qtd_jogos, gols_sofridos, saldo_gols, ordem) "
                               "VALUES (%(id_campeonato)i, %(id_time)i, %(sigla_time)s, "
                               "%(nome_time)s, %(pontos)i, %(vitorias)i, "
                               "%(empates)i, %(derrotas)i, %(gols_marcados)i, %(qtd_jogos)i, "
                               "%(gols_sofridos)i, %(saldo_gols)i, %(ordem)i)")

insert_resultados_xml       = ("INSERT INTO rschemar.resultados (id_campeonato, id_partida_aovivo, nome_time1, nome_time2, "
                               "sigla_time1, sigla_time2, data_hora, fase, estadio, cidade, gols_time1, gols_time2, inicio, fim)"
                               "VALUES (%(id_campeonato)i, %(id_partida_aovivo)i, %(nome_time1)s, %(nome_time2)s, "
                               "%(sigla_time1)s, %(sigla_time2)s, %(data_hora)s, %(fase)s, %(estadio)s, %(cidade)s, "
                               "%(gols_time1)i, %(gols_time2)i, %(inicio)i, %(fim)i)")

select_next_time_xml_seq    = ("SELECT nextval('rschemar.time_xml_id_time_seq') as next")

insert_time_xml             = ("INSERT INTO rschemar.time_xml (id_time, id_conteudo, nome, sigla, esquema_tatico, "
                               "tecnico, gols, penalts, id_time_externo) "
                               "VALUES (%(id_time)i, %(id_conteudo)i, %(nome)s, %(sigla)s, %(esquema_tatico)s, "
                               "%(tecnico)s, %(gols)i, %(penalts)i, %(id_time_externo)i)")

insert_escalacao_xml        = ("INSERT INTO rschemar.escalacao_xml (id_time, nome, posicao, gols, "
                               "amarelo, amarelo2, vermelho, substituido, id_jogador, gol_contra) "
                               "VALUES (%(id_time)i, %(nome)s, %(posicao)s, %(gols)i, "
                               "%(amarelo)i, %(amarelo2)i, %(vermelho)i, %(substituido)i, %(id_jogador)i, %(gol_contra)i)")

insert_narracao_xml         = ("INSERT INTO rschemar.narracao (id_narracao, id_conteudo, acao, jogador1, jogador2, "
                               "tempo, texto, minuto, time) VALUES (%(id_narracao)i, %(id_conteudo)i, "
                               "%(acao)s, %(jogador1)s, %(jogador2)s, "
                               "%(tempo)i, %(texto)s, %(minuto)i, %(time)s)")

insert_partida_xml          = ("INSERT INTO rschemar.conteudo (id_conteudo, id_campeonato, publicado_em, iniciado, finalizado, "
                               "arbitro, auxiliar1, auxiliar2, rodada, data_hora, local, estadio) "
                               "VALUES (%(id_conteudo)i, %(id_campeonato)i, %(publicado_em)s, %(iniciado)i, %(finalizado)i, "
                               "%(arbitro)s, %(auxiliar1)s, %(auxiliar2)s, %(rodada)s, %(data_hora)s, %(local)s, %(estadio)s)")

update_partida_xml          = ("UPDATE rschemar.conteudo SET iniciado=%(iniciado)i, finalizado=%(finalizado)i "
                               "WHERE id_conteudo=%(id_conteudo)i")

update_partida_com_data_xml = ("UPDATE rschemar.conteudo SET iniciado=%(iniciado)i, finalizado=%(finalizado)i, data_hora_inicio=%(data_hora_inicio)s "
                               "WHERE id_conteudo=%(id_conteudo)i")

update_partida_com_completo = ("UPDATE rschemar.conteudo SET iniciado=%(iniciado)i, finalizado=%(finalizado)i, "
                                "arbitro = %(arbitro)s, auxiliar1 = %(auxiliar1)s, auxiliar2 = %(auxiliar2)s, "
                                "local = %(local)s, estadio = %(estadio)s, data_hora = %(data_hora)s "
                                "WHERE id_conteudo=%(id_conteudo)i")

select_checa_partida        = ("SELECT id_campeonato FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

select_xmls_processados     = ("SELECT id_xml, nome_xml, bytes_xml, ultima_alteracao FROM rschemar.xmls_processados WHERE nome_xml=%(nome_xml)s")

select_campeonatos_h2       = ("SELECT id_campeonato, id_campeonato_aovivo, nome FROM rschemar.campeonato WHERE id_campeonato_aovivo=%(id_campeonato_aovivo)i")

insert_xmls_processados     = ("INSERT INTO rschemar.xmls_processados (nome_xml, bytes_xml, ultima_alteracao) "
                               "VALUES (%(nome_xml)s, %(bytes_xml)i, %(ultima_alteracao)s)")

update_xmls_processados     = ("UPDATE rschemar.xmls_processados SET bytes_xml=%(bytes_xml)i, ultima_alteracao=%(ultima_alteracao)s "
                               "WHERE id_xml=%(id_xml)i")

insert_campeonato_xml       = ("INSERT INTO rschemar.campeonato_aovivo (id_campeonato_aovivo, nome) "
                               "VALUES (%(id_campeonato_aovivo)i, %(nome)s)")

select_times_partida        = ("SELECT id_time, id_conteudo, nome, sigla, esquema_tatico, tecnico, gols, penalts "
                               "FROM rschemar.time_xml "
                               "WHERE id_conteudo=%(id_conteudo)i ORDER BY id_time ASC")

select_escalacao_partida    = ("SELECT id_escalacao, id_time, nome, posicao, gols, amarelo, amarelo2, vermelho, substituido, id_jogador, id_jogador_substituido, gol_contra "
                               "FROM rschemar.escalacao_xml "
                               "WHERE id_time=%(id_time)i "
                               "ORDER BY id_escalacao ASC")

select_narracao_partida     = ("SELECT id_narracao, acao, jogador1, jogador2, tempo, texto, minuto, time "
                               "FROM rschemar.narracao "
                               "WHERE id_conteudo=%(id_conteudo)i "
                               "ORDER BY tempo DESC, minuto DESC, id_narracao DESC")

select_campeonato_h2        = ("SELECT id_campeonato, nome, descricao, id_tree "
                               "FROM rschemar.campeonato "
                               "WHERE id_campeonato_aovivo=%(id_campeonato_aovivo)i")

select_ficha_partida        = ("SELECT id_campeonato, local, estadio, arbitro, auxiliar1, auxiliar2 "
                               "FROM rschemar.conteudo "
                               "WHERE id_conteudo=%(id_conteudo)i")

limpa_narracao_xml          = ("DELETE FROM rschemar.narracao WHERE id_conteudo=%(id_conteudo)i")

limpa_artilharia_xml        = ("DELETE FROM rschemar.artilharia WHERE id_campeonato=%(id_campeonato)i")

limpa_classificacao_xml     = ("DELETE FROM rschemar.classificacao WHERE id_campeonato=%(id_campeonato)i")

limpa_resultados_xml        = ("DELETE FROM rschemar.resultados WHERE id_campeonato=%(id_campeonato)i")

limpa_campeonatos_aovivo_xml= ("DELETE FROM rschemar.campeonato_aovivo")

update_partida_xml_addtime  = ("UPDATE rschemar.conteudo SET id_time1=%(id_time1)i, id_time2=%(id_time2)i, titulo=%(titulo)s, possui_narracao=%(possui_narracao)s "
                               "WHERE id_conteudo=%(id_conteudo)i")

select_partida              = ("SELECT id_time1, id_time2, iniciado, finalizado, intervalo, data_hora_inicio "
                               "FROM rschemar.conteudo "
                               "WHERE id_conteudo=%(id_conteudo)i")

limpa_escalacao_xml         = ("DELETE FROM rschemar.escalacao_xml WHERE id_time=%(id_time)i")

select_placar_partida       = ("SELECT nome, gols, sigla, penalts "
                               "FROM rschemar.time_xml "
                               "WHERE id_conteudo=%(id_conteudo)i "
                               "ORDER BY id_time ASC")

update_time_xml             = ("UPDATE rschemar.time_xml SET gols=%(gols)i, penalts=%(penalts)i, tecnico=%(tecnico)s, id_time_externo=%(id_time_externo)i "
                               "WHERE id_time=%(id_time)i")

select_d_resultados         = ("SELECT * FROM rschemar.resultados")
select_d_resultados1        = ("SELECT * FROM rschemar.resultados WHERE id_partida_aovivo = %(_id)i")
delete_d_resultados         = ("DELETE FROM rschemar.resultados WHERE id_partida_aovivo = %(_id)i")
delete_d_resultados1        = ("DELETE FROM rschemar.resultados WHERE id_resultados = %(_id)i")

select_d_conteudo           = ("SELECT * FROM rschemar.conteudo")
select_d_conteudo1          = ("SELECT * FROM rschemar.conteudo WHERE id_conteudo = %(_id)i")
delete_d_conteudo           = ("DELETE FROM rschemar.conteudo WHERE id_conteudo = %(_id)i")

select_d_time_xml           = ("SELECT * FROM rschemar.time_xml")
select_d_time_xml1          = ("SELECT * FROM rschemar.time_xml WHERE id_conteudo = %(_id)i")
delete_d_time_xml           = ("DELETE FROM rschemar.time_xml WHERE id_conteudo = %(_id)i")

select_d_conteudo_h2        = ("SELECT * FROM envsite.conteudo WHERE id_conteudo = %(_id)i AND id_aplicativo = 41")
delete_d_conteudo_h2        = ("DELETE FROM envsite.conteudo WHERE id_conteudo = %(_id)i")

select_partidas_simultaneas = ("SELECT DISTINCT C.id_conteudo, C.id_time1, C.id_time2, T1.nome AS t1_nome, T2.nome AS t2_nome, E.url, "
                               "T1.sigla AS t1_sigla, T2.sigla AS t2_sigla, T1.gols AS t1_gols, T2.gols AS t2_gols "
                               "FROM rschemar.conteudo C "
                               "LEFT JOIN rschemar.time_xml T1 ON(C.id_time1=T1.id_time) "
                               "LEFT JOIN rschemar.time_xml T2 ON(C.id_time2=T2.id_time) "
                               "LEFT JOIN envsite.conteudo E ON(E.id_conteudo=C.id_conteudo AND E.url is not null AND E.url <> '') "
                               "WHERE C.id_conteudo <> %(id_conteudo)i AND C.iniciado = 1 AND C.finalizado = 0 AND (C.data_hora BETWEEN %(data_ini)s AND %(data_fim)s)")

select_partida_portlet_capa = ("SELECT DISTINCT C.id_conteudo, R.data_hora, to_char(R.data_hora, 'dd/mm/YYYY às HH24:MI') as data_hora_f, C.id_time1, C.id_time2, T1.nome AS t1_nome, T2.nome AS t2_nome, E.url, "
                               "T1.sigla AS t1_sigla, T2.sigla AS t2_sigla, T1.gols AS t1_gols, T2.gols AS t2_gols, R.inicio "
                               "FROM rschemar.conteudo C "
                               "LEFT JOIN rschemar.time_xml T1 ON(C.id_time1=T1.id_time) "
                               "LEFT JOIN rschemar.time_xml T2 ON(C.id_time2=T2.id_time) "
                               "LEFT JOIN rschemar.resultados R ON(C.id_conteudo=R.id_partida_aovivo) "
                               "LEFT JOIN envsite.conteudo E ON(E.id_conteudo=C.id_conteudo AND E.url is not null AND E.url <> '') "
                               "WHERE C.id_conteudo = %(id_conteudo)i ")

insert_estatistica_xml      = ("INSERT INTO rschemar.estatistica (id_time, descricao, valor) "
                               "VALUES (%(id_time)i, %(descricao)s, %(valor)i)")

limpa_estatistica_xml       = ("DELETE FROM rschemar.estatistica WHERE id_time=%(id_time)i")

##select_estatistica_xml      = ("SELECT e.id_time || ';' || e.descricao || ';' || e.valor AS dados "
##                               " FROM rschemar.estatistica e, rschemar.conteudo c"
##                               " WHERE (e.id_time = c.id_time1 OR e.id_time = c.id_time2) and c.id_conteudo = %(id_conteudo)i")

##select_estatistica_xml      = ("SELECT e.id_time || ';' || e.descricao || ';' || e.valor AS dados,"
##                               " c.id_time1, c.id_time2, t1.nome as t1_nome, t2.nome as t2_nome,"
##                               " t1.sigla as t1_sigla, t2.sigla as t2_sigla, t1.gols as t1_gols, t2.gols as t2_gols"
##                               " FROM rschemar.estatistica e, rschemar.conteudo c"
##                               " LEFT JOIN rschemar.time_xml T1 ON(C.id_time1=T1.id_time)"
##                               " LEFT JOIN rschemar.time_xml T2 ON(C.id_time2=T2.id_time)"
##                               " WHERE (e.id_time = c.id_time1 OR e.id_time = c.id_time2) and c.id_conteudo = %(id_conteudo)i")

select_estatistica_xml      = ("SELECT e.id_time, e.descricao || '=' || e.valor AS dados,"
                               " t.nome AS t_nome, t.sigla AS t_sigla, t.gols AS t_gols, t.tecnico,"
                               " c.arbitro, c.auxiliar1, c.auxiliar2, c.data_hora, c.local, c.estadio"
                               " FROM rschemar.conteudo c, rschemar.estatistica e"
                               " LEFT JOIN rschemar.time_xml t ON (e.id_time = t.id_time)"
                               " WHERE (e.id_time = c.id_time1 OR e.id_time = c.id_time2) and c.id_conteudo = %(id_conteudo)i"
                               " ORDER BY e.id_time, e.descricao")

select_possui_narracao      = ("SELECT  cr.possui_narracao,"
                               " (SELECT max(ce.url) FROM envsite.conteudo ce WHERE id_aplicativo = %(id_aplicativo)i"
                               " AND ce.id_conteudo = cr.id_conteudo) AS url"
                               " FROM rschemar.conteudo cr"
                               " WHERE  cr.id_conteudo = %(id_conteudo)i")

update_partida_radio        = ("UPDATE rschemar.conteudo SET url_radio=%(url_radio)s "
                               "WHERE id_conteudo=%(id_conteudo)i")

select_partida_radio        = ("SELECT url_radio "
                               "FROM rschemar.conteudo "
                               "WHERE id_conteudo=%(id_conteudo)i")

select_classificacao_by_idconteudo = ("SELECT cla.nome_time, cla.pontos, cla.vitorias, cla.empates, cla.derrotas, cla.qtd_jogos, cla.ordem "
                                      "FROM rschemar.classificacao cla "
                                      "LEFT JOIN rschemar.conteudo con ON (cla.id_campeonato = con.id_campeonato) "
                                      "WHERE con.id_conteudo = %(id_conteudo)i "
                                      "ORDER BY cla.ordem ASC, cla.pontos DESC ")

select_campeonatos_atual = ("SELECT DISTINCT p.id_campeonato, c.nome "
                            "FROM rschemar.conteudo p, rschemar.campeonato c "
                            "WHERE p.data_hora >= now() "
                            "AND c.id_campeonato = p.id_campeonato")

select_partidas_by_time = ("SELECT t1.nome AS t1_nome, t1.sigla AS t1_sigla, "
                            "t1.id_time_externo AS t1_id_time_externo, t1.gols AS t1_gols, "
                            "t2.nome AS t2_nome, t2.sigla AS t2_sigla, "
                            "t2.id_time_externo AS t2_id_time_externo, t2.gols AS t2_gols, "
                            "to_char(c.data_hora, 'dd/mm/YYYY') AS data_f "
                            "FROM rschemar.conteudo c "
                            "INNER JOIN rschemar.time_xml t ON (t.id_time_externo = %(id_time_externo)i "
                            "AND c.id_conteudo = t.id_conteudo)"
                            "INNER JOIN rschemar.time_xml t1 ON (c.id_time1 = t1.id_time) "
                            "INNER JOIN rschemar.time_xml t2 ON (c.id_time2 = t2.id_time) "
                            "WHERE c.id_campeonato = %(id_campeonato)i AND c.iniciado = 1 AND c.finalizado = 1 "
                            "ORDER BY c.data_hora")

select_partidas_by_time_all = ("SELECT t1.nome AS t1_nome, t1.sigla AS t1_sigla, "
                                "t1.id_time_externo AS t1_id_time_externo, t1.gols AS t1_gols, "
                                "t2.nome AS t2_nome, t2.sigla AS t2_sigla, "
                                "t2.id_time_externo AS t2_id_time_externo, t2.gols AS t2_gols, "
                                "to_char(c.data_hora, 'dd/mm/YYYY') AS data_f "
                                "FROM rschemar.conteudo c "
                                "INNER JOIN rschemar.time_xml t ON (t.id_time_externo = %(id_time_externo)i "
                                "AND c.id_conteudo = t.id_conteudo)"
                                "INNER JOIN rschemar.time_xml t1 ON (c.id_time1 = t1.id_time) "
                                "INNER JOIN rschemar.time_xml t2 ON (c.id_time2 = t2.id_time) "
                                "WHERE c.id_campeonato = %(id_campeonato)i "
                                "ORDER BY c.data_hora")

insert_substituicoes        = ("INSERT INTO rschemar.escalacao_xml (id_time, nome, posicao, gols, "
                               "amarelo, amarelo2, vermelho, substituido, id_jogador, id_jogador_substituido, gol_contra) "
                               "VALUES (%(id_time)i, %(nome)s, %(posicao)s, %(gols)i, "
                               "%(amarelo)i, %(amarelo2)i, %(vermelho)i, %(substituido)i, %(id_jogador)i, %(id_jogador_substituido)i, %(gol_contra)i)")

update_partida_alterada     = ("UPDATE rschemar.conteudo SET titulo=%(titulo)s, data_hora=%(data_hora)s, "
                               "local=%(local)s, estadio=%(estadio)s "
                               "WHERE id_conteudo=%(id_conteudo)i")

update_time_partida_alterada = ("UPDATE rschemar.time_xml SET nome=%(nome)s, sigla=%(sigla)s "
                                "WHERE id_conteudo=%(id_conteudo)i AND id_time_externo=%(id_time_externo)i")

structure = """
  CREATE SCHEMA rschemar;

  CREATE TABLE rschemar.campeonato_aovivo (
    id_campeonato_aovivo SERIAL NOT NULL,
    nome VARCHAR,
    PRIMARY KEY(id_campeonato_aovivo)
  );

  CREATE TABLE rschemar.campeonato (
    id_campeonato SERIAL NOT NULL,
    id_campeonato_aovivo INTEGER NOT NULL,
    nome VARCHAR,
    descricao VARCHAR,
    id_tree INTEGER,
    PRIMARY KEY(id_campeonato)
  );

  CREATE INDEX index_rschemar_campeonato_id_campeonato_aovivo ON rschemar.campeonato USING btree (id_campeonato_aovivo);

  CREATE TABLE rschemar.classificacao (
    id_classificacao SERIAL NOT NULL,
    id_campeonato INTEGER NOT NULL,
    nome_time VARCHAR,
    sigla_time CHAR(3),
    id_time INTEGER,
    pontos INTEGER,
    vitorias INTEGER,
    empates INTEGER,
    derrotas INTEGER,
    gols_marcados INTEGER,
    qtd_jogos INTEGER,
    gols_sofridos INTEGER,
    saldo_gols INTEGER,
    ordem INTEGER,
    PRIMARY KEY(id_classificacao),
    FOREIGN KEY(id_campeonato)
      REFERENCES rschemar.campeonato(id_campeonato)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );

  CREATE INDEX index_rschemar_classificacao_id_campeonato ON rschemar.classificacao USING btree (id_campeonato);

  CREATE TABLE rschemar.artilharia (
    id_artilharia SERIAL NOT NULL,
    id_campeonato INTEGER NOT NULL,
    nome_jogador VARCHAR,
    quantidade_gols INTEGER,
    time_jogador VARCHAR,
    PRIMARY KEY(id_artilharia),
    FOREIGN KEY(id_campeonato)
      REFERENCES rschemar.campeonato(id_campeonato)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );

  CREATE INDEX index_rschemar_artilharia_id_campeonato ON rschemar.artilharia USING btree (id_campeonato);

  CREATE TABLE rschemar.resultados (
    id_resultados SERIAL NOT NULL,
    id_campeonato INTEGER NOT NULL,
    id_partida_aovivo INTEGER,
    nome_time1 VARCHAR,
    nome_time2 VARCHAR,
    sigla_time1 VARCHAR,
    sigla_time2 VARCHAR,
    data_hora TIMESTAMP,
    fase VARCHAR,
    estadio VARCHAR,
    cidade VARCHAR,
    gols_time1 INTEGER,
    gols_time2 INTEGER,
    inicio INTEGER,
    fim INTEGER,
    PRIMARY KEY(id_resultados),
    FOREIGN KEY(id_campeonato)
      REFERENCES rschemar.campeonato(id_campeonato)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );

  CREATE INDEX index_rschemar_resultados_id_campeonato ON rschemar.resultados USING btree (id_campeonato);

  CREATE TABLE rschemar.esquema_tatico (
    id_esquema_tatico SERIAL NOT NULL,
    titulo VARCHAR,
    descricao VARCHAR,
    imagem VARCHAR,
    PRIMARY KEY(id_esquema_tatico)
  );

  CREATE TABLE rschemar.time (
    id_time SERIAL NOT NULL,
    id_esquema_tatico INTEGER NOT NULL,
    titulo VARCHAR,
    tecnico VARCHAR,
    imagem VARCHAR,
    PRIMARY KEY(id_time),
    FOREIGN KEY(id_esquema_tatico)
      REFERENCES rschemar.esquema_tatico(id_esquema_tatico)
      ON DELETE CASCADE
      ON UPDATE CASCADE
  );
  CREATE INDEX index_rschemar_time_id_esquema_tatico ON rschemar.time USING btree (id_esquema_tatico);

  CREATE TABLE rschemar.escalacao (
    id_escalacao SERIAL NOT NULL,
    id_time INTEGER NOT NULL,
    camisa INTEGER,
    nome VARCHAR,
    titular BOOL DEFAULT true,
    ordem INTEGER,
    amarelo BOOL  DEFAULT false,
    vermelho BOOL  DEFAULT false,
    substituido BOOL  DEFAULT false,
    escalado BOOL  DEFAULT false,
    PRIMARY KEY(id_escalacao),
    FOREIGN KEY(id_time)
      REFERENCES rschemar.time(id_time)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );
  CREATE INDEX index_rschemar_escalacao_id_time ON rschemar.escalacao USING btree (id_time);

  CREATE TABLE rschemar.conteudo (
    id_conteudo SERIAL NOT NULL,
    id_time1 INTEGER,
    id_time2 INTEGER,
    id_idioma INTEGER DEFAULT 102,
    titulo VARCHAR,
    descricao VARCHAR,
    embed VARCHAR,
    html_videos VARCHAR,
    publicado_em TIMESTAMP NOT NULL,
    expira_em TIMESTAMP,
    publicado BOOL DEFAULT True,
    id_campeonato INTEGER NOT NULL,
    iniciado INTEGER,
    finalizado INTEGER,
    intervalo INTEGER,
    arbitro VARCHAR,
    auxiliar1 VARCHAR,
    auxiliar2 VARCHAR,
    rodada VARCHAR,
    data_hora TIMESTAMP,
    local VARCHAR,
    estadio VARCHAR,
    data_hora_inicio TIMESTAMP,
    url_radio VARCHAR,
    possui_narracao CHAR(1),
    PRIMARY KEY(id_conteudo),
    FOREIGN KEY(id_campeonato)
      REFERENCES rschemar.campeonato(id_campeonato)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );

  CREATE INDEX index_rschemar_conteudo_id_time1 ON rschemar.conteudo USING btree (id_time1);
  CREATE INDEX index_rschemar_conteudo_id_time2 ON rschemar.conteudo USING btree (id_time2);
  CREATE INDEX index_rschemar_conteudo_id_campeonato ON rschemar.conteudo USING btree (id_campeonato);

  CREATE TABLE rschemar.conteudobkp (
    id_conteudo SERIAL NOT NULL,
    id_time2 INTEGER NOT NULL,
    id_time1 INTEGER NOT NULL,
    id_idioma INTEGER DEFAULT 102,
    titulo VARCHAR,
    descricao VARCHAR,
    embed VARCHAR,
    html_videos VARCHAR,
    publicado_em TIMESTAMP NOT NULL,
    expira_em TIMESTAMP,
    publicado BOOL DEFAULT True,
    atualizado_em TIMESTAMP,
    finalizado BOOL DEFAULT False,
    PRIMARY KEY(id_conteudo),
    FOREIGN KEY(id_time1)
      REFERENCES rschemar.time(id_time)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
    FOREIGN KEY(id_time2)
      REFERENCES rschemar.time(id_time)
      ON DELETE CASCADE
      ON UPDATE CASCADE
  );
  CREATE INDEX index_rschemar_conteudobkp_id_time1 ON rschemar.conteudobkp USING btree (id_time1);
  CREATE INDEX index_rschemar_conteudobkp_id_time2 ON rschemar.conteudobkp USING btree (id_time2);

  CREATE TABLE rschemar.foto (
    id_foto SERIAL NOT NULL,
    id_conteudo INTEGER NOT NULL,
    arquivo VARCHAR,
    alinhamento VARCHAR,
    credito VARCHAR,
    legenda VARCHAR,
    link VARCHAR,
    PRIMARY KEY(id_foto),
    FOREIGN KEY(id_conteudo)
      REFERENCES rschemar.conteudo(id_conteudo)
      ON DELETE CASCADE
      ON UPDATE CASCADE
  );
  CREATE INDEX index_rschemar_foto_id_conteudo ON rschemar.foto USING btree (id_foto);

  CREATE TABLE rschemar.tempo (
    id_tempo SERIAL NOT NULL,
    id_conteudo INTEGER NOT NULL,
    nome VARCHAR,
    inicio TIMESTAMP,
    intervalo BOOL DEFAULT false,
    PRIMARY KEY(id_tempo),
    FOREIGN KEY(id_conteudo)
      REFERENCES rschemar.conteudo(id_conteudo)
      ON DELETE CASCADE
      ON UPDATE CASCADE
  );
  CREATE INDEX index_rschemar_tempo_id_conteudo ON rschemar.tempo USING btree (id_conteudo);

  CREATE TABLE rschemar.gol (
    id_gol SERIAL NOT NULL,
    id_escalacao INTEGER NOT NULL,
    minuto INTEGER,
    PRIMARY KEY(id_gol),
    FOREIGN KEY(id_escalacao)
      REFERENCES rschemar.escalacao(id_escalacao)
      ON DELETE CASCADE
      ON UPDATE CASCADE
  );
  CREATE INDEX index_rschemar_gol_id_escalacao ON rschemar.gol USING btree (id_escalacao);

  CREATE TABLE rschemar.lance (
    id_lance SERIAL NOT NULL,
    id_gol INTEGER NULL,
    id_tempo INTEGER NOT NULL,
    descricao VARCHAR,
    minuto INTEGER,
    amarelo BOOL DEFAULT false,
    vermelho BOOL DEFAULT false,
    gol BOOL DEFAULT false,
    substituicao BOOL DEFAULT false,
    PRIMARY KEY(id_lance),
    FOREIGN KEY(id_tempo)
      REFERENCES rschemar.tempo(id_tempo)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
    FOREIGN KEY(id_gol)
    REFERENCES rschemar.gol(id_gol)
      ON DELETE SET NULL
      ON UPDATE CASCADE
  );
  CREATE INDEX index_rschemar_lance_id_tempo ON rschemar.lance USING btree (id_tempo);
  CREATE INDEX index_rschemar_lance_id_gol ON rschemar.lance USING btree (id_gol);

  CREATE TABLE rschemar.destaque (
    id_destaque SERIAL NOT NULL,
    id_conteudo INTEGER NOT NULL,
    titulo VARCHAR,
    descricao VARCHAR,
    imagem VARCHAR,
    PRIMARY KEY(id_destaque),
    FOREIGN KEY(id_conteudo)
      REFERENCES rschemar.conteudo(id_conteudo)
      ON DELETE CASCADE
      ON UPDATE CASCADE
  );
  CREATE INDEX index_rschemar_destaque_id_conteudo ON rschemar.destaque USING btree (id_conteudo);

    CREATE TABLE rschemar.xmls_processados (
    id_xml SERIAL NOT NULL,
    nome_xml VARCHAR,
    bytes_xml INTEGER,
    ultima_alteracao TIMESTAMP,
    PRIMARY KEY(id_xml)
  );

  CREATE TABLE rschemar.partida (
    id_partida SERIAL NOT NULL,
    id_campeonato INTEGER NOT NULL,
    iniciado INTEGER,
    finalizado INTEGER,
    arbitro VARCHAR,
    auxiliar1 VARCHAR,
    auxiliar2 VARCHAR,
    rodada INTEGER,
    data_hora TIMESTAMP,
    local VARCHAR,
    estadio VARCHAR,
    PRIMARY KEY(id_partida),
    FOREIGN KEY(id_campeonato)
      REFERENCES rschemar.campeonato(id_campeonato)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );

  CREATE INDEX index_rschemar_partida_id_campeonato ON rschemar.partida USING btree (id_campeonato);

  CREATE TABLE rschemar.narracao (
    id_narracao SERIAL NOT NULL,
    id_conteudo INTEGER NOT NULL,
    acao VARCHAR,
    jogador1 VARCHAR,
    jogador2 VARCHAR,
    tempo INTEGER,
    texto VARCHAR,
    minuto INTEGER,
    time VARCHAR,
    PRIMARY KEY(id_narracao),
    FOREIGN KEY(id_conteudo)
      REFERENCES rschemar.conteudo(id_conteudo)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );

  CREATE INDEX index_rschemar_narracao_id_conteudo ON rschemar.narracao USING btree (id_conteudo);

  CREATE TABLE rschemar.time_xml (
    id_time SERIAL NOT NULL,
    id_conteudo INTEGER,
    id_time_externo SMALLINT,
    nome VARCHAR,
    sigla VARCHAR,
    esquema_tatico VARCHAR,
    tecnico VARCHAR,
    gols INTEGER,
    penalts INTEGER,
    PRIMARY KEY(id_time),
    FOREIGN KEY(id_conteudo)
      REFERENCES rschemar.conteudo(id_conteudo)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );

  CREATE INDEX index_rschemar_time_xml_id_conteudo ON rschemar.time_xml USING btree (id_conteudo);

  CREATE TABLE rschemar.escalacao_xml (
    id_escalacao SERIAL NOT NULL,
    id_time INTEGER NOT NULL,
    nome VARCHAR,
    posicao VARCHAR,
    gols INTEGER,
    amarelo INTEGER  DEFAULT 0,
    amarelo2 INTEGER  DEFAULT 0,
    vermelho INTEGER  DEFAULT 0,
    substituido INTEGER  DEFAULT 0,
    id_jogador INTEGER,
    id_jogador_substituido INTEGER,
    gol_contra INTEGER,
    PRIMARY KEY(id_escalacao),
    FOREIGN KEY(id_time)
      REFERENCES rschemar.time_xml(id_time)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );

  CREATE INDEX index_rschemar_escalacao_xml_id_time ON rschemar.escalacao_xml USING btree (id_time);

  CREATE TABLE rschemar.campeonato_grupo (
    id_grupo serial NOT NULL,
    descricao character varying(200),
    PRIMARY KEY(id_grupo)
  );

  CREATE TABLE rschemar.campeonato_grupo_rel (
    id_grupo integer NOT NULL,
    id_campeonato integer NOT NULL,
    PRIMARY KEY(id_grupo, id_campeonato)
  );

  CREATE INDEX index_rschemar_campeonato_grupo_rel_id_campeonato ON rschemar.campeonato_grupo_rel USING btree (id_campeonato);

  CREATE TABLE rschemar.estatistica
    (
    	id_estatistica BIGSERIAL NOT NULL,
    	id_time INTEGER NOT NULL,
    	descricao CHARACTER varying(200),
    	valor SMALLINT DEFAULT 0,
    	PRIMARY KEY(id_estatistica)
    );

  INSERT INTO rschemar.esquema_tatico (id_esquema_tatico, titulo, descricao, imagem) VALUES (1, '3-3-4', 'Neste sistema é utilizado dois zagueiros e um dos laterais na defesa. Compondo o meio-campo, outro lateral fica como meio-campo defensivo, enquanto o volante fica como meio-campo central junto a um dos meias-armadores. O outro meia-armador fica como atacante junto com os três atacantes.', '3-3-4.gif');
  INSERT INTO rschemar.esquema_tatico (id_esquema_tatico, titulo, descricao, imagem) VALUES (2, '3-4-3', 'A sua primeira aparição foi na Copa do Mundo de 1962, na sua defesa existe um líbero que faz a cobertura das jogadas, nos lados do meio-campo, um ala defensivo, e um ponta. Além de três atacantes, sendo dois pontas de lança e um centro avante.', '3-4-3.gif');
  INSERT INTO rschemar.esquema_tatico (id_esquema_tatico, titulo, descricao, imagem) VALUES (3, '3-5-2', 'O segundo mais utilizado atualmente, possui um meio-campo com 2 volantes e 2 laterais avançados e sem obrigação de marcar, assim denominados alas. Com dois centro-avantes que recebem bolas cruzadas na áreaz pelos alas.\nO 3-5-2 é um esquema tático com três jogadores na defesa, cinco jogadores no meio-campo e dois jogadores no ataque.\nEste esquema surgiu na Europa, como opção menos defensiva que o 4-4-2. Na defesa, foi adicionado um zagueiro, e o último jogador da defesa é conhecido como líbero. Os laterais foram colocados mais à frente, e passaram a ser chamados de alas.\nO líbero tem importância fundamental neste esquema. É ele o jogador que orienta a defesa, desarma adversários e cria as jogadas de ataque. Para este ataque funcionar, o meio-campo deve ter jogadores com capacidade de marcação.\nNo lado defensivo do esquema, cada zagueiro fica incubido de marcar um atacante, enquanto o líbero, que pode se posicionar na frente ou atrás da defesa, "na sobra", auxiliando o setor defensivo. Os meias protegem a entrada da área e os alas cuidam das laterais.', '3-5-2.gif');
  INSERT INTO rschemar.esquema_tatico (id_esquema_tatico, titulo, descricao, imagem) VALUES (4, '3-6-1', 'O 3-6-1, é um esquema tático com três jogadores na defesa, dois como volante, dois no meio-campo, um na lateral-direita, um na lateral-esquerda e somente um atacante.\nÉ uma tática muito rara em partidas de futebol, pois várias equipes já adotaram o 4-4-2, 3-5-2 e 4-5-1.\nNo lado ofensivo, ambos os meias e os laterais sobem ao ataque, um volante fecha o meio-campo e o outro fica de sobra na intermediária. No lado defensivo, os laterais e os volantes voltam, e os meias ficam na intermediária de seu clube.', '3-6-1.gif');
  INSERT INTO rschemar.esquema_tatico (id_esquema_tatico, titulo, descricao, imagem) VALUES (5, '4-2-4', 'O 4-2-4 é composto por 4 defensores, 2 meio-campo e 4 atacantes. Foi um esquema popular nas décadas de 40 e 50.\nO esquema funciona com os laterais a(c)tuando na defesa além dos zagueiros, então os laterais não avançam muito.No meio-campo, só direita e esquerda onde ambos ficam de sobra, pois na área já tem os 4 atacantes, além disso, eles precisam cuidar para impedir um contra-ataque do oponente.No ataque, ambos avançam, quando seu time não ataca, 2 deles voltam para o meio-campo e dois ficam mais avançados.', '4-2-4.gif');
  INSERT INTO rschemar.esquema_tatico (id_esquema_tatico, titulo, descricao, imagem) VALUES (6, '4-3-3', 'O 4-3-3 é conhecido como um esquema tático com quatro jogadores na defesa, três jogadores no meio-campo (com um ou dois volantes) e três jogadores no ataque (dois pontas e um atacante).\nEste esquema foi popular no final da década de 60 e início da década de 70, tendo sido usado pela Holanda na Copa de 1994.\nDo lado ofensivo do esquema, os pontas e os laterais sobem para o ataque, acabando por desarmar a defesa adversária --- já que o lateral adversário se vê obrigado a marcar dois jogadores. E, no aspecto defensivo, os três homens de frente auxiliam na marcação dos laterais/volantes adversários.\nO esquema 4-3-3 mostrou-se mais eficiênte nas equipes em que os jogadores de ataque, especialmente os que atuavam pelos flancos do campo, eram velozes, dinâmicos e capazes de ajudar na marcação. O fato de o meio-campo, teoricamente, ser composto por três jogadores faz com que a equipe dependa muito de um meia de ligação talentoso, pois se os outros dois homens de meio forem mais marcadores do que técnicos, as jogadas de ataque, em sua maioria, dependerão do jogador de criação. No entanto, muitas das equipes que adotam o esquema na atualidade apresentam volantes (também conhecidos como "volantes modernos"), polivalentes, versáteis e capazes de auxiliar na criação de jogadas ofensivas. Ainda no aspecto ofensivo, é muito conhecida a possibilidade de triangulação entre laterais e atacantes que atuem pelos flancos, criando jogadas de grande eficiência se efutuadas com velocidade e inteligência.', '4-3-3.gif');
  INSERT INTO rschemar.esquema_tatico (id_esquema_tatico, titulo, descricao, imagem) VALUES (7, '4-4-2', 'O mais utilizado atualmente, começou a ser usado nos anos 70, e é tão simples que não é necessária uma explicação detalhada sobre ele.', '4-4-2.gif');
  INSERT INTO rschemar.esquema_tatico (id_esquema_tatico, titulo, descricao, imagem) VALUES (8, '4-5-1', 'O 4-5-1 é um esquema de conteudo razoavelmente moderno dentro do mundo do futebol. Esse esquema de conteudo consiste em utilizar 4 defensores(2 zagueiros centrais e 2 laterais), 5 jogadores de meio-campo e apenas 1 atacante, além do goleiro. Muitas equipes utilizam um desdobramento do 4-5-1, o 4-4-1-1, que ao invés de jogar com uma linha de 5 jogadores no meio-de-campo, utilizam uma linha de 4 jogadores no meio-de-campo e 1 meia-atacante(como atuou Zidane na Copa do Mundo Fifa2006).\nEsse esquema permite uma melhor distribuição dos jogadores em campo na marcação, quando o time não tem a bola. Normalmente é usado o sistema de "back line", isto é: todos os jogadores atrás da linha da bola participando diretamente da marcação, as vezes com exceção do atacante.\nJogar desta forma também permite às equipes uma transição rápida para o ataque. O meio-campo normalmente se distribui com dois jogadores pelos lados e três mais centralizados. Assim, geralmente quando o time retoma a bola, os meio-campistas das pontas encostam no atacante se tornando praticamente pontas. Os outros três meio-campistas saem com a bola e organizam o conteudo na tentativa de chegar ao ataque.\nAssim, o sistema ofensivo de conteudo se torna praticamente um 4-3-3 à moda antiga, podendo variar a um 3-4-3 com a subida de um lateral. O sistema defensivo varia entre o 4-5-1, o 4-6-0(quando o atacante entra no "back line") e um 5-4-1 ou 5-5-0(se um meio-campista voltar para fazer a função de líbero)\nOs melhores exemplos de equipes que atuam ou atuaram no 4-5-1 são a França, Portugal a Itália e a Noruega, cada uma dentro das suas características próprias de sistemas ofensivo e defensivo.\n', '4-5-1.gif');
  INSERT INTO rschemar.esquema_tatico (id_esquema_tatico, titulo, descricao, imagem) VALUES (9, '4-6-0', 'O 4-6-0 é um esquema tá(c)tico com 4 defensores, 6 meio-campo e nenhum atacante.\nÉ usado quando seu time está sendo pressionado pelo adversário no esquema 4-5-1, sendo que o atacante volta ao meio-campo para ajudar a marcação.Uma tá(c)tica muito nova, foi criada no final dos anos 90.Ainda é pouco usado, pois as equipes usam o 4-5-1 ou o 5-4-1, para tá(c)ticas muito defensivas.', '4-6-0.gif');
  INSERT INTO rschemar.esquema_tatico (id_esquema_tatico, titulo, descricao, imagem) VALUES (10, '5-3-2', 'Uma tática muito defensiva no futebol, que é nova, criada nos anos 90.\nUma tática usada apenas quando seu time está na defesa para segurar algum resultado.Mas também é usada por alguns clubes quando se tem um conteudo difícil de ganhar ou de empatar.Funciona assim: os defensores contam com os laterais, que ficam mais atrás, há o líbero, e mais dois zagueiros. Os meias, todos avançam junto com os atacantes, porém os meias também voltam, os atacantes não. Nunca os dois laterais avançam, é costume nenhum avançar.', '5-3-2.gif');
  INSERT INTO rschemar.esquema_tatico (id_esquema_tatico, titulo, descricao, imagem) VALUES (11, '5-4-1', 'Formação de caráter muito defensivo, é constituída por três zagueiros, dois laterais (normalmente dois meias-ofensivos/armadores), dois volantes e somente um atacante.', '5-4-1.gif');
  INSERT INTO rschemar.esquema_tatico (id_esquema_tatico, titulo, descricao, imagem) VALUES (12, '5-5-0', 'O 5-5-0 é uma tática com cinco defensores( 2 laterais, 2 zagueiros e um líbero e cinco no meio-campo(2 volantes e três meias), é uma das mais defensivas táticas de uma equipe, uma tática muito usada para segurar o ataque da equipe adversária(quando sua equipe está ganhando uma partida complicada e com o aversário tentando empatar a partida).\nTudo acontece quando sua equipe está ganhando a partida por um gol(o) de diferença, na tática 5-4-1 e o adversário pressiona para tentar empatar, então o único atacante de sua equipe fica no bankline, isto é, volta para ajudar na marcação no [meio-campo], deixando assim de ser atacante.\nCaso sua equipe sofra o empate, aí o técnico terá que mudar o 5-4-1, para o 4-3-3, 3-4-3, 3-3-4 ou até mesmo o 4-2-4.', '5-5-0.gif');
"""
