# coding: utf-8
#
# Copyright 2009 Prima Tech Informatica Ltda.
#
# Licensed under the Environ License, Version 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.cmspublica.com.br/licenses/ENVIRON-LICENSE-1.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from publica import settings
from publica.utils.json import encode, decode
from publica.utils.decorators import dbconnectionapp, serialize, jsoncallback


class Public(object):

    """
        public class of methods of this content
    """
    @dbconnectionapp
    def _get_desabafo(self, limit=10, offset=0):
        """
        	Desabafo
        """
        lista = []
        for i in self.execSql("select_desabafo_limit",
                              limit=int(limit),
                              offset=int(offset)):
            lista.append(i)
            
        return {"itens":lista, "qtde":self.get_count()}

    @jsoncallback
    def get_desabafo(self, limit=10, offset=0):
        return self._get_desabafo(limit=limit, offset=offset)


    @dbconnectionapp
    def get_count(self):
        count = list(self.execSql("select_count_for_paginator"))[0]['count']
        return count
         
        

        

        

        