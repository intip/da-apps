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

select_dublin_core = ("SELECT titulo, descricao, "
"to_char(atualizado_em, 'YYYY-MM-DD HH24:MI:SS') as atualizado_em, "
"to_char(publicado_em, 'YYYY-MM-DD HH24:MI:SS') as publicado_em "
"FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

select_categoria = ("SELECT id_categoria, nome FROM rschemar.categoria ORDER BY nome")

select_regiao = ("SELECT id_regiao, nome FROM rschemar.regiao ORDER BY nome")

select_categoria_estabelecimento=("SELECT C.id_categoria, C.nome FROM rschemar.categoria C JOIN rschemar.estabelecimento_categoria B "
                      "ON (C.id_categoria=B.id_categoria) AND B.id_conteudo=%(id_conteudo)i")

select_regiao_estabelecimento=("SELECT id_regiao, nome FROM rschemar.regiao WHERE id_regiao=%(id_regiao)s")

select_conteudo = ("SELECT N.id_conteudo, N.titulo, N.pagamento, N.descricao, N.observacao,  "
"to_char(N.expira_em, 'DD/MM/YYYY HH24:MI') as expira_em, "
"to_char(N.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em, N.endereco, N.publicado,"
"N.img, N.credito, N.editor, N.id_regiao, N.telefone, N.telefonec, N.site,"
"N.estado, N.rua, N.num, N.bairro, N.cep, N.capacidade, N.cadeirantes, N.lat, N.lng, N.cidade, "
"D.id_destaque, D.titulo as titulo_destaque, D.descricao as descricao_destaque, "
"D.img as imagem_destaque, D.peso as peso_destaque "
"FROM rschemar.conteudo N "
"LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo) "
"WHERE N.id_conteudo=%(id_conteudo)i")

select_estabelecimento_publicado = ("SELECT E.id_conteudo, E.titulo, E.pagamento, E.descricao, "
"E.observacao, E.publicado, R.nome as regiao,"
" to_char(E.publicado_em, 'dd/mm/YYYY HH24:MI') as publicado_em, E.endereco,"
" E.img, E.credito, E.id_regiao, E.telefone, E.telefonec, E.site, E.estado, E.rua, E.num,"
" E.bairro, E.cep, E.cadeirantes, E.capacidade, E.lat, E.lng, E.cidade,"
" D.id_destaque, D.titulo as titulo_destaque, D.descricao as "
" descricao_destaque, D.img as imagem_destaque,"
" to_char(E.publicado_em, 'YYYY/mm/dd') as data"
" FROM rschemar.conteudo E"
" INNER JOIN rschemar.destaque D ON (E.id_conteudo=D.id_conteudo)"
" LEFT JOIN rschemar.regiao R ON (E.id_regiao=R.id_regiao)"
" WHERE E.publicado=True AND E.publicado_em <= now() AND"
" (E.expira_em IS NULL OR E.expira_em > now())"
" ORDER BY E.publicado_em DESC LIMIT %(limit)i OFFSET %(offset)i")

select_estabelecimento_nome = ("SELECT E.id_conteudo, E.titulo, E.pagamento, E.descricao, "
"E.observacao, E.publicado, R.nome as regiao,"
" to_char(E.publicado_em, 'dd/mm/YYYY HH24:MI') as publicado_em, E.endereco,"
" E.img, E.credito, E.editor, E.id_regiao, E.telefone, E.telefonec, E.site, E.estado, E.rua, E.num,"
" E.bairro, E.cep, E.capacidade, E.cadeirantes, E.lat, E.lng, E.cidade,"
" D.id_destaque, D.titulo as titulo_destaque, D.descricao as "
" descricao_destaque, D.img as imagem_destaque,"
" to_char(E.publicado_em, 'YYYY/mm/dd') as data"
" FROM rschemar.conteudo E"
" INNER JOIN rschemar.destaque D ON (E.id_conteudo=D.id_conteudo)"
" LEFT JOIN rschemar.regiao R ON (E.id_regiao=R.id_regiao)"
" WHERE E.titulo ~* %(nome)s AND E.publicado=True AND E.publicado_em <= now() AND"
" (E.expira_em IS NULL OR E.expira_em > now())"
" ORDER BY E.publicado_em DESC LIMIT %(limit)i OFFSET %(offset)i")

select_estabelecimento_categoria = ("SELECT E.id_conteudo, E.titulo, E.pagamento, E.descricao, "
"E.observacao, E.publicado, R.nome as regiao,"
" to_char(E.publicado_em, 'dd/mm/YYYY HH24:MI') as publicado_em, E.endereco,"
" E.img, E.credito, E.editor, E.id_regiao, E.telefone, E.telefonec, E.site, E.estado, E.rua, E.num,"
" E.bairro, E.cep, E.capacidade, E.cadeirantes, E.lat, E.lng, E.cidade,"
" D.id_destaque, D.titulo as titulo_destaque, D.descricao as "
" descricao_destaque, D.img as imagem_destaque,"
" to_char(E.publicado_em, 'YYYY/mm/dd') as data"
" FROM rschemar.conteudo E"
" INNER JOIN rschemar.destaque D ON (E.id_conteudo=D.id_conteudo)"
" LEFT JOIN rschemar.estabelecimento_categoria B ON (B.id_conteudo=E.id_conteudo)"
" LEFT JOIN rschemar.regiao R ON (E.id_regiao=R.id_regiao)"
" WHERE id_categoria=%(categoria)s AND E.publicado=True AND E.publicado_em <= now() AND"
" (E.expira_em IS NULL OR E.expira_em > now())"
" ORDER BY E.publicado_em DESC LIMIT %(limit)i OFFSET %(offset)i")

select_estabelecimento_categoria_regiao = ("SELECT E.id_conteudo, E.titulo, E.pagamento, E.descricao, "
"E.observacao, E.publicado, R.nome as regiao,"
" to_char(E.publicado_em, 'dd/mm/YYYY HH24:MI') as publicado_em, E.endereco,"
" E.img, E.credito, E.editor, E.id_regiao, E.telefone, E.telefonec, E.site, E.estado, E.rua, E.num,"
" E.bairro, E.cep, E.capacidade, E.cadeirantes, E.lat, E.lng, E.cidade,"
" D.id_destaque, D.titulo as titulo_destaque, D.descricao as "
" descricao_destaque, D.img as imagem_destaque,"
" to_char(E.publicado_em, 'YYYY/mm/dd') as data"
" FROM rschemar.conteudo E"
" INNER JOIN rschemar.destaque D ON (E.id_conteudo=D.id_conteudo)"
" LEFT JOIN rschemar.estabelecimento_categoria B ON (B.id_conteudo=E.id_conteudo)"
" LEFT JOIN rschemar.regiao R ON (E.id_regiao=R.id_regiao)"
" WHERE id_categoria=%(categoria)s AND E.id_regiao=%(regiao)i"
" AND E.publicado=True AND E.publicado_em <= now() AND"
" (E.expira_em IS NULL OR E.expira_em > now())"
" ORDER BY E.publicado_em DESC LIMIT %(limit)i OFFSET %(offset)i")

select_estabelecimento_categoria_regiao_nome = ("SELECT E.id_conteudo, E.titulo, E.pagamento, E.descricao, "
"E.observacao, E.publicado, R.nome as regiao,"
" to_char(E.publicado_em, 'dd/mm/YYYY HH24:MI') as publicado_em, E.endereco,"
" E.img, E.credito, E.editor, E.id_regiao, E.telefone, E.telefonec, E.site, E.estado, E.rua, E.num,"
" E.bairro, E.cep, E.capacidade, E.cadeirantes, E.lat, E.lng, E.cidade,"
" D.id_destaque, D.titulo as titulo_destaque, D.descricao as "
" descricao_destaque, D.img as imagem_destaque,"
" to_char(E.publicado_em, 'YYYY/mm/dd') as data"
" FROM rschemar.conteudo E"
" INNER JOIN rschemar.destaque D ON (E.id_conteudo=D.id_conteudo)"
" LEFT JOIN rschemar.estabelecimento_categoria B ON (B.id_conteudo=E.id_conteudo)"
" LEFT JOIN rschemar.regiao R ON (E.id_regiao=R.id_regiao)"
" WHERE id_categoria=%(categoria)s AND E.titulo ~* %(nome)s AND E.id_regiao=%(regiao)i"
" AND E.publicado=True AND E.publicado_em <= now() AND"
" (E.expira_em IS NULL OR E.expira_em > now())"
" ORDER BY E.publicado_em DESC LIMIT %(limit)i OFFSET %(offset)i")

select_estabelecimento_nome_categoria = ("SELECT E.id_conteudo, E.titulo, E.pagamento, E.descricao, "
"E.observacao, E.publicado, R.nome as regiao,"
" to_char(E.publicado_em, 'dd/mm/YYYY HH24:MI') as publicado_em, E.endereco,"
" E.img, E.credito, E.editor, E.id_regiao, E.telefone, E.telefonec, E.site, E.estado, E.rua, E.num,"
" E.bairro, E.cep, E.capacidade, E.cadeirantes, E.lat, E.lng, E.cidade,"
" D.id_destaque, D.titulo as titulo_destaque, D.descricao as "
" descricao_destaque, D.img as imagem_destaque,"
" to_char(E.publicado_em, 'YYYY/mm/dd') as data"
" FROM rschemar.conteudo E"
" INNER JOIN rschemar.destaque D ON (E.id_conteudo=D.id_conteudo)"
" LEFT JOIN rschemar.estabelecimento_categoria B ON (B.id_conteudo=E.id_conteudo)"
" LEFT JOIN rschemar.regiao R ON (E.id_regiao=R.id_regiao)"
" WHERE id_categoria=%(categoria)s AND E.titulo ~* %(nome)s"
" AND E.publicado=True AND E.publicado_em <= now() AND"
" (E.expira_em IS NULL OR E.expira_em > now())"
" ORDER BY E.publicado_em DESC LIMIT %(limit)i OFFSET %(offset)i")

select_estabelecimento_nome_regiao = ("SELECT E.id_conteudo, E.titulo, E.pagamento, E.descricao, "
"E.observacao, E.publicado, R.nome as regiao,"
" to_char(E.publicado_em, 'dd/mm/YYYY HH24:MI') as publicado_em, E.endereco,"
" E.img, E.credito, E.editor, E.id_regiao, E.telefone, E.telefonec, E.site, E.estado, E.rua, E.num,"
" E.bairro, E.cep, E.capacidade, E.cadeirantes, E.lat, E.lng, E.cidade,"
" D.id_destaque, D.titulo as titulo_destaque, D.descricao as "
" descricao_destaque, D.img as imagem_destaque,"
" to_char(E.publicado_em, 'YYYY/mm/dd') as data"
" FROM rschemar.conteudo E"
" INNER JOIN rschemar.destaque D ON (E.id_conteudo=D.id_conteudo)"
" LEFT JOIN rschemar.regiao R ON (E.id_regiao=R.id_regiao)"
" WHERE E.titulo ~* %(nome)s AND E.id_regiao= %(regiao)i AND E.publicado=True AND E.publicado_em <= now() AND"
" (E.expira_em IS NULL OR E.expira_em > now())"
" ORDER BY E.publicado_em DESC LIMIT %(limit)i OFFSET %(offset)i")

select_estabelecimento_regiao = ("SELECT E.id_conteudo, E.titulo, E.pagamento, E.descricao, "
"E.observacao, E.publicado, R.nome as regiao,"
" to_char(E.publicado_em, 'dd/mm/YYYY HH24:MI') as publicado_em, E.endereco,"
" E.img, E.credito, E.editor, E.id_regiao, E.telefone, E.telefonec, E.site, E.estado, E.rua, E.num,"
" E.bairro, E.cep, E.capacidade, E.cadeirantes, E.lat, E.lng, E.cidade,"
" D.id_destaque, D.titulo as titulo_destaque, D.descricao as "
" descricao_destaque, D.img as imagem_destaque,"
" to_char(E.publicado_em, 'YYYY/mm/dd') as data"
" FROM rschemar.conteudo E"
" INNER JOIN rschemar.destaque D ON (E.id_conteudo=D.id_conteudo)"
" LEFT JOIN rschemar.regiao R ON (E.id_regiao=R.id_regiao)"
" WHERE E.id_regiao= %(regiao)i AND E.publicado=True AND E.publicado_em <= now() AND"
" (E.expira_em IS NULL OR E.expira_em > now())"
" ORDER BY E.publicado_em DESC LIMIT %(limit)i OFFSET %(offset)i")

select_estabelecimento_publicado_count = ("SELECT count(*) as qtde FROM rschemar.conteudo E"
" INNER JOIN rschemar.destaque D ON (E.id_conteudo=D.id_conteudo)"
" WHERE E.publicado=True AND E.publicado_em <= now() AND"
" (E.expira_em IS NULL OR E.expira_em > now())")

select_estabelecimento_nome_count = ("SELECT count(*) as qtde FROM rschemar.conteudo E"
" INNER JOIN rschemar.destaque D ON (E.id_conteudo=D.id_conteudo)"
" WHERE E.titulo ~* %(nome)s AND E.publicado=True AND E.publicado_em <= now() AND"
" (E.expira_em IS NULL OR E.expira_em > now())")

select_count_estabelecimento_categoria = ("SELECT count(*) as qtde FROM rschemar.conteudo E"
" INNER JOIN rschemar.destaque D ON (E.id_conteudo=D.id_conteudo)"
" LEFT JOIN rschemar.estabelecimento_categoria B ON (B.id_conteudo=E.id_conteudo)"
" WHERE id_categoria=%(categoria)s AND E.publicado=True AND E.publicado_em <= now() AND"
" (E.expira_em IS NULL OR E.expira_em > now())")

select_estabelecimento_nome_categoria_count = ("SELECT count(*) as qtde FROM rschemar.conteudo E"
" INNER JOIN rschemar.destaque D ON (E.id_conteudo=D.id_conteudo)"
" LEFT JOIN rschemar.estabelecimento_categoria B ON (B.id_conteudo=E.id_conteudo)"
" WHERE id_categoria=%(categoria)s AND E.titulo ~* %(nome)s AND E.publicado=True AND E.publicado_em <= now() AND"
" (E.expira_em IS NULL OR E.expira_em > now())")

select_count_estabelecimento_categoria_regiao = ("SELECT count(*) as qtde FROM rschemar.conteudo E"
" INNER JOIN rschemar.destaque D ON (E.id_conteudo=D.id_conteudo)"
" LEFT JOIN rschemar.estabelecimento_categoria B ON (B.id_conteudo=E.id_conteudo)"
" WHERE id_categoria=%(categoria)s AND E.id_regiao=%(regiao)i"
" AND E.publicado=True AND E.publicado_em <= now() AND"
" (E.expira_em IS NULL OR E.expira_em > now())")

select_count_estabelecimento_categoria_regiao_nome = ("SELECT count(*) as qtde FROM rschemar.conteudo E"
" INNER JOIN rschemar.destaque D ON (E.id_conteudo=D.id_conteudo)"
" LEFT JOIN rschemar.estabelecimento_categoria B ON (B.id_conteudo=E.id_conteudo)"
" WHERE id_categoria=%(categoria)s AND E.titulo ~* %(nome)s AND E.id_regiao=%(regiao)i"
" AND E.publicado=True AND E.publicado_em <= now() AND"
" (E.expira_em IS NULL OR E.expira_em > now())")

select_estabelecimento_nome_regiao_count = ( "SELECT count(*) as qtde FROM rschemar.conteudo E"
" INNER JOIN rschemar.destaque D ON (E.id_conteudo=D.id_conteudo)"
" WHERE E.titulo ~* %(nome)s AND E.id_regiao=%(regiao)i AND E.publicado=True AND E.publicado_em <= now() AND"
" (E.expira_em IS NULL OR E.expira_em > now())")

select_count_estabelecimento_regiao = ("SELECT count(*) as qtde FROM rschemar.conteudo E"
" INNER JOIN rschemar.destaque D ON (E.id_conteudo=D.id_conteudo)"
" WHERE E.id_regiao=%(regiao)s AND E.publicado=True  AND E.publicado_em <= now() AND"
" (E.expira_em IS NULL OR E.expira_em > now())")

select_estabelecimento_publicado_unico = ("SELECT E.id_conteudo, E.titulo, E.pagamento, E.descricao,"
" E.observacao, E.publicado, "
"to_char(E.publicado_em, 'dd/mm/YYYY HH24:MI') as publicado_em, E.endereco, "
"E.img, E.credito, E.editor, R.nome as regiao, E.telefone, E.telefonec,"
"E.site, E.estado, E.rua, E.num, E.bairro, E.cep, E.capacidade, E.cadeirantes, E.lat, E.lng, E.cidade,"
"D.id_destaque, D.titulo as titulo_destaque, D.descricao as descricao_destaque, "
"D.img as imagem_destaque "
"FROM rschemar.conteudo E "
"LEFT JOIN rschemar.destaque D ON (E.id_conteudo=D.id_conteudo) "
"LEFT JOIN rschemar.regiao R ON (E.id_regiao=R.id_regiao)"
"WHERE E.id_conteudo=%(id_conteudo)i AND E.publicado='TRUE' AND E.publicado_em <= now() AND "
"(E.expira_em IS NULL OR E.expira_em > now())")

insert_conteudo = ("INSERT INTO rschemar.conteudo("
"id_conteudo, titulo, pagamento, descricao, observacao, publicado, "
"expira_em, publicado_em, endereco, "
"img, credito, editor, id_regiao, telefone, telefonec, site, estado, rua, num, bairro, cep, " 
"capacidade, cadeirantes, lat, lng,cidade)"
"VALUES (%(id_conteudo)i, %(titulo)s, %(pagamento)s, %(descricao)s, %(observacao)s, %(publicado)s,  "
"%(expira_em)s, %(publicado_em)s, %(endereco)s, "
"%(imagem)s, %(credito)s, %(editor)s, %(regiao)s, %(telefone)s, %(telefonec)s, " 
"%(site)s, %(estado)s, %(rua)s, %(num)s, %(bairro)s, %(cep)s, %(capacidade)s, %(cadeirantes)s, %(lat)s, %(lng)s, %(cidade)s)")

insert_categoria = ("INSERT INTO rschemar.categoria (nome) VALUES (%(nome)s)")

insert_regiao = ("INSERT INTO rschemar.regiao (nome) VALUES (%(nome)s)")

insert_destaque  = ("INSERT INTO rschemar.destaque (id_conteudo, titulo, descricao, img, peso) VALUES "
"(%(id_conteudo)i, %(titulo)s, %(descricao)s, %(img)s, %(peso)i)")

insert_categoria_estabelecimento = ("INSERT INTO rschemar.estabelecimento_categoria VALUES (%(id_conteudo)i, %(id_categoria)i)")

update_conteudo = ("UPDATE rschemar.conteudo SET titulo=%(titulo)s, "
"pagamento=%(pagamento)s, descricao=%(descricao)s, publicado=%(publicado)s, observacao=%(observacao)s,"
"expira_em=%(expira_em)s, publicado_em=%(publicado_em)s, endereco=%(endereco)s, img=%(imagem)s, "
"credito=%(credito)s, editor=%(editor)s, id_regiao=%(regiao)s," 
"telefone=%(telefone)s, telefonec=%(telefonec)s, site=%(site)s, estado=%(estado)s, rua=%(rua)s, num=%(num)s,"
"bairro=%(bairro)s, cep=%(cep)s, capacidade=%(capacidade)s, cadeirantes=%(cadeirantes)s, lat=%(lat)s, lng=%(lng)s, cidade=%(cidade)s"
"WHERE id_conteudo=%(id_conteudo)i")

update_categoria = ("UPDATE rschemar.categoria SET nome=%(nome)s WHERE id_categoria=%(id_categoria)i")
update_regiao = ("UPDATE rschemar.regiao SET nome=%(nome)s WHERE id_regiao=%(id_regiao)i")

delete_categoria = ("DELETE FROM rschemar.categoria WHERE id_categoria=%(id_categoria)i")

delete_categoria_estabelecimento = ("DELETE FROM rschemar.estabelecimento_categoria WHERE id_conteudo=%(id_conteudo)i")

delete_regiao = ("DELETE FROM rschemar.regiao WHERE id_regiao=%(id_regiao)i")

delete_conteudo = ("DELETE FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

delete_destaque = ("DELETE FROM rschemar.destaque WHERE id_conteudo=%(id_conteudo)i")

permissions = ("GRANT USAGE ON SCHEMA rschemar TO %(user)s;"
"GRANT SELECT ON rschemar.conteudo TO %(user)s;"
"GRANT SELECT ON rschemar.destaque TO %(user)s;"
)

permissions_admin = permissions

structure = """
  CREATE SCHEMA rschemar;


  CREATE TABLE rschemar.categoria (
    id_categoria SERIAL NOT NULL,
    nome VARCHAR NOT NULL,
    PRIMARY KEY (id_categoria)
   );  

   CREATE TABLE rschemar.regiao (
    id_regiao SERIAL NOT NULL,
    nome VARCHAR NOT NULL,
    PRIMARY KEY (id_regiao)

   );  

  CREATE TABLE rschemar.conteudo (
    id_conteudo SERIAL NOT NULL,
    id_idioma INTEGER DEFAULT 102,
    titulo VARCHAR NOT NULL,
    pagamento VARCHAR NULL,
    descricao VARCHAR NULL,
    observacao VARCHAR NULL,
    arquivo VARCHAR,
    publicado BOOL NOT NULL DEFAULT 'False',
    expira_em TIMESTAMP NULL,
    publicado_em TIMESTAMP NOT NULL,
    endereco VARCHAR NOT NULL,
    atualizado_em TIMESTAMP NULL,
    exportado BOOLEAN DEFAULT 'False',
    id_regiao INT NULL,
    img VARCHAR NULL,
    credito VARCHAR NULL,
    editor BOOL NOT NULL DEFAULT 'False',
    telefone VARCHAR NULL,
    telefonec VARCHAR NULL,
    site VARCHAR NULL,
    estado VARCHAR NOT NULL,
    rua VARCHAR NOT NULL,
    num VARCHAR NOT NULL,
    bairro VARCHAR NOT NULL,
    cep VARCHAR NULL,
    capacidade VARCHAR NULL,
    cadeirantes VARCHAR NULL,
    lat double precision,
    lng double precision,
    cidade VARCHAR NOT NULL,  
    PRIMARY KEY(id_conteudo),
    FOREIGN KEY(id_regiao)
      REFERENCES rschemar.regiao(id_regiao)
           ON DELETE SET NULL     
  );
  CREATE INDEX rschemar_conteudo_id_regiao_index ON rschemar.conteudo USING btree (id_regiao);
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

  CREATE TABLE rschemar.estabelecimento_categoria (
     id_conteudo INT NOT NULL,
     id_categoria INT NOT NULL,
     FOREIGN KEY(id_conteudo)
        REFERENCES rschemar.conteudo(id_conteudo)
          ON DELETE CASCADE,
     FOREIGN KEY(id_categoria)
        REFERENCES rschemar.categoria(id_categoria)
          ON DELETE CASCADE
); 
"""
