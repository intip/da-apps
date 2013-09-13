# -*- encoding: LATIN1 -*-

path_base = 'C:/Documents and Settings/intip/Desktop/tups/Super Esportes - Ao Vivo/aovivo/'

def filtra_xmls():
    import os
    arquivos = os.listdir(path_base)
    for i in arquivos:
        xml_ok = False
        arq = checa_xmls_processados(i)
        if arq:
            try:
                arq_aberto = open(path_base + i, 'rb')
                if(not(len(arq_aberto) == arq['arquivo_bytes'])):
                    xml_ok = checa_campeonatos_h2(i)
            finally:
                arq_aberto.close()
        else:
            xml_ok = checa_campeonatos_h2(i)

        if xml_ok:
            if(i.find('par_') > 0):
                atualiza_partida_xml(i)
            elif(i.find('sts.') > 0):
                atualiza_estatisticas_xml(i)
            elif(i.find('par.') > 0):
                atualiza_resultados_xml(i)
            elif(i.find('tab.') > 0):
                atualiza_classificacao_xml(i)
            elif(i.find('art.') > 0):
                atualiza_artilharia_xml(i)
            elif(i.find('campeonatos') > 0):
                atualiza_campeonatos_xml(i)

filtra_xmls()

#sqls
#  CREATE SCHEMA rschemar;
#
#  CREATE TABLE rschemar.xmls_processados (
#    id_xml SERIAL NOT NULL,
#    nome_xml VARCHAR,
#    bytes_xml,
#    ultima_alteracao TIMESTAMP
#    PRIMARY KEY(id_campeonato_aovivo)
#  );
#select_xmls_processados = ("SELECT id_xml, nome_xml, bytes_xml, ultima_alteracao FROM rschemar.xmls_processados WHERE nome_xml=%(nome_xml)i")
#select_campeonatos_h2 = ("SELECT id_campeonato, id_campeonato_aovivo, nome FROM rschemar.campeonato WHERE id_campeonato_aovivo=%(id_campeonato_aovivo)i")
#insert_xmls_processados = ("INSERT INTO rschemar.xmls_processados (nome_xml, bytes_xml, ultima_alteracao)"
#                    "VALUES (%(nome_xml)s, %(bytes_xml)i, %(ultima_alteracao)s)")
#update_xmls_processados = ("UPDATE rschemar.xmls_processados SET bytes_xml=%(bytes_xml)i, ultima_alteracao=%(ultima_alteracao)s "
#                           "WHERE id_xml=%(id_xml)i")


def checa_xmls_processados(arq_xml):
    return self.execSql("select_xmls_processados",nome_xml=arq_xml)

def checa_campeonatos_h2(arq_xml):
    id_campeonato_aovivo = arq_xml.split('_')[3]
    return self.execSql("select_campeonatos_h2",id_campeonato_aovivo=int(id_campeonato_aovivo))

def atualiza_partida_xml(arq_xml):
    atualiza

def atualiza_estatisticas_xml(arq_xml):
    atualiza

def atualiza_campeonatos_xml(arq_xml):
    atualiza

def insere_xml_processado(arq_xml):
    import datetime
    agora = datetime.datetime.now()
    try:
        arq_aberto = open(path_base + arq_xml, 'rb')
        bytes_xml = len(arq_aberto)
    finally:
        arq_aberto.close()
    xmls_processados = checa_xmls_processados(arq_xml=arq_xml)
    if xmls_processados:
        self.execSqlBatch("update_xmls_processados",
                           bytes_xml=bytes_xml,
                           ultima_alteracao=agora,
                           id_xml=int(xmls_processados['id_xml']))
    else:
        self.execSqlBatch("insert_xmls_processados",
                           nome_xml=arq_xml,
                           bytes_xml=bytes_xml,
                           ultima_alteracao=agora)

def parser_xml_padrao(arq_xml):
    import elementtree.ElementTree as ET
    registros = []
    path_xml = path_base + arq_xml
    try:
        root = ET.parse(path_xml)
    except:
        return ''
    for node in root.getiterator('item'):
        dictSaida = {}
        for n in node:
            dictSaida[n.tag] = n.text
        registros.append(dictSaida)
    return registros

def atualiza_artilharia_xml(arq_xml):
    registros = parser_xml_padrao(arq_xml)
    id_campeonato = arq_xml.split('_')[3]
    for i in registros:
        self.execSqlBatch("insert_artilharia_xml",
                          id_campeonato=int(id_campeonato),
                          nome_jogador=i['jogador'],
                          quantidade_gols=int(i['gols']),
                          time_jogador=i['time'])
    insere_xml_processado(arq_xml=arq_xml)
    self.execSqlCommit()

def atualiza_classificacao_xml(arq_xml):
    registros = parser_xml_padrao(arq_xml)
    id_campeonato = arq_xml.split('_')[3]
    for i in registros:
        self.execSqlBatch("insert_classificacao_xml",
                          id_campeonato=int(id_campeonato),
                          nome_time=i['time'],
                          pontos=int(i['pg']),
                          vitorias=int(i['v']),
                          empates=int(i['e']),
                          derrotas=int(i['d']),
                          gols_marcados=int(i['gp']),
                          qtd_jogos=int(i['j']),
                          gols_sofridos=int(i['gc']),
                          saldo_gols=int(i['sg']))
    insere_xml_processado(arq_xml=arq_xml)
    self.execSqlCommit()

def atualiza_resultados_xml(arq_xml):
    registros = parser_xml_padrao(arq_xml)
    id_campeonato = arq_xml.split('_')[3]
    for i in registros:
        data_hora = i['data'] + i['hora']
        self.execSqlBatch("insert_resultados_xml",
                          id_campeonato=int(id_campeonato),
                          id_partida_aovivo=i['id'],
                          nome_time1=i['time1'],
                          nome_time2=i['time2'],
                          data_hora=data_hora,
                          fase=i['rodada'],
                          estadio=i['estadio'],
                          cidade=i['local'],
                          gols_time1=int(i['gol1']),
                          gols_time2=int(i['gol2']),
                          inicio=int(i['ini']),
                          fim=int(i['fim']))
    insere_xml_processado(arq_xml=arq_xml)
    self.execSqlCommit()