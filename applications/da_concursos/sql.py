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
    SELECT
        NEXTVAL('rschemar.conteudo_id_conteudo_seq'::text) as id"""

select_status_content = """
    SELECT publicado FROM rschemar.conteudo
      WHERE id_conteudo=%(id_conteudo)i"""

select_dados = """
    SELECT
        N.id_conteudo,
        N.titulo,
        N.descricao,
        N.cargo,
        N.descricao_vagas,
        N.total_vagas,
        N.remuneracao_de,
        N.remuneracao_ate,
        N.vagas_especiais,
        N.descricao_remuneracao,
        N.inscricoes,
        N.banca_organizadora,
        N.cadastro_reserva,
        N.validade_concurso,
        N.previsto,
        N.nivel_escolaridade,
        to_char(N.data_edital, 'DD/MM/YYYY') as data_edital,
        to_char(N.data_inscricao, 'DD/MM/YYYY') as data_inscricao,
        to_char(N.data_fim_inscricao, 'DD/MM/YYYY') as data_fim_inscricao,
        to_char(N.data_prova, 'DD/MM/YYYY') as data_prova,
        to_char(N.data_resultado, 'DD/MM/YYYY') as data_resultado,
        to_char(N.expira_em, 'DD/MM/YYYY HH24:MI') as expira_em,
        to_char(N.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em,
        N.publicado,
        to_char(N.atualizado_em, 'YYYY-MM-DD HH24:MI') as atualizado_em,
        D.id_destaque, D.titulo as titulo_destaque, D.descricao
            as descricao_destaque,
        D.img as imagem_destaque, D.peso as peso_destaque
    FROM rschemar.conteudo N
        LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo)
        WHERE N.id_conteudo=%(id_conteudo)i"""

select_titulo = """
    SELECT titulo FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i"""

select_dublin_core = """
    SELECT
        titulo,
        descricao,
        to_char(atualizado_em, 'YYYY-MM-DD HH24:MI:SS') as atualizado_em,
        to_char(publicado_em, 'YYYY-MM-DD HH24:MI:SS') as publicado_em
    FROM rschemar.conteudo
        WHERE id_conteudo=%(id_conteudo)i"""

select_conteudo = """
    SELECT
        N.id_conteudo,
        N.titulo,
        N.descricao,
        N.cargo,
        N.descricao_vagas,
        N.total_vagas,
        N.remuneracao_de,
        N.remuneracao_ate,
        N.vagas_especiais,
        N.descricao_remuneracao,
        N.inscricoes,
        N.banca_organizadora,
        N.cadastro_reserva,
        N.validade_concurso,
        N.previsto,
        N.nivel_escolaridade,
        to_char(N.data_edital, 'DD/MM/YYYY') as data_edital,
        to_char(N.data_inscricao, 'DD/MM/YYYY') as data_inscricao,
        to_char(N.data_fim_inscricao, 'DD/MM/YYYY') as data_fim_inscricao,
        to_char(N.data_prova, 'DD/MM/YYYY') as data_prova,
        to_char(N.data_resultado, 'DD/MM/YYYY') as data_resultado,
        to_char(N.expira_em, 'DD/MM/YYYY HH24:MI') as expira_em,
        to_char(N.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em,
        N.publicado,
        D.id_destaque, D.titulo as titulo_destaque,
        D.descricao as descricao_destaque,
        D.img as imagem_destaque,
        D.peso as peso_destaque
    FROM rschemar.conteudo N
        LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo)
        WHERE N.id_conteudo=%(id_conteudo)i"""

select_count_novos = """
    SELECT COUNT(*) FROM rschemar.conteudo N
    WHERE (now()>=N.data_edital AND now()<N.data_inscricao);
"""

select_concursos_novos = """
    SELECT
        N.id_conteudo,
        N.titulo,
        N.descricao,
        N.cargo,
        N.descricao_vagas,
        N.total_vagas,
        N.remuneracao_de,
        N.remuneracao_ate,
        N.vagas_especiais,
        N.descricao_remuneracao,
        N.inscricoes,
        N.banca_organizadora,
        N.cadastro_reserva,
        N.validade_concurso,
        N.previsto,
        N.nivel_escolaridade,
        to_char(N.data_edital, 'DD/MM/YYYY') as data_edital,
        to_char(N.data_inscricao, 'DD/MM/YYYY') as data_inscricao,
        to_char(N.data_fim_inscricao, 'DD/MM/YYYY') as data_fim_inscricao,
        to_char(N.data_prova, 'DD/MM/YYYY') as data_prova,
        to_char(N.data_resultado, 'DD/MM/YYYY') as data_resultado,
        to_char(N.expira_em, 'DD/MM/YYYY HH24:MI') as expira_em,
        to_char(N.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em,
        N.publicado,
        D.id_destaque, D.titulo as titulo_destaque,
        D.descricao as descricao_destaque,
        D.img as imagem_destaque,
        D.peso as peso_destaque
    FROM rschemar.conteudo N
        LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo)
        WHERE (now()>=N.data_edital AND now()<N.data_inscricao)
        AND N.previsto=false AND N.publicado=true"""

select_concursos = """
    SELECT
        N.id_conteudo,
        N.titulo,
        N.descricao,
        N.cargo,
        N.descricao_vagas,
        N.total_vagas,
        N.remuneracao_de,
        N.remuneracao_ate,
        N.vagas_especiais,
        N.descricao_remuneracao,
        N.inscricoes,
        N.banca_organizadora,
        N.cadastro_reserva,
        N.validade_concurso,
        N.previsto,
        N.nivel_escolaridade,
        to_char(N.data_edital, 'DD/MM/YYYY') as data_edital,
        to_char(N.data_inscricao, 'DD/MM/YYYY') as data_inscricao,
        to_char(N.data_fim_inscricao, 'DD/MM/YYYY') as data_fim_inscricao,
        to_char(N.data_prova, 'DD/MM/YYYY') as data_prova,
        to_char(N.data_resultado, 'DD/MM/YYYY') as data_resultado,
        to_char(N.expira_em, 'DD/MM/YYYY HH24:MI') as expira_em,
        to_char(N.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em,
        N.publicado,
        D.id_destaque, D.titulo as titulo_destaque,
        D.descricao as descricao_destaque,
        D.img as imagem_destaque,
        D.peso as peso_destaque
    FROM rschemar.conteudo N
        LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo)
        WHERE N.publicado=true LIMIT %(limit)i OFFSET %(offset)i"""

select_count_inscricoes = """
    SELECT COUNT(*) FROM rschemar.conteudo N
    WHERE (now() BETWEEN N.data_inscricao AND N.data_fim_inscricao);
"""

select_concursos_inscricoes = """
    SELECT
        N.id_conteudo,
        N.titulo,
        N.descricao,
        N.cargo,
        N.descricao_vagas,
        N.total_vagas,
        N.remuneracao_de,
        N.remuneracao_ate,
        N.vagas_especiais,
        N.descricao_remuneracao,
        N.inscricoes,
        N.banca_organizadora,
        N.cadastro_reserva,
        N.validade_concurso,
        N.previsto,
        N.nivel_escolaridade,
        to_char(N.data_edital, 'DD/MM/YYYY') as data_edital,
        to_char(N.data_inscricao, 'DD/MM/YYYY') as data_inscricao,
        to_char(N.data_fim_inscricao, 'DD/MM/YYYY') as data_fim_inscricao,
        to_char(N.data_prova, 'DD/MM/YYYY') as data_prova,
        to_char(N.data_resultado, 'DD/MM/YYYY') as data_resultado,
        to_char(N.expira_em, 'DD/MM/YYYY HH24:MI') as expira_em,
        to_char(N.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em,
        N.publicado,
        D.id_destaque, D.titulo as titulo_destaque,
        D.descricao as descricao_destaque,
        D.img as imagem_destaque,
        D.peso as peso_destaque
    FROM rschemar.conteudo N
        LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo)
        WHERE (now() BETWEEN N.data_inscricao AND N.data_fim_inscricao)
        AND N.previsto=false AND N.publicado=true
        LIMIT %(limit)i OFFSET %(offset)i"""

select_count_andamentos = """
    SELECT COUNT(*) FROM rschemar.conteudo N
    WHERE (now()>N.data_fim_inscricao AND now()<N.data_resultado);
"""

select_concursos_andamentos = """
    SELECT
        N.id_conteudo,
        N.titulo,
        N.descricao,
        N.cargo,
        N.descricao_vagas,
        N.total_vagas,
        N.remuneracao_de,
        N.remuneracao_ate,
        N.vagas_especiais,
        N.descricao_remuneracao,
        N.inscricoes,
        N.banca_organizadora,
        N.cadastro_reserva,
        N.validade_concurso,
        N.previsto,
        N.nivel_escolaridade,
        to_char(N.data_edital, 'DD/MM/YYYY') as data_edital,
        to_char(N.data_inscricao, 'DD/MM/YYYY') as data_inscricao,
        to_char(N.data_fim_inscricao, 'DD/MM/YYYY') as data_fim_inscricao,
        to_char(N.data_prova, 'DD/MM/YYYY') as data_prova,
        to_char(N.data_resultado, 'DD/MM/YYYY') as data_resultado,
        to_char(N.expira_em, 'DD/MM/YYYY HH24:MI') as expira_em,
        to_char(N.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em,
        N.publicado,
        D.id_destaque, D.titulo as titulo_destaque,
        D.descricao as descricao_destaque,
        D.img as imagem_destaque,
        D.peso as peso_destaque
    FROM rschemar.conteudo N
        LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo)
        WHERE (now()>N.data_fim_inscricao AND now()<N.data_resultado)
        AND N.previsto=false AND N.publicado=true
        LIMIT %(limit)i OFFSET %(offset)i"""

select_count_previstos = """
    SELECT COUNT(*) FROM rschemar.conteudo N
    WHERE N.previsto=true AND N.publicado=true;
"""

select_concursos_previstos = """
    SELECT
        N.id_conteudo,
        N.titulo,
        N.descricao,
        N.cargo,
        N.descricao_vagas,
        N.total_vagas,
        N.remuneracao_de,
        N.remuneracao_ate,
        N.vagas_especiais,
        N.descricao_remuneracao,
        N.inscricoes,
        N.banca_organizadora,
        N.cadastro_reserva,
        N.validade_concurso,
        N.previsto,
        N.nivel_escolaridade,
        to_char(N.data_edital, 'DD/MM/YYYY') as data_edital,
        to_char(N.expira_em, 'DD/MM/YYYY HH24:MI') as expira_em,
        to_char(N.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em,
        N.publicado,
        D.id_destaque, D.titulo as titulo_destaque,
        D.descricao as descricao_destaque,
        D.img as imagem_destaque,
        D.peso as peso_destaque
    FROM rschemar.conteudo N
        LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo)
        WHERE N.previsto=true AND N.publicado=true
        LIMIT %(limit)i OFFSET %(offset)i"""

select_count_finalizados = """
    SELECT COUNT(*) FROM rschemar.conteudo N
    WHERE (now()>N.data_resultado);
"""

select_concursos_finalizados = """
    SELECT
        N.id_conteudo,
        N.titulo,
        N.descricao,
        N.cargo,
        N.descricao_vagas,
        N.total_vagas,
        N.remuneracao_de,
        N.remuneracao_ate,
        N.vagas_especiais,
        N.descricao_remuneracao,
        N.inscricoes,
        N.banca_organizadora,
        N.cadastro_reserva,
        N.validade_concurso,
        N.previsto,
        N.nivel_escolaridade,
        to_char(N.data_edital, 'DD/MM/YYYY') as data_edital,
        to_char(N.data_inscricao, 'DD/MM/YYYY') as data_inscricao,
        to_char(N.data_fim_inscricao, 'DD/MM/YYYY') as data_fim_inscricao,
        to_char(N.data_prova, 'DD/MM/YYYY') as data_prova,
        to_char(N.data_resultado, 'DD/MM/YYYY') as data_resultado,
        to_char(N.expira_em, 'DD/MM/YYYY HH24:MI') as expira_em,
        to_char(N.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em,
        N.publicado,
        D.id_destaque, D.titulo as titulo_destaque,
        D.descricao as descricao_destaque,
        D.img as imagem_destaque,
        D.peso as peso_destaque
    FROM rschemar.conteudo N
        LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo)
        WHERE (now()>N.data_resultado)
        AND N.previsto=false AND N.publicado=true
        LIMIT %(limit)i OFFSET %(offset)i"""

select_count_favoritos = """
    SELECT COUNT(*) FROM rschemar.conteudo N
    WHERE U.email=%(email)s;
"""

select_concursos_favoritos = """
    SELECT
        N.id_conteudo,
        N.titulo,
        N.descricao,
        N.cargo,
        N.descricao_vagas,
        N.total_vagas,
        N.remuneracao_de,
        N.remuneracao_ate,
        N.vagas_especiais,
        N.descricao_remuneracao,
        N.inscricoes,
        N.banca_organizadora,
        N.cadastro_reserva,
        N.validade_concurso,
        N.previsto,
        N.nivel_escolaridade,
        to_char(N.data_edital, 'DD/MM/YYYY') as data_edital,
        to_char(N.data_inscricao, 'DD/MM/YYYY') as data_inscricao,
        to_char(N.data_fim_inscricao, 'DD/MM/YYYY') as data_fim_inscricao,
        to_char(N.data_prova, 'DD/MM/YYYY') as data_prova,
        to_char(N.data_resultado, 'DD/MM/YYYY') as data_resultado,
        to_char(N.expira_em, 'DD/MM/YYYY HH24:MI') as expira_em,
        to_char(N.publicado_em, 'DD/MM/YYYY HH24:MI') as publicado_em,
        N.publicado,
        D.id_destaque, D.titulo as titulo_destaque,
        D.descricao as descricao_destaque,
        D.img as imagem_destaque,
        D.peso as peso_destaque
    FROM rschemar.conteudo N
        LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo)
        RIGHT JOIN rschemar.favoritos F ON (N.id_conteudo=F.id_conteudo)
        RIGHT JOIN rschemar.usuarios U ON (U.id_usuario=F.id_usuario)
        WHERE U.email=%(email)s
        LIMIT %(limit)i OFFSET %(offset)i"""

select_estados = """
    SELECT
        id_estado,
        nome,
        sigla
    FROM rschemar.estados ORDER BY nome ASC"""

select_user_id_wad = """
    SELECT
        U.id_usuario,
        U.id_usuario_wad,
        U.email,
        U.nome
    FROM rschemar.usuarios U
         WHERE U.id_usuario_wad=%(id_usuario_wad)s"""

select_user_email = """
    SELECT
        U.id_usuario,
        U.id_usuario_wad,
        U.nome,
        U.email
    FROM rschemar.usuarios U
         WHERE U.email=%(email)s"""

select_estados_concurso = """
    SELECT
        C.id_estado,
        E.nome
    FROM rschemar.estados_conteudo C
        LEFT JOIN rschemar.estados E ON (C.id_estado=E.id_estado)
        WHERE C.id_conteudo=%(id_conteudo)i"""

select_file = """
    SELECT
        id_arquivo,
        titulo,
        arquivo,
        tipo,
        permissao,
        categoria,
        descricao
    FROM rschemar.arquivos WHERE id_conteudo=%(id_conteudo)i"""

select_provas = """
    SELECT
        id_arquivo,
        titulo,
        arquivo,
        tipo,
        permissao,
        categoria,
        descricao
    FROM rschemar.arquivos
        WHERE tipo ='prova' AND permissao = 'livre'
    LIMIT %(limit)i OFFSET %(offset)i"""

select_provas_total="""
    SELECT COUNT(*) 
    FROM rschemar.arquivos
        WHERE tipo = %(docs)s AND permissao = 'livre'

"""

select_files = """
    SELECT
        id_arquivo,
        titulo,
        arquivo,
        tipo,
        permissao,
        categoria,
        descricao
    FROM rschemar.arquivos
        WHERE tipo ='documento' AND permissao = 'livre'
    LIMIT %(limit)i OFFSET %(offset)i"""

select_restricted_files = """
    SELECT
        id_arquivo,
        titulo,
        arquivo,
        tipo,
        permissao,
        categoria,
        descricao
    FROM rschemar.arquivos WHERE permissao='restrito'"""

select_soma_vagas = """
    SELECT
        sum(total_vagas)
    FROM
        rschemar.conteudo"""

select_soma_concursos_filtro = """
    SELECT
        sum(total_vagas)
    FROM rschemar.conteudo N
        LEFT JOIN rschemar.destaque D ON (N.id_conteudo=D.id_conteudo)
        WHERE ((now()>=N.data_edital AND now()<N.data_inscricao
                AND N.previsto=false)
               OR (now() BETWEEN N.data_inscricao AND N.data_fim_inscricao
                   AND N.previsto=false)
               OR (now()>N.data_fim_inscricao AND now()<N.data_resultado
                   AND N.previsto=false)
               OR (now()>N.data_resultado
                   AND N.previsto=false)
               OR (N.previsto=true))
        AND N.publicado=true"""

insert_conteudo = """
    INSERT INTO rschemar.conteudo (id_conteudo, descricao_vagas,
        total_vagas, remuneracao_de, remuneracao_ate, titulo,
        descricao, publicado_em, expira_em, publicado,
        cargo, vagas_especiais, descricao_remuneracao, inscricoes,
        banca_organizadora, cadastro_reserva, validade_concurso, previsto,
        nivel_escolaridade, data_edital, data_inscricao, data_fim_inscricao,
        data_prova, data_resultado)
    VALUES
        (%(id_conteudo)i, %(descricao_vagas)s, %(total_vagas)s,
         %(remuneracao_de)s, %(remuneracao_ate)s, %(titulo)s,
         %(descricao)s, %(publicado_em)s, %(expira_em)s, %(publicado)s,
         %(cargo)s, %(vagas_especiais)s,
         %(descricao_remuneracao)s, %(inscricoes)s, %(banca_organizadora)s,
         %(cadastro_reserva)s, %(validade_concurso)s, %(previsto)s,
         %(nivel_escolaridade)s, %(data_edital)s, %(data_inscricao)s,
         %(data_fim_inscricao)s, %(data_prova)s, %(data_resultado)s)"""

insert_favorito = """
    INSERT INTO rschemar.favoritos (id_conteudo, id_usuario, data)
    VALUES (%(id_conteudo)i, %(id_usuario)i, %(data)s)"""

insert_destaque = """
    INSERT INTO rschemar.destaque (id_conteudo,
        titulo, descricao, img, peso)
    VALUES
        (%(id_conteudo)i, %(titulo)s, %(descricao)s, %(img)s, %(peso)i)"""

insert_arquivo = """
    INSERT INTO rschemar.arquivos (id_conteudo,
        titulo, arquivo, tipo, permissao, categoria, descricao)
    VALUES
        (%(id_conteudo)i, %(titulo)s, %(arquivo)s, %(tipo)s, %(permissao)s,
         %(categoria)s, %(descricao)s)"""

insert_estados_concurso = """
    INSERT INTO rschemar.estados_conteudo (id_conteudo,
      id_estado)
    VALUES
       (%(id_conteudo)i, %(id_estado)i)"""

insert_usuario = """
    INSERT INTO rschemar.usuarios (id_usuario_wad,
      email, nome)
    VALUES
      (%(id_usuario_wad)i, %(email)s, %(nome)s)"""

update_conteudo = """
    UPDATE rschemar.conteudo
        SET titulo=%(titulo)s,
         descricao=%(descricao)s,
         publicado_em=%(publicado_em)s,
         cargo=%(cargo)s,
         remuneracao_de=%(remuneracao_de)s,
         remuneracao_ate=%(remuneracao_ate)s,
         total_vagas=%(total_vagas)s,
         descricao_vagas=%(descricao_vagas)s,
         vagas_especiais=%(vagas_especiais)s,
         previsto=%(previsto)s,
         descricao_remuneracao=%(descricao_remuneracao)s,
         inscricoes=%(inscricoes)s,
         banca_organizadora=%(banca_organizadora)s,
         cadastro_reserva=%(cadastro_reserva)s,
         validade_concurso=%(validade_concurso)s,
         nivel_escolaridade=%(nivel_escolaridade)s,
         data_edital=%(data_edital)s,
         data_inscricao=%(data_inscricao)s,
         data_fim_inscricao=%(data_fim_inscricao)s,
         data_prova=%(data_prova)s,
         data_resultado=%(data_resultado)s,
         expira_em=%(expira_em)s,
         publicado=%(publicado)s
    WHERE id_conteudo=%(id_conteudo)i"""

delete_conteudo = """
    DELETE FROM rschemar.conteudo WHERE id_conteudo=%(id_conteudo)i"""

delete_destaque = """
    DELETE FROM rschemar.destaque WHERE id_conteudo=%(id_conteudo)i"""

delete_arquivos = """
    DELETE FROM rschemar.arquivos WHERE id_conteudo=%(id_conteudo)i"""

delete_estados_conteudo = """
    DELETE FROM rschemar.estados_conteudo WHERE id_conteudo=%(id_conteudo)i"""

delete_favorito = """
    DELETE FROM rschemar.favoritos
    WHERE id_conteudo=%(id_conteudo)i AND id_usuario=%(id_usuario)i"""

permissions = """
    GRANT USAGE ON SCHEMA rschemar TO %(user)s;
    GRANT SELECT ON rschemar.conteudo TO %(user)s;
    GRANT SELECT ON rschemar.destaque TO %(user)s;
    GRANT SELECT ON rschemar.estados TO %(user)s;
    GRANT SELECT ON rschemar.arquivos TO %(user)s;
    GRANT SELECT ON rschemar.usuarios TO %(user)s;
    GRANT SELECT ON rschemar.estados_conteudo TO %(user)s"""


permissions_admin = permissions

structure = """
  CREATE SCHEMA rschemar;

  CREATE TABLE rschemar.estados (
     id_estado SERIAL NOT NULL,
     nome VARCHAR NOT NULL,
     sigla VARCHAR NOT NULL,
     PRIMARY KEY(id_estado)
  );

  CREATE TABLE rschemar.conteudo (
    id_conteudo SERIAL NOT NULL,
    id_idioma INTEGER DEFAULT 102,
    titulo VARCHAR NOT NULL,
    cargo VARCHAR NULL,
    total_vagas INTEGER NULL,
    descricao_vagas VARCHAR NULL,
    vagas_especiais VARCHAR NULL,
    remuneracao_de INTEGER NULL,
    remuneracao_ate INTEGER NULL,
    descricao_remuneracao VARCHAR NULL,
    inscricoes VARCHAR NULL,
    banca_organizadora VARCHAR NULL,
    cadastro_reserva VARCHAR NULL,
    validade_concurso VARCHAR NULL,
    previsto BOOL NOT NULL DEFAULT 'False',
    nivel_escolaridade VARCHAR NULL,
    data_edital TIMESTAMP NULL,
    data_inscricao TIMESTAMP NULL,
    data_fim_inscricao TIMESTAMP NULL,
    data_prova TIMESTAMP NULL,
    data_resultado TIMESTAMP NULL,
    descricao VARCHAR NULL,
    publicado BOOL NOT NULL DEFAULT 'False',
    expira_em TIMESTAMP NULL,
    publicado_em TIMESTAMP NOT NULL,
    atualizado_em TIMESTAMP NULL,
    exportado BOOLEAN DEFAULT 'False',
    PRIMARY KEY(id_conteudo)
  );

  CREATE TABLE rschemar.arquivos (
    id_arquivo SERIAL NOT NULL,
    id_conteudo INT NOT NULL,
    titulo VARCHAR NULL,
    arquivo VARCHAR NOT NULL,
    permissao VARCHAR NOT NULL,
    tipo VARCHAR NOT NULL,
    categoria VARCHAR NULL,
    descricao VARCHAR NULL,
    PRIMARY KEY(id_arquivo),
    FOREIGN KEY(id_conteudo)
      REFERENCES rschemar.conteudo(id_conteudo)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );

  CREATE TABLE rschemar.usuarios (
    id_usuario SERIAL NOT NULL,
    id_usuario_wad BIGINT NOT NULL,
    email VARCHAR NOT NULL,
    nome VARCHAR NOT NULL,
    PRIMARY KEY(id_usuario)
  );

  CREATE TABLE rschemar.favoritos (
    id_favorito SERIAL NOT NULL,
    id_conteudo INT NOT NULL,
    id_usuario BIGINT NOT NULL,
    data TIMESTAMP NOT NULL,
    PRIMARY KEY(id_favorito),
    FOREIGN KEY(id_conteudo)
      REFERENCES rschemar.conteudo(id_conteudo)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY(id_usuario)
      REFERENCES rschemar.usuarios(id_usuario)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );

  CREATE TABLE rschemar.estados_conteudo (
    id_estado_conteudo SERIAL NOT NULL,
    id_conteudo INT NOT NULL,
    id_estado INT NOT NULL,
    PRIMARY KEY(id_estado_conteudo),
    FOREIGN KEY(id_conteudo)
      REFERENCES rschemar.conteudo(id_conteudo)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY(id_estado)
      REFERENCES rschemar.estados(id_estado)
        ON DELETE CASCADE
        ON UPDATE CASCADE
  );

  CREATE INDEX rschemar_conteudo_publicado_index
    ON rschemar.conteudo USING btree (publicado);
  CREATE INDEX rschemar_conteudo_publicado_em_index
    ON rschemar.conteudo USING btree (publicado_em);
  CREATE INDEX rschemar_conteudo_expira_em_index
    ON rschemar.conteudo USING btree (expira_em);

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
  CREATE INDEX rschemar_destaque_id_conteudo_index
    ON rschemar.destaque USING btree (id_conteudo);

  INSERT INTO rschemar.estados (nome, sigla) VALUES
    ('Acre', 'AC'),
    ('Alagoas', 'AL'),
    ('Amazonas', 'AM'),
    ('Amap&aacute;', 'AP'),
    ('Bahia', 'BA'),
    ('Cear&aacute', 'CE'),
    ('Distrito Federal', 'DF'),
    ('Esp&iaacute;rito Santo', 'ES'),
    ('Goi&aacute;s', 'GO'),
    ('Maranh&atilde;o', 'MA'),
    ('Minas Gerais', 'MG'),
    ('Mato Grosso do Sul', 'MS'),
    ('Mato Grosso', 'MT'),
    ('Par&aacute', 'PA'),
    ('Para&iacute;ba', 'PB'),
    ('Pernambuco', 'PE'),
    ('Piau&iacute', 'PI'),
    ('Paran&aacute', 'PR'),
    ('Rio de Janeiro', 'RJ'),
    ('Rio Grande do Norte', 'RN'),
    ('Rond&ocirc;nia', 'RO'),
    ('Roraima', 'RR'),
    ('Rio Grande do Sul', 'RS'),
    ('Santa Catarina', 'SC'),
    ('Sergipe', 'SE'),
    ('S&atilde;o Paulo', 'SP'),
    ('Tocantins', 'TO');
"""
