# -*- encoding: latin1 -*-
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
"""
    Module with the sql queries for the establishment app.
"""

#FIXME: constantes deviam ser UPPER_CASE

#SELECTS
select_conteudo = """
    SELECT * FROM rschemar.conteudo WHERE id_conteudo = %(id_conteudo)i
"""

select_nextval_conteudo = """
    SELECT NEXTVAL('rschemar.conteudo_id_conteudo_seq'::text) as id
"""

select_status_content = """
    SELECT publicado FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i
"""

select_por_titulo = """
    SELECT id_conteudo FROM rschemar.conteudo WHERE titulo=%(titulo)s
"""

select_titulo = """
    SELECT titulo FROM rschemar.conteudo 
    WHERE id_conteudo=%(id_conteudo)i
"""

select_dublin_core = """
    SELECT titulo, descricao, 
    to_char(atualizado_em, 'YYYY-MM-DD HH24:MI:SS') as atualizado_em, 
    to_char(publicado_em, 'YYYY-MM-DD HH24:MI:SS') as publicado_em 
    FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i
"""

select_conteudo_dados = """SELECT N.id_conteudo, N.titulo, N.descricao, 
to_char(N.expira_em, 'YYYY-MM-DD HH24:MI') as expira_em, N.imagem, 
to_char(N.publicado_em, 'YYYY-MM-DD HH24:MI') as publicado_em, N.publicado, 
D.id_destaque, D.titulo as titulo_destaque, D.descricao as descricao_destaque, 
D.img as imagem_destaque FROM rschemar.conteudo N 
LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo) 
WHERE N.id_conteudo=%(id_conteudo)i"""

select_sorte = """
    SELECT id_conteudo, descricao, titulo FROM rschemar.conteudo WHERE 
    publicado = TRUE ORDER BY random() LIMIT 1
"""

select_caracteristicas = """
    SELECT * FROM rschemar.caracteristicas
"""

select_cara_conteudo = """
    SELECT id_caracteristica FROM rschemar.caracteristica_conteudo 
    WHERE id_conteudo=%(id_conteudo)s
"""

select_nome = """
    SELECT id_conteudo FROM rschemar.caracteristica_conteudo WHERE
    id_caracteristica=%(id_caracteristica)s
"""


#INSERTS
insert_conteudo_ = """
    INSERT INTO rschemar.conteudo (id_conteudo, titulo, descricao, 
    imagem, publicado, publicado_em, expira_em, musica) VALUES 
    (%(id_conteudo)i, %(titulo)s, %(descricao)s, 
     %(imagem)s, %(publicado)s, %(publicado_em)s, %(expira_em)s, %(musica)s)
"""

insert_destaque = """
    INSERT INTO rschemar.destaque (id_conteudo, titulo, descricao, img) VALUES 
    (%(id_conteudo)i, %(titulo)s, %(descricao)s, %(img)s)
"""

insert_persona = """
    INSERT INTO rschemar.caracteristica_conteudo (id_caracteristica, 
    id_conteudo) VALUES (%(id_caracteristica)s, %(id_conteudo)s)
"""

#UPDATES
update_conteudo = """
    UPDATE rschemar.conteudo SET titulo=%(titulo)s, 
    descricao=%(descricao)s, imagem=%(imagem)s,
    publicado_em=%(publicado_em)s, expira_em=%(expira_em)s, 
    musica=%(musica)s WHERE id_conteudo = %(id_conteudo)i
"""

update_destaque = """
    UPDATE rschemar.destaque SET titulo=%(titulo)s, descricao=%(descricao)s,
    img=%(img)s WHERE id_destaque=%(id_destaque)i"
"""

#DELETES
delete_conteudo_ = """
    DELETE FROM rschemar.conteudo WHERE id_conteudo = %(id_conteudo)i
"""

delete_persona = """
    DELETE FROM rschemar.caracteristica_conteudo WHERE 
    id_conteudo=%(id_conteudo)s
"""

#GRANTS
permissions = """
    GRANT USAGE ON SCHEMA rschemar TO %(user)s;
    GRANT SELECT ON rschemar.conteudo TO %(user)s;
"""

permissions_admin = """
    GRANT USAGE ON SCHEMA rschemar TO %(user)s;
    GRANT SELECT ON rschemar.conteudo TO %(user)s;
"""

#CREATES
structure = """
CREATE SCHEMA rschemar;

CREATE TABLE rschemar.conteudo
(
  id_conteudo serial NOT NULL,
  id_idioma integer DEFAULT 102,
  titulo character varying NOT NULL,
  publicado boolean NOT NULL DEFAULT false,
  expira_em timestamp without time zone,
  publicado_em timestamp without time zone NOT NULL,
  atualizado_em timestamp without time zone,
  descricao character varying,
  imagem character varying,
  musica character varying, 
  CONSTRAINT conteudo_pkey PRIMARY KEY (id_conteudo)
);

CREATE TABLE rschemar.caracteristicas
(
  id_caracteristica serial NOT NULL,
  nome character varying,
  CONSTRAINT caracteristicas_pkey PRIMARY KEY (id_caracteristica)
);

CREATE TABLE rschemar.caracteristica_conteudo
(
  id_caracteristica bigint,
  id_conteudo bigint,
  CONSTRAINT cara FOREIGN KEY (id_caracteristica)
      REFERENCES rschemar.caracteristicas (id_caracteristica) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT conteudo FOREIGN KEY (id_conteudo)
      REFERENCES rschemar.conteudo (id_conteudo) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE rschemar.destaque(
    id_destaque serial NOT NULL,
    id_conteudo integer NOT NULL,
    titulo character varying,
    descricao character varying,
    img character varying,
    CONSTRAINT destaque_pkey PRIMARY KEY (id_destaque),
    CONSTRAINT destaque_id_conteudo_fkey FOREIGN KEY (id_conteudo)
        REFERENCES rschemar.conteudo(id_conteudo) MATCH SIMPLE
        ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE INDEX rschemar_conteudo_id_conteudo_index ON rschemar.conteudo USING btree (id_conteudo);
CREATE INDEX rschemar_destaque_id_destaque_index ON rschemar.destaque USING btree (id_destaque);
CREATE INDEX fki_cara ON rschemar.caracteristica_conteudo USING btree (id_caracteristica);
CREATE INDEX fki_conteudo ON rschemar.caracteristica_conteudo USING btree (id_conteudo);

INSERT INTO rschemar.caracteristicas (nome) VALUES ('Inovador');
INSERT INTO rschemar.caracteristicas (nome) VALUES ('Acomodado(a)');
INSERT INTO rschemar.caracteristicas (nome) VALUES ('Adaptável');
INSERT INTO rschemar.caracteristicas (nome) VALUES ('Afetivo');
INSERT INTO rschemar.caracteristicas (nome) VALUES ('Ágil');
INSERT INTO rschemar.caracteristicas (nome) VALUES ('Inocente'); 
INSERT INTO rschemar.caracteristicas (nome) VALUES ('Agressivo');
INSERT INTO rschemar.caracteristicas (nome) VALUES ('Inteligente');
INSERT INTO rschemar.caracteristicas (nome) VALUES ('Alto astral');
INSERT INTO rschemar.caracteristicas (nome) VALUES ('Compenetrado');
INSERT INTO rschemar.caracteristicas (nome) VALUES ('Louco');
"""


