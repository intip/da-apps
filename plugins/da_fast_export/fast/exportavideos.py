# -*- coding: latin1 -*-
import random
import datetime

def exportavideos():
##    --Total 79060
##    --ALTER SESSION set NLS_DATE_FORMAT = 'yyyy-mm-dd hh24:mi:ss'
##    SELECT *
##    FROM (
##        SELECT
##          v.TV_VID_ID,                      --0
##          v.TV_VID_NOME,                    --1
##          v.TV_VID_DESCRICAO,               --2
##          v.TV_VID_TAGS,                    --3
##          v.TV_VID_DURACAO,                 --4
##          v.TV_VID_THUMB,                   --5
##          v.TV_VID_COMENTARIOS,             --6
##          v.TV_VID_RATING,                  --7
##          v.TV_VID_DATAPOPULARIDADE,        --8
##          m.TV_TIP_IDSTATUS,                --9
##          m.TV_MID_DATACRIACAO,             --10
##          m.TV_USU_ID,                      --11
##          m.TV_TIP_IDCATEGORIA,             --12
##          u.TV_USU_NOME,                    --13
##          u.TV_USU_LINK,                    --14
##          t.TV_TIP_NOME,                    --15
##          t2.TV_TIP_NOME as TV_TIP_IDORIGEM,--16
##          m.TV_MID_PRIVADO,                 --17
##          u.TV_USU_PATHSTATIC,              --18
##          ROW_NUMBER() OVER ( ORDER BY v.TV_VID_ID ) AS ORARN   --19
##        from TAOVOCE.TV_VID_VIDEO v
##        inner join TAOVOCE.TV_MID_MIDIA m on v.TV_MID_ID = m.TV_MID_ID
##        inner join TAOVOCE.TV_USU_USUARIO u on m.TV_USU_ID = u.TV_USU_ID
##        left join TAOVOCE.TV_TIP_TIPO t on m.TV_TIP_IDCATEGORIA = t.TV_TIP_ID
##        left join TAOVOCE.TV_TIP_TIPO t2 on m.TV_TIP_IDORIGEM = t.TV_TIP_ID
##    ) T1
##    WHERE T1.ORARN BETWEEN 0 AND 10
    import daFastXmlFileVideo
    xmlfile = daFastXmlFileVideo.daFastXmlFileVideo(
        portal='uai',
        origem='vrum'
        )
    f = open('videos.csv','r')
    try:
        inicio = datetime.datetime.now()
        iniciox = datetime.datetime.now()
        totalregistros = 0
        print inicio
        rrr = 0
        for i in f.readlines():
            rrr +=1
            if(i):
                i = i.replace(chr(1),' ')
                i = i.replace(chr(2),' ')
                cols = i.split(';')

                contentid = 'uai_vrum_video_'+cols[0]
                dataexpiracao = None
                datainsercao = cols[10]
                datapublicacao = cols[10]
                dataranking = cols[8]
                secao = cols[15]
                autores = cols[13]
                #converte para segundos o tempo de duração
                tempoduracao = cols[4]
                if(tempoduracao):
                    ss = tempoduracao.strip().split(':')
                    try:
                        tempoduracao = str(int(((int(ss[0])*60)+(int(ss[1]))*60)+float(ss[2])))
                    except:
                        tempoduracao = None
                else: tempoduracao = None
                fontemidia = cols[16]
                titulovideo = cols[1]
                descricaovideo = cols[2]
                statusinterno='0'
                statusativacao='1'
                try:
                    if(int(cols[17])):
                        statusmidiavisivel='1'
                except: statusmidiavisivel='0'
                ranking = cols[7]
                qtdestrelas = cols[7]

                urldestino = 'http://www.dzai.com.br/video/'+str(cols[0])

                urlthumb = ''
                thumb = cols[5]
                if(thumb):
                    thumb = thumb.replace('_preview.jpg','.jpg')
                    urlthumb = 'http://www.dzai.com.br/static/user' + cols[18].strip() +'/'+ thumb

                urlautor = 'http://www.dzai.com.br/'+cols[14]

                #pega as tags validas colocando elas separadas por '#'
                tags = ''
                tagss = cols[3]
                tagss = tagss.lower()
                sde = ' -/01234567890ABCDEFGHIJKLMNOPQRSTUVWXYabcdefghijklmnopqrstuvwxyÁÇÉÍÓÚÀÈÌÒÙÂÊÎÔÛÃÕËÜáçéíóúàèìòùâêîôûãõëü'
                spa = ' -/01234567890abcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyáçéíóúàèìòùâêîôûãõëüáçéíóúàèìòùâêîôûãõëü'
                for i in xrange(0,len(sde)):
                    tagss = tagss.replace(sde[i],spa[i])
                for k in tagss:
                    #se for um caracter valido
                    if k in spa:
                        tags += k
                tags = tags.replace('  ',' ').replace(' ','#')
                xmlfile.add(
                    #ID unico no fast
                    #deve comecar sempre com 'uai_vrum_noticia_' no caso do portal ser uai
                    #deve concatenar com com 'uai_vrum_noticia_' + numero encremental da noticia
                    #deve concatenar com com 'uai_vrum_forum_' + numero encremental do topico do forum
                    #deve concatenar com com 'uai_vrum_blog_' + numero encremental do post do blog
                    contentid=contentid,

                    #Data e hora de expiracao no formato YYYY-MM-DD HH:MM:SS a hora varia de 0 a 23
                    dataexpiracao=dataexpiracao,

                    #Data e hora de insercao no formato YYYY-MM-DD HH:MM:SS a hora varia de 0 a 23
                    datainsercao=datainsercao,

                    #Data e hora de publicacao no formato YYYY-MM-DD HH:MM:SS a hora varia de 0 a 23
                    datapublicacao=datapublicacao,

                    #Data e hora de atualziacao do ranking no formato YYYY-MM-DD HH:MM:SS a hora varia de 0 a 23
                    dataranking=dataranking,

                    #secao: Esporte, Turismo, Lazer, Humor, etc... etc...
                    secao=secao,

                    #Autor do conteudo separados por # se tiver mais de um
                    autores=autores,

                    #Tempo de duracao em segundos
                    tempoduracao=tempoduracao,

                    #Fonte de origem do conteudo
                    fontemidia=fontemidia,

                    #Tags do conteudo
                    tags=tags,

                    #Define se o conteudo foi adicionado por internauta ou usuaro do grupo
                    statusinterno=statusinterno,

                    #Define se o conteudo esta ativo
                    statusativacao=statusativacao,

                    #Define se o conteudo sera visivel ou nao
                    statusmidiavisivel=statusmidiavisivel,

                    #Ranking do conteudo se acordo com os acessos
                    ranking=ranking,

                    #Numero de estrelas do conteudo
                    qtdestrelas=qtdestrelas,

                    #Titulo do conteudo
                    titulovideo=titulovideo,

                    #Descricao
                    descricaovideo=descricaovideo,

                    #URL de destino do destino
                    urldestino=urldestino,

                    #URL thumb da noticia
                    urlthumb=urlthumb,

                    #URL do autor no conteudo se existir
                    urlautor=urlautor
                )
    finally:
        f.close()
        #salva o xml gerado no disco o
        #parametro comments nao e obrigatorio caso passado como True
        # a classe gera um comentario nos elementos do xml
        xmlfile.write(
            'uai_vrum_video_'+
            datetime.datetime.now().strftime('%Y%m%d%H%M')+
        '.xml', comments=True)
    fim = datetime.datetime.now()
    print fim
    print (fim - inicio)

exportavideos()





