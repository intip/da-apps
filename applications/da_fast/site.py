# -*- encoding: LATIN1 -*-
#
# Copyright 2009 Prima Tech.
#
# Licensed under the Environ License, Version 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.intip.com.br/licenses/ENVIRON-LICENSE-1.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from publica.core.portal import Portal
from fast.daSearch import pytojavascript, daSearch

class Site(object):
    """
    """

    def _getDados(self):
        """
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        dados = portal._getApp(env_site=self.id_site,
                               schema=self.schema)
        return dados["dados"]


    def _getDadosFast(self, **kargs):
        """
        """
        dados = self._getDados() 
        urlfastserver = dados["url"]
        dasearch = daSearch(urlfastserver=urlfastserver)
        resp = dasearch.search(**kargs)
        return resp
        #return pytojavascript(resp)
