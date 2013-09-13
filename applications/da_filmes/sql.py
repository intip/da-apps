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
select_nextval_conteudo = ("SELECT NEXTVAL('rschemar.conteudo_id_conteudo_seq'::text) as id")

select_nextval_genero = ("SELECT NEXTVAL('rschemar.genero_id_genero_seq'::text) as id")

select_nextval_pais = ("SELECT NEXTVAL('rschemar.pais_id_pais_seq'::text) as id")

select_status_content = ("SELECT publicado FROM rschemar.conteudo "
"WHERE id_conteudo=%(id_conteudo)i")

select_dados = ("SELECT N.id_conteudo, N.titulo, N.descricao, "
"to_char(N.expira_em, 'YYYY-MM-DD HH24:MI') as expira_em, "
"to_char(N.publicado_em, 'YYYY-MM-DD HH24:MI') as publicado_em, N.publicado, "
"to_char(N.atualizado_em, 'YYYY-MM-DD HH24:MI') as atualizado_em, "
"D.id_destaque, D.titulo as titulo_destaque, D.descricao as descricao_destaque, "
"D.img, D.img as imagem_destaque, D.peso as peso_destaque "
"FROM rschemar.conteudo N "
"LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo) "
"WHERE N.id_conteudo=%(id_conteudo)i")


select_titulo = ("SELECT titulo FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

select_genero = ("SELECT nome, id_genero FROM rschemar.genero")

select_pais = ("SELECT nome, id_pais FROM rschemar.pais")

select_genero_id = ("SELECT id_genero FROM rschemar.genero where nome=%(nome)s")
select_pais_id = ("SELECT id_pais FROM rschemar.pais where nome=%(nome)s")

select_dublin_core = ("SELECT titulo, descricao, "
"to_char(atualizado_em, 'YYYY-MM-DD HH24:MI:SS') as atualizado_em, "
"to_char(publicado_em, 'YYYY-MM-DD HH24:MI:SS') as publicado_em "
"FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

select_filmes_limit = ("SELECT titulo, id_conteudo as id_filme FROM rschemar.conteudo ORDER BY id_conteudo DESC LIMIT %(limit)i")
select_filmes = ("SELECT titulo, id_conteudo as id_filme FROM rschemar.conteudo ORDER BY id_conteudo DESC")

select_pais_filme = ("SELECT P.id_pais, P.nome FROM rschemar.pais P JOIN rschemar.pais_filme F ON (P.id_pais=F.id_pais) "
                     "AND F.id_conteudo=%(id_conteudo)i")
select_conteudo = ("SELECT N.id_conteudo, N.titulo, N.descricao,  "
"to_char(N.expira_em, 'DD/MM/YYYY HH24:MI') as expira_em, genero,"
" N.titulo_original, N.ano, N.id_genero, "
" N.direcao, N.duracao, N.censura, N.elenco, N.sinopse, N.trailer,"
"to_char(N.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em, N.publicado, "
"D.id_destaque, D.titulo as titulo_destaque, D.descricao as descricao_destaque, "
"D.img, D.img as imagem_destaque, D.peso as peso_destaque "
"FROM rschemar.conteudo N "
"LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo) "
"WHERE N.id_conteudo=%(id_conteudo)i")

select_filme = ("SELECT N.id_conteudo, N.id_conteudo as id_filme, N.titulo, N.descricao,  "
"to_char(N.expira_em, 'DD/MM/YYYY HH24:MI') as expira_em, genero as genero, "
" N.titulo_original, N.ano, N.id_genero, "
" N.direcao, N.duracao, N.censura, N.elenco, N.sinopse, N.trailer,"
"to_char(N.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em, N.publicado, "
"D.id_destaque, D.titulo as titulo_destaque, D.descricao as descricao_destaque, "
"D.img, D.img as imagem_destaque, D.peso as peso_destaque "
" FROM rschemar.conteudo N "
"LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo) "
"WHERE N.id_conteudo=%(id_conteudo)i")

insert_conteudo = ("INSERT INTO rschemar.conteudo (id_conteudo, titulo, descricao,"
" publicado_em, expira_em, publicado, titulo_original, ano, genero,"
" direcao, duracao, censura, elenco, sinopse, trailer) VALUES (%(id_conteudo)i, %(titulo)s,"
" %(descricao)s, %(publicado_em)s, %(expira_em)s, %(publicado)s, %(titulo_original)s, %(ano)s, "
" %(genero)s, "
" %(direcao)s, %(duracao)s, %(censura)s, %(elenco)s, %(sinopse)s, %(trailer)s)")

insert_destaque  = ("INSERT INTO rschemar.destaque (id_conteudo, titulo, descricao, img, peso) VALUES "
"(%(id_conteudo)i, %(titulo)s, %(descricao)s, %(img)s, %(peso)i)")

insert_genero = ("INSERT INTO rschemar.genero(nome,id_genero) VALUES (%(nome)s,%(id_genero)i)")

insert_pais_filme = ("INSERT INTO rschemar.pais_filme VALUES (%(id_conteudo)i, %(id_pais)i)")

insert_pais = ("INSERT INTO rschemar.pais(nome,id_pais) VALUES (%(nome)s,%(id_pais)i)")

update_conteudo = ("UPDATE rschemar.conteudo SET titulo=%(titulo)s, "
" descricao=%(descricao)s, publicado_em=%(publicado_em)s, "
" expira_em=%(expira_em)s, publicado=%(publicado)s, "
" titulo_original=%(titulo_original)s, ano=%(ano)s, "
" genero=%(genero)s, direcao=%(direcao)s, duracao=%(duracao)s, censura=%(censura)s,"
" elenco=%(elenco)s, sinopse=%(sinopse)s, trailer=%(trailer)s "
" WHERE id_conteudo=%(id_conteudo)i")

update_genero = ("UPDATE rschemar.genero SET nome=%(nome)s WHERE id_genero=%(id_genero)i")

update_pais = ("UPDATE rschemar.pais SET nome=%(nome)s WHERE id_pais=%(id_pais)i")

delete_conteudo = ("DELETE FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

delete_genero = ("DELETE FROM rschemar.genero WHERE id_genero=%(id_genero)i")

delete_pais = ("DELETE FROM rschemar.pais WHERE id_pais=%(id_pais)i")

exists_genero = ("SELECT g.id_genero from rschemar.genero g JOIN rschemar.conteudo c on "
                 "g.id_genero=c.id_genero WHERE g.id_genero=%(id_genero)i")

exists_pais = ("SELECT g.id_pais from rschemar.pais g JOIN rschemar.conteudo c on "
                 "g.id_pais=c.id_pais WHERE g.id_pais=%(id_pais)i")

delete_destaque = ("DELETE FROM rschemar.destaque WHERE id_conteudo=%(id_conteudo)i")

delete_pais_filme = ("DELETE FROM rschemar.pais_filme WHERE id_conteudo=%(id_conteudo)i")

permissions = ("GRANT USAGE ON SCHEMA rschemar TO %(user)s;"
"GRANT SELECT ON rschemar.conteudo TO %(user)s;"
"GRANT SELECT ON rschemar.destaque TO %(user)s;"
"GRANT SELECT ON rschemar.pais_filme TO %(user)s;"
"GRANT SELECT ON rschemar.pais TO %(user)s;"
)

permissions_admin = permissions

structure = """
  CREATE SCHEMA rschemar;

  CREATE TABLE rschemar.tipo(
    id_tipo SERIAL NOT NULL,
    tipo VARCHAR NOT NULL,
    PRIMARY KEY(id_tipo)
  );

  CREATE TABLE rschemar.genero(
    id_genero SERIAL NOT NULL,
    nome VARCHAR NOT NULL,
    PRIMARY KEY(id_genero)
  );

  CREATE TABLE rschemar.pais(
    id_pais SERIAL NOT NULL,
    nome VARCHAR NOT NULL,
    PRIMARY KEY(id_pais)

  );

  CREATE TABLE rschemar.conteudo (
    id_conteudo SERIAL NOT NULL,
    id_idioma INTEGER DEFAULT 102,
    titulo VARCHAR NOT NULL,
    descricao VARCHAR NULL,
    titulo_original VARCHAR NULL,
    genero VARCHAR NULL,
    ano VARCHAR NULL,
    id_tipo INT NULL,
    id_genero INT NULL,
    direcao VARCHAR NULL,
    duracao VARCHAR NULL,
    censura VARCHAR NULL,
    elenco VARCHAR NULL,
    sinopse VARCHAR NULL,
    trailer VARCHAR NULL,
    arquivo VARCHAR,
    publicado BOOL NOT NULL DEFAULT 'False',
    expira_em TIMESTAMP NULL,
    publicado_em TIMESTAMP NOT NULL,
    atualizado_em TIMESTAMP NULL,
    exportado BOOLEAN DEFAULT 'False',
    PRIMARY KEY(id_conteudo),
    FOREIGN KEY(id_tipo)
      REFERENCES rschemar.tipo(id_tipo)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY(id_genero)
      REFERENCES rschemar.genero(id_genero)
        ON DELETE CASCADE
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

  CREATE TABLE rschemar.pais_filme (
    id_conteudo INT NOT NULL,
    id_pais INT NOT NULL,
    FOREIGN KEY(id_conteudo)
       REFERENCES rschemar.conteudo(id_conteudo)
          ON DELETE CASCADE,
    FOREIGN KEY(id_pais)
       REFERENCES rschemar.pais(id_pais)
          ON DELETE CASCADE
);
"""
