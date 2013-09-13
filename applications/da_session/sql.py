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
insert_session = ("INSERT INTO rschemar.session (id_session, nome, email, datahora, extra) "
                   "VALUES (%(id_session)s, %(nome)s, %(email)s, now(), %(extra)s);"
                    "DELETE FROM rschemar.session WHERE datahora < %(datahorae)s;")

insert_captcha = ("DELETE FROM rschemar.captcha WHERE datahora < %(datah)s; "
                  "INSERT INTO rschemar.captcha (hash, solucao, datahora) VALUES (%(hash)s, %(solucao)s, now());")

insert_session_temp = ("DELETE FROM rschemar.temp_session WHERE email=%(email)s;"
                       "INSERT INTO rschemar.temp_session (codigo, login, master, email, nome, apelido, sexo, dt_expiracao, dt_nascimento, cpfcnpj, "
                       "pessoa, contato, rg, senha, rua, numero, complemento, bairro, cidade, estado, cep, pais, tipo_end, ddi, ddd, telefone, "
                       "tipo_tel, ramal, codigo_externo, data) VALUES (%(codigo)s, %(login)s, %(master)s, %(email)s, %(nome)s, %(apelido)s, %(sexo)s, " 
                       "%(dt_expiracao)s, %(dt_nascimento)s, %(cpfcnpj)s, %(pessoa)s, %(contato)s, %(rg)s, %(senha)s, %(rua)s, %(numero)s, " 
                       "%(complemento)s, %(bairro)s, %(cidade)s, %(estado)s, %(cep)s, %(pais)s, %(tipo_end)s, %(ddi)s, %(ddd)s, %(telefone)s, " 
                       "%(tipo_tel)s, %(ramal)s, %(codigo_externo)s, now())")

select_session_temp = ("SELECT * FROM rschemar.temp_session WHERE codigo=%(codigo)s")

delete_temp_session = ("DELETE FROM rschemar.temp_session WHERE codigo=%(codigo)s")

delete_session = ("DELETE FROM rschemar.session WHERE id_session=%(id_session)s;")

select_session_dados = ("SELECT id_session, nome, email, extra FROM rschemar.session "
                        "WHERE id_session=%(id_session)s AND datahora >= %(datahora)s LIMIT 1")

select_sessao_captcha = ("SELECT solucao FROM rschemar.captcha WHERE hash=%(hash)s LIMIT 1")

select_cadastro_captcha = ("SELECT hash, email, dados, data FROM rschemar.wad_temp WHERE hash=%(hash)s  LIMIT 1")

update_session_user = ("UPDATE rschemar.session SET datahora=now() WHERE id_session=%(id_session)s")

permissions = ("GRANT USAGE ON SCHEMA rschemar TO %(user)s;"
"GRANT SELECT, DELETE, INSERT, UPDATE ON rschemar.session TO %(user)s;"
"GRANT SELECT, INSERT, UPDATE, DELETE ON rschemar.captcha TO %(user)s;"
"GRANT SELECT, INSERT, UPDATE, DELETE ON rschemar.temp_session TO %(user)s;"
)
permissions_admin = permissions

structure = """
  CREATE SCHEMA rschemar;

   CREATE TABLE rschemar.session (
    id_session VARCHAR NOT NULL,
    nome VARCHAR NULL,
    email VARCHAR NULL,
    datahora TIMESTAMP NULL,
    extra VARCHAR NULL,
    PRIMARY KEY(id_session)
  );
  CREATE INDEX rschemar_session_datahora_index ON rschemar.session USING btree (datahora);

   CREATE TABLE rschemar.captcha (
    hash VARCHAR NOT NULL,
    solucao VARCHAR NOT NULL,
    datahora TIMESTAMP NOT NULL,
    PRIMARY KEY (hash)
    );
  
   CREATE TABLE rschemar.temp_session (
    codigo VARCHAR NOT NULL,
    login VARCHAR NOT NULL,
    master VARCHAR NULL,
    email VARCHAR NOT NULL,
    nome VARCHAR NOT NULL,
    apelido VARCHAR NOT NULL,
    sexo VARCHAR(2) NOT NULL,
    dt_expiracao VARCHAR NULL,
    dt_nascimento VARCHAR NOT NULL,
    cpfcnpj VARCHAR NOT NULL,
    pessoa VARCHAR(2) NOT NULL,
    contato VARCHAR NOT NULL,
    rg VARCHAR NOT NULL,
    senha VARCHAR NOT NULL,
    rua VARCHAR NOT NULL,
    numero VARCHAR NOT NULL,
    complemento VARCHAR NOT NULL,
    bairro VARCHAR NOT NULL,
    cidade VARCHAR NOT NULL,
    estado VARCHAR(2) NOT NULL,
    cep VARCHAR NOT NULL,
    pais VARCHAR NOT NULL,
    tipo_end VARCHAR NOT NULL,
    ddi VARCHAR NULL,
    ddd VARCHAR NOT NULL,
    telefone VARCHAR NOT NULL,
    tipo_tel VARCHAR NULL,
    ramal VARCHAR NULL,
    codigo_externo VARCHAR NULL,
    data TIMESTAMP NOT NULL,
    PRIMARY KEY (codigo)
    );
"""
