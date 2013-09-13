# -*- encoding: LATIN1 -*-
#
# Copyright 2008 Intip.
#
# Licensed under the Environ License, Version 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.intip.com.br/licenses/ENVIRON-LICENSE-1.0
#
# Unless required by appwadlicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#import re
#import datetime
from publica.utils.json import encode, decode
#from environ.conf import settings #from publicadm import settings
import httplib #cb
import xml.dom.minidom #cb
from publica.utils.decorators import dbconnectionapp, serialize, jsoncallback

globalToken = None
globalToken2 = None

class Site(object):
    """
    """

    #inicio: funcoes usadas para o conversor de moedas do correio braziliense
    def getToken(self):
        global globalToken
        code, msg, headers, data = self.sendCmd(
        host = 'api.rkd.reuters.com',
        path = '/api/2006/05/01/TokenManagement_1.svc/Anonymous',
        soapaction = 'CreateServiceToken_1',
        xml = """<Envelope xmlns="http://www.w3.org/2003/05/soap-envelope">
            <Header>
            <To xmlns="http://www.w3.org/2005/08/addressing">http://api.rkd.reuters.com/api/2006/05/01/TokenManagement_1.svc/Anonymous</To>
            <MessageID xmlns="http://www.w3.org/2005/08/addressing">2357468716598</MessageID>
            <Action xmlns="http://www.w3.org/2005/08/addressing">http://www.reuters.com/ns/2006/05/01/webservices/rkd/TokenManagement_1/CreateServiceToken_1</Action>
            </Header>
            <Body>
            <CreateServiceToken_Request_1 xmlns:global="http://www.reuters.com/ns/2006/05/01/webservices/rkd/Common_1" xmlns="http://www.reuters.com/ns/2006/05/01/webservices/rkd/TokenManagement_1">
            <ApplicationID xmlns="http://www.reuters.com/ns/2006/05/01/webservices/rkd/Common_1">AnadubeuxDfDabrComBr</ApplicationID>
            <Username>anadubeux.df@dabr.com.br</Username>
            <Password>reuters</Password>
            </CreateServiceToken_Request_1>
            </Body>
            </Envelope>""",
        https=True)

        if(code==200):
            globalToken,pointEnd = self.getTag(data,'<global:Token>','</global:Token>')

    def getImpToken(self):
        global globalToken2
        code, msg, headers, data = self.sendCmd(
        host = 'api.rkd.reuters.com',
        path = '/api/2006/05/01/TokenManagement_1.svc',
        soapaction = 'CreateImpersonationToken_1',
        xml = """<Envelope xmlns="http://www.w3.org/2003/05/soap-envelope">
            <Header>
            <To xmlns="http://www.w3.org/2005/08/addressing">https://api.rkd.reuters.com/api/2006/05/01/TokenManagement_1.svc</To>
            <MessageID xmlns="http://www.w3.org/2005/08/addressing">2357468716598</MessageID>
            <Action xmlns="http://www.w3.org/2005/08/addressing">http://www.reuters.com/ns/2006/05/01/webservices/rkd/TokenManagement_1/CreateImpersonationToken_1</Action>
            <Authorization xmlns="http://www.reuters.com/ns/2006/05/01/webservices/rkd/Common_1">
            <ApplicationID>AnadubeuxDfDabrComBr</ApplicationID>
            <Token>""" + globalToken + """</Token></Authorization>
            </Header>
            <Body>
            <CreateImpersonationToken_Request_1 xmlns="http://www.reuters.com/ns/2006/05/01/webservices/rkd/TokenManagement_1">
            <EffectiveUsername>anadubeux.df@dabr.com.br</EffectiveUsername>
            </CreateImpersonationToken_Request_1>
            </Body>
            </Envelope>""",
        https=True)

        if(code==200):
            globalToken2,pointEnd = self.getTag(data,'<global:Token>','</global:Token>')

    def getSession(self):
        global globalToken2
        self.getToken()
        self.getImpToken()
        if (globalToken2 == None):
            return 'erro'
        return globalToken2

    def getQuotes(self, requestKey):
        global globalToken2
        global data

        xml = """<Envelope xmlns="http://www.w3.org/2003/05/soap-envelope">
            <Header>
            <To xmlns="http://www.w3.org/2005/08/addressing">http://api.rkd.reuters.com/api/2006/05/01/Quotes_1.svc</To>
            <MessageID xmlns="http://www.w3.org/2005/08/addressing">12345678</MessageID>
            <Action xmlns="http://www.w3.org/2005/08/addressing">http://www.reuters.com/ns/2006/05/01/webservices/rkd/Quotes_1/RetrieveItem_2</Action>
            <Authorization xmlns="http://www.reuters.com/ns/2006/05/01/webservices/rkd/Common_1">
            <ApplicationID>AnadubeuxDfDabrComBr</ApplicationID>
            <Token>""" + str(globalToken2) + """</Token>
            </Authorization>
            </Header>
            <Body>
            <RetrieveItem_Request_2 xmlns="http://www.reuters.com/ns/2006/05/01/webservices/rkd/Quotes_1">
            <ItemRequest Scope="All" >
            <RequestKey Name=""" + '"' + str(requestKey) + '"' + """ />
            </ItemRequest>
            </RetrieveItem_Request_2>
            </Body>
            </Envelope>"""

        code, msg, headers, data = self.sendCmd(
        host = 'api.rkd.reuters.com',
        path = '/api/2006/05/01/Quotes_1.svc',
        soapaction = 'RetrieveItem_Request_2',
        xml =xml
        ,https=False)
        return data

    @jsoncallback
    def converte(self, de, para, valor, environment=None, request={}):

        try:
            url                 = 'http://ri2.rois.com/'
            session_id          = self.getSession()
            modulo              = 'CTIB/'
            funcao              = 'RI3APISNAP'
            formato             = '&ENCODING=ISO-8859-1&FORMAT=XML'

            nome_moeda          = self.get_nomeMoeda(para)
            valor               = valor.replace(",",".")

            if ( de != "USD" and para != "USD" ) or (de == "USD" and  para == "EUR" ) :

                ric             = str(de)+str(para)+"=X"
                moeda           = self.getQuotes(ric)
                doc             = xml.dom.minidom.parseString(moeda)
                #vl              = le_xml(doc).encode('latin1')
                vl              = self.le_xml(doc)
                resultado       = float(valor)* float(vl)


            elif  ((de == "EUR" and  para == "USD") or (de == "GBP" and  para == "USD" ) ) :

                ric             = str(de)+"=X"
                moeda           = self.getQuotes(ric)
                doc             = xml.dom.minidom.parseString(moeda)
                vl               = self.le_xml(doc).encode('latin1')
                resultado       = float(valor)* float(vl)

            elif  (de == "USD" and  para == "NZD" ) :

                de                  = de+"=X"
                para                = para+"=X"

                moeda_de            = self.getQuotes(de)
                moeda_para          = self.getQuotes(para)
                doc                 = xml.dom.minidom.parseString(moeda_de)
                vl_dolar_de         = self.le_xml(doc).encode('latin1')
                doc                 = xml.dom.minidom.parseString(moeda_para)
                vl_dolar_para       = self.le_xml(doc).encode('latin1')

                resultado           =  round(float(valor)*(float(vl_dolar_para)),2)

            else:

                de                  = de+"=X"
                para                = para+"=X"

                moeda_de            = self.getQuotes(de)
                moeda_para          = self.getQuotes(para)
                doc                 = xml.dom.minidom.parseString(moeda_de)
                vl_dolar_de         = self.le_xml(doc).encode('latin1')
                doc                 = xml.dom.minidom.parseString(moeda_para)
                vl_dolar_para       = self.le_xml(doc).encode('latin1')

                resultado           =  round(float(valor)*(float(vl_dolar_para) /  float(vl_dolar_de)),2)

            if(resultado):
                resultado           =  str(resultado)+" "
            if(nome_moeda):
                resultado           +=  str(nome_moeda)
            return resultado, None
        except Exception, e:
            import traceback as t
            e = 'except in tvpublisher ' + chr(13)+ chr(10) + str(e) + str(t.format_exc())
            return str(e)

    def le_xml(self, doc):
        try:
            asd = doc.getElementsByTagName('omm:Field')
            for a in asd:

                value = a.getAttribute('Name')
                if value == 'CF_LAST':
                    return  self.getText(a.childNodes)
        except Exception, e:
            import traceback as t
            e = 'except in tvpublisher ' + chr(13)+ chr(10) + str(e) + str(t.format_exc())
            return str(e)

    def getText(self, nodelist):
        try:
            rc = ""
            rc += nodelist[0].firstChild.data
            return rc
        except Exception, e:
            import traceback as t
            e = 'except in tvpublisher ' + chr(13)+ chr(10) + str(e) + str(t.format_exc())
            return str(e)


    def get_nomeMoeda(self, ric):
        try:
            pais=""
            if ric == "BRL":
                pais="Brasil"
                return "Reais"

            if ric == "USD":
                pais="Estados Unidos"
                return "Dolar"


            if ric =="ZAR":
                pais="?frica do Sul"
                return "Rands"

            if ric =="DZD":
                pais="Arg?lia"
                return "Dinar"

            if ric =="SAR":
                pais="Ar?bia Saudita"
                return "Rial"

            if ric =="ARS":
                pais="Argentina"
                return "Pesos"

            if ric =="AUD":
                pais="Austr?lia"
                return "Dolar"

            if ric =="BDT":
                pais="Bangladesh"
                return "Tecas"

            if ric =="BYR":
                pais="Belarus"
                return "Rublo"

            if ric =="BGN":
                pais="Bulg?ria"
                return "Lev"

            if ric =="CAD":
                pais="Canad?"
                return "Dolar"

            if ric =="KZT":
                pais="Cazaquist?o"
                return "Tenge"

            if ric =="SGD":
                pais="Cingapura"
                return "Dolar"

            if ric =="CLP":
                pais="Chile"
                return "Peso"

            if ric =="CNY":
                pais="China"
                return "Yuan"

            if ric =="COP":
                pais="Colombia"
                return "Peso"

            if ric =="KRW":
                pais="Cor?ia do Sul"
                return "Won"

            if ric =="HRK":
                pais="Cro?cia"
                return "Kuna"

            if ric =="DKK":
                pais="Dinamarca"
                return "Coroa"

            if ric =="EGP":
                pais="Egito"
                return "Libra"

            if ric =="SKK":
                pais="Eslov?quia"
                return "Coroa"

            if ric =="SIT":
                pais="Eslov?nia"
                return "Tolar"

            if ric =="EEK":
                pais="Est?nia"
                return "Coroa"

            if ric =="EUR":
                pais="Europa"
                return "Euros"

            if ric =="PHP":
                pais="Filipinas"
                return "Peso"

            if ric =="ISK":
                pais="Groenl?ndia"
                return "Coroa"

            if ric =="HKD":
                pais="Hong Kong"
                return "Dolar"

            if ric =="HUF":
                pais="Hungria"
                return "Florim"

            if ric =="INR":
                pais="?ndia"
                return "Rupia"

            if ric =="IDR":
                pais="Indon?sia"
                return "Rupia"

            if ric =="IRR":
                pais="Ir?"
                return "Rial"

            if ric =="ILS":
                pais="Israel"
                return "Shekel"

            if ric =="JPY":
                pais="Jap?o"
                return "Iene"

            if ric =="JOD":
                pais="Jord?nia"
                return "Dinar"

            if ric =="KWD":
                pais="Kuait"
                return "Dinar"

            if ric =="LAK":
                pais="Laos"
                return "Kip"

            if ric =="LVL":
                pais="Let?nia"
                return "Lat"

            if ric =="LBP":
                pais="L?bano"
                return "Libra"

            if ric =="LYD":
                pais="L?bia"
                return "Dinar"

            if ric =="LTL":
                pais="Litu?nia"
                return "Litas"

            if ric =="MYR":
                pais="Mal?sia"
                return "Ringgit"

            if ric =="MTL":
                pai="Malta"
                return "Lira"

            if ric =="MAD":
                pais="Marrocos"
                return "Dirham"

            if ric =="MXN":
                pais="M?xico"
                return "Pesos"

            if ric =="MDL":
                pais="Moldova"
                return "Leu"

            if ric =="NAD":
                pais="Nam?bia"
                return "Dolar"

            if ric =="NIO":
                pais="Nicar?gua"
                return "Cordoba"

            if ric =="NOK":
                pais="Noruega"
                return "Coroa"

            if ric =="NZD":
                pais="Nova Zel?ndia"
                return "Dolar"

            if ric =="PKR":
                pais="Paquist?o"
                return "Rupia"

            if ric =="PYG":
                pais="Paraguai"
                return "Guaranis"

            if ric =="PEN":
                pais="Peru"
                return "Sol novo"

            if ric =="PLN":
                pais="Pol?nia"
                return "Zloty"

            if ric =="QAR":
                pai="Qatar"
                return "Rial"

            if ric =="KES":
                pais="Qu?nia"
                return "Xelim"

            if ric =="GBP":
                pais="Reino Unido"
                return "Libra"

            if ric =="CZK":
                pais="Rep?blica Tcheca"
                return "Tcheca"

            if ric =="RON":
                pais="Rom?nia"
                return "Leu"

            if ric =="RUB":
                pais="R?ssia"
                return "Rublo"

            if ric =="SYP":
                pais="libra s?ria"
                return "Libras"

            if ric =="LKR":
                pais="Sri Lanka"
                return "Rupia"

            if ric =="SEK":
                pais="Su?cia"
                return "Coroa"

            if ric =="CHF":
                pais="Su??a"
                return "Franco su??o"

            if ric =="THB":
                pais="Tail?ndia"
                return "Baht"

            if ric =="TWD":
                pais="Taiwan"
                return "Dolar"

            if ric =="TND":
                pais="Tun?sia"
                return "Dinar"

            if ric =="TRY":
                pais="Turquia"
                return "Lira"

            if ric =="UAH":
                pais="Ucr?nia"
                return "Hrivna"

            if ric =="UYU":
                pais="Uruguai"
                return "Peso"

            if ric =="ZWD":
                pais="Zimb?bue"
                return "Dolar"
        except Exception, e:
            import traceback as t
            e = 'except in tvpublisher ' + chr(13)+ chr(10) + str(e) + str(t.format_exc())
            return str(e)

    def getTag(self, s,TagBegin,TagEnd,start=0):
        pointBegin = s.find(TagBegin,start)
        if(pointBegin>-1):
            pointEnd = s.find(TagEnd,pointBegin)
            if(pointEnd>-1):
                return s[pointBegin+len(TagBegin):pointEnd], pointEnd+len(TagEnd)

    def SOAPUserAgent(self):
        return "SOAPpy " + " (pywebsvcs.sf.net)" #+ __version__

    def sendCmd(self, host, path, soapaction, xml, https=False, encoding = 'UTF-8'):
        real_addr = host#'api.rkd.reuters.com'
        addr_host = host#'api.rkd.reuters.com'
        real_path = path#'/api/2006/05/01/TokenManagement_1.svc/Anonymous'
        encoding = 'UTF-8'
        t = 'application/soap+xml'
        data = xml
        if(https):
            r = httplib.HTTPS(real_addr)
        else:
            r = httplib.HTTP(real_addr)
        r.putrequest("POST", real_path)
        r.putheader("Host", addr_host)
        r.putheader("User-agent", self.SOAPUserAgent())
        if encoding != None:
            t += '; charset="%s"' % encoding
        r.putheader("Content-type", t)
        r.putheader("Content-length", str(len(data)))
        r.putheader("SOAPAction", '"%s"' % soapaction)
        r.endheaders()
        r.send(data)
        code, msg, headers = r.getreply()
        if headers:
            content_type = headers.get("content-type","text/xml")
            content_length = headers.get("Content-length")
        else:
            content_type=None
            content_length=None
        if content_length:
            comma=content_length.find(',')
            if comma>0:
                content_length = content_length[:comma]
        try:
            message_len = int(content_length)
        except:
            message_len = -1

        if message_len < 0:
            data = r.getfile().read()
            message_len = len(data)
        else:
            data = r.getfile().read(message_len)
        return code, msg, headers, data

    #fim: funcoes usadas para o conversor de moedas do correio braziliense
