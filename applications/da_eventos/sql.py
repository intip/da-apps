# -*- encoding: latin1 -*-
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
######################Evento##########################################


select_nextval_evento = ("SELECT NEXTVAL('rschemar.conteudo_id_conteudo_seq'::text) as id")

select_nextval_destaque = ("SELECT NEXTVAL('rschemar.destaque_id_destaque_seq'::text) as id")

select_nextval_categoria = ("SELECT NEXTVAL('rschemar.categoria_id_categoria_seq'::text) as id")

select_status_content = ("SELECT publicado FROM rschemar.conteudo "
"WHERE id_conteudo=%(id_conteudo)i")

select_categorias = ("SELECT id_categoria, nome_categoria FROM rschemar.categoria ORDER BY nome_categoria ASC")

select_titulo = ("SELECT titulo FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

select_eventos_publicado_order = ("SELECT * FROM rschemar.conteudo WHERE publicado = True AND publicado_em <= now() AND "
"(data_inicio >= %(data_inicio)s or data_fim >= %(data_inicio)s) ORDER BY titulo LIMIT %(limit)s")

select_eventos_publicado = ("SELECT * FROM rschemar.conteudo WHERE publicado = True AND publicado_em <= now() AND "
"(data_inicio >= %(data_inicio)s or data_fim >= %(data_inicio)s) LIMIT %(limit)s")

select_evento_publicado = ("SELECT * FROM rschemar.conteudo WHERE publicado_em <= now() AND id_conteudo =%(id_evento)i")

select_more_eventos = ("SELECT * FROM rschemar.conteudo WHERE publicado = True ORDER BY titulo LIMIT %(ate)i OFFSET %(de)i")

select_more_eventos_by_calendar = """
SELECT *, CASE WHEN data_inicio = %(date)s AND data_fim = %(date)s THEN 1 
WHEN data_inicio <= %(date)s AND data_fim = %(date)s THEN 2 
ELSE 3
END AS filter_date FROM rschemar.conteudo 
WHERE publicado = True AND publicado_em <= now() AND (data_inicio <= %(date)s 
and data_fim >= %(date)s) ORDER BY filter_date LIMIT %(ate)i OFFSET %(de)i"""

select_more_eventos_inicial = """
SELECT *, CASE WHEN data_inicio = %(date)s AND data_fim = %(date)s THEN 1 
WHEN data_inicio <= %(date)s AND data_fim = %(date)s THEN 2 
ELSE 3
END AS filter_date FROM rschemar.conteudo 
WHERE publicado = True AND publicado_em <= now() AND (data_inicio >= %(date)s 
or data_fim >= %(date)s) ORDER BY filter_date 
LIMIT %(ate)i OFFSET %(de)i"""

select_eventos_by_calendar_and_title = """
SELECT * , CASE WHEN E.data_inicio = %(date)s AND E.data_fim = %(date)s THEN 1 
WHEN E.data_inicio <= %(date)s AND E.data_fim = %(date)s THEN 2 
ELSE 3
END AS filter_date FROM rschemar.conteudo E INNER JOIN rschemar.destaque D 
ON (E.id_conteudo=D.id_conteudo) WHERE E.publicado = True AND 
E.publicado_em <= now() AND (E.data_inicio <= %(date)s AND E.data_fim >= %(date)s) 
AND (D.titulo ~* %(titulo)s OR E.local ~* %(titulo)s OR D.descricao ~* %(titulo)s) 
ORDER BY filter_date LIMIT %(ate)i OFFSET %(de)i """

select_eventos_by_calendar_title_count = """
SELECT count(*) FROM rschemar.conteudo E INNER JOIN rschemar.destaque D 
ON (E.id_conteudo=D.id_conteudo) WHERE E.publicado = True AND 
E.publicado_em <= now() AND (E.data_inicio <= %(date)s AND E.data_fim >= %(date)s) 
AND (D.titulo ~* %(titulo)s OR E.local ~* %(titulo)s OR D.descricao ~* %(titulo)s)
"""

select_more_eventos_inicial_count = ("SELECT count(*) FROM rschemar.conteudo WHERE publicado = True AND publicado_em <= now() "
"AND (data_inicio >= %(date)s or data_fim >= %(date)s)")

select_ultima_data = ("SELECT data_inicio FROM rschemar.conteudo WHERE publicado = True AND publicado_em <= now() ORDER BY data_inicio LIMIT 1 "
"OFFSET %(ultima_date)i")


select_more_eventos_by_calendar_count = ("SELECT count(*) FROM rschemar.conteudo WHERE publicado = True AND publicado_em <= now() "
"AND (data_inicio <= %(date)s and data_fim >= %(date)s)")

select_more_eventos_by_titulo="""SELECT * , CASE WHEN E.data_inicio = current_date AND E.data_fim = current_date THEN 1 
WHEN E.data_inicio <= current_date AND E.data_fim = current_date THEN 2
ELSE 3
END AS filter_date FROM rschemar.conteudo E INNER JOIN rschemar.destaque D ON (E.id_conteudo=D.id_conteudo)
 WHERE E.publicado = True AND publicado_em <= now() AND E.data_fim >= current_date  AND (D.titulo ~* %(titulo)s OR E.local ~* %(titulo)s 
OR D.descricao ~* %(titulo)s) ORDER BY filter_date LIMIT %(ate)i OFFSET %(de)i"""

select_more_eventos_by_titulo_count=("SELECT count(*) FROM rschemar.conteudo E INNER JOIN rschemar.destaque D ON (E.id_conteudo=D.id_conteudo)"
 "WHERE E.publicado = True AND publicado_em <= now() AND E.data_fim >= current_date AND (D.titulo ~* %(titulo)s OR E.local ~* %(titulo)s "
"OR D.descricao ~* %(titulo)s)")

select_status_evento = ("SELECT publicado FROM rschemar.conteudo WHERE "
"id_conteudo=%(id_conteudo)s")

select_count_eventos = ("SELECT count(*) FROM rschemar.conteudo WHERE publicado = True AND publicado_em <= now()")

select_nome_evento = ("SELECT titulo FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

select_categoria_evento = ("SELECT E.id_categoria, C.nome_categoria FROM rschemar.evento_categoria E "
                           "JOIN rschemar.categoria C ON (E.id_categoria=C.id_categoria) "
                           "WHERE id_conteudo=%(id_conteudo)i")

select_evento = ("SELECT id_conteudo, titulo, telefones, email, imagemint, "
"id_idioma, local, site, preco_entrada, consumacao_minima, hora_inicio, hora_fim, credito_imagem, data_inicio, data_fim, "
"usuario, email_user, to_char(atualizado_em, 'DD/MM/YYYY HH24:MI') as atualizado_em, "
"to_char(expira_em, 'DD/MM/YYYY HH24:MI') as expira_em, "
"to_char(publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em, publicado"
" FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

select_destaque = ("SELECT d.id_destaque, d.titulo, d.descricao, d.img, d.peso "
"FROM rschemar.destaque as d WHERE d.id_conteudo=%(id_conteudo)s")

select_temp_imagem = ("SELECT id_imagem, id_destaque, imagembin, tipoarq, nomearq FROM rschemar.temp_imagem WHERE id_destaque=%(id_destaque)i")

select_todos_eventos = ("SELECT id_conteudo, titulo, hora_inicio, hora_fim, telefones, email, data_inicio, data_fim,  "
"id_idioma, local, site, preco_entrada,consumacao_minima,credito_imagem, "
"to_char(expira_em, 'DD/MM/YYYY HH24:MI') as expira_em, "
"to_char(publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em, publicado"
" FROM rschemar.conteudo ")

select_ids_agendados = ("SELECT id_conteudo, publicado_em FROM rschemar.conteudo WHERE publicado = True AND publicado_em >= %(publicado_em)s")

# selects da busca da capa 

#1
select_eventos_by_categoria = """
SELECT * , CASE WHEN E.data_inicio = current_date AND E.data_fim = current_date THEN 1 
WHEN E.data_inicio <= current_date AND E.data_fim = current_date THEN 2
ELSE 3
END AS filter_date FROM rschemar.conteudo E INNER JOIN rschemar.evento_categoria EC
ON (E.id_conteudo=EC.id_conteudo) WHERE E.publicado=True AND 
E.publicado_em <= now() AND EC.id_categoria=%(categoria)i
AND E.data_fim >= current_date
ORDER BY filter_date LIMIT %(ate)i OFFSET %(de)i 
"""

select_eventos_by_categoria_count = """
SELECT count(*) FROM rschemar.conteudo E INNER JOIN rschemar.evento_categoria EC
ON (E.id_conteudo=EC.id_conteudo) WHERE E.publicado=True AND 
E.publicado_em <= now() AND EC.id_categoria=%(categoria)i
AND E.data_fim >= current_date
"""

#2
select_eventos_by_categoria_data1 = """
SELECT * FROM rschemar.conteudo E INNER JOIN rschemar.evento_categoria EC
ON (E.id_conteudo=EC.id_conteudo) WHERE E.publicado=True AND 
E.publicado_em <= now() AND EC.id_categoria=%(categoria)i 
AND E.data_inicio >= %(data1)s
ORDER BY E.data_inicio LIMIT %(ate)i OFFSET %(de)i 
"""

select_eventos_by_categoria_data1_count = """
SELECT count(*) FROM rschemar.conteudo E INNER JOIN rschemar.evento_categoria EC
ON (E.id_conteudo=EC.id_conteudo) WHERE E.publicado=True AND 
E.publicado_em <= now() AND EC.id_categoria=%(categoria)i 
AND E.data_inicio >= %(data1)s
"""

#3
select_eventos_by_categoria_data1_2 = """
SELECT * , CASE WHEN E.data_inicio = %(data1)s AND E.data_fim = %(data1)s THEN 1 
WHEN E.data_inicio >= %(data1)s AND E.data_fim = %(data2)s THEN 2
ELSE 3
END AS filter_date FROM rschemar.conteudo E INNER JOIN rschemar.evento_categoria EC
ON (E.id_conteudo=EC.id_conteudo) WHERE E.publicado=True AND 
E.publicado_em <= now() AND EC.id_categoria=%(categoria)i 
AND E.data_inicio >= %(data1)s AND E.data_fim <= %(data2)s
ORDER BY filter_date LIMIT %(ate)i OFFSET %(de)i 
"""

select_eventos_by_categoria_data1_2_count = """
SELECT count(*) FROM rschemar.conteudo E INNER JOIN rschemar.evento_categoria EC
ON (E.id_conteudo=EC.id_conteudo) WHERE E.publicado=True AND 
E.publicado_em <= now() AND EC.id_categoria=%(categoria)i 
AND E.data_inicio >= %(data1)s AND E.data_fim <= %(data2)s
"""

#4

select_eventos_by_categoria_data1_2_titulo = """
SELECT * , CASE WHEN E.data_inicio = %(data1)s AND E.data_fim = %(data1)s THEN 1 
WHEN E.data_inicio = %(data1)s AND E.data_fim >= %(data1)s THEN 2 
ELSE 3
END AS filter_date FROM rschemar.conteudo E INNER JOIN rschemar.evento_categoria EC
ON (E.id_conteudo=EC.id_conteudo) INNER JOIN rschemar.destaque D 
ON (E.id_conteudo=D.id_conteudo) WHERE E.publicado=True AND 
E.publicado_em <= now() AND EC.id_categoria=%(categoria)i 
AND E.data_inicio >= %(data1)s AND E.data_fim <= %(data2)s 
AND (D.titulo ~* %(titulo)s OR E.local ~* %(titulo)s)
ORDER BY filter_date LIMIT %(ate)i OFFSET %(de)i 
"""

select_eventos_by_categoria_data1_2_titulo_count = """
SELECT count(*) FROM rschemar.conteudo E INNER JOIN rschemar.evento_categoria EC
ON (E.id_conteudo=EC.id_conteudo) INNER JOIN rschemar.destaque D 
ON (E.id_conteudo=D.id_conteudo) WHERE E.publicado=True AND 
E.publicado_em <= now() AND EC.id_categoria=%(categoria)i 
AND E.data_inicio >= %(data1)s AND E.data_fim <= %(data2)s 
AND (D.titulo ~* %(titulo)s OR E.local ~* %(titulo)s)
"""

#5

select_eventos_by_categoria_data2_titulo = """
SELECT * , CASE WHEN E.data_inicio = current_date AND E.data_fim = current_date THEN 1 
WHEN E.data_inicio <= current_date AND E.data_fim <= %(data2)s THEN 2 
ELSE 3
END AS filter_date FROM rschemar.conteudo E INNER JOIN rschemar.evento_categoria EC
ON (E.id_conteudo=EC.id_conteudo) INNER JOIN rschemar.destaque D 
ON (E.id_conteudo=D.id_conteudo) WHERE E.publicado=True AND 
E.publicado_em <= now() AND EC.id_categoria=%(categoria)i 
AND E.data_fim <= %(data2)s 
AND (D.titulo ~* %(titulo)s OR E.local ~* %(titulo)s)
ORDER BY filter_date LIMIT %(ate)i OFFSET %(de)i 
"""

select_eventos_by_categoria_data2_titulo_count = """
SELECT count(*) FROM rschemar.conteudo E INNER JOIN rschemar.evento_categoria EC
ON (E.id_conteudo=EC.id_conteudo) INNER JOIN rschemar.destaque D 
ON (E.id_conteudo=D.id_conteudo) WHERE E.publicado=True AND 
E.publicado_em <= now() AND EC.id_categoria=%(categoria)i 
AND E.data_fim <= %(data2)s 
AND (D.titulo ~* %(titulo)s OR E.local ~* %(titulo)s)
"""

#5.1

select_eventos_by_categoria_data1_titulo = """
SELECT * FROM rschemar.conteudo E INNER JOIN rschemar.evento_categoria EC 
ON (E.id_conteudo=EC.id_conteudo) INNER JOIN rschemar.destaque D 
ON (E.id_conteudo=D.id_conteudo) WHERE E.publicado=True AND 
E.publicado_em <= now() AND EC.id_categoria=%(categoria)i 
AND E.data_inicio >= %(data1)s 
AND (D.titulo ~* %(titulo)s OR E.local ~* %(titulo)s) 
ORDER BY E.data_inicio LIMIT %(ate)i OFFSET %(de)i 
"""

select_eventos_by_categoria_data1_titulo_count = """
SELECT count(*) FROM rschemar.conteudo E INNER JOIN rschemar.evento_categoria EC 
ON (E.id_conteudo=EC.id_conteudo) INNER JOIN rschemar.destaque D 
ON (E.id_conteudo=D.id_conteudo) WHERE E.publicado=True AND 
E.publicado_em <= now() AND EC.id_categoria=%(categoria)i 
AND E.data_inicio >= %(data1)s 
AND (D.titulo ~* %(titulo)s OR E.local ~* %(titulo)s)
"""

#6

select_eventos_by_categoria_data2 = """
SELECT * , CASE WHEN E.data_inicio = current_date AND E.data_fim = current_date THEN 1 
WHEN E.data_inicio <= current_date AND E.data_fim <= %(data2)s THEN 2 
ELSE 3
END AS filter_date FROM rschemar.conteudo E INNER JOIN rschemar.evento_categoria EC
ON (E.id_conteudo=EC.id_conteudo) WHERE E.publicado=True AND 
E.publicado_em <= now() AND EC.id_categoria=%(categoria)i 
AND E.data_fim <= %(data2)s 
ORDER BY filter_date LIMIT %(ate)i OFFSET %(de)i 
"""

select_eventos_by_categoria_data2_count = """
SELECT count(*) FROM rschemar.conteudo E INNER JOIN rschemar.evento_categoria EC
ON (E.id_conteudo=EC.id_conteudo) WHERE E.publicado=True AND 
E.publicado_em <= now() AND EC.id_categoria=%(categoria)i 
AND E.data_fim <= %(data2)s 
"""

#7

select_eventos_by_categoria_titulo = """
SELECT * , CASE WHEN E.data_inicio = current_date AND E.data_fim = current_date THEN 1 
WHEN E.data_inicio <= current_date AND E.data_fim = current_date THEN 2
ELSE 3
END AS filter_date FROM rschemar.conteudo E INNER JOIN rschemar.evento_categoria EC
ON (E.id_conteudo=EC.id_conteudo) INNER JOIN rschemar.destaque D 
ON (E.id_conteudo=D.id_conteudo) WHERE E.publicado=True AND 
E.publicado_em <= now() AND EC.id_categoria=%(categoria)i 
AND E.data_fim >= current_date
AND (D.titulo ~* %(titulo)s OR E.local ~* %(titulo)s)
ORDER BY filter_date LIMIT %(ate)i OFFSET %(de)i 
"""

select_eventos_by_categoria_titulo_count = """
SELECT count(*) FROM rschemar.conteudo E INNER JOIN rschemar.evento_categoria EC
ON (E.id_conteudo=EC.id_conteudo) INNER JOIN rschemar.destaque D 
ON (E.id_conteudo=D.id_conteudo) WHERE E.publicado=True AND 
E.publicado_em <= now() AND EC.id_categoria=%(categoria)i 
AND E.data_fim >= current_date
AND (D.titulo ~* %(titulo)s OR E.local ~* %(titulo)s)
"""

#8

select_eventos_by_data2 = """
SELECT * , CASE WHEN E.data_inicio = current_date) AND E.data_fim = current_date THEN 1 
WHEN E.data_inicio <= current_date AND E.data_fim <= %(data2)s THEN 2 
ELSE 3
END AS filter_date FROM rschemar.conteudo E WHERE E.publicado=True AND 
E.publicado_em <= now() AND E.data_fim <= %(data2)s 
ORDER BY E.data_inicio LIMIT %(ate)i OFFSET %(de)i 
"""

select_eventos_by_data2_count = """
SELECT count(*) FROM rschemar.conteudo E WHERE E.publicado=True AND 
E.publicado_em <= now() AND E.data_fim <= %(data2)s 
"""

#9

select_eventos_by_data1 = """
SELECT * FROM rschemar.conteudo E WHERE E.publicado=True AND 
E.publicado_em <= now() AND E.data_inicio >= %(data1)s 
ORDER BY E.data_inicio LIMIT %(ate)i OFFSET %(de)i 
"""

select_eventos_by_data1_count = """
SELECT count(*) FROM rschemar.conteudo E WHERE E.publicado=True AND 
E.publicado_em <= now() AND E.data_inicio >= %(data1)s 
"""

#10

select_eventos_by_data1_2 = """
SELECT * , CASE WHEN E.data_inicio = %(data1)s AND E.data_fim = %(data1)s THEN 1 
WHEN E.data_inicio = %(data1)s AND E.data_fim >= %(data1)s THEN 2 
ELSE 3
END AS filter_date FROM rschemar.conteudo E WHERE E.publicado=True AND 
E.publicado_em <= now() AND E.data_inicio >= %(data1)s 
AND E.data_fim <= %(data2)s 
ORDER BY filter_date LIMIT %(ate)i OFFSET %(de)i 
"""

select_eventos_by_data1_2_count = """
SELECT count(*) FROM rschemar.conteudo E WHERE E.publicado=True AND 
E.publicado_em <= now() AND E.data_inicio >= %(data1)s 
AND E.data_fim <= %(data2)s 
"""

#11

select_eventos_by_data1_2_titulo = """
SELECT * , CASE WHEN E.data_inicio = %(data1)s AND E.data_fim = %(data1)s THEN 1 
WHEN E.data_inicio = %(data1)s AND E.data_fim >= %(data1)s THEN 2 
ELSE 3
END AS filter_date FROM rschemar.conteudo E INNER JOIN rschemar.destaque D 
ON (E.id_conteudo=D.id_conteudo) WHERE E.publicado=True AND 
E.publicado_em <= now() AND E.data_inicio >= %(data1)s 
AND E.data_fim <= %(data2)s 
AND (D.titulo ~* %(titulo)s OR E.local ~* %(titulo)s)
ORDER BY filter_date LIMIT %(ate)i OFFSET %(de)i 
"""

select_eventos_by_data1_2_titulo_count = """
SELECT count(*) FROM rschemar.conteudo E INNER JOIN rschemar.destaque D 
ON (E.id_conteudo=D.id_conteudo) WHERE E.publicado=True AND 
E.publicado_em <= now() AND E.data_inicio >= %(data1)s 
AND E.data_fim <= %(data2)s 
AND (D.titulo ~* %(titulo)s OR E.local ~* %(titulo)s)
"""

#12

select_eventos_by_data2_titulo = """
SELECT * , CASE WHEN E.data_inicio = current_date AND E.data_fim = current_date THEN 1 
WHEN E.data_inicio <= current_date AND E.data_fim <= %(data2)s THEN 2 
ELSE 3
END AS filter_date FROM rschemar.conteudo E INNER JOIN rschemar.destaque D 
ON (E.id_conteudo=D.id_conteudo) WHERE E.publicado=True AND 
E.publicado_em <= now() AND E.data_fim <= %(data2)s 
AND (D.titulo ~* %(titulo)s OR E.local ~* %(titulo)s)
ORDER BY filter_date LIMIT %(ate)i OFFSET %(de)i 
"""

select_eventos_by_data2_titulo_count = """
SELECT count(*) FROM rschemar.conteudo E INNER JOIN rschemar.destaque D 
ON (E.id_conteudo=D.id_conteudo) WHERE E.publicado=True AND 
E.publicado_em <= now() AND E.data_fim <= %(data2)s 
AND (D.titulo ~* %(titulo)s OR E.local ~* %(titulo)s)
"""

#13

select_eventos_by_data1_titulo = """
SELECT * FROM rschemar.conteudo E INNER JOIN rschemar.destaque D 
ON (E.id_conteudo=D.id_conteudo) WHERE E.publicado=True AND 
E.publicado_em <= now() AND E.data_inicio >= %(data1)s 
AND (D.titulo ~* %(titulo)s OR E.local ~* %(titulo)s)
ORDER BY E.data_inicio LIMIT %(ate)i OFFSET %(de)i 
"""

select_eventos_by_data1_titulo_count = """
SELECT count(*) FROM rschemar.conteudo E INNER JOIN rschemar.destaque D 
ON (E.id_conteudo=D.id_conteudo) WHERE E.publicado=True AND 
E.publicado_em <= now() AND E.data_inicio >= %(data1)s 
AND (D.titulo ~* %(titulo)s OR E.local ~* %(titulo)s)
"""

# fim selects da busca da capa 


insert_evento_ext = ("INSERT INTO rschemar.conteudo (id_conteudo,  titulo,"
"publicado_em, expira_em, publicado, local, site, telefones, email, "
"preco_entrada, consumacao_minima, credito_imagem, hora_inicio, hora_fim, "
"data_inicio,data_fim, usuario, email_user) VALUES (%(id_conteudo)i, %(titulo)s, "
"%(publicado_em)s, %(expira_em)s, %(publicado)s, %(local)s, %(site)s, %(telefones)s, "
"%(email)s, %(preco_entrada)s, %(consumacao_minima)s, %(credito_imagem)s, %(hora_inicio)s, "
"%(hora_fim)s, %(data_inicio)s, %(data_fim)s, %(usuario)s, %(email_user)s)")

insert_evento= ("INSERT INTO rschemar.conteudo (id_conteudo,  titulo,"
"publicado_em, expira_em, publicado, local, site, telefones, email, "
"preco_entrada, consumacao_minima, imagemint, credito_imagem, hora_inicio, hora_fim, "
"data_inicio,data_fim, usuario, email_user) VALUES (%(id_conteudo)i, %(titulo)s, "
"%(publicado_em)s, %(expira_em)s, %(publicado)s, %(local)s, %(site)s, %(telefones)s, "
"%(email)s, %(preco_entrada)s, %(consumacao_minima)s, %(imagemint)s, %(credito_imagem)s, %(hora_inicio)s, "
"%(hora_fim)s, %(data_inicio)s, %(data_fim)s, %(usuario)s, %(email_user)s)")

insert_destaque = ("INSERT INTO rschemar.destaque (id_destaque, id_conteudo, titulo, "
"descricao, img, peso) VALUES (%(id_destaque)i, %(id_conteudo)i, %(titulo)s, "
"%(descricao)s, %(img)s, %(peso)i)")

insert_tempimg = ("INSERT INTO rschemar.temp_imagem (id_destaque, imagembin, tipoarq, nomearq) VALUES (%(id_destaque)i, '%(imagembin)s', "
"%(tipoarq)s, %(nomearq)s)")

insert_categoria = ("INSERT INTO rschemar.categoria (id_categoria,nome_categoria) VALUES (%(id_categoria)i, %(nome_categoria)s)")

insert_categoria_evento = ("INSERT INTO rschemar.evento_categoria VALUES (%(id_categoria)i, %(id_conteudo)i)")

update_evento = ("UPDATE rschemar.conteudo SET titulo=%(titulo)s, "
"imagemint=%(imagemint)s, publicado_em=%(publicado_em)s, telefones=%(telefones)s, email = %(email)s, "
"expira_em=%(expira_em)s, publicado=%(publicado)s, data_inicio=%(data_inicio)s, data_fim=%(data_fim)s, "
"hora_inicio=%(hora_inicio)s, hora_fim=%(hora_fim)s, local=%(local)s, site =%(site)s, "
"usuario=%(usuario)s, email_user=%(email_user)s, "
"preco_entrada =%(preco_entrada)s, consumacao_minima =%(consumacao_minima)s, credito_imagem =%(credito_imagem)s"
"WHERE id_conteudo=%(id_conteudo)i")

update_categoria = ("UPDATE rschemar.categoria SET nome_categoria=%(nome_categoria)s WHERE id_categoria=%(id_categoria)i")

update_destaque = ("UPDATE rschemar.destaque SET img=%(img)s WHERE id_destaque=%(id_destaque)i")

update_imagem = ("UPDATE rschemar.conteudo SET imagemint=%(imagemint)s WHERE id_conteudo=%(id_conteudo)i")

delete_evento = ("DELETE FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

delete_destaque = ("DELETE FROM rschemar.destaque WHERE id_conteudo=%(id_conteudo)i")

delete_tempimg = ("DELETE FROM rschemar.temp_imagem WHERE id_destaque=%(id_destaque)i")

delete_categoria_evento = ("DELETE FROM rschemar.evento_categoria WHERE id_conteudo=%(id_conteudo)i")

delete_categoria = ("DELETE FROM rschemar.categoria WHERE id_categoria=%(id_categoria)i")
#permissão
permissions = ("GRANT USAGE ON SCHEMA rschemar TO %(user)s;"
"GRANT SELECT ON rschemar.conteudo TO %(user)s;"
"GRANT SELECT ON rschemar.destaque TO %(user)s;"
"GRANT SELECT ON rschemar.categoria TO %(user)s;"
"GRANT SELECT ON rschemar.evento_categoria TO %(user)s"
)

permissions_admin = permissions

structure = """
  CREATE SCHEMA rschemar;

    CREATE TABLE rschemar.categoria(
      id_categoria SERIAL NOT NULL,
      nome_categoria VARCHAR NOT NULL,
      PRIMARY key(id_categoria)
  );

  CREATE TABLE rschemar.conteudo (
    id_conteudo SERIAL NOT NULL,
    id_idioma INTEGER DEFAULT 102,
    titulo VARCHAR NOT NULL,
    local VARCHAR NOT NULL,
    site VARCHAR,
    data_inicio TIMESTAMP,
    data_fim TIMESTAMP,
    telefones VARCHAR,
    email VARCHAR,
    imagemint VARCHAR,
    preco_entrada VARCHAR,
    consumacao_minima VARCHAR,
    hora_inicio VARCHAR,
    hora_fim VARCHAR,
    credito_imagem VARCHAR,
    usuario VARCHAR,
    email_user VARCHAR,
    publicado BOOL NOT NULL DEFAULT 'False',
    expira_em TIMESTAMP NULL,
    publicado_em TIMESTAMP NOT NULL,
    atualizado_em TIMESTAMP NULL,
    exportado BOOLEAN DEFAULT 'False',
    PRIMARY KEY(id_conteudo) 
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


  CREATE TABLE rschemar.temp_imagem(
      id_imagem SERIAL NOT NULL,
      id_destaque INT NOT NULL,
      imagembin TEXT NULL,
      tipoarq VARCHAR NULL,
      nomearq VARCHAR NULL,
      PRIMARY KEY(id_imagem),
      FOREIGN KEY(id_destaque)
          REFERENCES rschemar.destaque(id_destaque)
   );
   
  CREATE TABLE rschemar.evento_categoria(
      id_categoria INT NOT NULL,
      id_conteudo INT NOT NULL,
      FOREIGN KEY(id_conteudo)
          REFERENCES rschemar.conteudo(id_conteudo)
              ON DELETE CASCADE,
      FOREIGN KEY(id_categoria)
          REFERENCES rschemar.categoria(id_categoria)
              ON DELETE CASCADE
   );
   
  INSERT INTO rschemar.categoria (nome_categoria) VALUES ('Artes Visuais');
  INSERT INTO rschemar.categoria (nome_categoria) VALUES ('Cinema');
  INSERT INTO rschemar.categoria (nome_categoria) VALUES ('Circo');
  INSERT INTO rschemar.categoria (nome_categoria) VALUES ('Dan&ccedil;a');
  INSERT INTO rschemar.categoria (nome_categoria) VALUES ('Exposi&ccedil;&atilde;o');
  INSERT INTO rschemar.categoria (nome_categoria) VALUES ('Festa');
  INSERT INTO rschemar.categoria (nome_categoria) VALUES ('Gastronomia');
  INSERT INTO rschemar.categoria (nome_categoria) VALUES ('Literatura');
  INSERT INTO rschemar.categoria (nome_categoria) VALUES ('Mostra de Cinema');
  INSERT INTO rschemar.categoria (nome_categoria) VALUES ('Novas M&iacute;dias');
  INSERT INTO rschemar.categoria (nome_categoria) VALUES ('Show');
  INSERT INTO rschemar.categoria (nome_categoria) VALUES ('Teatro');
  INSERT INTO rschemar.categoria (nome_categoria) VALUES ('Teatro Infantil');
"""
