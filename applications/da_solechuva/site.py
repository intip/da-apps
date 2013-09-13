# -*- coding:iso8859-1 -*-
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
from time import strftime, strptime
from publica import settings
from publica.core.portal import Portal
from publica.admin.exchange import getDadosSite
from publica.utils.json import encode, decode
from publica.utils.decorators import dbconnectionapp, serialize, jsoncallback


class Site(object):
    """
    """
    
    @dbconnectionapp
    def _listPrevisao(self, cidade, data=None, limit=1):
        """
        """
        if not cidade:
            return []

        try:
            data = strptime(data, "%d/%m/%Y")
            data = strftime("%Y-%m-%d", data)
        except:
           data = strftime("%Y-%m-%d")

        return self.execSql("select_previsao",
                            cidade=cidade,
                            data=data,
                            limit=int(limit))
