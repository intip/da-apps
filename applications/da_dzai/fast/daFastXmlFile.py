# -*- coding: latin1 -*-
#-------------------------------------------------------------------------------
# @name:        daFastXmlFile.py
# @author:      Alexandre Villela <alexandrebrandao.mg@diariosassociados.com.br>
# @created:     26/10/2010
# @copyright:   (c) Diarrios Associados
# @licence:     GPL
# @version:     1.0
# @required:    http://effbot.org/zone/element-index.htm
#-------------------------------------------------------------------------------
import datetime

#opções da classe
optionsSiglaEstado = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT',
            'MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO',
            'RR','SC','SP','SE','TO']

class MyFile(object):
    def __init__(self, filename):
        self.file = open(filename, "wb")

    def write(self,text):
        self.file.write(text)

    def close(self):
        self.file.close();

class daFastXmlFile(object):

    def __init__(self, portal, origem, tipoconteudo, fields):
        self.portal = portal.lower()
        self.origem = origem.lower()
        self.tipoconteudo = tipoconteudo.lower()
        self.precontentid = "%s_%s_%s_" % (portal,origem,tipoconteudo)
        self._documents = []
        self._fields = fields
        self._contentids = []


    def add(self, contentid, **k):
        contentid = contentid.lower()
        if(contentid.find(self.precontentid)!=0):
            raise Exception('contentid nao correspode a class')
        if(contentid in self._contentids):
            import warnings
            warnings.warn('contentid: %s ja foi adicionado' % contentid)
            return False
            #raise Exception('contentid: %s ja foi adicionado' % contentid)
        self._contentids.append(contentid)
        document = {}
        for n in self._fields:
            p = n.keys()[0]
            val = k.get(p,None)
            #if(val!=None):
            document[p] = val
        document['contentid']=contentid
        document['portal']=self.portal
        document['origem']=self.origem
        document['tipoconteudo']=self.tipoconteudo
        self._documents.append(document)
        return True


    def write(self, file, encoding='us-ascii',
        xmltagfast = True, comments=False):
        from xml.etree import ElementTree as ET

        documents = ET.Element("ROWSET")
        ii = 0
        for d in self._documents:
            ii += 1
            document = ET.SubElement(documents, 'ROW')
            document.attrib["num"] = str(ii)
            for n in self._fields:
                p = n.keys()[0]
                pf = n.values()[0]
                #if(d.has_key(f) and (d[f]!=None)):
                if(d[p]!=None and d[p]!=''):
                    if(xmltagfast):
                        el = ET.SubElement(document, pf)
                        if(comments):
                            el.attrib["comments"] = p
                        text = d[p]
                        if(type(text) is float):
                            text = "%.2f" % text
                        elif(type(text) is int):
                            text = str(text)
                        text = text.replace(chr(30),' ')
                        text = text.replace(chr(13)+chr(10),' ')
                        text = text.replace(chr(13),' ')
                        text = text.replace(chr(10),' ')
                        el.text = text.strip()
                    else:
                        ET.SubElement(document, p).text = d[p]
        mfile = file
        if not hasattr(file, "write"):
            mfile = MyFile(file)
        ET.ElementTree(documents).write(file=mfile, encoding=encoding)
        mfile.close()


    def getCapitalizeNameComplet(self, s, isnull=False):
        if((isnull) and (s==None)): return None
        ignoreword = ['a','o','e','da','de','di','do','du','das','dos','dus']
        r = []
        try: s = s.decode('iso-8859-1')
        except:pass
        try: s = s.lower()
        except:pass
        try: s = s.encode('iso-8859-1')
        except:pass
        for i in s.split(' '):
            if(i in ignoreword):
                r.append(i)
            else:
                r.append(i.capitalize())
        return ' '.join(r)


    def getOpcoes(self, s, opcoes=[], isnull=False,
        capitalize=False, upper=False):
        if((isnull) and (s==None)): return None
        import warnings

        try: s = s.decode('iso-8859-1')
        except:pass
        try: s = s.lower()
        except:pass
        try: s = s.encode('iso-8859-1')
        except:pass
        if(capitalize):
            s = s.capitalize()

        if(upper):
            if (not s.isupper()):
                warnings.warn("Opção passada(%s) deve vir sempre em maiusculo" %
                s
                )
            try: s = s.decode('iso-8859-1')
            except:pass
            try: s = s.upper()
            except:pass
            try: s = s.encode('iso-8859-1')
            except:pass
        if(opcoes!=None):
            if((type(opcoes) is list) and (not s in opcoes)):
                raise Exception('Opcoes nao cadastrado: %s validas: %s'
                    % (s,str(opcoes)))
            elif(type(opcoes) is dict):
                if(not s in opcoes.keys()):
                    raise Exception('Opcoes nao cadastrado: %s validas: %s'
                    % (s,str(opcoes)))
                else:
                    s = opcoes[s]
        return s


    def getFormatacao(self, s, mask, isnull=False):
        if((isnull) and (s==None)): return None
        if(len(s)!=len(mask)):
            raise Exception('Formatacao do valor invalido' % s)
        for i in xrange(0,len(mask)):
            if(mask[i]=='d'):
                if(not(s[i].isdigit())):
                    raise Exception('Formatacao do valor invalido' % s)
            elif(mask[i]!=s[i]):
                raise Exception('Formatacao do valor invalido' % s)
        return s


    def getDtFrm(self, s):
        import datetime
        if(s):
            if(type(s) is datetime.datetime):
                return datetime.datetime.strftime(s,'%Y-%m-%dT%H:%M:%S')
            try:
                s = s[:19]
                datetime.datetime.strptime(s,'%Y-%m-%dT%H:%M:%S')
                return s
            except:
                try:
                    dt = datetime.datetime.strptime(s,'%Y-%m-%d')
                    return datetime.datetime.strftime(dt,'%Y-%m-%dT%H:%M:%S')
                except:
                    dt=datetime.datetime.strptime(s,'%Y-%m-%d %H:%M:%S')
                    return datetime.datetime.strftime(dt,'%Y-%m-%dT%H:%M:%S')

        else:
            return None


    def getSeparetor(self, s, separator='#', capitalize=False):
        import warnings
        if(s):
            r = []
            for e in s.strip().split(separator):
                if(e):
                    if(capitalize):
                        r.append(self.getCapitalizeNameComplet(e))
                    else:
                        r.append(e)
            if((s.find(' ')>-1) and (s.find(separator)==-1)):
                warnings.warn(
                    message = "SEPARADOR PARA O CAMPO NAO ENCONTRADO " + \
                    "VERIFIQUE SE O CAMPO ESTA SENDO ALIMENTADO CORRETAMENTE",
                    )
            return separator.join(r)
        else:
            return None


    def getStatus(self, s, isnull=False):
        if((isnull) and (s==None)): return None
        if(not int(s) in [0,1]):
            raise Exception('Campo status nao e valido [0 ou 1]')
        return s


    def getFloat(self, s, isnull=False, pmin=None, pmax=None):
        if((isnull) and (s==None)): return None
        i = float(s)
        if((pmin!=None) and i<pmin):
            s = None
            if(not(isnull)):
                raise Exception('valor menor do que o esperado')
        if((pmax!=None) and i>pmax):
            s = None
            if(not(isnull)):
                raise Exception('valor maior do que o esperado')
        return s


    def getInt(self, s, isnull=False, pmin=None, pmax=None):
        if((isnull) and (s==None)): return None
        if type(s) is str: s = s.replace('.','')
        try: int(s)
        except:
            if(isnull):
                return None
        return self.getFloat(str(int(s)), isnull, pmin, pmax)


    def getDados(self, separator='|', **kargs):
        if len(kargs.keys())==0: return None
        l = []
        for k,v in kargs.iteritems():
            if(v!=None):
                v = v.replace(separator,' ')
                if(type(v) is unicode):
                    v = v.encode('latin1','replace')
                l.append("%s:%s" %(k, v.replace(separator,' ')))
        if(not(l)):
            return None
        else:
            return separator + separator.join(l) + separator


    def getBitmap(self, *args, **kargs):
        resp = ''
        for i in xrange(0,kargs['numelements']):
            v = args[i]
            resp += str(self.getInt(v,pmin=0,pmax=1))
        return resp


    def getSiglaEstado(self, s, isnull=False):
        return self.getOpcoes(s,opcoes=optionsSiglaEstado, isnull=isnull,
            capitalize=False, upper=True)

if __name__ == '__main__':
    e = daFastXmlFile(
        portal='uai', origem='vrum', tipoconteudo='noticia',
        fields = [
            {'contentid':'datasourcereference'},
            {'portal':'strclassifier36'},
            {'origem':'strclassifier27'},
            {'tipoconteudo':'strclassifier34'},
            {'dataexpiracao':'date1'},
            {'statusativacao':'intaggregate14'},
            {'datainsercao':'date2'},
            {'secao':'strclassifier33'},
            {'dados1':'bodypart1'},
            {'datapublicacao':'date3'},
            {'dataranking':'date4'},
            {'ranking':'intaggregate17'},
            {'qtdestrelas':'intaggregate13'},
            {'dados2':'bodypart2'},
            {'statusinterno':'intaggregate10'},
            {'corpoconteudo':'straggregate3'},
            {'tags':'strclassifier28'},
            {'autor':'strclassifier1'},
            {'statusmidiavisivel':'intaggredate15'}
        ])
    e.add(
            contentid = 'uai_vrum_noticia_1000',
            dataexpiracao = None,
            statusativacao = '1'
        )
    e.write('uai_vrum_noticia_20100826.xml')
    if(e.getDtFrm('2010-01-28 10:20:30')!='2010-01-28T10:20:30'):
        raise Exception('problema na funcao: getDtFrm')
    if(e.getDtFrm('2011-02-28T11:21:31')!='2011-02-28T11:21:31'):
        raise Exception('problema na funcao: getDtFrm')
    if(e.getSeparetor('Ola#Mundo#','#')!='Ola#Mundo'):
        raise Exception('problema na funcao: getSeparetor')
    if(e.getSeparetor('Ola//Mundo//','//')!='Ola//Mundo'):
        raise Exception('problema na funcao: getSeparetor')
    if(e.getDados(
        separator='$',
        titulo='ola mundo | cao: ',
        autor='slex luthor')!='$autor:slex luthor$titulo:ola mundo | cao: $'):
        raise Exception('problema na funcao: getDados')
    if(e.getDados(
        titulo='ola mundo | cao: ',
        autor='slex luthor')!='|autor:slex luthor|titulo:ola mundo   cao: |'):
        raise Exception('problema na funcao: getDados')
    if(e.getDados()!=None):
        raise Exception('problema na funcao: getDados')

    #print e.getBitmap(1,1,0,numelements=3)
    #print e.getSeparetor(None,'#',True)
##    print e.getOpcoes(
##        None,
##        opcoes=['Automatico','Manual'],
##        isnull=True,
##        capitalize=True)
    print e.getFormatacao('006000-7',mask='dddddd-d',isnull=False)
