# -*r encoding: LATIN1 -*-
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

insert_voto              = ("UPDATE envsite.conteudo SET voto=voto+%(voto)f, nvoto=(nvoto+1), publicado=False "
                            "WHERE id_conteudo=%(id_conteudo)i AND id_aplicativo="
                            "(SELECT id_aplicativo FROM envsite.aplicativo WHERE schema=%(schema)s)")

insert_comentario        = ("INSERT INTO envsite.comentario (id_comentario, id_conteudo, "
                            "id_aplicativo, autor, email, comentario, "
                            "datahora, ip, autorizado, bloqueado, reprovado, moderacao, dados) "
                            "VALUES "
                            "(%(id_comentario)i, %(id_conteudo)i, "
                            "(SELECT id_aplicativo FROM envsite.aplicativo WHERE schema=%(schema)s), "
                            "%(autor)s, %(email)s, %(comentario)s, now(), %(ip)s, "
                            "%(autorizado)s, False, False, False, '{}') ")

insert_captcha           = ("DELETE FROM rschemar.captcha WHERE datahora < %(datah)s;"
                           "INSERT INTO rschemar.captcha (hash, solucao, datahora) VALUES (%(hash)s, %(solucao)s, now());")

insert_wad_temp          = ("DELETE FROM rschemar.wad_temp WHERE (data < (now()- interval '1 day')) OR email=%(email)s OR hash=%(hash)s; "
                           "INSERT INTO rschemar.wad_temp(hash, email, dados, data) VALUES (%(hash)s, %(email)s, %(dados)s, now());")

update_conteudo_exportar = ("UPDATE envsite.conteudo SET publicado=False WHERE id_conteudo=%(id_conteudo)i "
                            "AND id_aplicativo=(SELECT id_aplicativo FROM envsite.aplicativo  WHERE schema=%(schema)s)")

update_session_user      = ("UPDATE rschemar.session SET datahora=now() WHERE id_session=%(id_session)s")

select_email             = ("SELECT A.email FROM %(sc)s.conteudo N"
                           " INNER JOIN %(sc)s.conteudo_autor NA ON(N.id_conteudo=NA.id_conteudo)"
                           " INNER JOIN %(sc)s.autor A ON(NA.id_autor=A.id_autor)"
                           " WHERE N.id_conteudo=%(id_conteudo)i")

select_email_moderado    = ("SELECT S.email FROM %(app)s.sessao S INNER JOIN %(app)s.noticia N ON(S.id_sessao=N.id_sessao) "
                            "WHERE N.id_noticia=%(id_noticia)i")

select_sessao_captcha    = "SELECT solucao FROM rschemar.captcha WHERE hash=%(hash)s LIMIT 1"

select_cadastro_captcha  = "SELECT hash, email, dados, data FROM rschemar.wad_temp WHERE hash=%(hash)s  LIMIT 1"

select_email_bloqueado   = "SELECT count(*) as qtde FROM %(app)s.email_bloqueado WHERE email=%(email)s"

select_moderado          = ("SELECT T.configuracao, CC.titulo, C.id_aplicativo "
                            "FROM envsite.conteudo C "
                            "INNER JOIN envsite.treeapp T ON(C.id_treeapp=T.id_treeapp) "
                            "INNER JOIN %(schema)s.conteudo CC ON(C.id_conteudo=CC.id_conteudo) "
                            "WHERE C.id_conteudo=%(id_conteudo)i AND "
                            "C.id_aplicativo=(SELECT id_aplicativo FROM envsite.aplicativo WHERE schema=%(schemai)s) ")

select_id_comentario     = ("SELECT NEXTVAL('envsite.comentario_id_comentario_seq') as next")

select_comentario        = ("SELECT autor, email, comentario FROM envsite.comentario WHERE id_comentario=%(id_comentario)i")

select_session_dados     = ("SELECT id_session, nome, email, extra FROM rschemar.session "
                            "WHERE id_session=%(id_session)s AND datahora >= %(datahora)s LIMIT 1")

insert_session           = ("INSERT INTO rschemar.session (id_session, nome, email, datahora, extra) "
                            "VALUES (%(id_session)s, %(nome)s, %(email)s, now(), %(extra)s);"
                            "DELETE FROM rschemar.session WHERE datahora < %(datahorae)s;")

delete_session           = "DELETE FROM rschemar.session WHERE id_session=%(id_session)s;"

permissions = """
  GRANT USAGE ON SCHEMA rschemar TO %(user)s;
  GRANT SELECT, DELETE, INSERT, UPDATE ON rschemar.session TO %(user)s;
  GRANT SELECT, INSERT, UPDATE, DELETE ON rschemar.captcha TO %(user)s;
  GRANT SELECT, INSERT, DELETE ON rschemar.wad_temp TO %(user)s;
"""

permissions_admin = permissions

structure = """
  CREATE SCHEMA rschemar;

  CREATE TABLE rschemar.session (
    id_session VARCHAR NOT NULL,
    nome VARCHAR NULL,
    email VARCHAR NULL,
    datahora TIMESTAMP NULL,
    extra VARCHAR NULL,
    PRIMARY KEY(id_session)
  );
  CREATE INDEX rschemar_session_datahora_index ON rschemar.session USING btree (datahora);

  CREATE TABLE rschemar.captcha (
    hash VARCHAR NOT NULL,
    solucao VARCHAR NOT NULL,
    datahora TIMESTAMP NOT NULL
  );

  CREATE TABLE rschemar.wad_temp (
    hash VARCHAR(32) NOT NULL,
    email VARCHAR(64) NOT NULL,
    dados VARCHAR NOT NULL,
    data TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY(hash)
  );
  CREATE INDEX rschemar_wad_temp_index1 ON rschemar.wad_temp USING btree (hash);
  CREATE INDEX rschemar_wad_temp_index2 ON rschemar.wad_temp USING btree (data);
  CREATE INDEX rschemar_wad_temp_index3 ON rschemar.wad_temp USING btree (email);
"""
