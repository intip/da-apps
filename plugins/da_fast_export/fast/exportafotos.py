# -*- coding: latin1 -*-
#http://admin.estadodeminas.vrum.com.br/veiculos/manage
#http://imgs.vrum.com.br/veiculos/galeriadefoto/
import random
import datetime

def exportanoticias():
    """
    select
    	f.id_foto,                                 --0
    	f.id_galeria,                              --1
    	f.descricao,                               --2
    	f.credito,                                 --3
    	f.imagem_pequena,                          --4
    	f.imagem_grande,                           --5
    	g.titulo as galeria_titulo,                --6
    	g.descricao as galeria_descricao,          --7
    	g.palavrachave as galeria_palavrachave,    --8
    	g.foto as galeria_foto,                    --9
    	g.publicada as galeria_publicada,          --10
    	g.criada_em  as galeria_criada_em          --11
    from foto_galeriadefoto f
    inner join galeria_galeriadefoto g on f.id_galeria = g.id_galeria
    order by f.id_galeria, f.id_foto
    limit <dtml-sqlvar limit type=int>
    offset <dtml-sqlvar offset type=int>
    """
    import daFastXmlFileFoto
    xmlfile = daFastXmlFileFoto.daFastXmlFileFoto(
        portal='uai',
        origem='vrum'
        )
    f = open('fotos.csv','r')
    try:
        inicio = datetime.datetime.now()
        iniciox = datetime.datetime.now()
        totalregistros = 0
        print inicio
        rrr = 0
        for i in f.readlines():
            rrr +=1
            #if(rrr == 1000): continue
            #if(rrr == 2000): break
            if(i):
                i = i.replace(chr(1),' ')
                i = i.replace(chr(2),' ')
                cols = i.split(';')
                #if(not cols[0] in ['20470','25068','26228','26008','27318','26544','35735','40310']):
                #    continue
                contentid = 'uai_vrum_foto_'+cols[0]
                id_foto = cols[0]
                id_galeria = cols[1]

                dataexpiracao = None
                datainsercao = cols[11]
                datapublicacao = cols[11]
                dataranking = None
                secao = None
                autores = cols[3]
                titulogaleria = cols[6]
                tags = cols[8]
                statusinterno = '1'
                statusativacao = '1'
                statusmidiavisivel = '1'
                ranking = None
                qtdestrelas = None
                fontemidia = None
                descricaofoto = cols[2]
                descricaogaleria= cols[7]
                urldestino = 'http://admin.estadodeminas.vrum.com.br/veiculos/modulos/galeriadefoto/galeriadefoto?id_galeria='+str(id_galeria)+'&id_foto' + str(id_foto)
                urlthumb = 'http://imgs.vrum.com.br/veiculos/galeriadefoto/'+ cols[4]
                urlautor = None

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

                    #secao: Moto, Nostalgia, Test
                    secao=secao,

                    #Autor da noticia separados por # se tiver mais de um
                    autores=autores,

                    #Titulo Galeria
                    titulogaleria=titulogaleria,

                    #Tags da noticia
                    tags=tags,


                    #Define se o conteudo foi adicionado por internauta
                    statusinterno=statusinterno,

                    #Define se o conteudo esta ativo
                    statusativacao=statusativacao,

                    #Define se o conteudo sera visivel ou nao
                    statusmidiavisivel=statusmidiavisivel,

                    #Ranking do conteudo se acordo com os acessos
                    ranking=ranking,

                    #Numero de estrelas do conteudo
                    qtdestrelas=qtdestrelas,

                    #Fonte da midia
                    fontemidia=fontemidia,

                    #Descricao da foto
                    descricaofoto=descricaofoto,

                    #Descricao da galeria
                    descricaogaleria=descricaogaleria,

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
            'uai_vrum_foto_'+
            datetime.datetime.now().strftime('%Y%m%d%H%M')+
        '.xml', comments=True)
    fim = datetime.datetime.now()
    print fim
    print (fim - inicio)

exportanoticias()





