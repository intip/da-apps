##
from daSearch import pytojavascript, daSearch


urlfastserver = "http://fast2.estaminas.com.br:15100"
dasearch = daSearch(urlfastserver=urlfastserver)
resp = dasearch.search(site="vrum",
                       method="getmodelosmaisprocurados",
                       limit=20)

resp = pytojavascript(resp)
print resp
 
