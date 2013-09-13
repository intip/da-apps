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
select_nextval_conteudo = ("SELECT NEXTVAL('"
                          "rschemar.conteudo_id_conteudo_seq'::text) as id")

select_nextval_programa_diaria = ("SELECT NEXTVAL('"
                             "rschemar.conteudo_id_conteudo_seq'::text) as id")

select_nextval_programa_programacao_diaria = (
"SELECT NEXTVAL('rschemar.programa_programacao_diaria_id"
                 "_programa_programacao_diaria_seq'::text) as id")

select_nextval_secao = ("SELECT NEXTVAL('rschemar.secao_id"
                        "_secao_seq'::text) as id")

select_nextval_tipo = ("SELECT NEXTVAL('rschemar.tipo_id"
                        "_tipo_seq'::text) as id")

select_nextval_programa = (
"SELECT NEXTVAL('rschemar.programa_id_programa_seq'::text) as id")

select_status_content = ("SELECT publicado FROM rschemar.conteudo "
"WHERE id_conteudo=%(id_conteudo)i")

select_compare_hour = ("select count(*) from rschemar.programa_programacao_diaria where "
" data=%(data)s and (hora_inicio between %(hora_inicio)s and %(hora_fim)s or "
"hora_fim between %(hora_inicio)s and %(hora_fim)s);")

select_compare_hour_edit = ("select count(*) from rschemar.programa_programacao_diaria where "
"id_programa_programacao_diaria <> %(id_programa_programacao_diaria)i and "
"data=%(data)s and (hora_inicio between %(hora_inicio)s and %(hora_fim)s or "
"hora_fim between %(hora_inicio)s and %(hora_fim)s);")

select_programas_id_conteudo = ("SELECT P.nome, P.id_programa, "
" to_char(PP.hora_inicio, 'HH24:MI') as hora_inicio,"
" to_char(PP.hora_fim, 'HH24:MI') as hora_fim, "
" PP.id_programa_programacao_diaria "
" FROM rschemar.programa_programacao_diaria PP"
"  JOIN rschemar.programa P ON (P.id_programa = PP.id_programa) "
"  WHERE id_programacao_diaria = %(id_programacao_diaria)i ORDER BY hora_inicio ASC")

select_full_programa_programacao_diaria = ("SELECT id_programa_programacao_diaria, to_char(data,'DD/MM/YYYY') as data "
"FROM rschemar.programa_programacao_diaria "
"WHERE to_char(data, 'ID')=%(dia)s AND hora_inicio=%(hora_inicio)s AND hora_fim=%(hora_fim)s " 
"AND id_programacao_diaria<>%(id_conteudo)i AND data>=now() AND id_programa=%(id_programa)i ")

select_unit_programa_programacao_diaria = ("SELECT id_programa,"
" to_char(hora_inicio,'HH24:MI') as hora_inicio,"
" to_char(hora_fim,'HH24:MI') as hora_fim,"
" to_char(data,'YYYY-MM-DD') as data,"
" id_programa_programacao_diaria, id_programacao_diaria "
" FROM rschemar.programa_programacao_diaria"
"  WHERE id_programa_programacao_diaria = %(id_programa_programacao_diaria)i")

select_unit_programa = ("SELECT id_secao, id_programa, id_tipo, link, slogan,"
" imagem, descricao, nome, data FROM rschemar.programa "
" WHERE id_programa = %(id_programa)i")

select_unit_secao = ("SELECT id_secao, nome FROM rschemar.secao "
" WHERE id_secao = %(id_secao)i")

select_dados = ("SELECT N.id_conteudo, N.titulo, N.descricao, "
"to_char(N.expira_em, 'YYYY-MM-DD HH24:MI') as expira_em, "
"to_char(N.publicado_em, 'YYYY-MM-DD HH24:MI') as publicado_em, N.publicado, "
"to_char(N.atualizado_em, 'YYYY-MM-DD HH24:MI') as atualizado_em, "
"D.id_destaque, D.titulo as titulo_destaque,"
" D.descricao as descricao_destaque, "
"D.img, D.img as imagem_destaque, D.peso as peso_destaque "
"FROM rschemar.conteudo N "
"LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo) "
"WHERE N.id_conteudo=%(id_conteudo)i")

select_programas = ("SELECT nome, id_secao, id_tipo,link,  "
                           "id_programa FROM rschemar.programa ORDER BY nome")

select_programas_nacional = ("SELECT P.nome,S.nome as secao,"
                           "P.id_programa FROM rschemar.programa P"
"      JOIN rschemar.secao S on(S.id_secao = P.id_secao) ORDER BY nome")

select_secaos = ("SELECT nome,id_secao FROM rschemar.secao ORDER BY nome")

select_tipos = ("SELECT nome,id_tipo FROM rschemar.tipo ORDER BY nome")

select_titulo = ("SELECT titulo FROM rschemar.conteudo "
                  "WHERE id_conteudo=%(id_conteudo)i ")

search_vinculo = ("SELECT P.nome, PD.titulo "
                 " FROM rschemar.programa_programacao_diaria PP "
                 " JOIN rschemar.programa P ON(P.id_programa = PP.id_programa)"
                 " JOIN rschemar.conteudo PD ON (PD.id_conteudo = "
                 " PP.id_programacao_diaria) "
                 " WHERE PP.id_programa= %(id_programa)i")

select_dublin_core = ("SELECT titulo, descricao, "
"to_char(atualizado_em, 'YYYY-MM-DD HH24:MI:SS') as atualizado_em, "
"to_char(publicado_em, 'YYYY-MM-DD HH24:MI:SS') as publicado_em "
"FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

select_programas_by_data = ("SELECT to_char(PPD.hora_inicio,'HH24:MI') "
" as hora_inicio, PG.nome, PG.link, PD.titulo as titulodata,  "
" to_char(PPD.hora_fim,'HH24:MI') as hora_fim,"
" PPD.id_programa, "
" PPD.id_programa_programacao_diaria FROM rschemar.programa_programacao_diaria PPD "
" JOIN rschemar.conteudo PD ON (PD.id_conteudo ="
" PPD.id_programacao_diaria) "
" JOIN rschemar.programa PG ON (PG.id_programa = PPD.id_programa)"
" WHERE PD.data = %(data)s ORDER BY PPD.hora_inicio ASC")

select_programas_vinculado = ("SELECT to_char(hora_inicio,'HH24:MI') "
" as hora_inicio, "
" to_char(hora_fim,'HH24:MI') as hora_fim,"
" id_programa, "
" id_programa_programacao_diaria FROM rschemar.programa_programacao_diaria "
" WHERE id_programa_programacao_diaria = %(id_programa_programacao_diaria)i")

select_programas_no_ar = ("SELECT P.nome, P.id_programa,  "
" to_char(PP.hora_inicio, 'HH24:MI') as hora_inicio,"
" to_char(PP.data, 'DD/MM/YYYY') as data, "
" to_char(PP.hora_fim, 'HH24:MI') as hora_fim, "
" P.slogan, P.imagem, P.descricao, "
" to_char(PP.hora_fim, 'HH24:MI') as hora_fim, "
" PP.id_programa_programacao_diaria, P.link "
" FROM rschemar.programa_programacao_diaria PP"
"  JOIN rschemar.programa P ON (P.id_programa = PP.id_programa) "
"  WHERE PP.hora_fim > %(hora_atual)s"
"  AND PP.data = %(data_atual)s"
"  ORDER BY PP.hora_inicio LIMIT %(limit)i")

select_clone_programas = ("SELECT to_char(PP.hora_inicio,'HH24:MI') "
" as hora_inicio, "
" to_char(PP.hora_fim,'HH24:MI') as hora_fim,"
" PP.id_programa, "
" PP.id_programa_programacao_diaria FROM rschemar.programa_programacao_diaria PP "
" JOIN rschemar.conteudo PD ON (PD.id_conteudo=PP.id_programacao_diaria)"
" WHERE PD.titulo = %(titulo)s")

select_conteudo = ("SELECT N.id_conteudo, N.titulo, N.descricao,  "
"to_char(N.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em, N.publicado, "
"D.id_destaque, D.titulo as titulo_destaque,"
" D.descricao as descricao_destaque, "
"D.img, D.img as imagem_destaque, D.peso as peso_destaque,  "
"to_char(N.data, 'DD/MM/YYYY') as data "
"FROM rschemar.conteudo N "
"LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo) "
"WHERE N.id_conteudo=%(id_conteudo)i")

select_conteudo_date = ("SELECT id_conteudo FROM rschemar.conteudo WHERE data=%(dt)s")

insert_conteudo = ("INSERT INTO rschemar.conteudo (id_conteudo, "
"titulo, descricao, publicado_em, expira_em, publicado, data) VALUES( "
"%(id_conteudo)i, %(titulo)s, %(descricao)s, %(publicado_em)s, %(expira_em)s,"
" %(publicado)s, %(data)s)")

insert_destaque = ("INSERT INTO rschemar.destaque (id_conteudo, titulo,"
" descricao, img, peso) VALUES "
"(%(id_conteudo)i, %(titulo)s, %(descricao)s, %(img)s, %(peso)i)")

insert_tipo = ("INSERT INTO rschemar.tipo (id_tipo, nome) VALUES "
"(%(id_tipo)i, %(nome)s)")

insert_secao = ("INSERT INTO rschemar.secao (id_secao, nome) VALUES "
"(%(id_secao)i, %(nome)s)")

insert_secao = ("INSERT INTO rschemar.secao (id_secao, nome) VALUES "
"(%(id_secao)i, %(nome)s)")

insert_programa_programacao_dia = (
"INSERT INTO rschemar.programa_programacao_diaria ("
"id_programa_programacao_diaria, id_programa, id_programacao_diaria,"
" hora_inicio, hora_fim, data) VALUES "
"(%(id_programa_programacao_diaria)i, %(id_programa)i, "
"%(id_programacao_diaria)i, %(hora_inicio)s, %(hora_fim)s, to_date(%(data)s, 'yyyy-mm-dd'))")

insert_programa = ("INSERT INTO rschemar.programa (id_secao,id_tipo,"
"link,slogan,imagem,descricao,nome,data) VALUES "
"(%(id_secao)i, %(id_tipo)i, %(link)s, %(slogan)s,"
" %(imagem)s, %(descricao)s, %(nome)s, %(data)s)")

insert_programa_nsec = ("INSERT INTO rschemar.programa (id_tipo,"
"link,slogan,imagem,descricao,nome,data) VALUES "
"(%(id_tipo)i, %(link)s, %(slogan)s,"
" %(imagem)s, %(descricao)s, %(nome)s, %(data)s)")

update_conteudo = ("UPDATE rschemar.conteudo SET titulo=%(titulo)s, "
"descricao=%(descricao)s, publicado_em=%(publicado_em)s, "
"expira_em=%(expira_em)s, publicado=%(publicado)s, "
"data=%(data)s "
"WHERE id_conteudo=%(id_conteudo)i")

update_secao = ("UPDATE rschemar.secao SET nome=%(nome)s "
"WHERE id_secao=%(id_secao)i")

update_full_programa_programacao_diaria = ("UPDATE rschemar.programa_programacao_diaria SET hora_inicio=%(hora_inicio)s, "
"hora_fim=%(hora_fim)s WHERE id_programa_programacao_diaria = %(id_programa_programacao_diaria)i")

update_programa_programacao_diaria = (
"UPDATE rschemar.programa_programacao_diaria SET hora_inicio=%(hora_inicio)s, "
"hora_fim=%(hora_fim)s, id_programa=%(id_programa)i, "
"id_programacao_diaria=%(id_programacao_diaria)i "
"WHERE id_programa_programacao_diaria=%(id_programa_programacao_diaria)i")

update_programa = ("UPDATE rschemar.programa SET nome=%(nome)s, "
"slogan=%(slogan)s, id_programa=%(id_programa)i, imagem=%(imagem)s, "
"id_tipo=%(id_tipo)i, id_secao=%(id_secao)i, link=%(link)s "
"WHERE id_programa=%(id_programa)i")

update_programa_nsec = ("UPDATE rschemar.programa SET nome=%(nome)s, "
"slogan=%(slogan)s, id_programa=%(id_programa)i, imagem=%(imagem)s, "
"id_tipo=%(id_tipo)i, link=%(link)s "
"WHERE id_programa=%(id_programa)i")

update_programa_programacao_diaria_date = ("UPDATE rschemar.programa_programacao_diaria SET  "
"data=%(data)s WHERE id_programa_programacao_diaria=%(id_programa_programacao_diaria)i")

delete_conteudo = ("DELETE FROM rschemar.conteudo"
                   " WHERE id_conteudo=%(id_conteudo)i")

del_programa = ("DELETE FROM rschemar.programa "
                "WHERE id_programa=%(id_programa)i")

del_programa_vinculado = ("DELETE FROM rschemar.programa_programacao_diaria"
" WHERE id_programa_programacao_diaria=%(id_programa_programacao_diaria)i")

del_secao = ("DELETE FROM rschemar.secao WHERE id_secao=%(id_secao)i")

delete_destaque = ("DELETE FROM rschemar.destaque "
                   "WHERE id_conteudo=%(id_conteudo)i")

delete_tipo = ("DELETE FROM rschemar.tipo WHERE id_tipo=%(id_tipo)i")

delete_secao = ("DELETE FROM rschemar.secao WHERE id_secao=%(id_secao)i")

delete_programacao_diaria = ("DELETE FROM rschemar.programa"
                            " WHERE id_programa=%(id_programa)i")

permissions = """GRANT USAGE ON SCHEMA rschemar TO %(user)s;
GRANT SELECT ON rschemar.conteudo TO %(user)s;
GRANT SELECT ON rschemar.destaque TO %(user)s;
GRANT SELECT ON rschemar.tipo TO %(user)s;
GRANT SELECT ON rschemar.programa TO %(user)s;
GRANT SELECT ON rschemar.secao TO %(user)s;
GRANT SELECT ON rschemar.programa_programacao_diaria TO %(user)s;"""



permissions_admin = permissions

structure = """
  CREATE SCHEMA rschemar;


  CREATE TABLE rschemar.tipo (
    id_tipo SERIAL NOT NULL,
    nome VARCHAR NOT NULL,
    PRIMARY KEY(id_tipo)
  );


  CREATE TABLE rschemar.secao (
    id_secao SERIAL NOT NULL,
    nome VARCHAR NOT NULL,
    PRIMARY KEY(id_secao)
  );

  CREATE TABLE rschemar.conteudo (
    id_conteudo SERIAL NOT NULL,
    id_idioma INTEGER DEFAULT 102,
    titulo VARCHAR NOT NULL,
    data DATE NOT NULL,
    descricao VARCHAR NULL,
    arquivo VARCHAR,
    publicado BOOL NOT NULL DEFAULT 'False',
    expira_em TIMESTAMP NULL,
    publicado_em TIMESTAMP NOT NULL,
    atualizado_em TIMESTAMP NULL,
    exportado BOOLEAN DEFAULT 'False',
    PRIMARY KEY(id_conteudo)
  );
  CREATE INDEX rschemar_conteudo_publicado_index ON rschemar.conteudo 
               USING btree (publicado);

  CREATE INDEX rschemar_conteudo_publicado_em_index
               ON rschemar.conteudo USING btree (publicado_em);

  CREATE INDEX rschemar_conteudo_expira_em_index
               ON rschemar.conteudo USING btree (expira_em);

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
  CREATE INDEX rschemar_destaque_id_conteudo_index
               ON rschemar.destaque USING btree (id_conteudo);

  CREATE TABLE rschemar.programa (
    id_programa SERIAL NOT NULL,
    id_secao INTEGER NULL,
    id_tipo INTEGER NULL,
    link VARCHAR NULL,
    slogan VARCHAR NULL,
    imagem VARCHAR NULL,
    descricao VARCHAR NULL,
    nome VARCHAR NULL,
    data DATE NOT NULL,
    PRIMARY KEY(id_programa),
    FOREIGN KEY(id_tipo)
      REFERENCES rschemar.tipo(id_tipo)
        ON DELETE SET NULL,
    FOREIGN KEY(id_secao)
      REFERENCES rschemar.secao(id_secao)
        ON DELETE SET NULL
  );
  CREATE INDEX rschemar_programa_id_secao_index ON
               rschemar.programa USING btree (id_secao);

  CREATE INDEX rschemar_programa_id_tipo_index
               ON rschemar.programa USING btree (id_tipo);

  CREATE TABLE rschemar.programa_programacao_diaria(
    id_programa_programacao_diaria SERIAL NOT NULL,
    id_programa INTEGER NOT NULL,
    id_programacao_diaria INTEGER NOT NULL,
    data DATE NULL,
    hora_inicio TIME,
    hora_fim TIME,
    PRIMARY KEY(id_programa_programacao_diaria),
    FOREIGN KEY(id_programa)
      REFERENCES rschemar.programa(id_programa)
        ON DELETE CASCADE,
    FOREIGN KEY(id_programacao_diaria)
      REFERENCES rschemar.conteudo(id_conteudo)
        ON DELETE CASCADE
  );

  INSERT INTO rschemar.secao VALUES (1,'Jornalismo');
  INSERT INTO rschemar.secao VALUES (2,'Humor');
  INSERT INTO rschemar.secao VALUES (3,'Novelas');
  INSERT INTO rschemar.secao VALUES (4,'Filmes');
  INSERT INTO rschemar.secao VALUES (5,'Infantil');
  INSERT INTO rschemar.secao VALUES (6,'Adulto');

  INSERT INTO rschemar.tipo VALUES (1,'Nacional');
  INSERT INTO rschemar.tipo VALUES (6,'Regional');


"""
