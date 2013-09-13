# coding: utf-8
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
select_status_content = ("SELECT publicado FROM rschemar.conteudo "
"WHERE id_conteudo=%(id_conteudo)i")

select_nextval_conteudo = ("SELECT NEXTVAL('rschemar.conteudo_"
"id_conteudo_seq'::text) as id")

select_titulo = ("SELECT titulo FROM rschemar.conteudo WHERE "
"id_conteudo=%(id_conteudo)i")

select_dublic_core = ("SELECT titulo, descricao, "
"to_char(atualizado_em, 'YYYY-MM-DD HH24:MI:SS') as atualizado_em, "
"to_char(publicado_em, 'YYYY-MM-DD HH24:MI:SS') as publicado_em "
"FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

select_conteudo = ("SELECT C.titulo, C.codigo_fipe, "
"C.ordem, C.publicado, C.fabricante, C.modelo, "
"C.modelo_extendido, C.ano_modelo, C.ano_fabricacao, "
"C.aval_design, C.aval_performance, C.aval_conforto_acabamento,"
"C.aval_dirigibilidade, C.aval_consumo, C.aval_manutencao, "
"C.aval_custo_beneficio,"
"to_char(C.publicado_em, 'YYYY-MM-DD HH24:MI') as publicado_em, "
"to_char(C.expira_em, 'YYYY-MM-DD HH24:MI') as expira_em, "
"to_char(C.atualizado_em, 'YYYY-MM-DD HH24:MI') as atualizado_em, "
"D.img as destaque_imagem, D.titulo as destaque_titulo, "
"D.descricao as destaque_descricao, D.id_destaque "
"FROM rschemar.conteudo C "
"LEFT JOIN rschemar.destaque D ON(C.id_conteudo=D.id_conteudo) "
"WHERE C.id_conteudo=%(id_conteudo)i")

select_ids = ("SELECT id_conteudo from rschemar.conteudo")

select_id_conteudo = ("SELECT id_conteudo "
"FROM rschemar.conteudo "
"WHERE fabricante=%(fabricante)s " 
"AND modelo=%(modelo)s "
"AND modelo_extendido=%(modelo_ext)s "
"AND ano_fabricacao=%(ano_fabricacao)s "
"AND ano_modelo=%(ano_modelo)s")

# C.id_categoria, C.imagem, 
select_conteudo_ = ("SELECT C.titulo, C.codigo_fipe, "
"C.ordem, C.publicado, C.fabricante, C.modelo, "
"C.modelo_extendido, C.ano_modelo, C.ano_fabricacao, "
"C.aval_design, C.aval_performance, C.aval_conforto_acabamento,"
"C.aval_dirigibilidade, C.aval_consumo, C.aval_manutencao, "
"C.aval_custo_beneficio,"
"to_char(C.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em, "
"to_char(C.expira_em, 'DD/MM/YYYY HH24:MI') as expira_em, "
"to_char(C.atualizado_em, 'DD/MM/YYYY HH24:MI') as atualizado_em, "
"D.img as destaque_imagem, D.titulo as destaque_titulo, "
"D.descricao as destaque_descricao, D.id_destaque "
"FROM rschemar.conteudo C "
"LEFT JOIN rschemar.destaque D ON(C.id_conteudo=D.id_conteudo) "
"WHERE C.id_conteudo=%(id_conteudo)i")

# C.id_categoria, 
select_conteudos = ("SELECT C.id_conteudo, "
"C.aval_design, C.aval_performance, C.aval_conforto_acabamento,"
"C.aval_dirigibilidade, C.aval_consumo, C.aval_manutencao, "
"C.aval_custo_beneficio "
"FROM rschemar.conteudo C "
"WHERE C.publicado AND C.publicado_em <= now() AND "
"(C.expira_em > now() OR C.expira_em IS NULL) ")

#select_categorias = ("SELECT id_categoria, titulo FROM rschemar.categoria "
#"ORDER BY titulo")

# R.rank_categoria, C.imagem
select_ranking_geral = ("SELECT C.id_conteudo, C.titulo, C.fabricante, C.modelo, "
"C.codigo_fipe, C.ano_modelo, R.rank_geral "
"FROM rschemar.conteudo C "
"INNER JOIN rschemar.ranking R ON(C.id_conteudo=R.id_conteudo) "
"WHERE C.publicado AND C.publicado_em <= now() AND "
"(C.expira_em > now() OR C.expira_em IS NULL) "
"ORDER BY R.rank_geral ASC LIMIT %(limit)i OFFSET %(offset)i")

#R.rank_categoria C.imagem, 
select_ranking_geral_modelo = ("SELECT C.id_conteudo, C.titulo, C.fabricante, C.modelo, "
"C.codigo_fipe, C.ano_modelo, R.rank_geral "
"FROM rschemar.conteudo C "
"INNER JOIN rschemar.ranking R ON(C.id_conteudo=R.id_conteudo) "
"WHERE C.publicado AND C.publicado_em <= now() AND "
"(C.expira_em > now() OR C.expira_em IS NULL) AND modelo=%(modelo)s "
"ORDER BY R.rank_geral ASC LIMIT %(limit)i OFFSET %(offset)i")

# C.id_categoria, C.imagem,  R.rank_categoria 
select_conteudo_site = ("SELECT C.titulo, "
"C.ordem, C.publicado, C.fabricante, C.modelo, C.codigo_fipe,"
"C.modelo_extendido, C.ano_modelo, C.ano_fabricacao, "
"C.aval_design, C.aval_performance, C.aval_conforto_acabamento, "
"C.aval_dirigibilidade, C.aval_consumo, C.aval_manutencao, "
"C.aval_custo_beneficio,"
"to_char(C.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em, "
"to_char(C.expira_em, 'DD/MM/YYYY HH24:MI') as expira_em, "
"to_char(C.atualizado_em, 'DD/MM/YYYY HH24:MI') as atualizado_em, "
"D.img as destaque_imagem, D.titulo as destaque_titulo, "
"D.descricao as destaque_descricao, D.id_destaque, "
"R.rank_geral "
"FROM rschemar.conteudo C "
"INNER JOIN rschemar.ranking R ON(C.id_conteudo=R.id_conteudo) "
"LEFT JOIN rschemar.destaque D ON(C.id_conteudo=D.id_conteudo) "
"WHERE C.id_conteudo=%(id_conteudo)i")

seleciona_avaliacao_user = ("SELECT id_opiniao FROM rschemar.opiniao WHERE "
"id_conteudo=%(id_conteudo)i AND email=%(email)s")

select_opiniao_desc = ("SELECT id_opiniao, id_conteudo, id_wad, "
"nome, cpf, email, apelido, titulo_opiniao, recomenda, "
"to_char(datahora, 'DD/MM/YYYY HH24:MI') as datahora,"
"pontos_positivos, pontos_negativos, comentario, aval_design, "
"aval_performance, aval_conforto_acabamento, aval_dirigibilidade, "
"aval_consumo, aval_manutencao, aval_custo_beneficio "
"FROM rschemar.opiniao "
"WHERE id_conteudo=%(id_conteudo)i ORDER BY datahora DESC "
"LIMIT %(limit)i OFFSET %(offset)i")

select_opiniao = ("SELECT id_opiniao, id_conteudo, id_wad, "
"nome, cpf, email, apelido, titulo_opiniao, recomenda, "
"to_char(datahora, 'DD/MM/YYYY HH24:MI') as datahora,"
"pontos_positivos, pontos_negativos, comentario, aval_design, "
"aval_performance, aval_conforto_acabamento, aval_dirigibilidade, "
"aval_consumo, aval_manutencao, aval_custo_beneficio, (aval_design+ "
"aval_performance+ aval_conforto_acabamento+ aval_dirigibilidade+ "
"aval_consumo+ aval_manutencao+ aval_custo_beneficio) as geral "
"FROM rschemar.opiniao "
"WHERE id_conteudo=%(id_conteudo)i ORDER BY geral DESC "
"LIMIT %(limit)i OFFSET %(offset)i")

select_opiniao_minor = ("SELECT id_opiniao, id_conteudo, id_wad, "
"nome, cpf, email, apelido, titulo_opiniao, recomenda, "
"to_char(datahora, 'DD/MM/YYYY HH24:MI') as datahora,"
"pontos_positivos, pontos_negativos, comentario, aval_design, "
"aval_performance, aval_conforto_acabamento, aval_dirigibilidade, "
"aval_consumo, aval_manutencao, aval_custo_beneficio, (aval_design+ "
"aval_performance+ aval_conforto_acabamento+ aval_dirigibilidade+ "
"aval_consumo+ aval_manutencao+ aval_custo_beneficio) as geral "
"FROM rschemar.opiniao "
"WHERE id_conteudo=%(id_conteudo)i ORDER BY geral ASC "
"LIMIT %(limit)i OFFSET %(offset)i")

select_opiniao_asc = ("SELECT id_opiniao, id_conteudo, id_wad, "
"nome, cpf, email, apelido, titulo_opiniao, recomenda, "
"to_char(datahora, 'DD/MM/YYYY HH24:MI') as datahora,"
"pontos_positivos, pontos_negativos, comentario, aval_design, "
"aval_performance, aval_conforto_acabamento, aval_dirigibilidade, "
"aval_consumo, aval_manutencao, aval_custo_beneficio "
"FROM rschemar.opiniao "
"WHERE id_conteudo=%(id_conteudo)i ORDER BY datahora ASC "
"LIMIT %(limit)i OFFSET %(offset)i")

select_opiniao_count = ("SELECT count(1) as qtde FROM rschemar.opiniao "
"WHERE id_conteudo=%(id_conteudo)i")

select_opiniao_conteudo = ("SELECT id_conteudo, aval_design, aval_performance, "
"aval_conforto_acabamento, aval_dirigibilidade, aval_consumo, "
"aval_manutencao, aval_custo_beneficio FROM rschemar.conteudo "
"WHERE id_conteudo=(SELECT id_conteudo FROM rschemar.opiniao "
"WHERE id_opiniao=%(id_opiniao)s)")

select_opiniao_simples = ("SELECT comentario, pontos_positivos, pontos_negativos, "
"nome, email, apelido, titulo_opiniao FROM rschemar.opiniao "
"WHERE id_opiniao=%(id_opiniao)s")

# id_categoria,  imagem
insert_conteudo = ("INSERT INTO rschemar.conteudo (id_conteudo, "
"titulo, codigo_fipe, ordem, aval_design, aval_performance, aval_conforto_acabamento,"
"aval_dirigibilidade, aval_consumo, aval_manutencao, aval_custo_beneficio,"
"publicado, publicado_em, expira_em, fabricante, modelo, modelo_extendido,"
" ano_modelo, ano_fabricacao) VALUES "
"(%(id_conteudo)i, %(titulo)s, %(codigo_fipe)s, %(ordem)i, "
"%(aval_design)i, %(aval_performance)i, %(aval_conforto_acabamento)i,"
"%(aval_dirigibilidade)i, %(aval_consumo)i, %(aval_manutencao)i, "
"%(aval_custo_beneficio)i, %(publicado)s, %(publicado_em)s, %(expira_em)s, "
"%(fabricante)s, %(modelo)s, %(modelo_extendido)s, %(ano_modelo)s, %(ano_fabricacao)s)")

insert_destaque = ("INSERT INTO rschemar.destaque (id_conteudo, titulo, "
"descricao, img) VALUES (%(id_conteudo)i, "
"%(titulo)s, %(descricao)s, %(imagem)s)")

# id_categoria,  rank_categoria%(id_categoria)i, %(rank_categoria)i 
insert_ranking = ("INSERT INTO rschemar.ranking (id_conteudo,"
"rank_geral) VALUES (%(id_conteudo)i, "
"%(rank_geral)i)")

insert_user_avaliacao = ("INSERT INTO rschemar.opiniao ("
"id_conteudo, id_wad, nome, cpf, email, apelido, titulo_opiniao, "
"recomenda, pontos_positivos, pontos_negativos, comentario, "
"aval_design, aval_performance, aval_conforto_acabamento, "
"aval_dirigibilidade, aval_consumo, aval_manutencao, aval_custo_beneficio, datahora) VALUES "
"(%(id_conteudo)i, %(id_wad)i, %(nome)s, %(cpf)s, %(email)s, %(apelido)s, %(titulo_opiniao)s,"
"%(recomenda)s, %(pontos_positivos)s, %(pontos_negativos)s, %(comentario)s, "
"%(aval_design)i, %(aval_performance)i, %(aval_conforto_acabamento)i, "
"%(aval_dirigibilidade)i, %(aval_consumo)i, %(aval_manutencao)i, %(aval_custo_beneficio)i, now())")

# id_categoria=%(id_categoria)i, imagem=%(imagem)s, 
update_conteudo = ("UPDATE rschemar.conteudo SET titulo=%(titulo)s, codigo_fipe=%(codigo_fipe)s, " 
"ordem=%(ordem)i, publicado_em=%(publicado_em)s, expira_em=%(expira_em)s, "
"fabricante=%(fabricante)s, modelo=%(modelo)s, modelo_extendido=%(modelo_extendido)s, "
"ano_modelo=%(ano_modelo)s, ano_fabricacao=%(ano_fabricacao)s WHERE id_conteudo=%(id_conteudo)i")

update_conteudo_avaliacao_minus = ("UPDATE rschemar.conteudo SET "
"aval_design=aval_design-%(aval_design)i, "
"aval_performance=aval_performance-%(aval_performance)i, "
"aval_conforto_acabamento=aval_conforto_acabamento-%(aval_conforto_acabamento)i, "
"aval_dirigibilidade=aval_dirigibilidade-%(aval_dirigibilidade)i, "
"aval_consumo=aval_consumo-%(aval_consumo)i, "
"aval_manutencao=aval_manutencao-%(aval_manutencao)i, "
"aval_custo_beneficio=aval_custo_beneficio-%(aval_custo_beneficio)i "
"WHERE id_conteudo=%(id_conteudo)i")

update_conteudo_avaliacao = ("UPDATE rschemar.conteudo SET "
"aval_design=aval_design+%(aval_design)i, "
"aval_performance=aval_performance+%(aval_performance)i, "
"aval_conforto_acabamento=aval_conforto_acabamento+%(aval_conforto_acabamento)i, "
"aval_dirigibilidade=aval_dirigibilidade+%(aval_dirigibilidade)i, "
"aval_consumo=aval_consumo+%(aval_consumo)i, "
"aval_manutencao=aval_manutencao+%(aval_manutencao)i, "
"aval_custo_beneficio=aval_custo_beneficio+%(aval_custo_beneficio)i "
"WHERE id_conteudo=%(id_conteudo)i")

delete_opiniao = ("DELETE FROM rschemar.opiniao WHERE email=%(email)s or cpf=%(cpf)s")

delete_opiniao_id = ("DELETE FROM rschemar.opiniao WHERE id_opiniao=%(id_opiniao)s")

delete_conteudo = ("DELETE FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

delete_destaque = ("DELETE FROM rschemar.destaque WHERE id_conteudo=%(id_conteudo)i")

delete_ranking = ("DELETE FROM rschemar.ranking")

permissions = """
 GRANT USAGE ON SCHEMA rschemar TO %(user)s;
 GRANT SELECT, UPDATE ON rschemar.conteudo TO %(user)s;
 GRANT SELECT ON rschemar.destaque TO %(user)s;
 GRANT SELECT, INSERT ON rschemar.opiniao TO %(user)s;
 GRANT SELECT, INSERT, UPDATE ON rschemar.ranking TO %(user)s;
"""

permissions_admin = """
 GRANT USAGE ON SCHEMA rschemar TO %(user)s;
 GRANT SELECT ON rschemar.conteudo TO %(user)s;
 GRANT SELECT ON rschemar.destaque TO %(user)s;
 GRANT SELECT ON rschemar.opiniao TO %(user)s;
 GRANT SELECT ON rschemar.ranking TO %(user)s;
"""

"""

CREATE TABLE rschemar.categoria (

    id_categoria SERIAL NOT NULL,

    titulo VARCHAR NOT NULL,

    PRIMARY KEY(id_categoria)

  );

  

  INSERT INTO rschemar.categoria (titulo) VALUES ('Hatch');

  INSERT INTO rschemar.categoria (titulo) VALUES ('Sedan');

  INSERT INTO rschemar.categoria (titulo) VALUES ('Convers\EDvel');

  INSERT INTO rschemar.categoria (titulo) VALUES ('Pick-up');

  INSERT INTO rschemar.categoria (titulo) VALUES ('Van');

  INSERT INTO rschemar.categoria (titulo) VALUES ('Esportivo');


c
id_categoria INT NOT NULL,
imagem VARCHAR NOT NULL,
,
    FOREIGN KEY(id_categoria)
      REFERENCES rschemar.categoria(id_categoria)
        ON DELETE CASCADE
        ON UPDATE CASCADE
r
rank_categoria INT NOT NULL,
id_categoria INT NOT NULL,
,
    FOREIGN KEY(id_categoria)
      REFERENCES rschemar.categoria(id_categoria)
        ON DELETE CASCADE
        ON UPDATE CASCADE

indexes
CREATE INDEX rschemar_ranking_id_categoria_index ON rschemar.ranking USING btree (id_categoria);
CREATE INDEX rschemar_ranking_categoria_index ON rschemar.ranking USING btree (rank_categoria);
"""

structure = """
  CREATE SCHEMA rschemar;

  CREATE TABLE rschemar.conteudo (
    id_conteudo SERIAL NOT NULL,
    titulo VARCHAR NULL,
    codigo_fipe VARCHAR NOT NULL,
    fabricante VARCHAR NOT NULL,
    modelo VARCHAR NOT NULL,
    modelo_extendido VARCHAR NOT NULL,
    ano_modelo VARCHAR NOT NULL,
    ano_fabricacao VARCHAR NOT NULL,
    ordem INT NOT NULL,
    
    aval_design FLOAT NOT NULL,
    aval_performance FLOAT NOT NULL,
    aval_conforto_acabamento FLOAT NOT NULL,
    aval_dirigibilidade FLOAT NOT NULL,
    aval_consumo FLOAT NOT NULL,
    aval_manutencao FLOAT NOT NULL,
    aval_custo_beneficio FLOAT NOT NULL,

    publicado BOOL NULL DEFAULT False,
    publicado_em TIMESTAMP NULL,
    expira_em TIMESTAMP NULL,
    atualizado_em TIMESTAMP NULL,
    PRIMARY KEY(id_conteudo)

  );
  CREATE INDEX rschemar_conteudo_fabricante_index ON rschemar.conteudo USING btree (fabricante);
  CREATE INDEX rschemar_conteudo_modelo_index ON rschemar.conteudo USING btree (modelo);

  CREATE TABLE rschemar.opiniao (
    id_opiniao SERIAL NOT NULL,
    id_conteudo INT NOT NULL,
    id_wad INT NOT NULL,
    nome VARCHAR NOT NULL,
    cpf VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    apelido VARCHAR NOT NULL,
    titulo_opiniao VARCHAR NOT NULL,
    recomenda BOOLEAN NOT NULL,
    pontos_positivos VARCHAR NOT NULL,
    pontos_negativos VARCHAR NOT NULL,
    comentario VARCHAR NOT NULL,
    aval_design FLOAT NOT NULL,
    aval_performance FLOAT NOT NULL,
    aval_conforto_acabamento FLOAT NOT NULL,
    aval_dirigibilidade FLOAT NOT NULL,
    aval_consumo FLOAT NOT NULL,
    aval_manutencao FLOAT NOT NULL,
    aval_custo_beneficio FLOAT NOT NULL,
    datahora TIMESTAMP,
    PRIMARY KEY(id_opiniao),
    FOREIGN KEY(id_conteudo)
      REFERENCES rschemar.conteudo(id_conteudo)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );
  CREATE INDEX rschemar_opiniao_id_conteudo_index ON rschemar.opiniao USING btree (id_conteudo);

  CREATE TABLE rschemar.ranking (
    id_conteudo INT NOT NULL,
    rank_geral INT NOT NULL,
    FOREIGN KEY(id_conteudo)
      REFERENCES rschemar.conteudo(id_conteudo)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );
  CREATE INDEX rschemar_ranking_id_conteudo_index ON rschemar.ranking USING btree (id_conteudo);
  CREATE INDEX rschemar_ranking_geral_index ON rschemar.ranking USING btree (rank_geral);

  CREATE TABLE rschemar.destaque (
    id_destaque SERIAL NOT NULL,
    id_conteudo INTEGER NOT NULL,
    titulo VARCHAR NULL,
    descricao VARCHAR NULL,
    img VARCHAR NULL,
    PRIMARY KEY(id_destaque),
    FOREIGN KEY(id_conteudo)
      REFERENCES rschemar.conteudo(id_conteudo)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );
  CREATE INDEX rschemar_destaque_id_destaque_index ON rschemar.destaque USING btree (id_destaque);
"""
