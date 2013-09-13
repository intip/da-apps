# -*- coding: latin1 -*-
import random
import datetime

def exportanoticias():
##    select
##    	n.id_noticias,             --0
##    	n.id_sessoes,              --1
##    	n.titulo,                  --2
##    	n.bigode,                  --3
##    	n.corpo,                   --4
##    	n.publicado,               --5
##    	n.expira,                  --6
##    	n.estado,                  --7
##    	n.fixar,                   --8
##    	n.fabricante,              --9
##    	n.modelo,                  --10
##    	n.ano,                     --11
##    	n.fabmodano,               --12
##    	n.fipe,                    --13
##    	s.nome as nome_sessao,     --14
##    	p.nome as nome_parceiro    --15
##    from public.noticias n
##    left join public.sessoes s on n.id_sessoes = s.id_sessoes
##    left join public.parceiros p on s.id_parceiros = p.id_parceiros
##    where p.id_parceiros = <dtml-sqlvar id_parceiros type=int>
##    order by id_noticias
##    limit <dtml-sqlvar limit type=int>
##    offset <dtml-sqlvar offset type=int>
    import daFastXmlFileNoticia
    #Tipoconteudo pode ser 'noticia','forum','blog','fichatecnica'
    #blog = post de blog
    #forum = topico de forum
    #Abaixo seque exemplo de exportacao de um xml de noticia
    #pra os demais e so segui o modelo, lembrando que alguns campos seram
    #definidos somente para alguns tipos de conteudos.
    #exe.: tituloblog
    xmlfile = daFastXmlFileNoticia.daFastXmlFileNoticia(
        portal='uai',
        origem='vrum',
        tipoconteudo='noticia'
        )
    f = open('noticias.csv','r')
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
                contentid = 'uai_vrum_noticia_'+cols[0]
                if(cols[5]):    cols[5] = cols[5][:19].replace('/','-')
                if(cols[6]):    cols[6] = cols[6][:19].replace('/','-')
                dataexpiracao = cols[6]
                datainsercao = cols[5]
                datapublicacao = cols[5]
                dataranking = None
                secao = cols[14]
                autors = {}
                for i in xrange(0,random.randint(0,5)):
                    autors[random.choice(('Alexandre Villela','Marcelo Galvao','Juliano Hallac'))] = 1
                autores = str('#').join(autors)
                corpoconteudo = cols[4]
                #deve pegar o novo campo tag e atravez
                tags = cols[9] + ' ' + cols[10] + ' ' + cols[11] + ' ' + cols[12] + ' ' + cols[13]
                tags = tags.strip().replace('  ',' ')
                #campos do ano
                        #n.fabricante,              --9
                        #n.modelo,                  --10
                        #n.ano,                     --11
                        #n.fabmodano,               --12
        	            #n.fipe,                    --13
                tagsrelacionadas = cols[9] + ' ' + cols[10] + ' ' + cols[11] + ' ' + cols[12] + ' ' + cols[13]
                tagsrelacionadas = tagsrelacionadas.strip().replace('  ',' ')
                statusinterno = '1'
                if(cols[7]=='P'):   statusativacao = '1'
                else:               statusativacao = '0'
                statusmidiavisivel = '1'
                ranking = str(random.randint(0,1000))
                qtdestrelas = random.randint(0,5)
                qtdcomentarios = random.randint(0,1000)
                titulo = cols[2]
                categoria = None
                resumo = cols[3]
                urldestino = 'http://noticias.vrum.com.br/veiculos/'+ \
                    'template_interna_noticias,id_noticias=%s&id_sessoes=%s/' + \
                    'template_interna_noticias.shtml'
                urldestino = urldestino % (cols[0], cols[1])
                urlthumb = None
                tituloblog = None
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

                    #Corpo da noticia
                    corpoconteudo=corpoconteudo,

                    #Tags da noticia
                    tags=tags,

                    #Tags para efetuar o relacionamento do conteudo #fabricante, modelo, ano, fabmodano, fipe
                    tagsrelacionadas=tagsrelacionadas,

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

                    #Numero de comentarios do conteudo
                    qtdcomentarios=qtdcomentarios,

                    #Titulo do conteudo
                    titulo=titulo,

                    #Categoria do conteudo,
                    categoria=categoria,

                    #Resumo do conteudo
                    resumo=resumo,

                    #URL de destino do destino
                    urldestino=urldestino,

                    #URL thumb da noticia
                    urlthumb=urlthumb,

                    #Titulo do blog se for post
                    tituloblog=tituloblog,

                    #URL do autor no conteudo se existir
                    urlautor=urlautor
                )
    finally:
        f.close()
        #salva o xml gerado no disco o
        #parametro comments nao e obrigatorio caso passado como True
        # a classe gera um comentario nos elementos do xml

        xmlfile.write(
            'uai_vrum_noticia_'+
            datetime.datetime.now().strftime('%Y%m%d%H%M')+
        '.xml', comments=True)
    fim = datetime.datetime.now()
    print fim
    print (fim - inicio)

exportanoticias()





