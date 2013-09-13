# -*- coding: latin1 -*-
#-------------------------------------------------------------------------------
# @name:
# @purpose:
# @author:      Juliano Hallac" <juliano.hallac@gmail.com>
# @created:     26/10/2010
# @copyright:   (c) Diarrios Associados
# @licence:     GPL
#-------------------------------------------------------------------------------
from daFastXmlFile import daFastXmlFile as _daFastXmlFile

class daFastXmlFileFoto(_daFastXmlFile):
    def __init__(self, portal, origem):
        tipoconteudo = 'foto'
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
            {'dados1'                       : 'bodypart1'},
            {'dados2'                       : 'bodypart2'},
            {'bitmap'                       : 'bitmap'}, #statusativacao_statusinterno_statusmidiavisivel
            {'fontemidia'                   : 'strclassifier9'},
            {'titulogaleria'                : 'strclassifier10'}
        ]
        _daFastXmlFile.__init__(self, portal, origem, tipoconteudo, fields)

    def add(self, contentid,
            dataexpiracao, datainsercao, datapublicacao, dataranking,
            secao, autores, titulogaleria,
            tags,
            statusinterno, statusativacao, statusmidiavisivel,
            ranking, qtdestrelas, fontemidia,
            #dados1
            descricaofoto,
            descricaogaleria,
            #dados2
            urldestino,
            urlthumb,
            #dados2
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

        dados1 = self.getDados(descricaofoto=descricaofoto,
                                descricaogaleria=descricaogaleria)

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
            bitmap=bitmap,
            ranking=ranking,
            qtdestrelas=qtdestrelas,
            dados1=dados1,
            dados2=dados2,

            fontemidia=fontemidia,
            titulogaleria=titulogaleria
        )

if __name__ == '__main__':
    ele = daFastXmlFileFoto('uai','vrum')
    ele.add(
            contentid='vrum_uai_foto_1001',
            dataexpiracao='2001-01-20 14:30:00',
            datainsercao='2000-01-20 14:30:00',
            datapublicacao='2000-01-21 14:30:00',
            dataranking=None,
            secao='Jogos',
            autores='Mario Brothers',
            titulogaleria='Super Mario III',
            descricaofoto='20 anos do melhor jogo de todos os tempos',
            descricaogaleria=None,
            fontemidia='',
            tags='Nintendo#Jogos',
            statusinterno='0',
            statusativacao='1',
            statusmidiavisivel='0',
            ranking=None,
            qtdestrelas='5',
            urldestino='http://www.uai.com.br/morreuhjroris',
            urlthumb='http://www.uai.com.br/morreuhjroris.jpg',
            urlautor=None
    )
    ele.add(
            contentid='vrum_uai_foto_1002',
            dataexpiracao='2008-01-20 14:30:00',
            datainsercao='2006-01-20 14:30:00',
            datapublicacao='2007-01-21 14:30:00',
            dataranking=None,
            secao='Jogos',
            autores='Mario Brothers',
            titulogaleria='Super Mario III',
            descricaofoto='20 anos do melhor jogo de todos os tempos',
            descricaogaleria=None,
            fontemidia='',
            tags='Nintendo#Jogos',
            statusinterno='0',
            statusativacao='1',
            statusmidiavisivel='0',
            ranking=None,
            qtdestrelas='5',
            urldestino='http://www.uai.com.br/supermarioiii',
            urlthumb='http://www.uai.com.br/supermarioiii.jpg',
            urlautor=None
    )
    ele.write('uai_vrum_foto_001.xml', comments=True)

