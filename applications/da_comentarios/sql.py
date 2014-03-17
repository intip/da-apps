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

#selects
select_nextval_conteudo = ("SELECT NEXTVAL('rschemar.conteudo_id_conteudo_seq'::text) as id")

select_nextval_participante = ("SELECT NEXTVAL('rschemar.participante_id_usuario_seq'::text) as id")

select_status_content = ("SELECT publicado FROM rschemar.conteudo "
"WHERE id_conteudo=%(id_conteudo)i")

select_dados = ("SELECT N.id_conteudo, N.titulo, N.descricao, "
"N.vigencia_de, N.vigencia_ate, N.resultado, N.categoria, N.tipo, "
"N.servico, N.extra, N.finalizada, "
"to_char(N.expira_em, 'YYYY-MM-DD HH24:MI') as expira_em, "
"to_char(N.publicado_em, 'YYYY-MM-DD HH24:MI') as publicado_em, N.publicado, "
"to_char(N.atualizado_em, 'YYYY-MM-DD HH24:MI') as atualizado_em, "
"D.id_destaque, D.titulo as titulo_destaque, D.descricao as descricao_destaque, "
"D.img, D.img as imagem_destaque, D.peso as peso_destaque "
"FROM rschemar.conteudo N "
"LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo) "
"WHERE N.id_conteudo=%(id_conteudo)i")

select_titulo = ("SELECT titulo FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

select_dublin_core = ("SELECT titulo, descricao, "
"to_char(atualizado_em, 'YYYY-MM-DD HH24:MI:SS') as atualizado_em, "
"to_char(publicado_em, 'YYYY-MM-DD HH24:MI:SS') as publicado_em "
"FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

select_conteudo = ("SELECT N.id_conteudo, N.titulo, N.descricao, N.finalizada, "
"to_char(N.vigencia_de, 'DD/MM/YYYY HH24:MI') as vigencia_de, " 
"to_char(N.vigencia_ate, 'DD/MM/YYYY HH24:MI') as vigencia_ate, " 
"to_char(N.resultado, 'DD/MM/YYYY HH24:MI') as resultado, "
"R.id_regulamento, R.regulamento, "
"R.titulo as titulo_regulamento, N.servico, N.extra, N.categoria, N.tipo, "
"N.num_sorteados, to_char(N.expira_em, 'DD/MM/YYYY HH24:MI') as expira_em, "
"to_char(N.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em, N.publicado, "
"D.id_destaque, D.titulo as titulo_destaque, D.descricao as descricao_destaque, "
"D.img, D.img as imagem_destaque, D.peso as peso_destaque "
"FROM rschemar.conteudo N "
"LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo) "
"INNER JOIN rschemar.regulamento R ON (N.id_regulamento=R.id_regulamento) "
"WHERE N.id_conteudo=%(id_conteudo)i")

select_conteudos = ("SELECT id_conteudo, titulo FROM rschemar.conteudo "
"ORDER BY id_conteudo ASC")

select_usuario_promocao_id_conteudo = ("SELECT P.id_usuario, P.nome, P.cpf, P.email, P.bloqueio, N.status, "
"C.id_conteudo, C.titulo, "
"(SELECT count(*) FROM rschemar.participante_promocao PPS "
"INNER JOIN rschemar.participante PS ON (PS.id_usuario=PPS.id_usuario) "
"INNER JOIN rschemar.conteudo CS ON (CS.id_conteudo=PPS.id_conteudo) "
"WHERE PS.cpf=P.cpf AND PS.nome=P.nome AND CS.id_conteudo=C.id_conteudo) as total "
"FROM rschemar.participante P "
"INNER JOIN rschemar.participante_promocao N ON (N.id_usuario=P.id_usuario) "
"INNER JOIN rschemar.conteudo C ON (C.id_conteudo=N.id_conteudo) "
"WHERE P.duplicado='false' AND "
"N.id_conteudo =%(id_conteudo)i AND P.bloqueio <> 'true' "
"AND N.status='livre'"
"LIMIT %(limit)i OFFSET %(offset)i ")

select_usuarios_promocoes_all = ("SELECT P.id_usuario, P.nome, P.cpf, P.email, P.bloqueio, N.status, "
"C.id_conteudo, C.titulo, "
"(SELECT count(*) FROM rschemar.participante_promocao PPS "
"INNER JOIN rschemar.participante PS ON (PS.id_usuario=PPS.id_usuario) "
"INNER JOIN rschemar.conteudo CS ON (CS.id_conteudo=PPS.id_conteudo) "
"WHERE PS.cpf=P.cpf AND PS.nome=P.nome AND CS.id_conteudo=C.id_conteudo) as total "
"FROM rschemar.participante P "
"INNER JOIN rschemar.participante_promocao N ON (N.id_usuario=P.id_usuario) "
"INNER JOIN rschemar.conteudo C ON (C.id_conteudo=N.id_conteudo) "
"WHERE P.duplicado='false' AND "
"N.id_conteudo =%(id_conteudo)i ")

select_promocoes_sort_auto = ("SELECT id_conteudo, titulo FROM rschemar.conteudo "
"WHERE resultado >= %(data_de)s AND resultado <= %(data_ate)s AND finalizada ='false' "
"AND tipo <>'cultural'")

select_contemplados = ("""SELECT DISTINCT ON (P.email) email, P.nome, P.endereco, P.bairro, 
P.numero, P.cidade, P.estado, P.cep, P.cpf, P.telefone,
(SELECT count(*) FROM rschemar.sorteados S 
LEFT JOIN rschemar.participante PS ON (S.id_usuario=PS.id_usuario) 
WHERE PS.email=P.email) as total 
FROM rschemar.participante P RIGHT JOIN rschemar.sorteados SS
ON (SS.id_usuario=P.id_usuario)""")

select_usuarios_promocoes_all2 = ("SELECT P.id_usuario, P.nome, P.cpf, P.email, N.status, "
"P.telefone, P.endereco, P.cep, P.bairro, P.cidade, P.numero, P.estado, "
"(SELECT count(*) FROM rschemar.participante_promocao "
"WHERE id_conteudo=%(id_conteudo)i) as total, "
"to_char(dhora_participacao, 'DD/MM/YYYY HH24:MI') as dhora_participacao  "
"FROM rschemar.participante P "
"INNER JOIN rschemar.participante_promocao N ON (N.id_usuario=P.id_usuario) "
"WHERE N.id_conteudo =%(id_conteudo)i ")

select_usuarios_promocoes = ("SELECT P.id_usuario, P.nome, P.cpf, P.email, P.bloqueio, N.status, "
"C.id_conteudo, C.titulo, "
"(SELECT count(*) FROM rschemar.participante_promocao PPS "
"INNER JOIN rschemar.participante PS ON (PS.id_usuario=PPS.id_usuario) WHERE PS.cpf=P.cpf "
"AND PS.nome=P.nome ) as total "
"FROM rschemar.participante P "
"INNER JOIN rschemar.participante_promocao N ON (N.id_usuario=P.id_usuario) "
"INNER JOIN rschemar.conteudo C ON (C.id_conteudo=N.id_conteudo) "
"WHERE P.bloqueio='false' AND P.duplicado='false' "
"AND N.status='livre' "
"LIMIT %(limit)i OFFSET %(offset)i")

select_usuario_promocao_blackid = ("SELECT P.id_usuario, P.nome, P.cpf, P.email, "
"P.bloqueio, C.id_conteudo, C.titulo, N.status, "
"(SELECT count(*) FROM rschemar.participante_promocao PPS "
"INNER JOIN rschemar.participante PS ON (PS.id_usuario=PPS.id_usuario) "
"INNER JOIN rschemar.conteudo CS ON (CS.id_conteudo=PPS.id_conteudo) "
"WHERE PS.cpf=P.cpf AND PS.nome=P.nome AND CS.id_conteudo=C.id_conteudo) as total "
"FROM rschemar.participante P "
"INNER JOIN rschemar.participante_promocao N ON (N.id_usuario=P.id_usuario) "
"INNER JOIN rschemar.conteudo C ON (C.id_conteudo=N.id_conteudo) "
"WHERE N.id_conteudo=%(id_conteudo)i AND (P.bloqueio='true' OR N.status<>'livre') "
"AND P.duplicado='false' "
"LIMIT %(limit)i OFFSET %(offset)i")

select_usuario_blacklist = ("SELECT P.id_usuario, P.nome, P.cpf, P.email, "
"P.bloqueio, N.status, "
"(SELECT count(*) FROM rschemar.participante_promocao PPS "
"INNER JOIN rschemar.participante PS ON (PS.id_usuario=PPS.id_usuario) "
"INNER JOIN rschemar.conteudo CS ON (CS.id_conteudo=PPS.id_conteudo) "
"WHERE PS.cpf=P.cpf AND PS.nome=P.nome) as total "
"FROM rschemar.participante P "
"INNER JOIN rschemar.participante_promocao N ON (N.id_usuario=P.id_usuario) "
"WHERE (P.bloqueio='true' OR N.status<>'livre') AND P.duplicado='false' "
"LIMIT %(limit)i OFFSET %(offset)i")

select_usuario_email = ("SELECT P.id_usuario, P.nome, P.cpf, P.email, P.bloqueio, N.status, "
"(SELECT count(*) FROM rschemar.participante_promocao PPS "
"INNER JOIN rschemar.participante PS ON (PS.id_usuario=PPS.id_usuario) "
"INNER JOIN rschemar.conteudo CS ON (CS.id_conteudo=PPS.id_conteudo) "
"WHERE PS.cpf=P.cpf AND PS.nome=P.nome) as total "
"FROM rschemar.participante P "
"INNER JOIN rschemar.participante_promocao N ON (N.id_usuario=P.id_usuario) "
"WHERE P.email=%(email)s AND P.duplicado='false'")

select_usuario_nome = ("SELECT P.id_usuario, P.nome, P.cpf, P.email, P.bloqueio, N.status, "
"(SELECT count(*) FROM rschemar.participante_promocao PPS "
"INNER JOIN rschemar.participante PS ON (PS.id_usuario=PPS.id_usuario) "
"INNER JOIN rschemar.conteudo CS ON (CS.id_conteudo=PPS.id_conteudo) "
"WHERE PS.cpf=P.cpf AND PS.nome=P.nome) as total "
"FROM rschemar.participante P "
"INNER JOIN rschemar.participante_promocao N ON (N.id_usuario=P.id_usuario) "
"WHERE P.nome ~* %(nome)s AND P.duplicado='false'")

select_user_cpf = ("SELECT P.id_usuario, P.nome, P.cpf, P.email, P.bloqueio, N.status, "
"(SELECT count(*) FROM rschemar.participante_promocao PPS "
"INNER JOIN rschemar.participante PS ON (PS.id_usuario=PPS.id_usuario) "
"INNER JOIN rschemar.conteudo CS ON (CS.id_conteudo=PPS.id_conteudo) "
"WHERE PS.cpf=P.cpf AND PS.nome=P.nome) as total "
"FROM rschemar.participante P "
"INNER JOIN rschemar.participante_promocao N ON (N.id_usuario=P.id_usuario) "
"WHERE P.cpf=%(cpf)s AND P.duplicado='false'")

select_user_cpf_id_conteudo =  ("SELECT P.id_usuario, P.nome, P.cpf, P.email, P.bloqueio, N.status, "
"(SELECT count(*) FROM rschemar.participante_promocao PPS "
"INNER JOIN rschemar.participante PS ON (PS.id_usuario=PPS.id_usuario) "
"INNER JOIN rschemar.conteudo CS ON (CS.id_conteudo=PPS.id_conteudo) "
"WHERE PS.cpf=P.cpf AND PS.nome=P.nome AND PPS.id_conteudo=N.id_conteudo) as total "
"FROM rschemar.participante P "
"INNER JOIN rschemar.participante_promocao N ON (N.id_usuario=P.id_usuario) "
"WHERE P.cpf=%(cpf)s AND P.duplicado='false' AND N.id_conteudo=%(id_conteudo)i")

select_usuario = ("SELECT U.id_usuario, U.nome, U.cpf, U.email, U.bloqueio, U.numero, "
"U.bairro, U.cidade, U.endereco, U.cep, " 
"P.status, P.frase FROM rschemar.participante U "
"LEFT JOIN rschemar.participante_promocao P ON (P.id_usuario=U.id_usuario) "
"WHERE U.id_usuario=%(id_usuario)i ")

select_regulamentos = ("SELECT id_regulamento, titulo, regulamento FROM rschemar.regulamento ORDER BY titulo ASC")

select_dhora_participante = ("SELECT to_char(dhora_participacao, 'DD/MM/YYYY HH24:MI') as dhora_participacao "  
"FROM rschemar.participante WHERE email=%(email)s ORDER BY id_usuario DESC LIMIT 1")

select_dhora_participante_idconteudo = ("SELECT to_char(dhora_participacao, 'DD/MM/YYYY HH24:MI') as dhora_participacao "  
"FROM rschemar.participante P "
"RIGHT JOIN rschemar.participante_promocao PP ON (P.id_usuario=PP.id_usuario) "
"WHERE P.email=%(email)s AND PP.id_conteudo=%(id_conteudo)s ORDER BY P.id_usuario DESC LIMIT 1")

select_sorteados_promocao = ("SELECT P.id_usuario, P.nome, P.cpf, P.email, "
"P.bloqueio, C.id_conteudo, C.titulo, N.status, S.dia_hora, "
"(SELECT count(*) FROM rschemar.participante_promocao PPS "
"INNER JOIN rschemar.participante PS ON (PS.id_usuario=PPS.id_usuario) "
"INNER JOIN rschemar.conteudo CS ON (CS.id_conteudo=PPS.id_conteudo) "
"WHERE PS.cpf=P.cpf AND PS.nome=P.nome AND CS.id_conteudo=C.id_conteudo) as total "
"FROM rschemar.participante P "
"INNER JOIN rschemar.sorteados S ON (P.id_usuario=S.id_usuario) "
"INNER JOIN rschemar.conteudo C ON (C.id_conteudo=S.id_conteudo) "
"INNER JOIN rschemar.participante_promocao N ON (P.id_usuario=N.id_usuario) "
"WHERE N.status<>'desclassificado' AND S.id_conteudo=%(id_conteudo)i "
"ORDER BY S.id_sort ASC LIMIT %(limit)i OFFSET %(offset)i ")

select_sorteados_promocao_not_limit = ("SELECT P.id_usuario, P.nome, P.cpf, P.email, "
"P.bloqueio, C.id_conteudo, C.titulo, N.status, S.dia_hora "
"FROM rschemar.participante P "
"INNER JOIN rschemar.sorteados S ON (P.id_usuario=S.id_usuario) "
"INNER JOIN rschemar.conteudo C ON (C.id_conteudo=S.id_conteudo) "
"INNER JOIN rschemar.participante_promocao N ON (P.id_usuario=N.id_usuario) "
"WHERE N.status<>'desclassificado' AND S.id_conteudo=%(id_conteudo)i "
"ORDER BY P.nome ASC")

select_desclassificados_promocao = ("SELECT P.id_usuario, P.nome, P.cpf, P.email, "
"P.bloqueio, C.id_conteudo, C.titulo, N.status, S.dia_hora, "
"(SELECT count(*) FROM rschemar.participante_promocao PPS "
"INNER JOIN rschemar.participante PS ON (PS.id_usuario=PPS.id_usuario) "
"INNER JOIN rschemar.conteudo CS ON (CS.id_conteudo=PPS.id_conteudo) "
"WHERE PS.cpf=P.cpf AND PS.nome=P.nome AND CS.id_conteudo=C.id_conteudo) as total "
"FROM rschemar.participante P "
"INNER JOIN rschemar.participante_promocao N ON (N.id_usuario=P.id_usuario) "
"INNER JOIN rschemar.conteudo C ON (C.id_conteudo=N.id_conteudo) "
"LEFT JOIN rschemar.sorteados S ON (S.id_usuario=P.id_usuario) "
"WHERE N.id_conteudo=%(id_conteudo)i AND N.status='desclassificado' "
"LIMIT %(limit)i OFFSET %(offset)i")

select_desclassificados = ("SELECT P.id_usuario, P.nome, P.cpf, P.email, "
"P.bloqueio, N.status, S.dia_hora, "
"(SELECT count(*) FROM rschemar.participante_promocao PPS "
"INNER JOIN rschemar.participante PS ON (PS.id_usuario=PPS.id_usuario) "
"INNER JOIN rschemar.conteudo CS ON (CS.id_conteudo=PPS.id_conteudo) "
"WHERE PS.cpf=P.cpf AND PS.nome=P.nome) as total "
"FROM rschemar.participante P "
"INNER JOIN rschemar.participante_promocao N ON (N.id_usuario=P.id_usuario) "
"INNER JOIN rschemar.sorteados S ON (S.id_usuario=N.id_usuario) "
"WHERE N.status='desclassificado' "
"LIMIT %(limit)i OFFSET %(offset)i")

select_sorteados = ("SELECT P.id_usuario, P.nome, P.cpf, P.email, "
"P.bloqueio, N.status, S.dia_hora, "
"(SELECT count(*) FROM rschemar.participante_promocao PPS "
"INNER JOIN rschemar.participante PS ON (PS.id_usuario=PPS.id_usuario) "
"INNER JOIN rschemar.conteudo CS ON (CS.id_conteudo=PPS.id_conteudo) "
"WHERE PS.cpf=P.cpf AND PS.nome=P.nome) as total "
"FROM rschemar.participante P "
"INNER JOIN rschemar.participante_promocao N ON (N.id_usuario=P.id_usuario) "
"INNER JOIN rschemar.sorteados S ON (S.id_usuario=N.id_usuario) "
"WHERE N.status <>'desclassificado' "
"LIMIT %(limit)i OFFSET %(offset)i")

select_status_usuario = ("SELECT P.bloqueio FROM rschemar.participante P "
"WHERE P.email=%(email)s AND P.duplicado='false' LIMIT 1")

select_status_usuario_promocao = ("SELECT P.nome, P.cpf, PP.status FROM rschemar.participante P "
"INNER JOIN rschemar.participante_promocao PP ON (P.id_usuario=PP.id_usuario) "
"WHERE P.cpf=%(cpf)s AND PP.id_conteudo=%(id_conteudo)i AND P.duplicado='false'")

select_frases_participantes = ("SELECT P.id_usuario, P.nome, P.cpf, P.email, PP.frase, "
" P.endereco, P.cep, P.numero, P.bairro, P.cidade FROM rschemar.participante P "
"INNER JOIN rschemar.participante_promocao PP ON (P.id_usuario=PP.id_usuario) "
"WHERE PP.id_conteudo=%(id_conteudo)i AND P.bloqueio<>'true' AND PP.status<>'desclassificado' "
"AND P.id_usuario NOT IN (SELECT S.id_usuario FROM rschemar.sorteados S )")

select_frases_participantes_limit = ("SELECT P.id_usuario, P.nome, P.cpf, P.email, PP.frase, "
" P.endereco, P.cep, P.numero, P.bairro, P.cidade FROM rschemar.participante P "
"INNER JOIN rschemar.participante_promocao PP ON (P.id_usuario=PP.id_usuario) "
"WHERE PP.id_conteudo=%(id_conteudo)i AND P.bloqueio<>'true' AND PP.status<>'desclassificado' "
"AND P.id_usuario NOT IN (SELECT S.id_usuario FROM rschemar.sorteados S ) LIMIT %(limit)i "
"OFFSET %(offset)i")

select_id_user_email = ("SELECT P.id_usuario FROM rschemar.participante P "
"RIGHT JOIN rschemar.participante_promocao PP ON (P.id_usuario=PP.id_usuario) "
"WHERE PP.id_conteudo=%(id_conteudo)i AND email=%(email)s")

select_user_email_id_conteudo = ("SELECT P.id_usuario, P.nome, P.cpf, P.email, P.bloqueio, N.status, "
"(SELECT count(*) FROM rschemar.participante_promocao PPS "
"INNER JOIN rschemar.participante PS ON (PS.id_usuario=PPS.id_usuario) "
"INNER JOIN rschemar.conteudo CS ON (CS.id_conteudo=PPS.id_conteudo) "
"WHERE PS.cpf=P.cpf AND PS.nome=P.nome AND PPS.id_conteudo=N.id_conteudo) as total "
"FROM rschemar.participante P "
"INNER JOIN rschemar.participante_promocao N ON (N.id_usuario=P.id_usuario) "
"WHERE P.email=%(email)s AND P.duplicado='false' AND N.id_conteudo=%(id_conteudo)i")

select_user_nome_id_conteudo = ("SELECT P.id_usuario, P.nome, P.cpf, P.email, P.bloqueio, N.status, "
"(SELECT count(*) FROM rschemar.participante_promocao PPS "
"INNER JOIN rschemar.participante PS ON (PS.id_usuario=PPS.id_usuario) "
"INNER JOIN rschemar.conteudo CS ON (CS.id_conteudo=PPS.id_conteudo) "
"WHERE PS.cpf=P.cpf AND PS.nome=P.nome AND PPS.id_conteudo=N.id_conteudo) as total "
"FROM rschemar.participante P "
"INNER JOIN rschemar.participante_promocao N ON (N.id_usuario=P.id_usuario) "
"WHERE P.nome ~* %(nome)s AND P.duplicado='false' AND N.id_conteudo=%(id_conteudo)i")

select_sorteio_primeiro_cadastrar = ("""SELECT MIN(P.id_usuario) as id_usuario FROM rschemar.participante P 
                                        INNER JOIN rschemar.participante_promocao PP ON (P.id_usuario=PP.id_usuario) 
                                        WHERE PP.id_conteudo=%(id_conteudo)i AND PP.status='livre' AND P.bloqueio='false' AND P.email 
                                        NOT IN(SELECT PS.email FROM rschemar.participante PS RIGHT JOIN 
                                        rschemar.sorteados S ON (PS.id_usuario=S.id_usuario) WHERE S.id_conteudo=PP.id_conteudo
                                        OR S.dia_hora >= %(data)s)
                                        GROUP BY P.email ORDER BY email 
                                        ASC LIMIT %(limit)i""")

select_sorteio_aleatorio = ("""SELECT  DISTINCT ON (P.email) email, random() as user_rand, P.id_usuario as id_usuario 
	                             FROM rschemar.participante P 
                               INNER JOIN rschemar.participante_promocao PP ON (P.id_usuario=PP.id_usuario) 
                               WHERE PP.id_conteudo=%(id_conteudo)i AND PP.status='livre' AND P.bloqueio='false' AND P.email 
                               NOT IN(SELECT PS.email FROM rschemar.participante PS RIGHT JOIN 
                               rschemar.sorteados S ON (PS.id_usuario=S.id_usuario) WHERE S.id_conteudo=PP.id_conteudo
                               OR %(data)s <= S.dia_hora)
                               ORDER BY P.email, user_rand""")

select_sorteio_aleatorio_prom = ("""SELECT  DISTINCT ON (P.email) email, random() as user_rand, P.id_usuario as id_usuario 
                                    FROM rschemar.participante P 
                                    INNER JOIN rschemar.participante_promocao PP ON (P.id_usuario=PP.id_usuario) 
                                    WHERE PP.id_conteudo=%(id_conteudo)i AND PP.status='livre' AND P.bloqueio='false' AND  
                                    (SELECT count(PS.email) FROM rschemar.participante PS 
                                     RIGHT JOIN rschemar.sorteados S ON (PS.id_usuario=S.id_usuario) 
                                     INNER JOIN rschemar.participante_promocao PPS ON (PPS.id_usuario=PS.id_usuario)
                                     WHERE PS.email=P.email AND PPS.status='sorteado' AND (PPS.id_conteudo < PP.id_conteudo 
                                     OR PPS.id_conteudo > PP.id_conteudo) LIMIT %(bloqueio_numero)i) = 0
                                    ORDER BY P.email, user_rand""")


select_sorteio_primeiro_cadastrar_prom = ("""SELECT MIN(P.id_usuario) as id_usuario  FROM rschemar.participante P 
                                             INNER JOIN rschemar.participante_promocao PP ON (P.id_usuario=PP.id_usuario) 
                                             WHERE PP.id_conteudo=%(id_conteudo)i AND PP.status='livre' AND P.bloqueio='false' AND
                                             (SELECT count(PS.email) FROM rschemar.participante PS 
                                             RIGHT JOIN rschemar.sorteados S ON (PS.id_usuario=S.id_usuario) 
                                             INNER JOIN rschemar.participante_promocao PPS ON (PPS.id_usuario=PS.id_usuario)
                                             WHERE PS.email=P.email AND PPS.status='sorteado' AND (PPS.id_conteudo < PP.id_conteudo 
                                             OR PPS.id_conteudo > PP.id_conteudo)LIMIT %(bloqueio_numero)i) = 0""")

select_promocoes_limit = ("SELECT N.id_conteudo, N.titulo, N.descricao, N.finalizada,  "
"to_char(N.vigencia_de, 'DD/MM/YYYY HH24:MI') as vigencia_de, " 
"to_char(N.vigencia_ate, 'DD/MM/YYYY HH24:MI') as vigencia_ate, " 
"to_char(N.resultado, 'DD/MM/YYYY HH24:MI') as resultado, "
"N.servico, N.extra, N.categoria, N.tipo, "
"N.num_sorteados, to_char(N.expira_em, 'DD/MM/YYYY HH24:MI') as expira_em, "
"to_char(N.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em, N.publicado, "
"D.id_destaque, D.titulo as titulo_destaque, D.descricao as descricao_destaque, "
"D.img, D.img as imagem_destaque, D.peso as peso_destaque "
"FROM rschemar.conteudo N "
"RIGHT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo) "
"WHERE N.publicado ='true' AND N.finalizada='false' "
"AND N.vigencia_ate >= now() "
"ORDER BY N.id_conteudo DESC LIMIT %(limit)i")

select_promocoes = ("SELECT N.id_conteudo, N.titulo, N.descricao, N.finalizada,  "
"to_char(N.vigencia_de, 'DD/MM/YYYY HH24:MI') as vigencia_de, " 
"to_char(N.vigencia_ate, 'DD/MM/YYYY HH24:MI') as vigencia_ate, " 
"to_char(N.resultado, 'DD/MM/YYYY HH24:MI') as resultado, "
"N.servico, N.extra, N.categoria, N.tipo, "
"N.num_sorteados, to_char(N.expira_em, 'DD/MM/YYYY HH24:MI') as expira_em, "
"to_char(N.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em, N.publicado, "
"D.id_destaque, D.titulo as titulo_destaque, D.descricao as descricao_destaque, "
"D.img, D.img as imagem_destaque, D.peso as peso_destaque "
"FROM rschemar.conteudo N "
"RIGHT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo) "
"WHERE N.publicado ='true' AND N.finalizada='false' "
"AND N.vigencia_ate >= now() "
"ORDER BY N.id_conteudo DESC")

select_promocoes_limit_finalizadas = ("SELECT N.id_conteudo, N.titulo, N.descricao, N.finalizada,  "
"to_char(N.vigencia_de, 'DD/MM/YYYY HH24:MI') as vigencia_de, " 
"to_char(N.vigencia_ate, 'DD/MM/YYYY HH24:MI') as vigencia_ate, " 
"to_char(N.resultado, 'DD/MM/YYYY HH24:MI') as resultado, "
"N.servico, N.extra, N.categoria, N.tipo, "
"N.num_sorteados, to_char(N.expira_em, 'DD/MM/YYYY HH24:MI') as expira_em, "
"to_char(N.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em, N.publicado, "
"D.id_destaque, D.titulo as titulo_destaque, D.descricao as descricao_destaque, "
"D.img, D.img as imagem_destaque, D.peso as peso_destaque "
"FROM rschemar.conteudo N "
"RIGHT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo) "
"WHERE N.publicado ='true' AND N.finalizada='true' "
"ORDER BY N.id_conteudo DESC LIMIT %(limit)i")

select_promocoes_finalizadas = ("SELECT N.id_conteudo, N.titulo, N.descricao, N.finalizada,  "
"to_char(N.vigencia_de, 'DD/MM/YYYY HH24:MI') as vigencia_de, " 
"to_char(N.vigencia_ate, 'DD/MM/YYYY HH24:MI') as vigencia_ate, " 
"to_char(N.resultado, 'DD/MM/YYYY HH24:MI') as resultado, "
"N.servico, N.extra, N.categoria, N.tipo, "
"N.num_sorteados, to_char(N.expira_em, 'DD/MM/YYYY HH24:MI') as expira_em, "
"to_char(N.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em, N.publicado, "
"D.id_destaque, D.titulo as titulo_destaque, D.descricao as descricao_destaque, "
"D.img, D.img as imagem_destaque, D.peso as peso_destaque "
"FROM rschemar.conteudo N "
"RIGHT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo) "
"WHERE N.publicado ='true' AND N.finalizada='true' "
"ORDER BY N.id_conteudo DESC")

#counts do database:(Arrumar todos os counts pois eles estao doidao) criar o select count com o group by acima
select_count_user_nome = ("SELECT count(*) "
  "FROM rschemar.participante P WHERE P.nome ~* %(nome)s AND P.duplicado='false'")

select_count_user_email = ("SELECT count(*) "
  "FROM rschemar.participante P WHERE P.email=%(email)s AND P.duplicado='false'")

select_count_user_email_id_conteudo = ("SELECT count(*) "
"FROM rschemar.participante P  "
"INNER JOIN rschemar.participante_promocao PP ON (P.id_usuario=PP.id_usuario) "
"WHERE P.email=%(email)s AND P.duplicado='false' AND PP.id_conteudo=%(id_conteudo)i")

select_count_user_nome_id_conteudo = ("SELECT count(*) "
"FROM rschemar.participante P  "
"INNER JOIN rschemar.participante_promocao PP ON (P.id_usuario=PP.id_usuario) "
"WHERE P.nome ~* %(nome)s AND P.duplicado='false' AND PP.id_conteudo=%(id_conteudo)i")

select_count_user_cpf_id_conteudo = ("SELECT count(*) "
"FROM rschemar.participante P  "
"INNER JOIN rschemar.participante_promocao PP ON (P.id_usuario=PP.id_usuario) "
"WHERE P.cpf=%(cpf)s AND P.duplicado='false' AND PP.id_conteudo=%(id_conteudo)i")

select_count_user_cpf = ("SELECT count(*) "
  "FROM rschemar.participante P WHERE P.cpf=%(cpf)s AND P.duplicado='false'")

select_count_usuario_promocao = ("SELECT count(*) FROM rschemar.participante_promocao PP "
"INNER JOIN rschemar.participante P ON (PP.id_usuario=P.id_usuario) WHERE id_conteudo=%(id_conteudo)i "
" AND P.bloqueio <> 'true' AND P.duplicado='false' AND PP.status='livre'")

select_count_usuario_total = ("SELECT count(*) FROM rschemar.participante_promocao PP "
"LEFT JOIN rschemar.participante P ON (P.id_usuario=PP.id_usuario) "
"WHERE P.duplicado='false' AND PP.status='livre'")

select_usuario_promocao_blackid_count = ("SELECT count(*) FROM rschemar.participante_promocao PP "
"INNER JOIN rschemar.participante P ON (P.id_usuario=PP.id_usuario) "
"WHERE PP.id_conteudo=%(id_conteudo)i AND (P.bloqueio='true' OR PP.status<>'livre') AND P.duplicado='false' ")

select_usuario_blacklist_count = ("SELECT count(*) FROM rschemar.participante P "
"INNER JOIN rschemar.participante_promocao N ON (P.id_usuario=N.id_usuario) "
"WHERE (P.bloqueio='true' OR N.status<>'livre') AND P.duplicado='false'")

select_count_sorteados_promocao = ("SELECT count(*) FROM rschemar.participante_promocao PP "
"LEFT JOIN rschemar.participante P ON (P.id_usuario=PP.id_usuario) "
"WHERE PP.id_conteudo=%(id_conteudo)i and PP.status='sorteado' ")

select_sorteados_promocao_desclassificados_count = ("SELECT count(*) FROM rschemar.sorteados S "
"LEFT JOIN rschemar.participante_promocao PP ON (PP.id_usuario=S.id_usuario) "
"LEFT JOIN rschemar.participante P ON (P.id_usuario=S.id_usuario) "
"WHERE PP.id_conteudo=%(id_conteudo)i AND PP.status='desclassificado' ")

select_sorteados_desclassificados_count = ("SELECT count(*) FROM rschemar.sorteados S "
"LEFT JOIN rschemar.participante_promocao PP ON (S.id_usuario=PP.id_usuario) "
"LEFT JOIN rschemar.participante P ON (S.id_usuario=P.id_usuario) "
"WHERE PP.status='desclassificado' ")

select_count_sorteados_total = ("SELECT count(*) FROM rschemar.sorteados S "
"LEFT JOIN rschemar.participante_promocao PP ON (S.id_usuario=PP.id_usuario) "
"LEFT JOIN rschemar.participante P ON (P.id_usuario=S.id_usuario) "
"WHERE PP.status ='sorteado' ")

select_duplicado_user = ("SELECT P.duplicado FROM rschemar.participante P "
"LEFT JOIN rschemar.participante_promocao PP ON (P.id_usuario=PP.id_usuario) "
"WHERE P.nome=%(nome)s AND P.cpf=%(cpf)s AND PP.id_conteudo=%(id_conteudo)s LIMIT 1")

select_count_participacoes_promocao = ("SELECT count(*) FROM rschemar.participante_promocao "
"WHERE id_conteudo=%(id_conteudo)i")

select_promocoes_finalizada_dias = ("SELECT N.id_conteudo, N.titulo, N.descricao, N.finalizada,  "
"to_char(N.vigencia_de, 'DD/MM/YYYY HH24:MI') as vigencia_de, " 
"to_char(N.vigencia_ate, 'DD/MM/YYYY HH24:MI') as vigencia_ate, " 
"to_char(N.resultado, 'DD/MM/YYYY HH24:MI') as resultado, "
"R.id_regulamento, R.regulamento, "
"R.titulo as titulo_regulamento, N.servico, N.extra, N.categoria, N.tipo, "
"N.num_sorteados, to_char(N.expira_em, 'DD/MM/YYYY HH24:MI') as expira_em, "
"to_char(N.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em, N.publicado, "
"D.id_destaque, D.titulo as titulo_destaque, D.descricao as descricao_destaque, "
"D.img, D.img as imagem_destaque, D.peso as peso_destaque "
"FROM rschemar.conteudo N "
"RIGHT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo) "
"INNER JOIN rschemar.regulamento R ON (N.id_regulamento=R.id_regulamento) "
"WHERE N.finalizada='true' AND N.publicado='true' AND N.resultado >= %(data)s")

select_promocoes_finalizada_dias_limit = ("SELECT N.id_conteudo, N.titulo, N.descricao, N.finalizada,  "
"to_char(N.vigencia_de, 'DD/MM/YYYY HH24:MI') as vigencia_de, " 
"to_char(N.vigencia_ate, 'DD/MM/YYYY HH24:MI') as vigencia_ate, " 
"to_char(N.resultado, 'DD/MM/YYYY HH24:MI') as resultado, "
"R.id_regulamento, R.regulamento, "
"R.titulo as titulo_regulamento, N.servico, N.extra, N.categoria, N.tipo, "
"N.num_sorteados, to_char(N.expira_em, 'DD/MM/YYYY HH24:MI') as expira_em, "
"to_char(N.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em, N.publicado, "
"D.id_destaque, D.titulo as titulo_destaque, D.descricao as descricao_destaque, "
"D.img, D.img as imagem_destaque, D.peso as peso_destaque "
"FROM rschemar.conteudo N "
"RIGHT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo) "
"INNER JOIN rschemar.regulamento R ON (N.id_regulamento=R.id_regulamento) "
"WHERE N.finalizada='true' AND N.publicado='true' AND N.resultado >= %(data)s "
"LIMIT %(limit)i")

#inserts
insert_conteudo = ("INSERT INTO rschemar.conteudo (id_conteudo, titulo, descricao, vigencia_de, vigencia_ate,"
"resultado, id_regulamento, servico, extra, categoria, publicado_em, expira_em, publicado, tipo, num_sorteados) " 
" VALUES (%(id_conteudo)i, %(titulo)s, %(descricao)s, %(vigencia_de)s, %(vigencia_ate)s, %(resultado)s, "
" %(id_regulamento)i, %(servico)s, %(extra)s, %(categoria)s, %(publicado_em)s, %(expira_em)s, %(publicado)s,"
" %(tipo)s, %(num_sorteados)s)")

insert_destaque  = ("INSERT INTO rschemar.destaque (id_conteudo, titulo, descricao, img, peso) VALUES "
"(%(id_conteudo)i, %(titulo)s, %(descricao)s, %(img)s, %(peso)i)")

insert_regulamento = ("INSERT INTO rschemar.regulamento (titulo, regulamento) VALUES "
"(%(titulo)s, %(regulamento)s)")

insert_promocao_user = ("INSERT INTO rschemar.participante_promocao (id_usuario, id_conteudo, status, frase) "
"VALUES(%(id_usuario)i, %(id_conteudo)s, %(status)s, %(frase)s)")

insert_participante = ("INSERT INTO rschemar.participante (id_usuario, id_usuario_wad, nome, cpf, email, "
"endereco, numero, complemento, cep, bairro, cidade, estado, pais, telefone, dhora_participacao, bloqueio, duplicado) "
"VALUES (%(id_usuario)i, %(id_usuario_wad)i, %(nome)s, %(cpf)s, %(email)s, %(endereco)s, %(numero)s, "
"%(complemento)s, %(cep)s, %(bairro)s, %(cidade)s, %(estado)s, %(pais)s, %(telefone)s, "
"%(dhora_participacao)s, %(bloqueio)s, %(duplicado)s)")

insert_sorteado = ("INSERT INTO rschemar.sorteados (id_usuario, id_conteudo, dia_hora) "
"VALUES (%(id_usuario)i, %(id_conteudo)i, %(dia_hora)s)")


#updates

update_conteudo = ("UPDATE rschemar.conteudo SET titulo=%(titulo)s, "
"descricao=%(descricao)s, vigencia_de=%(vigencia_de)s, vigencia_ate=%(vigencia_ate)s, resultado=%(resultado)s, "
"id_regulamento=%(id_regulamento)i, servico=%(servico)s, extra=%(extra)s, categoria=%(categoria)s, tipo=%(tipo)s, "
"publicado_em=%(publicado_em)s, num_sorteados=%(num_sorteados)s, "
"expira_em=%(expira_em)s, publicado=%(publicado)s "
"WHERE id_conteudo=%(id_conteudo)i")

update_status_promocao = ("UPDATE rschemar.conteudo SET finalizada=%(finalizada)s "
"WHERE id_conteudo=%(id_conteudo)i")

update_publicacao_promocao = ("UPDATE rschemar.conteudo SET publicado='true' "
"WHERE id_conteudo=%(id_conteudo)i")

update_regulamento = ("UPDATE rschemar.regulamento SET titulo=%(titulo)s, "
"regulamento=%(regulamento)s WHERE id_regulamento=%(id_regulamento)i")

update_blacklist_user = ("UPDATE rschemar.participante SET bloqueio='true' "
 "WHERE email=%(email)s")

update_blacklist_user_desbloq = ("UPDATE rschemar.participante SET bloqueio='false' "
"WHERE email=%(email)s")

update_status_user_promocao = ("UPDATE rschemar.participante_promocao SET status=%(status)s "
"WHERE id_conteudo=%(id_conteudo)i AND id_usuario=%(id_usuario)i")

#deletes
delete_conteudo = ("DELETE FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

delete_destaque = ("DELETE FROM rschemar.destaque WHERE id_conteudo=%(id_conteudo)i")

delete_regulamento = ("DELETE FROM rschemar.regulamento WHERE id_regulamento=%(id_regulamento)i")

delete_user_sorteado = ("DELETE FROM rschemar.sorteados WHERE id_usuario=%(id_usuario)i")

permissions = ("GRANT USAGE ON SCHEMA rschemar TO %(user)s;"
"GRANT SELECT ON rschemar.conteudo TO %(user)s;"
"GRANT SELECT ON rschemar.destaque TO %(user)s;"
"GRANT SELECT ON rschemar.regulamento TO %(user)s;"
"GRANT SELECT ON rschemar.participante TO %(user)s;"
"GRANT SELECT ON rschemar.participante_promocao TO %(user)s;"
"GRANT SELECT ON rschemar.sorteados TO %(user)s;"
)

permissions_admin = permissions

structure = """
  CREATE SCHEMA rschemar;

   CREATE TABLE rschemar.regulamento (
    id_regulamento SERIAL NOT NULL,
    titulo VARCHAR NULL,
    regulamento VARCHAR NOT NULL,
    PRIMARY KEY(id_regulamento)
   );

  CREATE TABLE rschemar.conteudo (
    id_conteudo SERIAL NOT NULL,
    id_idioma INTEGER DEFAULT 102,
    titulo VARCHAR NOT NULL,
    descricao VARCHAR NULL,
    vigencia_de TIMESTAMP NOT NULL,
    vigencia_ate TIMESTAMP NOT NULL,
    resultado TIMESTAMP NOT NULL,
    id_regulamento INT NOT NULL,
    categoria VARCHAR NULL,
    tipo VARCHAR NOT NULL,
    servico VARCHAR NULL,
    num_sorteados VARCHAR NULL,
    extra VARCHAR NULL,
    publicado BOOL NOT NULL DEFAULT 'False',
    expira_em TIMESTAMP NULL,
    publicado_em TIMESTAMP NOT NULL,
    atualizado_em TIMESTAMP NULL,
    exportado BOOLEAN DEFAULT 'False',
    finalizada BOOLEAN DEFAULT 'False',
    PRIMARY KEY(id_conteudo),
    FOREIGN KEY(id_regulamento)
       REFERENCES rschemar.regulamento(id_regulamento)
          ON UPDATE CASCADE
  );
  CREATE INDEX rschemar_conteudo_publicado_index ON rschemar.conteudo USING btree (publicado);
  CREATE INDEX rschemar_conteudo_publicado_em_index ON rschemar.conteudo USING btree (publicado_em);
  CREATE INDEX rschemar_conteudo_expira_em_index ON rschemar.conteudo USING btree (expira_em);

  CREATE TABLE rschemar.destaque (
    id_destaque SERIAL NOT NULL,
    id_conteudo INT NOT NULL,
    titulo VARCHAR NULL,
    descricao VARCHAR NULL,
    img VARCHAR NULL,
    peso INT NULL,
    PRIMARY KEY(id_destaque),
    FOREIGN KEY(id_conteudo)
      REFERENCES rschemar.conteudo(id_conteudo)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );
  CREATE INDEX rschemar_destaque_id_conteudo_index ON rschemar.destaque USING btree (id_conteudo);

  CREATE TABLE rschemar.participante (
    id_usuario SERIAL NOT NULL,
    id_usuario_wad BIGINT NOT NULL,
    nome VARCHAR NOT NULL,
    cpf VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    endereco VARCHAR NOT NULL,
    numero VARCHAR NOT NULL,
    complemento VARCHAR NOT NULL,
    cep VARCHAR NOT NULL,
    bairro VARCHAR NOT NULL,
    cidade VARCHAR NOT NULL,
    estado VARCHAR NOT NULL,
    pais VARCHAR NOT NULL,
    telefone VARCHAR NOT NULL,
    bloqueio BOOLEAN DEFAULT 'False',
    dhora_participacao TIMESTAMP NOT NULL,
    duplicado BOOLEAN DEFAULT 'False',
    PRIMARY KEY(id_usuario)
  );  
  CREATE INDEX rschemar_participante_id_usuario_index ON rschemar.participante USING btree (id_usuario);
  CREATE INDEX rschemar_email_index ON rschemar.participante USING btree(email);

  CREATE TABLE rschemar.participante_promocao (
    id_participante_promocao SERIAL NOT NULL,
    id_usuario INT NOT NULL,
    id_conteudo INT NOT NULL,
    status VARCHAR NOT NULL,
    frase VARCHAR NULL,
    FOREIGN KEY(id_usuario)
      REFERENCES rschemar.participante(id_usuario)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY(id_conteudo)
      REFERENCES rschemar.conteudo(id_conteudo)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );

 CREATE TABLE rschemar.sorteados (
    id_sort SERIAL NOT NULL,
    id_usuario INT NOT NULL,
    id_conteudo INT NOT NULL,
    dia_hora TIMESTAMP NOT NULL,
    FOREIGN KEY(id_usuario)
      REFERENCES rschemar.participante(id_usuario)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY(id_conteudo)
      REFERENCES rschemar.conteudo(id_conteudo)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );

"""
