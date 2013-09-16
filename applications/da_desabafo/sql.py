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
select_nextval_conteudo = """
    SELECT NEXTVAL
        ('rschemar.conteudo_id_conteudo_seq'::text) as id
"""

select_status_content = """
    SELECT 
        publicado 
    FROM rschemar.conteudo 
        WHERE id_conteudo=%(id_conteudo)i
"""

select_dados = """
    SELECT 
        N.id_conteudo,
        N.titulo,        
        N.nome,
        N.descricao, 
        to_char(N.expira_em, 'YYYY-MM-DD HH24:MI') as expira_em, 
        to_char(N.publicado_em, 'YYYY-MM-DD HH24:MI') as publicado_em, N.publicado, 
        to_char(N.atualizado_em, 'YYYY-MM-DD HH24:MI') as atualizado_em, 
        D.id_destaque, D.titulo as titulo_destaque, D.descricao as descricao_destaque, 
        D.img, D.img as imagem_destaque, D.peso as peso_destaque 
    FROM rschemar.conteudo N 
        LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo) 
        WHERE N.id_conteudo=%(id_conteudo)i
"""

select_titulo = """
    SELECT 
        titulo
    FROM rschemar.conteudo 
        WHERE id_conteudo=%(id_conteudo)i
"""

select_dublin_core = """
    SELECT 
        titulo, descricao, 
        to_char(atualizado_em, 'YYYY-MM-DD HH24:MI:SS') as atualizado_em, 
        to_char(publicado_em, 'YYYY-MM-DD HH24:MI:SS') as publicado_em 
    FROM rschemar.conteudo 
        WHERE id_conteudo=%(id_conteudo)i
"""

select_conteudo = """
    SELECT 
        N.id_conteudo, N.titulo, N.nome, N.descricao,  
        to_char(N.expira_em, 'DD/MM/YYYY HH24:MI') as expira_em, 
        to_char(N.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em, N.publicado, 
        D.id_destaque, D.titulo as titulo_destaque, D.descricao as descricao_destaque, 
        D.img, D.img as imagem_destaque, D.peso as peso_destaque 
    FROM rschemar.conteudo N 
        LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo) 
        WHERE N.id_conteudo=%(id_conteudo)i
"""

select_desabafo_limit = """
   SELECT 
        N.id_conteudo,
        N.titulo,        
        N.nome,
        N.descricao, 
        to_char(N.expira_em, 'YYYY-MM-DD HH24:MI') as expira_em, 
        to_char(N.publicado_em, 'YYYY-MM-DD HH24:MI') as publicado_em, N.publicado, 
        to_char(N.atualizado_em, 'YYYY-MM-DD HH24:MI') as atualizado_em         
    FROM rschemar.conteudo N 
        LIMIT  %(limit)i 
        OFFSET %(offset)i
"""

select_count_for_paginator = """
    SELECT COUNT(*) FROM rschemar.conteudo;
"""


insert_conteudo = """
    INSERT INTO
        rschemar.conteudo (id_conteudo, nome, titulo, descricao,
        publicado_em, expira_em, publicado) 
    VALUES (%(id_conteudo)i, %(nome)s, %(titulo)s, %(descricao)s, %(publicado_em)s, %(expira_em)s, %(publicado)s)
"""

insert_destaque  = """
    INSERT INTO 
        rschemar.destaque (id_conteudo, titulo, descricao, img, peso)
    VALUES (%(id_conteudo)i, %(titulo)s, %(descricao)s, %(img)s, %(peso)i)"""

update_conteudo = """
    UPDATE 
        rschemar.conteudo SET titulo=%(titulo)s, nome=%(nome)s,
        descricao=%(descricao)s, publicado_em=%(publicado_em)s, 
        expira_em=%(expira_em)s, publicado=%(publicado)s 
    WHERE id_conteudo=%(id_conteudo)i
"""

delete_conteudo = """
    DELETE FROM 
        rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i
"""

delete_destaque = """
    DELETE FROM 
        rschemar.destaque  
    WHERE id_conteudo=%(id_conteudo)i
"""

permissions = """
    GRANT USAGE ON SCHEMA rschemar TO %(user)s;
    GRANT SELECT ON rschemar.conteudo TO %(user)s;
    GRANT SELECT ON rschemar.destaque TO %(user)s;
"""

permissions_admin = permissions

structure = """
  CREATE SCHEMA rschemar;

  CREATE TABLE rschemar.conteudo (
    id_conteudo SERIAL NOT NULL,
    id_idioma INTEGER DEFAULT 102,
    titulo VARCHAR NOT NULL,
    nome VARCHAR NOT NULL,    
    descricao VARCHAR NULL,
    arquivo VARCHAR,
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
"""
