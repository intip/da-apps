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
select_nextval_conteudo     = "SELECT NEXTVAL('rschemar.conteudo_id_conteudo_seq'::text) as id"

select_menu                 = ("SELECT id_conteudo, titulo, json FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

select_conteudo            = ("SELECT C.id_conteudo, C.titulo, C.publicado, C.publicado_em, "
                              "C.expira_em, '' as titulo_destaque, '' as descricao_destaque, "
                              "'' as imagem_destaque "
                              "FROM rschemar.conteudo C ORDER BY C.id_conteudo")

insert_conteudo             = ("INSERT INTO rschemar.conteudo (id_conteudo, titulo, json) VALUES ( "
                               "%(id_conteudo)i, %(titulo)s, %(json)s)")

update_menu                 = ("UPDATE rschemar.conteudo SET titulo=%(titulo)s, json=%(json)s "
                               "WHERE id_conteudo=%(id_conteudo)i")

delete_menu                 = "DELETE FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i"

permissions = """
  GRANT USAGE ON SCHEMA rschemar TO %(user)s;
  GRANT SELECT ON rschemar.conteudo TO %(user)s;
"""

permissions_admin = permissions

structure = """
  CREATE SCHEMA rschemar;

  CREATE TABLE rschemar.conteudo (
    id_conteudo SERIAL NOT NULL,
    titulo VARCHAR NULL,
    descricao VARCHAR NULL,
    json VARCHAR NOT NULL,
    publicado_em TIMESTAMP DEFAULT now(),
    expira_em TIMESTAMP DEFAULT NULL,
    publicado BOOL DEFAULT True,
    PRIMARY KEY(id_conteudo)
  );
"""
