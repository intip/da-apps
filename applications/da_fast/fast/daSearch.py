# -*- coding: latin1 -*-
#-------------------------------------------------------------------------------
# @name:
# @purpose:
# @author:      SleX - slex@slex.com.br
# @created:     15/09/2010
# @copyright:   (c) Diarrios Associados
# @licence:     GPL
# @version:     1.0 SIMPLE CLIENT
#-------------------------------------------------------------------------------
import sys
import os
PATH = os.path.dirname(__file__) # /home/storage/vrum/ad-hoc/fast/mod
PATH = "/".join( PATH.split("/")[:-1] )
sys.path.append(PATH)

class daSearch(object):
    def __init__(self, urlfastserver):
        self.urlfastserver = urlfastserver
    def search(self, site, method, **k):
        import datetime
        import urllib
        urlfastserver = self.urlfastserver.replace(':15100','')+'/dasearch'
        params = '?site='+site
        params +='&method='+method
        k['dataType'] = 'python'
        if(k.has_key('i')): k.pop('i')
        #for c,v in k.iteritems():
        #    if(v):
        #        params += '&' + c + '=' + str(v)
        for c,v in k.iteritems():
            if(v):
                if((type(v) is list)):
                    for i in v:
                        params += '&' + c + '=' + str(i)
                else:
                    params += '&' + c + '=' + str(v)

        resp = urllib.urlopen(urlfastserver+params).read()
        return eval(resp)
    
def dasearch(urlfastserver, site, method, **k):
     return daSearch(urlfastserver).search(site=site, method=method,**k)

def pytojavascript(v,utf8=False,n=0,identado=False):
    import datetime
    r = ''
    if(type(v) is list):
        rr = []
        for i in v:
            iss = ''
            if(identado):iss += ''.rjust(n)
            iss += pytojavascript(i,utf8,n+2,identado)
            rr.append(iss)
        r += '['
        if(identado):
            if(rr):r += '\n'
            r += ',\n'.join(rr)
        else:
            r += ','.join(rr)
        r += ']'
    elif(type(v) is dict):
        lnum = len(v.keys())
        r = ''
        #print n
        an=0
        if(n>=4):an=n/2
        if(n>=6):an=n/4
        if(identado):r += (''.rjust(an))
        r +='{'
        if(identado):
            if(lnum>1): r +='\n'
        pr = 0
        rrs = []
        for k,i in v.iteritems():
            raux = ''
            pr += 1
            if(identado):
                if(lnum>1):# and (pr!=1):
                    raux += ''.rjust(n + 2)
            try:
                raux += "'"+str(k)+"':"+pytojavascript(i,utf8,n+2,identado)
                rrs.append(raux)
            except:
                raise str(r)
        if(identado):
            r += ',\n'.join(rrs)
        else:
            r += ','.join(rrs)
        if(identado):
            if(lnum>1):
                r += '\n'
                r += (''.rjust(n))
        r += '}'
    elif((type(v) is datetime.time) or ((type(v) is datetime.datetime))):
        r += v.strftime('new Date(%Y, %m - 1, %d, %H, %M, %S, 0)')
    elif(v == None):
        r += 'null'
    elif(type(v) is int):
        r += "%d" % v
    elif(type(v) is float):
        r += "%f" % v
    elif(type(v) is bool):
        if(v): r += 'true'
        else: r += 'false'
    elif(type(v) is str):
        if(utf8):
            v = v.decode('utf-8')
        r += "'%s'" % v.replace("'","\\'").replace('\n','\\n').replace('\r','\\r')
    else:
        raise 'tipo: %s nao esperado \n valor %s'+ (str(type(v)),str(v))
    return str(r)

if __name__ == '__main__':
    import datetime
    #print pytojavascript(v={'nome':'slex','lis':[{'a':'1','b':'2'},{'a':'1','b':'2'}]})
    resps = dasearch(
            urlfastserver = 'http://fast2.estaminas.com.br:15100',
            site = 'vrum',
            method = 'busca',
            limit = 0,
            offset = 1,
            navigation_enabled = '1',
            i = '1',
            #s = 'fiat',
            #sortby='random',
            filters = [
                #'strclassifier8:em',                            #origem
                #'strclassifier7:fichatecnica',                 #tipoconteudo
                #recall
                #'strclassifier1:"Sandro Barnabe"',             #autor
            ],
            #conteudo = 'fichatecnica,topicoforum,noticia'
            conteudo = 'anuncio'
##            conteudo = [
##                #'noticia', #'recall',
##                #'video',
##                #'foto',
##                #'anuncio',
##                #'fichatecnica',
##
##                #'topicoforum',
##                #'oficina',
##                #'revenda'
##            ]
##            query = 'or('+ \
##            'strclassifier7:fichatecnica,'+
##            'strclassifier7:recall,'+
##            'strclassifier7:topicoforum,'+
##            'strclassifier7:noticia,'+
##
##            'strclassifier7:video,'+
##            'strclassifier7:foto,'+
##
##            'strclassifier7:anuncio,'+
##
##            'strclassifier7:oficina,'+
##            'strclassifier7:revenda,'+
##
##            ')',
        )
    resp = resps[0]
    respx = resps[1]
    print '\nResultados (%s)' % str(len(resp['rec']))
    print '\nResultados (%s)' % str(resp['cnt'])
    print '\nNavegadores'
    for i in resp['nav']:
        print i['d'] + ' | ' + i['m'] + ' | ' + i['n'] + ' (%s)' % str(len(i['v']))
        for y in i['v']:
            print '\t' + str(y)
    print '\n------------------------------------------------------------------'
    print '\nResultados (%s)' % str(len(respx['rec']))
    print '\nResultados (%s)' % str(respx['cnt'])
    print '\nNavegadores'
    for i in respx['nav']:
        print i['d'] + ' | ' + i['m'] + ' | ' + i['n'] + ' (%s)' % str(len(i['v']))
        for y in i['v']:
            print '\t' + str(y)

    #resp = pytojavascript(resp,identado='1')
    #print resp
##    #resp = pytojavascript(resp)
##    print resp
