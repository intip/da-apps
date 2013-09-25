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
select_nextval_conteudo  = ("SELECT nextval('rschemar.conteudo_id_conteudo_seq') as id")

select_status_content    = ("SELECT publicado FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

select_titulo            = ("SELECT titulo FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

select_sea               = ("SELECT id_conteudo FROM rschemar.conteudo WHERE sea_id=%(sea_id)i")

select_conteudo          = ("SELECT C.id_conteudo, C.titulo, C.descricao, C.publicado, "
                            "to_char(C.publicado_em, 'YYYY-MM-DD HH24:MI') as publicado_em, "
                            "C.sea_id, C.embed, C.thumb, C.tags, "
                            "to_char(C.expira_em, 'YYYY-MM-DD HH24:MI') as expira_em, D.titulo as titulo_destaque, "
                            "D.descricao as descricao_destaque, "
                            "D.img as imagem_destaque "
                            "FROM rschemar.conteudo C "
                            "LEFT JOIN rschemar.destaque D ON(C.id_conteudo=D.id_conteudo) "
                            "ORDER BY C.id_conteudo")

select_conteudo_id       = ("SELECT C.id_conteudo, C.sea_id, C.titulo, C.descricao, C.publicado, " 
                            "to_char(C.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em, "
                            "C.sea_id, C.embed, C.thumb, C.tags, "
                            "C.expira_em, D.id_destaque, D.titulo as titulo_destaque, " 
                            "D.descricao as descricao_destaque, D.peso as peso_destaque, "
                            "D.img as imagem_destaque "
                            "FROM rschemar.conteudo C "
                            "LEFT JOIN rschemar.destaque D ON(C.id_conteudo=D.id_conteudo) "
                            "WHERE C.id_conteudo=%(id_conteudo)i")  

select_destaque_video    = ("SELECT id_destaque, titulo, descricao, peso, img "
                            "FROM rschemar.destaque WHERE id_conteudo=%(id_conteudo)s")

select_videos_count      = ("SELECT count(*) as qtde FROM rschemar.conteudo "
                            "WHERE tags ~* %(tag)s ")

select_count_videos     = ("SELECT count(*) as qtde FROM rschemar.conteudo")

select_videos            = ("SELECT id_conteudo, id_conteudo as id_video, sea_id, "
                            "titulo, descricao, embed, thumb "
                            "FROM rschemar.conteudo "
                            "WHERE tags ~* %(tag)s ")
 
select_video             = ("SELECT id_conteudo, id_conteudo as id_video, sea_id, "
                            "titulo, descricao, embed, thumb "
                            "FROM rschemar.conteudo " 
                            "WHERE sea_id = %(sea_id)i ")

select_video_by_id       = ("SELECT id_conteudo, sea_id, titulo, descricao, embed, thumb "
                            "FROM rschemar.conteudo WHERE id_conteudo= %(id_conteudo)i") 

insert_videos            = ("INSERT INTO rschemar.conteudo (id_conteudo, titulo, descricao, embed, thumb, tags, sea_id, publicado_em, publicado) "
                            "VALUES (%(id_conteudo)i, %(titulo)s, %(descricao)s, %(embed)s, %(thumb)s, %(tags)s, %(sea_id)i, %(publicado_em)s, True)")

insert_destaque          = ("INSERT INTO rschemar.destaque (id_conteudo, titulo, descricao, img, peso) "
                            "VALUES (%(id_conteudo)i, %(titulo)s, %(descricao)s, %(img)s, %(peso)s)")

update_conteudo          = ("UPDATE rschemar.conteudo SET titulo=%(titulo)s, descricao=%(descricao)s, sea_id=%(sea_id)s, "
                            "embed=%(embed)s, thumb=%(thumb)s, tags=%(tags)s, publicado=%(publicado)s, expira_em=%(expira_em)s, "
                            "publicado_em=%(publicado_em)s, atualizado_em=%(atualizado_em)s, data_edicao=%(data_edicao)s, "
                            "exportado=%(exportado)s WHERE id_conteudo=%(id_conteudo)i")

delete_video             = ("DELETE FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

delete_videos            = ("DELETE FROM rschemar.conteudo; "
                            "SELECT setval('rschemar.conteudo_id_conteudo_seq', 1);")

delete_destaque          = ("DELETE FROM rschemar.destaque WHERE id_conteudo=%(id_conteudo)i")

create_rule              = ("CREATE OR REPLACE RULE rschemar_seac AS ON INSERT TO rschemar.conteudo "
                            "WHERE new.sea_id = (SELECT sea_id FROM rschemar.conteudo "
                            "WHERE sea_id=new.sea_id LIMIT 1)"
                            "DO INSTEAD UPDATE rschemar.conteudo SET titulo=new.titulo, "
                            "descricao=new.descricao, embed=new.embed, "
                            "thumb=new.thumb, tags=new.tags WHERE sea_id=new.sea_id;")

permissions = """
  GRANT USAGE ON SCHEMA rschemar TO %(user)s;
  GRANT SELECT ON rschemar.conteudo TO %(user)s;
  GRANT SELECT ON rschemar.destaque TO %(user)s;
"""

permissions_admin = """
  GRANT USAGE ON SCHEMA rschemar TO %(user)s;
  GRANT SELECT, UPDATE, INSERT, DELETE ON rschemar.conteudo TO %(user)s;
  GRANT SELECT, UPDATE ON TABLE rschemar.conteudo_id_conteudo_seq TO publica_export;
"""

structure = """
  CREATE SCHEMA rschemar;

  CREATE TABLE rschemar.conteudo (
    id_conteudo SERIAL NOT NULL,
    titulo VARCHAR NOT NULL,
    descricao VARCHAR,
    -- custom fields
    sea_id BIGINT NOT NULL,
    embed VARCHAR,
    thumb VARCHAR,
    tags VARCHAR,
    --   
    publicado BOOL NOT NULL DEFAULT 'False',
    expira_em TIMESTAMP NULL,
    publicado_em TIMESTAMP NOT NULL,
    atualizado_em TIMESTAMP NULL,
    data_edicao DATE NULL,
    exportado BOOLEAN DEFAULT 'False',
    PRIMARY KEY(id_conteudo)
  );
  CREATE INDEX rschemar_conteudo_sea_id_index ON rschemar.conteudo USING btree (sea_id);

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

  CREATE OR REPLACE RULE rschemar_seac AS ON INSERT TO rschemar.conteudo 
  WHERE new.sea_id = (SELECT sea_id FROM rschemar.conteudo 
  WHERE sea_id=new.sea_id LIMIT 1)
  DO INSTEAD UPDATE rschemar.conteudo SET titulo=new.titulo, 
  descricao=new.descricao, embed=new.embed, 
  thumb=new.thumb, tags=new.tags WHERE sea_id=new.sea_id;

--  CREATE TABLE rschemar.video (
--    id_video SERIAL NOT NULL,
--    sea_id BIGINT NOT NULL,
--    titulo VARCHAR,
--    descricao VARCHAR,
--    embed VARCHAR,
--    thumb VARCHAR,
--    tags VARCHAR,
--    PRIMARY KEY(id_video)
--  );
--  CREATE INDEX index_rschemar_video_sea_id ON rschemar.video USING btree (sea_id);
--  CREATE RULE rschemar_sea AS ON INSERT TO rschemar.video 
--  WHERE new.sea_id = (SELECT sea_id FROM rschemar.video WHERE sea_id=new.sea_id LIMIT 1)
--  DO INSTEAD nothing;

"""
