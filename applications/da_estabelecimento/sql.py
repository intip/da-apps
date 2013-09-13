# -*- encoding: LATIN1 -*-
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
#SELECT id_filial, id_conteudo, endereco FROM rschemar.filiais 
select_filiais = """
    SELECT * FROM rschemar.filiais 
    WHERE id_conteudo = %(id_conteudo)i
"""

select_filial = """
    SELECT * FROM rschemar.filiais WHERE id_filial = %(id_filial)i
"""

select_status_content = """
    SELECT publicado FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i
"""

select_titulo = """
    SELECT titulo FROM rschemar.conteudo 
    WHERE id_conteudo=%(id_conteudo)i
"""

select_tipo = """
    SELECT tipo FROM rschemar.conteudo 
    WHERE id_conteudo=%(id_conteudo)i
"""

select_tipos = """
    SELECT tipo, id_tipo FROM rschemar.tipo 
    ORDER BY tipo 
"""

select_tipo_conteudo = """
    SELECT id_tipo, nome FROM rschemar.tipo_conteudo 
    WHERE id_conteudo=%(id_conteudo)i
"""

select_nome_tipo = """
    SELECT tipo FROM rschemar.tipo 
    WHERE id_tipo=%(id_tipo)i
"""

select_dublin_core = """
    SELECT titulo, descricao, 
    to_char(atualizado_em, 'YYYY-MM-DD HH24:MI:SS') as atualizado_em, 
    to_char(publicado_em, 'YYYY-MM-DD HH24:MI:SS') as publicado_em 
    FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i
"""

select_kml_regiao = """
    SELECT id_filial, id_conteudo, lat, lng, htmlbalao
    FROM rschemar.filiais WHERE regiao=%(regiao)s
"""

select_tipos_lista = """
    SELECT id_tipo FROM rschemar.tipo_conteudo 
    WHERE id_conteudo=%(id_conteudo)i
"""


select_filiado_t = """
    SELECT filiado, titulo FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)s
"""

select_regioes = """
    SELECT nome FROM rschemar.regioes ORDER BY nome
"""

select_conteudo_dados = """SELECT N.id_conteudo, N.titulo, N.descricao, 
to_char(N.expira_em, 'YYYY-MM-DD HH24:MI') as expira_em, N.imagem, N.filiado,
to_char(N.publicado_em, 'YYYY-MM-DD HH24:MI') as publicado_em, N.publicado, 
D.id_destaque, D.titulo as titulo_destaque, D.descricao as descricao_destaque, 
D.img as imagem_destaque FROM rschemar.conteudo N 
LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo) 
WHERE N.id_conteudo=%(id_conteudo)i"""

select_primeira_filial = """
    SELECT * FROM rschemar.filiais WHERE id_conteudo=%(id_conteudo)s 
    ORDER BY id_filial LIMIT 1
"""

select_busca_completa = """
    SELECT * 
    FROM rschemar.filiais F, rschemar.conteudo C, rschemar.tipo_conteudo T 
    WHERE F.regiao = %(regiao)s AND F.id_conteudo = C.id_conteudo 
    AND T.id_tipo = %(categoria)s AND F.id_conteudo = T.id_conteudo 
"""

select_busca_regiao = """
    SELECT * 
    FROM rschemar.filiais F, rschemar.conteudo C, rschemar.tipo_conteudo T 
    WHERE F.regiao = %(regiao)s AND F.id_conteudo = C.id_conteudo 
    AND F.id_conteudo = T.id_conteudo
"""

select_busca_categoria = """
    SELECT * 
    FROM rschemar.filiais F, rschemar.conteudo C, rschemar.tipo_conteudo T 
    WHERE T.id_tipo = %(categoria)s AND T.id_conteudo = C.id_conteudo 
    AND T.id_conteudo = F.id_conteudo 
"""

select_busca = """
    SELECT * 
    FROM rschemar.filiais F, rschemar.conteudo C, rschemar.tipo_conteudo T 
    WHERE T.id_conteudo = C.id_conteudo AND F.id_conteudo = C.id_conteudo
    AND T.id_conteudo = F.id_conteudo
"""

#INSERTS
insert_conteudo_ = """
    INSERT INTO rschemar.conteudo (id_conteudo, titulo, filiado, descricao, 
    informacoes, imagem, publicado, publicado_em, expira_em) VALUES 
    (%(id_conteudo)i, %(titulo)s, %(filiado)s, %(descricao)s, %(informacoes)s,
     %(imagem)s, %(publicado)s, %(publicado_em)s, %(expira_em)s)
"""

insert_destaque = """
    INSERT INTO rschemar.destaque (id_conteudo, titulo, descricao, img) VALUES 
    (%(id_conteudo)i, %(titulo)s, %(descricao)s, %(img)s)
"""

insert_filial = """
    INSERT INTO rschemar.filiais (id_conteudo, endereco, site, telefone, 
    capacidade, forma_pagamento, acesso_cadeirante, observacoes, regiao, lat,
    lng, rua, numero, complemento, bairro, cep, cidade, estado) 
    VALUES (%(id_conteudo)i, %(endereco)s, %(site)s, %(telefone)s, 
    %(capacidade)s, %(forma_pagamento)s, %(acesso_cadeirante)s, %(observacoes)s,
    %(regiao)s, %(lat)s, %(lng)s, %(rua)s, %(numero)s, %(complemento)s, 
    %(bairro)s, %(cep)s, %(cidade)s, %(estado)s)
"""

insert_tipo = """
    INSERT INTO rschemar.tipo (tipo) VALUES 
    (%(tipo)s) 
"""

insert_tipo_conteudo = """
    INSERT INTO rschemar.tipo_conteudo (id_conteudo, id_tipo, nome) VALUES 
    (%(id_conteudo)i, %(id_tipo)i, %(nome)s)
"""

insert_regiao = """
    INSERT INTO rschemar.regioes (nome) VALUES (%(regiao)s)
"""

#UPDATES
update_conteudo = """
    UPDATE rschemar.conteudo SET titulo=%(titulo)s, filiado=%(filiado)s, 
    descricao=%(descricao)s, informacoes=%(informacoes)s, imagem=%(imagem)s,
    publicado_em=%(publicado_em)s, expira_em=%(expira_em)s 
    WHERE id_conteudo = %(id_conteudo)i
"""

update_destaque = """
    UPDATE rschemar.destaque SET titulo=%(titulo)s, descricao=%(descricao)s,
    img=%(img)s WHERE id_destaque=%(id_destaque)i"
"""

update_filial = """
    UPDATE rschemar.filiais SET endereco=%(endereco)s, site=%(site)s, 
    telefone=%(telefone)s, capacidade=%(capacidade)i, regiao=%(regiao)s,
    forma_pagamento=%(forma_pagamento)s, acesso_cadeirante=%(acesso_cadeirante)s,
    observacoes=%(observacoes)s, lat=%(lat)f, lng=%(lng)f, 
    htmlbalao=%(htmlbalao)s, rua=%(rua)s, icone=%(icone)s, 
    numero = %(numero)s, complemento=%(complemento)s, bairro=%(bairro)s, 
    cep=%(cep)s, cidade=%(cidade)s, estado=%(estado)s
    WHERE id_filial=%(id_filial)i
"""

#DELETES
delete_conteudo_ = """
    DELETE FROM rschemar.conteudo WHERE id_conteudo = %(id_conteudo)i
"""

delete_filial = """
    DELETE FROM rschemar.filiais WHERE id_filial=%(id_filial)i
"""

delete_tipo_conteudo = """
    DELETE FROM rschemar.tipo_conteudo WHERE id_conteudo=%(id_conteudo)i
"""

delete_filiais = """
    DELETE FROM rschemar.filiais WHERE id_conteudo=%(id_conteudo)i
"""

delete_tipo = """
    DELETE FROM rschemar.tipo WHERE tipo=%(tipo)s
"""

delete_regiao = """
    DELETE FROM rschemar.regioes WHERE nome=%(regiao)s
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

#TODO: indexes??
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
  promocoes character varying,
  filiais character varying,
  informacoes character varying,
  filiado boolean,
  tipo integer[],
  CONSTRAINT conteudo_pkey PRIMARY KEY (id_conteudo)
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
        ON UPDATE CASCADE ON DELETE CASCADE);
        

CREATE TABLE rschemar.filiais
(
  id_filial serial NOT NULL,
  id_conteudo integer NOT NULL,
  endereco character varying,
  site character varying,
  telefone character varying,
  capacidade integer,
  forma_pagamento character varying,
  acesso_cadeirante boolean,
  observacoes character varying,
  regiao character varying,
  lat double precision,
  lng double precision,
  htmlbalao character varying,
  rua character varying,
  numero character varying,
  complemento character varying,
  cep character varying,
  cidade character varying,
  estado character varying,
  bairro character varying,
  icone character varying,
  CONSTRAINT infos_pkey PRIMARY KEY (id_filial),
  CONSTRAINT estabelecimento_id_conteudo_fkey FOREIGN KEY (id_conteudo)
      REFERENCES rschemar.conteudo (id_conteudo) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE rschemar.regiao_filial
(
  id_filial integer,
  id_regiao integer,
  CONSTRAINT regiao_conteudo_id_conteudo_fkey FOREIGN KEY (id_filial)
      REFERENCES rschemar.conteudo (id_conteudo) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE rschemar.regioes
(
  id serial NOT NULL ,
  nome character varying,
  CONSTRAINT regioes_pkey PRIMARY KEY (id)
);

CREATE TABLE rschemar.tipo
(
  tipo character varying,
  id_tipo serial NOT NULL,
  CONSTRAINT id_tipo_pkey PRIMARY KEY (id_tipo)
);

CREATE TABLE rschemar.tipo_conteudo
(
  id_tipo integer,
  id_conteudo integer,
  nome character varying,
  CONSTRAINT id_conteudo FOREIGN KEY (id_conteudo)
      REFERENCES rschemar.conteudo (id_conteudo) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT tipo_conteudo_id_tipo_fkey FOREIGN KEY (id_tipo)
      REFERENCES rschemar.tipo (id_tipo) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE INDEX rschemar_conteudo_id_conteudo_index ON rschemar.conteudo USING btree (id_conteudo);
CREATE INDEX rschemar_destaque_id_destaque_index ON rschemar.destaque USING btree (id_destaque);
CREATE INDEX rschemar_filiais_id_filial_index ON rschemar.filiais USING btree (id_filial);
CREATE INDEX rschemar_regioes_id_index ON rschemar.regioes USING btree (id);
CREATE INDEX rschemar_tipo_id_tipo_index ON rschemar.tipo USING btree (id_tipo);
"""


