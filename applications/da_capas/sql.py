# -*- encoding: iso8859-1 -*-
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
select_status_content    = ("SELECT publicado FROM rschemar.conteudo "
                            "WHERE id_conteudo=%(id_conteudo)i")

select_nextval_conteudo  = ("SELECT NEXTVAL('rschemar.conteudo_id_conteudo_seq'::text) as id")

select_titulo            = ("SELECT titulo FROM rschemar.conteudo WHERE "
                            "id_conteudo=%(id_conteudo)i")

select_dublic_core       = ("SELECT titulo, "
                            "to_char(atualizado_em, 'YYYY-MM-DD HH24:MI:SS') as atualizado_em, "
                            "to_char(publicado_em, 'YYYY-MM-DD HH24:MI:SS') as publicado_em "
                            "FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

select_conteudo_         = ("SELECT C.titulo, C.imagem_destaque, "
                            "C.publicado, C.imagem_grande, "
                            "to_char(C.publicado_em, 'YYYY-MM-DD HH24:MI') as publicado_em, "
                            "to_char(C.expira_em, 'YYYY-MM-DD HH24:MI') as expira_em, "
                            "to_char(C.atualizado_em, 'YYYY-MM-DD HH24:MI') as atualizado_em, "
                            "D.img as destaque_imagem, D.titulo as destaque_titulo, "
                            "D.descricao as destaque_descricao, D.id_destaque "
                            "FROM rschemar.conteudo C "
                            "LEFT JOIN rschemar.destaque D ON(C.id_conteudo=D.id_conteudo) "
                            "WHERE C.id_conteudo=%(id_conteudo)i")

select_conteudo          = ("SELECT C.id_conteudo, C.titulo, C.imagem_destaque, "
                            "C.publicado, C.imagem_grande, "
                            "to_char(C.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em, "
                            "to_char(C.expira_em, 'DD/MM/YYYY HH24:MI') as expira_em, "
                            "to_char(C.atualizado_em, 'DD/MM/YYYY HH24:MI') as atualizado_em, "
                            "D.img as destaque_imagem, D.titulo as destaque_titulo, "
                            "D.descricao as destaque_descricao, D.id_destaque "
                            "FROM rschemar.conteudo C "
                            "LEFT JOIN rschemar.destaque D ON(C.id_conteudo=D.id_conteudo) "
                            "WHERE C.id_conteudo=%(id_conteudo)i")

select_conteudo2         = ("SELECT C.id_conteudo, C.titulo, C.imagem_destaque, "
                            "C.publicado, C.imagem_grande, "
                            "to_char(C.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em, "
                            "to_char(C.expira_em, 'DD/MM/YYYY HH24:MI') as expira_em, "
                            "to_char(C.atualizado_em, 'DD/MM/YYYY HH24:MI') as atualizado_em, "
                            "D.img as destaque_imagem, D.titulo as destaque_titulo, "
                            "D.descricao as destaque_descricao, D.id_destaque "
                            "FROM rschemar.conteudo C "
                            "LEFT JOIN rschemar.destaque D ON(C.id_conteudo=D.id_conteudo) "
                            "WHERE C.publicado_em <= now() AND C.publicado AND "
                            "(C.expira_em > now() OR C.expira_em IS NULL) "
                            "ORDER BY C.publicado_em DESC LIMIT 1")

select_destaque1         = ("SELECT id_destaque, titulo, imagem, descricao, link, ordem, chapeu, tipo "
                            "FROM rschemar.destaque1 "
                            "WHERE id_conteudo=%(id_conteudo)i ORDER BY ordem ASC")

select_dates             = ("SELECT C.id_conteudo, to_char(C.publicado_em, 'YYYY-MM-DD') as data, "
                            "CC.id_treeapp, CC.url "
                            "FROM rschemar.conteudo C "
                            "INNER JOIN envsite.conteudo CC ON(C.id_conteudo=CC.id_conteudo) "
                            "WHERE CC.id_aplicativo=(SELECT id_aplicativo FROM envsite.aplicativo WHERE schema=%(schema)s) "
                            "AND C.publicado_em <= now() AND C.publicado AND (C.expira_em > now() OR C.expira_em IS NULL) "
                            "ORDER BY C.publicado_em DESC")

select_tipos = """
    SELECT * FROM rschemar.tipos
"""

insert_conteudo          = ("INSERT INTO rschemar.conteudo (id_conteudo, titulo, "
                            " imagem_destaque, imagem_grande, "
                            " publicado, "
                            "publicado_em, expira_em) VALUES "
                            "(%(id_conteudo)i, %(titulo)s, "
                            "%(imagem)s, %(imagem_grande)s, "
                            "%(publicado)s, %(publicado_em)s, %(expira_em)s)")

insert_destaque          = ("INSERT INTO rschemar.destaque (id_conteudo, titulo, "
                            "descricao, img) VALUES (%(id_conteudo)i, "
                            "%(titulo)s, %(descricao)s, %(imagem)s)")

insert_destaque1         = ("INSERT INTO rschemar.destaque1 (id_conteudo, titulo, "
                            "descricao, link, imagem, ordem, chapeu, tipo) VALUES "
                            "(%(id_conteudo)i, %(titulo)s, %(descricao)s, "
                            "%(link)s, %(imagem)s, %(ordem)i, %(chapeu)s, %(tipo)s)")

insert_destaque2         = ("INSERT INTO rschemar.destaque2 (id_conteudo, titulo, "
                            "descricao, link, imagem, ordem) VALUES "
                            "(%(id_conteudo)i, %(titulo)s, %(descricao)s, "
                            "%(link)s, %(imagem)s, %(ordem)i)")

update_conteudo          = ("UPDATE rschemar.conteudo SET titulo=%(titulo)s, "
                            "imagem_destaque=%(imagem)s, imagem_grande=%(imagem_grande)s, "
                            "publicado=%(publicado)s, "
                            "publicado_em=%(publicado_em)s, expira_em=%(expira_em)s "
                            "WHERE id_conteudo=%(id_conteudo)i")

delete_conteudo          = ("DELETE FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

delete_destaque1         = ("DELETE FROM rschemar.destaque1 WHERE id_conteudo=%(id_conteudo)i")

delete_destaque          = ("DELETE FROM rschemar.destaque WHERE id_conteudo=%(id_conteudo)i")


permissions = """
  GRANT USAGE ON SCHEMA rschemar TO %(user)s;
  GRANT SELECT ON rschemar.conteudo TO %(user)s;
  GRANT SELECT ON rschemar.destaque1 TO %(user)s;
  GRANT SELECT ON rschemar.destaque TO %(user)s;
"""

permissions_admin = """
  GRANT USAGE ON SCHEMA rschemar TO %(user)s;
  GRANT SELECT ON rschemar.conteudo TO %(user)s;
  GRANT SELECT ON rschemar.destaque1 TO %(user)s;
  GRANT SELECT ON rschemar.destaque TO %(user)s;
"""

structure = """
  CREATE SCHEMA rschemar;

  CREATE TABLE rschemar.conteudo (
    id_conteudo SERIAL NOT NULL,
    titulo VARCHAR NULL,
    imagem_destaque VARCHAR NULL,
    imagem_grande VARCHAR NULL,
    publicado BOOL NULL DEFAULT False,
    publicado_em TIMESTAMP NULL,
    expira_em TIMESTAMP NULL,
    atualizado_em TIMESTAMP NULL,
    PRIMARY KEY(id_conteudo)
  );

  CREATE TABLE rschemar.destaque1 (
    id_destaque SERIAL NOT NULL,
    id_conteudo INTEGER NOT NULL,
    titulo VARCHAR,
    imagem VARCHAR,
    descricao VARCHAR,
    link VARCHAR,
    chapeu VARCHAR,
    tipo VARCHAR,
    ordem INT NULL DEFAULT 0,
    PRIMARY KEY(id_destaque),
    FOREIGN KEY(id_conteudo)
      REFERENCES rschemar.conteudo(id_conteudo)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );
  CREATE INDEX rschemar_destaque1_id_conteudo_index ON rschemar.destaque1 USING btree (id_conteudo);

  CREATE TABLE rschemar.tipos (
    id_tipo SERIAL NOT NULL,
    nome VARCHAR NOT NULL
  );
  INSERT INTO rschemar.tipos (id_tipo, nome) VALUES (1, 'Principal'), 
    (2, 'Destaque'), (3, 'Lista1'), (4, 'Lista2'), (5, 'Complementar');

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
