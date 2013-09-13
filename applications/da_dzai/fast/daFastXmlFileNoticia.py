# -*- coding: latin1 -*-
#-------------------------------------------------------------------------------
# @name:
# @purpose:
# @author:      SleX - slex@slex.com.br
# @created:     26/10/2010
# @copyright:   (c) Diarrios Associados
# @licence:     GPL
#-------------------------------------------------------------------------------
from daFastXmlFile import daFastXmlFile as _daFastXmlFile

class daFastXmlFileNoticia(_daFastXmlFile):
    def __init__(self, portal, origem, tipoconteudo):
        #'recall',
        if (not tipoconteudo in ['noticia','fichatecnica','topicoforum','postblog','recall']):
            raise Exception('tipoconteudo deve ser noticia ou forum ou blog ou fichatecnica')
        fields = [
            {'contentid'                    : 'documentid'},
            {'portal'                       : 'strclassifier5'},#VRUM
            {'origem'                       : 'strclassifier8'},#UAI / CB
            {'tipoconteudo'                 : 'strclassifier7'},
            {'dataexpiracao'                : 'date1'},
            {'datainsercao'                 : 'date2'},
            {'datapublicacao'               : 'date3'},
            {'dataranking'                  : 'date4'},
            {'secao'                        : 'strclassifier6'},
            {'autores'                      : 'strclassifier1'},
            {'tags'                         : 'keywords'},
            {'ranking'                      : 'floataggregate1'},
            {'qtdestrelas'                  : 'floatclassifier2'},
            {'dados1'                       : 'bodypart1'},                     #titulo,categoria,resumo,tituloblog
            {'dados2'                       : 'bodypart2'},                     #urldestino,urlthumb,urlautor
            {'bitmap'                       : 'bitmap'},                        #statusativacao_statusinterno_statusmidiavisivel
            {'qtdcomentarios'               : 'intaggregate2'},
            {'corpoconteudo'                : 'straggregate1'},
            {'tagsrelacionadas'             : 'generic1'}                       #modelobase,palavraschave,codigomoelo


        ]
        _daFastXmlFile.__init__(self, portal, origem, tipoconteudo, fields)

    def add(self,
            contentid,
            dataexpiracao, datainsercao, datapublicacao, dataranking,
            secao,
            autores,
            corpoconteudo,
            tags,
            tagsrelacionadas,
            statusinterno,
            statusativacao,
            statusmidiavisivel,
            ranking,
            qtdestrelas,
            qtdcomentarios,
            titulo,
            categoria,
            resumo,
            urldestino,
            urlthumb,
            tituloblog=None,
            idblog=None,
            urlautor=None):
        """
        @purpose:
        @return: True
        """
        dataexpiracao = self.getDtFrm(dataexpiracao)
        datainsercao = self.getDtFrm(datainsercao)
        datapublicacao = self.getDtFrm(datapublicacao)
        dataranking = self.getDtFrm(dataranking)

        if(not(dataexpiracao)): dataexpiracao = "2200-01-01T00:00:00"
        if(not(datapublicacao)): datapublicacao = "1950-01-01T00:00:00"

        tags = self.getSeparetor(tags,'#')
        autores = self.getSeparetor(autores,'#')

        statusinterno = self.getStatus(statusinterno, isnull=True)
        statusativacao = self.getStatus(statusativacao)
        statusmidiavisivel = self.getStatus(statusmidiavisivel, isnull=True)

        ranking = self.getInt(ranking, isnull=True)
        qtdestrelas = self.getInt(qtdestrelas, isnull=True, pmin=0, pmax=5)
        qtdcomentarios = self.getInt(qtdcomentarios, isnull=True, pmin=0)

        dados1 = self.getDados(titulo=titulo,categoria=categoria,
                    resumo=resumo,tituloblog=tituloblog,idblog=idblog)

        dados2 = self.getDados(
            urldestino=urldestino,
            urlthumb=urlthumb,
            urlautor=urlautor)

        bitmap = self.getBitmap(
            statusativacao,
            statusinterno,
            statusmidiavisivel,
            '1',
            numelements=4)

        _daFastXmlFile.add(self,
            contentid=contentid,
            dataexpiracao=dataexpiracao,
            datainsercao=datainsercao,
            datapublicacao=datapublicacao,
            dataranking=dataranking,
            secao=secao,
            autores=autores,
            tags=tags,
            tagsrelacionadas=tagsrelacionadas,
            bitmap=bitmap,
            ranking=ranking,
            qtdestrelas=qtdestrelas,
            qtdcomentarios=qtdcomentarios,
            dados1=dados1,
            dados2=dados2,
            corpoconteudo=corpoconteudo
        )

if __name__ == '__main__':
    ele = daFastXmlFileAnuncioVrum('uai','vrum','noticia')
    ele.add(
            contentid='vrum_uai_noticia_1001',
            dataexpiracao='2001-01-20 14:30:00',
            datainsercao='2000-01-20 14:30:00',
            datapublicacao='2000-01-21 14:30:00',
            dataranking=None,
            secao='Politica',
            autores='Carlos Drummond de Andrades',
            corpoconteudo="""Morreu hj o governador Roriz bla bla bla bla bla
bal blalbla shd wbiudasjdnaius awe l\\bsWN EDH BASMDNQJW
BASMDNQJWbal blalbla shd wbiudasjdnaius awe l\\bsWN EDH.""",
            tags='Morte#Governador#Politica',
            statusinterno='0',
            statusativacao='1',
            statusmidiavisivel='0',
            ranking=None,
            qtdestrelas='3',
            qtdcomentarios='1209809',
            titulo='Morreu hj o governador Roriz',
            categoria='Politica',
            resumo='Morreu hj o governador Roriz de madrugada em acidente.',
            urldestino='http://www.uai.com.br/morreuhjroris',
            urlthumb='http://www.uai.com.br/morreuhjroris.jpg',
            tituloblog=None,
            urlautor=None
    )
    ele.add(
            contentid='vrum_uai_noticia_1002',
            dataexpiracao='2001-01-20 14:30:00',
            datainsercao='2000-01-20 14:30:00',
            datapublicacao='2000-01-21 14:30:00',
            dataranking=None,
            secao='Politica',
            autores='Carlos Drummond de Andrades#SleX Luthor',
            corpoconteudo="""Morreu hj o governador Roriz bla bla bla bla bla
bal blalbla shd wbiudasjdnaius awe l\\bsWN EDH BASMDNQJW
BASMDNQJWbal blalbla shd wbiudasjdnaius awe l\\bsWN EDH.""",
            tags='Morte#Governador#Politica',
            statusinterno='0',
            statusativacao='1',
            statusmidiavisivel='0',
            ranking='20032',
            qtdestrelas='3',
            qtdcomentarios='1209809',
            titulo='Morreu hj o <html></html>governador Roriz',
            categoria='Politica',
            resumo='Morreu hj o governador Roriz de madrugada em acidente.',
            urldestino='http://www.uai.com.br/morreuhjroris',
            urlthumb='http://www.uai.com.br/morreuhjroris.jpg',
            tituloblog=None,
            urlautor=None
    )
    ele.write('vrum_uai_noticia_001.xml', comments=True)
    #forum
    ele = daFastXmlFileNoticiaTopicoForum('uai','vrum','forum')
    ele.add(
            contentid='vrum_uai_forum_1001',
            dataexpiracao='2001-01-20 14:30:00',
            datainsercao='2000-01-20 14:30:00',
            datapublicacao='2000-01-21 14:30:00',
            dataranking=None,
            secao='Politica',
            autores='Carlos Drummond de Andrades',
            corpoconteudo="""Morreu hj o governador Roriz bla bla bla bla bla
bal blalbla shd wbiudasjdnaius awe l\\bsWN EDH BASMDNQJW
BASMDNQJWbal blalbla shd wbiudasjdnaius awe l\\bsWN EDH.""",
            tags='Morte#Governador#Politica',
            statusinterno='0',
            statusativacao='1',
            statusmidiavisivel='0',
            ranking=None,
            qtdestrelas='3',
            qtdcomentarios='1209809',
            titulo='Morreu hj o governador Roriz',
            categoria='Politica',
            resumo='Morreu hj o governador Roriz de madrugada em acidente.',
            urldestino='http://www.uai.com.br/morreuhjroris',
            urlthumb='http://www.uai.com.br/morreuhjroris.jpg',
            tituloblog=None,
            urlautor=None
    )
    ele.add(
            contentid='vrum_uai_forum_1002',
            dataexpiracao='2001-01-20 14:30:00',
            datainsercao='2000-01-20 14:30:00',
            datapublicacao='2000-01-21 14:30:00',
            dataranking=None,
            secao='Politica',
            autores='Carlos Drummond de Andrades#SleX Luthor',
            corpoconteudo="""Morreu hj o governador Roriz bla bla bla bla bla
bal blalbla shd wbiudasjdnaius awe l\\bsWN EDH BASMDNQJW
BASMDNQJWbal blalbla shd wbiudasjdnaius awe l\\bsWN EDH.""",
            tags='Morte#Governador#Politica',
            statusinterno='0',
            statusativacao='1',
            statusmidiavisivel='0',
            ranking='20032',
            qtdestrelas='3',
            qtdcomentarios='1209809',
            titulo='Morreu hj o <html></html>governador Roriz',
            categoria='Politica',
            resumo='Morreu hj o governador Roriz de madrugada em acidente.',
            urldestino='http://www.uai.com.br/morreuhjroris',
            urlthumb='http://www.uai.com.br/morreuhjroris.jpg',
            tituloblog=None,
            urlautor=None
    )
    ele.write('vrum_uai_forum_001.xml', comments=True)

