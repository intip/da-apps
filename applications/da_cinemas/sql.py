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
select_nextval_cinema = ("SELECT NEXTVAL('rschemar.conteudo_id_conteudo_seq'::text) as id")


select_nextval_foto_conteudo = ("SELECT NEXTVAL('rschemar.fotos_conteudo_id_foto_seq'::text) as id")


select_nextval_cidade = ("SELECT NEXTVAL('rschemar.cidade_id_cidade_seq'::text) as id")

select_nextval_genero = ("SELECT NEXTVAL('rschemar.genero_id_genero_seq'::text) as id")

select_nextval_sessao = ("SELECT NEXTVAL('rschemar.sessoes_id_sessao_seq'::text) as id")

select_nextval_sala = ("SELECT NEXTVAL('rschemar.salas_id_sala_seq'::text) as id")

select_cinema_dados = ("SELECT id_conteudo, titulo, precos, site, "
"telefone, telefonec, site, estado, rua, endereco, num, bairro,"
" cep, lat, lng, id_cidade, "
"to_char(expira_em, 'YYYY-MM-DD HH24:MI') as expira_em, "
"to_char(publicado_em, 'YYYY-MM-DD HH24:MI') as publicado_em, publicado, "
"to_char(atualizado_em, 'YYYY-MM-DD') as atualizado_em "
"FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

select_status_cinema = ("SELECT publicado FROM rschemar.conteudo WHERE "
"id_conteudo=%(id_conteudo)s")

select_tipo_sala = ("SELECT * FROM rschemar.tipo ORDER BY tipo")

select_tipo_sala_id = ("SELECT (SELECT id_tipo FROM rschemar.tipo WHERE tipo=%(tipo)s::text) as id")

select_sessoes_cinema = ("SELECT CO.titulo as cinema_nome, FI.titulo as filme_nome,"
" SE.id_conteudo, SE.id_tipo, SE.horarios as horario, SE.id_sessao,  "
"SE.id_filme, SA.nome as sala_nome, SE.data_inicio, SE.data_fim, SE.Horarios, SE.status"
" FROM rschemar.sessoes SE JOIN rschemar.conteudo CO ON (CO.id_conteudo = SE.id_conteudo)"
" JOIN rschemar.salas SA ON (SA.id_sala = SE.id_sala) "
" JOIN %(SCHEMA)s.conteudo FI ON (FI.id_conteudo = SE.id_filme)"
" WHERE SE.id_conteudo = %(id_conteudo)i")

select_sessoes_id_sessao = ("SELECT id_sessao, id_sala, id_tipo, id_conteudo, "
  "id_filme, data_inicio, data_fim , horarios, status FROM rschemar.sessoes"
" WHERE id_sessao = %(id_sessao)i")

select_nome_cinema = ("SELECT titulo FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i")

select_cinema = ("SELECT C.id_conteudo, C.titulo, C.endereco, C.precos, CI.nome as cidade,  "
"C.id_cidade, C.publicado, C.cep, C.lat, C.lng, "
"C.telefone, C.telefonec, C.site, C.estado, C.rua, C.num, C.bairro,"
"to_char(publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em, "
"to_char(expira_em, 'DD/MM/YYYY HH24:MI') as expira_em "
"FROM rschemar.conteudo C "
"JOIN rschemar.cidade CI ON (C.id_cidade = CI.id_cidade)  WHERE C.id_conteudo=%(id_conteudo)i")

select_sessoes_filme = ("SELECT SE.id_sessao, SE.horarios, SE.data_inicio,"
" SE.data_fim, SE.status, CO.titulo as cinema_nome, SA.nome, SA.is3d"
" FROM rschemar.sessoes SE "
" JOIN rschemar.salas SA ON (SA.id_sala = SE.id_sala )"
" JOIN rschemar.conteudo CO ON (CO.id_conteudo = SE.id_conteudo)"
" WHERE SE.id_filme = %(id_filme)i AND SE.id_conteudo = %(id_conteudo)i"
" AND (SE.data_inicio <= %(data_atual)s AND %(data_atual)s <= SE.data_fim) AND %(data_atual)s >= SE.data_inicio")

select_cidades = ("SELECT nome, id_cidade FROM rschemar.cidade ORDER BY nome ASC")

select_filmes_sessoes = ("SELECT distinct FI.id_conteudo, FI.titulo FROM %(SCHEMA)s.conteudo FI"
" JOIN rschemar.sessoes SE  ON (SE.id_filme = FI.id_conteudo)"
" WHERE (SE.data_inicio <= %(data_atual)s AND %(data_atual)s <= SE.data_fim) AND %(data_atual)s >= SE.data_inicio"
" ORDER BY FI.titulo ASC")

select_sessao = ("SELECT CI.nome as cinema_nome,SE.id_conteudo, SE.id_tipo, "
"SE.id_filme, SA.nome as sala_nome, SE.data_inicio, SE.data_fim, SE.horarios, SE.status"
" FROM rschemar.sessoes SE JOIN rschemar.conteudo CO ON (CO.id_conteudo = SE.id_conteudo)"
" JOIN rschemar.salas SA ON (SA.id_sala = SE.id_sala)")

select_sessao_by_cinema = ("SELECT distinct id_conteudo FROM rschemar.sessoes")

select_sessao_by_film = ("SELECT distinct id_filme FROM rschemar.sessoes")

select_filmes_conteudo = ("SELECT distinct FI.titulo, FI.id_conteudo,FI.titulo_original,"
"  SA.nome as sala_nome, FI.ano, FI.id_tipo, FI.id_genero, FI.direcao, FI.duracao,"
"  FI.censura, FI.elenco, SE.id_sessao, FI.sinopse, SE.horarios, FI.descricao, FI.trailer,"
"  FF.img as img"
"  FROM rschemar.sessoes SE JOIN %(SCHEMA)s.conteudo FI ON (FI.id_conteudo = SE.id_filme)"
"  JOIN rschemar.salas SA ON(SA.id_sala = SE.id_sala)"
"  JOIN %(SCHEMA)s.destaque FF ON(FF.id_conteudo = FI.id_conteudo)"
"  WHERE SE.id_conteudo = %(id_conteudo)i AND SE.data_inicio <= %(data_atual)s"
"  AND %(data_atual)s <= SE.data_fim AND %(data_atual)s >= SE.data_inicio ORDER BY SA.nome, SE.horarios ASC")


select_genero = ("SELECT nome,id_genero FROM rschemar.genero")

select_cinemas_by_cidade = ("SELECT id_conteudo, titulo FROM rschemar.conteudo "
"WHERE id_cidade=%(id_cidade)s ORDER BY titulo ASC")

select_salas = ("SELECT id_sala, id_conteudo, nome, is3D "
"FROM rschemar.salas WHERE id_conteudo=%(id_conteudo)i")

select_filmes = ("SELECT titulo,id_filme FROM rschemar.filme ORDER BY id_filme DESC LIMIT 30")

select_nome_cidade = ("SELECT nome FROM rschemar.cidade"
" WHERE id_cidade=%(id_cidade)i")


select_cinema_cidade = ("SELECT titulo,id_conteudo FROM rschemar.conteudo"
 " WHERE id_cidade=%(id_cidade)i ORDER BY titulo ASC")

select_cinema_nome_cidade = ("SELECT CN.titulo, CN.id_conteudo FROM rschemar.conteudo CN "
"JOIN rschemar.cidade CI ON (CN.id_cidade=CI.id_cidade) WHERE CI.nome=%(nome_cidade)s ORDER BY CN.titulo ASC")

select_sessao_byfilm = ("SELECT id_conteudo FROM rschemar.sessoes WHERE id_filme=%(id_filme)i")

select_filme = ("SELECT  FI.id_filme, FI.titulo, GE.nome as genero, FI.titulo_original,"
                "FI.ano, FI.id_tipo, FI.id_genero, FI.direcao, FI.duracao, FI.censura,"
                "FI.elenco, FI.sinopse, FO.arquivo as imagem_destaque, FI.descricao, FI.trailer,"
                " FROM %(SCHEMA)s.conteudo FI JOIN rschemar.genero GE ON (FI.id_genero = GE.id_genero)"
                " JOIN %(SCHEMA)s.destaque FO ON (FO.id_conteudo = FI.id_conteudo) "
                " WHERE FI.id_conteudo = %(id_filme)i")

select_sala = ("SELECT nome FROM rschemar.salas WHERE id_sala=%(id_sala)i")

select_fotos_conteudo = ("SELECT id_foto, id_conteudo, arquivo, credito "
"FROM rschemar.fotos_conteudo WHERE id_conteudo=%(id_conteudo)i")

select_sessoes_by_cinema = ("SELECT s.id_sala, s.horario,  s.id_filme, t.id_tipo "
"FROM rschemar.sessoes s "
"LEFT JOIN rschemar.tipo t ON (s.id_tipo=t.id_tipo) "
"LEFT JOIN rschemar.salas sa ON (sa.id_sala=s.id_sala)"
"WHERE s.id_conteudo=%(id_conteudo)s")

select_sessoes_by_sala = ("SELECT s.horario, s.id_filme, t.tipo "
"FROM rschemar.sessoes s "
"LEFT JOIN rschemar.tipo t ON (s.id_tipo=t.id_tipo) "
"LEFT JOIN rschemar.salas sa ON (sa.id_sala=s.id_sala)"
"WHERE s.id_sala=%(id_sala)s")


select_filmes_cartaz = ("SELECT DISTINCT ON (FI.titulo) FI.titulo, FI.id_conteudo as id_conteudo,"
" FF.img as img, FI.sinopse, SE.status FROM %(SCHEMA)s.conteudo FI"
" JOIN rschemar.sessoes SE ON (SE.id_filme = FI.id_conteudo) "
" JOIN %(SCHEMA)s.destaque FF ON (FF.id_conteudo = FI.id_conteudo) "
" WHERE SE.data_inicio <= %(data_atual)s  AND %(data_atual)s"
" <= SE.data_fim AND %(data_atual)s >= SE.data_inicio"
" LIMIT %(limit)i ")

select_sessoes_by_filme = ("SELECT c.titulo as cinema, sa.nome, s.horario, t.tipo "
"FROM rschemar.sessoes s "
"LEFT JOIN rschemar.tipo t ON (s.id_tipo=t.id_tipo) "
"LEFT JOIN rschemar.salas sa ON (s.id_sala=sa.id_sala) "
"LEFT JOIN rschemar.conteudo c ON (s.id_conteudo=c.id_conteudo) "
"WHERE s.id_filme=%(id_filme)s ORDER BY c.titulo, sa.nome, s.horario")

select_Cinemas_id_filme = ("SELECT DISTINCT ON (CO.id_conteudo) CO.titulo,SE.id_sala, CO.id_conteudo FROM rschemar.sessoes SE "
"JOIN rschemar.Conteudo CO ON (CO.id_conteudo = SE.id_conteudo)"
" WHERE SE.id_filme=%(id_filme)i AND (SE.data_inicio <= %(data_atual)s"
" AND %(data_atual)s <= SE.data_fim) AND %(data_atual)s >= SE.data_inicio")

select_sessao_byid= ("SELECT id_filme, id_conteudo FROM rschemar.sessoes WHERE id_sessao=%(id_sessao)i")

select_cinemas_filme = ("SELECT c.titulo, c.id_conteudo FROM rschemar.sessoes s "
"LEFT JOIN rschemar.conteudo c ON (s.id_conteudo=c.id_conteudo) "
"WHERE s.id_filme=%(id_filme)s ORDER BY c.titulo")

select_cinemas = ("SELECT id_conteudo, titulo FROM rschemar.conteudo")

select_ids_sala = ("SELECT id_sala FROM rschemar.salas WHERE id_conteudo = %(id_conteudo)i")

select_filmes_last = ("SELECT titulo, id_filme FROM rschemar.filme"
" ORDER BY date LIMIT %(limit)i")

select_salas_filme_cinema = ("SELECT distinct(sa.nome), sa.id_sala, sa.is3D FROM rschemar.sessoes s "
"LEFT JOIN rschemar.salas sa ON (s.id_sala=sa.id_sala) "
"WHERE s.id_filme=%(id_filme)s AND s.id_conteudo=%(id_cinema)s ORDER BY sa.nome")

select_sessoes_by_sala = ("SELECT s.horario, t.tipo FROM rschemar.sessoes s "
"LEFT JOIN rschemar.tipo t on (s.id_tipo=t.id_tipo) "
"WHERE s.id_sala=%(id_sala)s AND s.id_filme=%(id_filme)s ORDER BY s.horario")

select_filmes_by_cinema = ("SELECT distinct(f.id_filme), f.nome FROM rschemar.filmes f "
"LEFT JOIN rschemar.sessoes s ON (s.id_filme=f.id_filme) "
"LEFT JOIN rschemar.conteudo c ON (c.id_conteudo=s.id_conteudo) "
"WHERE c.id_conteudo=%(id_cinema)s")

select_top10 = ("SELECT * FROM rschemar.top10")

exists_id_sala = ("SELECT nome FROM rschemar.salas WHERE id_sala = %(id_sala)i")

insert_cinema = ("INSERT INTO rschemar.conteudo (id_conteudo, "
"titulo, precos, telefone, telefonec, site, estado, rua, num, bairro,"
" cep, lat, lng, endereco, id_cidade, "
"publicado, expira_em, publicado_em) VALUES "
"(%(id_conteudo)s, %(nome)s, %(precos)s, %(telefone)s, %(telefonec)s, %(site)s, "
" %(estado)s, %(rua)s, %(num)s, %(bairro)s, %(cep)s, %(lat)s, %(lng)s, %(endereco)s,  %(id_cidade)s,"
" %(publicado)s, %(expira_em)s, %(publicado_em)s)")

insert_sala = ("INSERT INTO rschemar.salas (id_sala, "
"id_conteudo, nome, is3D) VALUES "
"(%(id_sala)s, %(id_conteudo)s, %(nome)s, %(is3D)s)")


insert_filme = ("INSERT INTO rschemar.filme (id_filme, titulo, titulo_original, pais, "
" ano, id_genero, direcao, duracao, censura, elenco, sinopse, status, descricao,"
" trailer, date"
") VALUES (%(id_filme)s, %(titulo)s, %(titulo_original)s, %(pais)s, %(ano)s, %(genero)s,"
" %(direcao)s, %(duracao)s, %(censura)s, %(elenco)s, %(sinopse)s, %(status)s,"
" %(descricao)s, %(trailer)s, %(data)s)")

insert_sessao = ("INSERT INTO rschemar.sessoes (id_sessao, "
"id_sala, id_conteudo, id_tipo, id_filme, horarios, data_inicio, data_fim, status, publicado_em) VALUES "
"(%(id_sessao)s, %(id_sala)s, %(id_conteudo)s, %(id_tipo)s, %(id_filme)s,"
" %(horarios)s, %(data_inicio)s, %(data_fim)s,%(status)s, '2000-01-01 00:00')")

insert_top = ("INSERT INTO rschemar.top10 (id_top10, "
"titulo, texto, top1, top2 ,top3, top4, top5, top6, top7, top8, top9, top10) VALUES "
"(1, %(titulo)s, %(texto)s, %(top1)s, %(top2)s, %(top3)s, %(top4)s, %(top5)s, %(top6)s, %(top7)s, %(top8)s, "
"%(top9)s, %(top10)s)")

insert_fotos_conteudo = ("INSERT INTO rschemar.fotos_conteudo (id_foto, "
"id_conteudo, arquivo, credito) VALUES "
"(%(id_foto)s, %(id_conteudo)s, %(arquivo)s, %(credito)s)")


insert_cidade = ("INSERT INTO rschemar.cidade(id_cidade, nome) "
                 "VALUES (%(id_cidade)i, %(nome)s)")

insert_genero = ("INSERT INTO rschemar.genero(nome,id_genero) VALUES (%(nome)s,%(id_genero)i)")


exists_genero = ("SELECT titulo FROM rschemar.filme WHERE id_genero = %(id_genero)i")

exists_cidade = ("SELECT titulo FROM rschemar.conteudo WHERE id_cidade = %(id_cidade)i")

delete_cinema = ("DELETE FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)s; "
"DELETE FROM rschemar.salas WHERE id_conteudo=%(id_conteudo)s;"
"DELETE FROM rschemar.fotos_conteudo WHERE id_conteudo=%(id_conteudo)s;"
"DELETE FROM rschemar.sessoes WHERE id_conteudo=%(id_conteudo)s;")

delete_dados_cinema = ("DELETE FROM rschemar.fotos_conteudo WHERE id_conteudo=%(id_conteudo)s")


delete_sala = ("DELETE FROM rschemar.salas WHERE id_sala=%(id_sala)s;")


delete_foto_filme = ("DELETE FROM rschemar.fotos_conteudo WHERE id_foto=%(id_foto)s")

delete_cidade = ("DELETE FROM rschemar.cidade WHERE id_cidade=%(id_cidade)i")

delete_genero = ("DELETE FROM rschemar.genero WHERE id_genero=%(id_genero)i")

delete_fotos_conteudo = ("DELETE FROM rschemar.fotos_conteudo WHERE id_conteudo=%(id_conteudo)s")


delete_sessao = ("DELETE FROM rschemar.sessoes WHERE id_sessao=%(id_sessao)i")

delete_filme = ("DELETE FROM rschemar.filme WHERE id_filme=%(id_filme)i")

update_cinema = ("UPDATE rschemar.conteudo SET titulo=%(nome)s, "
"precos=%(precos)s, site=%(site)s, endereco=%(endereco)s, estado=%(estado)s,"
"id_cidade=%(id_cidade)s, telefone=%(telefone)s, publicado=%(publicado)s, "
"lat=%(lat)s, lng=%(lng)s, cep=%(cep)s, num=%(num)s, bairro=%(bairro)s,"
"expira_em=%(expira_em)s, publicado_em=%(publicado_em)s"
"WHERE id_conteudo=%(id_conteudo)s")

update_sessao = ("UPDATE rschemar.sessoes SET id_sessao=%(id_sessao)i,"
"  id_sala=%(id_sala)i, id_tipo=%(id_tipo)i, id_conteudo=%(id_conteudo)i,"
"  id_filme=%(id_filme)i, data_inicio=%(data_inicio)s, data_fim=%(data_fim)s,"
"  horarios=%(horarios)s, status=%(status)s WHERE id_sessao=%(id_sessao)i")

update_filme = ("UPDATE rschemar.filme SET " 
" titulo=%(titulo)s, titulo_original=%(titulo_original)s, pais=%(pais)s, "
" ano=%(ano)s, id_genero=%(genero)s, direcao=%(direcao)s, duracao=%(duracao)s,"
" censura=%(censura)s, elenco=%(elenco)s, sinopse=%(sinopse)s, status=%(status)s,"
" descricao=%(descricao)s, trailer=%(trailer)s"
" WHERE id_filme=%(id_filme)s")

update_sala = ("UPDATE rschemar.salas SET nome=%(nome)s, is3D=%(is3D)s"
" WHERE id_sala=%(id_sala)i")

update_cidade = ("UPDATE rschemar.cidade SET nome=%(nome)s"
" WHERE id_cidade = %(id_cidade)i")


update_genero = ("UPDATE rschemar.genero SET nome=%(nome)s WHERE id_genero=%(id_genero)i")

update_top10 = ("UPDATE rschemar.top10 SET titulo=%(titulo)s, texto=%(texto)s, top1=%(top1)s, top2=%(top2)s, "
"top3=%(top3)s, top4=%(top4)s, top5=%(top5)s, top6=%(top6)s, top7=%(top7)s, top8=%(top8)s, top9=%(top1)s, top10=%(top10) "
"WHERE id_top10=1")

delete_top10 = ("DELETE FROM rschemar.top10 WHERE id_top10=1")



permissions = """
  GRANT USAGE ON SCHEMA rschemar TO %(user)s;
  GRANT SELECT ON rschemar.conteudo TO %(user)s;
  GRANT SELECT ON rschemar.salas TO %(user)s;
  GRANT SELECT ON rschemar.tipo TO %(user)s;
  GRANT SELECT ON rschemar.sessoes TO %(user)s;
  GRANT SELECT ON rschemar.fotos_conteudo TO %(user)s;
  GRANT SELECT ON rschemar.cidade TO %(user)s;
  GRANT SELECT ON rschemar.top10 TO %(user)s;
"""

structure = """
CREATE SCHEMA rschemar;

CREATE TABLE rschemar.cidade(
  id_cidade SERIAL NOT NULL,
  nome VARCHAR NOT NULL,
  PRIMARY KEY(id_cidade)
);

CREATE TABLE rschemar.conteudo(
  id_conteudo SERIAL NOT NULL,
  titulo VARCHAR NOT NULL,
  telefone VARCHAR NULL,
  telefonec VARCHAR NULL,
  site VARCHAR NULL,
  estado VARCHAR NOT NULL,
  rua VARCHAR NOT NULL,
  num VARCHAR NOT NULL,
  bairro VARCHAR NOT NULL,
  cep VARCHAR NULL,
  lat double precision,
  lng double precision,
  id_cidade int NOT NULL,  
  precos VARCHAR,
  endereco VARCHAR,
  publicado BOOL NOT NULL DEFAULT 'False',
  expira_em TIMESTAMP NULL,
  publicado_em TIMESTAMP NOT NULL,
  atualizado_em TIMESTAMP NULL,
  exportado BOOLEAN DEFAULT 'False',
  PRIMARY KEY(id_conteudo),
  FOREIGN KEY(id_cidade)
    REFERENCES rschemar.cidade(id_cidade)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);

CREATE TABLE rschemar.salas(
  id_sala SERIAL NOT NULL,
  id_conteudo INT NOT NULL,
  nome VARCHAR NOT NULL,
  is3D BOOL NOT NULL DEFAULT 'False',
  PRIMARY KEY(id_sala),
  FOREIGN KEY(id_conteudo)
    REFERENCES rschemar.conteudo(id_conteudo)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);

CREATE INDEX rschemar_salas_id_conteudo_index ON
  rschemar.salas USING btree (id_conteudo);

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

INSERT INTO rschemar.tipo (id_tipo, tipo)
  VALUES (1, 'Legendado');
INSERT INTO rschemar.tipo (id_tipo, tipo)
  VALUES (2, 'Dublado');
INSERT INTO rschemar.tipo (id_tipo, tipo)
  VALUES (3, 'Nacional');

CREATE TABLE rschemar.sessoes(
  id_sessao SERIAL NOT NULL,
  id_sala INT NOT NULL,
  id_tipo INT NOT NULL,
  id_conteudo INT NOT NULL,
  id_filme INT NOT NULL,
  data_inicio DATE NOT NULL,
  data_fim DATE NOT NULL,
  publicado_em TIMESTAMP NULL,
  horarios VARCHAR NOT NULL,
  status VARCHAR NOT NULL,
  PRIMARY KEY(id_sessao),
  FOREIGN KEY(id_sala)
    REFERENCES rschemar.salas(id_sala)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(id_tipo)
    REFERENCES rschemar.tipo(id_tipo)
      ON UPDATE CASCADE,
  FOREIGN KEY(id_conteudo)
    REFERENCES rschemar.conteudo(id_conteudo)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);

CREATE INDEX rschemar_sessoes_id_sala_index ON
  rschemar.sessoes USING btree (id_sala);
CREATE INDEX rschemar_sessoes_id_tipo_index ON
  rschemar.sessoes USING btree (id_tipo);
CREATE INDEX rschemar_sessoes_id_conteudo_index ON
  rschemar.sessoes USING btree (id_conteudo);

CREATE TABLE rschemar.fotos_conteudo(
  id_foto SERIAL NOT NULL,
  id_conteudo INT NOT NULL,
  arquivo VARCHAR NOT NULL,
  credito VARCHAR NULL,
  PRIMARY KEY(id_foto),
  FOREIGN KEY(id_conteudo)
    REFERENCES rschemar.conteudo(id_conteudo)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);




CREATE TABLE rschemar.top10(
  id_top10 SERIAL NOT NULL,
  titulo VARCHAR,
  texto VARCHAR,
  top1 VARCHAR,
  top2 VARCHAR,
  top3 VARCHAR,
  top4 VARCHAR,
  top5 VARCHAR,
  top6 VARCHAR,
  top7 VARCHAR,
  top8 VARCHAR,
  top9 VARCHAR,
  top10 VARCHAR,
  PRIMARY KEY(id_top10)
);

INSERT INTO rschemar.top10 VALUES ('1', '', '', '', '','','','','','','','','');

CREATE INDEX rschemar_fotos_id_conteudo_index ON
  rschemar.fotos_conteudo USING btree (id_conteudo);
"""
