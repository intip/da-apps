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
select_status_content      = ("SELECT publicado FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

select_conteudo            = ("SELECT C.id_conteudo, C.titulo, C.publicado, C.publicado_em, "
                              "C.expira_em, D.titulo as titulo_destaque, D.descricao as descricao_destaque, "
                              "D.img as imagem_destaque "
                              "FROM rschemar.conteudo C "
                              "LEFT JOIN rschemar.destaque D ON(C.id_conteudo=D.id_conteudo) "
                              "ORDER BY C.id_conteudo")

select_tipo_noticia        = ("SELECT id_tipo_noticia, titulo FROM rschemar.tipo_noticia ORDER BY titulo")

select_autor_unico         = ("SELECT nome, email, grupo FROM rschemar.autor WHERE id_autor=%(id_autor)s")

select_autor_unico_titulo  = ("SELECT id_autor, nome, email, grupo FROM rschemar.autor WHERE nome=%(nome)s")

select_autor               = ("SELECT id_autor, nome, email, grupo FROM rschemar.autor ORDER BY nome")

select_nextval_noticia     = ("SELECT NEXTVAL('rschemar.conteudo_id_conteudo_seq'::text) as id")

select_nextval_autor       = ("SELECT NEXTVAL('rschemar.autor_id_autor_seq'::text) as id")

select_titulo              = ("SELECT titulo FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

select_noticia             = ("SELECT N.id_conteudo, N.titulo_categoria, N.titulo, N.ordem, N.pdf, N.is_capa, N.titulo_capa, N.titulo_galeria, "
                              "N.descricao, N.id_tipo_noticia, N.editor, N.corpo, N.video, N.audio, N.galeria, "
                              "to_char(N.expira_em, 'DD/MM/YYYY HH24:MI') as expira_em, "
                              "to_char(N.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em, N.publicado, "
                              "to_char(N.data_edicao, 'DD/MM/YYYY') as data_edicao, to_char(N.atualizado_em, 'DD/MM/YYYY') as atualizado_em, "
                              "D.id_destaque, D.titulo as titulo_destaque, D.descricao as descricao_destaque, "
                              "D.img, D.img as imagem_destaque, D.peso as peso_destaque, T.titulo as tipo_noticia, "
                              "N.autor "
                              "FROM rschemar.conteudo N "
                              "LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo) "
                              "LEFT JOIN rschemar.tipo_noticia T ON(N.id_tipo_noticia=T.id_tipo_noticia) "
                              "WHERE N.id_conteudo=%(id_conteudo)i")

select_noticia_dados       = ("SELECT N.id_conteudo, N.titulo_categoria, N.titulo, N.titulo_capa, N.is_capa, N.ordem, N.pdf, "
                              "N.descricao, N.id_tipo_noticia, N.editor, N.corpo, N.video, N.audio, N.galeria, N.titulo_galeria, "
                              "to_char(N.expira_em, 'YYYY-MM-DD HH24:MI') as expira_em, "
                              "to_char(N.publicado_em, 'YYYY-MM-DD HH24:MI') as publicado_em, N.publicado, "
                              "to_char(N.data_edicao, 'YYYY-MM-DD') as data_edicao, to_char(N.atualizado_em, 'YYYY-MM-DD') as atualizado_em, "
                              "D.id_destaque, D.titulo as titulo_destaque, D.descricao as descricao_destaque, "
                              "D.img, D.img as imagem_destaque, D.peso as peso_destaque, T.titulo as tipo_noticia, "
                              "N.autor "
                              "FROM rschemar.conteudo N "
                              "LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo) "
                              "LEFT JOIN rschemar.tipo_noticia T ON(N.id_tipo_noticia=T.id_tipo_noticia) "
                              "WHERE N.id_conteudo=%(id_conteudo)i")

select_noticia_destaque    = ("SELECT titulo, descricao, img FROM rschemar.destaque WHERE id_conteudo=%(id_conteudo)i")

select_noticia_fotos       = ("SELECT id_foto, arquivo, arquivo_grande, alinhamento, credito, legenda, link "
                              "FROM rschemar.foto WHERE id_conteudo=%(id_conteudo)d ORDER BY id_foto ASC")

select_videos              = ("SELECT id_video, embed FROM rschemar.video WHERE id_conteudo=%(id_conteudo)i "
                              "ORDER BY id_video ASC")

select_fotos_ipad = """
    SELECT * FROM rschemar.fotos_ipad WHERE id_conteudo=%(id_conteudo)s
"""

select_videos_ipad = """
    SELECT * FROM rschemar.videos_ipad WHERE id_conteudo=%(id_conteudo)s
"""

select_noticia_autores     = ("SELECT NA.id_autor, NA.id_autor, NA.id_conteudo, A.nome, A.email "
                              "FROM rschemar.conteudo_autor NA "
                              "INNER JOIN rschemar.autor A ON (NA.id_autor=A.id_autor) "
                              "WHERE NA.id_conteudo=%(id_conteudo)i ORDER BY NA.ordem ASC")

select_noticia_publicada   = ("SELECT N.id_conteudo, N.titulo_categoria, N.titulo, N.descricao, "
                              "N.id_tipo_noticia, N.editor, N.corpo, "
                              "N.video, N.audio, N.galeria, to_char(N.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em, N.publicado, "
                              "to_char(N.atualizado_em, 'DD/MM/YYYY HH24:MI') as atualizado_em, "
                              "D.id_destaque, D.titulo as titulo_destaque, D.descricao as descricao_destaque, D.img as imagem_destaque, "
                              "T.titulo as titulo_tree, CC.breadcrump, N.autor "
                              "FROM rschemar.conteudo N "
                              "INNER JOIN envsite.conteudo CC ON(N.id_conteudo=CC.id_conteudo) "
                              "INNER JOIN envsite.treeapp T ON(CC.id_treeapp=T.id_treeapp) "
                              "LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo) "
                              "WHERE N.id_conteudo=%(id_conteudo)i AND "
                              "CC.id_aplicativo=(SELECT id_aplicativo FROM envsite.aplicativo WHERE schema='rschemar')")

select_noticia_publicada_ultima = ("SELECT N.id_conteudo, N.titulo_categoria, N.titulo, N.descricao, N.id_tipo_noticia, N.editor, N.corpo, "
                                   "N.video, N.audio, N.galeria, to_char(N.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em, N.publicado, "
                                   "to_char(N.atualizado_em, 'DD/MM/YYYY HH24:MI') as atualizado_em, "
                                   "D.id_destaque, D.titulo as titulo_destaque, D.descricao as descricao_destaque, D.img as imagem_destaque, "
                                   "T.titulo as titulo_tree, CC.breadcrump, N.autor "
                                   "FROM rschemar.conteudo N "
                                   "INNER JOIN envsite.conteudo CC ON(N.id_conteudo=CC.id_conteudo) "
                                   "INNER JOIN envsite.treeapp T ON(CC.id_treeapp=T.id_treeapp) "                                   
                                   "LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo) "
                                   "WHERE (N.expira_em > now() OR expira_em IS NULL) "
                                   "AND N.publicado_em <= now() AND N.publicado='True' AND "
                                   "CC.id_aplicativo=(SELECT id_aplicativo FROM envsite.aplicativo WHERE schema='rschemar')"
                                   "ORDER BY N.publicado_em DESC LIMIT 1 ")

select_autor_noticia       = ("SELECT A.id_autor, A.nome, A.email, A.grupo FROM rschemar.conteudo_autor NA "
                              "INNER JOIN rschemar.autor A ON(NA.id_autor=A.id_autor) "
                              "WHERE NA.id_conteudo=%(id_conteudo)i ORDER BY NA.ordem ")

select_svg                 = ("SELECT audio, video, galeria FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

select_svgs                = ("SELECT id_conteudo, audio, video, galeria FROM "
                              "rschemar.conteudo WHERE id_conteudo IN (%(id_conteudos)s)")

select_dublin_core         = ("SELECT titulo, descricao, corpo, "
                              "to_char(atualizado_em, 'YYYY-MM-DD HH24:MI:SS') as atualizado_em, "
                              "to_char(publicado_em, 'YYYY-MM-DD HH24:MI:SS') as publicado_em "
                              "FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

select_treeapp             = ("SELECT C.id_treeapp, T.hash FROM envsite.conteudo C "
                              "INNER JOIN envsite.treeapp T ON(C.id_treeapp=T.id_treeapp) "
                              "WHERE C.id_aplicativo=(SELECT id_aplicativo FROM envsite.aplicativo WHERE schema=%(schema)s) "
                              "GROUP BY C.id_treeapp, T.hash")

select_data_edicao         = ("SELECT C.data_edicao, C.id_conteudo, C.titulo, C.publicado_em, C.descricao, CC.breadcrump as breadcrumb "
                              "FROM rschemar.conteudo C "
                              "INNER JOIN envsite.conteudo CC ON(C.id_conteudo=CC.id_conteudo) "
                              "INNER JOIN envsite.treeapp T ON(CC.id_treeapp=T.id_treeapp) "
                              "WHERE CC.id_aplicativo=(SELECT id_aplicativo FROM envsite.aplicativo WHERE schema=%(schema)s) "
                              "AND C.data_edicao=%(data_edicao)s AND C.publicado AND C.publicado_em <= now() AND "
                              "(C.expira_em > now() OR C.expira_em IS NULL) AND T.hash=%(hash)s")

select_ultima_data_edicao  = ("SELECT C.data_edicao, C.id_conteudo, C.titulo, C.publicado_em "
                              "FROM rschemar.conteudo C "
                              "INNER JOIN envsite.conteudo CC ON(C.id_conteudo=CC.id_conteudo) "
                              "INNER JOIN envsite.treeapp T ON(CC.id_treeapp=T.id_treeapp) "
                              "WHERE CC.id_aplicativo=(SELECT id_aplicativo FROM envsite.aplicativo WHERE schema=%(schema)s) "
                              "AND C.data_edicao<%(data_edicao)s AND C.publicado AND C.publicado_em <= now() AND "
                              "(C.expira_em > now() OR C.expira_em IS NULL) AND T.hash=%(hash)s")

select_ultimas_app         = ("SELECT C.id_conteudo, C.titulo, to_char(C.publicado_em, 'HH24:MI') as hora, "
                              "to_char(C.publicado_em, 'DD/MM/YYYY') as data, C.publicado_em "
                              "FROM rschemar.conteudo C "
                              "WHERE C.publicado AND C.publicado_em <= now() AND "
                              "(C.expira_em > now() OR C.expira_em IS NULL) "
                              "ORDER BY C.publicado_em DESC "
                              "LIMIT %(limit)i OFFSET %(offset)i")

select_ultimas_app_qtde     = ("SELECT count(1) as qtde FROM rschemar.conteudo C "
                              "WHERE C.publicado AND C.publicado_em <= now() AND "
                              "(C.expira_em > now() OR C.expira_em IS NULL) ")

select_ultimas_app_acesso24h = ("SELECT C.id_conteudo, C.titulo, to_char(C.publicado_em, 'HH24:MI') as hora, "
                                "to_char(C.publicado_em, 'DD/MM/YYYY') as data "
                                "FROM rschemar.conteudo C "
                                "INNER JOIN envsite.conteudo CC ON(C.id_conteudo=CC.id_conteudo) "
                                "WHERE C.publicado AND C.publicado_em <= now() AND "
                                "(C.expira_em > now() OR C.expira_em IS NULL) AND "
                                "C.publicado_em >= (now() - interval '48 hours') AND "
                                "CC.id_aplicativo=(SELECT id_aplicativo FROM envsite.aplicativo WHERE schema='rschemar') AND "
                                "CC.acesso > 0 "
                                "ORDER BY C.publicado_em DESC "
                                "LIMIT %(limit)i OFFSET %(offset)i")

select_ultima_data_edicao  = ("SELECT C.data_edicao, C.id_conteudo, C.titulo, C.publicado_em "
                              "FROM rschemar.conteudo C "
                              "INNER JOIN envsite.conteudo CC ON(C.id_conteudo=CC.id_conteudo) "
                              "INNER JOIN envsite.treeapp T ON(CC.id_treeapp=T.id_treeapp) "
                              "WHERE CC.id_aplicativo=(SELECT id_aplicativo FROM envsite.aplicativo WHERE schema=%(schema)s) "
                              "AND C.data_edicao<%(data_edicao)s AND C.publicado AND C.publicado_em <= now() AND "
                              "(C.expira_em > now() OR C.expira_em IS NULL) AND T.hash=%(hash)s")

select_ultimas             = ("SELECT N.id_conteudo, N.titulo_categoria, N.titulo, N.descricao, "
                              "N.video, N.audio, N.galeria, to_char(N.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em, N.publicado, "
                              "to_char(N.atualizado_em, 'DD/MM/YYYY HH24:MI') as atualizado_em, "
                              "D.id_destaque, D.titulo as titulo_destaque, D.descricao as descricao_destaque, D.img as imagem_destaque "
                              "FROM rschemar.conteudo N "
                              "LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo) "
                              "WHERE (N.expira_em > now() OR expira_em IS NULL) "
                              "AND N.publicado_em <= now() AND N.publicado='True' "
                              "ORDER BY N.publicado_em DESC LIMIT %(limit)i OFFSET %(offset)i ")

select_ultimas_qtde        = ("SELECT count(1) as qtde FROM rschemar.conteudo N "
                              "LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo) "
                              "WHERE (N.expira_em > now() OR expira_em IS NULL) "
                              "AND N.publicado_em <= now() AND N.publicado='True' ")

select_content_retranca    = ("SELECT id_conteudo, publicado_em FROM rschemar.conteudo WHERE retranca=%(retranca)s")

select_content_date        = ("SELECT id_conteudo FROM rschemar.conteudo WHERE "
                              "publicado_em >= %(data1)s AND publicado_em <= %(data2)s "
                              "AND pdf IS NOT NULL ORDER BY pdf, publicado_em")

select_content_date_capa   = ("SELECT id_conteudo FROM rschemar.conteudo WHERE "
                              "publicado_em >= %(data1)s AND publicado_em <= %(data2)s "
                              "AND pdf IS NOT NULL AND is_capa ORDER BY pdf, publicado_em")

select_datetime_hash       = ("SELECT to_char(N.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em FROM rschemar.conteudo N "
                              "INNER JOIN envsite.conteudo C ON(N.id_conteudo=C.id_conteudo) "
                              "WHERE C.id_treeapp=%(id_treeapp)i AND C.id_aplicativo=%(id_aplicativo)i "
                              "ORDER BY N.publicado_em DESC LIMIT 1")


select_last_date_by_hash3 = """
EXPLAIN SELECT * FROM envsite.conteudo WHERE id_conteudo IN (
    SELECT id_conteudo FROM envsite.conteudo 
        WHERE id_treeapp = 
            (SELECT id_treeapp FROM envsite.treeapp WHERE hash = %(hash)s) )
"""

select_last_date_by_hash = """
SELECT t4.titulo_categoria, t4.titulo, t4.ordem, t4.id_conteudo FROM envsite.treeapp t1 
CROSS JOIN envsite.aplicativo t2
INNER JOIN envsite.conteudo t3 ON 
    (t1.id_treeapp=t3.id_treeapp AND t2.id_aplicativo=t3.id_aplicativo) 
INNER JOIN rschemar.conteudo t4 ON (t4.id_conteudo=t3.id_conteudo) 
    WHERE t1.hash = %(hash)s 
    AND t2.schema='rschemar' 
    AND (t4.expira_em > now() OR t4.expira_em IS NULL) 
    AND t4.publicado_em <= now() AND t4.publicado='True'
    AND t4.id_tipo_noticia <> 7
    AND date_trunc('day', t4.publicado_em) = 
(    
SELECT date_trunc('day' , MAX(t4.publicado_em)) FROM envsite.treeapp t1 
CROSS JOIN envsite.aplicativo t2
INNER JOIN envsite.conteudo t3 ON 
    (t1.id_treeapp=t3.id_treeapp AND t2.id_aplicativo=t3.id_aplicativo) 
INNER JOIN rschemar.conteudo t4 ON (t4.id_conteudo=t3.id_conteudo) 
    WHERE t1.hash = %(hash)s 
    AND t2.schema='rschemar' 
    AND (t4.expira_em > now() OR t4.expira_em IS NULL) 
    AND t4.publicado_em <= now() AND t4.publicado='True'
    AND t4.id_tipo_noticia <> 7
)
ORDER BY t4.ordem
"""

select_latest = """
SELECT t4.titulo, t4.ordem, t4.id_conteudo FROM envsite.treeapp t1 
CROSS JOIN envsite.aplicativo t2
INNER JOIN envsite.conteudo t3 ON 
    (t1.id_treeapp=t3.id_treeapp AND t2.id_aplicativo=t3.id_aplicativo) 
INNER JOIN rschemar.conteudo t4 ON (t4.id_conteudo=t3.id_conteudo) 
    WHERE t1.hash = %(hash)s 
    AND t2.schema='rschemar' 

    AND (t4.expira_em > now() OR t4.expira_em IS NULL) 
    AND t4.publicado_em <= now() AND t4.publicado='True'
    AND t4.id_tipo_noticia = 1
    AND date_trunc('day', t4.publicado_em) = 
(    

SELECT date_trunc('day' , MAX(t4.publicado_em)) FROM envsite.treeapp t1 
CROSS JOIN envsite.aplicativo t2
INNER JOIN envsite.conteudo t3 ON 
    (t1.id_treeapp=t3.id_treeapp AND t2.id_aplicativo=t3.id_aplicativo) 
INNER JOIN rschemar.conteudo t4 ON (t4.id_conteudo=t3.id_conteudo) 

    WHERE t1.hash = %(hash)s 
    AND t2.schema='rschemar' 
    AND (t4.expira_em > now() OR t4.expira_em IS NULL) 
    AND t4.publicado_em <= now() AND t4.publicado='True'
    AND t4.id_tipo_noticia = 1

)
ORDER BY t4.ordem
"""


select_last_date_by_hash2 = """
EXPLAIN SELECT id_conteudo, titulo, titulo_capa, is_capa, descricao, ordem, id_tipo_noticia 
FROM rschemar.conteudo 
    WHERE date_trunc('day', publicado_em) = 
    (SELECT date_trunc('day', MAX(publicado_em)) 
    FROM rschemar.conteudo WHERE id_conteudo IN 
        (SELECT id_conteudo FROM envsite.conteudo 
        WHERE id_treeapp = 
            (SELECT id_treeapp FROM envsite.treeapp WHERE hash = %(hash)s) 
        AND id_aplicativo = 
            (SELECT id_aplicativo FROM envsite.aplicativo 
            WHERE schema='rschemar'))
    AND (expira_em > now() OR expira_em IS NULL) 
    AND publicado_em <= now() AND publicado='True')
"""

select_last_ids = """
    SELECT id_conteudo FROM rschemar.conteudo 
    WHERE date_trunc('day', publicado_em) =
        (SELECT date_trunc('day', max(publicado_em)) FROM rschemar.conteudo
        WHERE (expira_em > now() OR expira_em IS NULL) 
        AND publicado_em <= now() AND publicado='True')
"""

insert_autor               = ("INSERT INTO rschemar.autor (nome, email, grupo) VALUES "
                              "(%(nome)s, %(email)s, %(grupo)s)")

insert_autori              = ("INSERT INTO rschemar.autor (id_autor, nome, email, grupo) VALUES "
                              "(%(id_autor)i, %(nome)s, %(email)s, %(grupo)s)")

insert_noticia             = ("INSERT INTO rschemar.conteudo (id_conteudo, "
                              "titulo, titulo_categoria, descricao, id_tipo_noticia, "
                              "corpo, publicado_em, expira_em, publicado, editor, video, "
                              "audio, galeria, data_edicao, ordem, pdf, is_capa, titulo_capa, titulo_galeria, autor) VALUES "
                              "(%(id_conteudo)d, %(titulo)s, %(titulo_categoria)s, "
                              "%(descricao)s, %(id_tipo_noticia)i, %(corpo)s, %(publicado_em)s, "
                              "%(expira_em)s, %(publicado)s, %(editor)s, %(video)s, "
                              "%(audio)s, %(galeria)s, %(data_edicao)s, "
                              "%(ordem)s, %(pdf)s, %(is_capa)s, %(titulo_capa)s, %(titulo_galeria)s, %(autor)s)")

insert_noticia_autor       = ("INSERT INTO rschemar.conteudo_autor (id_conteudo, id_autor, ordem) "
                              "VALUES (%(id_conteudo)d, %(id_autor)d, %(ordem)i)")

insert_foto_noticia        = ("INSERT INTO rschemar.foto (id_conteudo, arquivo, arquivo_grande, "
                              "alinhamento, credito, legenda, link) VALUES (%(id_conteudo)d, "
                              "%(arquivo)s, %(arquivo_grande)s, %(alinhamento)s, "
                              "%(credito)s, %(legenda)s, %(link)s)")

insert_video               = ("INSERT INTO rschemar.video (id_conteudo, embed) VALUES "
                              "(%(id_conteudo)i, %(embed)s)")

insert_destaque            = ("INSERT INTO rschemar.destaque (id_conteudo, titulo, descricao, img, peso) VALUES "
                              "(%(id_conteudo)i, %(titulo)s, %(descricao)s, %(img)s, %(peso)i)")

insert_video_ipad = """
    INSERT INTO rschemar.videos_ipad (id_conteudo, nome, is_audio, thumb, link)
    VALUES (%(id_conteudo)s, %(nome)s, %(is_audio)s, %(thumb)s, %(link)s)
"""

insert_foto_ipad = """
    INSERT INTO rschemar.fotos_ipad (id_conteudo, credito, foto, legenda) VALUES
    (%(id_conteudo)s, %(credito)s, %(foto)s, %(legenda)s)
"""

delete_autor               = ("DELETE FROM rschemar.autor WHERE id_autor=%(id_autor)i")

delete_noticia             = ("DELETE FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

delete_dados_noticia       = ("DELETE FROM rschemar.foto WHERE id_conteudo=%(id_conteudo)d; "
                              "DELETE FROM rschemar.video WHERE id_conteudo=%(id_conteudo)d; "
                              "DELETE FROM rschemar.conteudo_autor WHERE id_conteudo=%(id_conteudo)d; "
                              "DELETE FROM rschemar.videos_ipad WHERE id_conteudo=%(id_conteudo)d; "
                              "DELETE FROM rschemar.fotos_ipad WHERE id_conteudo=%(id_conteudo)d; ")

delete_destaque            = ("DELETE FROM rschemar.destaque WHERE id_destaque=%(id_destaque)i")

update_autor               = ("UPDATE rschemar.autor SET nome=%(nome)s, email=%(email)s, grupo=%(grupo)s WHERE id_autor=%(id_autor)s")

update_noticia             = ("UPDATE rschemar.conteudo SET titulo_categoria=%(titulo_categoria)s, "
                              "titulo=%(titulo)s, descricao=%(descricao)s, "
                              "id_tipo_noticia=%(id_tipo_noticia)i, corpo=%(corpo)s, "
                              "publicado_em=%(publicado_em)s, expira_em=%(expira_em)s, "
                              "publicado=%(publicado)s, atualizado_em=%(atualizado_em)s, "
                              "editor=%(editor)s, video=%(video)s, audio=%(audio)s, "
                              "galeria=%(galeria)s, data_edicao=%(data_edicao)s, "
                              "ordem=%(ordem)s, pdf=%(pdf)s, titulo_capa=%(titulo_capa)s, "
                              "is_capa=%(is_capa)s, titulo_galeria=%(titulo_galeria)s, autor=%(autor)s "
                              "WHERE id_conteudo=%(id_conteudo)i")

update_destaque            = ("UPDATE rschemar.destaque SET titulo=%(titulo)s, descricao=%(descricao)s, "
                              "img=%(img)s, peso=%(peso)i WHERE id_conteudo=%(id_conteudo)i")

update_retranca            = ("UPDATE rschemar.conteudo SET retranca=%(retranca)s WHERE id_conteudo=%(id_conteudo)i")

permissions = """
  GRANT USAGE ON SCHEMA rschemar TO %(user)s;
  GRANT SELECT ON rschemar.conteudo TO %(user)s;
  GRANT SELECT ON rschemar.foto TO %(user)s;
  GRANT SELECT ON rschemar.autor TO %(user)s;
  GRANT SELECT ON rschemar.conteudo_autor TO %(user)s;
  GRANT SELECT ON rschemar.destaque TO %(user)s;
  GRANT SELECT ON rschemar.tipo_noticia TO %(user)s;
  GRANT SELECT ON rschemar.video TO %(user)s;
  GRANT SELECT ON rschemar.videos_ipad TO %(user)s;
  GRANT SELECT ON rschemar.fotos_ipad TO %(user)s;
"""

permissions_admin = permissions

structure = """
  CREATE SCHEMA rschemar;

  CREATE TABLE rschemar.tipo_noticia (
    id_tipo_noticia SERIAL NOT NULL,
    titulo VARCHAR NULL,
    PRIMARY KEY(id_tipo_noticia)
  );

  CREATE TABLE rschemar.autor (
    id_autor SERIAL NOT NULL,
    nome VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    grupo VARCHAR NULL,
    PRIMARY KEY(id_autor)
  );

  CREATE TABLE rschemar.conteudo (
    id_conteudo SERIAL NOT NULL,
    id_idioma INTEGER DEFAULT 102,
    id_tipo_noticia INT NOT NULL,
    titulo_categoria VARCHAR NULL,
    titulo VARCHAR NOT NULL,
    autor VARCHAR NULL,
    descricao VARCHAR NULL,
    editor BOOL NULL DEFAULT 'False',
    corpo VARCHAR NOT NULL,
    video BOOL NOT NULL DEFAULT 'False',
    audio BOOL NOT NULL DEFAULT 'False',
    galeria BOOL NULL DEFAULT 'False',
    publicado BOOL NOT NULL DEFAULT 'False',
    expira_em TIMESTAMP NULL,
    publicado_em TIMESTAMP NOT NULL,
    atualizado_em TIMESTAMP NULL,
    data_edicao DATE NULL,
    exportado BOOLEAN DEFAULT 'False',
    ordem INTEGER NULL,
    pdf VARCHAR NULL,
    is_capa BOOLEAN DEFAULT 'False',
    titulo_capa VARCHAR NULL,
    titulo_galeria VARCHAR NULL,
    PRIMARY KEY(id_conteudo),
    FOREIGN KEY(id_tipo_noticia)
      REFERENCES rschemar.tipo_noticia(id_tipo_noticia)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );
  CREATE INDEX rschemar_conteudo_id_tipo_noticia_index ON rschemar.conteudo USING btree (id_tipo_noticia);
  CREATE INDEX rschemar_conteudo_publicado_index ON rschemar.conteudo USING btree (publicado);
  CREATE INDEX rschemar_conteudo_publicado_em_index ON rschemar.conteudo USING btree (publicado_em);
  CREATE INDEX rschemar_conteudo_expira_em_index ON rschemar.conteudo USING btree (expira_em);
  CREATE INDEX rschemar_conteudo_data_edicao_index ON rschemar.conteudo USING btree (data_edicao);
  CREATE INDEX rschemar_conteudo_data_edicao_index_plus on rschemar.conteudo USING BTREE (data_edicao, publicado_em) WHERE data_edicao IS NOT NULL;

  CREATE TABLE rschemar.conteudo_autor(
    id_conteudo INT NOT NULL,
    id_autor INT NOT NULL,
    ordem INT NULL,
    FOREIGN KEY(id_conteudo)
      REFERENCES rschemar.conteudo(id_conteudo)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY(id_autor)
      REFERENCES rschemar.autor(id_autor)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );
  CREATE INDEX rschemar_conteudo_autor_id_conteudo_index ON rschemar.conteudo_autor USING btree (id_conteudo);

  CREATE TABLE rschemar.foto (
    id_foto SERIAL NOT NULL,
    id_conteudo INT NOT NULL,
    arquivo VARCHAR NOT NULL,
    arquivo_grande VARCHAR NULL,
    alinhamento VARCHAR NOT NULL,
    credito VARCHAR NULL,
    legenda VARCHAR NULL,
    link VARCHAR NULL,
    PRIMARY KEY(id_foto),
    FOREIGN KEY(id_conteudo)
      REFERENCES rschemar.conteudo(id_conteudo)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );
  CREATE INDEX rschemar_foto_id_conteudo_index ON rschemar.foto USING btree (id_foto);

  CREATE TABLE rschemar.video (
    id_video SERIAL NOT NULL,
    id_conteudo INT NOT NULL,
    embed VARCHAR NOT NULL,
    PRIMARY KEY(id_video),
    FOREIGN KEY(id_conteudo)
      REFERENCES rschemar.conteudo(id_conteudo)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );
  CREATE INDEX rschemar_video_id_conteudo_index ON rschemar.video USING btree (id_video);

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
  
  CREATE TABLE rschemar.videos_ipad (
    id_video SERIAL NOT NULL,
    id_conteudo INT NOT NULL,
    nome VARCHAR NULL,
    is_audio BOOLEAN NULL,
    thumb VARCHAR NULL,
    link VARCHAR NULL,
    PRIMARY KEY(id_video),
    FOREIGN KEY(id_conteudo)
      REFERENCES rschemar.conteudo(id_conteudo)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );
  CREATE INDEX rschemar_videos_ipad_id_video_index ON rschemar.videos_ipad USING btree (id_video);
  
  CREATE TABLE rschemar.fotos_ipad (
    id_foto SERIAL NOT NULL,
    id_conteudo INT NOT NULL,
    foto VARCHAR NULL,
    credito VARCHAR NULL,
    legenda VARCHAR NULL,
    PRIMARY KEY(id_foto),
    FOREIGN KEY(id_conteudo)
      REFERENCES rschemar.conteudo(id_conteudo)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );
  CREATE INDEX rschemar_fotos_ipad_id_foto_index ON rschemar.fotos_ipad USING btree (id_foto);

  INSERT INTO rschemar.tipo_noticia (id_tipo_noticia, titulo) VALUES (1, 'Manchete principal');
  INSERT INTO rschemar.tipo_noticia (id_tipo_noticia, titulo) VALUES (6, 'Normal');
  INSERT INTO rschemar.tipo_noticia (id_tipo_noticia, titulo) VALUES (7, 'Retranca');
"""
